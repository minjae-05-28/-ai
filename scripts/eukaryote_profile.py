"""Pfam family profile of one species (run by .github/workflows/eukaryote-pfam.yml).

    python scripts/eukaryote_profile.py --species "Entamoeba histolytica" --pfam Pfam-A.hmm
    python scripts/eukaryote_profile.py --list-missing        # species still to profile (JSON)
    python scripts/eukaryote_profile.py --pfam Pfam-A.hmm --dump-meta
"""

import argparse
import json
import time
from pathlib import Path

from organelle_evo.eukaryotes.catalog import SPECIES, slug

OUT = Path("data/eukaryotes")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--species")
    ap.add_argument("--pfam", default="pfam/Pfam-A.hmm")
    ap.add_argument("--list-missing", action="store_true")
    ap.add_argument("--dump-meta", action="store_true")
    args = ap.parse_args()

    if args.list_missing:
        print(json.dumps([s for s in SPECIES if not (OUT / f"{slug(s)}.json").exists()]))
        return

    from organelle_evo.eukaryotes.pfam import family_profile, hmm_metadata, load_hmms

    OUT.mkdir(parents=True, exist_ok=True)
    t0 = time.time()
    hmms = load_hmms(args.pfam)
    print(f"loaded {len(hmms)} Pfam HMMs in {time.time() - t0:.0f}s")
    if args.dump_meta:
        (OUT / "pfam_meta.json").write_text(json.dumps(hmm_metadata(hmms)))
        return

    from organelle_evo.eukaryotes.proteomes import fetch_proteome

    report, proteins = fetch_proteome(args.species)
    print(f"{args.species}: {report['accession']} "
          f"({report.get('organism', {}).get('organism_name')}), {len(proteins)} genes")
    t0 = time.time()
    families = family_profile(proteins, hmms)
    print(f"{len(families)} families in {time.time() - t0:.0f}s")
    (OUT / f"{slug(args.species)}.json").write_text(json.dumps({
        "species": args.species,
        "organism": report.get("organism", {}).get("organism_name"),
        "accession": report["accession"],
        "n_genes": len(proteins),
        "columns": ["n_genes", "n_domains", "sum_gravy", "sum_tm_helices", "sum_length"],
        "families": families,
    }))


if __name__ == "__main__":
    main()
