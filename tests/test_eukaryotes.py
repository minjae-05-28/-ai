import io
import json
import zipfile

import pyhmmer
import pytest

from organelle_evo.eukaryotes import proteomes
from organelle_evo.eukaryotes.catalog import PAIRS, SPECIES
from organelle_evo.eukaryotes.pfam import family_profile
from organelle_evo.laws import load_law
from organelle_evo.realdata.dataset import read_genbank

from .test_realdata import FIXTURE


def test_catalog_pairs_use_known_species():
    for anc, desc in PAIRS:
        assert anc in SPECIES and desc in SPECIES
        assert SPECIES[anc][1] == "free_living"


def _report(name, acc, refseq=True, level="Chromosome", genes=100, annotated=True):
    r = {
        "accession": acc,
        "organism": {"organism_name": name},
        "source_database": "SOURCE_DATABASE_REFSEQ" if refseq else "SOURCE_DATABASE_GENBANK",
        "assembly_info": {"assembly_level": level},
    }
    if annotated:
        r["annotation_info"] = {"stats": {"gene_counts": {"protein_coding": genes}}}
    return r


def test_choose_assembly_prefers_species_refseq_annotated():
    reports = [
        _report("Entamoeba dispar", "GCF_1"),
        _report("Entamoeba histolytica HM-1:IMSS", "GCA_2", refseq=False, level="Scaffold"),
        _report("Entamoeba histolytica HM-1:IMSS", "GCF_3", level="Scaffold"),
        _report("Entamoeba histolytica", "GCF_4", annotated=False, level="Complete Genome"),
    ]
    assert proteomes.choose_assembly(reports, "Entamoeba histolytica")["accession"] == "GCF_3"
    assert proteomes.choose_assembly([reports[3]], "Entamoeba histolytica") is None


GFF = """##gff-version 3
chr1\tRefSeq\tgene\t1\t900\t.\t+\t.\tID=gene-A;Name=A
chr1\tRefSeq\tCDS\t1\t300\t.\t+\t0\tID=cds-XP_1;Parent=rna-1;gene=A;protein_id=XP_1
chr1\tRefSeq\tCDS\t1\t600\t.\t+\t0\tID=cds-XP_2;Parent=rna-2;gene=A;protein_id=XP_2
chr1\tRefSeq\tCDS\t700\t900\t.\t+\t0\tID=cds-XP_3;Parent=rna-3;locus_tag=B_001;protein_id=XP_3
"""
FAA = ">XP_1 short isoform\nMKV\n>XP_2 long isoform\nMKVLLA\nGG\n>XP_3 other\nMAAA\n>XP_9 unmapped\nMW\n"


def test_longest_isoform_per_gene():
    gene_of = proteomes.protein_to_gene(GFF)
    assert gene_of == {"XP_1": "A", "XP_2": "A", "XP_3": "B_001"}
    best = proteomes.longest_per_gene(proteomes.read_fasta(FAA), gene_of)
    assert best == {"A": "MKVLLAGG", "B_001": "MAAA", "XP_9": "MW"}


def test_fetch_proteome_with_mocked_api(monkeypatch):
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w") as z:
        z.writestr("ncbi_dataset/data/GCF_3/protein.faa", FAA)
        z.writestr("ncbi_dataset/data/GCF_3/genomic.gff", GFF)

    def fake_get(url):
        if "dataset_report" in url:
            assert "Entamoeba%20histolytica" in url
            return json.dumps({"reports": [_report("Entamoeba histolytica", "GCF_3")]}).encode()
        assert "GCF_3/download" in url and "PROT_FASTA" in url
        return buf.getvalue()

    monkeypatch.setattr(proteomes, "_get", fake_get)
    report, prots = proteomes.fetch_proteome("Entamoeba histolytica")
    assert report["accession"] == "GCF_3" and len(prots) == 3


def test_family_profile_counts_genes_with_domain():
    rec = read_genbank(FIXTURE)
    alpha = pyhmmer.easel.Alphabet.amino()
    builder, bg = pyhmmer.plan7.Builder(alpha), pyhmmer.plan7.Background(alpha)
    seq = pyhmmer.easel.TextSequence(name=b"psba", sequence=rec.proteins["psba"]).digitize(alpha)
    hmm, _, _ = builder.build(seq, bg)
    prof = family_profile(rec.proteins, [hmm], cutoffs=None)
    n_genes, n_domains, sum_gravy, sum_tm, sum_len = prof["psba"]
    assert n_genes == 2  # psbA and its paralogue psbD
    assert n_domains >= 2 and sum_tm > 0 and sum_len > 300


def test_endosymbiosis_law_registry():
    law = load_law("endosymbiosis_v1")
    assert set(law.weights) == {"mitochondrion", "plastid", "insect_endosymbiont"}
    assert "Not valid for free-living" in law.scope
    # The headline laws: energy and translation genes are kept everywhere.
    for ctx in law.weights:
        idx = [law.feature_names.index(f) for f in ("redox_core", "atp_synthase", "translation")]
        assert (law.weights[ctx][idx] < 0).all() and law.significant(ctx)[idx].all()


@pytest.mark.parametrize("name", ["Dictyostelium discoideum"])
def test_slug(name):
    from organelle_evo.eukaryotes.catalog import slug

    assert slug(name) == "Dictyostelium_discoideum"
