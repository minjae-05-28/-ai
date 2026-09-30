"""Download real organelle / endosymbiont genomes from NCBI into data/raw/.

    python scripts/fetch_data.py                 # every system in the catalog
    python scripts/fetch_data.py --system plastid

Needs network access to eutils.ncbi.nlm.nih.gov. Downloads are cached, so re-running
only fetches what is missing.
"""

import argparse
import sys
from pathlib import Path

from organelle_evo.realdata.catalog import CATALOG
from organelle_evo.realdata.ncbi import fetch_species


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--system", choices=list(CATALOG), action="append")
    ap.add_argument("--data", default="data/raw")
    args = ap.parse_args()
    missing = []
    for system in args.system or CATALOG:
        spec = CATALOG[system]
        cache = Path(args.data) / system
        jobs = [(org, spec["query"]) for org in spec["species"]]
        jobs += list(spec.get("extra_queries", {}).items())
        if spec["ancestor"]:
            jobs.append((spec["ancestor"], spec["query"]))
        for org, query in jobs:
            try:
                path = fetch_species(org, query, cache)
            except OSError as e:
                if "403" in str(e):
                    sys.exit(f"NCBI is unreachable ({e}). Allow eutils.ncbi.nlm.nih.gov in the "
                             "network settings and re-run.")
                print(f"  ! {system}/{org}: network error ({e})", file=sys.stderr)
                path = None
            print(f"  {'ok' if path else '--'} {system:20s} {org}" + (f" -> {path.name}" if path else ""))
            if path is None:
                missing.append(f"{system}/{org}")
    if missing:
        print(f"\n{len(missing)} not found: " + ", ".join(missing))


if __name__ == "__main__":
    main()
