"""Beyond proliferation: does the tumour lean towards unicellular-era genes once proliferation is removed?
(pre-registration 18, docs/preregistration/2026-10-16_cancer_atavism_proliferation.md)

    python scripts/cancer_proliferation.py   -> results/cancer_atavism/proliferation.json
"""

import json
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import cancer_atavism as ca  # noqa: E402

OUT = Path("results/cancer_atavism/proliferation.json")


def load_p():
    go = set()
    lines = Path("data/human/proliferation_go.tsv").read_text().splitlines()
    for line in lines[1:]:
        x = line.split("\t")
        if len(x) > 1 and x[1]:
            go.add(x[1])
    h = json.loads(Path("data/human/hallmark_proliferation.json").read_text())
    hall = {g for v in h["sets"].values() for g in v}
    return go, hall, h["source"]


def boot(fn, n, seed=ca.SEED):
    rng = np.random.default_rng(seed)
    vals = np.array([fn(rng.integers(0, n, n)) for _ in range(ca.N_BOOT)])
    return vals


def verdict(est, vals):
    lo, hi = np.percentile(vals, [2.5, 97.5])
    return {"estimate": round(float(est), 4), "lo": round(float(lo), 4), "hi": round(float(hi), 4),
            "verdict": "양성" if lo > 0 else ("음성" if hi < 0 else "무승부")}


def intercept(delta, s):
    A = np.vstack([np.ones_like(s), s]).T
    coef, *_ = np.linalg.lstsq(A, delta, rcond=None)
    return coef


def cohort(path, ages, P):
    z = np.load(path, allow_pickle=False)
    genes = [str(g) for g in z["genes"]]
    lfc = z["lfc"].astype(np.float32)
    nm, tm = z["normal_mean"], z["tumour_mean"]
    expressed = (nm >= 1) | (tm >= 1)
    is_p = np.array([g in P for g in genes]) & expressed
    s = np.nanmean(lfc[:, is_p], 1)                                   # proliferation score per patient
    keep = np.array([g in ages for g in genes]) & expressed & ~is_p
    gi = np.where(keep)[0]
    L, N = lfc[:, gi], nm[gi]
    age = np.array([ages[genes[i]][0] for i in gi])
    uc, mc = age <= 3, age > 3
    cuts = np.quantile(N, np.linspace(0, 1, 11)[1:-1])
    dec = np.searchsorted(cuts, N, side="right")
    d = ca.delta_per_patient(L, uc, mc, dec)
    n = len(d)
    a, b = intercept(d, s)
    bv = boot(lambda i: intercept(d[i], s[i]), n)
    # stricter: also drop genes whose LFC follows the proliferation score (r > 0.5 across patients)
    Lc = L - np.nanmean(L, 0)
    sc = s - s.mean()
    r = np.nansum(Lc * sc[:, None], 0) / (np.sqrt(np.nansum(Lc ** 2, 0) * (sc ** 2).sum()) + 1e-12)
    loose = r <= 0.5
    d2 = ca.delta_per_patient(L, uc & loose, mc & loose, dec)
    p_ages = [ages[g][0] for g in genes if g in P and g in ages]
    return {"pairs": n, "p_genes_removed": int(is_p.sum()), "genes_left": int(len(gi)),
            "p_uc_share": round(float(np.mean([x <= 3 for x in p_ages])), 4),
            "all_uc_share": round(float(uc.mean()), 4),
            "s_range": [round(float(s.min()), 3), round(float(s.max()), 3)], "s_mean": round(float(s.mean()), 3),
            "primary_intercept": verdict(a, bv[:, 0]), "slope": verdict(b, bv[:, 1]),
            "removal_only": verdict(d.mean(), boot(lambda i: d[i].mean(), n)),
            "strict_removal": {**verdict(d2.mean(), boot(lambda i: d2[i].mean(), n)),
                               "extra_genes_dropped": int((~loose).sum())}}


def overall(res, key):
    v = [r[key]["verdict"] for r in res.values()]
    n, pos, neg = len(v), v.count("양성"), v.count("음성")
    call = "지지" if pos >= 2 * n / 3 else ("반대" if neg >= 2 * n / 3 else "판단 보류")
    return {"cohorts": n, "positive": pos, "negative": neg, "draw": n - pos - neg, "call": call}


def run(ages, P):
    res = {p.stem: cohort(p, ages, P) for p in sorted(ca.DATA.glob("*.npz"))}
    return {"overall": {k: overall(res, k) for k in ["primary_intercept", "removal_only", "strict_removal", "slope"]},
            "cohorts": res}


def main():
    ages = ca.load_ages()
    go, hall, source = load_p()
    out = {"p_sizes": {"go": len(go), "hallmark": len(hall), "union": len(go | hall), "hallmark_source": source},
           "main": run(ages, go | hall), "go_only": run(ages, go)}
    if hall:
        out["hallmark_only"] = run(ages, hall)
    OUT.write_text(json.dumps(out, ensure_ascii=False, indent=1))
    for c, r in out["main"]["cohorts"].items():
        print(f"{c:5s} n={r['pairs']:3d} P={r['p_genes_removed']:4d}  intercept {r['primary_intercept']}  "
              f"removal {r['removal_only']['estimate']}  strict {r['strict_removal']['estimate']}  slope {r['slope']['estimate']}")
    print(json.dumps({k: v for k, v in out.items() if k == "p_sizes"}, ensure_ascii=False))
    for k in ("main", "go_only", "hallmark_only"):
        if k in out:
            print(k, json.dumps(out[k]["overall"], ensure_ascii=False))


if __name__ == "__main__":
    main()
