"""Law search: is parasitic gene loss convergent across lineages?

    python scripts/run_transfer.py [--epochs 300]

Leave-one-clade-out: every pair whose descendant belongs to the held-out clade is removed
from training. If the feature law still predicts that clade's losses, the rule is shared
across independent origins of parasitism (convergence). Memorisation (each family's loss
rate in the training parasites) is the comparison: it needs the same families to behave
the same way, the law only needs the same kinds of families to.
"""

import argparse
import json
import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import torch

from organelle_evo.eukaryotes.catalog import AXES, SPECIES, design, resolve_pairs
from organelle_evo.eukaryotes.features import enriched_features
from organelle_evo.eukaryotes.model import counts, family_features, fit_bd
from organelle_evo.predict import auroc

sys.path.insert(0, str(Path(__file__).resolve().parent))
from run_features import predict  # noqa: E402

DATA = Path("data/eukaryotes")
LABELS = ("base", *AXES)


def clade(species: str) -> str:
    return SPECIES[species].group.split("_")[0]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--epochs", type=int, default=300)
    ap.add_argument("--out", default="results/transfer")
    args = ap.parse_args()
    torch.set_num_threads(4)
    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)

    meta = json.loads((DATA / "pfam_meta.json").read_text())
    ann = json.loads((DATA / "family_annotations.json").read_text())
    profiles = {}
    for f in DATA.glob("*.json"):
        if f.name not in ("pfam_meta.json", "family_annotations.json"):
            d = json.loads(f.read_text())
            profiles[d["species"]] = d
    fams, _ = family_features(list(profiles.values()), meta)
    c = {s: counts(p, fams) for s, p in profiles.items()}
    fams, names, x = enriched_features(profiles, meta, ann, c)
    pairs = resolve_pairs(profiles)
    data = [(c[a], c[d], design(d)) for a, d in pairs]
    par_clades = sorted({clade(d) for (a, d), (_, _, z) in zip(pairs, data) if z[1]})

    rows = []
    for cl in par_clades:
        test = [i for i, ((a, d), (_, _, z)) in enumerate(zip(pairs, data)) if z[1] and clade(d) == cl]
        drop = {i for i, (a, d) in enumerate(pairs) if clade(d) == cl}
        train = [d_ for j, d_ in enumerate(data) if j not in drop]
        law = fit_bd(x, train, LABELS, epochs=args.epochs)
        train_par = [(n, m) for n, m, z in train if z[1]]
        for i in test:
            (a, d), (n, m, z) = pairs[i], data[i]
            had = n > 0
            lost = (m == 0)[had]
            idx = np.flatnonzero(had)
            seen = [any(tn[j] > 0 for tn, _ in train_par) for j in idx]
            freq = np.array([np.mean([tm[j] == 0 for tn, tm in train_par if tn[j] > 0]) if s else 0.5
                             for j, s in zip(idx, seen)])
            row = {"pair": f"{a} -> {d}", "clade": cl,
                   "copies_only": auroc(-n[had].astype(float), lost),
                   "memorisation": auroc(freq, lost),
                   "law": auroc(predict(law, train, z, n[had], x[had], lost.sum()), lost)}
            rows.append(row)
            print(f"  {cl:14s} {d:34s} copies {row['copies_only']:.3f}  law {row['law']:.3f}  "
                  f"memorisation {row['memorisation']:.3f}", flush=True)

    keys = ("copies_only", "law", "memorisation")
    mean = {k: float(np.mean([r[k] for r in rows])) for k in keys}
    by_clade = {cl: {k: float(np.mean([r[k] for r in rows if r["clade"] == cl])) for k in keys} for cl in par_clades}
    print("leave-one-clade-out mean AUROC: " + ", ".join(f"{k}={v:.3f}" for k, v in mean.items()))
    within = json.loads(Path("results/features/metrics.json").read_text())["mean_heldout_auroc"] \
        if Path("results/features/metrics.json").exists() else None
    (out / "metrics.json").write_text(json.dumps(
        {"scheme": "leave-one-clade-out", "mean_auroc": mean, "by_clade": by_clade,
         "within_clade_5fold": within, "heldout": rows}, indent=2))

    fig, ax = plt.subplots(figsize=(10, 4.2))
    xs = np.arange(len(par_clades))
    for off, k, col, lab in [(-0.27, "copies_only", "#b0b0b0", "copies only"),
                             (0, "law", "#e76f51", "enriched law"),
                             (0.27, "memorisation", "#264653", "memorisation")]:
        ax.bar(xs + off, [by_clade[cl][k] for cl in par_clades], 0.27, color=col, label=f"{lab} ({mean[k]:.3f})")
    ax.set_xticks(xs, par_clades, rotation=30, ha="right")
    ax.set(ylim=(0.45, 1), ylabel="AUROC, clade never seen in training",
           title="Does the loss law transfer to a lineage it never saw?")
    ax.legend(fontsize=8)
    fig.tight_layout()
    fig.savefig(out / "fig_transfer.png", dpi=130)
    print(f"Done -> {out}/")


if __name__ == "__main__":
    main()
