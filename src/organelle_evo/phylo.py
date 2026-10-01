"""Phylogenetic correction from taxonomy: Grafen-style covariance and PGLS with Pagel's lambda.

Without a sequence-based tree, the NCBI classification (domain, kingdom, phylum, class,
order, family, genus, species) is used as a tree with one unit per rank. Two species
share as much branch length as the number of leading ranks they have in common, so
V[i, j] = shared ranks and V[i, i] = all ranks (Grafen 1989, equal branch lengths).

PGLS fits y = X b under covariance sigma^2 * V_lambda, where V_lambda scales the
off-diagonal (shared-history) part by Pagel's lambda in [0, 1]: lambda = 0 is ordinary
least squares, lambda = 1 the full taxonomy tree. lambda is chosen by maximum likelihood.

Equal branch lengths can understate how alike close relatives are, so `rank_gls` instead
estimates one variance component per taxonomic rank (nested random intercepts) by maximum
likelihood: V = s0 I + sum_r s_r Z_r Z_r^T. Its `shares` say how much of the residual
variance each rank carries.
"""

from dataclasses import dataclass

import numpy as np
from scipy import stats

RANKS = ("domain", "kingdom", "phylum", "class", "order", "family", "genus")


def taxonomy_cov(names: list[str], tax: dict[str, dict]) -> np.ndarray:
    depth = len(RANKS) + 1
    lin = []
    for n in names:
        t = tax.get(n, {})
        lin.append([t.get(r) for r in RANKS])
    V = np.zeros((len(names), len(names)))
    for i in range(len(names)):
        for j in range(len(names)):
            if i == j:
                V[i, j] = depth
                continue
            shared = 0
            for a, b in zip(lin[i], lin[j]):
                if a is None or b is None or a != b:
                    break
                shared += 1
            V[i, j] = shared
    return V / depth


@dataclass
class PGLSResult:
    coef: np.ndarray
    se: np.ndarray
    p: np.ndarray
    lam: float
    loglik: float


def _gls(X, y, V):
    L = np.linalg.cholesky(V + 1e-9 * np.eye(len(y)))
    Xw, yw = np.linalg.solve(L, X), np.linalg.solve(L, y)
    b, *_ = np.linalg.lstsq(Xw, yw, rcond=None)
    r = yw - Xw @ b
    n, k = X.shape
    s2 = r @ r / n
    loglik = -0.5 * (n * np.log(2 * np.pi * s2) + 2 * np.log(np.diag(L)).sum() + n)
    cov = np.linalg.inv(Xw.T @ Xw) * (r @ r / (n - k))
    return b, np.sqrt(np.diag(cov)), loglik


def pgls(X: np.ndarray, y: np.ndarray, V: np.ndarray, lam: float | None = None) -> PGLSResult:
    """X should include an intercept column. lam=None estimates Pagel's lambda by ML."""
    D = np.diag(np.diag(V))
    grid = [lam] if lam is not None else np.linspace(0, 1, 41)
    best = None
    for g in grid:
        b, se, ll = _gls(X, y, D + g * (V - D))
        if best is None or ll > best[3]:
            best = (b, se, g, ll)
    b, se, g, ll = best
    t = b / se
    p = 2 * stats.t.sf(np.abs(t), df=len(y) - X.shape[1])
    return PGLSResult(b, se, p, float(g), float(ll))


def rank_labels(names: list[str], tax: dict[str, dict]) -> list[list]:
    """Per rank, a nested group label for each species (unknown ranks get their own label)."""
    out = []
    for k in range(len(RANKS)):
        labels = []
        for n in names:
            t = tax.get(n, {})
            lin = tuple(t.get(r) for r in RANKS[: k + 1])
            labels.append(lin if all(lin) else ("?", n, k))
        out.append(labels)
    return out


@dataclass
class RankGLSResult:
    coef: np.ndarray
    se: np.ndarray
    p: np.ndarray
    shares: dict
    loglik: float


def rank_gls(X: np.ndarray, y: np.ndarray, names: list[str], tax: dict[str, dict]) -> RankGLSResult:
    from scipy.optimize import minimize

    Zs = []
    for labels in rank_labels(names, tax):
        u = {l: i for i, l in enumerate(dict.fromkeys(labels))}
        if len(u) in (1, len(labels)):
            continue  # a rank that groups everyone or no one adds nothing identifiable
        Z = np.zeros((len(labels), len(u)))
        Z[np.arange(len(labels)), [u[l] for l in labels]] = 1
        Zs.append(Z @ Z.T)
    n, k = X.shape
    scale = np.var(y) + 1e-12

    def build(theta):
        return np.exp(theta[0]) * np.eye(n) + sum(np.exp(t) * K for t, K in zip(theta[1:], Zs))

    def nll(theta):
        V = build(theta) * scale
        try:
            L = np.linalg.cholesky(V)
        except np.linalg.LinAlgError:
            return 1e12
        Xw, yw = np.linalg.solve(L, X), np.linalg.solve(L, y)
        b, *_ = np.linalg.lstsq(Xw, yw, rcond=None)
        r = yw - Xw @ b
        return 0.5 * (r @ r + 2 * np.log(np.diag(L)).sum())

    th0 = np.full(1 + len(Zs), np.log(1.0 / (1 + len(Zs))))
    opt = minimize(nll, th0, method="L-BFGS-B", bounds=[(-12, 4)] * len(th0))
    V = build(opt.x) * scale
    L = np.linalg.cholesky(V)
    Xw, yw = np.linalg.solve(L, X), np.linalg.solve(L, y)
    b, *_ = np.linalg.lstsq(Xw, yw, rcond=None)
    cov = np.linalg.inv(Xw.T @ Xw)
    se = np.sqrt(np.diag(cov))
    p = 2 * stats.norm.sf(np.abs(b / se))
    comps = np.exp(opt.x)
    shares = {"species": float(comps[0] / comps.sum()), "shared_history": float(comps[1:].sum() / comps.sum())}
    return RankGLSResult(b, se, p, shares, float(-opt.fun))
