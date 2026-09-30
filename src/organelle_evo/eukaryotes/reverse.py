"""Run the laws backwards: infer an ancestor's gene-family content from one genome.

For each family, Bayes' rule combines
  - a prior over ancestral copy number n (what free-living eukaryotes usually carry), and
  - the forward law's likelihood P(m | n) of ending with the observed m copies,
into a posterior P(n | m). A family that is absent today but common in free-living
relatives, and that the law says is easily lost, is inferred to have been ancestral.

How much evolution separates ancestor and descendant is unknown, so the per-lineage
offsets (a_lam, a_mu, a_nu) are fitted by maximising the marginal likelihood
sum_f log sum_n P(m_f | n) P(n) of the observed genome.
"""

from dataclasses import dataclass

import numpy as np
import torch

from .birthdeath import transition_log_prob

# Copy numbers are capped lower than in the forward fit: presence is what matters here,
# and the state space sets the cost of every posterior.
MAX_COUNT = 12
N_STATES = MAX_COUNT + 1


def count_prior(reference_counts: np.ndarray, pseudo: float = 0.5) -> np.ndarray:
    """(F, K+1) prior over ancestral copy number from free-living reference genomes.

    P(present) is the smoothed fraction of references carrying the family; given
    presence, copies follow a geometric distribution with the references' mean.
    """
    ref = np.minimum(np.asarray(reference_counts), MAX_COUNT)  # (S, F)
    n_ref = ref.shape[0]
    present = (ref > 0).sum(0)
    p_present = (present + pseudo) / (n_ref + 2 * pseudo)
    mean_if_present = np.where(present > 0, ref.sum(0) / np.maximum(present, 1), 1.0)
    q = 1.0 / np.maximum(mean_if_present, 1.0)  # geometric success probability
    k = np.arange(1, N_STATES)
    geom = q[:, None] * (1 - q[:, None]) ** (k[None, :] - 1)
    geom /= geom.sum(1, keepdims=True)
    return np.concatenate([(1 - p_present)[:, None], p_present[:, None] * geom], axis=1)


def _log_lik_table(m, x, w_lam, w_mu, w_nu, a_lam, a_mu, a_nu):
    """(F, K+1) log P(m_f | n) for every ancestral state n."""
    m_t = torch.as_tensor(np.minimum(m, MAX_COUNT))
    xt = torch.as_tensor(x, dtype=torch.float64)
    log_lam = a_lam + xt @ torch.as_tensor(w_lam, dtype=torch.float64)
    log_mu = a_mu + xt @ torch.as_tensor(w_mu, dtype=torch.float64)
    log_nu = a_nu + xt @ torch.as_tensor(w_nu, dtype=torch.float64)
    n = torch.arange(1, N_STATES, dtype=torch.float64)[None, :]  # (1, K)
    ll_pos = transition_log_prob(n, m_t[:, None], log_lam[:, None], log_mu[:, None], MAX_COUNT)  # (F, K)
    nu = log_nu.exp()
    # From zero copies: origination, then a geometric number of copies (P(m) = 0.5^m).
    ll_zero = torch.where(
        m_t > 0,
        torch.log(-torch.expm1(-nu).clamp_max(-1e-12)) + m_t * np.log(0.5),
        -nu,
    )
    return torch.cat([ll_zero[:, None], ll_pos], dim=1)


@dataclass
class Reconstruction:
    posterior: np.ndarray  # (F, K+1) P(ancestral copies = n | observed genome)
    offsets: tuple[float, float, float]
    log_marginal: float

    @property
    def p_present(self) -> np.ndarray:
        return 1.0 - self.posterior[:, 0]

    @property
    def expected_copies(self) -> np.ndarray:
        return self.posterior @ np.arange(N_STATES)


def reconstruct(
    m: np.ndarray,
    x: np.ndarray,
    w_lam: np.ndarray,
    w_mu: np.ndarray,
    w_nu: np.ndarray,
    prior: np.ndarray,
    *,
    steps: int = 150,
    lr: float = 0.1,
) -> Reconstruction:
    """Posterior ancestral content of one genome under a (possibly mixed) law."""
    log_prior = torch.as_tensor(np.log(np.clip(prior, 1e-300, None)), dtype=torch.float64)
    a = torch.tensor([-1.0, -1.0, -3.0], dtype=torch.float64, requires_grad=True)
    opt = torch.optim.Adam([a], lr=lr)
    for _ in range(steps):
        opt.zero_grad()
        table = _log_lik_table(m, x, w_lam, w_mu, w_nu, a[0], a[1], a[2])
        loss = -torch.logsumexp(table + log_prior, dim=1).sum()
        loss.backward()
        opt.step()
    with torch.no_grad():
        joint = _log_lik_table(m, x, w_lam, w_mu, w_nu, a[0], a[1], a[2]) + log_prior
        marg = torch.logsumexp(joint, dim=1, keepdim=True)
        post = (joint - marg).exp().numpy()
    return Reconstruction(post, tuple(float(v) for v in a.detach()), float(marg.sum()))
