"""AI part 1: learn the evolutionary rules from many independent lineages.

We only observe end states (organelle / nucleus / lost) of the same ancestral genes in
several lineages (e.g. animals, plants, jakobids, apicomplexans). Ignoring pathway
coupling, each gene is an independent two-way competing-risk process with integrated
hazards kT, kL, so its end-state probabilities have a closed form:

    P(organelle) = exp(-(kT + kL))
    P(nucleus)   = kT / (kT + kL) * (1 - P(organelle))
    P(lost)      = kL / (kT + kL) * (1 - P(organelle))

with log kT = a_T[lineage] + x @ w_T and log kL = a_L[lineage] + x @ w_L.
The shared weights w are the "laws"; a_T, a_L absorb each lineage's pressure x time
(and the rule biases, which are not separately identifiable).

Real organelle genomes usually only tell us whether a gene is still in the organelle,
not whether a missing gene moved to the nucleus or vanished. For that case
`fit_retention` fits the single combined hazard K = kT + kL:
P(retained) = exp(-exp(a[lineage] + x @ w)).
"""

from dataclasses import dataclass

import numpy as np
import torch

from .simulator import Rules


def end_state_log_probs(log_kt: torch.Tensor, log_kl: torch.Tensor) -> torch.Tensor:
    """Log P(state) for the competing-risk model, stacked on the last axis."""
    log_k = torch.logaddexp(log_kt, log_kl)
    k = log_k.exp()
    log_p_any = torch.log(-torch.expm1(-k).clamp_max(-1e-12))
    return torch.stack([-k, log_kt - log_k + log_p_any, log_kl - log_k + log_p_any], dim=-1)


def retention_log_probs(log_k: torch.Tensor) -> torch.Tensor:
    """Log P(retained), log P(gone) under a single integrated hazard."""
    k = log_k.exp()
    return torch.stack([-k, torch.log(-torch.expm1(-k).clamp_max(-1e-12))], dim=-1)


@dataclass
class FittedRules:
    transfer_weights: np.ndarray
    loss_weights: np.ndarray
    lineage_log_transfer: np.ndarray
    lineage_log_loss: np.ndarray
    final_nll: float
    transfer_se: np.ndarray | None = None
    loss_se: np.ndarray | None = None

    def to_rules(self) -> Rules:
        """Rules with biases folded into the lineage offsets (bias = 0)."""
        return Rules(0.0, tuple(self.transfer_weights), 0.0, tuple(self.loss_weights))


def _optimise(params, closure, epochs, lr):
    opt = torch.optim.Adam(params, lr=lr)
    for _ in range(epochs):
        opt.zero_grad()
        loss = closure()
        loss.backward()
        opt.step()


def fit_rules(
    features: np.ndarray,
    states: np.ndarray,
    *,
    epochs: int = 1500,
    lr: float = 0.05,
    l2: float = 1e-4,
    seed: int = 0,
) -> FittedRules:
    """Maximum-likelihood fit. features: (G, F); states: (L, G) ints."""
    torch.manual_seed(seed)
    x = torch.as_tensor(features, dtype=torch.float64)
    y = torch.as_tensor(states, dtype=torch.long)
    n_lineages, n_features = y.shape[0], x.shape[1]

    w_t = torch.zeros(n_features, dtype=torch.float64, requires_grad=True)
    w_l = torch.zeros(n_features, dtype=torch.float64, requires_grad=True)
    a_t = torch.zeros(n_lineages, 1, dtype=torch.float64, requires_grad=True)
    a_l = torch.zeros(n_lineages, 1, dtype=torch.float64, requires_grad=True)
    nll = None

    def closure():
        nonlocal nll
        log_p = end_state_log_probs(a_t + x @ w_t, a_l + x @ w_l)
        nll = -log_p.gather(-1, y.unsqueeze(-1)).mean()
        return nll + l2 * (w_t.square().sum() + w_l.square().sum())

    _optimise([w_t, w_l, a_t, a_l], closure, epochs, lr)
    return FittedRules(
        transfer_weights=w_t.detach().numpy().copy(),
        loss_weights=w_l.detach().numpy().copy(),
        lineage_log_transfer=a_t.detach().numpy().ravel(),
        lineage_log_loss=a_l.detach().numpy().ravel(),
        final_nll=float(nll.detach()),
    )


def fit_rules_bootstrap(
    features: np.ndarray, states: np.ndarray, *, n_boot: int = 20, seed: int = 0, **kwargs
) -> FittedRules:
    """Point estimate plus standard errors from resampling lineages."""
    fitted = fit_rules(features, states, seed=seed, **kwargs)
    rng = np.random.default_rng(seed)
    boots_t, boots_l = [], []
    for b in range(n_boot):
        idx = rng.integers(0, len(states), len(states))
        f = fit_rules(features, states[idx], seed=seed + b + 1, **kwargs)
        boots_t.append(f.transfer_weights)
        boots_l.append(f.loss_weights)
    fitted.transfer_se = np.std(boots_t, axis=0)
    fitted.loss_se = np.std(boots_l, axis=0)
    return fitted


# ---------------------------------------------------------------------------------
# Presence/absence ("retention") model, used for real genomes.
# ---------------------------------------------------------------------------------


@dataclass
class RetentionLaw:
    """log hazard of leaving the organelle = a[lineage] + x @ weights[group]."""

    weights: np.ndarray  # (n_groups, F)
    lineage_offsets: list[np.ndarray]  # per block, (L_b,)
    final_nll: float
    weights_se: np.ndarray | None = None

    def log_hazard(self, features: np.ndarray, offset: float, group: int = 0) -> np.ndarray:
        return offset + features @ self.weights[group]

    def p_retained(self, features: np.ndarray, offset: float, group: int = 0) -> np.ndarray:
        return np.exp(-np.exp(self.log_hazard(features, offset, group)))


def fit_retention(
    blocks: list[tuple[np.ndarray, np.ndarray]],
    *,
    groups: list[int] | None = None,
    epochs: int = 1500,
    lr: float = 0.05,
    prior_sd: float = 2.0,
    seed: int = 0,
) -> RetentionLaw:
    """Fit retention laws to one or more gene-content blocks.

    Each block is (features (G_b, F), present (L_b, G_b) bool) — e.g. one per system
    (mitochondria, plastids, endosymbionts), with its own gene universe. `groups[b]`
    says which law block b obeys: all zeros = one universal law shared by every
    system; 0..B-1 = a separate law per system. Weights get a N(0, prior_sd^2) prior,
    so shrinkage does not grow with the number of genes.
    """
    torch.manual_seed(seed)
    groups = [0] * len(blocks) if groups is None else list(groups)
    n_features = blocks[0][0].shape[1]
    w = torch.zeros(max(groups) + 1, n_features, dtype=torch.float64, requires_grad=True)
    data, offsets = [], []
    for x, present in blocks:
        data.append((torch.as_tensor(x, dtype=torch.float64), torch.as_tensor(~present, dtype=torch.long)))
        offsets.append(torch.zeros(len(present), 1, dtype=torch.float64, requires_grad=True))
    total = sum(y.numel() for _, y in data)
    nll = None

    def closure():
        nonlocal nll
        nll = 0.0
        for (x, y), a, g in zip(data, offsets, groups):
            log_p = retention_log_probs(a + x @ w[g])
            nll = nll - log_p.gather(-1, y.unsqueeze(-1)).sum()
        penalty = w.square().sum() / (2 * prior_sd**2)
        loss = (nll + penalty) / total  # per-observation scale keeps Adam's step sizes sane
        nll = nll / total
        return loss

    _optimise([w, *offsets], closure, epochs, lr)
    return RetentionLaw(
        weights=w.detach().numpy().copy(),
        lineage_offsets=[a.detach().numpy().ravel() for a in offsets],
        final_nll=float(nll.detach()),
    )


def fit_retention_bootstrap(blocks, *, n_boot: int = 20, seed: int = 0, **kwargs) -> RetentionLaw:
    """Standard errors by resampling lineages within each block."""
    law = fit_retention(blocks, seed=seed, **kwargs)
    rng = np.random.default_rng(seed)
    boots = []
    for b in range(n_boot):
        resampled = [(x, p[rng.integers(0, len(p), len(p))]) for x, p in blocks]
        boots.append(fit_retention(resampled, seed=seed + b + 1, **kwargs).weights)
    law.weights_se = np.std(boots, axis=0)
    return law


def offset_for_count(log_hazard_no_offset: np.ndarray, n_retained: float) -> float:
    """Lineage offset whose expected number of retained genes equals n_retained.

    Lets us predict *which* genes an unseen lineage keeps from only *how many* it keeps.
    """
    target = np.clip(n_retained, 0.5, len(log_hazard_no_offset) - 0.5)
    lo, hi = -30.0, 30.0
    for _ in range(100):
        mid = (lo + hi) / 2
        expected = np.exp(-np.exp(mid + log_hazard_no_offset)).sum()
        lo, hi = (mid, hi) if expected > target else (lo, mid)
    return (lo + hi) / 2
