"""Reconstruction, known-truth grade and transfer level for one clade, in one short command
(run-analysis.yml names its concurrency group after the command, and a long one is rejected).

    python scripts/run_clade_pipeline.py fungi
    python scripts/run_clade_pipeline.py leca --root-split Discoba
"""

import argparse
import subprocess
import sys

PRESETS = {
    "fungi": {"tree": "results/phylo_tree/fungi_nb.nwk", "kingdom": "fungi",
              "pick": "data/markers/fungi_nb_pick.json", "label": "균류 + 외군"},
    "leca": {"tree": "results/phylo_tree/leca.nwk", "kingdom": "*",
             "pick": "data/markers/leca_pick.json", "label": "진핵생물 전체"},
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
    name = args.clade + (f"_{args.root_split.lower()}" if args.root_split else "")
    py = sys.executable
    root = (["--root-split", args.root_split, "--lineage", p["pick"]] if args.root_split
            else ["--root-outgroup"])
    steps = args.steps.split(",")
    if "ancestor" in steps:
        run([py, "scripts/run_clade_ancestor.py", "--tree", tree, "--clade-kingdom", p["kingdom"], "--name", name,
             "--completeness", "--no-reduced-mult"] + root)
    split = ["--root-split", args.root_split, "--lineage", p["pick"]] if args.root_split else []
    if "power" in steps:
        run([py, "scripts/node_power.py", "--clade", name, "--tree", tree, "--clade-kingdom", p["kingdom"],
             "--pick", p["pick"]] + split)
    if "hgt" in steps:
        run([py, "scripts/hgt_rate.py", "--tree", tree, "--name", name, "--clade-kingdom", p["kingdom"],
             "--label", p["label"]] + split)


if __name__ == "__main__":
    main()
