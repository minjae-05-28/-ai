"""GTDB reference trees (bacteria bac120, archaea ar53) for ancestral reconstruction.
Run on Actions (GTDB is not reachable from the sandbox):

    python scripts/fetch_gtdb_tree.py      -> results/phylo_tree/gtdb_{bac120,ar53}.tree.gz

The trees are the GTDB species-representative trees of the same release as
data/gtdb/species_reps.tsv.gz; tips are genome accessions (GB_GCA_... / RS_GCF_...), internal
labels carry GTDB support values and taxon names. Kept whole and gzipped (results/ is what
run-analysis.yml commits).
"""

import gzip
import re
import sys
import urllib.request
from pathlib import Path

BASE = "https://data.gtdb.ecogenomic.org/releases/latest"
OUT = Path("results/phylo_tree")


def fetch(url):
    with urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": "organelle-evo"}), timeout=900) as r:
        return r.read()


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    index = fetch(f"{BASE}/").decode()
    names = sorted(set(re.findall(r'href="([^"/]*(?:bac120|ar53)[^"/]*\.tree(?:\.gz|\.tar\.gz)?)"', index)))
    print("tree files in the release:", names)
    if not names:
        # some releases keep trees under auxillary_files/ or as *_r<ver>.tree
        sub = fetch(f"{BASE}/auxillary_files/").decode()
        names = ["auxillary_files/" + n for n in sorted(set(re.findall(r'href="([^"/]*(?:bac120|ar53)[^"/]*\.tree[^"/]*)"', sub)))]
        print("in auxillary_files:", names)
    done = set()
    for n in names:
        kind = "bac120" if "bac120" in n else "ar53"
        if kind in done:
            continue
        data = fetch(f"{BASE}/{n}")
        if n.endswith(".tar.gz"):
            import io
            import tarfile

            tar = tarfile.open(fileobj=io.BytesIO(data), mode="r:gz")
            m = next(m for m in tar.getmembers() if m.name.endswith(".tree"))
            data = tar.extractfile(m).read()
        elif n.endswith(".gz"):
            data = gzip.decompress(data)
        text = data.decode().strip()
        if not text.endswith(";"):
            sys.exit(f"{n}: not a newick tree")
        (OUT / f"gtdb_{kind}.tree.gz").write_bytes(gzip.compress(text.encode()))
        print(f"{n}: {text.count(',') + 1} tips -> {OUT}/gtdb_{kind}.tree.gz")
        done.add(kind)
    if done != {"bac120", "ar53"}:
        sys.exit(f"missing trees: {sorted({'bac120', 'ar53'} - done)}")


if __name__ == "__main__":
    main()
