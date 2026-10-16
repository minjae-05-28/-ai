"""Does the tilt-SREBP link survive EMT and stemness adjustment? (pre-registration 25,
docs/preregistration/2026-10-16_tilt_vs_emt_stemness.md)

    python scripts/tilt_vs_emt.py   -> results/srebp/emt_control.json
"""

import json
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import cancer_atavism as ca  # noqa: E402
from drug_fetch import rank_center  # noqa: E402
from srebp_validation import MODULE  # noqa: E402

OUT = Path("results/srebp/emt_control.json")


def scores():
    rows = [x.split("\t") for x in Path("data/emt/scores.tsv").read_text().splitlines()[1:]]
    return {r[0]: {"lineage": r[1], "tilt": float(r[2]), "prol": float(r[3]), "emt": float(r[6]),
                   "stem": float(r[7])} for r in rows}


def resid(y, covs):
    """Residual of y after least-squares removal of the covariate columns (all already rank-centered)."""
    A = np.column_stack(covs)
    coef, *_ = np.linalg.lstsq(A, y, rcond=None)
    return y - A @ coef


def partial(y, t, covs, g, boot=True):
    """Rank-based partial correlation of y and t given covs, within lineage."""
    yr, tr = rank_center(y, g), rank_center(t, g)
    cr = [rank_center(c, g) for c in covs]
    a, b = (resid(yr, cr), resid(tr, cr)) if cr else (yr, tr)
    est = float(np.corrcoef(a, b)[0, 1])
    if not boot:
        return {"rho_partial": round(est, 4), "n": int(len(y))}
    rng = np.random.default_rng(ca.SEED)
    bs = [np.corrcoef(a[i], b[i])[0, 1] for i in (rng.integers(0, len(y), len(y)) for _ in range(ca.N_BOOT))]
    lo, hi = np.percentile(bs, [2.5, 97.5])
    return {"rho_partial": round(est, 4), "lo": round(float(lo), 4), "hi": round(float(hi), 4), "n": int(len(y)),
            "verdict": "양성" if hi < 0 else ("음성" if lo > 0 else "무승부")}


def arm(name, lines, mod, S):
    g = np.array([S[l]["lineage"] for l in lines])
    t = np.array([S[l]["tilt"] for l in lines])
    p = np.array([S[l]["prol"] for l in lines])
    e = np.array([S[l]["emt"] for l in lines])
    s = np.array([S[l]["stem"] for l in lines])
    out = {"lines": len(lines),
           "primary_full_adjustment": partial(mod, t, [p, e, s], g),
           "steps": {"lineage_only": partial(mod, t, [], g, boot=False),
                     "plus_proliferation": partial(mod, t, [p], g, boot=False),
                     "plus_emt": partial(mod, t, [p, e], g, boot=False),
                     "plus_stemness": partial(mod, t, [p, e, s], g, boot=False)},
           "emt_vs_module_given_prol": partial(mod, e, [p], g),
           "stem_vs_module_given_prol": partial(mod, s, [p], g),
           "emt_vs_module_given_prol_tilt": partial(mod, e, [p, t], g),
           "stem_vs_module_given_prol_tilt": partial(mod, s, [p, t], g)}
    return name, out


def main():
    S = scores()
    res = {"source": json.loads(Path("data/emt/source.json").read_text())}
    lines = sorted(S)
    t = np.array([S[l]["tilt"] for l in lines])
    res["score_overlap_pearson"] = {
        k: round(float(np.corrcoef(t, np.array([S[l][k] for l in lines]))[0, 1]), 3) for k in ("prol", "emt", "stem")}
    res["emt_vs_stem"] = round(float(np.corrcoef([S[l]["emt"] for l in lines], [S[l]["stem"] for l in lines])[0, 1]), 3)
    arms = {}
    # Project Score arm: module fold changes per line
    p = Path("data/srebp/score_module.tsv")
    if p.exists():
        rows = [x.split("\t") for x in p.read_text().splitlines()[1:]]
        rows = [r for r in rows if r[0] in S]
        F = np.array([[float(v) if v not in ("", "NA", "nan") else np.nan for v in r[2:7]] for r in rows])
        ok = ~np.isnan(F).any(1)
        F, keep = F[ok], [r[0] for r, o in zip(rows, ok) if o]
        Z = (F - F.mean(0)) / (F.std(0) + 1e-9)
        name, out = arm("project_score", keep, Z.mean(1), S)
        arms[name] = out
    p = Path("data/emt/depmap_module.tsv")
    if p.exists():
        lines_ = p.read_text().splitlines()
        rows = [x.split("\t") for x in lines_[1:]]
        rows = [r for r in rows if r[0] in S]
        F = np.array([[float(v) for v in r[1:]] for r in rows])
        ok = ~np.isnan(F).any(1)
        F, keep = F[ok], [r[0] for r, o in zip(rows, ok) if o]
        Z = (F - F.mean(0)) / (F.std(0) + 1e-9)
        name, out = arm("depmap", keep, Z.mean(1), S)
        arms[name] = out
    res["arms"] = arms
    verdicts = [a["primary_full_adjustment"]["verdict"] for a in arms.values()]
    res["overall"] = {"arms": len(verdicts), "positive": verdicts.count("양성"),
                      "call": "설명 A 지지" if verdicts and all(v == "양성" for v in verdicts)
                      else ("설명 B" if verdicts and not any(v == "양성" for v in verdicts) else "판단 보류")}
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(res, ensure_ascii=False, indent=1))
    print(json.dumps(res, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
