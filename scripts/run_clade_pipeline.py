"""Reconstruction, known-truth grade and transfer level for one clade, in one short command
(run-analysis.yml names its concurrency group after the command, and a long one is rejected).

    python scripts/run_clade_pipeline.py fungi
    python scripts/run_clade_pipeline.py leca --root-split Discoba
"""

import argparse
import subprocess
from pathlib import Path
import sys

PRESETS = {
    "fungi": {"tree": "results/phylo_tree/fungi_nb.nwk", "kingdom": "fungi",
              "pick": "data/markers/fungi_nb_pick.json", "label": "균류 + 외군"},
    "leca": {"tree": "results/phylo_tree/leca.nwk", "kingdom": "*",
             "pick": "data/markers/leca_pick.json", "label": "진핵생물 전체"},
    # Second LECA sample (thin groups keep their reduced lineages) on an IQ-TREE tree constrained to
    # the uncontested supergroups (ribosomal_tree.py --method iqtree).
    "leca2": {"tree": "results/phylo_tree/leca2.nwk", "kingdom": "*",
              "pick": "data/markers/leca2_pick.json", "label": "진핵생물 전체 (2판)"},
    # The GTDB tree, pruned to Cyanobacteriota + 150 other bacteria (make_gtdb_subtree.py).
    # Gloeomargarita is the closest living relative of the plastid; ^ = the node where it split off.
    "cyano": {"tree": "results/phylo_tree/cyano.nwk", "kingdom": "lineage:c__Cyanobacteriia",
              "pick": "data/markers/cyano_lineage.json", "label": "남세균 + 외군",
              "lineage_for_clade": True, "extra": "g__Gloeomargarita,^g__Gloeomargarita"},
}


def run(cmd):
    print("+", " ".join(cmd), flush=True)
    subprocess.run(cmd, check=True)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("clade", choices=sorted(PRESETS))
    ap.add_argument("--root-split", default="")
    ap.add_argument("--tree", default="")
    ap.add_argument("--steps", default="ancestor,power,hgt")
    args = ap.parse_args()
    p = PRESETS[args.clade]
    tree = args.tree or p["tree"]
    name = args.clade + (f"_{args.root_split.split('+')[0].lower()}" if args.root_split else "")
    py = sys.executable
    root = (["--root-split", args.root_split, "--lineage", p["pick"]] if args.root_split
            else ["--root-outgroup"] + (["--lineage", p["pick"]] if p.get("lineage_for_clade") else []))
    extra = ["--extra-nodes", p["extra"]] if p.get("extra") else []
    bt = tree.replace(".nwk", ".boot.nwk")
    boot = ["--bootstrap-trees", bt] if Path(bt).exists() else []
    steps = args.steps.split(",")
    if "ancestor" in steps:
        run([py, "scripts/run_clade_ancestor.py", "--tree", tree, "--clade-kingdom", p["kingdom"], "--name", name,
             "--completeness", "--no-reduced-mult"] + root + extra + boot)
    split = (["--root-split", args.root_split, "--lineage", p["pick"]] if args.root_split
             else ["--lineage", p["pick"]] if p.get("lineage_for_clade") else [])
    if "power" in steps:
        run([py, "scripts/node_power.py", "--clade", name, "--tree", tree, "--clade-kingdom", p["kingdom"],
             "--pick", p["pick"]] + split)
    if "hgt" in steps:
        run([py, "scripts/hgt_rate.py", "--tree", tree, "--name", name, "--clade-kingdom", p["kingdom"],
             "--label", p["label"]] + split)


if __name__ == "__main__":
    main()
