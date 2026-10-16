"""Beyond cell composition: immune / stromal markers and tumour purity (pre-registration 19,
docs/preregistration/2026-10-16_cancer_atavism_composition.md).

    python scripts/cancer_composition.py   -> results/cancer_atavism/composition.json
"""

import json
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import cancer_atavism as ca  # noqa: E402
import cancer_proliferation as cp  # noqa: E402

OUT = Path("results/cancer_atavism/composition.json")
PURITY = Path("data/tcga_purity/absolute.tsv")
IMMUNE = ["PTPRC", "CD2", "CD3D", "CD3E", "CD3G", "CD247", "CD8A", "CD4", "CD19", "MS4A1", "CD79A", "CD68", "CD163",
          "CD14", "LYZ", "ITGAM", "FCGR3A", "NKG7", "GZMA", "PRF1", "CCL5", "CXCL9", "LCP2", "CORO1A"]
STROMAL = ["COL1A1", "COL1A2", "COL3A1", "COL5A1", "COL6A3", "DCN", "LUM", "FAP", "PDGFRA", "PDGFRB", "ACTA2", "THY1",
           "FN1", "SPARC", "VCAN", "POSTN", "MMP2", "CDH11", "PECAM1", "VWF", "CDH5"]


def load_purity():
    if not PURITY.exists():
        return {}
    out = {}
    for line in PURITY.read_text().splitlines()[1:]:
        s, p = line.split("\t")
        try:
            out.setdefault(s[:15], float(p))
        except ValueError:
            pass
    return out


def fit(y, X):
    A = np.column_stack([np.ones(len(y))] + list(X))
    coef, *_ = np.linalg.lstsq(A, y, rcond=None)
    return coef


def cohort(path, ages, P, purity):
    z = np.load(path, allow_pickle=False)
    genes = [str(g) for g in z["genes"]]
    lfc = z["lfc"].astype(np.float32)
    nm, tm = z["normal_mean"], z["tumour_mean"]
    expressed = (nm >= 1) | (tm >= 1)
    gset = np.array(genes)
    is_p = np.isin(gset, list(P)) & expressed
    imm = np.isin(gset, IMMUNE)
    stro = np.isin(gset, STROMAL)
    s = np.nanmean(lfc[:, is_p], 1)
    i = np.nanmean(lfc[:, imm], 1)
    t = np.nanmean(lfc[:, stro], 1)
    keep = np.array([g in ages for g in genes]) & expressed & ~is_p & ~imm & ~stro
    gi = np.where(keep)[0]
    L, N = lfc[:, gi], nm[gi]
    age = np.array([ages[genes[k]][0] for k in gi])
    uc, mc = age <= 3, age > 3
    cuts = np.quantile(N, np.linspace(0, 1, 11)[1:-1])
    d = ca.delta_per_patient(L, uc, mc, np.searchsorted(cuts, N, side="right"))
    n = len(d)
    coef = fit(d, [s, i, t])
    bv = cp.boot(lambda idx: fit(d[idx], [s[idx], i[idx], t[idx]]), n)
    out = {"pairs": n, "small_for_covariates": n < 20, "immune_markers": int(imm.sum()), "stromal_markers": int(stro.sum()),
           "primary_intercept": cp.verdict(coef[0], bv[:, 0]),
           "coef": {"proliferation": cp.verdict(coef[1], bv[:, 1]), "immune": cp.verdict(coef[2], bv[:, 2]),
                    "stromal": cp.verdict(coef[3], bv[:, 3])},
           "covariate_means": {"s": round(float(s.mean()), 3), "i": round(float(i.mean()), 3), "t": round(float(t.mean()), 3)}}
    pats = [str(p) for p in z["patients"]]
    pi = np.array([purity.get(p + "-01", np.nan) for p in pats])
    has = ~np.isnan(pi)
    out["purity_pairs"] = int(has.sum())
    if has.sum() >= 10:
        dp, sp, ip = d[has], s[has], 1 - pi[has]
        c2 = fit(dp, [ip, sp])
        b2 = cp.boot(lambda idx: fit(dp[idx], [ip[idx], sp[idx]]), int(has.sum()))
        med = np.median(pi[has])
        hi, lo = dp[pi[has] >= med], dp[pi[has] < med]
        out["pure_tumour_extrapolation"] = {**cp.verdict(c2[0], b2[:, 0]),
                                            "impurity_coef": round(float(c2[1]), 4),
                                            "purity_range": [round(float(pi[has].min()), 3), round(float(pi[has].max()), 3)]}
        out["purity_halves"] = {"high_mean": round(float(hi.mean()), 4), "low_mean": round(float(lo.mean()), 4),
                                "high_minus_low": round(float(hi.mean() - lo.mean()), 4)}
    return out


def overall(res, key):
    v = [r[key]["verdict"] for r in res.values() if key in r]
    n, pos, neg = len(v), v.count("양성"), v.count("음성")
    call = "지지" if n and pos >= 2 * n / 3 else ("반대" if n and neg >= 2 * n / 3 else "판단 보류")
    return {"cohorts": n, "positive": pos, "negative": neg, "draw": n - pos - neg, "call": call}


def main():
    ages = ca.load_ages()
    go, hall, _ = cp.load_p()
    purity = load_purity()
    res = {p.stem: cohort(p, ages, go | hall, purity) for p in sorted(ca.DATA.glob("*.npz"))}
    coef_dir = {k: {"positive": sum(r["coef"][k]["estimate"] > 0 for r in res.values()),
                    "negative": sum(r["coef"][k]["estimate"] < 0 for r in res.values())}
                for k in ("proliferation", "immune", "stromal")}
    out = {"purity_source": Path("data/tcga_purity/source.txt").read_text().strip() if Path("data/tcga_purity/source.txt").exists() else None,
           "purity_samples": len(purity),
           "overall_primary": overall(res, "primary_intercept"),
           "overall_pure_tumour": overall(res, "pure_tumour_extrapolation"),
           "high_purity_more_tilted": sum(r["purity_halves"]["high_minus_low"] > 0 for r in res.values() if "purity_halves" in r),
           "coef_signs": coef_dir, "cohorts": res}
    OUT.write_text(json.dumps(out, ensure_ascii=False, indent=1))
    for c, r in res.items():
        print(c, r["pairs"], r["primary_intercept"], {k: v["estimate"] for k, v in r["coef"].items()},
              r.get("purity_pairs"), r.get("pure_tumour_extrapolation"), r.get("purity_halves"))
    print(json.dumps({k: v for k, v in out.items() if k != "cohorts"}, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
