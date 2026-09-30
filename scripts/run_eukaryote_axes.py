"""Split laws: base + parasite + intracellular + reduced-mitochondria effects.

    python scripts/run_eukaryote_axes.py [--n-boot 10] [--out results/eukaryote_axes]

Questions:
1. Do the axes explain gene-family evolution better than one parasite switch? (AIC)
2. Do split laws predict a held-out parasite's losses better than the lumped law?
3. The Plasmodium ancestor again: rebuilt with its free-living relatives (Chromera,
   Vitrella) and evolved under every combination of axes. Does the law matching
   Plasmodium's real biology (intracellular, aerobic) fit best?
The stored laws in laws/ are compared with and scored as references only.
"""

import argparse
import json
from itertools import product
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import torch

from organelle_evo.eukaryotes.ancestral import prune, wagner_ancestor
from organelle_evo.eukaryotes.birthdeath import simulate
from organelle_evo.eukaryotes.catalog import AXES, SPECIES, design, resolve_pairs
from organelle_evo.eukaryotes.model import (
    FAMILY_FEATURES,
    counts,
    family_features,
    fit_bd,
    fit_bd_bootstrap,
    loss_probability,
    offset_for_losses,
)
from organelle_evo.laws import LAWS_DIR, load_law, save_law
from organelle_evo.predict import auroc

DATA = Path("data/eukaryotes")
LABELS = ("base", *AXES)
PLASMO = "Plasmodium falciparum"
# Rooted at the ancestor of apicomplexans + chromerids (Plasmodium's closest free-living kin).
ALVEOLATE_TREE_AT_ANCESTOR = (
    (((PLASMO, "Babesia bovis"), ("Toxoplasma gondii", "Eimeria tenella")), "Cryptosporidium parvum"),
    ("Chromera velia", "Vitrella brassicaformis"),
    ("Perkinsus marinus", ("Tetrahymena thermophila", "Ichthyophthirius multifiliis")),
)


def lumped(z):
    return (1.0, z[1], 0.0, 0.0)  # base + parasite only


def predict_losses(law, train, z, n, x, n_lost):
    """P(lost) for families with n > 0 under design z; offsets from similar training pairs."""
    wl, wm, _ = law.weights(z)
    same = [i for i, (_, _, zi) in enumerate(train) if zi[1] == z[1]] or list(range(len(train)))
    a_lam = law.a_lam[same].mean()
    a_mu = offset_for_losses(n, x, wl, wm, a_lam, n_lost)
    return loss_probability(n, x, wl, wm, a_lam, a_mu)


def class_fraction(p, x):
    return {c: float(p[x[:, i] == 1].mean()) if (x[:, i] == 1).any() else float("nan")
            for i, c in enumerate(FAMILY_FEATURES) if i >= 3}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--n-boot", type=int, default=10)
    ap.add_argument("--epochs", type=int, default=400)
    ap.add_argument("--out", default="results/eukaryote_axes")
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
    pairs = resolve_pairs(profiles)
    fams, x = family_features([profiles[s] for s in profiles], meta)
    c = {s: counts(p, fams) for s, p in profiles.items()}
    data = [(c[a], c[d], design(d)) for a, d in pairs]
    print(f"{len(profiles)} species, {len(pairs)} pairs, {len(fams)} families; "
          f"missing: {sorted(set(SPECIES) - set(profiles))}")
    for (a, d), (_, _, z) in zip(pairs, data):
        print(f"  {a:26s} -> {d:30s} parasite={int(z[1])} intracellular={int(z[2])} reduced={int(z[3])}")

    # 1. Model comparison
    fits = {
        "shared": fit_bd(x, [(n, m, (1.0, 0, 0, 0)) for n, m, _ in data], LABELS, epochs=args.epochs),
        "parasite_only": fit_bd(x, [(n, m, lumped(z)) for n, m, z in data], LABELS, epochs=args.epochs),
        "axes": fit_bd_bootstrap(x, data, LABELS, n_boot=args.n_boot, epochs=args.epochs),
    }
    aic = {k: 2 * f.nll + 2 * f.n_params for k, f in fits.items()}
    print("AIC relative to best: " + ", ".join(f"{k}={v - min(aic.values()):.1f}" for k, v in aic.items()))
    law = fits["axes"]

    # 2. Held-out parasites: split vs lumped law
    heldout = []
    for i, ((a, d), (n, m, z)) in enumerate(zip(pairs, data)):
        if not z[1]:
            continue
        train = data[:i] + data[i + 1:]
        had = n > 0
        lost = (m == 0)[had]
        f_axes = fit_bd(x, train, LABELS, epochs=args.epochs)
        f_lump = fit_bd(x, [(tn, tm, lumped(tz)) for tn, tm, tz in train], LABELS, epochs=args.epochs)
        row = {
            "pair": f"{a} -> {d}",
            "design": dict(zip(AXES, map(int, z[1:]))),
            "copies_only": auroc(-n[had].astype(float), lost),
            "lumped_parasite_law": auroc(predict_losses(f_lump, train, lumped(z), n[had], x[had], lost.sum()), lost),
            "split_law": auroc(predict_losses(f_axes, train, z, n[had], x[had], lost.sum()), lost),
        }
        heldout.append(row)
        print(f"  held-out {d:30s} copies {row['copies_only']:.3f}  lumped {row['lumped_parasite_law']:.3f}  "
              f"split {row['split_law']:.3f}")

    # 3. Plasmodium ancestor under every axis combination
    tree = prune(ALVEOLATE_TREE_AT_ANCESTOR, {PLASMO} | (set(SPECIES) - set(profiles)))
    anc = wagner_ancestor(tree, c)
    target = c[PLASMO]
    had = anc > 0
    lost = (target == 0)[had]
    ip = next(i for i, (_, d) in enumerate(pairs) if d == PLASMO)
    train = data[:ip] + data[ip + 1:]
    f_axes = fit_bd(x, train, LABELS, epochs=args.epochs)
    plasmo = {"ancestor_families": int(had.sum()), "lost": int(lost.sum()), "laws": {}}
    rng = np.random.default_rng(0)
    for par, intra, red in product([0, 1], repeat=3):
        if not par and intra:
            continue  # "free-living but intracellular" is not a lifestyle
        z = (1.0, float(par), float(intra), float(red))
        name = ("parasite" if par else "free-living") + (", intracellular" if intra else "") + \
               (", reduced mito" if red else ", aerobic")
        p = predict_losses(f_axes, train, z, anc[had], x[had], lost.sum())
        wl, wm, wn = f_axes.weights(z)
        same = [j for j, (_, _, zj) in enumerate(train) if zj[1] == z[1]]
        sims = simulate(np.tile(anc, (100, 1)), f_axes.a_lam[same].mean() + x @ wl,
                        f_axes.a_mu[same].mean() + x @ wm, f_axes.a_nu[same].mean() + x @ wn,
                        n_steps=100, rng=rng)
        plasmo["laws"][name] = {
            "auroc": auroc(p, lost),
            "fraction_lost_by_class": class_fraction(p, x[had]),
            "projected_families_kept": float(((sims > 0) & (anc > 0)).sum(1).mean()),
            "matches_plasmodium_biology": bool(par and intra and not red),
        }
    ref = load_law("endosymbiosis_v1")
    for ctx in ref.weights:
        base = x[had] @ ref.weights[ctx]
        n_h = anc[had]
        lo, hi = -15.0, 10.0
        for _ in range(60):
            mid = (lo + hi) / 2
            val = ((-np.expm1(-np.exp(mid + base))) ** n_h).sum()
            lo, hi = (mid, hi) if val < lost.sum() else (lo, mid)
        p = (-np.expm1(-np.exp((lo + hi) / 2 + base))) ** n_h
        plasmo["laws"][f"reference: endosymbiosis ({ctx})"] = {
            "auroc": auroc(p, lost), "fraction_lost_by_class": class_fraction(p, x[had])}
    plasmo["actual_fraction_lost_by_class"] = class_fraction(lost.astype(float), x[had])
    plasmo["actual_families_kept"] = int((~lost).sum())
    print(f"Plasmodium ancestor: {had.sum()} families, lost {lost.sum()}")
    for k, v in plasmo["laws"].items():
        print(f"  {k:48s} AUROC {v['auroc']:.3f}" + ("  <- Plasmodium's biology" if v.get("matches_plasmodium_biology") else ""))

    # 4. Save law, metrics, figure
    def table(w, se):
        return {lab: {f: {"weight": float(w[r, j]), "se": float(se[r, j])} for j, f in enumerate(FAMILY_FEATURES)}
                for r, lab in enumerate(LABELS)}

    metrics = {
        "pairs": [f"{a} -> {d}" for a, d in pairs],
        "n_families": len(fams),
        "aic_relative": {k: v - min(aic.values()) for k, v in aic.items()},
        "loss_effects": table(law.w_mu, law.se["mu"]),
        "duplication_effects": table(law.w_lam, law.se["lam"]),
        "heldout_parasites": heldout,
        "plasmodium_ancestor": plasmo,
    }
    (out / "metrics.json").write_text(json.dumps(metrics, indent=2))
    save_law(
        LAWS_DIR / "eukaryote_axes_v1.json",
        id="eukaryote_axes_v1",
        scope=("Gene-family (Pfam) loss and duplication in eukaryotes, split into a base law plus "
               "the additive effects of parasitism, intracellular life and reduced mitochondria."),
        model=("Linear birth-death per family with origination; log rate = a_pair + x @ (design @ W), "
               "design = [1, parasite, intracellular, reduced_mitochondria]."),
        feature_names=list(FAMILY_FEATURES),
        data={"pairs": metrics["pairs"], "n_families": len(fams)},
        caveats=["Extant free-living relatives stand in for ancestors.",
                 "Few pairs per axis; bootstrap over pairs.",
                 "Axis labels are coarse summaries of each species' biology."],
        contexts={
            f"{kind}_{lab}": {f: {"weight": round(float(w[r, j]), 4),
                                  "ci95": [round(float(w[r, j] - 1.96 * se[r, j]), 4),
                                           round(float(w[r, j] + 1.96 * se[r, j]), 4)]}
                              for j, f in enumerate(FAMILY_FEATURES)}
            for kind, w, se in [("loss", law.w_mu, law.se["mu"]), ("duplication", law.w_lam, law.se["lam"])]
            for r, lab in enumerate(LABELS)
        },
    )

    fig, axes_ = plt.subplots(1, 3, figsize=(18, 5), gridspec_kw={"width_ratios": [1.4, 1, 1.2]})
    ax = axes_[0]
    xs = np.arange(len(FAMILY_FEATURES))
    colors = ["#8d99ae", "#e76f51", "#6d597a", "#2a9d8f"]
    for r, lab in enumerate(LABELS):
        ax.bar(xs + (r - 1.5) * 0.2, law.w_mu[r], 0.2, yerr=1.96 * law.se["mu"][r], capsize=1.5,
               color=colors[r], label=lab if r == 0 else f"+ {lab}")
    ax.axhline(0, color="k", lw=0.6)
    ax.set_xticks(xs, [f.replace("_", "\n") for f in FAMILY_FEATURES], fontsize=7)
    ax.set(ylabel="effect on log loss rate (+ = lost faster)", title="Loss law, split by axis")
    ax.legend(fontsize=8)
    ax = axes_[1]
    names = [r["pair"].split(" -> ")[1] for r in heldout]
    yy = np.arange(len(heldout))
    ax.scatter([r["lumped_parasite_law"] for r in heldout], yy, label="lumped parasite law", color="#b0b0b0")
    ax.scatter([r["split_law"] for r in heldout], yy, label="split law", color="#e76f51")
    ax.set_yticks(yy, names, fontsize=7)
    ax.set(xlabel="AUROC (held out)", title="Predicting a new parasite's losses")
    ax.legend(fontsize=8)
    ax = axes_[2]
    items = sorted(plasmo["laws"].items(), key=lambda kv: kv[1]["auroc"])
    ax.barh([k for k, _ in items], [v["auroc"] for _, v in items],
            color=["#e76f51" if v.get("matches_plasmodium_biology") else
                   ("#b0b0b0" if k.startswith("reference") else "#8d99ae") for k, v in items])
    ax.set(xlim=(0.5, max(v["auroc"] for _, v in items) + 0.05),
           xlabel="AUROC: which ancestral families Plasmodium lost", title="Plasmodium ancestor, by law")
    ax.tick_params(axis="y", labelsize=7)
    fig.tight_layout()
    fig.savefig(out / "fig_eukaryote_axes.png", dpi=130)
    print(f"Done -> {out}/ and laws/eukaryote_axes_v1.json")


if __name__ == "__main__":
    main()
