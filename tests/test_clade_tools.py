import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

from pick_clade_sample import pick, ranks_of  # noqa: E402
from run_clade_ancestor import farthest_outgroup_tip, mrca, reroot  # noqa: E402
from run_mito_ancestor import parse_newick, postorder  # noqa: E402


def _tips(parent, label):
    inner = set(np.asarray(parent).tolist())
    return [v for v in range(len(parent)) if v not in inner]


def test_reroot_puts_clade_under_one_node():
    # FastTree-style unrooted tree whose written root sits inside the clade A-D
    P, L, lab = parse_newick("((A:1,B:1):1,(C:1,D:1):1,(O1:1,O2:3):2);")
    tips = _tips(P, lab)
    clade = {v: lab[v] in ("A", "B", "C", "D") for v in tips}
    assert mrca([v for v in tips if clade[v]], P, np.zeros(len(P))) == 0   # before: the root
    t = farthest_outgroup_tip(P, L, set(tips), clade)
    assert lab[t] == "O2"
    P2, L2, lab2 = reroot(P, L, lab, t)
    assert abs(L2.sum() - L.sum()) < 1e-3                                   # same tree length
    order, children = postorder(P2)
    depth = np.zeros(len(P2))
    for v in reversed(order):
        if v:
            depth[v] = depth[P2[v]] + L2[v]
    tips2 = _tips(P2, lab2)
    node = mrca([v for v in tips2 if lab2[v] in "ABCD"], P2, depth)
    below, stack = set(), [node]
    while stack:
        v = stack.pop()
        if not children[v]:
            below.add(lab2[v])
        stack.extend(children[v])
    assert below == {"A", "B", "C", "D"}


def test_ranks_of_reads_both_lineage_forms():
    e = {"scientificName": "x", "rank": "species",
         "lineage": [{"scientificName": "Ascomycota", "rank": "phylum"},
                     {"scientificName": "Saccharomycetales", "rank": "order"}]}
    assert ranks_of(e) == {"phylum": "Ascomycota", "order": "Saccharomycetales"}
    assert ranks_of({"lineage": ["Basidiomycota (phylum)", "Agaricales (order)"]}) == \
        {"phylum": "Basidiomycota", "order": "Agaricales"}


def test_pick_gives_every_order_one_before_any_gets_two():
    rows = {f"u{i}": {"organism": f"o{i}", "n_families": 1000 + i} for i in range(6)}
    lin = {"u0": {"order": "A"}, "u1": {"order": "A"}, "u2": {"order": "A"},
           "u3": {"order": "B"}, "u4": {"order": "C"}, "u5": {"order": "C"}}
    chosen, n_orders = pick(rows, lin, 4)
    assert n_orders == 3
    assert set(chosen[:3]) == {"u2", "u3", "u5"}      # richest of each order first
    assert chosen[3] == "u1"
