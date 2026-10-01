"""Proteome statistics for organelles and insect endosymbionts from the GenBank files in data/raw.

    python scripts/endosymbiont_composition.py

Writes data/composition/endosymbiosis/<system>/<record>.json (every protein-coding CDS).
"""

import json
from pathlib import Path

from organelle_evo.realdata.dataset import read_genbank
from organelle_evo.sequence import proteome_stats

OUT = Path("data/composition/endosymbiosis")


def main():
    for system_dir in sorted(Path("data/raw").iterdir()):
        if not system_dir.is_dir():
            continue
        (OUT / system_dir.name).mkdir(parents=True, exist_ok=True)
        for gb in sorted(system_dir.glob("*.gb")):
            rec = read_genbank(gb)
            prots = list(rec.cds.values()) or list(rec.proteins.values())
            if len(prots) < 3:
                continue
            stats = proteome_stats(prots)
            if not stats["n_proteins"]:
                continue
            (OUT / system_dir.name / f"{gb.stem}.json").write_text(json.dumps(
                {"species": rec.organism, "accession": rec.accession, **stats}, indent=1))
            print(f"{system_dir.name:20s} {rec.organism[:40]:40s} {stats['n_proteins']:5d} proteins  "
                  f"FYMINK {stats['fymink']:.3f}  N/res {stats['n_side']:.3f}  pI {stats['median_pi']:.2f}")


if __name__ == "__main__":
    main()
