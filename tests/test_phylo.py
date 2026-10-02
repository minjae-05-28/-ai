import numpy as np

from organelle_evo.phylo import pgls, rank_gls, taxonomy_cov


def test_taxonomy_cov_shares_ranks():
    tax = {"a": {"domain": "B", "phylum": "P1", "genus": "G1"}, "b": {"domain": "B", "phylum": "P1", "genus": "G1"},
           "c": {"domain": "B", "phylum": "P2", "genus": "G2"}}
    for t in tax.values():
        t.update(kingdom=None)
    V = taxonomy_cov(["a", "b", "c"], {k: {**v, "kingdom": "K", "class": v["phylum"] + "c", "order": v["phylum"] + "o",
                                             "family": v["genus"] + "f"} for k, v in tax.items()})
    assert V[0, 0] == 1 and V[0, 1] > V[0, 2] > 0


def test_pgls_discounts_pseudoreplicated_clades():
    # x and y are unrelated, but each is shared within clades (8 clades of 6 species):
    # ordinary least squares counts 48 points, the phylogenetic fit about 8.
    rng = np.random.default_rng(3)
    clade = np.repeat(np.arange(8), 6)
    tax = {f"s{i}": {"domain": "B", "kingdom": "K", "phylum": f"P{c}", "class": f"C{c}", "order": f"O{c}",
                     "family": f"F{c}", "genus": f"G{c}"} for i, c in enumerate(clade)}
    V = taxonomy_cov(list(tax), tax)
    trials = []
    for _ in range(40):
        cx, cy = rng.normal(size=8), rng.normal(size=8)
        x = cx[clade] + 0.1 * rng.normal(size=48)
        y = cy[clade] + 0.1 * rng.normal(size=48)
        X = np.c_[np.ones(48), x]
        trials.append((pgls(X, y, V, lam=0.0).p[1] < 0.05, rank_gls(X, y, list(tax), tax).p[1] < 0.05))
    false_ols = np.mean([t[0] for t in trials])
    false_pgls = np.mean([t[1] for t in trials])
    assert false_ols > 0.3 and false_pgls < 0.15


def test_tree_cov_shares_history_by_clade():
    from organelle_evo.phylo import tree_cov

    nwk = "((A:1,B:1):2,(C:1,D:1):2);"
    keep, V = tree_cov(["A", "B", "C", "D", "E"], nwk)
    assert keep == ["A", "B", "C", "D"]
    assert np.allclose(np.diag(V), 1)
    assert V[0, 1] > 0.5 and V[0, 2] == 0 and np.allclose(V, V.T)
