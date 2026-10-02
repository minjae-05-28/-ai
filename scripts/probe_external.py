"""Probe public expression and knockout data sources (run on Actions; prints what is reachable).

    python scripts/probe_external.py

Writes results/external/probe.json: for each candidate URL, HTTP status, size and the first
lines, so the collectors can be written against what actually exists.
"""

import gzip
import json
import urllib.request
from pathlib import Path

CANDIDATES = {
    # round 3: processed RNA-seq expression
    "atlas_ftp": "https://ftp.ebi.ac.uk/pub/databases/microarray/data/atlas/experiments/",
    "atlas_api_species": "https://www.ebi.ac.uk/gxa/json/experiments",
    "imodulondb_site": "https://imodulondb.org/",
    "imodulondb_github": "https://api.github.com/repos/SBRG/iModulonDB/contents/",
    "imodulondb_data_github": "https://api.github.com/search/repositories?q=imodulon+data",
    "sra_tools_release": "https://api.github.com/repos/ncbi/sra-tools/releases/latest",
    "ena_filereport": "https://www.ebi.ac.uk/ena/portal/api/search?result=read_run&query=tax_eq(1140)%20AND%20library_strategy=%22RNA-Seq%22&fields=run_accession,fastq_ftp,read_count,base_count&limit=5",

    # round 2: directory listings and bulk files
    "fb_cgi_data": "https://fit.genomics.lbl.gov/cgi_data/",
    "fb_feba_db": "https://fit.genomics.lbl.gov/cgi_data/feba.db",
    "fb_fitness_tab": "https://fit.genomics.lbl.gov/cgi_data/fit_genes.tab",
    "pombase_latest_genome": "https://www.pombase.org/latest_release/genome_sequence_and_features/",
    "pombase_latest_feature_seq": "https://www.pombase.org/latest_release/genome_sequence_and_features/feature_sequences/",
    "paxdb_latest_datasets": "https://pax-db.org/downloads/latest/datasets/",
    "paxdb_latest_seqs": "https://pax-db.org/downloads/latest/paxdb-protein-sequences-v6.1/",
    "deg_download_links": "http://origin.tubic.org/deg/public/index.php/download",
    "figshare_feba": "https://api.figshare.com/v2/articles/search?search_for=fitness%20browser%20Price",

    # Fitness Browser (genome-wide transposon knockout fitness, 40+ bacteria)
    "fb_orgs": "https://fit.genomics.lbl.gov/cgi-bin/orgAll.cgi",
    "fb_aaseqs": "https://fit.genomics.lbl.gov/cgi_data/aaseqs",
    "fb_fit_keio": "https://fit.genomics.lbl.gov/cgi-bin/createFitData.cgi?orgId=Keio",
    "fb_exp_keio": "https://fit.genomics.lbl.gov/cgi-bin/createExpData.cgi?orgId=Keio",
    "fb_genes_keio": "https://fit.genomics.lbl.gov/cgi-bin/orgGenes.cgi?orgId=Keio",
    # PaxDb (integrated measured protein abundance) and STRING sequences
    "paxdb_latest": "https://pax-db.org/downloads/latest/",
    "paxdb_5": "https://pax-db.org/downloads/5.0/",
    "paxdb_5_datasets": "https://pax-db.org/downloads/5.0/datasets/",
    "string_seq_ecoli": "https://stringdb-downloads.org/download/protein.sequences.v12.0/511145.protein.sequences.v12.0.fa.gz",
    # Yeast and fission yeast deletion phenotypes
    "sgd_phenotype": "https://downloads.yeastgenome.org/curation/literature/phenotype_data.tab",
    "sgd_orf_trans": "https://downloads.yeastgenome.org/sequence/S288C_reference/orf_protein/orf_trans_all.fasta.gz",
    "pombase_root": "https://www.pombase.org/data/",
    "pombase_latest": "https://www.pombase.org/latest_release/",
    "pombase_phaf": "https://www.pombase.org/latest_release/phenotypes_and_genotypes/pombase_single_locus_haploid_phenotype_annotation.phaf.tsv",
    "pombase_pep": "https://www.pombase.org/latest_release/genome_sequence_and_features/feature_sequences/peptide.fa.gz",
    # Databases of essential genes
    "deg": "http://origin.tubic.org/deg/public/index.php/download",
    "ogee": "https://v3.ogee.info/#/downloads",
    # WormBase RNAi, PlasmoGEM
    "wormbase_ftp": "https://downloads.wormbase.org/releases/current-production-release/ONTOLOGY/",
    "plasmogem": "https://plasmogem.umu.se/pbgem/",
}


def probe(url):
    req = urllib.request.Request(url, headers={"User-Agent": "organelle-evo/1.0 (research; github.com/minjae-05-28/-ai)"})
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            raw = r.read(400_000)
            status = r.status
    except Exception as e:  # noqa: BLE001
        return {"ok": False, "error": str(e)[:300]}
    if raw[:2] == b"\x1f\x8b":
        try:
            raw = gzip.decompress(raw)
        except Exception:  # noqa: BLE001  (truncated gzip)
            import zlib

            raw = zlib.decompressobj(16 + zlib.MAX_WBITS).decompress(raw)
    text = raw.decode("utf-8", "replace")
    import re

    links = sorted(set(re.findall(r'href="([^"?#][^"]*)"', text)))[:3000]
    return {"ok": True, "status": status, "bytes_read": len(raw), "head": text[:3000], "links": links}


def main():
    out = {k: {"url": u, **probe(u)} for k, u in CANDIDATES.items()}
    for k, v in out.items():
        print(f"{k:18s} {'OK ' + str(v.get('status')) if v['ok'] else 'FAIL'} {v.get('bytes_read', '')} {v.get('error', '')[:120]}")
        if v["ok"]:
            print("    " + v["head"][:400].replace("\n", "\n    "))
    p = Path("results/external")
    p.mkdir(parents=True, exist_ok=True)
    (p / "probe.json").write_text(json.dumps(out, indent=1))


if __name__ == "__main__":
    main()
