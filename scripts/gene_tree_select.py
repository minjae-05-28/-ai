"""Pick the families for the gene-tree test (pre-registration 6) and write the panel of proteomes.

    python scripts/gene_tree_select.py   -> data/gene_trees/families.json

Families: Vosseberg-tested Pfams that we score and that occur in at least 1% of UniProt bacterial
or archaeal proteomes. Vosseberg-LECA and non-LECA matched on present-day eukaryotic frequency:
within each frequency decile the same number of each (up to 25 of each), drawn with seed 0.
"""

import json
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
from leca_model_variants import OUT  # noqa: E402,F401
from prokaryote_and_loso import labels, prokaryote_shares  # noqa: E402

PER_BIN = 25


def main():
    z = np.load("results/leca_models/posteriors.npz", allow_pickle=False)
    fams = [str(f) for f in z["families"]]
    freq = z["clade_frequency"].astype(float)
    pro = prokaryote_shares(fams)
    meta = json.loads(Path("data/eukaryotes/pfam_meta.json").read_text())
    acc = np.array([meta.get(f, {}).get("accession", "").split(".")[0] for f in fams])
    leca, tested = labels()
    ok = np.isin(acc, list(tested)) & ((pro["bacteria"] >= 0.01) | (pro["archaea"] >= 0.01))
    y = np.isin(acc, list(leca))
    idx = np.flatnonzero(ok)
    edges = np.quantile(freq[idx], np.linspace(0, 1, 11))
    dec = np.clip(np.searchsorted(edges, freq, side="right") - 1, 0, 9)
    rng = np.random.default_rng(0)
    per_bin = PER_BIN
    picked = []
    for b in range(10):
        pos = [i for i in idx if dec[i] == b and y[i]]
        neg = [i for i in idx if dec[i] == b and not y[i]]
        k = min(per_bin, len(pos), len(neg))
        picked += list(rng.choice(pos, k, replace=False)) + list(rng.choice(neg, k, replace=False))
    out = [{"family": fams[i], "accession": str(acc[i]), "vosseberg_leca": bool(y[i]),
            "eukaryote_frequency": round(float(freq[i]), 4), "bacteria_share": round(float(pro["bacteria"][i]), 4),
            "archaea_share": round(float(pro["archaea"][i]), 4), "frequency_decile": int(dec[i])} for i in picked]
    Path("data/gene_trees").mkdir(parents=True, exist_ok=True)
    Path("data/gene_trees/families.json").write_text(json.dumps(
        {"rule": __doc__.strip().split("\n\n")[1], "n_candidates": int(len(idx)), "families": out}, indent=1))
    n_pos = sum(r["vosseberg_leca"] for r in out)
    print(f"{len(idx)} candidates; picked {len(out)} ({n_pos} LECA, {len(out) - n_pos} not)")


if __name__ == "__main__":
    main()
