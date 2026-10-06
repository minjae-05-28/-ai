"""Ribosomal marker sequences from UniProt proteomes, for clades outside the project catalogues.

    python scripts/uniprot_markers.py --group amoebozoa,discoba --set amoeba [--shard 0 --n-shards 8]

Writes data/markers/<set>/<slug>.json in the format scripts/ribosomal_tree.py --build already
reads ({"species": ..., "markers": {family: sequence}}), so the tree is built by that script.

Why: ribosomal_tree.py collects markers by fetching proteomes from NCBI Datasets keyed by the
project catalogues. Clades collected from UniProt (Amoebozoa, Patescibacteria, giant viruses) are
not in those catalogues, and NCBI has no annotated assembly for many of them. Here the markers come
from the same UniProt proteomes the gene-content data came from: for each proteome, the longest
protein carrying each wanted ribosomal Pfam family, by UniProt's own Pfam cross-references.

The family filter is ribosomal_tree.wanted(fam, "eukaryotes") for eukaryotic sets and
wanted(fam, "prokaryotes") otherwise, so mitochondrial-type ribosomal paralogs are excluded.
"""

import argparse
import json
import re
import sys
import urllib.parse
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from ribosomal_tree import wanted  # noqa: E402
from uniprot_proteomes import GROUPS, REST, get  # noqa: E402

OUT = Path("data/markers")


def slug(name):
    return re.sub(r"[^A-Za-z0-9]+", "_", name).strip("_")


def families(pfam_meta, cat):
    """Pfam accession -> family name, for the ribosomal families wanted in this set."""
    return {v["accession"].split(".")[0]: k for k, v in pfam_meta.items() if wanted(k, cat)}


def markers_for(upid, acc_to_name):
    """family -> longest protein sequence carrying it, from one UniProt proteome."""
    q = urllib.parse.quote(f"proteome:{upid}")
    text = get(f"{REST}/uniprotkb/stream?query={q}&format=tsv&fields=accession,xref_pfam,sequence&compressed=true")
    best = {}
    for ln in text.split("\n")[1:]:
        parts = ln.split("\t")
        if len(parts) < 3 or not parts[2]:
            continue
        seq = parts[2].rstrip("*")
        for a in {x for x in parts[1].split(";") if x}:
            fam = acc_to_name.get(a)
            if fam and (fam not in best or len(seq) > len(best[fam])):
                best[fam] = seq
    return best


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--group", default="", help="comma-separated keys of uniprot_proteomes.GROUPS")
    ap.add_argument("--upids", default="", help="a <set>_pick.json from pick_clade_sample.py: these "
                                                "proteomes too, whatever their kingdom")
    ap.add_argument("--set", required=True, help="output set name under data/markers/")
    ap.add_argument("--shard", type=int, default=0)
    ap.add_argument("--n-shards", type=int, default=1)
    args = ap.parse_args()
    groups = [g for g in args.group.split(",") if g]
    unknown = [g for g in groups if g not in GROUPS]
    if unknown:
        raise SystemExit(f"unknown groups: {unknown}; known: {sorted(GROUPS)}")
    picked = set(json.loads(Path(args.upids).read_text())["upids"]) if args.upids else set()
    if not groups and not picked:
        raise SystemExit("give --group and/or --upids")

    # Proteomes of these groups, from the collected shards (kingdom + organism are stored there).
    import gzip

    kingdoms = {GROUPS[g][1] for g in groups}
    rows, row_kingdoms = {}, set()
    for f in sorted(Path("data/uniprot/shards").glob("*.json.gz")):
        for upid, p in json.loads(gzip.open(f, "rt").read()).items():
            if p.get("kingdom") in kingdoms or upid in picked:
                rows[upid] = p["organism"]
                row_kingdoms.add(p.get("kingdom"))
    if not rows:
        raise SystemExit(f"no collected proteomes with kingdom in {sorted(kingdoms)}; run public-genomes first")
    if picked - set(rows):
        print(f"  {len(picked - set(rows))} picked proteomes are not in the shards")
    cat = "eukaryotes" if row_kingdoms & {"eukaryotes", "fungi"} else "prokaryotes"
    meta = json.loads(Path("data/eukaryotes/pfam_meta.json").read_text())
    acc_to_name = families(meta, cat)
    print(f"{len(acc_to_name)} ribosomal Pfam families wanted for set '{args.set}' (filter: {cat})")
    mine = sorted(rows)[args.shard :: args.n_shards]
    out = OUT / args.set
    out.mkdir(parents=True, exist_ok=True)
    print(f"{len(rows)} proteomes in the set, {len(mine)} in this shard", flush=True)
    for i, upid in enumerate(mine):
        dest = out / f"{slug(rows[upid])}.json"
        if dest.exists():
            continue
        try:
            best = markers_for(upid, acc_to_name)
        except Exception as e:
            print(f"  skip {upid} ({rows[upid]}): {e}", flush=True)
            continue
        dest.write_text(json.dumps({"species": rows[upid], "markers": best}))
        if i % 10 == 0 or len(best) < 10:
            print(f"  {i + 1}/{len(mine)} {rows[upid][:50]}: {len(best)} markers", flush=True)
    print(f"Done -> {out}/")


if __name__ == "__main__":
    main()
