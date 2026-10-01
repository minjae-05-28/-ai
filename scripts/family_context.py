"""Context features (expression, domain partners, operons, exons) per Pfam family in one genome.

    python scripts/family_context.py --list-missing
    python scripts/family_context.py --entry "prokaryotes/Thermus thermophilus" --pfam pfam/Pfam-A.hmm

Covers every catalogued bacterium/archaeon and the free-living eukaryotes (family features
are measured where the families are still present). Runs on GitHub Actions
(.github/workflows/family-context.yml). Writes data/family_context/<catalog>/<species>.json;
see organelle_evo.context for the columns.
"""

import argparse
import io
import json
import re
import zipfile
from collections import defaultdict
from pathlib import Path

from organelle_evo.eukaryotes import catalog as euk
from organelle_evo.prokaryotes import catalog as pro

OUT = Path("data/family_context")


def entries():
    out = [f"prokaryotes/{s}" for s in pro.SPECIES]
    out += [f"eukaryotes/{s}" for s in euk.SPECIES if euk.lifestyle(s) == "free_living"]
    return out


def path(entry):
    cat, sp = entry.split("/", 1)
    return OUT / cat / f"{(pro if cat == 'prokaryotes' else euk).slug(sp)}.json"


def fetch(species):
    from organelle_evo.eukaryotes.proteomes import API, _get, find_assembly, protein_to_gene, read_fasta

    report = find_assembly(species)
    if report is None:
        raise LookupError(f"no annotated assembly for {species}")
    url = (f"{API}/genome/accession/{report['accession']}/download"
           "?include_annotation_type=PROT_FASTA&include_annotation_type=GENOME_GFF&include_annotation_type=CDS_FASTA")
    zf = zipfile.ZipFile(io.BytesIO(_get(url)))
    names = zf.namelist()
    proteins = read_fasta(zf.read(next(n for n in names if n.endswith("protein.faa"))).decode())
    gff = zf.read(next(n for n in names if re.search(r"genomic\.gff$", n))).decode()
    cdsn = next((n for n in names if n.endswith("cds_from_genomic.fna")), None)
    cds = zf.read(cdsn).decode() if cdsn else ""
    gene_of = protein_to_gene(gff)
    best = {}
    for pid, seq in proteins.items():
        g = gene_of.get(pid, pid)
        if len(seq) > len(proteins.get(best.get(g), "")):
            best[g] = pid
    return report, {pid: proteins[pid] for pid in best.values()}, cds, gff


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--entry")
    ap.add_argument("--pfam", default="pfam/Pfam-A.hmm")
    ap.add_argument("--families", help="only search these Pfam families (one per line)")
    ap.add_argument("--list-missing", action="store_true")
    args = ap.parse_args()
    if args.list_missing:
        print(json.dumps([e for e in entries() if not path(e).exists()]))
        return

    import pyhmmer

    from organelle_evo.context import COLUMNS, family_context, gff_cds, parse_cds_fasta
    from organelle_evo.eukaryotes.pfam import _digitize, _s, load_hmms

    cat, species = args.entry.split("/", 1)
    report, proteins, cds_text, gff = fetch(species)
    hmms = load_hmms(args.pfam)
    if args.families:
        keep = set(Path(args.families).read_text().split())
        hmms = [h for h in hmms if _s(h.name) in keep]
    fams_of = defaultdict(set)
    for top in pyhmmer.hmmsearch(hmms, _digitize(proteins), bit_cutoffs="gathering"):
        fam = _s(top.query.name)
        for hit in top:
            if hit.included:
                fams_of[_s(hit.name)].add(fam)
    cds = parse_cds_fasta(cds_text)
    loc = gff_cds(gff)
    fams = family_context(dict(fams_of), {p: s for p, s in cds.items() if p in proteins}, loc, cat == "prokaryotes")
    p = path(args.entry)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps({"species": species, "accession": report["accession"], "n_genes": len(proteins),
                             "n_cds": len(cds), "columns": COLUMNS, "families": fams}, separators=(",", ":")))
    print(f"{args.entry}: {len(proteins)} genes, {len(cds)} CDS, {len(fams)} families")


if __name__ == "__main__":
    main()
