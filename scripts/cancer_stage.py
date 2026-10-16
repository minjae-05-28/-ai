"""Is the unicellular tilt already there in stage I? (pre-registration 20,
docs/preregistration/2026-10-16_cancer_atavism_stage.md)

    python scripts/cancer_stage.py   -> results/cancer_atavism/stage.json
"""

import json
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import cancer_atavism as ca  # noqa: E402
import cancer_proliferation as cp  # noqa: E402
from cancer_composition import fit  # noqa: E402

DATA = Path("data/tcga_stage")
OUT = Path("results/cancer_atavism/stage.json")


def auroc(pos, neg):
    from scipy.stats import mannwhitneyu
    return float(mannwhitneyu(pos, neg).statistic / (len(pos) * len(neg)))


def load(path):
    rows = [line.split("\t") for line in path.read_text().splitlines()[1:]]
    kind = np.array([r[1] for r in rows])
    stage = np.array([int(r[2]) if r[2] else 0 for r in rows])
    v = np.array([[float(x) for x in r[3:7]] for r in rows])
    return kind, stage, v[:, 0], v[:, 1], v[:, 2], v[:, 3]


def cohort(path):
    from scipy.stats import spearmanr
    kind, stage, d, s, i, t = load(path)
    tum, nor = kind == "tumour", kind == "normal"
    st1 = tum & (stage == 1)
    out = {"tumours": int(tum.sum()), "normals": int(nor.sum()),
           "by_stage": {str(k): int((tum & (stage == k)).sum()) for k in range(1, 5)}}
    if st1.sum() >= 10:
        x = d[st1]
        out["stage1_delta"] = cp.verdict(x.mean(), cp.boot(lambda idx: x[idx].mean(), len(x)))
        y, S, I, T = d[st1], s[st1], i[st1], t[st1]
        c = fit(y, [S, I, T])
        b = cp.boot(lambda idx: fit(y[idx], [S[idx], I[idx], T[idx]]), len(y))
        out["stage1_adjusted_intercept"] = cp.verdict(c[0], b[:, 0])
        if nor.sum() >= 10:
            out["stage1_vs_normal_auroc"] = {"delta": round(auroc(d[st1], d[nor]), 4),
                                             "proliferation_s": round(auroc(s[st1], s[nor]), 4)}
    staged = tum & (stage > 0)
    if sum((tum & (stage == k)).sum() >= 10 for k in range(1, 5)) >= 2:
        y, g = d[staged], stage[staged].astype(float)
        rho = spearmanr(y, g).correlation
        bv = cp.boot(lambda idx: spearmanr(y[idx], g[idx]).correlation, len(y))
        out["stage_trend_spearman"] = cp.verdict(rho, bv)
        S, I, T = s[staged], i[staged], t[staged]
        c = fit(y, [S, I, T, g])
        b = cp.boot(lambda idx: fit(y[idx], [S[idx], I[idx], T[idx], g[idx]]), len(y))
        out["stage_effect_adjusted"] = cp.verdict(c[4], b[:, 4])
    return out


def overall(res, key):
    v = [r[key]["verdict"] for r in res.values() if key in r]
    n, pos, neg = len(v), v.count("양성"), v.count("음성")
    call = "지지" if n and pos >= 2 * n / 3 else ("반대" if n and neg >= 2 * n / 3 else "판단 보류")
    return {"cohorts": n, "positive": pos, "negative": neg, "draw": n - pos - neg, "call": call}


def main():
    res = {p.stem: cohort(p) for p in sorted(DATA.glob("*.tsv"))}
    au = [r["stage1_vs_normal_auroc"] for r in res.values() if "stage1_vs_normal_auroc" in r]
    out = {"overall_stage1": overall(res, "stage1_delta"),
           "overall_stage1_adjusted": overall(res, "stage1_adjusted_intercept"),
           "overall_trend": overall(res, "stage_trend_spearman"),
           "overall_trend_adjusted": overall(res, "stage_effect_adjusted"),
           "auroc_summary": {"cohorts": len(au), "delta_ge_0.8": sum(a["delta"] >= 0.8 for a in au),
                             "delta_beats_s": sum(a["delta"] > a["proliferation_s"] for a in au),
                             "median_delta": round(float(np.median([a["delta"] for a in au])), 4) if au else None,
                             "median_s": round(float(np.median([a["proliferation_s"] for a in au])), 4) if au else None},
           "cohorts": res, "manifest": json.loads((DATA / "manifest.json").read_text())}
    OUT.write_text(json.dumps(out, ensure_ascii=False, indent=1))
    for c, r in res.items():
        print(c, r["by_stage"], r.get("stage1_delta"), r.get("stage1_vs_normal_auroc"), r.get("stage_trend_spearman"))
    print(json.dumps({k: v for k, v in out.items() if k not in ("cohorts", "manifest")}, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
