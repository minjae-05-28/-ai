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
