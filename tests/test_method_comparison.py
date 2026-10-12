import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

import method_comparison as mc  # noqa: E402

# ((a, b), c): node 0 root, 1 = (a,b), 2 = a, 3 = b, 4 = c
D = {"parent": np.array([-1, 0, 1, 1, 0]), "children": [[1, 4], [2, 3], [], [], []], "order": [2, 3, 1, 4, 0]}


def mat(*cols):
    X = np.zeros((5, len(cols)), bool)
    for j, present in enumerate(cols):
        for v in present:
            X[v, j] = True
    return X


def test_wagner_root_and_hidden_tip():
    vis = np.array([False, False, True, True, True])
    X = mat({2, 3}, {2, 4}, set())
    root, tip = mc.wagner(D, X, vis)
    # a,b only: root present costs one loss (1), absent costs one gain (2) -> present
    assert root[0] == 1.0 and root[2] == 0.0
    vis_b = np.array([False, False, True, False, True])        # hide b; a and c carry family 1
    _, tip = mc.wagner(D, X, vis_b)
    assert tip[3, 1] == 1.0


def test_dollo_root_needs_both_root_sides():
    vis = np.array([False, False, True, True, True])
    X = mat({2, 3}, {2, 4})
    root, _ = mc.dollo(D, X, vis)
    assert root[0] == 0.0 and root[1] == 1.0
    vis_b = np.array([False, False, True, False, True])
    _, tip = mc.dollo(D, X, vis_b)
    assert tip[3, 1] == 1.0       # family 1 (a and c): gained at the root, so b keeps it
    assert tip[3, 0] == 0.0       # family 0 with b hidden: only a carries it, gained at a itself


def test_fold_is_deterministic():
    assert mc.fold_of("Homo sapiens") == mc.fold_of("Homo sapiens") < 5
