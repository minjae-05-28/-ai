"""Learn lifestyle-dependent birth-death laws for gene families.

For each (ancestor proxy -> descendant) pair p and Pfam family f:

    log lam_pf = a_lam[p] + x_f @ W_lam[s_p]      duplication / expansion
    log mu_pf  = a_mu[p]  + x_f @ W_mu[s_p]       loss
    log nu_pf  = a_nu[p]  + x_f @ W_nu[s_p]       origination when absent (HGT / de novo)

s_p is the descendant's lifestyle. Per-pair offsets absorb divergence time and overall
genome-size change, so the shared W's are the laws: how a family's features shift its
fate, and how that differs between free-living and parasitic lineages.
"""

import re
from dataclasses import dataclass

import numpy as np
import torch

from .birthdeath import MAX_COUNT, origination_log_prob, transition_log_prob

FAMILY_FEATURES = (
    "hydrophobicity_gravy",
    "tm_helices",
    "protein_length",
    "redox_core",
    "atp_synthase",
    "translation",
    "transcription",
    "protein_targeting",
)

_CLASSES = [
    ("redox_core", r"^(Oxidored_q\d|NADHdh|Proton_antipo|COX\d|Cytochrom_B|Cyt_b|Rieske|Photo_RC|PSII|PsaA)",
     r"cytochrome c oxidase|nadh[- ]ubiquinone|photosystem|cytochrome b6|ubiquinol-cytochrome"),
    ("atp_synthase", r"^ATP-synt", r"atp synthase"),
    ("translation", r"^(Ribosomal_|tRNA-synt|GTP_EFTU|EFG_|eIF|IF2|IF3|RRF)",
     r"ribosomal protein|trna synthetase|translation initiation factor|elongation factor"),
    ("transcription", r"^RNA_pol", r"rna polymerase"),
    ("protein_targeting", r"^(SecY|SecA|Sec61|Sec62|Sec63|SRP|TatC|Tom\d|Tim\d|Tim17)",
     r"translocase|signal recognition particle|translocon"),
]


def pfam_class(name: str, description: str = "") -> str:
    desc = description.lower()
    for cls, name_re, desc_re in _CLASSES:
        if re.match(name_re, name) or re.search(desc_re, desc):
            return cls
    return "other"


def family_features(profiles: list[dict], meta: dict) -> tuple[list[str], np.ndarray]:
    """Families seen in any species, with features averaged over all their domains."""
    totals: dict[str, np.ndarray] = {}
    for prof in profiles:
        for fam, row in prof["families"].items():
            totals[fam] = totals.get(fam, np.zeros(4)) + np.array(row[1:5], dtype=float)
    fams = sorted(totals)
    t = np.array([totals[f] for f in fams])  # n_domains, sum_gravy, sum_tm, sum_len
    nd = np.maximum(t[:, 0], 1)
    cont = np.stack([t[:, 1] / nd, np.log1p(t[:, 2] / nd), np.log(np.maximum(t[:, 3] / nd, 1))], 1)
    cont = (cont - cont.mean(0)) / np.where(cont.std(0) > 0, cont.std(0), 1)
    classes = [pfam_class(f, meta.get(f, {}).get("description", "")) for f in fams]
    onehot = np.array([[c == k for k in FAMILY_FEATURES[3:]] for c in classes], dtype=float)
    return fams, np.concatenate([cont, onehot.reshape(len(fams), -1)], 1)


def counts(profile: dict, fams: list[str]) -> np.ndarray:
    return np.array([profile["families"].get(f, [0])[0] for f in fams], dtype=np.int64)


@dataclass
class BDLaw:
    lifestyles: tuple[str, ...]
    w_lam: np.ndarray  # (S, F)
    w_mu: np.ndarray
    w_nu: np.ndarray
    a_lam: np.ndarray  # (P,)
    a_mu: np.ndarray
    a_nu: np.ndarray
    nll: float  # total negative log-likelihood
    n_params: int
    se: dict | None = None  # name -> (S, F) bootstrap standard errors


def _pair_terms(x, n, m, a_lam, a_mu, a_nu, w_lam, w_mu, w_nu):
    n_c = n.clamp_max(MAX_COUNT)
    m_c = m.clamp_max(MAX_COUNT)
    had = n > 0
    ll_bd = transition_log_prob(n_c[had], m_c[had], a_lam + x[had] @ w_lam, a_mu + x[had] @ w_mu)
    ll_or = origination_log_prob(m[~had] > 0, a_nu + x[~had] @ w_nu)
    return ll_bd.sum() + ll_or.sum()


def fit_bd(
    x: np.ndarray,
    pairs: list[tuple[np.ndarray, np.ndarray, int]],
    lifestyles: tuple[str, ...],
    *,
    epochs: int = 600,
    lr: float = 0.05,
    prior_sd: float = 2.0,
    seed: int = 0,
) -> BDLaw:
    """pairs: (ancestor counts, descendant counts, lifestyle index). Counts are (F,)."""
    torch.manual_seed(seed)
    xt = torch.as_tensor(x, dtype=torch.float64)
    data = [(torch.as_tensor(n), torch.as_tensor(m), s) for n, m, s in pairs]
    S, F, P = len(lifestyles), x.shape[1], len(pairs)
    w = {k: torch.zeros(S, F, dtype=torch.float64, requires_grad=True) for k in ("lam", "mu", "nu")}
    a = {k: torch.full((P,), -1.0, dtype=torch.float64, requires_grad=True) for k in ("lam", "mu", "nu")}
    n_obs = sum(len(n) for n, _, _ in pairs)
    opt = torch.optim.Adam([*w.values(), *a.values()], lr=lr)
    nll = None
    for _ in range(epochs):
        opt.zero_grad()
        ll = sum(
            _pair_terms(xt, n, m, a["lam"][p], a["mu"][p], a["nu"][p], w["lam"][s], w["mu"][s], w["nu"][s])
            for p, (n, m, s) in enumerate(data)
        )
        penalty = sum(v.square().sum() for v in w.values()) / (2 * prior_sd**2)
        nll = -ll
        ((nll + penalty) / n_obs).backward()
        opt.step()
    used = sorted({s for _, _, s in pairs})
    return BDLaw(
        lifestyles=lifestyles,
        w_lam=w["lam"].detach().numpy().copy(),
        w_mu=w["mu"].detach().numpy().copy(),
        w_nu=w["nu"].detach().numpy().copy(),
        a_lam=a["lam"].detach().numpy().copy(),
        a_mu=a["mu"].detach().numpy().copy(),
        a_nu=a["nu"].detach().numpy().copy(),
        nll=float(nll.detach()),
        n_params=3 * F * len(used) + 3 * P,
    )


def fit_bd_bootstrap(x, pairs, lifestyles, *, n_boot: int = 20, seed: int = 0, **kw) -> BDLaw:
    """Standard errors by resampling pairs within each lifestyle."""
    law = fit_bd(x, pairs, lifestyles, seed=seed, **kw)
    rng = np.random.default_rng(seed)
    by_s = {}
    for i, (_, _, s) in enumerate(pairs):
        by_s.setdefault(s, []).append(i)
    boots = {"lam": [], "mu": [], "nu": []}
    for b in range(n_boot):
        idx = [i for ids in by_s.values() for i in rng.choice(ids, len(ids))]
        f = fit_bd(x, [pairs[i] for i in idx], lifestyles, seed=seed + b + 1, **kw)
        boots["lam"].append(f.w_lam)
        boots["mu"].append(f.w_mu)
        boots["nu"].append(f.w_nu)
    law.se = {k: np.std(v, axis=0) for k, v in boots.items()}
    return law


def loss_probability(n, x, w_lam, w_mu, a_lam, a_mu) -> np.ndarray:
    """P(family with n copies has none left) for one pair."""
    with torch.no_grad():
        n_t = torch.as_tensor(np.minimum(n, MAX_COUNT))
        lp = transition_log_prob(
            n_t, torch.zeros_like(n_t),
            torch.as_tensor(a_lam + x @ w_lam), torch.as_tensor(a_mu + x @ w_mu),
        )
    return lp.exp().numpy()


def offset_for_losses(n, x, w_lam, w_mu, a_lam, n_lost) -> float:
    """Loss offset whose expected number of lost families equals n_lost."""
    lo, hi = -15.0, 10.0
    for _ in range(60):
        mid = (lo + hi) / 2
        exp_lost = loss_probability(n, x, w_lam, w_mu, a_lam, mid).sum()
        lo, hi = (mid, hi) if exp_lost < n_lost else (lo, mid)
    return (lo + hi) / 2
