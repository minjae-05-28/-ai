"""Pre-registration 15: Lecio (G3c, G3c + H2) against Wagner and Dollo parsimony and simple baselines, on the
same tree (learning-loop tree after round 10, commit 2d7628f) and the same Pfam presence/absence matrix.

    python scripts/method_comparison.py      -> results/method_comparison/summary.json

A  LECA scores against Vosseberg 2021 (AUROC, F1)
B  5-fold held-out species (per-species AUROC; hard families = held by < half of the relatives)
C  stability of the LECA call set across the five 80% fits (mean Jaccard)
"""

import hashlib
import json
import subprocess
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))

OUT = Path("results/method_comparison")
TREE_COMMIT = "2d7628f"
GAIN, LOSS = 2.0, 1.0          # Wagner costs
CHUNK = 2000


# ---------------------------------------------------------------- data
def load():
    import learning_loop as ll
    import run_clade_ancestor as rca
    OUT.mkdir(parents=True, exist_ok=True)
    tree = OUT / "tree_round10.nwk"
    if not tree.exists():
        tree.write_text(subprocess.run(["git", "show", f"{TREE_COMMIT}:results/learning_loop/tree.nwk"],
                                       capture_output=True, text=True, check=True).stdout)
    base_prof = ll.compact(rca.load_profiles())
    ll.load_shares_cache()
    held = ll.compact(ll.all_new_species())
    base_lin = {r["organism"].replace("'", ""): r["lineage"]
                for r in json.loads(Path("data/markers/leca2_pick.json").read_text())["lineage"].values()}
    lin_all = {**base_lin, **{k: v["lineage"] for k, v in held.items()}}
    prof_all = {**base_prof, **{k: {**v, "kingdom": "eukaryotes"} for k, v in held.items()}}
    plain = {k.replace("'", ""): v for k, v in prof_all.items()}
    rca.load_profiles = lambda: {**prof_all, **plain}
    d, fams, names, *_ = rca.build(str(tree), set(), 100, "*", False, None, lin_all)
    names = {v: names[v] for v in d["tips"]}
    tip_lin = {v: list(lin_all.get(n, [])) for v, n in names.items()}
    return d, fams, names, tip_lin


# ---------------------------------------------------------------- parsimony
def wagner(d, Xtips, visible):
    """Two-state Sankoff parsimony, gain cost GAIN, loss cost LOSS. Returns (root score, tip score) where a
    score is 1 if presence is strictly cheaper, 0 if absence is, 0.5 on a tie; tip scores for hidden tips.
    Xtips: (n_nodes, F) bool with tip rows filled; visible: (n_nodes,) bool."""
    n, F = Xtips.shape
    children, parent, order = d["children"], d["parent"], d["order"]
    cost = np.array([[0.0, GAIN], [LOSS, 0.0]])            # cost[from, to]
    INF = 1e9
    D = np.zeros((n, 2, F), np.float32)
    for v in order:
        if not children[v]:
            if visible[v]:
                x = Xtips[v]
                D[v, 0] = np.where(x, INF, 0)
                D[v, 1] = np.where(x, 0, INF)
            continue
        for s in (0, 1):
            acc = np.zeros(F, np.float32)
            for c in children[v]:
                acc += np.minimum(cost[s, 0] + D[c, 0], cost[s, 1] + D[c, 1])
            D[v, s] = acc
    root = int(np.where(np.asarray(parent) < 0)[0][0])
    root_score = np.where(D[root, 1] < D[root, 0], 1.0, np.where(D[root, 1] > D[root, 0], 0.0, 0.5))
    U = np.zeros((n, 2, F), np.float32)
    for v in reversed(order):
        for c in children[v]:
            sib = np.zeros((2, F), np.float32)                # cost of v's other subtrees given v's state t
            for w in children[v]:
                if w != c:
                    for t in (0, 1):
                        sib[t] += np.minimum(cost[t, 0] + D[w, 0], cost[t, 1] + D[w, 1])
            for s in (0, 1):
                U[c, s] = np.minimum(cost[0, s] + U[v, 0] + sib[0], cost[1, s] + U[v, 1] + sib[1])
    tips = np.array([v for v in range(n) if not children[v]])
    tip_score = np.full((n, F), np.nan, np.float32)
    t0, t1 = U[tips, 0], U[tips, 1]
    tip_score[tips] = np.where(t1 < t0, 1.0, np.where(t1 > t0, 0.0, 0.5))
    return root_score, tip_score


def dollo(d, Xtips, visible):
    """Dollo parsimony: one gain at the common ancestor of all (visible) carriers, losses below it.
    A node is present if it has a visible carrier below it and lies at or below that common ancestor."""
    n, F = Xtips.shape
    children, parent, order = d["children"], d["parent"], d["order"]
    cnt = np.zeros((n, F), np.int32)
    for v in order:
        if not children[v]:
            cnt[v] = Xtips[v] & visible[v]
        else:
            cnt[v] = sum(cnt[c] for c in children[v])
    root = int(np.where(np.asarray(parent) < 0)[0][0])
    total = cnt[root]
    is_lca = (cnt == total[None, :]) & (total[None, :] > 0)
    child_full = np.zeros((n, F), bool)
    for v in range(n):
        for c in children[v]:
            child_full[v] |= is_lca[c]
    lca = is_lca & ~child_full
    present = (cnt > 0) & ((cnt < total[None, :]) | lca)
    root_score = present[root].astype(float)
    tip_score = np.full((n, F), np.nan, np.float32)
    for v in range(n):
        if not children[v]:
            tip_score[v] = present[parent[v]] if parent[v] >= 0 else 0
    return root_score, tip_score


# ---------------------------------------------------------------- helpers
def chunked(fn, d, X, visible):
    F = X.shape[1]
    r = np.zeros(F)
    t = np.full(X.shape, np.nan, np.float32)
    for a in range(0, F, CHUNK):
        rs, ts = fn(d, X[:, a:a + CHUNK], visible)
        r[a:a + CHUNK] = rs
        t[:, a:a + CHUNK] = ts
    return r, t


def fold_of(name):
    return hashlib.md5(name.encode()).digest()[0] % 5


def ci(diff, n=2000, seed=0):
    rng = np.random.default_rng(seed)
    bs = [diff[rng.integers(0, len(diff), len(diff))].mean() for _ in range(n)]
    lo, hi = np.percentile(bs, [2.5, 97.5])
    return {"mean": round(float(diff.mean()), 4), "ci95": [round(float(lo), 4), round(float(hi), 4)],
            "verdict": "양성" if lo > 0 else ("음성" if hi < 0 else "무승부"),
            "share_positive": round(float((diff > 0).mean()), 3)}


def boot_auroc_diff(a, b, y, n=2000, seed=0):
    from organelle_evo.predict import auroc
    rng = np.random.default_rng(seed)
    out = []
    for _ in range(n):
        ix = rng.integers(0, len(y), len(y))
        if y[ix].min() != y[ix].max():
            out.append(auroc(a[ix], y[ix]) - auroc(b[ix], y[ix]))
    lo, hi = np.percentile(out, [2.5, 97.5])
    m = float(auroc(a, y) - auroc(b, y))
    return {"diff": round(m, 4), "ci95": [round(float(lo), 4), round(float(hi), 4)],
            "verdict": "양성" if lo > 0 else ("음성" if hi < 0 else "무승부")}


def f1(score, y):
    call = score >= 0.5
    tp = (call & (y == 1)).sum()
    prec = tp / max(call.sum(), 1)
    rec = tp / max((y == 1).sum(), 1)
    return round(float(2 * prec * rec / max(prec + rec, 1e-9)), 4)


def lecio_fit(d, fams, tip_lin, nodes, vis):
    """G3c and G3c + H2 posteriors at `nodes` (H2 applied at nodes whose tips are mostly not plastid-bearing)."""
    import learning_loop as ll
    from tree_scramble_transfer import PLASTID
    post, _, info = ll.fit_model(d, fams, nodes, vis=vis)
    tips = np.array(d["tips"])
    plastid = np.array([bool(PLASTID & set(tip_lin[v])) for v in d["tips"]])
    vt = vis[tips]
    X = d["X"][tips]
    enriched = X[plastid & vt].mean(0) > 2 * X[~plastid & vt].mean(0)
    vis_h = vis.copy()
    vis_h[tips[plastid]] = False
    post_h, _, _ = ll.fit_model(d, fams, nodes, vis=vis_h)
    is_pl = np.zeros(len(d["parent"]))
    is_pl[tips] = plastid
    cnt, tot = np.zeros(len(d["parent"])), np.zeros(len(d["parent"]))
    for v in d["order"]:
        if not d["children"][v]:
            cnt[v], tot[v] = is_pl[v], 1
        else:
            cnt[v] = sum(cnt[c] for c in d["children"][v])
            tot[v] = sum(tot[c] for c in d["children"][v])
    h2 = {v: (np.where(enriched, post_h[v], post[v]) if cnt[v] < 0.5 * tot[v] else post[v]) for v in nodes}
    return {v: post[v] for v in nodes}, h2, info


# ---------------------------------------------------------------- main
def main():
    from external_benchmark_phylo import theirs
    from organelle_evo.predict import auroc
    d, fams, names, tip_lin = load()
    n = len(d["parent"])
    tips = np.array(d["tips"])
    root = int(np.where(d["parent"] < 0)[0][0])
    X = np.zeros((n, len(fams)), bool)
    X[tips] = d["X"][tips]
    print(f"tree {len(tips)} tips, {len(fams)} families", flush=True)

    # ---- A: LECA vs Vosseberg (all tips visible)
    vis_all = np.zeros(n, bool)
    vis_all[tips] = True
    g3, h2, _ = lecio_fit(d, fams, tip_lin, [root], vis_all)
    wag_root, _ = chunked(wagner, d, X, vis_all)
    dol_root, _ = chunked(dollo, d, X, vis_all)
    freq = X[tips].mean(0)
    meta = json.loads(Path("data/eukaryotes/pfam_meta.json").read_text())
    acc = {f: (meta.get(f, {}).get("accession") or "").split(".")[0] for f in fams}
    leca, tested = theirs()
    js = np.array([j for j, f in enumerate(fams) if acc[f] in tested])
    y = np.array([acc[fams[j]] in leca for j in js], float)
    scores = {"Lecio (G3c+H2)": h2[root][js], "G3c": g3[root][js], "Wagner": wag_root[js], "Dollo": dol_root[js],
              "frequency": freq[js]}
    A = {"n_families": int(len(js)), "n_leca": int(y.sum()),
         "auroc": {k: round(float(auroc(v, y)), 4) for k, v in scores.items()},
         "f1": {k: f1(v, y) for k, v in scores.items() if k != "frequency"},
         "leca_calls": {k: int((v >= 0.5).sum()) for k, v in [("Lecio (G3c+H2)", h2[root]), ("G3c", g3[root]),
                                                               ("Wagner", wag_root), ("Dollo", dol_root)]},
         "primary_lecio_minus_wagner": boot_auroc_diff(scores["Lecio (G3c+H2)"], scores["Wagner"], y),
         "lecio_minus_dollo": boot_auroc_diff(scores["Lecio (G3c+H2)"], scores["Dollo"], y),
         "lecio_minus_frequency": boot_auroc_diff(scores["Lecio (G3c+H2)"], scores["frequency"], y)}
    print(json.dumps({"A": A}, ensure_ascii=False, indent=1), flush=True)

    # ---- B + C: five folds of held-out species
    fold = np.array([fold_of(names[v]) for v in tips])
    rows, leca_sets = [], {"Lecio (G3c+H2)": [], "G3c": [], "Wagner": [], "Dollo": []}
    for k in range(5):
        hidden = tips[fold == k]
        vis = vis_all.copy()
        vis[hidden] = False
        g3k, h2k, _ = lecio_fit(d, fams, tip_lin, [root] + [int(v) for v in hidden], vis)
        wr, wt = chunked(wagner, d, X, vis)
        dr, dt = chunked(dollo, d, X, vis)
        for name, s in [("Lecio (G3c+H2)", h2k[root]), ("G3c", g3k[root]), ("Wagner", wr), ("Dollo", dr)]:
            leca_sets[name].append(set(np.flatnonzero(s >= 0.5).tolist()))
        vis_tips = [v for v in tips if vis[v]]
        for v in hidden:
            L = set(tip_lin[v][:-1])
            cands = [(sum(t in tip_lin[u] for u in vis_tips), t) for t in L if t]
            cands = [c for c in cands if c[0] > 0]
            rel = [u for u in vis_tips if min(cands)[1] in tip_lin[u]] if cands else []
            relp = X[rel].mean(0) if rel else X[vis_tips].mean(0)
            truth = X[v].astype(float)
            if truth.min() == truth.max():
                continue
            r = {"species": names[v], "fold": k, "n_relatives": len(rel),
                 "Lecio (G3c)": float(auroc(g3k[v], truth)), "Wagner": float(auroc(wt[v], truth)),
                 "Dollo": float(auroc(dt[v], truth)), "relatives": float(auroc(relp, truth))}
            hard = relp < 0.5
            if rel and truth[hard].min() != truth[hard].max():
                for key, s in [("Lecio (G3c)", g3k[v]), ("Wagner", wt[v]), ("Dollo", dt[v]), ("relatives", relp)]:
                    r["hard_" + key] = float(auroc(s[hard], truth[hard]))
            rows.append(r)
        print(f"fold {k}: {len(hidden)} hidden species, {len(rows)} scored so far", flush=True)
    M = {k: np.array([r[k] for r in rows]) for k in ("Lecio (G3c)", "Wagner", "Dollo", "relatives")}
    hard_rows = [r for r in rows if "hard_Wagner" in r]
    H = {k: np.array([r["hard_" + k] for r in hard_rows]) for k in ("Lecio (G3c)", "Wagner", "Dollo", "relatives")}
    B = {"n_species": len(rows), "mean_auroc": {k: round(float(v.mean()), 4) for k, v in M.items()},
         "primary_lecio_minus_wagner": ci(M["Lecio (G3c)"] - M["Wagner"]),
         "lecio_minus_dollo": ci(M["Lecio (G3c)"] - M["Dollo"]),
         "lecio_minus_relatives": ci(M["Lecio (G3c)"] - M["relatives"]),
         "hard": {"n_species": len(hard_rows), "mean_auroc": {k: round(float(v.mean()), 4) for k, v in H.items()},
                  "lecio_minus_wagner": ci(H["Lecio (G3c)"] - H["Wagner"]),
                  "lecio_minus_relatives": ci(H["Lecio (G3c)"] - H["relatives"])}}

    def jacc(sets):
        vals = [len(a & b) / max(len(a | b), 1) for i, a in enumerate(sets) for b in sets[i + 1:]]
        return round(float(np.mean(vals)), 4)
    C = {k: {"mean_jaccard": jacc(v), "sizes": [len(s) for s in v]} for k, v in leca_sets.items()}
    summary = {"preregistration": "docs/preregistration/2026-10-12_method_comparison.md", "tree_commit": TREE_COMMIT,
               "tree_tips": int(len(tips)), "families": len(fams), "A_leca_vs_vosseberg": A,
               "B_heldout_species": B, "C_leca_stability": C}
    (OUT / "summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=1))
    (OUT / "species.json").write_text(json.dumps(rows, ensure_ascii=False))
    print(json.dumps({"B": B, "C": C}, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
