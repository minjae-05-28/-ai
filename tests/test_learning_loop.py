import json
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

import learning_loop as ll  # noqa: E402


def test_to_newick_binary_scaffold():
    parent = [-1, 0, 0, 0, 0]
    length = [0.0, 0.1, 0.2, 0.3, 0.4]
    label = ["", "a", "b'x", "c", "d"]
    nwk = ll.to_newick(parent, length, label)
    assert nwk.endswith(";")
    assert "'bx'" in nwk                     # apostrophes stripped from labels
    assert nwk.count("(") == 3               # 4 children -> balanced binary: 2 scaffold nodes + root


def test_lesson_from_picks_best_weight(tmp_path, monkeypatch):
    monkeypatch.setattr(ll, "RES", tmp_path)
    rows = [{"group": "Metazoa", "blend": [0.90, 0.95, 0.93, 0.92, 0.91]} for _ in range(30)]
    rows += [{"group": "Fungi", "blend": [0.80, 0.81, 0.82, 0.83, 0.90]} for _ in range(5)]
    (tmp_path / "round_002.json").write_text(json.dumps({"species": rows}))
    lesson = ll.lesson_from({"rounds": [{"round": 2}]})
    assert lesson["w_global"] == 0.25
    assert lesson["w_by_group"] == {"Metazoa": 0.25}     # Fungi has fewer than 30 scored species
    assert lesson["n_from"] == 35


def test_lesson_default_without_history():
    assert ll.lesson_from({"rounds": []}) == {"w_global": 1.0, "w_by_group": {}, "n_from": 0}


def test_group_of():
    assert ll.group_of(["Eukaryota", "Opisthokonta", "Metazoa", "Homo"]) == "Metazoa"
    assert ll.group_of(["Eukaryota", "Haptista"]) == "기타"


def test_graft_single_and_multi_anchor():
    # root 0 -> internal 1 (tips 2, 3) and tip 4
    d = {"parent": np.array([-1, 0, 1, 1, 0]), "length": np.array([0, 0.1, 0.2, 0.2, 0.5]),
         "tips": [2, 3, 4], "depth": np.array([0, 0.1, 0.3, 0.3, 0.5])}
    names = {2: "a", 3: "b", 4: "c"}
    tip_lin = {2: {"E", "X"}, 3: {"E", "X"}, 4: {"E", "Y"}}
    new = {"NS_1": {"lineage": ["E", "X", "sp1"]}, "NS_2": {"lineage": ["E", "Y", "sp2"]}}
    parent, length, label, placed = ll.graft(d, names, tip_lin, new)
    assert placed == {"NS_1": "X", "NS_2": "Y"}
    i1 = label.index("NS_1")
    assert parent[i1] == 1                                   # under the ancestor of a and b
    i2 = label.index("NS_2")
    mid = parent[i2]
    assert parent[4] == mid and abs(length[4] - 0.25) < 1e-9  # c's branch split in half
