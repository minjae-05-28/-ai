"""Measured RNA expression per Pfam family, quantified from raw RNA-seq reads.

    python scripts/rna_expression.py --list-missing
    python scripts/rna_expression.py --entry "prokaryotes/Bacillus subtilis" --pfam pfam/Pfam-A.hmm

For every free-living species that stands in for an ancestor (the relatives in the pairs):
  1. proteins + coding sequences from the NCBI annotated assembly
  2. Pfam families of the proteins (HMMER, gathering thresholds)
  3. up to three public Illumina RNA-seq runs from ENA (different studies when possible),
     the first READS reads of each streamed from the FASTQ
  4. transcript abundance with salmon against the coding sequences (TPM)
  5. per family: number of genes with data, mean log2(TPM+1), mean within-species percentile

Runs on GitHub Actions (.github/workflows/rna-expression.yml; needs salmon on PATH).
Output: data/expression/<catalog>/<species>.json.
"""

import argparse
import json
import math
import os
import re
import subprocess
import tempfile
import urllib.parse
import urllib.request
from collections import defaultdict
from pathlib import Path

from organelle_evo.eukaryotes import catalog as euk
from organelle_evo.prokaryotes import catalog as pro

OUT = Path("data/expression")
READS = 3_000_000
ENA = "https://www.ebi.ac.uk/ena/portal/api/search"


def entries():
    anc_p = sorted({a for a, _ in pro.resolve_pairs(pro.SPECIES)})
    anc_e = sorted(s for s in euk.SPECIES if euk.SPECIES[s].lifestyle == euk.FREE)
    return [f"prokaryotes/{s}" for s in anc_p] + [f"eukaryotes/{s}" for s in anc_e]


def path(entry):
    cat, sp = entry.split("/", 1)
    return OUT / cat / f"{(pro if cat == 'prokaryotes' else euk).slug(sp)}.json"


def ena_runs(taxid, n=3):
    q = f'tax_tree({taxid}) AND library_strategy="RNA-Seq" AND library_source="TRANSCRIPTOMIC" AND instrument_platform="ILLUMINA"'
    url = ENA + "?" + urllib.parse.urlencode({"result": "read_run", "query": q, "limit": 500, "format": "tsv",
                                              "fields": "run_accession,study_accession,fastq_ftp,read_count,library_layout"})
    with urllib.request.urlopen(url, timeout=120) as r:
        lines = r.read().decode().splitlines()
    rows = [dict(zip(lines[0].split("\t"), l.split("\t"))) for l in lines[1:]] if lines else []
    rows = [r for r in rows if r.get("fastq_ftp") and r.get("read_count", "").isdigit() and int(r["read_count"]) >= 2_000_000]
    rows.sort(key=lambda r: int(r["read_count"]))
    picked, studies = [], set()
    for r in rows:  # one run per study first
        if r["study_accession"] not in studies:
            picked.append(r)
            studies.add(r["study_accession"])
        if len(picked) == n:
            break
    for r in rows:
        if len(picked) == n:
            break
        if r not in picked:
            picked.append(r)
    return picked


def stream_reads(ftp, dest):
    first = ftp.split(";")[0]
    url = "https://" + first if not first.startswith("http") else first
    cmd = f"curl -sSL --retry 3 '{url}' | gunzip -c 2>/dev/null | head -n {READS * 4} > '{dest}'"
    subprocess.run(["bash", "-o", "pipefail", "-c", cmd + " || true"], check=False, timeout=3600)
    return dest.stat().st_size if dest.exists() else 0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--entry")
    ap.add_argument("--pfam", default="pfam/Pfam-A.hmm")
    ap.add_argument("--families", help="only these Pfam families (one per line)")
    ap.add_argument("--list-missing", action="store_true")
    args = ap.parse_args()
    if args.list_missing:
        print(json.dumps([e for e in entries() if not path(e).exists()]))
        return

    import sys

    import pyhmmer

    sys.path.insert(0, str(Path(__file__).resolve().parent))
    from family_context import fetch

    from organelle_evo.context import parse_cds_fasta
    from organelle_evo.eukaryotes.pfam import _digitize, _s, load_hmms

    cat, species = args.entry.split("/", 1)
    report, proteins, cds_text, _ = fetch(species)
    taxid = report.get("organism", {}).get("tax_id")
    cds = {p: s for p, s in parse_cds_fasta(cds_text).items() if p in proteins}
    runs = ena_runs(taxid) if taxid else []
    print(f"{species}: taxid {taxid}, {len(proteins)} proteins, {len(cds)} CDS, {len(runs)} RNA-seq runs", flush=True)
    result = {"species": species, "accession": report["accession"], "taxid": taxid, "runs": [], "families": {}}
    if runs and cds:
        hmms = load_hmms(args.pfam)
        if args.families:
            keep = set(Path(args.families).read_text().split())
            hmms = [h for h in hmms if _s(h.name) in keep]
        fams_of = defaultdict(set)
        for top in pyhmmer.hmmsearch(hmms, _digitize(proteins), bit_cutoffs="gathering"):
            for hit in top:
                if hit.included:
                    fams_of[_s(hit.name)].add(_s(top.query.name))
        with tempfile.TemporaryDirectory(dir=os.environ.get("RNA_TMP")) as tmp:
            tx = Path(tmp) / "cds.fa"
            tx.write_text("".join(f">{p}\n{s}\n" for p, s in cds.items()))
            subprocess.run(["salmon", "index", "-t", str(tx), "-i", f"{tmp}/idx", "-k", "25", "-p", "4"],
                           check=True, capture_output=True)
            logtpm = defaultdict(list)
            for r in runs:
                fq = Path(tmp) / f"{r['run_accession']}.fq"
                size = stream_reads(r["fastq_ftp"], fq)
                if size < 1_000_000:
                    print(f"  {r['run_accession']}: download failed")
                    continue
                q = Path(tmp) / f"q_{r['run_accession']}"
                subprocess.run(["salmon", "quant", "-i", f"{tmp}/idx", "-l", "A", "-r", str(fq), "-p", "4",
                                "--validateMappings", "-o", str(q)], check=True, capture_output=True)
                meta = json.loads((q / "aux_info" / "meta_info.json").read_text())
                rate = meta.get("percent_mapped", 0)
                print(f"  {r['run_accession']} ({r['study_accession']}): mapping rate {rate:.1f}%", flush=True)
                fq.unlink()
                if rate < 10:
                    continue  # wrong organism, rRNA-dominated or degraded
                result["runs"].append({"run": r["run_accession"], "study": r["study_accession"], "mapped_percent": rate})
                for line in (q / "quant.sf").read_text().splitlines()[1:]:
                    name, _, _, tpm, _ = line.split("\t")
                    logtpm[name].append(math.log2(float(tpm) + 1))
        if result["runs"]:
            gene = {p: sum(v) / len(v) for p, v in logtpm.items() if len(v) == len(result["runs"])}
            order = sorted(gene, key=gene.get)
            pct = {p: i / max(len(order) - 1, 1) for i, p in enumerate(order)}
            acc = defaultdict(list)
            for p, fs in fams_of.items():
                if p in gene:
                    for f in fs:
                        acc[f].append(p)
            result["families"] = {f: [len(ps), round(sum(gene[p] for p in ps) / len(ps), 3),
                                      round(sum(pct[p] for p in ps) / len(ps), 3)] for f, ps in acc.items()}
            result["n_genes_quantified"] = len(gene)
    p = path(args.entry)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(result, separators=(",", ":")))
    print(f"{species}: {len(result['runs'])} runs used, {len(result['families'])} families")


if __name__ == "__main__":
    main()
