"""The Cox model of pre-registration 28 is written here, so it is checked against simulated data
whose answer is known."""

import sys
from pathlib import Path

import numpy as np
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import cancer_survival as cs  # noqa: E402


def simulate(beta, n=4000, seed=0, censor=0.0):
    """Exponential survival with hazard exp(X beta); optional uniform censoring."""
    rng = np.random.default_rng(seed)
    X = rng.normal(size=(n, len(beta)))
    t = rng.exponential(1.0) if False else rng.exponential(size=n) / np.exp(X @ beta)
    event = np.ones(n, int)
    if censor:
        c = rng.uniform(0, np.quantile(t, 1 - censor) * 3, size=n)
        event = (t <= c).astype(int)
        t = np.minimum(t, c)
    return X, t, event


def test_cox_recovers_a_known_coefficient():
    X, t, e = simulate(np.array([0.7]))
    b = cs.cox(X, t, e)
    assert b is not None
    assert abs(b[0] - 0.7) < 0.1


def test_cox_recovers_two_coefficients_with_censoring():
    X, t, e = simulate(np.array([0.5, -0.3]), censor=0.4)
    b = cs.cox(X, t, e)
    assert b is not None
    assert abs(b[0] - 0.5) < 0.12 and abs(b[1] + 0.3) < 0.12


def test_cox_finds_no_effect_when_there_is_none():
    X, t, e = simulate(np.array([0.0]), n=3000, seed=1)
    b = cs.cox(X, t, e)
    assert abs(b[0]) < 0.08


def test_cox_handles_tied_times():
    """Times rounded to whole days produce many ties; Breslow must still recover the coefficient."""
    X, t, e = simulate(np.array([0.6]), n=4000, seed=2)
    t = np.round(t * 20) + 1                      # heavy ties
    b = cs.cox(X, t, e)
    assert b is not None
    assert abs(b[0] - 0.6) < 0.15


def test_cox_returns_none_without_deaths():
    X, t, e = simulate(np.array([0.5]), n=200)
    assert cs.cox(X, t, np.zeros_like(e)) is None


def test_concordance_direction():
    """A score that predicts early death perfectly has concordance 1, the reverse 0."""
    t = np.array([1.0, 2, 3, 4, 5])
    e = np.ones(5, int)
    assert cs.concordance(-t, t, e) == pytest.approx(1.0)
    assert cs.concordance(t, t, e) == pytest.approx(0.0)
    assert cs.concordance(np.zeros(5), t, e) == pytest.approx(0.5)


def test_concordance_matches_the_simulated_effect():
    X, t, e = simulate(np.array([1.0]), n=600, seed=3)
    assert cs.concordance(X[:, 0], t, e) > 0.65


def test_fit_hr_interval_covers_the_truth_and_calls_it_positive():
    X, t, e = simulate(np.array([0.7]), n=1500, seed=4)
    r = cs.fit_hr(X, t, e, boot=200)
    assert r["lo"] < np.exp(0.7) < r["hi"]
    assert r["verdict"] == "양성"


def test_fit_hr_rarely_calls_a_verdict_on_no_effect():
    """One unlucky seed is not a bug: what matters is how often the interval misses zero. Measured over
    40 null runs it should stay near 5% (seed 5 alone does call a verdict)."""
    wrong = 0
    for s in range(40):
        X, t, e = simulate(np.array([0.0]), n=500, seed=s, censor=0.6)
        if cs.fit_hr(X, t, e, boot=300)["verdict"] != "무승부":
            wrong += 1
    assert wrong <= 6                             # 15% of 40; the measured rate over 200 runs was 5.0%


def test_design_drops_missing_covariates_and_keeps_tilt_first():
    D = {"delta": np.array([1.0, 2, 3, 4]), "age": np.array([50.0, np.nan, 70, 80]),
         "time": np.array([5.0, 6, 7, 8]), "event": np.array([1, 1, 0, 1])}
    X, t, e, n = cs.design(D, ["delta", "age"])
    assert n == 3
    assert list(X[:, 0]) == [1.0, 3.0, 4.0]       # tilt column untouched
    assert abs(X[:, 1].mean()) < 1e-9             # adjustment centred
