"""Co-loss modules: are gene families lost together, beyond each family's own propensity?

Each parasite pair gives a loss vector over the families its ancestor proxy had
(1 = lost, 0 = kept, missing = not in the ancestor). The model is logistic:

    logit P(lost_pf) = a_p + b_f + u_p . v_f

a_p is how reduced the parasite is, b_f how loss-prone the family is, and the rank-k
term says that families with similar v_f are lost together (a module). k = 0 is the
additive model, with no coupling. A module law is real if revealing part of a new
parasite's losses predicts the rest better with k > 0 than with k = 0.
"""

from dataclasses import dataclass

import numpy as np
import torch


def loss_matrix(pairs, counts_by_species) -> np.ndarray:
    """(pairs, families) with 1 lost, 0 kept, nan where the ancestor lacks the family."""
    rows = []
    for a, d in pairs:
        n, m = counts_by_species[a], counts_by_species[d]
        rows.append(np.where(n > 0, (m == 0).astype(float), np.nan))
    return np.array(rows)


@dataclass
class ModuleModel:
    a: np.ndarray  # (P,)
    b: np.ndarray  # (F,)
    u: np.ndarray  # (P, k)
    v: np.ndarray  # (F, k)


def fit_modules(L: np.ndarray, k: int, *, l2: float = 1.0, epochs: int = 400, lr: float = 0.05,
                seed: int = 0) -> ModuleModel:
    """Masked logistic matrix factorisation with Gaussian priors on b, u, v."""
    torch.manual_seed(seed)
    mask = torch.tensor(~np.isnan(L))
    y = torch.tensor(np.nan_to_num(L), dtype=torch.float32)
    P, F = L.shape
    a = torch.zeros(P, requires_grad=True)
    b = torch.zeros(F, requires_grad=True)
    u = (0.1 * torch.randn(P, k)).requires_grad_()
    v = (0.1 * torch.randn(F, k)).requires_grad_()
    opt = torch.optim.Adam([a, b, u, v], lr=lr)
    n_obs = mask.sum()
    for _ in range(epochs):
        opt.zero_grad()
        logit = a[:, None] + b[None, :] + u @ v.T
        nll = torch.nn.functional.binary_cross_entropy_with_logits(logit[mask], y[mask], reduction="sum")
        pen = 0.5 * (b.pow(2).sum() / 4.0 + l2 * (u.pow(2).sum() + v.pow(2).sum()))
        ((nll + pen) / n_obs).backward()
        opt.step()
    d = lambda t: t.detach().numpy().copy()  # noqa: E731
    return ModuleModel(d(a), d(b), d(u), d(v))


def fit_new_pair(model: ModuleModel, y: np.ndarray, idx: np.ndarray, *, l2: float = 1.0,
                 steps: int = 300) -> tuple[float, np.ndarray]:
    """a and u for a new pair from its revealed losses y at families idx (b, v fixed)."""
    k = model.v.shape[1]
    b = torch.tensor(model.b[idx], dtype=torch.float32)
    v = torch.tensor(model.v[idx], dtype=torch.float32)
    t = torch.tensor(y, dtype=torch.float32)
    a = torch.zeros(1, requires_grad=True)
    u = torch.zeros(k, requires_grad=True)
    opt = torch.optim.Adam([a, u], lr=0.05)
    for _ in range(steps):
        opt.zero_grad()
        logit = a + b + v @ u
        loss = torch.nn.functional.binary_cross_entropy_with_logits(logit, t, reduction="sum") \
            + 0.5 * l2 * u.pow(2).sum()
        loss.backward()
        opt.step()
    return float(a.detach()), u.detach().numpy().copy()


def predict_hidden(model: ModuleModel, row: np.ndarray, reveal: float, rng) -> tuple[np.ndarray, np.ndarray]:
    """Reveal a random share of a held-out pair's families; score the rest. -> (scores, lost)."""
    obs = np.flatnonzero(~np.isnan(row))
    perm = rng.permutation(obs)
    n_rev = int(round(reveal * len(obs)))
    shown, hidden = perm[:n_rev], perm[n_rev:]
    a, u = fit_new_pair(model, row[shown], shown)
    scores = a + model.b[hidden] + model.v[hidden] @ u
    return scores, row[hidden].astype(bool)
