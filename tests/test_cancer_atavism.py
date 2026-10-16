import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import cancer_atavism as ca  # noqa: E402


def test_delta_per_patient_removes_expression_level_effect():
    # UC genes sit in high deciles where every gene rises by 1; within each decile UC and MC move the same
    decile = np.array([0, 0, 1, 1])
    uc = np.array([True, False, True, False])
    lfc = np.array([[0.0, 0.0, 1.0, 1.0], [0.0, 0.0, 1.0, 1.0]])
    assert np.allclose(ca.delta_per_patient(lfc, uc, ~uc, decile), 0.0)
    lfc2 = np.array([[1.0, 0.0, 1.0, 0.0]])
    assert np.allclose(ca.delta_per_patient(lfc2, uc, ~uc, decile), 1.0)


def test_ci_verdicts():
    rng = np.random.default_rng(0)
    assert ca.ci(np.full(20, 0.5) + rng.normal(0, 0.01, 20), rng)["verdict"] == "양성"
    assert ca.ci(np.full(20, -0.5), rng)["verdict"] == "음성"
    assert ca.ci(rng.normal(0, 1, 20) - rng.normal(0, 1, 20).mean(), rng)["verdict"] == "무승부"


def test_overall_two_thirds_rule():
    mk = lambda v: {"primary": {"verdict": v}}
    res = {"A": mk("양성"), "B": mk("양성"), "C": mk("무승부")}
    assert ca.overall(res, "primary")["call"] == "지지"
    res["D"] = mk("음성")
    assert ca.overall(res, "primary")["call"] == "판단 보류"


def test_qc_drops_swapped_pairs():
    import tcga_fetch as tf
    rng = np.random.default_rng(0)
    base, shift = rng.normal(5, 2, 2000), rng.normal(0, 1.5, 2000)
    N = base + rng.normal(0, .3, (30, 2000))
    T = base + shift + rng.normal(0, .3, (30, 2000))
    N[3] = T[3] + rng.normal(0, .1, 2000)
    T[7] = N[7] + rng.normal(0, .1, 2000)
    keep, _, counts = tf.qc(T, N)
    assert not keep[3] and not keep[7] and counts["swapped_or_low_purity"] == 2


def test_intercept_recovers_effect_beyond_proliferation():
    import cancer_proliferation as cp
    s = np.linspace(-1, 2, 40)
    d = 0.1 + 0.3 * s
    a, b = cp.intercept(d, s)
    assert abs(a - 0.1) < 1e-9 and abs(b - 0.3) < 1e-9
