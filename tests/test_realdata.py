import json
from pathlib import Path

import numpy as np
import pytest

from organelle_evo.realdata import ncbi
from organelle_evo.realdata.analysis import forecast_lineages, leave_one_lineage_out, universality_test
from organelle_evo.realdata.dataset import GenomeRecord, build_dataset, read_genbank
from organelle_evo.realdata.genes import functional_class, normalize_gene_name, tm_helices
from organelle_evo.rules import fit_retention, offset_for_count

FIXTURE = Path(__file__).parent / "data" / "NC_000932.gb"  # Arabidopsis thaliana chloroplast


@pytest.fixture(scope="module")
def arabidopsis_cp():
    return read_genbank(FIXTURE)


@pytest.mark.parametrize(
    "raw, canonical",
    [("ND1", "nad1"), ("nd4L", "nad4l"), ("COI", "cox1"), ("CYTB", "cob"), ("cob", "cob"),
     ("rpoC1", "rpoc1"), ("nad5-1", "nad5"), ("psbA", "psba"), ("orf25", None), ("", None),
     ("ArthCp001", None)],
)  # fmt: skip
def test_normalize_gene_name(raw, canonical):
    assert normalize_gene_name(raw) == canonical


def test_functional_classes():
    assert functional_class("psba") == "redox_core"
    assert functional_class("nad4l") == "redox_core"
    assert functional_class("rps12") == "translation"
    assert functional_class("alas") == "translation"  # alanyl-tRNA synthetase
    assert functional_class("rpoc1") == "transcription"
    assert functional_class("atp6") == "atp_synthase"
    assert functional_class("thra") == "other"


def test_read_real_chloroplast(arabidopsis_cp):
    assert arabidopsis_cp.organism == "Arabidopsis thaliana"
    assert len(arabidopsis_cp.proteins) == 78
    assert {"psba", "rbcl", "ndhb", "rpoc2", "ycf1"} <= set(arabidopsis_cp.proteins)
    # Membrane proteins look membrane-bound, soluble ones don't.
    assert tm_helices(arabidopsis_cp.proteins["ndhb"]) >= 8
    assert tm_helices(arabidopsis_cp.proteins["rbcl"]) == 0


def _derived_lineages(base: GenomeRecord, weights, n=12, seed=0):
    """Reduce the real gene set with a known law (test-only data)."""
    ds = build_dataset("plastid", [base], min_lineages=1)
    rng = np.random.default_rng(seed)
    records = []
    for i in range(n):
        p_keep = np.exp(-np.exp(rng.uniform(-2.5, 0.5) + ds.features @ weights))
        keep = rng.random(len(ds.genes)) < p_keep
        prots = {g: base.proteins[g] for g, k in zip(ds.genes, keep) if k}
        records.append(GenomeRecord(f"lineage_{i}", f"X{i}", prots))
    return ds, records


def test_build_dataset_and_learn_on_real_features(arabidopsis_cp):
    w = np.array([0.0, -0.8, 0.0, -1.5, -0.5, 0.0, 0.0, 0.0])  # TM + redox-core genes stay
    universe, records = _derived_lineages(arabidopsis_cp, w, n=30)
    ds = build_dataset("plastid", [arabidopsis_cp, *records], min_lineages=1)
    assert ds.genes == universe.genes
    assert ds.present[0].all()
    law = fit_retention([(ds.features, ds.present[1:])])
    assert law.weights[0][3] < -0.7  # redox_core retained
    assert law.weights[0][1] < -0.3  # TM helices retained


def test_ancestor_proxy_defines_universe(arabidopsis_cp):
    small = GenomeRecord("reduced", "R", {g: p for g, p in list(arabidopsis_cp.proteins.items())[:20]})
    ds = build_dataset("x", [small], ancestor=arabidopsis_cp)
    assert len(ds.genes) == 78 and ds.present.sum() == 20


def test_offset_for_count_matches_expected_size():
    base = np.random.default_rng(0).normal(size=200)
    a = offset_for_count(base, 37)
    assert abs(np.exp(-np.exp(a + base)).sum() - 37) < 0.01


def test_lolo_forecast_and_universality(arabidopsis_cp):
    w = np.array([0.0, -0.8, 0.0, -1.5, -0.5, 0.0, 0.0, 0.0])
    _, recs_a = _derived_lineages(arabidopsis_cp, w, n=10, seed=1)
    _, recs_b = _derived_lineages(arabidopsis_cp, -w, n=10, seed=2)  # opposite law
    ds_a = build_dataset("a", recs_a, ancestor=arabidopsis_cp)
    ds_b = build_dataset("b", recs_b, ancestor=arabidopsis_cp)

    lolo = leave_one_lineage_out(ds_a, epochs=400)
    assert np.nanmean(lolo.auroc_law) > 0.6

    law = fit_retention([(ds_a.features, ds_a.present)], epochs=400)
    fcs = forecast_lineages(ds_a, law, law.lineage_offsets[0], n_samples=50)
    for fc, present in zip(fcs, ds_a.present):
        assert fc.count_quantiles[2] <= present.sum()  # genes never come back
        assert all(0 <= p <= 1 for _, p in fc.at_risk)

    uni = universality_test([ds_a, ds_b], epochs=400)
    assert uni["delta_aic"] > 10  # different laws are detected


def test_ncbi_fetch_with_mocked_eutils(tmp_path, monkeypatch):
    calls = []

    def fake_get(endpoint, **params):
        calls.append(endpoint)
        if endpoint == "esearch.fcgi":
            return json.dumps({"esearchresult": {"idlist": ["1", "2"]}}).encode()
        if endpoint == "esummary.fcgi":
            return json.dumps({"result": {"uids": ["1", "2"],
                "1": {"caption": "AB000001", "accessionversion": "AB000001.1", "title": "partial", "slen": 900},
                "2": {"caption": "NC_000932", "accessionversion": "NC_000932.1",
                      "title": "Arabidopsis thaliana chloroplast, complete genome", "slen": 154478}}}).encode()
        assert params["id"] == "NC_000932.1"
        return FIXTURE.read_bytes()

    monkeypatch.setattr(ncbi, "_get", fake_get)
    path = ncbi.fetch_species("Arabidopsis thaliana", "{org}", tmp_path)
    assert path.name == "Arabidopsis_thaliana.gb"
    assert len(read_genbank(path).proteins) == 78
    ncbi.fetch_species("Arabidopsis thaliana", "{org}", tmp_path)  # cached
    assert calls == ["esearch.fcgi", "esummary.fcgi", "efetch.fcgi"]


@pytest.mark.parametrize(
    "product, organelle, symbol",
    [("NADH dehydrogenase subunit 4L", "mitochondrion", "nad4l"),
     ("NADH dehydrogenase subunit 2", "plastid:chloroplast", None),  # that's ndhB
     ("cytochrome c oxidase subunit III", "mitochondrion", "cox3"),
     ("apocytochrome b", "mitochondrion", "cob"),
     ("ATPase subunit 9", "mitochondrion", "atp9"),
     ("ribosomal protein S12", "plastid:apicoplast", "rps12"),
     ("RNA polymerase beta' chain", "plastid:apicoplast", "rpoc1"),
     ("RNA polymerase beta'' subunit", "plastid:chloroplast", "rpoc2"),
     ("apicoplast ribosomal protein L14", "plastid:apicoplast", "rpl14"),
     ("elongation factor Tu, putative", "plastid:apicoplast", "tufa"),
     ("hypothetical protein", "mitochondrion", None)],
)  # fmt: skip
def test_symbol_from_product(product, organelle, symbol):
    from organelle_evo.realdata.genes import symbol_from_product

    assert symbol_from_product(product, organelle) == symbol


def test_homology_recovers_stripped_gene_names(arabidopsis_cp):
    from organelle_evo.realdata.homology import name_by_homology, reference_from_records

    # The same genome with every annotation name removed must be renamed correctly.
    anon = GenomeRecord("anon", "A", {}, dict(arabidopsis_cp.cds), {})
    (named,), added = name_by_homology([anon], reference_from_records([arabidopsis_cp]))
    assert added["anon"] >= 70
    wrong = [cid for cid, sym in named.cds_symbol.items() if arabidopsis_cp.cds_symbol.get(cid) != sym]
    assert not wrong
