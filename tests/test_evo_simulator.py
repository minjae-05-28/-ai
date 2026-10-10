import sys
from pathlib import Path

import numpy as np
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

from evo_simulator import Simulator  # noqa: E402
from mito_model_search import branch_probs  # noqa: E402


class Toy(Simulator):
    """The simulator's machinery on a hand-made law bank (no data files needed)."""
    def __init__(self):
        self.fams = ["A", "B", "C"]
        self.col = {f: j for j, f in enumerate(self.fams)}
        self.grid = np.array([[0.3, 0.03], [3.0, 0.3]])
        self.W = np.array([[1.0, 0.0, 0.5], [0.0, 1.0, 0.5]])
        self.default = self.W.mean(1)


def test_exact_probability_matches_two_state_chain():
    s = Toy()
    p = s.probabilities({"A"}, ["A"], [(set(), 0.7)], {})
    P00, P01, P10, P11 = branch_probs(0.7, 0.03, 0.3)
    assert p[0] == pytest.approx(P11)


def test_two_segments_equal_one_long_segment_without_environment():
    s = Toy()
    one = s.probabilities({"A", "C"}, ["A", "B", "C"], [(set(), 1.0)], {})
    two = s.probabilities({"A", "C"}, ["A", "B", "C"], [(set(), 0.4), (set(), 0.6)], {})
    assert np.allclose(one, two)


def test_sampling_agrees_with_exact_probabilities():
    s = Toy()
    laws = {"x": {"loss": {"A": 5.0}, "gain": {}, "loss_default": 1.0, "gain_default": 1.0}}
    sched = [(set(), 0.3), ({"x"}, 0.5)]
    exact = s.probabilities({"A", "B"}, ["A", "B", "C"], sched, laws)
    sampled = s.sample({"A", "B"}, ["A", "B", "C"], sched, laws, reps=20000, seed=1).mean(0)
    assert np.allclose(exact, sampled, atol=0.015)


def test_environment_loss_multiplier_lowers_retention():
    s = Toy()
    laws = {"x": {"loss": {"A": 5.0}, "gain": {}, "loss_default": 1.0, "gain_default": 1.0}}
    base = s.probabilities({"A"}, ["A"], [(set(), 0.5)], {})
    env = s.probabilities({"A"}, ["A"], [({"x"}, 0.5)], laws)
    assert env[0] < base[0]
