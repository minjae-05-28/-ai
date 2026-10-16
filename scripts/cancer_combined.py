"""Does tilt + proliferation pick out stage I cancer better than proliferation alone? Held-out half
(pre-registration 22, docs/preregistration/2026-10-16_cancer_combined_detection.md).

    python scripts/cancer_combined.py   -> results/cancer_atavism/combined.json
"""

import hashlib
import json
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import cancer_atavism as ca  # noqa: E402
from cancer_stage import DATA, auroc  # noqa: E402

OUT = Path("results/cancer_atavism/combined.json")


def logistic(X, y, iters=50, ridge=1e-6):
    """Plain logistic regression by Newton steps (intercept added); returns coefficients."""
    A = np.column_stack([np.ones(len(y)), X])
    w = np.zeros(A.shape[1])
    for _ in range(iters):
        p = 1 / (1 + np.exp(-A @ w))
        g = A.T @ (y - p)
        H = A.T @ (A * (p * (1 - p))[:, None]) + ridge * np.eye(len(w))
        step = np.linalg.solve(H, g)
        w += step
        if np.abs(step).max() < 1e-8:
            break
    return w


def score(w, X):
    return np.column_stack([np.ones(len(X)), X]) @ w


def is_train(sample):
    return hashlib.md5(sample[:12].encode()).digest()[0] % 2 == 0


def cohort(path):
    rows = [line.split("\t") for line in path.read_text().splitlines()[1:]]
    sample = [r[0] for r in rows]
    kind = np.array([r[1] for r in rows])
    stage = np.array([int(r[2]) if r[2] else 0 for r in rows])
    d = np.array([float(r[3]) for r in rows])
    s = np.array([float(r[4]) for r in rows])
    use = ((kind == "tumour") & (stage == 1)) | (kind == "normal")
    y = (kind == "tumour").astype(float)
    tr = np.array([is_train(x) for x in sample])
    a, b = use & tr, use & ~tr
    n = {"train_tumour": int((a & (y == 1)).sum()), "train_normal": int((a & (y == 0)).sum()),
         "test_tumour": int((b & (y == 1)).sum()), "test_normal": int((b & (y == 0)).sum())}
    if (kind == "normal").sum() < 10 or ((kind == "tumour") & (stage == 1)).sum() < 10:
        return None
    if min(n["test_tumour"], n["test_normal"], n["train_tumour"], n["train_normal"]) < 5:
        return {**n, "skipped": True}
    wa = logistic(s[a, None], y[a])
    wb = logistic(np.column_stack([d[a], s[a]]), y[a])
    wd = logistic(d[a, None], y[a])
    sa, sb, sd = score(wa, s[b, None]), score(wb, np.column_stack([d[b], s[b]])), score(wd, d[b, None])
    nm = a & (y == 0)
    z = lambda v: (v - v[nm].mean()) / (v[nm].std() + 1e-12)
    sz = (z(d) + z(s))[b]
    yb = y[b]
    pos, neg = np.where(yb == 1)[0], np.where(yb == 0)[0]
    rng = np.random.default_rng(ca.SEED)
    diffs = []
    for _ in range(ca.N_BOOT):
        p_, n_ = rng.choice(pos, len(pos)), rng.choice(neg, len(neg))
        diffs.append(auroc(sb[p_], sb[n_]) - auroc(sa[p_], sa[n_]))
    est = auroc(sb[pos], sb[neg]) - auroc(sa[pos], sa[neg])
    lo, hi = np.percentile(diffs, [2.5, 97.5])
    return {**n, "auroc_s_only": round(auroc(sa[pos], sa[neg]), 4), "auroc_combined": round(auroc(sb[pos], sb[neg]), 4),
            "auroc_delta_only": round(auroc(sd[pos], sd[neg]), 4), "auroc_z_sum": round(auroc(sz[pos], sz[neg]), 4),
            "difference": {"estimate": round(float(est), 4), "lo": round(float(lo), 4), "hi": round(float(hi), 4),
                           "verdict": "양성" if lo > 0 else ("음성" if hi < 0 else "무승부")}}


def main():
    res = {}
    for p in sorted(DATA.glob("*.tsv")):
        r = cohort(p)
        if r is not None:
            res[p.stem] = r
    done = {k: v for k, v in res.items() if "difference" in v}
    v = [r["difference"]["verdict"] for r in done.values()]
    n, pos, neg = len(v), v.count("양성"), v.count("음성")
    out = {"overall": {"cohorts": n, "positive": pos, "negative": neg, "draw": n - pos - neg,
                       "call": "지지" if pos >= 2 * n / 3 else ("반대" if neg >= 2 * n / 3 else "판단 보류")},
           "median_auroc": {k: round(float(np.median([r[k] for r in done.values()])), 4)
                            for k in ("auroc_s_only", "auroc_combined", "auroc_delta_only", "auroc_z_sum")},
           "cohorts": res}
    OUT.write_text(json.dumps(out, ensure_ascii=False, indent=1))
    for c, r in res.items():
        print(c, r)
    print(json.dumps({k: v for k, v in out.items() if k != "cohorts"}, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
