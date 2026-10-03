"""The genome-quality correction: the completeness score and the dropout term in the likelihood."""

import sys
from pathlib import Path

import numpy as np
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))


def tiny_tree():
    """Four tips on a star, one of which will be the incomplete one."""
    parent = np.array([-1, 0, 0, 0, 0])
    length = np.array([1e-6, 0.3, 0.3, 0.3, 0.3])
    children = [[1, 2, 3, 4], [], [], [], []]
    order = [1, 2, 3, 4, 0]
    return {"parent": parent, "length": length, "children": children, "order": order,
            "tips": [1, 2, 3, 4], "reduced_branch": np.zeros(5, dtype=bool),
            "busco": np.full(5, np.nan), "mag": np.zeros(5, dtype=bool)}


def test_too_few_proteomes_yield_no_markers_rather_than_a_bad_score():
    """Below a handful of proteomes there is nothing to define completeness against, and the
    function must say so instead of inventing a score from two genomes."""
    from genome_quality import markers_for

    assert markers_for({"a": {"x", "y"}, "b": {"x"}}) == []


def test_completeness_score_ranks_incomplete_proteomes_last():
    from genome_quality import completeness_for

    full = {f"g{i}" for i in range(100)}
    # markers_for needs a handful of proteomes to define "what a complete one looks like"
    profiles = {f"complete{i}": set(full) for i in range(8)}
    profiles["half"] = set(list(full)[:50])
    profiles["quarter"] = set(list(full)[:25])
    score, markers = completeness_for(profiles)
    assert markers, "a set where most proteomes share families must yield markers"
    assert score["complete0"] == pytest.approx(1.0)
    assert score["half"] < score["complete0"] and score["quarter"] < score["half"]


def test_tip_message_is_the_plain_indicator_without_completeness():
    from mito_model_search import tip_message

    d = tiny_tree()
    X = np.array([[0, 0], [1, 0], [1, 1], [0, 1], [1, 0]], dtype=bool)
    m0, m1 = tip_message(d, X, 1)
    assert np.allclose(m0, 1 - X[1])
    assert np.allclose(m1, X[1])
    d["completeness"] = np.ones(5)
    assert np.allclose(tip_message(d, X, 1)[1], X[1])


def test_dropout_raises_the_ancestor_for_a_family_only_missing_from_an_incomplete_tip():
    """A family in every complete tip but absent from the incomplete one should not read as loss."""
    from mito_model_search import posterior

    d = tiny_tree()
    # family 0: in all four tips. family 1: in the three complete tips, missing from tip 4.
    X = np.zeros((5, 2), dtype=bool)
    X[[1, 2, 3, 4], 0] = True
    X[[1, 2, 3], 1] = True
    vis = np.zeros(5, dtype=bool)
    vis[d["tips"]] = True
    g, lo = np.full(2, 0.1, np.float32), np.full(2, 1.0, np.float32)
    mult, root = np.ones(5, np.float32), np.full(2, 0.5, np.float32)

    plain = posterior(d, X, vis, g, lo, mult, root)[0]
    d["completeness"] = np.array([1.0, 1.0, 1.0, 1.0, 0.4])
    corrected = posterior(d, X, vis, g, lo, mult, root)[0]

    assert corrected[1] > plain[1], "the absence is explained as a miss, so the ancestor keeps the family"
    assert corrected[0] == pytest.approx(plain[0], abs=0.02), "a family present everywhere is unaffected"
