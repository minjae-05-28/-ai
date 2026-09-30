"""Reverse the laws: reconstruct the ancestors of modern parasites from their genomes.

    python scripts/run_reverse.py [--out results/reverse]

1. Leave-one-out validation over the 14 parasite pairs: the ancestor is inferred from
   the parasite genome alone (the law is refitted without that pair; the prior uses
   free-living species from *other* groups) and scored against the free-living
   relative that stands in for the true ancestor.
2. Several law mixes compete: prior only, the axis law, the axis law blended with each
   stored endosymbiosis law, an endosymbiosis law alone, and a wrong-lifestyle control.
3. The best mix is stored as laws/composite_v1.json and used to reconstruct the
   ancestors of every parasite.
"""

import argparse
import json
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import torch

from organelle_evo.eukaryotes.catalog import AXES, FREE, SPECIES, design, resolve_pairs
from organelle_evo.eukaryotes.model import FAMILY_FEATURES, counts, family_features, fit_bd, pfam_class
from organelle_evo.eukaryotes.reverse import count_prior, reconstruct
from organelle_evo.laws import LAWS_DIR, load_law, save_law
from organelle_evo.predict import auroc

DATA = Path("data/eukaryotes")
LABELS = ("base", *AXES)
FREE_DESIGN = (1.0, 0.0, 0.0, 0.0)

# name -> (weight on the axis law, endosymbiosis context or None, weight on it, design override)
MIXES = {
    "prior only (no law)": (0.0, None, 0.0, None),
    "axis law": (1.0, None, 0.0, None),
    "axis + mitochondrion law": (0.5, "mitochondrion", 0.5, None),
    "axis + plastid law": (0.5, "plastid", 0.5, None),
    "axis + insect-endosymbiont law": (0.5, "insect_endosymbiont", 0.5, None),
    "plastid law only": (0.0, "plastid", 1.0, None),
    "axis law, wrong lifestyle (free-living)": (1.0, None, 0.0, FREE_DESIGN),
}


def mixed_weights(fit, z, mix, endo):
    a, ctx, e, override = mix
    wl, wm, wn = fit.weights(override or z)
    wm = a * wm + (e * endo.weights[ctx] if ctx else 0.0)
    return a * wl, wm, a * wn


def references(profiles, c, exclude_group):
    refs = [c[s] for s in profiles if SPECIES[s].lifestyle == FREE and SPECIES[s].group != exclude_group]
    return np.array(refs)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--epochs", type=int, default=300)
    ap.add_argument("--out", default="results/reverse")
    args = ap.parse_args()
    torch.set_num_threads(4)
    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)

    meta = json.loads((DATA / "pfam_meta.json").read_text())
    profiles = {}
    for f in DATA.glob("*.json"):
        if f.name != "pfam_meta.json":
            d = json.loads(f.read_text())
            profiles[d["species"]] = d
    fams, x = family_features([profiles[s] for s in profiles], meta)
    c = {s: counts(p, fams) for s, p in profiles.items()}
    pairs = resolve_pairs(profiles)
    data = [(c[a], c[d], design(d)) for a, d in pairs]
    endo = load_law("endosymbiosis_v1")
    parasite_idx = [i for i, (_, _, z) in enumerate(data) if z[1]]
    print(f"{len(fams)} families, {len(parasite_idx)} parasite pairs")

    # 1-2. Leave-one-out validation of the mixes
    scores = {name: [] for name in MIXES}
    per_pair = []
    for i in parasite_idx:
        anc, desc = pairs[i]
        _, m, z = data[i]
        fit = fit_bd(x, data[:i] + data[i + 1:], LABELS, epochs=args.epochs)
        prior = count_prior(references(profiles, c, SPECIES[desc].group))
        truth = c[anc] > 0
        absent = m == 0
        row = {"pair": f"{anc} -> {desc}", "proxy_families": int(truth.sum()),
               "descendant_families": int((m > 0).sum()), "mixes": {}}
        for name, mix in MIXES.items():
            wl, wm, wn = mixed_weights(fit, z, mix, endo)
            r = reconstruct(m, x, wl, wm, wn, prior)
            s = {"auroc_recover_lost": auroc(r.p_present[absent], truth[absent]),
                 "estimated_families": float(r.p_present.sum())}
            scores[name].append(s["auroc_recover_lost"])
            row["mixes"][name] = s
        per_pair.append(row)
        print(f"  {desc:30s} " + "  ".join(f"{k.split(' (')[0][:18]}={v['auroc_recover_lost']:.3f}"
                                            for k, v in row["mixes"].items()))
    mean = {k: float(np.mean(v)) for k, v in scores.items()}
    best = max(mean, key=mean.get)
    print("mean AUROC (recovering lost families): " + ", ".join(f"{k}={v:.3f}" for k, v in mean.items()))
    print(f"best mix: {best}")

    # 3. Composite law from all pairs; reconstruct every parasite's ancestor
    fit = fit_bd(x, data, LABELS, epochs=args.epochs)
    mix = MIXES[best]
    recon = {}
    for i in parasite_idx:
        anc, desc = pairs[i]
        _, m, z = data[i]
        prior = count_prior(references(profiles, c, SPECIES[desc].group))
        wl, wm, wn = mixed_weights(fit, z, mix, endo)
        r = reconstruct(m, x, wl, wm, wn, prior)
        absent = m == 0
        recovered = np.argsort(-(r.p_present * absent))[:8]
        by_class = {}
        for j, cls in enumerate(FAMILY_FEATURES):
            if j >= 3:
                sel = x[:, j] == 1
                by_class[cls] = {"ancestor": float(r.p_present[sel].sum()), "today": int((m[sel] > 0).sum())}
        recon[desc] = {
            "proxy": anc,
            "families_today": int((m > 0).sum()),
            "estimated_ancestor_families": float(r.p_present.sum()),
            "proxy_families": int((c[anc] > 0).sum()),
            "estimated_lost": float((r.p_present * absent).sum()),
            "top_recovered": [
                {"family": fams[k], "description": meta.get(fams[k], {}).get("description", ""),
                 "class": pfam_class(fams[k], meta.get(fams[k], {}).get("description", "")),
                 "p_ancestral": float(r.p_present[k])} for k in recovered
            ],
            "by_class": by_class,
        }
        print(f"  {desc:30s} today {recon[desc]['families_today']:5d}  ancestor ≈ "
              f"{recon[desc]['estimated_ancestor_families']:.0f}  (proxy {anc}: {recon[desc]['proxy_families']})")

    a, ctx, e, _ = mix
    contexts = {}
    for label, z in [("parasite_extracellular_aerobic", (1, 1, 0, 0)), ("parasite_extracellular_reduced", (1, 1, 0, 1)),
                     ("parasite_intracellular_aerobic", (1, 1, 1, 0)), ("parasite_intracellular_reduced", (1, 1, 1, 1)),
                     ("free_living", FREE_DESIGN)]:
        _, wm, _ = mixed_weights(fit, z, mix, endo)
        contexts[f"loss_{label}"] = {f: {"weight": round(float(w), 4), "ci95": [round(float(w), 4)] * 2}
                                     for f, w in zip(FAMILY_FEATURES, wm)}
    save_law(
        LAWS_DIR / "composite_v1.json",
        id="composite_v1",
        scope=("Composite loss law for reconstructing ancestors of eukaryotic parasites from their "
               "genomes (reverse inference). Chosen by leave-one-out validation among law mixes."),
        model=(f"loss weights = {a} x eukaryote_axes law(design)"
               + (f" + {e} x endosymbiosis_v1[{ctx}]" if ctx else "")
               + "; used inside a Bayesian reverse birth-death reconstruction."),
        feature_names=list(FAMILY_FEATURES),
        components={"eukaryote_axes": a, "endosymbiosis_context": ctx, "endosymbiosis_weight": e},
        validation={"mean_auroc_recover_lost": mean, "best": best},
        caveats=["Point weights only (no intervals): a mix of separately fitted laws.",
                 "Validated against extant free-living relatives, not true ancestors."],
        contexts=contexts,
    )

    (out / "metrics.json").write_text(json.dumps(
        {"mixes": list(MIXES), "mean_auroc_recover_lost": mean, "best_mix": best,
         "per_pair": per_pair, "reconstructions": recon}, indent=2))

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 5), gridspec_kw={"width_ratios": [1, 1.2]})
    items = sorted(mean.items(), key=lambda kv: kv[1])
    ax1.barh([k for k, _ in items], [v for _, v in items],
             color=["#e76f51" if k == best else "#8d99ae" for k, _ in items])
    ax1.set(xlim=(0.5, max(mean.values()) + 0.05), xlabel="mean AUROC: recovering families the ancestor had",
            title="Which law mix reconstructs ancestors best?")
    ax1.tick_params(axis="y", labelsize=8)
    names = list(recon)
    yy = np.arange(len(names))
    ax2.barh(yy - 0.25, [recon[n]["families_today"] for n in names], 0.25, label="today", color="#b0b0b0")
    ax2.barh(yy, [recon[n]["estimated_ancestor_families"] for n in names], 0.25, label="reconstructed ancestor",
             color="#e76f51")
    ax2.barh(yy + 0.25, [recon[n]["proxy_families"] for n in names], 0.25, label="free-living relative",
             color="#2a9d8f")
    ax2.set_yticks(yy, names, fontsize=7)
    ax2.set(xlabel="Pfam families", title="Modern parasites and their reconstructed ancestors")
    ax2.legend(fontsize=8)
    fig.tight_layout()
    fig.savefig(out / "fig_reverse.png", dpi=130)
    print(f"Done -> {out}/ and laws/composite_v1.json")


if __name__ == "__main__":
    main()
