"""Model search for the mitochondrial-ancestor reconstruction: enumerate every candidate model,
score each on criteria that do not use the expected answer, iterate, keep the best.

    python scripts/mito_model_search.py --round 1 --shard 0 --n-shards 1   # evaluate models
    python scripts/mito_model_search.py --round 1 --rank                    # rank a finished round

A model = (gain/loss bound, root prior, genome filter, loss multiplier on reduced lineages).
Selection criteria (the Reclinomonas positive control is reported but never used to select):
  sim        simulation on the real pruned GTDB tree with known truth: several generators with
             lineage-specific loss acceleration in reduced orders, incomplete tips (real BUSCO),
             horizontal gains. Scored at the alphaproteobacterial root: log-loss, Brier, AUROC and
             size bias (expected minus true family count, relative). Primary criterion.
  hide       real data, whole orders hidden in turn; their tips are predicted through the deep
             backbone. Log-loss and AUROC over hidden tips x families.
  stable     how much the alphaproteobacterial-root posterior moves when each order is removed
             (mean absolute change).
Ranking: mean rank over sim log-loss, hide log-loss and stability; sim log-loss breaks ties.
Families: a fixed stratified sample (default 1,500) for the search; the winner is rerun on all.
Stopping rule (applied by whoever reads the rounds): the top model is unchanged for two rounds and
its lead over the second exceeds the bootstrap interval of the difference.
"""

import argparse
import gzip
import json
import sys
from itertools import product
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
from run_mito_ancestor import RECLINOMONAS_CORE, key, parse_newick, postorder, prune  # noqa: E402

from organelle_evo.predict import auroc  # noqa: E402

OUT = Path("results/mito_models")
CACHE = Path("results/mito_models/cache.npz")
REDUCED_ORDERS = ("o__Rickettsiales", "o__Holosporales", "o__Pelagibacterales", "o__Paracaedibacterales",
                  "o__Caedimonadales")
HIDE_ORDERS = ("o__Rhizobiales", "o__Rhodobacterales", "o__Sphingomonadales", "o__Acetobacterales",
               "o__Caulobacterales", "o__Rickettsiales")
L_GRID = np.array([0.03, 0.1, 0.3, 1.0, 3.0, 10.0], dtype=np.float32)
Q_GRID = np.array([0.01, 0.03, 0.1, 0.2, 0.3, 0.5, 1.0, 3.0, 10.0], dtype=np.float32)  # gain / loss


# ---- data ----------------------------------------------------------------------------------------

def build_cache(n_outgroup=300, n_families=1500, seed=0):
    import csv
    import re

    csv.field_size_limit(10**8)
    reps = {}
    for r in csv.DictReader(gzip.open("data/gtdb/species_reps.tsv.gz", "rt"), delimiter="\t"):
        tax = r["gtdb_taxonomy"]
        if "c__Alphaproteobacteria" in tax or "c__Gammaproteobacteria" in tax:
            reps.setdefault(key(r["ncbi_organism_name"]), (r["accession"], tax, r["ncbi_genome_category"]))
    prot = {}
    for f in sorted(Path("data/uniprot/shards").glob("*.json.gz")):
        for p in json.loads(gzip.open(f, "rt").read()).values():
            k = key(p["organism"])
            if p.get("kingdom") == "bacteria" and k in reps and k not in prot:
                b = re.search(r"C:([\d.]+)%", p.get("busco") or "")
                prot[k] = (set(p["pfam"]), float(b.group(1)) if b else np.nan)
    alpha = [k for k in prot if "c__Alphaproteobacteria" in reps[k][1]]
    gamma = sorted(k for k in prot if "c__Gammaproteobacteria" in reps[k][1])
    rng = np.random.default_rng(seed)
    gamma = list(rng.choice(gamma, min(n_outgroup, len(gamma)), replace=False))
    tips = {reps[k][0]: k for k in alpha + gamma}
    parent, length, label = parse_newick(gzip.open("results/phylo_tree/gtdb_bac120.tree.gz", "rt").read())
    node = {lab: i for i, lab in enumerate(label) if lab in tips}
    parent, length, label, _ = prune(parent, length, label, list(node.values()))
    order, children = postorder(parent)
    tipnodes = [v for v in range(len(parent)) if not children[v]]
    counts = {}
    for v in tipnodes:
        for fam in prot[tips[label[v]]][0]:
            counts[fam] = counts.get(fam, 0) + 1
    fams_all = sorted(f for f, c in counts.items() if c >= 3)
    freq = np.array([counts[f] for f in fams_all]) / len(tipnodes)
    # Stratified sample over frequency deciles, so rare and common families are both tested.
    bins = np.digitize(freq, np.quantile(freq, np.linspace(0, 1, 11)[1:-1]))
    pick = np.concatenate([rng.choice(np.flatnonzero(bins == b), min(n_families // 10, (bins == b).sum()), replace=False)
                           for b in range(10)])
    fams = [fams_all[j] for j in sorted(pick)]
    col = {f: j for j, f in enumerate(fams)}
    X = np.zeros((len(parent), len(fams)), dtype=bool)
    busco = np.full(len(parent), np.nan)
    mag = np.zeros(len(parent), dtype=bool)
    order_of = np.array([""] * len(parent), dtype=object)
    is_alpha = np.zeros(len(parent), dtype=bool)
    for v in tipnodes:
        k = tips[label[v]]
        X[v, [col[f] for f in prot[k][0] if f in col]] = True
        busco[v] = prot[k][1]
        acc, tax, cat = reps[k]
        mag[v] = cat == "derived from metagenome"
        order_of[v] = tax.split(";")[3]
        is_alpha[v] = "c__Alphaproteobacteria" in tax
    OUT.mkdir(parents=True, exist_ok=True)
    np.savez_compressed(CACHE, parent=parent, length=length, X=X, busco=busco, mag=mag, order_of=order_of.astype(str),
                        is_alpha=is_alpha, fams=np.array(fams))
    print(f"cache: {len(tipnodes)} tips, {len(parent)} nodes, {len(fams)} of {len(fams_all)} families")


def load_cache():
    z = np.load(CACHE, allow_pickle=False)
    parent = z["parent"]
    order, children = postorder(parent)
    d = {k: z[k] for k in z.files}
    d.update(order=order, children=children)
    depth = np.zeros(len(parent))
    for v in reversed(order):
        if v:
            depth[v] = depth[parent[v]] + d["length"][v]
    d["depth"] = depth
    tips = [v for v in range(len(parent)) if not children[v]]
    d["tips"] = tips
    alpha_tips = [v for v in tips if d["is_alpha"][v]]
    d["alpha_root"] = mrca(alpha_tips, parent, depth)
    # loss multiplier applies to every branch whose subtree lies inside a reduced order
    inside = np.zeros(len(parent), dtype=bool)
    for o in REDUCED_ORDERS:
        members = [v for v in tips if d["order_of"][v] == o]
        if len(members) >= 1:
            top = mrca(members, parent, depth) if len(members) > 1 else members[0]
            stack = [top]
            while stack:
                u = stack.pop()
                inside[u] = True
                stack.extend(children[u])
    d["reduced_branch"] = inside
    return d


def mrca(nodes, parent, depth):
    common = None
    for u in nodes:
        s, w = set(), u
        while w != -1:
            s.add(w)
            w = parent[w]
        common = s if common is None else common & s
    return max(common, key=lambda x: depth[x])


# ---- model ---------------------------------------------------------------------------------------

def branch_probs(t, g, lo):
    r = g + lo
    pi = g / r
    e = np.exp(-r * t)
    p01, p10 = pi * (1 - e), (1 - pi) * (1 - e)
    return 1 - p01, p01, p10, 1 - p10


def tip_message(d, X, v):
    """Likelihood of what was OBSERVED at a tip, given the tip's true state (absent, present).

    An incomplete proteome misses a share of the genes it really has, so an observed absence is
    not proof of absence. With the tip's completeness c, P(observe present | present) = c and
    P(observe absent | present) = 1 - c, while an observed presence is never a false positive.
    c = 1 gives back the plain indicator, so runs without a completeness vector are unchanged.
    """
    x = X[v].astype(np.float32)
    comp = d.get("completeness")
    if comp is None:
        return 1 - x, x
    c = np.float32(comp[v])
    return 1 - x, x * c + (1 - x) * (1 - c)


def loglik(d, X, visible, g, lo, mult, root):
    """Log-likelihood per (grid, family). g, lo: (G, 1) or (F,); root: P(present) at the root."""
    msg, logs = {}, 0.0
    children, length = d["children"], d["length"]
    shape = np.broadcast_shapes(np.shape(g), (1, X.shape[1]))
    for v in d["order"]:
        if not children[v]:
            if visible[v]:
                m0, m1 = tip_message(d, X, v)
                msg[v] = (np.broadcast_to(m0, shape), np.broadcast_to(m1, shape))
            else:
                msg[v] = (np.ones(shape, np.float32), np.ones(shape, np.float32))
            continue
        L0 = np.ones(shape, np.float32)
        L1 = np.ones(shape, np.float32)
        for c in children[v]:
            c0, c1 = msg.pop(c)
            P00, P01, P10, P11 = branch_probs(length[c], g, lo * mult[c])
            L0 *= P00 * c0 + P01 * c1
            L1 *= P10 * c0 + P11 * c1
        s = np.maximum(np.maximum(L0, L1), 1e-30)
        msg[v] = (L0 / s, L1 / s)
        logs = logs + np.log(s)
    L0, L1 = msg[0]
    return logs + np.log((1 - root) * L0 + root * L1)


def posterior(d, X, visible, g, lo, mult, root):
    """Marginal P(present) at every node, per family (g, lo, root: (F,))."""
    children, parent, length, order = d["children"], d["parent"], d["length"], d["order"]
    n, F = len(parent), X.shape[1]
    down = np.ones((n, 2, F), np.float32)
    for v in order:
        if not children[v]:
            if visible[v]:
                down[v, 0], down[v, 1] = tip_message(d, X, v)
            continue
        L0 = np.ones(F, np.float32)
        L1 = np.ones(F, np.float32)
        for c in children[v]:
            P00, P01, P10, P11 = branch_probs(length[c], g, lo * mult[c])
            L0 *= P00 * down[c, 0] + P01 * down[c, 1]
            L1 *= P10 * down[c, 0] + P11 * down[c, 1]
        s = np.maximum(np.maximum(L0, L1), 1e-30)
        down[v, 0], down[v, 1] = L0 / s, L1 / s
    up = np.zeros((n, 2, F), np.float32)
    up[0, 0], up[0, 1] = 1 - root, root
    post = np.zeros((n, F), np.float32)
    for v in reversed(order):
        a0, a1 = up[v, 0], up[v, 1]
        p1, p0 = a1 * down[v, 1], a0 * down[v, 0]
        post[v] = p1 / np.maximum(p0 + p1, 1e-30)
        for c in children[v]:
            s0, s1 = a0.copy(), a1.copy()
            for sib in children[v]:
                if sib != c:
                    P00, P01, P10, P11 = branch_probs(length[sib], g, lo * mult[sib])
                    s0 *= P00 * down[sib, 0] + P01 * down[sib, 1]
                    s1 *= P10 * down[sib, 0] + P11 * down[sib, 1]
            P00, P01, P10, P11 = branch_probs(length[c], g, lo * mult[c])
            u0, u1 = s0 * P00 + s1 * P10, s0 * P01 + s1 * P11
            z = np.maximum(u0 + u1, 1e-30)
            up[c, 0], up[c, 1] = u0 / z, u1 / z
    return post


def fit(d, X, visible, spec):
    """Grid maximum likelihood of per-family (gain, loss) under a model spec; returns g, lo, root."""
    q_max = spec["ratio"] if spec["ratio"] is not None else np.inf
    grid = [(lv, lv * q) for lv, q in product(L_GRID, Q_GRID) if q <= q_max + 1e-9]
    lo = np.array([a for a, _ in grid], np.float32)[:, None]
    g = np.array([b for _, b in grid], np.float32)[:, None]
    mult = np.where(d["reduced_branch"], spec["mult"], 1.0).astype(np.float32)
    # Incomplete genomes read as extra loss on their own terminal branch.
    if spec.get("tip_mult", 1.0) != 1.0:
        low = np.zeros(len(mult), dtype=bool)
        low[d["tips"]] = ~(d["busco"][d["tips"]] >= 97) | d["mag"][d["tips"]]
        mult = np.where(low, mult * spec["tip_mult"], mult).astype(np.float32)
    vis_tips = [v for v in d["tips"] if visible[v]]
    emp = X[vis_tips].mean(0).astype(np.float32)
    if spec["root"] == "stationary":
        root = g / (g + lo) * np.ones((1, X.shape[1]), np.float32)
    elif spec["root"] == "flat":
        root = np.float32(0.5)
    else:
        root = np.clip(emp, 0.02, 0.98)[None, :]
    ll = loglik(d, X, visible, g, lo, mult, root)
    k = np.argmax(ll, axis=0)
    fi = np.arange(X.shape[1])
    g_f, lo_f = g[k, 0], lo[k, 0]
    if spec["root"] == "stationary":
        root_f = g_f / (g_f + lo_f)
    elif spec["root"] == "flat":
        root_f = np.full(X.shape[1], 0.5, np.float32)
    else:
        root_f = np.clip(emp, 0.02, 0.98)
    return g_f, lo_f, root_f, mult, float(ll[k, fi].sum())


def visible_mask(d, spec, hidden_order=None):
    vis = np.zeros(len(d["parent"]), dtype=bool)
    for v in d["tips"]:
        ok = True
        if spec["min_busco"] and not (d["busco"][v] >= spec["min_busco"]):
            ok = False
        if spec["drop_mag"] and d["mag"][v]:
            ok = False
        if hidden_order and d["order_of"][v] == hidden_order:
            ok = False
        vis[v] = ok
    return vis


# ---- simulation ----------------------------------------------------------------------------------

GENERATORS = {
    "neutral": dict(M=1.0, hgt=0.0, ratio=0.3, incomplete=True),
    "reduced_x5": dict(M=5.0, hgt=0.02, ratio=0.1, incomplete=True),
    "reduced_x20_hgt": dict(M=20.0, hgt=0.05, ratio=0.1, incomplete=True),
    "gain_heavy": dict(M=5.0, hgt=0.05, ratio=1.0, incomplete=True),
}


def simulate(d, gen, n_fam=600, seed=0):
    """Truth at every node and observed tips for n_fam synthetic families."""
    rng = np.random.default_rng(seed)
    parent, length, order = d["parent"], d["length"], d["order"]
    lo = np.exp(rng.uniform(np.log(0.05), np.log(5.0), n_fam)).astype(np.float32)
    g = lo * rng.uniform(0.0, gen["ratio"], n_fam).astype(np.float32)
    root = rng.random(n_fam) < rng.beta(2, 2, n_fam)
    mult = np.where(d["reduced_branch"], gen["M"], 1.0)
    state = np.zeros((len(parent), n_fam), dtype=bool)
    state[0] = root
    for v in reversed(order):
        if v == 0:
            continue
        P00, P01, P10, P11 = branch_probs(length[v], g, lo * mult[v])
        u = rng.random(n_fam)
        p_present = np.where(state[parent[v]], P11, P01)
        state[v] = u < p_present
        if gen["hgt"]:
            state[v] |= rng.random(n_fam) < gen["hgt"] * length[v] * 10  # horizontal gains, length-scaled
    obs = state.copy()
    if gen["incomplete"]:
        for v in d["tips"]:
            comp = d["busco"][v] / 100 if np.isfinite(d["busco"][v]) else 0.9
            obs[v] &= rng.random(n_fam) < comp
    return state, obs


# ---- evaluation ------------------------------------------------------------------------------------

def logloss(p, y):
    p = np.clip(p, 1e-4, 1 - 1e-4)
    return float(-np.mean(y * np.log(p) + (1 - y) * np.log(1 - p)))


def evaluate(spec, d, n_sim_fam=600):
    out = {"spec": spec}
    X = d["X"]
    vis = visible_mask(d, spec)
    g, lo, root, mult, ll = fit(d, X, vis, spec)
    post = posterior(d, X, vis, g, lo, mult, root)
    ar = d["alpha_root"]
    fams = list(d["fams"])
    out["real"] = {"loglik": ll, "visible_tips": int(vis.sum()), "alpha_root_expected_share": float(post[ar].mean()),
                   "alpha_root_p_ge_0.9_share": float((post[ar] >= 0.9).mean()),
                   "positive_control": {gname: float(post[ar][fams.index(f)]) for gname, f in RECLINOMONAS_CORE.items()
                                        if f in fams}}
    # Hide whole orders: predict their tips through the deep backbone; stability of the alpha root.
    hide, moves = {}, []
    for o in HIDE_ORDERS:
        vis_h = visible_mask(d, spec, hidden_order=o)
        hidden = [v for v in d["tips"] if d["order_of"][v] == o and vis[v]]
        if len(hidden) < 3:
            continue
        gh, loh, rooth, _, _ = fit(d, X, vis_h, spec)
        ph = posterior(d, X, vis_h, gh, loh, mult, rooth)
        y = X[hidden].ravel()
        p = ph[hidden].ravel()
        hide[o] = {"n_tips": len(hidden), "logloss": logloss(p, y), "auroc": float(auroc(p, y))}
        moves.append(float(np.abs(ph[ar] - post[ar]).mean()))
    out["hide"] = hide
    out["hide_logloss"] = float(np.mean([h["logloss"] for h in hide.values()]))
    out["stability_mean_abs_change"] = float(np.mean(moves))
    # Simulation with known truth.
    sims = {}
    for i, (name, gen) in enumerate(GENERATORS.items()):
        truth, obs = simulate(d, gen, n_sim_fam, seed=100 + i)
        vis_s = visible_mask(d, spec)
        gs, los, roots, ms, _ = fit(d, obs, vis_s, spec)
        ps = posterior(d, obs, vis_s, gs, los, ms, roots)[ar]
        t = truth[ar].astype(float)
        sims[name] = {"logloss": logloss(ps, t), "brier": float(np.mean((ps - t) ** 2)), "auroc": float(auroc(ps, t)),
                      "size_bias": float((ps.sum() - t.sum()) / max(t.sum(), 1))}
    out["sim"] = sims
    out["sim_logloss"] = float(np.mean([s["logloss"] for s in sims.values()]))
    out["sim_size_bias"] = float(np.mean([s["size_bias"] for s in sims.values()]))
    return out


def round1_models():
    models = []
    for ratio, root, (busco, mag), mult in product((None, 0.3, 0.1, 0.03, 0.01), ("stationary", "flat", "empirical"),
                                                  ((0, False), (90, False), (90, True)), (1.0, 5.0)):
        models.append({"ratio": ratio, "root": root, "min_busco": busco, "drop_mag": mag, "mult": mult})
    return models


def model_id(spec):
    r = "free" if spec["ratio"] is None else f"q{spec['ratio']}"
    tip = f"_t{spec['tip_mult']:g}" if spec.get("tip_mult", 1.0) != 1.0 else ""
    return f"{r}_{spec['root']}_b{spec['min_busco']}{'_nomag' if spec['drop_mag'] else ''}_m{spec['mult']:g}{tip}"


def rank(round_no):
    rows = [json.loads(p.read_text()) for p in sorted((OUT / f"round{round_no}").glob("*.json"))]
    if not rows:
        sys.exit("no results")
    for key_, name in (("sim_logloss", "r_sim"), ("hide_logloss", "r_hide"), ("stability_mean_abs_change", "r_stab")):
        vals = np.array([r[key_] for r in rows])
        for r, rk in zip(rows, vals.argsort().argsort() + 1):
            r[name] = int(rk)
    for r in rows:
        r["mean_rank"] = (r["r_sim"] + r["r_hide"] + r["r_stab"]) / 3
    rows.sort(key=lambda r: (r["mean_rank"], r["sim_logloss"]))
    table = [{"model": model_id(r["spec"]), "mean_rank": round(r["mean_rank"], 2), "sim_logloss": round(r["sim_logloss"], 4),
              "sim_size_bias": round(r["sim_size_bias"], 3), "hide_logloss": round(r["hide_logloss"], 4),
              "stability": round(r["stability_mean_abs_change"], 4),
              "alpha_root_expected_share": round(r["real"]["alpha_root_expected_share"], 3),
              "positive_control_ge_0.9": sum(v >= 0.9 for v in r["real"]["positive_control"].values()),
              "positive_control_n": len(r["real"]["positive_control"])} for r in rows]
    # Paired comparison of the top two over the evaluation units (simulation generators, hidden orders).
    if len(rows) > 1:
        a_, b_ = rows[0], rows[1]
        diffs = [a_["sim"][k]["logloss"] - b_["sim"][k]["logloss"] for k in a_["sim"]]
        diffs += [a_["hide"][k]["logloss"] - b_["hide"][k]["logloss"] for k in a_["hide"] if k in b_["hide"]]
        rng = np.random.default_rng(0)
        boots = [np.mean(rng.choice(diffs, len(diffs))) for _ in range(5000)]
        table[0]["vs_second"] = {"second": model_id(b_["spec"]), "mean_logloss_diff": round(float(np.mean(diffs)), 4),
                                 "ci95": [round(float(np.percentile(boots, 2.5)), 4), round(float(np.percentile(boots, 97.5)), 4)],
                                 "units": len(diffs), "note": "negative = top model better"}
        print("top vs second:", table[0]["vs_second"])
    (OUT / f"round{round_no}_ranking.json").write_text(json.dumps(table, indent=1))
    print(f"{'model':38s} rank  simLL  sizeBias hideLL  stab  rootShare  posCtrl")
    for t in table[:25]:
        print(f"{t['model']:38s} {t['mean_rank']:5.1f} {t['sim_logloss']:.4f} {t['sim_size_bias']:+.3f} "
              f"{t['hide_logloss']:.4f} {t['stability']:.4f} {t['alpha_root_expected_share']:.3f} "
              f"{t['positive_control_ge_0.9']}/{t['positive_control_n']}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--round", type=int, default=1)
    ap.add_argument("--shard", type=int, default=0)
    ap.add_argument("--n-shards", type=int, default=1)
    ap.add_argument("--rank", action="store_true")
    ap.add_argument("--build-cache", action="store_true")
    ap.add_argument("--families", type=int, default=1500)
    ap.add_argument("--sim-families", type=int, default=600)
    ap.add_argument("--models", help="JSON file with a list of model specs (later rounds)")
    ap.add_argument("--limit", type=int, default=0)
    args = ap.parse_args()
    if args.rank:
        rank(args.round)
        return
    if args.build_cache or not CACHE.exists():
        build_cache(n_families=args.families)
        if args.build_cache:
            return
    d = load_cache()
    models = json.loads(Path(args.models).read_text()) if args.models else round1_models()
    mine = models[args.shard::args.n_shards]
    if args.limit:
        mine = mine[: args.limit]
    out = OUT / f"round{args.round}"
    out.mkdir(parents=True, exist_ok=True)
    for spec in mine:
        mid = model_id(spec)
        if (out / f"{mid}.json").exists():
            continue
        res = evaluate(spec, d, args.sim_families)
        (out / f"{mid}.json").write_text(json.dumps(res, indent=1))
        print(f"{mid}: sim LL {res['sim_logloss']:.4f} (size bias {res['sim_size_bias']:+.3f}), hide LL "
              f"{res['hide_logloss']:.4f}, stability {res['stability_mean_abs_change']:.4f}, root share "
              f"{res['real']['alpha_root_expected_share']:.3f}", flush=True)


if __name__ == "__main__":
    main()
