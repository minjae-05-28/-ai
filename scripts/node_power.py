"""Is a reconstruction of THIS node worth anything? Known truth, per node.

    PYTHONPATH=src python scripts/node_power.py

Hiding a few tips and predicting them is the wrong instrument for a tight clade: among 53
Rickettsiales that share nearly every family, "what does the hidden one have" is answered at
AUROC 0.988 by present-day frequency alone, so the test cannot tell a good reconstruction from a
useless one. It measures how similar the living members are, not how well the ancestor is found.

Here the ancestor is scored directly. Families evolve on the real tree with the truth recorded at
every node; the reconstruction then runs on the tips alone and its posterior at each target node is
scored against that node's true content, next to the baseline a reader would otherwise use:

    frequency   the family's share among the node's present-day descendants (no tree)
    root_prior  the model with the data ignored

Reported per node: AUROC, log loss, and the error in ancestor size. The question is not whether
accuracy is high - it is whether the tree buys anything over frequency AT THAT NODE.
"""

import argparse
import json
import sys
from collections import Counter
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
from mito_model_search import GENERATORS, fit, load_cache, mrca, posterior, simulate, visible_mask  # noqa: E402

from organelle_evo.predict import auroc  # noqa: E402

OUT = Path("results/node_power")
SPEC = {"ratio": None, "root": "stationary", "min_busco": 0, "drop_mag": False, "mult": 14.0, "tip_mult": 1.0}
AMOEBA_GENERA = {"Acanthamoeba", "Balamuthia", "Cavenderia", "Dictyostelium", "Entamoeba",
                 "Heterostelium", "Pelomyxa", "Planoprotostelium", "Polysphondylium", "Physarum",
                 "Vermamoeba", "Mastigamoeba", "Tieghemostelium"}
ORDERS = ("o__Rickettsiales", "o__Rhodospirillales", "o__Caulobacterales", "o__Rhizobiales",
          "o__Rhodobacterales", "o__Sphingomonadales")


def logloss(p, y):
    p = np.clip(p, 1e-4, 1 - 1e-4)
    return float(-np.mean(y * np.log(p) + (1 - y) * np.log(1 - p)))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--families", type=int, default=800)
    ap.add_argument("--reps", type=int, default=3)
    ap.add_argument("--clade", default="bacteria",
                    help="bacteria (alphaproteobacterial tree), amoebozoa, or a name used with --tree")
    ap.add_argument("--tree", default="", help="a marker tree whose clade is --clade-kingdom (rooted on the outgroup)")
    ap.add_argument("--clade-kingdom", default="")
    ap.add_argument("--root-split", default="", help="root between this lineage name and the rest (LECA)")
    ap.add_argument("--lineage", default="")
    ap.add_argument("--pick", default="", help="<set>_pick.json: also grade each phylum with >= 5 sampled tips")
    ap.add_argument("--out", default=str(OUT))
    args = ap.parse_args()
    out = Path(args.out) / ("" if args.clade == "bacteria" else args.clade)
    out.mkdir(parents=True, exist_ok=True)
    if args.clade == "bacteria":
        d = load_cache()
        vis = visible_mask(d, SPEC)
        alpha = [v for v in d["tips"] if d["is_alpha"][v]]
        nodes = {"Alphaproteobacteria": (d["alpha_root"], alpha)}
        for o in ORDERS:
            members = [v for v in d["tips"] if d["order_of"][v] == o]
            if len(members) >= 5:
                nodes[o[3:]] = (mrca(members, d["parent"], d["depth"]), members)
    elif args.tree:
        from hgt_rate import clade_tree, load_lineage

        d, _, vis, _, names, in_clade = clade_tree(args.tree, (), args.clade_kingdom, not args.root_split,
                                                   args.root_split or None, load_lineage(args.lineage))
        members = [v for v in d["tips"] if in_clade.get(v)]
        nodes = {f"{args.clade} (표본이 도달한 마디)": (mrca(members, d["parent"], d["depth"]), members)}
        if args.pick:
            lin = json.loads(Path(args.pick).read_text())["lineage"]
            phylum = {r["organism"].replace("'", ""): r.get("phylum") or r.get("supergroup") or "?" for r in lin.values()}
            groups = {}
            for v in members:
                groups.setdefault(phylum.get(names[v], "?"), []).append(v)
            for ph, vs in sorted(groups.items()):
                if ph != "?" and len(vs) >= 5:
                    nodes[ph] = (mrca(vs, d["parent"], d["depth"]), vs)
    else:
        from hgt_rate import amoeba_tree
        from run_clade_ancestor import build

        d, _, vis, _ = amoeba_tree()
        _, _, names, in_clade, _, _ = build("results/phylo_tree/amoeba.nwk", AMOEBA_GENERA, 100)
        members = [v for v in d["tips"] if in_clade.get(v)]
        nodes = {"Amoebozoa (표본이 도달한 마디)": (mrca(members, d["parent"], d["depth"]), members)}
    print({k: len(v[1]) for k, v in nodes.items()})

    rows = []
    for rep in range(args.reps):
        truth, obs = simulate(d, GENERATORS["reduced_x5"], args.families, seed=5000 + rep)
        g, lo, root, mult, _ = fit(d, obs, vis, SPEC)
        post = posterior(d, obs, vis, g, lo, mult, root)
        for name, (node, members) in nodes.items():
            t = truth[node].astype(float)
            p = post[node]
            freq = obs[members].mean(0).astype(float)
            rows.append({"rep": rep, "node": name, "n_tips": len(members),
                         "recon_auroc": float(auroc(p, t)), "freq_auroc": float(auroc(freq, t)),
                         "recon_logloss": logloss(p, t), "freq_logloss": logloss(freq, t),
                         "prior_logloss": logloss(np.full_like(t, t.mean()), t),
                         "recon_size_bias": float((p.sum() - t.sum()) / max(t.sum(), 1)),
                         "freq_size_bias": float((freq.sum() - t.sum()) / max(t.sum(), 1)),
                         "true_share": float(t.mean())})
            r = rows[-1]
            print(f"rep{rep} {name:22s} n={len(members):5d}  AUROC {r['recon_auroc']:.4f} vs freq "
                  f"{r['freq_auroc']:.4f} ({r['recon_auroc'] - r['freq_auroc']:+.4f})  "
                  f"logloss {r['recon_logloss']:.3f} vs {r['freq_logloss']:.3f}  size "
                  f"{r['recon_size_bias']:+.3f} vs {r['freq_size_bias']:+.3f}", flush=True)

    agg = {}
    for name in nodes:
        sel = [r for r in rows if r["node"] == name]
        a = {k: round(float(np.mean([r[k] for r in sel])), 4) for k in
             ("recon_auroc", "freq_auroc", "recon_logloss", "freq_logloss", "prior_logloss",
              "recon_size_bias", "freq_size_bias")}
        a["n_tips"] = sel[0]["n_tips"]
        a["auroc_margin"] = round(a["recon_auroc"] - a["freq_auroc"], 4)
        a["logloss_margin"] = round(a["freq_logloss"] - a["recon_logloss"], 4)
        headroom = 1 - a["freq_auroc"]
        a["auroc_headroom"] = round(headroom, 4)
        # Where the baseline already ranks at 0.99+, AUROC has nothing left to win, so calibration
        # (log loss) decides. Demanding both would call a saturated node a failure.
        a["verdict"] = ("계통수가 도움이 됨" if a["logloss_margin"] > 0.02
                        and (a["auroc_margin"] > 0.005 or headroom < 0.01)
                        else "기준선과 구별되지 않음")
        agg[name] = a
    (out / "summary.json").write_text(json.dumps(
        {"generator": GENERATORS["reduced_x5"], "model": SPEC, "families": args.families,
         "reps": args.reps, "note": "알려진 정답으로 각 마디의 조상을 직접 채점. 잎 숨기기와 달리 "
                                    "꽉 짜인 분류군에서도 변별력이 있음.",
         "aggregate": agg, "runs": rows}, ensure_ascii=False, indent=1))
    print("\n마디별 (평균)")
    for k, v in sorted(agg.items(), key=lambda t: -t[1]["n_tips"]):
        print(f"  {k:22s} {v['n_tips']:5d}종  AUROC {v['recon_auroc']:.4f} vs {v['freq_auroc']:.4f} "
              f"({v['auroc_margin']:+.4f})  logloss {v['recon_logloss']:.3f} vs {v['freq_logloss']:.3f} "
              f"({v['logloss_margin']:+.3f})  크기 {v['recon_size_bias']:+.3f} vs {v['freq_size_bias']:+.3f}"
              f"  -> {v['verdict']}")
    print(f"Done -> {out}/summary.json")
    print(Counter(v["verdict"] for v in agg.values()))


if __name__ == "__main__":
    main()
