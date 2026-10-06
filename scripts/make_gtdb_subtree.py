"""A clade of the GTDB bacterial tree with UniProt organism names on the tips, so the general
clade pipeline (run_clade_ancestor.py) can reconstruct it.

    python scripts/make_gtdb_subtree.py --phylum p__Cyanobacteriota --outgroup 150 --set cyano
        -> results/phylo_tree/cyano.nwk           (rooted: GTDB's own root, pruned)
        -> data/markers/cyano_lineage.json       {"lineage": {acc: {"organism", "lineage": [GTDB ranks]}}}

Tips: GTDB species representatives whose NCBI species name matches a collected UniProt bacterial
proteome (the same matching as run_mito_ancestor.load_tips), plus a seeded random sample of other
bacteria as outgroup. Names that do not identify a species ("Synechococcus sp.", "uncultured
cyanobacterium") are skipped: several GTDB species share them, so the proteome could sit on the
wrong branch.
"""

import argparse
import csv
import gzip
import json
import re
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
from run_mito_ancestor import key, parse_newick, postorder, prune  # noqa: E402


def to_newick(parent, length, label):
    order, children = postorder(parent)
    out = {}
    for v in order:
        if children[v]:
            s = "(" + ",".join(out[c] for c in children[v]) + ")"
        else:
            s = "'" + label[v].replace("'", "") + "'"
        out[v] = s + (f":{length[v]:.6f}" if v else "")
    return out[0] + ";"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--phylum", required=True)
    ap.add_argument("--outgroup", type=int, default=150)
    ap.add_argument("--set", required=True)
    args = ap.parse_args()
    csv.field_size_limit(10**8)
    reps, clash = {}, set()
    for r in csv.DictReader(gzip.open("data/gtdb/species_reps.tsv.gz", "rt"), delimiter="\t"):
        k = key(r["ncbi_organism_name"])
        if k.endswith(" sp.") or k.startswith("uncultured") or " bacterium" in k or k.endswith(" cyanobacterium"):
            continue
        if k in reps:
            clash.add(k)
        reps.setdefault(k, (r["accession"], r["gtdb_taxonomy"]))
    for k in clash:          # a name shared by two GTDB species cannot place its proteome
        reps.pop(k, None)
    prof = {}
    for f in sorted(Path("data/uniprot/shards").glob("*.json.gz")):
        for p in json.loads(gzip.open(f, "rt").read()).values():
            k = key(p["organism"])
            if p.get("kingdom") == "bacteria" and k in reps and len(p.get("pfam") or {}) >= 100:
                old = prof.get(k)
                if old is None or len(p["pfam"]) > len(old["pfam"]):
                    prof[k] = p
    inside = sorted(k for k in prof if args.phylum in reps[k][1])
    others = sorted(k for k in prof if args.phylum not in reps[k][1])
    rng = np.random.default_rng(0)
    out = list(rng.choice(others, min(args.outgroup, len(others)), replace=False))
    chosen = {reps[k][0]: k for k in inside + out}
    parent, length, label = parse_newick(gzip.open("results/phylo_tree/gtdb_bac120.tree.gz", "rt").read())
    nodes = [i for i, lab in enumerate(label) if lab in chosen]
    parent, length, label, _ = prune(parent, length, label, nodes)
    order, children = postorder(parent)
    names = [prof[chosen[lab]]["organism"].replace("'", "") if not children[i] else "" for i, lab in enumerate(label)]
    Path("results/phylo_tree").mkdir(parents=True, exist_ok=True)
    (Path("results/phylo_tree") / f"{args.set}.nwk").write_text(to_newick(parent, length, names))
    lin = {reps[k][0]: {"organism": prof[k]["organism"].replace("'", ""),
                        "lineage": [x for x in reps[k][1].split(";")]} for k in inside + out}
    dest = Path("data/markers") / f"{args.set}_lineage.json"
    dest.write_text(json.dumps({"lineage": lin, "phylum": args.phylum,
                                "rule": "GTDB species reps matched to UniProt proteomes by species name; "
                                        f"ambiguous names skipped; {len(out)} random other bacteria as outgroup"},
                               indent=1))
    n_tips = sum(1 for i in range(len(parent)) if not children[i])
    print(f"{len(inside)} in {args.phylum}, {len(out)} outgroup; tree {n_tips} tips -> "
          f"results/phylo_tree/{args.set}.nwk, {dest}")
    by = {}
    for k in inside:
        c = reps[k][1].split(";")[2]
        by[c] = by.get(c, 0) + 1
    print(by, [prof[k]["organism"] for k in inside if re.search("Gloeomargarit|Gloeobacter", reps[k][1])])


if __name__ == "__main__":
    main()
