"""Proteome sequence statistics for one species (run by .github/workflows/proteome-composition.yml).

    python scripts/proteome_composition.py --list-missing            # "catalog|species" entries (JSON)
    python scripts/proteome_composition.py --entry "prokaryotes|Thermus thermophilus"

Downloads the same proteome as the Pfam profiles (NCBI Datasets) and stores only summary
statistics in data/composition/<catalog>/<species>.json.
"""

import argparse
import importlib
import json
from pathlib import Path

OUT = Path("data/composition")
CATALOGS = ("prokaryotes", "eukaryotes")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--list-missing", action="store_true")
    ap.add_argument("--entry")
    args = ap.parse_args()
    if args.list_missing:
        todo = []
        for cat in CATALOGS:
            mod = importlib.import_module(f"organelle_evo.{cat}.catalog")
            todo += [f"{cat}|{s}" for s in mod.SPECIES if not (OUT / cat / f"{mod.slug(s)}.json").exists()]
        print(json.dumps(todo))
        return
    cat, species = args.entry.split("|", 1)
    mod = importlib.import_module(f"organelle_evo.{cat}.catalog")
    from organelle_evo.eukaryotes.proteomes import fetch_proteome
    from organelle_evo.sequence import proteome_stats

    report, proteins = fetch_proteome(species)
    stats = proteome_stats(proteins.values())
    (OUT / cat).mkdir(parents=True, exist_ok=True)
    (OUT / cat / f"{mod.slug(species)}.json").write_text(json.dumps(
        {"species": species, "accession": report["accession"], **stats}, indent=1))
    print(f"{species}: {stats['n_proteins']} proteins, IVYWREL {stats['ivywrel']:.3f}, median pI {stats['median_pi']:.2f}")


if __name__ == "__main__":
    main()
