"""Law search: do parasites lose gene families in a shared order?

    python scripts/run_loss_order.py

If loss follows one order, a strongly reduced parasite loses what a mildly reduced one
lost, plus more (nestedness). For every pair of parasites from *different* clades (no
shared ancestry), among the families both ancestor proxies had:

    containment = share of the milder parasite's losses that the harsher one also lost
    null        = the harsher parasite's overall loss rate (random losses)

containment / null > 1 means ordered loss. A second check splits the parasites into the
milder and the harsher half and correlates each family's loss rate between the halves.
"""

import json
import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
from run_modules import MIN_ANCESTORS, clade, load  # noqa: E402

from organelle_evo.eukaryotes.catalog import SPECIES, resolve_pairs  # noqa: E402
from organelle_evo.eukaryotes.modules import loss_matrix  # noqa: E402
from organelle_evo.laws import LAWS_DIR, save_law  # noqa: E402


def main():
    out = Path("results/loss_order")
    out.mkdir(parents=True, exist_ok=True)
    profiles, meta, ann, fams, c = load()
    pairs = [(a, d) for a, d in resolve_pairs(profiles) if SPECIES[d].lifestyle == "parasite"]
    L = loss_matrix(pairs, c)
    obs = ~np.isnan(L)
    severity = np.nanmean(L, 1)
    cl = [clade(d) for _, d in pairs]

    ratios, rows = [], []
    for p in range(len(pairs)):
        for q in range(len(pairs)):
            if cl[p] == cl[q] or severity[p] >= severity[q]:
                continue
            both = obs[p] & obs[q]
            lost_p = both & (L[p] == 1)
            if lost_p.sum() < 20:
                continue
            contain = float((L[q][lost_p] == 1).mean())
            null = float(np.nanmean(L[q][both]))
            ratios.append(contain / null)
            rows.append({"milder": pairs[p][1], "harsher": pairs[q][1], "containment": contain, "null": null})
    ratios = np.array(ratios)
    print(f"{len(ratios)} cross-clade parasite pairs: containment / random = "
          f"median {np.median(ratios):.2f} (IQR {np.percentile(ratios, 25):.2f}-{np.percentile(ratios, 75):.2f}), "
          f"> 1 in {(ratios > 1).mean():.0%}")

    order = np.argsort(severity)
    mild, harsh = order[: len(order) // 2], order[len(order) // 2:]
    enough = (obs[mild].sum(0) >= MIN_ANCESTORS) & (obs[harsh].sum(0) >= MIN_ANCESTORS)
    r_mild, r_harsh = np.nanmean(L[mild][:, enough], 0), np.nanmean(L[harsh][:, enough], 0)
    from scipy.stats import spearmanr

    rho = float(spearmanr(r_mild, r_harsh).correlation)
    print(f"family loss rate, milder vs harsher half: Spearman {rho:.2f} over {enough.sum()} families "
          f"(mean loss {np.nanmean(L[mild]):.2f} vs {np.nanmean(L[harsh]):.2f})")

    # Which families are lost first (already by mild parasites) and which only by the harshest?
    fam_names = np.array(fams)[enough]
    first = np.argsort(-r_mild)[:12]
    last = np.argsort(-(r_harsh - r_mild))[:12]
    desc = lambda f: f"{f}: {meta.get(f, {}).get('description', '')}"  # noqa: E731
    print("lost first: " + "; ".join(desc(fam_names[j]) for j in first[:6]))
    print("lost only by the harshest: " + "; ".join(desc(fam_names[j]) for j in last[:6]))

    (out / "metrics.json").write_text(json.dumps({
        "n_cross_clade_comparisons": len(ratios),
        "containment_over_random": {"median": float(np.median(ratios)), "q25": float(np.percentile(ratios, 25)),
                                    "q75": float(np.percentile(ratios, 75)), "share_above_1": float((ratios > 1).mean())},
        "mild_vs_harsh_spearman": rho, "n_families": int(enough.sum()),
        "severity": {pairs[i][1]: float(severity[i]) for i in order},
        "lost_first": [desc(fam_names[j]) for j in first],
        "lost_only_by_harshest": [desc(fam_names[j]) for j in last],
        "comparisons": rows}, indent=2))

    save_law(
        LAWS_DIR / "loss_order_v1.json",
        id="loss_order_v1",
        scope="Gene-family loss across independent origins of parasitism in eukaryotes.",
        model="Nestedness: a more reduced parasite loses what a less reduced one lost, plus more.",
        feature_names=[],
        data={"pairs": [f"{a} -> {d}" for a, d in pairs], "n_families": int(enough.sum())},
        validation={"cross_clade_comparisons": len(ratios),
                    "containment_over_random_median": round(float(np.median(ratios)), 3),
                    "share_above_random": round(float((ratios > 1).mean()), 3),
                    "mild_vs_harsh_spearman": round(rho, 3)},
        caveats=["Ancestor proxies are extant free-living relatives.",
                 "Order is a population tendency; single families can deviate."],
        contexts={"lost_first": [desc(fam_names[j]) for j in first],
                  "lost_only_by_harshest": [desc(fam_names[j]) for j in last]},
    )

    fig, axes = plt.subplots(1, 2, figsize=(11, 4.2))
    axes[0].hist(ratios, bins=40, color="#e76f51")
    axes[0].axvline(1, color="k", ls="--", lw=1)
    axes[0].set(xlabel="containment / random", ylabel="parasite pairs (different clades)",
                title="Harsher parasites lose what milder ones lost")
    axes[1].scatter(r_mild, r_harsh, s=3, alpha=0.25, color="#264653")
    axes[1].plot([0, 1], [0, 1], "k--", lw=1)
    axes[1].set(xlabel="loss rate, milder half", ylabel="loss rate, harsher half",
                title=f"Same order of loss (Spearman {rho:.2f})")
    fig.tight_layout()
    fig.savefig(out / "fig_loss_order.png", dpi=130)
    print(f"Done -> {out}/")


if __name__ == "__main__":
    main()
