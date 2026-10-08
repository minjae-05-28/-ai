"""LECA under several gain/loss models, judged split-half against Vosseberg et al. 2021 gene-tree LECA.

    python scripts/leca_model_variants.py [--step fit|eval|all]
        fit   -> results/leca_models/posteriors.npz   (LECA posterior per model and root; no labels used)
        eval  -> results/leca_models/summary.json     (docs/preregistration/2026-10-08_leca_model_variants.md)

Same tree (leca2_fast.nwk, the one leca_ancestor_v2 used), roots, completeness model and no reduced-lineage multiplier as leca_ancestor_v2;
only the gain/loss constraint and the root prior change. Shared parameters (M7-M9) are chosen by the
likelihood of our genome data alone.
"""

import argparse
import hashlib
import json
import sys
from itertools import product
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
from mito_model_search import L_GRID, Q_GRID, loglik, posterior  # noqa: E402
from run_clade_ancestor import build, mrca  # noqa: E402

from organelle_evo.predict import auroc  # noqa: E402

OUT = Path("results/leca_models")
TREE = "results/phylo_tree/leca2_fast.nwk"
PICK = "data/markers/leca2_pick.json"
ROOTS = {"discoba": "Discoba", "opisthokonta": "Opisthokonta",
         "amorphea": "Opisthokonta+Amoebozoa+Apusozoa+Breviatea", "metamonada": "Metamonada"}
PI_GRID = [0.05, 0.1, 0.2, 0.3, 0.5, 0.7, 0.9]
# id: (gain/loss cap or "shared", root prior: "stationary" | "empirical" | float | "shared")
MODELS = {
    "M0": (None, "stationary"), "M1": (None, 0.5), "M2": (None, "empirical"),
    "M3": (0.3, "stationary"), "M4": (0.1, "stationary"), "M5": (0.1, 0.5), "M6": (0.01, 0.5),
    "M7": ("shared", "stationary"), "M8": (None, "shared"), "M9": ("shared", "shared"),
}


def fit_fixed(d, X, vis, qs, root_mode):
    """Per-family ML over the (loss, gain/loss) grid restricted to ratios `qs`; returns g, lo, root, total ll."""
    grid = [(lv, lv * q) for lv, q in product(L_GRID, qs)]
    lo = np.array([a for a, _ in grid], np.float32)[:, None]
    g = np.array([b for _, b in grid], np.float32)[:, None]
    mult = np.ones(len(d["parent"]), np.float32)
    emp = np.clip(X[d["tips"]].mean(0).astype(np.float32), 0.02, 0.98)
    if root_mode == "stationary":
        root = g / (g + lo) * np.ones((1, X.shape[1]), np.float32)
    elif root_mode == "empirical":
        root = emp[None, :]
    else:
        root = np.float32(root_mode)
    ll = loglik(d, X, vis, g, lo, mult, root)
    k = np.argmax(ll, axis=0)
    fi = np.arange(X.shape[1])
    g_f, lo_f = g[k, 0], lo[k, 0]
    if root_mode == "stationary":
        root_f = g_f / (g_f + lo_f)
    elif root_mode == "empirical":
        root_f = emp
    else:
        root_f = np.full(X.shape[1], root_mode, np.float32)
    return g_f, lo_f, root_f, mult, float(ll[k, fi].sum())


def run_model(d, X, vis, cap, root):
    qs_all = list(Q_GRID)
    q_opts = [[q] for q in qs_all] if cap == "shared" else [[q for q in qs_all if cap is None or q <= cap + 1e-9]]
    r_opts = PI_GRID if root == "shared" else [root]
    best = None
    for qs, r in product(q_opts, r_opts):
        g, lo, rt, mult, ll = fit_fixed(d, X, vis, qs, r)
        if best is None or ll > best[0]:
            best = (ll, g, lo, rt, mult, {"ratio": qs if cap == "shared" else cap, "root": r})
    ll, g, lo, rt, mult, chosen = best
    return posterior(d, X, vis, g, lo, mult, rt), chosen, ll


def fit_all():
    lineage = {r["organism"].replace("'", ""): r["lineage"]
               for r in json.loads(Path(PICK).read_text())["lineage"].values()}
    post, chosen, fams_ref, freq = {}, {}, None, None
    for rname, split in ROOTS.items():
        d, fams, names, in_clade, _, _ = build(TREE, set(), 100, "*", False, split, lineage)
        d["completeness"] = d["completeness_vec"]
        tips = [v for v in d["tips"] if in_clade[v]]
        node = mrca(tips, d["parent"], d["depth"])
        vis = np.zeros(len(d["parent"]), bool)
        vis[d["tips"]] = True
        if fams_ref is None:
            fams_ref, freq = fams, d["X"][tips].mean(0).astype(np.float32)
        col = {f: j for j, f in enumerate(fams)}
        idx = np.array([col.get(f, -1) for f in fams_ref])   # a root may drop stray tips, so align by name
        for mid, (cap, root) in MODELS.items():
            p, ch, ll = run_model(d, d["X"], vis, cap, root)
            post[(mid, rname)] = np.where(idx >= 0, p[node][np.maximum(idx, 0)], 0.0)
            chosen[f"{mid} {rname}"] = {**{k: (v if not isinstance(v, np.floating) else float(v)) for k, v in ch.items()},
                                         "loglik": round(ll, 1), "sum_posterior": round(float(p[node].sum()), 1)}
            print(f"{rname} {mid}: sum P {p[node].sum():.0f}  chosen {ch}  ll {ll:.0f}", flush=True)
    OUT.mkdir(parents=True, exist_ok=True)
    arr = np.stack([[post[(m, r)] for r in ROOTS] for m in MODELS])   # (model, root, family)
    np.savez_compressed(OUT / "posteriors.npz", models=list(MODELS), roots=list(ROOTS), families=fams_ref,
                        per_root=arr, clade_frequency=freq)
    (OUT / "fit.json").write_text(json.dumps(chosen, indent=1, default=float))


# ---------------------------------------------------------------- evaluation
def labels():
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    from external_benchmark_phylo import theirs
    return theirs()


def boot_diff(a, b, y, seed=0, n=2000):
    rng = np.random.default_rng(seed)
    out = []
    for _ in range(n):
        ix = rng.integers(0, len(y), len(y))
        if y[ix].min() != y[ix].max():
            out.append(auroc(a[ix], y[ix]) - auroc(b[ix], y[ix]))
    lo, hi = np.percentile(out, [2.5, 97.5])
    return round(float(lo), 4), round(float(hi), 4)


def stratified(p, freq, y):
    edges = np.quantile(freq, np.linspace(0, 1, 11))
    bins = np.clip(np.searchsorted(edges, freq, side="right") - 1, 0, 9)
    tot = w = 0
    for b in range(10):
        m = bins == b
        if m.sum() and y[m].min() != y[m].max():
            tot += auroc(p[m], y[m]) * m.sum()
            w += m.sum()
    return round(float(tot / w), 4)


def logit(p):
    p = np.clip(p, 1e-4, 1 - 1e-4)
    return np.log(p / (1 - p))


def logistic(Xtr, ytr, Xte):
    from sklearn.linear_model import LogisticRegression
    m = LogisticRegression(C=1.0, max_iter=1000).fit(Xtr, ytr)
    return m.predict_proba(Xte)[:, 1], [round(float(c), 4) for c in m.coef_[0]] + [round(float(m.intercept_[0]), 4)]


def evaluate():
    z = np.load(OUT / "posteriors.npz", allow_pickle=False)
    models = [str(m) for m in z["models"]]
    fams = [str(f) for f in z["families"]]
    leca, tested = labels()
    meta = json.loads(Path("data/eukaryotes/pfam_meta.json").read_text())
    acc = np.array([meta.get(f, {}).get("accession", "").split(".")[0] for f in fams])
    keep = np.isin(acc, list(tested))
    acc = acc[keep]
    y = np.isin(acc, list(leca)).astype(float)
    test = np.array([hashlib.md5(a.encode()).digest()[0] % 2 == 1 for a in acc])
    cal = ~test
    freq = z["clade_frequency"][keep].astype(float)
    P = {m: z["per_root"][i][:, keep].min(0).astype(float) for i, m in enumerate(models)}

    # Learned models: trained on the calibration half only.
    lf = np.log(np.clip(freq, 1e-3, 1))
    best_tree = max((m for m in models if m != "M0"), key=lambda m: auroc(P[m][cal], y[cal]))
    learned, coefs = {}, {}
    for sid, cols in {"S1": [lf], "S2": [lf, logit(P["M0"])], "S3": [lf, logit(P[best_tree])]}.items():
        Xf = np.column_stack(cols)
        learned[sid] = np.zeros(len(y))
        learned[sid][test], coefs[sid] = logistic(Xf[cal], y[cal], Xf[test])
        # calibration-half score by 5-fold cross-validation inside the half, so the selection does not
        # favour the learned models for having seen those labels
        ci = np.flatnonzero(cal)
        fold = np.random.default_rng(0).integers(0, 5, len(ci))
        for k in range(5):
            tr, te = ci[fold != k], ci[fold == k]
            learned[sid][te], _ = logistic(Xf[tr], y[tr], Xf[te])
    allp = {**P, **learned}

    rows = {}
    for m, p in allp.items():
        rows[m] = {
            "calibration_auroc": round(float(auroc(p[cal], y[cal])), 4),
            "test_auroc": round(float(auroc(p[test], y[test])), 4),
            "test_frequency_auroc": round(float(auroc(freq[test], y[test])), 4),
            "test_minus_frequency": round(float(auroc(p[test], y[test]) - auroc(freq[test], y[test])), 4),
            "test_minus_frequency_ci95": boot_diff(p[test], freq[test], y[test]),
            "test_stratified_auroc": stratified(p[test], freq[test], y[test]),
            "test_size_ratio": round(float(p[test].sum() / y[test].sum()), 3),
        }
    chosen = max(rows, key=lambda m: rows[m]["calibration_auroc"])
    lo, hi = rows[chosen]["test_minus_frequency_ci95"]
    verdict = "양성" if lo > 0 else ("음성" if hi < 0 else "무승부")
    res = {"preregistration": "docs/preregistration/2026-10-08_leca_model_variants.md",
           "n_calibration": int(cal.sum()), "n_test": int(test.sum()),
           "lecas_calibration": int(y[cal].sum()), "lecas_test": int(y[test].sum()),
           "best_tree_model_on_calibration": best_tree, "chosen_by_calibration_auroc": chosen,
           "verdict_on_test": verdict, "learned_coefficients": coefs,
           "fit": json.loads((OUT / "fit.json").read_text()), "models": rows}
    (OUT / "summary.json").write_text(json.dumps(res, ensure_ascii=False, indent=1))
    print(f"calibration {cal.sum()} / test {test.sum()}; chosen {chosen} -> {verdict}; best tree model {best_tree}")
    print(f"{'model':5} {'cal':>7} {'test':>7} {'freq':>7} {'diff':>8} {'ci95':>18} {'strat':>6} {'size':>6}")
    for m, r in rows.items():
        print(f"{m:5} {r['calibration_auroc']:7.4f} {r['test_auroc']:7.4f} {r['test_frequency_auroc']:7.4f} "
              f"{r['test_minus_frequency']:+8.4f} {str(r['test_minus_frequency_ci95']):>18} "
              f"{r['test_stratified_auroc']:6.3f} {r['test_size_ratio']:6.3f}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--step", default="all", choices=["fit", "eval", "all"])
    a = ap.parse_args()
    if a.step in ("fit", "all"):
        fit_all()
    if a.step in ("eval", "all"):
        evaluate()


if __name__ == "__main__":
    main()
