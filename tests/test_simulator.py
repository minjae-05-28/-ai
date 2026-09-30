import numpy as np

from organelle_evo.ancestor import FEATURES, make_ancestor
from organelle_evo.simulator import LOST, NUCLEUS, ORGANELLE, TRUE_RULES, Rules, simulate


def test_ancestor_shapes_and_ranges():
    g = make_ancestor(0)
    assert g.features.shape == (g.n_genes, len(FEATURES))
    assert ((g.features > 0) & (g.features < 1)).all()
    assert len(set(g.gene_names)) == g.n_genes


def test_transitions_are_irreversible():
    g = make_ancestor(0)
    params = np.array([[1.0, 1.0, 1.0]] * 8)
    res = simulate(g, TRUE_RULES, params, snapshot_steps=(30, 60), rng=np.random.default_rng(0))
    early, late = res.snapshots[30], res.snapshots[60]
    assert (late[early == NUCLEUS] == NUCLEUS).all()
    assert (late[early == LOST] == LOST).all()
    assert (np.diff(res.counts[:, :, ORGANELLE], axis=1) <= 0).all()
    assert (res.counts.sum(-1) == g.n_genes).all()


def test_matches_closed_form_without_coupling():
    g = make_ancestor(0)
    rules = Rules(0.0, (0.0,) * 4, 0.0, (0.0,) * 4)  # every gene: kT = kL = e^param
    params = np.tile([np.log(0.4), np.log(0.2), 0.0], (400, 1))
    states = simulate(g, rules, params, rng=np.random.default_rng(1)).states
    k = 0.6
    expected = [np.exp(-k), 0.4 / k * (1 - np.exp(-k)), 0.2 / k * (1 - np.exp(-k))]
    observed = [(states == s).mean() for s in (ORGANELLE, NUCLEUS, LOST)]
    np.testing.assert_allclose(observed, expected, atol=0.01)


def test_coupling_accelerates_loss():
    g = make_ancestor(0)
    rng = np.random.default_rng(2)
    base = simulate(g, TRUE_RULES, np.tile([0.5, 1.5, 0.0], (50, 1)), rng=rng).states
    coupled = simulate(g, TRUE_RULES, np.tile([0.5, 1.5, 3.0], (50, 1)), rng=rng).states
    assert (coupled == LOST).mean() > (base == LOST).mean()
