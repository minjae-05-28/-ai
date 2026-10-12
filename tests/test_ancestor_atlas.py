import base64
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

import ancestor_atlas as aa  # noqa: E402


def pack(codes):
    """Same packing as build(): two 3-bit codes per byte, high nibble first."""
    pf = np.asarray(codes, np.uint8)
    packed = np.zeros((len(pf) + 1) // 2, np.uint8)
    packed[:len(pf[0::2])] = pf[0::2] << 4
    packed[:len(pf[1::2])] |= pf[1::2]
    return base64.b64encode(packed.tobytes()).decode()


def test_pack_decode_roundtrip_odd_length():
    codes = [4, 7, 0, 3, 5]
    atlas = {"family_order": list("abcde"), "nodes": {"1": {"codes": pack(codes)}}}
    assert list(aa.decode(atlas, 1)) == codes


def test_path_to_root():
    atlas = {"parent": {"5": 2, "2": 0, "0": None}}
    assert aa.path_to_root(atlas, 5) == [0, 2, 5]


def test_modules_have_unique_keys_and_go_terms():
    keys = [k for k, _, _ in aa.MODULES]
    assert len(keys) == len(set(keys))
    assert all(g.startswith("GO:") for _, _, gos in aa.MODULES for g in gos)
