"""Figures for results/eukaryotes/metrics.json (written by run_eukaryotes.py)."""

import json
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

OUT = Path("results/eukaryotes")


def main():
    m = json.loads((OUT / "metrics.json").read_text())
    feats = list(m["loss_law"]["free_living"])
    fig, axes = plt.subplots(1, 3, figsize=(17, 4.8), gridspec_kw={"width_ratios": [1.4, 1, 1]})

    ax = axes[0]
    x = np.arange(len(feats))
    for j, (life, color) in enumerate([("free_living", "#2a9d8f"), ("parasite", "#e76f51")]):
        w = [m["loss_law"][life][f]["weight"] for f in feats]
        se = [m["loss_law"][life][f]["se"] for f in feats]
        ax.bar(x + (j - 0.5) * 0.38, w, 0.38, yerr=1.96 * np.array(se), capsize=2, color=color, label=life)
    ax.axhline(0, color="k", lw=0.6)
    ax.set_xticks(x, [f.replace("_", "\n") for f in feats], fontsize=7)
    ax.set(ylabel="effect on log loss rate (+ = lost faster)", title="Gene-family loss law by lifestyle")
    ax.legend(fontsize=8)

    ax = axes[1]
    rows = m["heldout_parasites"]
    keys = [("copies_only", "copies only"), ("learned_law", "learned law"),
            ("reference_plastid", "endosymbiosis law\n(plastid, reference)"),
            ("loss_frequency_elsewhere", "loss frequency\nin other parasites")]
    vals = [np.mean([r[k] for r in rows]) for k, _ in keys]
    ax.bar([lbl for _, lbl in keys], vals, color=["#b0b0b0", "#e76f51", "#8d99ae", "#264653"])
    for i, v in enumerate(vals):
        ax.text(i, v + 0.005, f"{v:.2f}", ha="center", fontsize=8)
    ax.set(ylim=(0.5, 0.9), ylabel="mean AUROC (8 held-out parasites)",
           title="Which families does a new parasite lose?")
    ax.tick_params(axis="x", labelsize=7)

    ax = axes[2]
    comp = m["comparison_with_endosymbiosis_v1"]
    ctxs = ["mitochondrion", "plastid", "insect_endosymbiont"]
    for j, (life, color) in enumerate([("free_living", "#2a9d8f"), ("parasite", "#e76f51")]):
        ax.bar(np.arange(3) + (j - 0.5) * 0.38, [comp[f"{life}_loss_vs_{c}"]["correlation"] for c in ctxs],
               0.38, color=color, label=life)
    ax.axhline(0, color="k", lw=0.6)
    ax.set_xticks(np.arange(3), ["mitochondrion", "plastid", "insect\nendosymbiont"], fontsize=8)
    ax.set(ylim=(-1, 1), ylabel="correlation of law coefficients",
           title="Similarity to stored endosymbiosis laws")
    ax.legend(fontsize=8)
    fig.tight_layout()
    fig.savefig(OUT / "fig_eukaryotes.png", dpi=130)
    print(f"wrote {OUT / 'fig_eukaryotes.png'}")


if __name__ == "__main__":
    main()
