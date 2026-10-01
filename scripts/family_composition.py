"""Amino-acid composition of each Pfam family's domains in one bacterium or archaeon.

    python scripts/family_composition.py --list-missing
    python scripts/family_composition.py --species "Thermus thermophilus" --pfam pfam/Pfam-A.hmm

Writes data/family_composition/prokaryotes/<species>.json: family -> [n_genes, n_domains,
20 amino-acid counts over the domain regions (order ACDEFGHIKLMNPQRSTVWY)].
"""

import argparse
import json
import re
from collections import defaultdict
from pathlib import Path

from organelle_evo.prokaryotes.catalog import SPECIES, slug

AA = "ACDEFGHIKLMNPQRSTVWY"  # same order as organelle_evo.sequence.AA (kept numpy-free for --list-missing)

OUT = Path("data/family_composition/prokaryotes")


def family_composition(proteins, hmms):
    import pyhmmer

    from organelle_evo.eukaryotes.pfam import _digitize, _s

    seqs = _digitize(proteins)
    genes = defaultdict(set)
    acc = defaultdict(lambda: [0] + [0] * len(AA))
    for top in pyhmmer.hmmsearch(hmms, seqs, bit_cutoffs="gathering"):
        fam = _s(top.query.name)
        for hit in top:
            if not hit.included:
                continue
            pid = _s(hit.name)
            for dom in hit.domains:
                if not dom.included:
                    continue
                seg = re.sub(r"[^A-Z]", "", proteins[pid][dom.env_from - 1: dom.env_to].upper())
                a = acc[fam]
                a[0] += 1
                for i, aa in enumerate(AA):
                    a[i + 1] += seg.count(aa)
                genes[fam].add(pid)
    return {f: [len(genes[f]), *acc[f]] for f in genes}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--species")
    ap.add_argument("--pfam", default="pfam/Pfam-A.hmm")
    ap.add_argument("--list-missing", action="store_true")
    args = ap.parse_args()
    if args.list_missing:
        print(json.dumps([s for s in SPECIES if not (OUT / f"{slug(s)}.json").exists()]))
        return
    from organelle_evo.eukaryotes.pfam import load_hmms
    from organelle_evo.eukaryotes.proteomes import fetch_proteome

    report, proteins = fetch_proteome(args.species)
    fams = family_composition(proteins, load_hmms(args.pfam))
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / f"{slug(args.species)}.json").write_text(json.dumps(
        {"species": args.species, "accession": report["accession"], "columns": ["n_genes", "n_domains", *AA],
         "families": fams}, separators=(",", ":")))
    print(f"{args.species}: {len(fams)} families")


if __name__ == "__main__":
    main()
