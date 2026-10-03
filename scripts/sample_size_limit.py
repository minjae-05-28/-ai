"""How many species does an ancestral reconstruction need?

    python scripts/sample_size_limit.py [--sizes 12,25,50,100,300,1000,2323]

Known-truth simulation on the real tree (the cache of mito_model_search.py): families evolve on
the full 2,623-tip tree, the truth at the alphaproteobacterial root is recorded, then the tree is
pruned to a subsample of the clade's tips and the ancestor is reconstructed from that subsample
alone. Accuracy against the same truth says what a reconstruction can be worth at that sample size.

Two sampling patterns, because real clades are not sampled evenly:
    spread      tips drawn at random across the clade
    clustered   most tips drawn from one subclade (as Amoebozoa is 8/12 social amoebae),
                the rest at random

Reported next to the reconstruction: present-day frequency among the sampled tips (no tree), and
whether the subsample's root is still the same node as the full tree's root (with clustered
sampling the most recent common ancestor can slide to a younger node, so the reconstruction then
answers a different question).
"""

import argparse
import json
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
from mito_model_search import GENERATORS, fit, load_cache, mrca, posterior, simulate  # noqa: E402
from run_mito_ancestor import postorder, prune  # noqa: E402

from organelle_evo.predict import auroc  # noqa: E402

OUT = Path("results/sample_size")
SPEC = {"ratio": None, "root": "stationary", "min_busco": 0, "drop_mag": False, "mult": 14.0, "tip_mult": 1.0}


def logloss(p, y):
    p = np.clip(p, 1e-4, 1 - 1e-4)
    return float(-np.mean(y * np.log(p) + (1 - y) * np.log(1 - p)))


def subtree_of(node, children):
    out, stack = [], [node]
    while stack:
        v = stack.pop()
        out.append(v)
        stack.extend(children[v])
    return out


def pick(d, n, pattern, rng):
    """n alphaproteobacterial tips plus every outgroup tip."""
    alpha = [v for v in d["tips"] if d["is_alpha"][v]]
    out = [v for v in d["tips"] if not d["is_alpha"][v]]
    if pattern == "spread" or n >= len(alpha):
        sel = list(rng.choice(alpha, min(n, len(alpha)), replace=False))
    else:
        # A subclade holding at least two thirds of the picks, as a real skewed sample looks.
        want = max(2, int(round(n * 2 / 3)))
        cands = [v for v in range(len(d["parent"]))
                 if d["children"][v] and want <= sum(1 for u in subtree_of(v, d["children"])
                                                     if not d["children"][u] and d["is_alpha"][u]) <= want * 3]
        hub = int(rng.choice(cands)) if cands else mrca(alpha, d["parent"], d["depth"])
        pool = [u for u in subtree_of(hub, d["children"]) if not d["children"][u] and d["is_alpha"][u]]
        sel = list(rng.choice(pool, min(want, len(pool)), replace=False))
        rest = [v for v in alpha if v not in set(sel)]
        sel += list(rng.choice(rest, min(n - len(sel), len(rest)), replace=False))
    return sorted(set(sel)), out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--sizes", default="12,25,50,100,300,1000,2323")
    ap.add_argument("--families", type=int, default=800)
    ap.add_argument("--reps", type=int, default=3)
    ap.add_argument("--out", default=str(OUT))
    args = ap.parse_args()
    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    d = load_cache()
    full_root = d["alpha_root"]
    rows = []
    for rep in range(args.reps):
        truth_all, obs_all = simulate(d, GENERATORS["reduced_x5"], args.families, seed=2000 + rep)
        t = truth_all[full_root].astype(float)
        for n in [int(x) for x in args.sizes.split(",")]:
            for pattern in ("spread", "clustered"):
                if n >= 2323 and pattern == "clustered":
                    continue
                rng = np.random.default_rng(10_000 * rep + n + (0 if pattern == "spread" else 7))
                sel, outg = pick(d, n, pattern, rng)
                keep = sel + outg
                parent, length, label, old = prune(d["parent"], d["length"], [""] * len(d["parent"]), keep)
                order, children = postorder(parent)
                sub = {"parent": parent, "length": length, "order": order, "children": children,
                       "tips": [v for v in range(len(parent)) if not children[v]]}
                depth = np.zeros(len(parent))
                for v in reversed(order):
                    if v:
                        depth[v] = depth[parent[v]] + length[v]
                sub["depth"] = depth
                sub["reduced_branch"] = d["reduced_branch"][old]
                sub["busco"] = np.where(np.isin(old, d["tips"]), d["busco"][old], np.nan)
                sub["mag"] = d["mag"][old]
                X = obs_all[old]
                vis = np.zeros(len(parent), dtype=bool)
                vis[sub["tips"]] = True
                alpha_sub = [v for v in sub["tips"] if d["is_alpha"][old[v]]]
                root_sub = mrca(alpha_sub, parent, depth)
                same_node = bool(old[root_sub] == full_root)
                g, lo, root, mult, _ = fit(sub, X, vis, SPEC)
                post = posterior(sub, X, vis, g, lo, mult, root)[root_sub]
                freq = X[alpha_sub].mean(0).astype(float)
                # Two separate errors: estimating the node the subsample can actually reach, and
                # that node not being the clade's real root (with few tips the basal lineages are
                # almost never sampled, so the "ancestor" is a younger node).
                t_reached = truth_all[old[root_sub]].astype(float)
                rows.append({"rep": rep, "n_alpha": len(alpha_sub), "pattern": pattern,
                             "same_root_node": same_node,
                             "reached_vs_true_root_jaccard": float(np.logical_and(t_reached > 0, t > 0).sum()
                                                                   / max(np.logical_or(t_reached > 0, t > 0).sum(), 1)),
                             "reached_size_vs_true_root": float((t_reached.sum() - t.sum()) / max(t.sum(), 1)),
                             "recon_auroc_reached": float(auroc(post, t_reached)),
                             "recon_logloss_reached": logloss(post, t_reached),
                             "recon_size_bias_reached": float((post.sum() - t_reached.sum()) / max(t_reached.sum(), 1)),
                             "recon_auroc": float(auroc(post, t)), "freq_auroc": float(auroc(freq, t)),
                             "recon_logloss": logloss(post, t), "freq_logloss": logloss(freq, t),
                             "prior_logloss": logloss(np.full_like(t, t.mean()), t),
                             "recon_size_bias": float((post.sum() - t.sum()) / max(t.sum(), 1))})
                r = rows[-1]
                print(f"rep{rep} n={len(alpha_sub):5d} {pattern:9s} | vs true root: AUROC {r['recon_auroc']:.3f} "
                      f"(freq {r['freq_auroc']:.3f}) size {r['recon_size_bias']:+.3f} | vs node reached: AUROC "
                      f"{r['recon_auroc_reached']:.3f} size {r['recon_size_bias_reached']:+.3f} | node reached vs "
                      f"true root: Jaccard {r['reached_vs_true_root_jaccard']:.3f} size "
                      f"{r['reached_size_vs_true_root']:+.3f}", flush=True)
    agg = {}
    for pattern in ("spread", "clustered"):
        for n in sorted({r["n_alpha"] for r in rows}):
            sel = [r for r in rows if r["pattern"] == pattern and r["n_alpha"] == n]
            if sel:
                agg[f"{pattern}_{n}"] = {k: round(float(np.mean([r[k] for r in sel])), 4)
                                         for k in ("recon_auroc", "freq_auroc", "recon_logloss", "freq_logloss",
                                                   "prior_logloss", "recon_size_bias", "recon_auroc_reached",
                                                   "recon_logloss_reached", "recon_size_bias_reached",
                                                   "reached_vs_true_root_jaccard", "reached_size_vs_true_root")}
                agg[f"{pattern}_{n}"]["same_root_node_share"] = float(np.mean([r["same_root_node"] for r in sel]))
    (out / "summary.json").write_text(json.dumps({"model": SPEC, "aggregate": agg, "runs": rows}, indent=1))
    print("\naggregate (mean over reps)")
    for k, v in agg.items():
        beats = "recon" if v["recon_logloss"] < v["freq_logloss"] else "frequency"
        calib = "ok" if v["recon_logloss"] < v["prior_logloss"] else "WORSE THAN BASE RATE"
        print(f"  {k:18s} true root: AUROC {v['recon_auroc']:.3f} (freq {v['freq_auroc']:.3f}, {beats}) size "
              f"{v['recon_size_bias']:+.3f} {calib} | node reached: AUROC {v['recon_auroc_reached']:.3f} size "
              f"{v['recon_size_bias_reached']:+.3f} | reached vs true root: Jaccard "
              f"{v['reached_vs_true_root_jaccard']:.3f} size {v['reached_size_vs_true_root']:+.3f}")
    print(f"Done -> {out}/summary.json")


if __name__ == "__main__":
    main()
