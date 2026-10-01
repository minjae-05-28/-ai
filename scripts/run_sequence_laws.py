"""Sequence-level laws: how proteome composition tracks temperature, salt, nutrients and genome reduction.

    python scripts/run_sequence_laws.py

Reads data/composition/{prokaryotes,eukaryotes,endosymbiosis}. Tests published sequence laws
and fits the same kind of axis laws as for gene content, so the two levels can be compared:

  temperature   OGT vs IVYWREL (Zeldovich et al. 2007) and charged-vs-polar (Suhre & Claverie
                2003); a ridge model on the 20 amino acids, leave-one-group-out
  salt          acidic excess and median pI vs optimal NaCl; 'salt-in' halophiles
  oligotrophy   side-chain nitrogen in each oligotroph vs its relative (Grzymski & Dussaq 2012)
  reduction     FYMINK and pI vs proteome size in insect endosymbionts (AT bias); eukaryote
                parasite pairs: change in FYMINK, pI and nitrogen on the lifestyle axes
  environment   per pair: change in each statistic regressed on the environment change, leave-
                one-pair-out R^2 -- does environment predict *sequence* change, unlike gene loss?
"""

import json
from pathlib import Path

import numpy as np
from scipy.stats import spearmanr

from organelle_evo.eukaryotes import catalog as euk
from organelle_evo.laws import LAWS_DIR, save_law
from organelle_evo.prokaryotes import catalog as pro
from organelle_evo.sequence import AA, SCALARS

C = Path("data/composition")
OUT = Path("results/sequence")


def load(sub):
    out = {}
    for f in (C / sub).glob("**/*.json"):
        d = json.loads(f.read_text())
        out[d["species"]] = d
    return out


def loo_r2(Z, y, groups=None):
    groups = np.arange(len(y)) if groups is None else np.asarray(groups)
    pred = np.zeros_like(y)
    for g in np.unique(groups):
        tr = groups != g
        b = np.linalg.lstsq(Z[tr], y[tr], rcond=None)[0]
        pred[~tr] = Z[~tr] @ b
    return float(1 - np.sum((y - pred) ** 2) / np.sum((y - y.mean()) ** 2))


def ridge_loo(X, y, groups, lam=1.0):
    pred = np.zeros_like(y)
    for g in np.unique(groups):
        tr = groups != g
        mu, sd = X[tr].mean(0), X[tr].std(0) + 1e-9
        A = np.c_[np.ones(tr.sum()), (X[tr] - mu) / sd]
        w = np.linalg.solve(A.T @ A + lam * np.eye(A.shape[1]), A.T @ y[tr])
        pred[~tr] = np.c_[np.ones((~tr).sum()), (X[~tr] - mu) / sd] @ w
    return pred


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    res = {}
    P = {s: d for s, d in load("prokaryotes").items() if s in pro.SPECIES}
    E = {s: d for s, d in load("eukaryotes").items() if s in euk.SPECIES}
    S = load("endosymbiosis/insect_endosymbiont")
    print(f"{len(P)} prokaryote, {len(E)} eukaryote, {len(S)} insect-endosymbiont proteomes")

    # ---- temperature ----
    sp = sorted(P)
    ogt = np.array([pro.SPECIES[s].temp for s in sp])
    grp = np.array([pro.SPECIES[s].group for s in sp])
    iv, cvp = (np.array([P[s][k] for s in sp]) for k in ("ivywrel", "cvp"))
    X = np.array([[P[s]["composition"][a] for a in AA] for s in sp])
    pred = ridge_loo(X, ogt, grp)
    b = np.polyfit(iv, ogt, 1)
    iv_pred = ridge_loo(iv[:, None], ogt, grp, lam=1e-6)
    rmse = lambda p: float(np.sqrt(np.mean((p - ogt) ** 2)))  # noqa: E731
    res["temperature"] = {
        "n": len(sp), "spearman_ivywrel": float(spearmanr(iv, ogt).correlation),
        "pearson_ivywrel": float(np.corrcoef(iv, ogt)[0, 1]), "ogt_per_0.01_ivywrel": float(b[0] / 100),
        "spearman_cvp": float(spearmanr(cvp, ogt).correlation),
        "rmse_mean_only": float(ogt.std()), "rmse_ivywrel_loo_group": rmse(iv_pred), "rmse_20aa_ridge_loo_group": rmse(pred),
    }
    print("temperature:", {k: round(v, 3) if isinstance(v, float) else v for k, v in res["temperature"].items()})

    # ---- salt ----
    nacl = np.array([pro.SPECIES[s].nacl for s in sp])
    acid = np.array([P[s]["acidic_excess"] for s in sp])
    pi = np.array([P[s]["median_pi"] for s in sp])
    salt_in = [s for s in sp if pro.SPECIES[s].nacl >= 15]
    res["salt"] = {"spearman_acidic_excess": float(spearmanr(acid, nacl).correlation),
                   "spearman_median_pi": float(spearmanr(pi, nacl).correlation),
                   "halophiles_ge_15pct": {s: {"acidic_excess": P[s]["acidic_excess"], "median_pi": P[s]["median_pi"]} for s in salt_in},
                   "others_median_pi": float(np.median([P[s]["median_pi"] for s in sp if s not in salt_in]))}
    print("salt:", res["salt"]["spearman_acidic_excess"], res["salt"]["spearman_median_pi"], res["salt"]["others_median_pi"])

    # ---- pairs: environment -> sequence change ----
    pairs = [(a, d) for a, d in pro.resolve_pairs(P)]
    Z = np.array([pro.design(a, d) for a, d in pairs])
    env = {}
    for k in SCALARS:
        dy = np.array([P[d][k] - P[a][k] for a, d in pairs])
        coef = np.linalg.lstsq(Z, dy, rcond=None)[0]
        env[k] = {"loo_r2_environment": loo_r2(Z, dy), "coef": dict(zip(("base", *pro.AXES), map(float, coef)))}
    res["environment_pairs"] = {"n_pairs": len(pairs), "by_statistic": env}
    for k in ("ivywrel", "cvp", "acidic_excess", "median_pi", "n_side", "fymink"):
        print(f"  env -> change in {k:14s} LOO R^2 {env[k]['loo_r2_environment']:+.2f}  "
              + ", ".join(f"{a} {v:+.4f}" for a, v in env[k]['coef'].items() if a != "base"))
    olig = [(a, d) for a, d in pairs if pro.SPECIES[d].oligo and not pro.SPECIES[a].oligo]
    res["oligotrophy"] = [{"pair": f"{a} -> {d}", "n_side_change": P[d]["n_side"] - P[a]["n_side"]} for a, d in olig]
    print("oligotrophs, change in side-chain N per residue:", [round(r["n_side_change"], 4) for r in res["oligotrophy"]])

    # ---- reduction: insect endosymbionts ----
    sym = sorted(S)
    n = np.array([S[s]["n_proteins"] for s in sym])
    res["endosymbionts"] = {"spearman_size_fymink": float(spearmanr(n, [S[s]["fymink"] for s in sym]).correlation),
                            "spearman_size_pi": float(spearmanr(n, [S[s]["median_pi"] for s in sym]).correlation),
                            "table": {s: {k: S[s][k] for k in ("n_proteins", "fymink", "median_pi", "n_side")} for s in sym}}
    print("endosymbionts: size vs FYMINK", round(res["endosymbionts"]["spearman_size_fymink"], 2),
          "size vs pI", round(res["endosymbionts"]["spearman_size_pi"], 2))

    # ---- reduction: eukaryote parasite pairs on lifestyle axes ----
    ep = [(a, d) for a, d in euk.resolve_pairs(E)]
    Ze = np.array([euk.design(d) for _, d in ep])
    cl = np.array([euk.SPECIES[d].group.split("_")[0] for _, d in ep])
    eu = {}
    for k in ("fymink", "median_pi", "n_side", "ivywrel", "mean_length"):
        dy = np.array([E[d][k] - E[a][k] for a, d in ep])
        coef = np.linalg.lstsq(Ze, dy, rcond=None)[0]
        eu[k] = {"loo_clade_r2": loo_r2(Ze, dy, cl), "coef": dict(zip(("base", *euk.AXES), map(float, coef)))}
        print(f"  eukaryote axes -> change in {k:12s} LOO-clade R^2 {eu[k]['loo_clade_r2']:+.2f}  "
              + ", ".join(f"{a} {v:+.4f}" for a, v in eu[k]['coef'].items()))
    res["eukaryote_pairs"] = {"n_pairs": len(ep), "by_statistic": eu}

    (OUT / "metrics.json").write_text(json.dumps(res, indent=2))
    save_law(LAWS_DIR / "sequence_v1.json", id="sequence_v1",
             scope="Proteome amino-acid composition: temperature, salt, nutrient and genome-reduction signals.",
             model="Correlations and least-squares axis laws on proteome statistics (scripts/run_sequence_laws.py).",
             feature_names=[], data={"prokaryotes": len(P), "eukaryotes": len(E), "insect_endosymbionts": len(S)},
             validation=res, contexts={},
             caveats=["Optimal temperatures and salinities are approximate literature values.",
                      "Species are treated as independent (no phylogenetic correction)."])
    print(f"Done -> {OUT}/ and laws/sequence_v1.json")


if __name__ == "__main__":
    main()
