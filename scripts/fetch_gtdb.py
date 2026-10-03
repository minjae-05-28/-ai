"""GTDB species representatives: taxonomy and genome traits for every bacterial and archaeal
species in the Genome Taxonomy Database (run by .github/workflows/uniprot-proteomes.yml;
GTDB is not reachable from the sandbox).

    python scripts/fetch_gtdb.py      -> data/gtdb/species_reps.tsv.gz, data/gtdb/VERSION

Keeps one row per GTDB species (gtdb_representative == t) and the columns a genome-level law
needs: GTDB and NCBI taxonomy, NCBI taxid (to join the trait table in data/traits/), GC,
genome size, protein count, coding density and CheckM2 completeness/contamination
(assembly quality, to filter or correct apparent gene loss).
"""

import csv
import gzip
import io
import re
import sys
import urllib.request
from pathlib import Path

BASE = "https://data.gtdb.ecogenomic.org/releases/latest"
OUT = Path("data/gtdb")
KEEP = ["accession", "gtdb_taxonomy", "ncbi_taxonomy", "ncbi_taxid", "ncbi_species_taxid", "ncbi_organism_name",
        "gc_percentage", "genome_size", "protein_count", "coding_density", "checkm2_completeness",
        "checkm2_contamination", "checkm_completeness", "checkm_contamination", "ncbi_isolation_source",
        "ncbi_genome_category", "mimag_high_quality"]


def fetch(url):
    with urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": "organelle-evo"}), timeout=600) as r:
        return r.read()


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    version = fetch(f"{BASE}/VERSION.txt").decode().strip()
    (OUT / "VERSION").write_text(version + "\n")
    index = fetch(f"{BASE}/").decode()
    found = set(re.findall(r'href="([^"/]*_metadata[^"/]*\.(?:tsv\.gz|tar\.gz))"', index))
    # Prefer .tsv.gz; some releases ship the table only inside a .tar.gz.
    stems = {}
    for n in sorted(found):
        stem = n.split("_metadata")[0]
        if stem not in stems or n.endswith(".tsv.gz"):
            stems[stem] = n
    names = sorted(stems.values())
    print("GTDB", version.splitlines()[0], names)
    if not names:
        sys.exit("no metadata files found in the release index")
    n_out = 0
    with gzip.open(OUT / "species_reps.tsv.gz", "wt", newline="") as fo:
        w = None
        for name in names:
            local = OUT / name
            urllib.request.urlretrieve(f"{BASE}/{name}", local)  # hundreds of MB: stream from disk
            if name.endswith(".tar.gz"):
                import tarfile

                tar = tarfile.open(local, "r:gz")
                member = next(m for m in tar.getmembers() if m.name.endswith(".tsv"))
                fi = io.TextIOWrapper(tar.extractfile(member), newline="")
            else:
                fi = gzip.open(local, "rt", newline="")
            csv.field_size_limit(10**8)
            reader = csv.DictReader(fi, delimiter="\t")
            cols = KEEP  # fixed columns, so bacterial and archaeal rows line up
            missing = [c for c in KEEP if c not in reader.fieldnames]
            if missing:
                print(f"  {name}: columns not in this release (left empty): {missing}")
            if w is None:
                w = csv.writer(fo, delimiter="\t")
                w.writerow(["domain", *cols])
            domain = "archaea" if name.startswith("ar") else "bacteria"
            n = 0
            for row in reader:
                if row.get("gtdb_representative") == "t":
                    w.writerow([domain, *[row.get(c, "") for c in cols]])
                    n += 1
            n_out += n
            fi.close()
            local.unlink()
            print(f"  {name}: {n} species representatives")
    print(f"{n_out} species -> {OUT}/species_reps.tsv.gz")


if __name__ == "__main__":
    main()
