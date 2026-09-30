import numpy as np

from organelle_evo.ancestor import make_ancestor
from organelle_evo.inference import EvolutionInferrer
from organelle_evo.predict import auroc, forecast
from organelle_evo.rules import fit_rules
from organelle_evo.simulator import ORGANELLE, PRIOR_HIGH, PRIOR_LOW, TRUE_RULES, sample_prior, simulate


def test_rule_learner_recovers_true_laws():
    g = make_ancestor(0)
    rng = np.random.default_rng(0)
    params = sample_prior(30, rng)
    params[:, 2] = 0.0  # model is exactly specified without pathway coupling
    states = simulate(g, TRUE_RULES, params, rng=rng).states
    fitted = fit_rules(g.features, states)
    np.testing.assert_allclose(fitted.transfer_weights, TRUE_RULES.transfer_weights, atol=0.35)
    np.testing.assert_allclose(fitted.loss_weights, TRUE_RULES.loss_weights, atol=0.35)
    # Lineage offsets absorb the rule biases (extreme lineages carry little signal).
    offset = fitted.lineage_log_transfer - params[:, 0]
    assert abs(np.median(offset) - TRUE_RULES.transfer_bias) < 0.15
    assert np.corrcoef(fitted.lineage_log_transfer, params[:, 0])[0, 1] > 0.98


def test_inferrer_learns_something():
    g = make_ancestor(0)
    inf = EvolutionInferrer(g, TRUE_RULES, PRIOR_LOW, PRIOR_HIGH)
    history = inf.train(n_sims=1500, epochs=6)
    assert history[-1] < history[0]
    params, states = inf.simulate_dataset(200, np.random.default_rng(5))
    post = inf.infer(states)
    corr = np.corrcoef(post.mean[:, 0], params[:, 0])[0, 1]
    assert corr > 0.8


def test_forecast_probabilities_and_absorbing_states():
    g = make_ancestor(0)
    rng = np.random.default_rng(3)
    now = simulate(g, TRUE_RULES, np.array([[1.0, 1.0, 1.0]]), rng=rng).states[0]
    fc = forecast(g, TRUE_RULES, now, np.tile([1.0, 1.0, 1.0], (64, 1)), 0.5, rng=rng)
    np.testing.assert_allclose(fc.state_probs.sum(1), 1.0)
    gone = now != ORGANELLE
    assert (fc.p_leaves_organelle[gone] == 1.0).all()


def test_auroc():
    assert auroc([0.1, 0.2, 0.8, 0.9], [0, 0, 1, 1]) == 1.0
    assert auroc([0.9, 0.8, 0.2, 0.1], [0, 0, 1, 1]) == 0.0
    assert auroc([0.5, 0.5, 0.5, 0.5], [0, 1, 0, 1]) == 0.5
