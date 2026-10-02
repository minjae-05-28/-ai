"""Genome GC content of every proteome in data/composition, for the GC confound check.

    python scripts/fetch_gc.py --out results/gc/gc.json

Assemblies (GCF_/GCA_) take NCBI's assembly_stats.gc_percent from the Datasets API, so this
part runs on GitHub Actions (NCBI is not reachable from the development sandbox). Organelle
and endosymbiont records (nucleotide accessions) are counted from the GenBank files in
data/raw. Output: {species: {"accession", "gc"}} per catalogue (gc as a fraction).
"""

import argparse
import json
from pathlib import Path

from organelle_evo.eukaryotes.proteomes import API, _get

C = Path("data/composition")


def raw_gc():
    """VERSION accession -> GC fraction, from the sequences in data/raw."""
    out = {}
    for gb in Path("data/raw").glob("*/*.gb"):
        acc, seq, in_seq = None, [], False
        for line in gb.read_text().splitlines():
            if line.startswith("VERSION"):
                acc, seq, in_seq = line.split()[1], [], False
            elif line.startswith("ORIGIN"):
                in_seq = True
            elif line.startswith("//"):
                s = "".join(seq).lower()
                gc, at = s.count("g") + s.count("c"), s.count("a") + s.count("t")
                if acc and gc + at:
                    out[acc] = gc / (gc + at)
                in_seq = False
            elif in_seq:
                seq.append("".join(line.split()[1:]))
    return out


def gc3_of(cds_seqs):
    """GC at third codon positions over all coding sequences (stop codons excluded)."""
    gc = at = 0
    for s in cds_seqs:
        s = s.upper()
        for i in range(2, len(s) - 3, 3):  # last codon is the stop
            b = s[i]
            if b in "GC":
                gc += 1
            elif b in "AT":
                at += 1
    return gc / (gc + at) if gc + at else None


def raw_gc3():
    from Bio import SeqIO

    out = {}
    for gb in Path("data/raw").glob("*/*.gb"):
        for rec in SeqIO.parse(gb, "genbank"):
            seqs = [str(f.extract(rec.seq)) for f in rec.features if f.type == "CDS" and "translation" in f.qualifiers]
            out[rec.id] = gc3_of(seqs)
    return out


def assembly_gc3(accs):
    import io
    import zipfile

    from organelle_evo.context import parse_cds_fasta

    out = {}
    for i, acc in enumerate(accs):
        try:
            zf = zipfile.ZipFile(io.BytesIO(_get(f"{API}/genome/accession/{acc}/download?include_annotation_type=CDS_FASTA")))
            name = next(n for n in zf.namelist() if n.endswith("cds_from_genomic.fna"))
            out[acc] = gc3_of(parse_cds_fasta(zf.read(name).decode()).values())
        except Exception as e:  # noqa: BLE001
            print(f"{acc}: {e}")
        print(f"{i + 1}/{len(accs)} GC3")
    return out


def assembly_gc(accs, batch=20):
    out = {}
    for i in range(0, len(accs), batch):
        chunk = accs[i:i + batch]
        url = f"{API}/genome/accession/{','.join(chunk)}/dataset_report?page_size={batch}"
        for r in json.loads(_get(url)).get("reports", []):
            gc = r.get("assembly_stats", {}).get("gc_percent")
            if gc is not None:
                out[r["accession"]] = float(gc) / 100
        print(f"{min(i + batch, len(accs))}/{len(accs)} assemblies")
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default="results/gc/gc.json")
    ap.add_argument("--local-only", action="store_true", help="skip NCBI (organelles and symbionts only)")
    ap.add_argument("--gc3", action="store_true", help="also GC at third codon positions (downloads every CDS set)")
    args = ap.parse_args()
    entries = {}
    for f in C.glob("**/*.json"):
        d = json.loads(f.read_text())
        entries.setdefault(str(f.parent.relative_to(C)), {})[d["species"]] = d["accession"]
    raw = raw_gc()
    asm = [a for cat in entries.values() for a in cat.values() if a.startswith(("GCF_", "GCA_"))]
    found = {} if args.local_only else assembly_gc(sorted(set(asm)))
    found.update(raw)
    gc3 = {}
    if args.gc3:
        gc3 = raw_gc3()
        if not args.local_only:
            gc3.update(assembly_gc3(sorted(set(asm))))
    res = {cat: {s: {"accession": a, "gc": found.get(a), **({"gc3": gc3.get(a)} if args.gc3 else {})}
                 for s, a in sorted(sp.items())} for cat, sp in sorted(entries.items())}
    missing = [(c, s) for c, sp in res.items() for s, v in sp.items() if v["gc"] is None]
    print(f"{sum(len(v) for v in res.values()) - len(missing)} with GC, {len(missing)} missing: {missing[:10]}")
    Path(args.out).parent.mkdir(parents=True, exist_ok=True)
    Path(args.out).write_text(json.dumps(res, indent=1))


if __name__ == "__main__":
    main()
