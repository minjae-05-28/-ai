"""Do tumours lean towards unicellular-era genes? Paired TCGA test (pre-registration 17,
docs/preregistration/2026-10-16_cancer_atavism.md).

    python scripts/cancer_atavism.py   -> results/cancer_atavism/summary.json
"""

import gzip
import json
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))

import os
DATA = Path(os.environ.get("TCGA_DIR", "data/tcga_qc"))   # QC pairs (pre-registration 17, deviation 1)
OUT = Path("results/cancer_atavism")
AGES = Path("results/human_gene_ages/gene_ages.tsv")
N_BOOT, SEED = 2000, 0


def load_ages():
    """symbol -> (primary age, oldest-domain age, grade, domains); youngest primary age wins for a symbol."""
    out = {}
    with open(AGES) as f:
        head = next(f).rstrip("\n").split("\t")
        for line in f:
            r = dict(zip(head, line.rstrip("\n").split("\t")))
            g = r["gene"]
            if not g:
                continue
            a = int(r["age_stratum"][2:])
            rec = (a, int(r["age_oldest_domain"][2:]), r["grade"], set(r["domains"].split(",")))
            if g not in out or a > out[g][0]:
                out[g] = rec
    return out


def proliferation_families():
    from ancestor_atlas import module_families
    with gzip.open("results/human_gene_ages/strata_posteriors.json.gz", "rt") as f:
        fams = set(json.load(f)["families"])
    m, _ = module_families(fams)
    return set(m["mitosis"]) | set(m["chromosome"])


def delta_per_patient(lfc, uc, mc, decile):
    """δ_p: mean over expression deciles of (mean LFC of UC genes - mean LFC of MC genes)."""
    parts = []
    for k in range(10):
        u, m = uc & (decile == k), mc & (decile == k)
        if u.any() and m.any():
            parts.append(np.nanmean(lfc[:, u], 1) - np.nanmean(lfc[:, m], 1))
    return np.mean(parts, 0)


def ci(x, rng):
    idx = rng.integers(0, len(x), (N_BOOT, len(x)))
    b = x[idx].mean(1)
    lo, hi = np.percentile(b, [2.5, 97.5])
    return {"delta": round(float(x.mean()), 4), "lo": round(float(lo), 4), "hi": round(float(hi), 4),
            "verdict": "양성" if lo > 0 else ("음성" if hi < 0 else "무승부")}


def cohort(path, ages, prolif):
    from scipy.stats import spearmanr
    z = np.load(path, allow_pickle=False)
    genes = [str(g) for g in z["genes"]]
    lfc = z["lfc"].astype(np.float32)
    nm, tm = z["normal_mean"], z["tumour_mean"]
    keep = np.array([g in ages for g in genes]) & ((nm >= 1) | (tm >= 1))
    gi = np.where(keep)[0]
    G = [genes[i] for i in gi]
    L, N = lfc[:, gi], nm[gi]
    age1 = np.array([ages[g][0] for g in G])
    age2 = np.array([ages[g][1] for g in G])
    grade_a = np.array([ages[g][2] == "A" for g in G])
    no_prolif = np.array([not (ages[g][3] & prolif) for g in G])
    cuts = np.quantile(N, np.linspace(0, 1, 11)[1:-1])
    decile = np.searchsorted(cuts, N, side="right")
    rng = np.random.default_rng(SEED)

    def run(age, mask=None, uc_max=3):
        mask = np.ones(len(G), bool) if mask is None else mask
        uc, mc = mask & (age <= uc_max), mask & (age > uc_max)
        return ci(delta_per_patient(L, uc, mc, decile), np.random.default_rng(SEED))
    uc, mc = age1 <= 3, age1 > 3
    unadj = np.nanmean(L[:, uc], 1) - np.nanmean(L[:, mc], 1)
    rho = spearmanr(age1, np.nanmean(L, 0)).correlation
    del rng
    return {"pairs": int(L.shape[0]), "genes": len(G), "uc_genes": int(uc.sum()), "mc_genes": int(mc.sum()),
            "primary": run(age1),
            "unadjusted": ci(unadj, np.random.default_rng(SEED)),
            "age_slope_spearman": round(float(rho), 4),
            "sensitivity": {"a_oldest_domain": run(age2), "b_grade_A_only": run(age1, grade_a),
                            "c_PS4_as_UC": run(age1, uc_max=4), "d_no_mitosis_chromosome": run(age1, no_prolif)}}


def overall(res, key):
    v = [r[key]["verdict"] if key in r else r["sensitivity"][key]["verdict"] for r in res.values()]
    n, pos, neg = len(v), v.count("양성"), v.count("음성")
    call = "지지" if pos >= 2 * n / 3 else ("반대" if neg >= 2 * n / 3 else "판단 보류")
    return {"cohorts": n, "positive": pos, "negative": neg, "draw": n - pos - neg, "call": call}


def main():
    ages = load_ages()
    prolif = proliferation_families()
    res = {}
    for p in sorted(DATA.glob("*.npz")):
        res[p.stem] = cohort(p, ages, prolif)
        r = res[p.stem]
        print(f"{p.stem:5s} pairs {r['pairs']:3d}  primary {r['primary']}  unadjusted {r['unadjusted']['delta']}  "
              f"slope {r['age_slope_spearman']}", flush=True)
    summary = {"overall_primary": overall(res, "primary"), "overall_unadjusted": overall(res, "unadjusted"),
               "overall_sensitivity": {k: overall(res, k) for k in ["a_oldest_domain", "b_grade_A_only",
                                                                    "c_PS4_as_UC", "d_no_mitosis_chromosome"]},
               "negative_age_slope_cohorts": sum(r["age_slope_spearman"] < 0 for r in res.values()),
               "cohorts": res, "manifest": json.loads((DATA / "manifest.json").read_text())}
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=1))
    print(json.dumps({k: v for k, v in summary.items() if k not in ("cohorts", "manifest")}, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
