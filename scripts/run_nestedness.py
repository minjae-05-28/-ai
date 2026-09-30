"""Is loss order a law of genome reduction in general, beyond per-gene propensity?

    python scripts/run_nestedness.py

For a loss matrix (lineages x genes, 1 = lost), containment is the mean over lineage
pairs (milder, harsher) of the share of the milder lineage's losses that the harsher one
also lost. Two nulls:
  row null    each lineage keeps its number of losses; genes drawn at random
  fixed-fixed each lineage keeps its number of losses AND each gene keeps its number of
              lineages that lost it (curveball swaps)
Beating the row null only says that some genes are lost more often everywhere. Beating
the fixed-fixed null says the losses are ordered more strictly than those per-gene rates
alone produce: a lineage that has lost a "late" gene has lost the "early" ones too.

Systems: mitochondria, plastids, insect endosymbionts (genes of the ancestral universe),
and eukaryotic parasites (Pfam families present in every ancestor proxy, so nothing is
missing).
"""

import json
import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
from run_modules import load  # noqa: E402
from run_realdata import CATALOG, load_system  # noqa: E402

from organelle_evo.eukaryotes.catalog import SPECIES, resolve_pairs  # noqa: E402
from organelle_evo.laws import LAWS_DIR, save_law  # noqa: E402

N_NULL = 200
N_SWAPS = 5


def containment(M: np.ndarray) -> float:
    """Mean over (milder, harsher) pairs of |lost_p & lost_q| / |lost_p|."""
    M = M.astype(float)
    n = M.sum(1)
    inter = M @ M.T
    vals = []
    for p in range(len(M)):
        for q in range(len(M)):
            if n[p] > 0 and n[p] < n[q]:
                vals.append(inter[p, q] / n[p])
    return float(np.mean(vals))


def curveball(M: np.ndarray, rng, n_swaps: int) -> np.ndarray:
    """Uniform random matrix with the same row and column sums (Strona et al. 2014)."""
    rows = [set(np.flatnonzero(r)) for r in M]
    L = len(rows)
    for _ in range(n_swaps * L):
        a, b = rng.choice(L, 2, replace=False)
        only_a, only_b = rows[a] - rows[b], rows[b] - rows[a]
        if not only_a or not only_b:
            continue
        pool = list(only_a | only_b)
        k = len(only_a)
        rng.shuffle(pool)
        common = rows[a] & rows[b]
        rows[a], rows[b] = common | set(pool[:k]), common | set(pool[k:])
    out = np.zeros_like(M)
    for i, r in enumerate(rows):
        out[i, list(r)] = 1
    return out


def row_null(M: np.ndarray, rng) -> np.ndarray:
    out = np.zeros_like(M)
    for i, k in enumerate(M.sum(1)):
        out[i, rng.choice(M.shape[1], int(k), replace=False)] = 1
    return out


def test(M: np.ndarray, rng) -> dict:
    keep = (M.sum(0) > 0) & (M.sum(0) < len(M))  # genes lost by some but not all
    M = M[:, keep].astype(np.int8)
    obs = containment(M)
    rn = np.array([containment(row_null(M, rng)) for _ in range(N_NULL)])
    ff = np.array([containment(curveball(M, rng, N_SWAPS)) for _ in range(N_NULL)])
    return {"lineages": int(M.shape[0]), "genes": int(M.shape[1]), "containment": obs,
            "row_null_mean": float(rn.mean()), "row_null_z": float((obs - rn.mean()) / rn.std()),
            "fixed_null_mean": float(ff.mean()), "fixed_null_z": float((obs - ff.mean()) / ff.std()),
            "fixed_null_p": float((ff >= obs).mean())}


def main():
    out = Path("results/nestedness")
    out.mkdir(parents=True, exist_ok=True)
    rng = np.random.default_rng(0)
    cache = json.loads(Path("data/processed/homology.json").read_text()) \
        if Path("data/processed/homology.json").exists() else {}
    matrices = {}
    for system in CATALOG:
        ds, _ = load_system(system, Path("data/raw"), cache)
        matrices[system] = ~ds.present
    profiles, meta, ann, fams, c = load()
    pairs = [(a, d) for a, d in resolve_pairs(profiles) if SPECIES[d].lifestyle == "parasite"]
    anc_all = np.all([c[a] > 0 for a, _ in pairs], 0)
    matrices["eukaryote_parasites"] = np.array([(c[d] == 0)[anc_all] for _, d in pairs])

    results = {}
    for name, M in matrices.items():
        r = test(np.asarray(M), rng)
        results[name] = r
        print(f"  {name:22s} {r['lineages']:3d} lineages x {r['genes']:4d} genes  containment {r['containment']:.3f}  "
              f"row null {r['row_null_mean']:.3f} (z {r['row_null_z']:+.1f})  "
              f"fixed-fixed {r['fixed_null_mean']:.3f} (z {r['fixed_null_z']:+.1f}, p {r['fixed_null_p']:.3f})")
    (out / "metrics.json").write_text(json.dumps(results, indent=2))
    save_law(
        LAWS_DIR / "loss_order_v2.json",
        id="loss_order_v2",
        scope="Order of gene loss in genome reduction: organelles, insect endosymbionts and eukaryotic parasites.",
        model="Nestedness (containment) against row-fixed and row-and-column-fixed (curveball) nulls.",
        feature_names=[],
        data={k: {"lineages": v["lineages"], "genes": v["genes"]} for k, v in results.items()},
        validation={"n_null": N_NULL, "results": results},
        caveats=["Beating the fixed-fixed null means ordering beyond per-gene loss rates.",
                 "Lineages are not independent (shared ancestry inflates nestedness)."],
        contexts={},
    )

    fig, ax = plt.subplots(figsize=(8, 4))
    names = list(results)
    xs = np.arange(len(names))
    for off, key, col, lab in [(-0.25, "row_null_mean", "#b0b0b0", "random losses (row null)"),
                               (0, "fixed_null_mean", "#8d99ae", "same per-gene loss rates (fixed-fixed)"),
                               (0.25, "containment", "#e76f51", "observed")]:
        ax.bar(xs + off, [results[n][key] for n in names], 0.25, color=col, label=lab)
    ax.set_xticks(xs, [n.replace("_", " ") for n in names], fontsize=9)
    ax.set(ylabel="share of milder lineage's losses\nalso lost by harsher lineage", ylim=(0, 1),
           title="Is gene loss ordered?")
    ax.legend(fontsize=8)
    fig.tight_layout()
    fig.savefig(out / "fig_nestedness.png", dpi=130)
    print(f"Done -> {out}/")


if __name__ == "__main__":
    main()
