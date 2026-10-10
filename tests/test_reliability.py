import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

from reliability import gene_tree_masks  # noqa: E402

PANEL = {"E1": {"domain": "E", "organism": "a1"}, "E2": {"domain": "E", "organism": "a2"},
         "E3": {"domain": "E", "organism": "b1"}, "E4": {"domain": "E", "organism": "b2"},
         "P1": {"domain": "P"}, "P2": {"domain": "P"}, "P3": {"domain": "P"}, "P4": {"domain": "P"}}
TIP = {"a1": 0, "a2": 1, "b1": 2, "b2": 3}
A, B = 0b0011, 0b1100


def verdict(nwk):
    strong, groups, present = gene_tree_masks(nwk, PANEL, TIP)
    if any((m & A) and (m & B) for m in strong):
        return "shared"
    if not any((m & A) and (m & B) for m in groups):
        return "separate"
    return "unclear"


def test_one_eukaryote_clade_is_shared():
    nwk = ("(((E1|x:0.1,E2|x:0.1)1.0:0.1,(E3|x:0.1,E4|x:0.1)1.0:0.1)0.99:0.5,"
           "((P1|x:0.1,P2|x:0.1)1.0:0.2,(P3|x:0.1,P4|x:0.1)1.0:0.2)1.0:0.3);")
    assert verdict(nwk) == "shared"


def test_copies_split_by_supported_prokaryotes_are_separate():
    nwk = ("(((E1|x:0.1,E2|x:0.1)1.0:0.1,(P1|x:0.1,P2|x:0.1)0.99:0.1)0.99:0.3,"
           "((E3|x:0.1,E4|x:0.1)1.0:0.1,(P3|x:0.1,P4|x:0.1)0.99:0.1)0.99:0.3);")
    assert verdict(nwk) == "separate"


def test_weak_split_is_unclear():
    nwk = ("(((E1|x:0.1,E2|x:0.1)1.0:0.1,(P1|x:0.1,P2|x:0.1)0.99:0.1)0.3:0.3,"
           "((E3|x:0.1,E4|x:0.1)1.0:0.1,(P3|x:0.1,P4|x:0.1)0.99:0.1)0.4:0.3);")
    assert verdict(nwk) == "unclear"


def test_eukaryote_only_tree_is_not_checked():
    assert gene_tree_masks("((E1|x:0.1,E2|x:0.1)1.0:0.1,(E3|x:0.1,E4|x:0.1)1.0:0.1);", PANEL, TIP) is None
