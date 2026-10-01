"""NCBI taxonomy (domain ... genus) for every species in the project, for phylogenetic correction.

    python scripts/fetch_taxonomy.py --out results/taxonomy/taxonomy.json

Runs on GitHub Actions (NCBI is not reachable from the development sandbox). Species are
the eukaryote and prokaryote catalogues plus the organisms of the GenBank records in
data/raw (organelle hosts and insect endosymbionts). Names NCBI cannot resolve are retried
with the genus alone.
"""

import argparse
import json
import re
import time
import urllib.parse
from pathlib import Path

from organelle_evo.eukaryotes import catalog as euk
from organelle_evo.eukaryotes.proteomes import API, _get
from organelle_evo.prokaryotes import catalog as pro

RANKS = ("domain", "kingdom", "phylum", "class", "order", "family", "genus")


def raw_organisms():
    names = set()
    for gb in Path("data/raw").glob("*/*.gb"):
        with open(gb) as f:
            for line in f:
                if line.startswith("  ORGANISM"):
                    names.add(line.split("ORGANISM", 1)[1].strip())
                    break
    return names


def lookup(name):
    url = f"{API}/taxonomy/taxon/{urllib.parse.quote(name)}/dataset_report"
    reports = json.loads(_get(url)).get("reports", [])
    for r in reports:
        cls = r.get("taxonomy", {}).get("classification", {})
        if cls:
            return {k: cls[k]["name"] for k in RANKS if k in cls}
    return None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default="results/taxonomy/taxonomy.json")
    args = ap.parse_args()
    names = sorted(set(euk.SPECIES) | set(pro.SPECIES) | raw_organisms())
    out = {}
    for n in names:
        tries = [n, re.sub(r"^Candidatus ", "", n), " ".join(n.split()[:2]), n.split()[0]]
        for t in dict.fromkeys(tries):
            try:
                cls = lookup(t)
            except Exception as e:  # noqa: BLE001
                print(f"  {t}: {e}")
                cls = None
            if cls:
                out[n] = {**cls, "queried": t}
                break
            time.sleep(0.4)
        print(f"{n}: {out.get(n, {}).get('phylum', '?')} / {out.get(n, {}).get('genus', '?')}")
    Path(args.out).parent.mkdir(parents=True, exist_ok=True)
    Path(args.out).write_text(json.dumps(out, indent=1))
    print(f"{len(out)}/{len(names)} resolved -> {args.out}")


if __name__ == "__main__":
    main()
