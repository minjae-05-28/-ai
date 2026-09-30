"""Download one annotated proteome per species from NCBI Datasets (v2 REST API).

Only the longest protein isoform per gene is kept, so gene-family counts are not
inflated by alternative splicing.
"""

import io
import json
import re
import urllib.parse
import urllib.request
import zipfile

API = "https://api.ncbi.nlm.nih.gov/datasets/v2"
_LEVEL = {"Complete Genome": 3, "Chromosome": 2, "Scaffold": 1, "Contig": 0}


def _get(url: str) -> bytes:
    req = urllib.request.Request(url, headers={"Accept": "application/json, application/zip"})
    with urllib.request.urlopen(req, timeout=600) as r:
        return r.read()


def _score(report: dict, species: str) -> tuple:
    info = report.get("assembly_info", {})
    genes = (
        report.get("annotation_info", {}).get("stats", {}).get("gene_counts", {}).get("protein_coding", 0)
    )
    name = report.get("organism", {}).get("organism_name", "")
    return (
        name.lower().startswith(species.lower()),
        report.get("source_database") == "SOURCE_DATABASE_REFSEQ",
        info.get("refseq_category") == "reference genome",
        _LEVEL.get(info.get("assembly_level", ""), 0),
        int(genes or 0),
    )


def choose_assembly(reports: list[dict], species: str) -> dict | None:
    """Best annotated assembly: the species itself, RefSeq, reference, most complete."""
    annotated = [r for r in reports if r.get("annotation_info")]
    return max(annotated, key=lambda r: _score(r, species)) if annotated else None


def find_assembly(species: str) -> dict | None:
    taxon = urllib.parse.quote(species)
    url = f"{API}/genome/taxon/{taxon}/dataset_report?filters.has_annotation=true&page_size=100"
    reports = json.loads(_get(url)).get("reports", [])
    return choose_assembly(reports, species)


def _gff_attrs(field: str) -> dict:
    return dict(kv.split("=", 1) for kv in field.strip().split(";") if "=" in kv)


def protein_to_gene(gff_text: str) -> dict[str, str]:
    """protein_id -> gene key, from CDS lines of an NCBI GFF3."""
    mapping = {}
    for line in gff_text.splitlines():
        if line.startswith("#"):
            continue
        cols = line.split("\t")
        if len(cols) < 9 or cols[2] != "CDS":
            continue
        a = _gff_attrs(cols[8])
        pid = a.get("protein_id")
        gene = a.get("gene") or a.get("locus_tag") or a.get("Parent")
        if pid and gene:
            mapping[pid] = gene
    return mapping


def read_fasta(text: str) -> dict[str, str]:
    seqs, name, buf = {}, None, []
    for line in text.splitlines():
        if line.startswith(">"):
            if name is not None:
                seqs[name] = "".join(buf)
            name, buf = line[1:].split()[0], []
        elif line.strip():
            buf.append(line.strip())
    if name is not None:
        seqs[name] = "".join(buf)
    return seqs


def longest_per_gene(proteins: dict[str, str], gene_of: dict[str, str]) -> dict[str, str]:
    """gene -> longest protein; proteins without a gene mapping count as their own gene."""
    best: dict[str, str] = {}
    for pid, seq in proteins.items():
        gene = gene_of.get(pid, pid)
        if len(seq) > len(best.get(gene, "")):
            best[gene] = seq
    return best


def fetch_proteome(species: str) -> tuple[dict, dict[str, str]]:
    """(assembly report, gene -> longest protein) for a species."""
    report = find_assembly(species)
    if report is None:
        raise LookupError(f"no annotated assembly for {species}")
    acc = report["accession"]
    url = (
        f"{API}/genome/accession/{acc}/download"
        "?include_annotation_type=PROT_FASTA&include_annotation_type=GENOME_GFF"
    )
    zf = zipfile.ZipFile(io.BytesIO(_get(url)))
    names = zf.namelist()
    faa = next(n for n in names if n.endswith("protein.faa"))
    gff = next((n for n in names if re.search(r"genomic\.gff$", n)), None)
    proteins = read_fasta(zf.read(faa).decode())
    gene_of = protein_to_gene(zf.read(gff).decode()) if gff else {}
    return report, longest_per_gene(proteins, gene_of)
