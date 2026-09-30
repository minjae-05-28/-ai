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


def test_birth_death_matches_simulation():
    import numpy as np
    import torch

    from organelle_evo.eukaryotes.birthdeath import simulate, transition_log_prob

    for n, log_lam, log_mu in [(1, -0.5, 0.2), (3, 0.3, -0.2), (2, 0.0, 0.0)]:
        m = torch.arange(0, 31)
        p = transition_log_prob(torch.tensor(n), m, torch.tensor(float(log_lam), dtype=torch.float64),
                                torch.tensor(float(log_mu), dtype=torch.float64)).exp().numpy()
        sim = simulate(np.full(50000, n), log_lam, log_mu, -50.0, n_steps=500, rng=np.random.default_rng(0))
        emp = np.bincount(np.minimum(sim, 30), minlength=31) / len(sim)
        assert abs(p.sum() - 1) < 1e-3
        assert np.abs(emp[:10] - p[:10]).max() < 0.01


def test_single_copy_no_birth_reduces_to_retention_model():
    import torch

    from organelle_evo.eukaryotes.birthdeath import transition_log_prob

    log_mu = torch.tensor(0.3, dtype=torch.float64)
    p0 = transition_log_prob(torch.tensor(1), torch.tensor(0), torch.tensor(-30.0, dtype=torch.float64), log_mu)
    assert abs(float(p0.exp()) - float(-torch.expm1(-log_mu.exp()))) < 1e-6


def test_fit_bd_recovers_lifestyle_specific_laws():
    import numpy as np
    import torch

    from organelle_evo.eukaryotes.birthdeath import simulate
    from organelle_evo.eukaryotes.model import fit_bd

    torch.set_num_threads(1)
    rng = np.random.default_rng(0)
    F = 800
    x = np.stack([rng.normal(size=F), (rng.random(F) < 0.15).astype(float)], 1)
    w_mu = np.array([[0.0, -1.0], [0.8, -1.5]])  # parasites lose feature-0 families faster
    pairs = []
    for p in range(6):
        s = p % 2
        n0 = rng.geometric(0.4, size=F) * (rng.random(F) < 0.8)
        m = simulate(n0, -1.2 + np.zeros(F), -1.0 + x @ w_mu[s], -3 + np.zeros(F), n_steps=200, rng=rng)
        pairs.append((n0, m, s))
    law = fit_bd(x, pairs, ("free", "parasite"), epochs=300)
    np.testing.assert_allclose(law.w_mu, w_mu, atol=0.35)


def test_pfam_class():
    from organelle_evo.eukaryotes.model import pfam_class

    assert pfam_class("Ribosomal_L2") == "translation"
    assert pfam_class("tRNA-synt_1") == "translation"
    assert pfam_class("ATP-synt_ab") == "atp_synthase"
    assert pfam_class("Oxidored_q1") == "redox_core"
    assert pfam_class("COX1") == "redox_core"
    assert pfam_class("RNA_pol_Rpb1_1") == "transcription"
    assert pfam_class("SecY") == "protein_targeting"
    assert pfam_class("Pkinase", "Protein kinase domain") == "other"


def test_wagner_parsimony_ancestor():
    import numpy as np

    from organelle_evo.eukaryotes.ancestral import leaves, prune, wagner_ancestor

    tree = ((("P", "T"), "C"), ("Te", "Ich"))
    c = {"P": np.array([0, 5, 1]), "T": np.array([0, 4, 1]), "C": np.array([1, 4, 0]),
         "Te": np.array([3, 6, 0]), "Ich": np.array([2, 5, 0])}
    anc = wagner_ancestor(tree, c)
    assert anc[2] == 0  # only the P+T clade has it: gained there, not at the root
    assert 4 <= anc[1] <= 5
    assert leaves(prune(tree, {"P"})) == ["T", "C", "Te", "Ich"]
