"""The vault's verdicts are read off law files automatically, so they are pinned to cases whose
answer is known from the project record. The first version compared a count of pairs with an AUROC
and called a negative law positive; these tests are what would have caught it."""

import json
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

ROOT = Path(__file__).resolve().parents[1]


def law(lid):
    for f in (ROOT / "laws" / f"{lid}.json", ROOT / "laws" / "animals" / f"{lid}.json"):
        if f.exists():
            return json.loads(f.read_text())
    pytest.skip(f"{lid} not in this checkout")


@pytest.mark.parametrize("lid,expected", [
    ("animal_content_v1", "음성"),     # axis law 0.794 against rarity 0.836
    ("loss_prediction_v1", "음성"),    # the law alone 0.793 against memorisation 0.813
    ("environment_v3", "음성"),        # environment law 0.814 against memorisation 0.849
    ("proteome_traits_v1", "양성"),    # composition beats taxonomy, interval clear of zero
    ("genome_traits_v1", "무승부"),     # point estimate ahead, interval holds zero
    ("animal_temperature_v1", "전이 검정"),
    # its own claim is the difference from a no-selection control, whose interval holds zero; it
    # beats rarity by 0.023, which is not the question it asks
    ("lab_evolution_v1", "무승부"),
    # leave-tips-out saturates (0.986 vs 0.980); the known-truth test against present-day
    # frequency is the ancestor test and is clear (0.995 vs 0.976)
    ("plastid_ancestor_v1", "양성"),
])
def test_known_verdicts(lid, expected):
    from build_lab_vault import verdict_of

    d = law(lid)
    assert verdict_of(d.get("validation"), lid)[0] == expected


def test_never_compares_different_metrics():
    """A count beside an AUROC must not be read as a competing method."""
    from build_lab_vault import comparison_groups

    v = {"leave_one_out_auroc": {"axes_better_in": 9, "rarity": 0.836, "axis_law": 0.794}}
    (g,) = comparison_groups(v)
    assert g["law"] == "axis_law" and g["margin"] < 0


def test_loss_in_a_path_name_does_not_flip_the_direction():
    from build_lab_vault import comparison_groups

    v = {"loss_biased · leave_tips_out_auroc": {"reconstruction": 0.98, "alpha_frequency": 0.96}}
    (g,) = comparison_groups(v)
    assert g["lower_is_better"] is False and g["margin"] > 0


def test_law_plus_something_is_not_the_law():
    from build_lab_vault import comparison_groups

    v = {"heldout_auroc": {"law": 0.79, "law+relatives": 0.92, "memorisation": 0.81}}
    (g,) = comparison_groups(v)
    assert g["law"] == "law" and g["margin"] < 0


def test_ancestor_verdict_uses_the_laws_own_node_and_frequency_baseline():
    """Known truth decides, against present-day frequency (not the flat prior), on the law's own
    node; subclade and core-node grades are other nodes."""
    from build_lab_vault import verdict_of

    d = law("fungal_ancestor_v1")
    kt = d["validation"]["known_truth"]
    label, margin, _ = verdict_of(d["validation"], "fungal_ancestor_v1")
    assert label == "양성"
    assert margin == pytest.approx(kt["recon_auroc"] - kt["freq_auroc"], abs=1e-3)


def test_several_roots_are_judged_on_the_worst():
    from build_lab_vault import verdict_of

    d = law("leca_ancestor_v2")
    per = d["validation"]["known_truth_per_root"]
    worst = min(g["recon_auroc"] - g["freq_auroc"] for g in per.values())
    assert verdict_of(d["validation"], "leca_ancestor_v2")[1] == pytest.approx(worst, abs=1e-3)
