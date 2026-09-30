"""Does describing gene families better make the laws predictive?

    python scripts/run_features.py [--folds 5] [--out results/features]

Same 5-fold split over parasite pairs for every arm:
  base      the 8 original features
  enriched  + GO-slim functions, Pfam clans, HMM length, ubiquity, typical copy number
Baselines: copy number only, and each family's loss frequency in the training parasites
(memorisation, the strongest so far). The enriched law is stored as
laws/eukaryote_axes_v3.json.
"""

import argparse
import json
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import torch

from organelle_evo.eukaryotes.catalog import AXES, design, resolve_pairs
from organelle_evo.eukaryotes.features import enriched_features
from organelle_evo.eukaryotes.model import counts, fit_bd, fit_bd_bootstrap, loss_probability, offset_for_losses
from organelle_evo.laws import LAWS_DIR, save_law
from organelle_evo.predict import auroc

DATA = Path("data/eukaryotes")
LABELS = ("base", *AXES)


def predict(law, train, z, n, x, n_lost):
    wl, wm, _ = law.weights(z)
    same = [i for i, (_, _, zi) in enumerate(train) if zi[1] == z[1]] or list(range(len(train)))
    a_lam = law.a_lam[same].mean()
    return loss_probability(n, x, wl, wm, a_lam, offset_for_losses(n, x, wl, wm, a_lam, n_lost))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--folds", type=int, default=5)
    ap.add_argument("--epochs", type=int, default=300)
    ap.add_argument("--n-boot", type=int, default=4)
    ap.add_argument("--out", default="results/features")
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
    from organelle_evo.eukaryotes.model import family_features

    fams, _ = family_features(list(profiles.values()), meta)
    c = {s: counts(p, fams) for s, p in profiles.items()}
    fams, names, x_rich = enriched_features(profiles, meta, ann, c)
    x_base = x_rich[:, :8]
    pairs = resolve_pairs(profiles)
    data = [(c[a], c[d], design(d)) for a, d in pairs]
    print(f"{len(profiles)} species, {len(pairs)} pairs, {len(fams)} families, "
          f"{x_rich.shape[1]} enriched features ({x_rich.shape[1] - 8} new)")

    parasites = [i for i, (_, _, z) in enumerate(data) if z[1]]
    order = np.random.default_rng(0).permutation(parasites)
    folds = [sorted(order[k::args.folds].tolist()) for k in range(args.folds)]
    rows = []
    for k, fold in enumerate(folds):
        train = [d_ for j, d_ in enumerate(data) if j not in fold]
        laws = {arm: fit_bd(x, train, LABELS, epochs=args.epochs) for arm, x in (("base", x_base), ("enriched", x_rich))}
        train_par = [(n, m) for n, m, z in train if z[1]]
        for i in fold:
            (a, d), (n, m, z) = pairs[i], data[i]
            had = n > 0
            lost = (m == 0)[had]
            idx = np.flatnonzero(had)
            freq = np.array([np.mean([tm[j] == 0 for tn, tm in train_par if tn[j] > 0])
                             if any(tn[j] > 0 for tn, _ in train_par) else 0.5 for j in idx])
            row = {"pair": f"{a} -> {d}",
                   "copies_only": auroc(-n[had].astype(float), lost),
                   "memorisation": auroc(freq, lost)}
            for arm, x in (("base", x_base), ("enriched", x_rich)):
                row[arm] = auroc(predict(laws[arm], train, z, n[had], x[had], lost.sum()), lost)
            rows.append(row)
            print(f"  fold {k} {d:32s} copies {row['copies_only']:.3f}  base {row['base']:.3f}  "
                  f"enriched {row['enriched']:.3f}  memorisation {row['memorisation']:.3f}")
    mean = {k: float(np.mean([r[k] for r in rows])) for k in ("copies_only", "base", "enriched", "memorisation")}
    print("mean held-out AUROC: " + ", ".join(f"{k}={v:.3f}" for k, v in mean.items()))

    law = fit_bd_bootstrap(x_rich, data, LABELS, n_boot=args.n_boot, epochs=args.epochs)
    effects = {}
    for r, lab in enumerate(LABELS):
        w, se = law.w_mu[r], law.se["mu"][r]
        sig = [(names[j], float(w[j]), float(se[j])) for j in range(len(names)) if abs(w[j]) > 1.96 * se[j]]
        effects[lab] = sorted(sig, key=lambda t: -abs(t[1]))[:12]
        print(f"  {lab}: " + ", ".join(f"{n_}={w_:+.2f}" for n_, w_, _ in effects[lab][:6]))

    save_law(
        LAWS_DIR / "eukaryote_axes_v3.json",
        id="eukaryote_axes_v3",
        scope=("Gene-family loss and duplication in eukaryotes (base law + parasite / intracellular / "
               "reduced-mitochondria effects), with families described by GO-slim functions, Pfam clans "
               "and cross-species statistics."),
        model="Linear birth-death per family; log rate = a_pair + x @ (design @ W), enriched x.",
        feature_names=names,
        data={"pairs": [f"{a} -> {d}" for a, d in pairs], "n_families": len(fams)},
        validation={"folds": args.folds, "mean_heldout_auroc": mean},
        caveats=["Ubiquity and copy-number features are computed from free-living species.",
                 "Families never observed in the first 32 species are not counted in later ones."],
        contexts={
            f"{kind}_{lab}": {f: {"weight": round(float(w[r, j]), 4),
                                  "ci95": [round(float(w[r, j] - 1.96 * se[r, j]), 4),
                                           round(float(w[r, j] + 1.96 * se[r, j]), 4)]}
                              for j, f in enumerate(names)}
            for kind, w, se in [("loss", law.w_mu, law.se["mu"]), ("duplication", law.w_lam, law.se["lam"])]
            for r, lab in enumerate(LABELS)
        },
    )
    (out / "metrics.json").write_text(json.dumps(
        {"n_features": {"base": 8, "enriched": len(names)}, "feature_names": names,
         "mean_heldout_auroc": mean, "heldout": rows, "significant_loss_effects": effects}, indent=2))

    fig, ax = plt.subplots(figsize=(8, 4.5))
    keys = ["copies_only", "base", "enriched", "memorisation"]
    labels = ["copies only", "base law (8 features)", f"enriched law ({len(names)})", "memorisation"]
    ax.bar(labels, [mean[k] for k in keys], color=["#b0b0b0", "#8d99ae", "#e76f51", "#264653"])
    for i, k in enumerate(keys):
        ax.text(i, mean[k] + 0.004, f"{mean[k]:.3f}", ha="center")
    ax.set(ylim=(0.5, max(mean.values()) + 0.05), ylabel=f"mean AUROC ({len(rows)} held-out parasites)",
           title="Which families does a new parasite lose?")
    ax.tick_params(axis="x", labelsize=8)
    fig.tight_layout()
    fig.savefig(out / "fig_features.png", dpi=130)
    print(f"Done -> {out}/ and laws/eukaryote_axes_v3.json")


if __name__ == "__main__":
    main()
