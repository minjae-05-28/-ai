"""Gene-family birth-death model: families can grow as well as shrink.

Each copy of a family independently duplicates (birth, rate lam) or is lost (death,
rate mu) — Kendall's linear birth-death process. Over an integrated time of 1 (time is
absorbed into the rates, as in the organelle model) a family with n copies ends with
m copies with probability

    P(0 | n)  = alpha^n
    P(m | n)  = sum_{j>=1} C(n,j) (1-alpha)^j alpha^(n-j) * C(m-1,j-1) (1-beta)^j beta^(m-j)

(j copies leave surviving descendants; j surviving lineages hold m copies in total)

    alpha = mu (E - 1) / (lam E - mu),  beta = lam (E - 1) / (lam E - mu),  E = exp(lam - mu)

A linear process can never create a family from zero copies, so families absent from
the ancestor get a separate origination channel (horizontal transfer or de novo
birth): P(present | absent) = 1 - exp(-exp(log_nu)).

With a single copy and lam = 0 this reduces exactly to the organelle retention model.
"""

import numpy as np
import torch

MAX_COUNT = 30  # copy numbers are capped; very large families carry little extra signal


def _alpha_beta(log_lam: torch.Tensor, log_mu: torch.Tensor):
    lam, mu = log_lam.exp(), log_mu.exp()
    r = lam - mu
    small = r.abs() < 1e-6
    r_safe = torch.where(small, torch.ones_like(r), r)
    em1 = torch.expm1(r_safe)  # E - 1
    denom = lam * (em1 + 1) - mu
    alpha = torch.where(small, lam / (1 + lam), mu * em1 / denom)
    beta = torch.where(small, lam / (1 + lam), lam * em1 / denom)
    eps = 1e-12
    return alpha.clamp(eps, 1 - eps), beta.clamp(eps, 1 - eps)


def _log_binom(n, k):
    return torch.lgamma(n + 1) - torch.lgamma(k + 1) - torch.lgamma(n - k + 1)


def transition_log_prob(n: torch.Tensor, m: torch.Tensor, log_lam, log_mu, max_count: int = MAX_COUNT) -> torch.Tensor:
    """log P(m | n) for n >= 1 (elementwise; all tensors broadcast together; n, m <= max_count)."""
    shape = torch.broadcast_shapes(n.shape, m.shape, log_lam.shape, log_mu.shape)
    n = n.to(log_lam.dtype).expand(shape)
    m = m.to(log_lam.dtype).expand(shape)
    alpha, beta = _alpha_beta(log_lam.expand(shape), log_mu.expand(shape))
    la, lb = alpha.log(), beta.log()
    l1a, l1b = torch.log1p(-alpha), torch.log1p(-beta)
    # j of the n copies leave surviving descendants (binomial); j surviving lineages
    # hold m copies in total (negative binomial). Sum over j on a new leading axis.
    j = torch.arange(1, max_count + 1, dtype=n.dtype).reshape(-1, *([1] * len(shape)))
    valid = j <= torch.minimum(n, m)
    jj = torch.minimum(j, torch.minimum(n, m).clamp_min(1))
    terms = (
        _log_binom(n, jj) + jj * l1a + (n - jj) * la
        + _log_binom(m - 1, jj - 1) + jj * l1b + (m - jj) * lb
    )
    terms = torch.where(valid & (m > 0), terms, torch.full_like(terms, -torch.inf))
    log_pos = torch.logsumexp(terms, dim=0)
    return torch.where(m > 0, log_pos, n * la)


def origination_log_prob(present: torch.Tensor, log_nu: torch.Tensor) -> torch.Tensor:
    """log P(family present | absent in ancestor) under hazard exp(log_nu)."""
    nu = log_nu.exp()
    return torch.where(present, torch.log(-torch.expm1(-nu).clamp_max(-1e-12)), -nu)


def simulate(
    n0: np.ndarray,
    log_lam: np.ndarray,
    log_mu: np.ndarray,
    log_nu: np.ndarray,
    *,
    horizon: float = 1.0,
    n_steps: int = 200,
    rng: np.random.Generator | None = None,
) -> np.ndarray:
    """Forward-simulate copy numbers (broadcast over leading sample dims)."""
    rng = rng or np.random.default_rng()
    lam, mu, nu = np.exp(log_lam), np.exp(log_mu), np.exp(log_nu)
    n = np.array(n0, dtype=np.int64)
    dt = horizon / n_steps
    p_birth, p_death, p_orig = -np.expm1(-lam * dt), -np.expm1(-mu * dt), -np.expm1(-nu * dt)
    for _ in range(n_steps):
        births = rng.binomial(n, np.broadcast_to(p_birth, n.shape))
        deaths = rng.binomial(n, np.broadcast_to(p_death, n.shape))
        n = n + births - deaths
        zero = n == 0
        n = n + (zero & (rng.random(n.shape) < p_orig))
    return n
