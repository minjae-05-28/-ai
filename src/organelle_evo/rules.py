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
    opt = torch.optim.Adam([w_t, w_l, a_t, a_l], lr=lr)

    for _ in range(epochs):
        opt.zero_grad()
        log_p = end_state_log_probs(a_t + x @ w_t, a_l + x @ w_l)
        nll = -log_p.gather(-1, y.unsqueeze(-1)).mean()
        loss = nll + l2 * (w_t.square().sum() + w_l.square().sum())
        loss.backward()
        opt.step()

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
