"""Reconstruct the alveolate ancestor of Plasmodium and evolve it under different laws.

    python scripts/run_plasmodium_ancestor.py [--out results/plasmodium_ancestor]

1. Wagner parsimony over ((Plasmodium, Toxoplasma), Cryptosporidium) + (Tetrahymena,
   Ichthyophthirius) gives the gene-family content of their common ancestor. For
   scoring, the ancestor is rebuilt *without* Plasmodium so the answer cannot leak in.
2. That ancestor is evolved under each law: free-living, parasite (without the
   Plasmodium pair), parasite (without any apicomplexan), and — as a reference only —
   the three stored endosymbiosis laws.
3. Each law is scored on which ancestral families Plasmodium actually lost (AUROC, at a
   matched number of losses) and, for the birth-death laws, on how many families remain.
"""

import argparse
import json
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import torch

from organelle_evo.eukaryotes.ancestral import prune, wagner_ancestor
from organelle_evo.eukaryotes.birthdeath import simulate
from organelle_evo.eukaryotes.catalog import PAIRS, PARASITE, lifestyle, slug
from organelle_evo.eukaryotes.model import (
    FAMILY_FEATURES,
    counts,
    family_features,
    fit_bd,
    loss_probability,
    offset_for_losses,
)
from organelle_evo.laws import load_law
from organelle_evo.predict import auroc

DATA = Path("data/eukaryotes")
LIFESTYLES = ("free_living", "parasite")
PLASMO = "Plasmodium falciparum"
APICOMPLEXA = {"Plasmodium falciparum", "Toxoplasma gondii", "Cryptosporidium parvum"}
TREE = (((PLASMO, "Toxoplasma gondii"), "Cryptosporidium parvum"),
        ("Tetrahymena thermophila", "Ichthyophthirius multifiliis"))


def _bisect(f, target, lo=-15.0, hi=10.0):
    for _ in range(60):
        mid = (lo + hi) / 2
        lo, hi = (mid, hi) if f(mid) < target else (lo, mid)
    return (lo + hi) / 2


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default="results/plasmodium_ancestor")
    ap.add_argument("--epochs", type=int, default=400)
    args = ap.parse_args()
    torch.set_num_threads(4)
    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)

    meta = json.loads((DATA / "pfam_meta.json").read_text()) if (DATA / "pfam_meta.json").exists() else {}
    profiles = {}
    for f in DATA.glob("*.json"):
        if f.name != "pfam_meta.json":
            d = json.loads(f.read_text())
            profiles[d["species"]] = d
    fams, x = family_features(list(profiles.values()), meta)
    c = {sp: counts(p, fams) for sp, p in profiles.items()}

    # 1. Ancestors
    anc_eval = wagner_ancestor(prune(TREE, {PLASMO}), c)
    anc_full = wagner_ancestor(TREE, c)
    target = c[PLASMO]
    had = anc_eval > 0
    lost = had & (target == 0)
    print(f"ancestor (without Plasmodium): {had.sum()} families; with Plasmodium: {(anc_full > 0).sum()}")
    print(f"Plasmodium keeps {int((had & (target > 0)).sum())}, lost {int(lost.sum())} of them, "
          f"has {int(((~had) & (target > 0)).sum())} families the ancestor lacked")

    # 2. Laws
    pairs = [(a, d) for a, d in PAIRS if a in profiles and d in profiles]

    def data_for(exclude):
        return [(c[a], c[d], LIFESTYLES.index(lifestyle(d))) for a, d in pairs if d not in exclude]

    laws = {
        "parasite (Plasmodium pair held out)": (fit_bd(x, data_for({PLASMO}), LIFESTYLES, epochs=args.epochs),
                                                data_for({PLASMO}), 1),
        "parasite (no apicomplexan seen)": (fit_bd(x, data_for(APICOMPLEXA), LIFESTYLES, epochs=args.epochs),
                                            data_for(APICOMPLEXA), 1),
    }
    laws["free-living"] = (laws["parasite (Plasmodium pair held out)"][0], data_for({PLASMO}), 0)

    n_had, x_had = anc_eval[had], x[had]
    results, projections, class_loss = {}, {}, {}
    rng = np.random.default_rng(0)

    def class_fractions(p_lost):
        out_ = {}
        for i, cls in enumerate(FAMILY_FEATURES):
            if i >= 3:
                m = x_had[:, i] == 1
                out_[cls] = float(p_lost[m].mean()) if m.any() else float("nan")
        return out_

    for name, (law, train, s) in laws.items():
        idx = [i for i, (_, _, si) in enumerate(train) if si == s]
        a_lam, a_mu, a_nu = law.a_lam[idx].mean(), law.a_mu[idx].mean(), law.a_nu[idx].mean()
        # which families: offsets matched to the observed number of losses
        a_mu_m = offset_for_losses(n_had, x_had, law.w_lam[s], law.w_mu[s], a_lam, lost.sum())
        p_lost = loss_probability(n_had, x_had, law.w_lam[s], law.w_mu[s], a_lam, a_mu_m)
        results[name] = auroc(p_lost, lost[had])
        class_loss[name] = class_fractions(p_lost)
        # how many: the law's own typical divergence
        sims = simulate(np.tile(anc_eval, (200, 1)), a_lam + x @ law.w_lam[s], a_mu + x @ law.w_mu[s],
                        a_nu + x @ law.w_nu[s], n_steps=100, rng=rng)
        projections[name] = np.quantile((sims > 0).sum(1), [0.05, 0.5, 0.95]).tolist()

    ref = load_law("endosymbiosis_v1")
    for ctx in ref.weights:
        base = x_had @ ref.weights[ctx]

        def p_lost_at(a, base=base):
            return (-np.expm1(-np.exp(a + base))) ** n_had

        a = _bisect(lambda a: p_lost_at(a).sum(), lost.sum())
        name = f"reference: endosymbiosis ({ctx})"
        results[name] = auroc(p_lost_at(a), lost[had])
        class_loss[name] = class_fractions(p_lost_at(a))

    results["baseline: fewer copies lost first"] = auroc(-n_had.astype(float), lost[had])
    class_loss["actual Plasmodium"] = class_fractions(lost[had].astype(float))

    for k, v in results.items():
        print(f"  AUROC {k:48s} {v:.3f}")
    for k, v in projections.items():
        print(f"  families after evolving under {k:36s}: {v[1]:.0f} ({v[0]:.0f}-{v[2]:.0f}); "
              f"actual Plasmodium {int((target > 0).sum())}")

    # 3. Figure
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5), gridspec_kw={"width_ratios": [1, 1.3]})
    names = list(results)
    ax1.barh(names[::-1], [results[n] for n in names[::-1]],
             color=["#b0b0b0" if n.startswith(("reference", "baseline")) else "#e76f51" for n in names[::-1]])
    ax1.axvline(0.5, color="k", lw=0.6)
    ax1.set(xlim=(0.4, 1), xlabel="AUROC: which ancestral families Plasmodium lost",
            title="Evolving the alveolate ancestor")
    for i, n in enumerate(names[::-1]):
        ax1.text(results[n] + 0.005, i, f"{results[n]:.2f}", va="center", fontsize=8)
    classes = [k for k in class_loss["actual Plasmodium"]]
    show = ["actual Plasmodium", "parasite (no apicomplexan seen)", "free-living",
            "reference: endosymbiosis (mitochondrion)"]
    width = 0.8 / len(show)
    for j, n in enumerate(show):
        ax2.bar(np.arange(len(classes)) + (j - (len(show) - 1) / 2) * width,
                [class_loss[n][k] for k in classes], width, label=n)
    ax2.set_xticks(np.arange(len(classes)), [k.replace("_", "\n") for k in classes], fontsize=8)
    ax2.set(ylabel="fraction of ancestral families lost", title="What is lost, by function")
    ax2.legend(fontsize=7)
    fig.tight_layout()
    fig.savefig(out / "fig_plasmodium_ancestor.png", dpi=130)

    (out / "metrics.json").write_text(json.dumps({
        "tree": str(TREE),
        "ancestor_families_without_plasmodium": int(had.sum()),
        "ancestor_families_with_plasmodium": int((anc_full > 0).sum()),
        "plasmodium_families": int((target > 0).sum()),
        "plasmodium_lost_from_ancestor": int(lost.sum()),
        "auroc_which_families_lost": results,
        "projected_family_count": projections,
        "fraction_lost_by_class": class_loss,
    }, indent=2))
    print(f"Done -> {out}/")


if __name__ == "__main__":
    main()
