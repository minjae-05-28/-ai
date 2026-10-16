"""SREBP-SCD dependency of high-tilt cancer cells in independent data (pre-registration 24,
docs/preregistration/2026-10-16_srebp_validation.md).

    python scripts/srebp_validation.py   -> results/srebp/summary.json
"""

import json
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import cancer_atavism as ca  # noqa: E402
from drug_fetch import rank_center  # noqa: E402

S = Path("data/srebp")
OUT = Path("results/srebp")
MODULE = ["SCD", "SREBF1", "SCAP", "MBTPS1", "MBTPS2"]
TARGETS = ["SCD", "FASN", "HMGCR", "LDLR", "INSIG1", "SQLE", "HMGCS1"]


def lines():
    rows = [x.split("\t") for x in Path("data/drug/lines.tsv").read_text().splitlines()[1:]]
    return {r[0]: (r[1], float(r[2]), float(r[3])) for r in rows}


def residuals(y, t, p, g):
    yr, tr, pr = rank_center(y, g), rank_center(t, g), rank_center(p, g)
    res = lambda a: a - (np.dot(a, pr) / np.dot(pr, pr)) * pr
    return res(yr), res(tr)


def partial_ci(y, t, p, g):
    ok = ~np.isnan(y) & ~np.isnan(t) & ~np.isnan(p)
    y, t, p, g = y[ok], t[ok], p[ok], g[ok]
    a, b = residuals(y, t, p, g)
    est = np.corrcoef(a, b)[0, 1]
    rng = np.random.default_rng(ca.SEED)
    bs = []
    for _ in range(ca.N_BOOT):
        i = rng.integers(0, len(y), len(y))
        bs.append(np.corrcoef(a[i], b[i])[0, 1])
    lo, hi = np.percentile(bs, [2.5, 97.5])
    return {"rho_partial": round(float(est), 4), "lo": round(float(lo), 4), "hi": round(float(hi), 4), "n": int(ok.sum()),
            "verdict": "양성" if hi < 0 else ("음성" if lo > 0 else "무승부")}


def project_score(L):
    path = S / "score_module.tsv"
    if not path.exists():
        return None
    rows = [x.split("\t") for x in path.read_text().splitlines()[1:]]
    rows = [r for r in rows if r[0] in L]
    F = np.array([[float(v) if v not in ("", "NA", "nan") else np.nan for v in r[2:7]] for r in rows])
    Z = (F - np.nanmean(F, 0)) / (np.nanstd(F, 0) + 1e-9)
    mod = np.nanmean(Z, 1)
    g = np.array([L[r[0]][0] for r in rows])
    t = np.array([L[r[0]][1] for r in rows])
    p = np.array([L[r[0]][2] for r in rows])
    if len(rows) < 100:
        return {"lines": len(rows), "skipped": "fewer than 100 lines"}
    out = {"lines": len(rows), "module": partial_ci(mod, t, p, g)}
    out["genes"] = {gname: partial_ci(F[:, k], t, p, g) for k, gname in enumerate(MODULE)}
    return out


def depmap_genes():
    rows = {x.split("\t")[0]: x.split("\t") for x in Path("data/drug/genes.tsv").read_text().splitlines()[1:]}
    return {g: float(rows[g][4]) for g in MODULE if g in rows}


def tumours():
    from scipy.stats import spearmanr
    ages = ca.load_ages()
    res = {}
    for path in sorted(ca.DATA.glob("*.npz")):
        z = np.load(path, allow_pickle=False)
        genes = [str(x) for x in z["genes"]]
        lfc = z["lfc"].astype(np.float32)
        nm, tm = z["normal_mean"], z["tumour_mean"]
        keep = np.array([x in ages for x in genes]) & ((nm >= 1) | (tm >= 1))
        gi = np.where(keep)[0]
        age = np.array([ages[genes[i]][0] for i in gi])
        N = nm[gi]
        cuts = np.quantile(N, np.linspace(0, 1, 11)[1:-1])
        d = ca.delta_per_patient(lfc[:, gi], age <= 3, age > 3, np.searchsorted(cuts, N, side="right"))
        ti = [genes.index(x) for x in TARGETS if x in genes]
        s = np.nanmean(lfc[:, ti], 1)
        rho = spearmanr(d, s).correlation
        res[path.stem] = {"pairs": len(d), "spearman_delta_vs_srebp_targets": round(float(rho), 4)}
    return res


def gdsc(L):
    path = S / "gdsc_lipid.tsv"
    if not path.exists():
        return None
    rows = [x.split("\t") for x in path.read_text().splitlines()[1:]]
    by = {}
    for m, drug, tg, ic in rows:
        if m in L and ic not in ("", "None"):
            by.setdefault((drug, tg), {})[m] = float(ic)
    out = {}
    for (drug, tg), v in by.items():
        ms = list(v)
        if len(ms) < 100:
            continue
        y = np.array([v[m] for m in ms])
        g = np.array([L[m][0] for m in ms])
        t = np.array([L[m][1] for m in ms])
        p = np.array([L[m][2] for m in ms])
        out[f"{drug} ({tg})"] = partial_ci(y, t, p, g)
    return out


def main():
    L = lines()
    out = {"source": json.loads((S / "source.json").read_text()), "project_score": project_score(L),
           "depmap_partial_rho_for_comparison": depmap_genes(), "tumours": tumours(), "gdsc_lipid_drugs": gdsc(L)}
    tv = [r["spearman_delta_vs_srebp_targets"] for r in out["tumours"].values()]
    out["tumours_positive"] = f"{sum(x > 0 for x in tv)} / {len(tv)}"
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "summary.json").write_text(json.dumps(out, ensure_ascii=False, indent=1))
    print(json.dumps(out, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
