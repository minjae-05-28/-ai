"""Pre-registration 4 (docs/preregistration/2026-10-09_tree_scramble_and_transfer.md).

    python scripts/tree_scramble_transfer.py   -> results/leca_models/scramble_transfer.json

A. Does the tree carry information beyond present-day frequency? The best tree model of
   pre-registration 3 (M7: one shared gain/loss ratio) on the real tree (T0), on the same tree with
   the species names shuffled (T1, five shuffles per root), and on a star tree (T2).
B. Endosymbiotic gene transfer: plastid genes spread sideways by secondary endosymbiosis read as
   ancestral presence plus losses. H1 hides every plastid-bearing tip; H2 does so only for families
   concentrated in plastid-bearing lineages.
Judged on the test half against Vosseberg et al. 2021 gene-tree LECA, as in pre-registration 3.
"""

import hashlib
import json
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
from leca_model_variants import OUT, PICK, ROOTS, TREE, labels, run_model  # noqa: E402
from run_clade_ancestor import build, mrca  # noqa: E402

from organelle_evo.predict import auroc  # noqa: E402

PLASTID = {"Viridiplantae", "Rhodophyta", "Glaucocystophyceae", "Ochrophyta", "Haptophyta", "Cryptophyceae",
           "Dinophyceae", "Euglenophyceae", "Chlorarachniophyceae", "Chromerida", "Apicomplexa", "Bolidophyceae"}
CONTROL = ["Photo_RC", "PSII", "PsbP", "Chloroa_b-bind", "PsaA_PsaB"]


def m7(d, vis):
    p, chosen, _ = run_model(d, d["X"], vis, "shared", "stationary")
    return p, chosen


def star(d):
    """Every tip hangs off the root; tip branch length = mean root-to-tip distance of the real tree.

    Built as a balanced binary tree whose internal branches have length 1e-6, which is the same model
    as a 250-way star: a single node with 250 children underflows (the product of 250 probabilities
    reaches zero in float32 and the log-likelihood becomes -inf)."""
    tips = list(d["tips"])
    L = float(np.mean(d["depth"][tips]))
    parent, length, Xrows, comp = [], [], [], []

    def add(par, bl, row=None, c=1.0):
        parent.append(par), length.append(bl), Xrows.append(row), comp.append(c)
        return len(parent) - 1

    root = add(-1, 0.0)
    level = [root]
    while len(level) * 2 < len(tips):     # internal scaffold
        level = [add(v, 1e-6) for v in level for _ in (0, 1)]
    for i, t in enumerate(tips):
        add(level[i % len(level)], L, t, float(d["completeness_vec"][t]))
    n = len(parent)
    children = [[] for _ in range(n)]
    for v in range(1, n):
        children[parent[v]].append(v)
    # internal scaffold nodes left without children would be fake tips: give each at least one tip
    assert all(children[v] for v in range(n) if Xrows[v] is None)
    order, stack, seen = [], [root], set()
    while stack:
        v = stack.pop()
        if v in seen:
            order.append(v)
            continue
        seen.add(v)
        stack.append(v)
        stack.extend(children[v])
    X = np.zeros((n, d["X"].shape[1]), bool)
    for v, r in enumerate(Xrows):
        if r is not None:
            X[v] = d["X"][r]
    return {"parent": np.array(parent), "length": np.array(length), "children": children, "order": order,
            "tips": [v for v in range(n) if not children[v]], "X": X, "completeness": np.array(comp)}


def main():
    lineage = {r["organism"].replace("'", ""): r["lineage"]
               for r in json.loads(Path(PICK).read_text())["lineage"].values()}
    fams_ref, freq, res_fit = None, None, {}
    P = {k: [] for k in ["T0", "T2", "H1", "H2"] + [f"T1_{s}" for s in range(1, 6)]}
    for rname, split in ROOTS.items():
        d, fams, names, in_clade, _, _ = build(TREE, set(), 100, "*", False, split, lineage)
        d["completeness"] = d["completeness_vec"]
        tips = d["tips"]
        node = mrca(tips, d["parent"], d["depth"])
        vis = np.zeros(len(d["parent"]), bool)
        vis[tips] = True
        if fams_ref is None:
            fams_ref = fams
            freq = d["X"][tips].mean(0).astype(float)
        col = {f: j for j, f in enumerate(fams)}
        idx = np.array([col.get(f, -1) for f in fams_ref])

        def align(v):
            return np.where(idx >= 0, v[np.maximum(idx, 0)], 0.0)

        p, ch = m7(d, vis)
        P["T0"].append(align(p[node]))
        res_fit[f"T0 {rname}"] = str(ch)
        # T1: shuffle which species sits on which tip (gene table and completeness move with it)
        for s in range(1, 6):
            perm = np.random.default_rng(s).permutation(tips)
            ds = dict(d)
            X = d["X"].copy()
            X[tips] = d["X"][perm]
            comp = d["completeness_vec"].copy()
            comp[tips] = d["completeness_vec"][perm]
            ds["X"], ds["completeness"] = X, comp
            p, _ = m7(ds, vis)
            P[f"T1_{s}"].append(align(p[node]))
        # H1 / H2: plastid-bearing tips unobserved
        plastid = np.array([bool(PLASTID & set(lineage.get(names[v], []))) for v in tips])
        vis_h = vis.copy()
        vis_h[np.array(tips)[plastid]] = False
        p_h, ch_h = m7(d, vis_h)
        res_fit[f"H1 {rname}"] = str(ch_h)
        fp = d["X"][np.array(tips)[plastid]].mean(0)
        fn = d["X"][np.array(tips)[~plastid]].mean(0)
        enriched = fp > 2 * fn
        P["H1"].append(align(p_h[node]))
        P["H2"].append(np.where(align(enriched.astype(float)) > 0.5, P["H1"][-1], P["T0"][-1]))
        res_fit[f"plastid tips {rname}"] = int(plastid.sum())
        res_fit[f"enriched families {rname}"] = int(enriched.sum())
        print(f"{rname}: {plastid.sum()} plastid tips of {len(tips)}, {enriched.sum()} enriched families", flush=True)
        if rname == "discoba":
            sd = star(d)
            p, ch = m7(sd, np.ones(len(sd["parent"]), bool))
            P["T2"].append(align(p[0]))
            res_fit["T2"] = str(ch)
    mins = {k: np.min(np.stack(v), 0) for k, v in P.items()}
    perroot = {k: np.stack(v) for k, v in P.items()}

    # ---- evaluation, same families, labels and halves as pre-registration 3
    leca, tested = labels()
    meta = json.loads(Path("data/eukaryotes/pfam_meta.json").read_text())
    acc = np.array([meta.get(f, {}).get("accession", "").split(".")[0] for f in fams_ref])
    keep = np.isin(acc, list(tested))
    y = np.isin(acc[keep], list(leca)).astype(float)
    test = np.array([hashlib.md5(a.encode()).digest()[0] % 2 == 1 for a in acc[keep]])
    cal = ~test
    S = {k: v[keep] for k, v in mins.items()}
    fq = freq[keep]
    yt = y[test]

    def A(p, m=test):
        return float(auroc(p[m], y[m]))

    rng = np.random.default_rng(0)
    nt = int(test.sum())
    shuf = [f"T1_{s}" for s in range(1, 6)]

    def boot(fa, fb):
        out = []
        for _ in range(2000):
            ix = rng.integers(0, nt, nt)
            if yt[ix].min() != yt[ix].max():
                out.append(fa(ix) - fb(ix))
        lo, hi = np.percentile(out, [2.5, 97.5])
        return [round(float(lo), 4), round(float(hi), 4)]

    def sc(k):
        return lambda ix: auroc(S[k][test][ix], yt[ix])

    def shuf_mean(ix):
        return np.mean([auroc(S[k][test][ix], yt[ix]) for k in shuf])

    def verdict(ci):
        return "양성" if ci[0] > 0 else ("음성" if ci[1] < 0 else "무승부")

    t0, t1 = A(S["T0"]), float(np.mean([A(S[k]) for k in shuf]))
    ciA = boot(sc("T0"), shuf_mean)
    res = {"preregistration": "docs/preregistration/2026-10-09_tree_scramble_and_transfer.md",
           "A_tree_information": {
               "T0_real": round(t0, 4), "T1_shuffled_each": [round(A(S[k]), 4) for k in shuf],
               "T1_shuffled_mean": round(t1, 4), "T2_star": round(A(S["T2"]), 4),
               "frequency": round(A(fq), 4),
               "T0_minus_T1": {"mean": round(t0 - t1, 4), "ci95": ciA}, "verdict": verdict(ciA),
               "T0_minus_T2": {"mean": round(t0 - A(S["T2"]), 4), "ci95": boot(sc("T0"), sc("T2"))},
               "T2_minus_frequency": round(A(S["T2"]) - A(fq), 4)}}
    chosen = max(["H1", "H2"], key=lambda k: A(S[k], cal))
    ciB = boot(sc(chosen), sc("T0"))
    fam_col = {f: j for j, f in enumerate(fams_ref)}
    control = {k: {f: [round(float(perroot[k][r, fam_col[f]]), 3) for r in range(len(ROOTS))]
                   for f in CONTROL if f in fam_col} for k in ["T0", "H1", "H2"]}
    res["B_transfer"] = {
        "calibration_auroc": {k: round(A(S[k], cal), 4) for k in ["T0", "H1", "H2"]},
        "test_auroc": {k: round(A(S[k]), 4) for k in ["T0", "H1", "H2"]},
        "chosen": chosen, "chosen_minus_H0": {"mean": round(A(S[chosen]) - t0, 4), "ci95": ciB},
        "verdict": verdict(ciB),
        "chosen_minus_frequency": {"mean": round(A(S[chosen]) - A(fq), 4),
                                   "ci95": boot(sc(chosen), lambda ix: auroc(fq[test][ix], yt[ix]))},
        "negative_control_posterior_per_root": control,
        "negative_control_passed": {k: all(max(v) < 0.1 for v in c.values()) for k, c in control.items()},
        "size_ratio_test": {k: round(float(S[k][test].sum() / yt.sum()), 3) for k in ["T0", "H1", "H2"]}}
    res["fit"] = res_fit
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "scramble_transfer.json").write_text(json.dumps(res, ensure_ascii=False, indent=1))
    print(json.dumps({k: v for k, v in res.items() if k != "fit"}, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
