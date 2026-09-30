"""Law search: which gene families expand, independently, in several parasite lineages?

    python scripts/run_expansion.py

Most families shrink in parasites; a few grow. A family counts as expanded in a pair
when the parasite has at least twice the ancestor proxy's copies and at least 3 more.
Expansion is scored per clade (any pair in the clade), so ten Plasmodium species count
once. The null keeps each clade's number of expansions and shuffles which families
they hit, weighted by how often each family could expand at all (present in the
ancestor proxy); a family expanded in more clades than the null allows is convergent.
Free-living control pairs give the background rate.
"""

import json
import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
from run_modules import clade, load  # noqa: E402

from organelle_evo.eukaryotes.catalog import SPECIES, resolve_pairs  # noqa: E402
from organelle_evo.eukaryotes.features import enriched_features  # noqa: E402
from organelle_evo.laws import LAWS_DIR, save_law  # noqa: E402

N_NULL = 2000


def expanded(n, m):
    return (n > 0) & (m >= 2 * n) & (m >= n + 3)


def main():
    out = Path("results/expansion")
    out.mkdir(parents=True, exist_ok=True)
    profiles, meta, ann, fams, c = load()
    pairs = resolve_pairs(profiles)
    par = [(a, d) for a, d in pairs if SPECIES[d].lifestyle == "parasite"]
    ctrl = [(a, d) for a, d in pairs if SPECIES[d].lifestyle != "parasite"]
    clades = sorted({clade(d) for _, d in par})

    E = np.array([np.any([expanded(c[a], c[d]) for a, d in par if clade(d) == cl], 0) for cl in clades])
    A = np.array([np.any([c[a] > 0 for a, d in par if clade(d) == cl], 0) for cl in clades])
    n_clades = E.sum(0)
    ctrl_rate = np.mean([expanded(c[a], c[d]).sum() / max((c[a] > 0).sum(), 1) for a, d in ctrl])
    par_rate = np.mean([expanded(c[a], c[d]).sum() / max((c[a] > 0).sum(), 1) for a, d in par])
    print(f"{len(par)} parasite pairs in {len(clades)} clades; expansion rate per family: "
          f"parasites {par_rate:.4f}, free-living controls {ctrl_rate:.4f}")

    rng = np.random.default_rng(0)
    null_max = np.zeros((N_NULL, len(fams)), dtype=np.int16)
    for t in range(N_NULL):
        sim = np.zeros(len(fams), dtype=np.int16)
        for r in range(len(clades)):
            elig = np.flatnonzero(A[r])
            hit = rng.choice(elig, size=int(E[r].sum()), replace=False)
            sim[hit] += 1
        null_max[t] = sim
    # Per-family p-value: share of null draws with at least as many clades.
    p = (null_max >= n_clades[None, :]).mean(0)
    # Family-wise threshold: largest per-family count in each null draw.
    fw = np.quantile(null_max.max(1), 0.95)
    conv = np.flatnonzero(n_clades > fw)
    conv = conv[np.argsort(-n_clades[conv])]
    print(f"convergent threshold (95% family-wise): > {fw:.0f} clades; {len(conv)} families pass")
    desc = lambda j: f"{fams[j]}: {meta.get(fams[j], {}).get('description', '')}"  # noqa: E731
    for j in conv[:20]:
        which = [clades[r] for r in range(len(clades)) if E[r, j]]
        print(f"  {n_clades[j]} clades  {desc(j)}  [{', '.join(which)}]")

    _, names, X = enriched_features(profiles, meta, ann, c)
    cats = [k for k, n in enumerate(names) if n.startswith(("go:", "kw:"))]
    multi = n_clades >= 2
    fr, base = X[multi][:, cats].mean(0), X[:, cats].mean(0)
    ratio = (fr + 0.005) / (base + 0.005)
    enriched = [(names[cats[k]], round(float(ratio[k]), 2), round(float(fr[k]), 3))
                for k in np.argsort(-ratio)[:10] if fr[k] >= 0.03]
    print("functions over-represented among families expanded in >= 2 clades: "
          + ", ".join(f"{n} x{r}" for n, r, _ in enriched[:6]))

    result = {
        "n_parasite_pairs": len(par), "clades": clades,
        "expansion_rate": {"parasites": float(par_rate), "controls": float(ctrl_rate)},
        "familywise_threshold_clades": float(fw),
        "convergent": [{"family": fams[j], "description": meta.get(fams[j], {}).get("description", ""),
                        "n_clades": int(n_clades[j]), "p": float(p[j]),
                        "clades": [clades[r] for r in range(len(clades)) if E[r, j]]} for j in conv],
        "enriched_functions_multi_clade": enriched,
    }
    (out / "metrics.json").write_text(json.dumps(result, indent=2))
    save_law(
        LAWS_DIR / "convergent_expansion_v1.json",
        id="convergent_expansion_v1",
        scope="Gene-family copy-number expansion in eukaryotic parasites, across independent lineages.",
        model=("Family expanded in a pair: parasite copies >= 2x and >= ancestor + 3. Convergent: expanded "
               "in more clades than a family-wise 95% permutation threshold."),
        feature_names=[],
        data={"pairs": [f"{a} -> {d}" for a, d in par], "clades": clades},
        validation={"null": f"{N_NULL} permutations of expanded families within each clade",
                    "familywise_threshold_clades": float(fw), "n_convergent": len(conv),
                    "expansion_rate": result["expansion_rate"]},
        caveats=["Copy number is Pfam-domain gene counts; assembly and annotation quality affect it.",
                 "Clades are coarse; fungi merges several independent parasitic origins."],
        contexts={"convergent": result["convergent"], "enriched_functions": enriched},
    )

    fig, ax = plt.subplots(figsize=(9, 4.5))
    top = conv[:15][::-1]
    ax.barh([f"{fams[j]}" for j in top], n_clades[top], color="#e76f51")
    ax.axvline(fw + 0.5, color="k", ls="--", lw=1, label="family-wise 95% null")
    ax.set(xlabel=f"parasite clades with expansion (of {len(clades)})",
           title="Families that expand independently in several parasite lineages")
    ax.legend(fontsize=8)
    fig.tight_layout()
    fig.savefig(out / "fig_expansion.png", dpi=130)
    print(f"Done -> {out}/")


if __name__ == "__main__":
    main()
