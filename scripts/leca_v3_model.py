"""Integrated gain/loss model G3 (pre-registration 7: docs/preregistration/2026-10-10_leca_v3_model.md).

    python scripts/leca_v3_model.py [--part loso|sim|leca|all]
        -> results/leca_v3/{loso,sim,leca}.json and leca_posterior.npz

G3, all parameters from our genome data (no external labels):
  1. a prior over the (loss, gain/loss) grid learned by EM across families (nonparametric empirical
     Bayes); each family's ancestral posterior is averaged over grid points by their posterior weight
  2. separate priors for three prokaryote strata (absent from prokaryotes / < 10% / >= 10%)
  3. a loss multiplier m in {1, 2, 4, 8} on reduced lineages, chosen by marginal likelihood
  4. plastid transfer: families concentrated in plastid-bearing lineages use a fit with those tips hidden
Variants for the contribution of each part: G3a = 1, G3b = 1+2, G3c = 1+2+3, G3 = all.
"""

import argparse
import json
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
from mito_model_search import L_GRID, Q_GRID, branch_probs, loglik, posterior  # noqa: E402
from prokaryote_and_loso import GROUPS, prokaryote_shares  # noqa: E402
from leca_model_variants import PICK, ROOTS, TREE, labels  # noqa: E402
from run_clade_ancestor import build, mrca  # noqa: E402
from tree_scramble_transfer import CONTROL, PLASTID, m7  # noqa: E402

from organelle_evo.predict import auroc  # noqa: E402

OUT = Path("results/leca_v3")
GRID = [(lv, lv * q) for lv in L_GRID for q in Q_GRID]
MULTS = (1.0, 2.0, 4.0, 8.0)


def strata_of(fams, shares):
    b = np.array([shares["bacteria"].get(f, 0.0) for f in fams])
    a = np.array([shares["archaea"].get(f, 0.0) for f in fams])
    top = np.maximum(a, b)
    return np.where(top == 0, 0, np.where(top < 0.1, 1, 2))


def em_prior(ll, iters=500, tol=1e-6):
    """Nonparametric EM for prior weights over grid points; ll: (G, F) log-likelihoods."""
    G = ll.shape[0]
    w = np.full(G, 1.0 / G)
    mx = ll.max(0)
    L = np.exp(ll - mx)                       # (G, F)
    for _ in range(iters):
        num = w[:, None] * L
        R = num / num.sum(0, keepdims=True)
        w_new = R.mean(1)
        if np.abs(w_new - w).max() < tol:
            w = w_new
            break
        w = w_new
    num = w[:, None] * L
    marg = float((np.log(num.sum(0)) + mx).sum())
    return w, num / num.sum(0, keepdims=True), marg


def g3_fit(d, vis, strata, use_strata=True, choose_mult=True):
    """Posterior at every node (n_nodes, F), chosen m, per-stratum priors, marginal log-likelihood."""
    X = d["X"]
    F = X.shape[1]
    g = np.array([b for _, b in GRID], np.float32)[:, None]
    lo = np.array([a for a, _ in GRID], np.float32)[:, None]
    root = (g / (g + lo)) * np.ones((1, F), np.float32)
    strata = strata if use_strata else np.zeros(F, int)
    best = None
    for m in (MULTS if choose_mult else (1.0,)):
        mult = np.where(d["reduced_branch"], m, 1.0).astype(np.float32)
        ll = loglik(d, X, vis, g, lo, mult, root).astype(np.float64)
        R = np.zeros_like(ll)
        marg, priors = 0.0, {}
        for s in np.unique(strata):
            cols = strata == s
            w, Rs, ms = em_prior(ll[:, cols])
            R[:, cols] = Rs
            marg += ms
            priors[int(s)] = w
        if best is None or marg > best[0]:
            best = (marg, m, mult, R, priors)
    marg, m, mult, R, priors = best
    post = np.zeros((len(d["parent"]), F), np.float32)
    for k, (lv, gv) in enumerate(GRID):
        if R[k].max() < 1e-6:
            continue
        gk = np.full(F, gv, np.float32)
        lk = np.full(F, lv, np.float32)
        post += R[k][None, :].astype(np.float32) * posterior(d, X, vis, gk, lk, mult, gk / (gk + lk))
    return post, {"m": m, "marginal_loglik": round(marg, 1),
                  "prior_mean_ratio": {s: round(float(sum(w[k] * GRID[k][1] / GRID[k][0] for k in range(len(GRID)))), 4)
                                       for s, w in priors.items()}}


def g3_full(d, vis, strata, plastid_tips, variant="G3"):
    """variant: G3a (EB only), G3b (+strata), G3c (+multiplier), G3 (+plastid transfer)."""
    use_strata = variant in ("G3b", "G3c", "G3")
    choose_mult = variant in ("G3c", "G3")
    post, info = g3_fit(d, vis, strata, use_strata, choose_mult)
    if variant != "G3":
        return post, info
    X = d["X"]
    vt = [v for v in d["tips"] if vis[v]]
    pl = [v for v in vt if v in plastid_tips]
    npl = [v for v in vt if v not in plastid_tips]
    enriched = X[pl].mean(0) > 2 * X[npl].mean(0) if pl and npl else np.zeros(X.shape[1], bool)
    vis_h = vis.copy()
    vis_h[pl] = False
    post_h, info_h = g3_fit(d, vis_h, strata, use_strata, choose_mult)
    info["plastid_enriched_families"] = int(enriched.sum())
    info["m_plastid_hidden_fit"] = info_h["m"]
    return np.where(enriched[None, :], post_h, post), info


# ---------------------------------------------------------------- shared setup
def setup(root_split):
    lin = json.loads(Path(PICK).read_text())["lineage"]
    lineage = {r["organism"].replace("'", ""): r["lineage"] for r in lin.values()}
    sg = {r["organism"].replace("'", ""): r["supergroup"] for r in lin.values()}
    d, fams, names, _, _, _ = build(TREE, set(), 100, "*", False, root_split, lineage)
    d["completeness"] = d["completeness_vec"]
    plastid = {v for v in d["tips"] if PLASTID & set(lineage.get(names[v], []))}
    return d, fams, names, sg, plastid, lineage


_SHARES = {}


def shares_for(fams):
    missing = [f for f in fams if f not in _SHARES.get("bacteria", {})]
    if missing:
        pro = prokaryote_shares(missing)
        for k in ("bacteria", "archaea"):
            _SHARES.setdefault(k, {}).update(dict(zip(missing, pro[k].tolist())))
    return _SHARES


def boot_mean_diff(per, a, b, target, n=1000, seed=0):
    rng = np.random.default_rng(seed)
    out = []
    for _ in range(n):
        ds = []
        for r in per.values():
            k = len(r[target])
            ix = rng.integers(0, k, k)
            if r[target][ix].min() != r[target][ix].max():
                ds.append(auroc(r[a][ix], r[target][ix]) - auroc(r[b][ix], r[target][ix]))
        out.append(np.mean(ds))
    lo, hi = np.percentile(out, [2.5, 97.5])
    return [round(float(lo), 4), round(float(hi), 4)]


def verdict(ci):
    return "양성" if ci[0] > 0 else ("음성" if ci[1] < 0 else "무승부")


# ---------------------------------------------------------------- 1. leave one supergroup out (primary)
def part_loso():
    d, fams, names, sg, plastid, _ = setup(ROOTS["amorphea"])
    strata = strata_of(fams, shares_for(fams))
    tips = np.array(d["tips"])
    grp = np.array([sg.get(names[v], "?") for v in tips])
    X = d["X"]
    per, info = {}, {}
    for G in GROUPS:
        gt = tips[grp == G]
        others = tips[grp != G]
        vis = np.zeros(len(d["parent"]), bool)
        vis[others] = True
        node = mrca(list(gt), d["parent"], d["depth"])
        ok = X[others].any(0)
        y = X[gt].any(0)[ok].astype(float)
        row = {"y": y, "count": X[others].mean(0)[ok].astype(float)}
        p7, _ = m7(d, vis)
        row["M7"] = p7[node][ok].astype(float)
        for var in ("G3a", "G3b", "G3c", "G3"):
            p, inf = g3_full(d, vis, strata, set(others.tolist()) & plastid, var)
            row[var] = p[node][ok].astype(float)
            if var == "G3":
                info[G] = inf
        per[G] = row
        print(f"  {G}: " + ", ".join(f"{k} {auroc(row[k], y):.4f}" for k in ("count", "M7", "G3a", "G3b", "G3c", "G3")),
              flush=True)
    res = {"groups": {G: {k: round(float(auroc(r[k], r["y"])), 4) for k in ("count", "M7", "G3a", "G3b", "G3c", "G3")}
                      for G, r in per.items()}, "fit": info}
    for a, b in (("G3", "M7"), ("G3", "count"), ("G3a", "M7"), ("G3b", "G3a"), ("G3c", "G3b"), ("G3", "G3c")):
        mean = float(np.mean([auroc(r[a], r["y"]) - auroc(r[b], r["y"]) for r in per.values()]))
        ci = boot_mean_diff(per, a, b, "y")
        res[f"{a}_minus_{b}"] = {"mean": round(mean, 4), "ci95": ci, "verdict": verdict(ci)}
    return res


# ---------------------------------------------------------------- 2. simulation from a different generator
def part_sim(n_fam=3000, seed=0):
    d, fams, names, sg, plastid, _ = setup(ROOTS["amorphea"])
    rng = np.random.default_rng(seed)
    parent, length, order = d["parent"], d["length"], d["order"]
    n = len(parent)
    lo = 0.3 * np.exp(rng.normal(0, 1, n_fam))
    g = lo * 0.15 * np.exp(rng.normal(0, 1, n_fam))
    bm = np.exp(rng.normal(0, 0.5, n)) * np.where(d["reduced_branch"], 5.0, 1.0)
    hgt = rng.random(n_fam) < 0.2
    hot = rng.random((n, n_fam)) < 0.05
    state = np.zeros((n, n_fam), bool)
    state[0] = rng.random(n_fam) < 0.5
    for v in reversed(order):                  # preorder: parents before children
        if v == 0:
            continue
        gv = g * np.where(hgt & hot[v], 20.0, 1.0)
        P00, P01, P10, P11 = branch_probs(length[v], gv, lo * bm[v])
        u = rng.random(n_fam)
        par = state[parent[v]]
        state[v] = np.where(par, u < P11, u < P01)
    comp = d["completeness_vec"]
    X = np.zeros((n, n_fam), bool)
    for v in d["tips"]:
        X[v] = state[v] & (rng.random(n_fam) < comp[v])
    keep = X[d["tips"]].sum(0) >= 1
    ds = dict(d)
    ds["X"] = X[:, keep]
    truth = state[0, keep].astype(float)
    vis = np.zeros(n, bool)
    vis[d["tips"]] = True
    p7, _ = m7(ds, vis)
    strata = np.zeros(int(keep.sum()), int)
    pg, info = g3_fit(ds, vis, strata, use_strata=False, choose_mult=True)
    count = X[d["tips"]][:, keep].mean(0).astype(float)
    s = {"G3": pg[0].astype(float), "M7": p7[0].astype(float), "count": count}
    res = {"n_families": int(keep.sum()), "root_present_share": round(float(truth.mean()), 3),
           "auroc": {k: round(float(auroc(v, truth)), 4) for k, v in s.items()},
           "size_ratio": {k: round(float(v.sum() / truth.sum()), 3) for k, v in s.items() if k != "count"},
           "fit": info}
    rng2 = np.random.default_rng(0)
    bs = []
    for _ in range(2000):
        ix = rng2.integers(0, len(truth), len(truth))
        bs.append(auroc(s["G3"][ix], truth[ix]) - auroc(s["M7"][ix], truth[ix]))
    lo_, hi_ = np.percentile(bs, [2.5, 97.5])
    res["G3_minus_M7"] = {"mean": round(res["auroc"]["G3"] - res["auroc"]["M7"], 4),
                          "ci95": [round(float(lo_), 4), round(float(hi_), 4)]}
    return res


# ---------------------------------------------------------------- 3. LECA under four roots (reference)
def part_leca():
    import hashlib
    fams_ref, per_root, info = None, [], {}
    for rname, split in ROOTS.items():
        d, fams, names, sg, plastid, _ = setup(split)
        strata = strata_of(fams, shares_for(fams))
        vis = np.zeros(len(d["parent"]), bool)
        vis[d["tips"]] = True
        node = mrca(d["tips"], d["parent"], d["depth"])
        p, inf = g3_full(d, vis, strata, plastid, "G3")
        info[rname] = inf
        if fams_ref is None:
            fams_ref = fams
            freq = d["X"][d["tips"]].mean(0).astype(float)
        col = {f: j for j, f in enumerate(fams)}
        idx = np.array([col.get(f, -1) for f in fams_ref])
        per_root.append(np.where(idx >= 0, p[node][np.maximum(idx, 0)], 0.0))
        print(f"  {rname}: m {inf['m']}, sum P {p[node].sum():.0f}", flush=True)
    P = np.stack(per_root)
    leca_p = P.min(0)
    OUT.mkdir(parents=True, exist_ok=True)
    np.savez_compressed(OUT / "leca_posterior.npz", families=fams_ref, roots=list(ROOTS), per_root=P,
                        posterior=leca_p, clade_frequency=freq)
    leca, tested = labels()
    meta = json.loads(Path("data/eukaryotes/pfam_meta.json").read_text())
    acc = np.array([meta.get(f, {}).get("accession", "").split(".")[0] for f in fams_ref])
    keep = np.isin(acc, list(tested))
    y = np.isin(acc[keep], list(leca)).astype(float)
    test = np.array([hashlib.md5(a.encode()).digest()[0] % 2 == 1 for a in acc[keep]])
    col = {f: j for j, f in enumerate(fams_ref)}
    return {"vosseberg_test_half_auroc": {"G3": round(float(auroc(leca_p[keep][test], y[test])), 4),
                                          "frequency": round(float(auroc(freq[keep][test], y[test])), 4)},
            "size_ratio_test_half": round(float(leca_p[keep][test].sum() / y[test].sum()), 3),
            "ancestor_size_per_root": {r: round(float(P[i].sum()), 1) for i, r in enumerate(ROOTS)},
            "negative_control": {f: [round(float(P[i, col[f]]), 3) for i in range(len(ROOTS))] for f in CONTROL if f in col},
            "negative_control_passed": all(max(P[i, col[f]] for i in range(len(ROOTS))) < 0.1 for f in CONTROL if f in col),
            "fit": info}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--part", default="all", choices=["loso", "sim", "leca", "all"])
    a = ap.parse_args()
    OUT.mkdir(parents=True, exist_ok=True)
    for name, fn in (("loso", part_loso), ("sim", part_sim), ("leca", part_leca)):
        if a.part in (name, "all"):
            print(f"== {name}", flush=True)
            r = fn()
            (OUT / f"{name}.json").write_text(json.dumps(r, ensure_ascii=False, indent=1, default=float))
            print(json.dumps({k: v for k, v in r.items() if k != "fit"}, ensure_ascii=False, indent=1, default=float),
                  flush=True)


if __name__ == "__main__":
    main()
