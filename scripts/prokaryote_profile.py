"""Pfam family profile of one bacterium or archaeon (run by .github/workflows/prokaryote-pfam.yml).

    python scripts/prokaryote_profile.py --species "Colwellia psychrerythraea" --pfam Pfam-A.hmm
    python scripts/prokaryote_profile.py --list-missing

Same pipeline as eukaryote_profile.py (NCBI Datasets proteome, HMMER against Pfam), with
the prokaryote catalog and every Pfam family searched.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import eukaryote_profile as profile  # noqa: E402

from organelle_evo.prokaryotes import catalog  # noqa: E402

profile.SPECIES, profile.slug, profile.OUT = catalog.SPECIES, catalog.slug, Path("data/prokaryotes")

if __name__ == "__main__":
    profile.main()
