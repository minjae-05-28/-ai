import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

from gene_trees import metrics, trim  # noqa: E402


def tags(spec):
    out = {}
    for name, (dom, sg, am) in spec.items():
        out[name] = {"domain": dom, "supergroup": sg, "amorphea": am}
    return out


T = tags({"e1": ("E", "Metazoa", True), "e2": ("E", "Fungi", True), "e3": ("E", "Viridiplantae", False),
          "e4": ("E", "Discoba", False), "p1": ("P", None, None), "p2": ("P", None, None),
          "p3": ("P", None, None), "p4": ("P", None, None)})


def test_one_eukaryote_clade():
    nwk = "(((e1:0.1,e2:0.1)1.0:0.1,(e3:0.1,e4:0.1)1.0:0.1)1.0:0.5,((p1:0.1,p2:0.1)1.0:0.2,(p3:0.1,p4:0.1)1.0:0.2)1.0:0.3);"
    m = metrics(nwk, T)
    assert m["K_raw"] == 1 and m["K_sup"] == 1
    assert m["leca_like"] and m["largest_group_supergroups"] == 4
    assert m["prok_nearest"] == 0


def test_supported_split_counts_twice():
    # eukaryotes split by a strongly supported prokaryote clade
    nwk = "(((e1:0.1,e2:0.1)1.0:0.1,(p1:0.1,p2:0.1)0.99:0.1)0.99:0.3,((e3:0.1,e4:0.1)1.0:0.1,(p3:0.1,p4:0.1)0.99:0.1)0.99:0.3);"
    m = metrics(nwk, T)
    assert m["K_raw"] == 2 and m["K_sup"] == 2
    assert not m["leca_like"]


def test_unsupported_split_collapses():
    # same topology, but the nodes that separate the eukaryote groups have weak support
    nwk = "(((e1:0.1,e2:0.1)1.0:0.1,(p1:0.1,p2:0.1)0.99:0.1)0.3:0.3,((e3:0.1,e4:0.1)1.0:0.1,(p3:0.1,p4:0.1)0.99:0.1)0.4:0.3);"
    m = metrics(nwk, T)
    assert m["K_raw"] == 2
    assert m["K_sup"] == 1
    assert m["leca_like"]


def test_trim_drops_gappy_columns_and_sparse_rows():
    rows = {"a": "AC-D", "b": "A--D", "c": "-C-D", "d": "----"}
    out = trim(rows)
    assert set(out) == {"a", "b", "c"}
    assert all(len(v) == 3 for v in out.values())
