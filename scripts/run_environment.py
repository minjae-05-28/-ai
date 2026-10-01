"""Environment laws for bacteria and archaea, and a Mars forecast.

    python scripts/run_environment.py [--epochs 300]

1. Law: the gene-family birth-death model with an environment design
   (base, colder, saltier, anaerobic, radiation_resistant, oligotrophic), one pair per
   ordinary relative -> extremophile.
2. Validation, leave-one-pair-out: which families does a held-out extremophile lose?
   The environment law is compared with the same model without environment axes (base
   only), copy number alone, and each family's loss rate in the other pairs.
3. Mars: an ordinary soil bacterium moved to a Mars-like niche (0 C perchlorate brine, no
   oxygen, radiation, little carbon). The axes are added (the eukaryote laws were
   additive); pair intercepts are predicted from the environment by least squares.
   Output: families most likely lost, expanded and gained, and their functions.

Scope: this predicts how *Earth* life would change under Mars conditions, extrapolated
from Earth extremophiles. It says nothing about life that arose on Mars.
"""

import argparse
import json
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import torch

from organelle_evo.eukaryotes.features import enriched_features
from organelle_evo.eukaryotes.model import counts, family_features, fit_bd, fit_bd_bootstrap, loss_probability, offset_for_losses
from organelle_evo.laws import LAWS_DIR, save_law
from organelle_evo.predict import auroc
from organelle_evo.prokaryotes.catalog import AXES, MARS, SPECIES, design, env_change, resolve_pairs

DATA = Path("data/prokaryotes")
ANN = Path("data/eukaryotes")
LABELS = ("base", *AXES)
ANCESTORS = ("Bacillus subtilis", "Shewanella oneidensis", "Pseudomonas putida")


def load():
    meta = json.loads((ANN / "pfam_meta.json").read_text())
    ann = json.loads((ANN / "family_annotations.json").read_text())
    profiles = {}
    for f in DATA.glob("*.json"):
        d = json.loads(f.read_text())
        profiles[d["species"]] = d
    fams, _ = family_features(list(profiles.values()), meta)
    c = {s: counts(p, fams) for s, p in profiles.items()}
    fams, names, x = enriched_features(profiles, meta, ann, c, free=list(profiles))
    return profiles, meta, fams, names, x, c


def heldout_losses(law, train_designs, z, n, x, n_lost):
    wl, wm, _ = law.weights(z)
    a_lam = float(np.mean(law.a_lam))
    return loss_probability(n, x, wl, wm, a_lam, offset_for_losses(n, x, wl, wm, a_lam, n_lost))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--epochs", type=int, default=300)
    ap.add_argument("--n-boot", type=int, default=4)
    ap.add_argument("--threads", type=int, default=4)
    ap.add_argument("--out", default="results/environment")
    args = ap.parse_args()
    torch.set_num_threads(args.threads)
    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)

    profiles, meta, fams, names, x, c = load()
    pairs = resolve_pairs(profiles)
    data = [(c[a], c[d], design(a, d)) for a, d in pairs]
    print(f"{len(profiles)} prokaryotes, {len(pairs)} pairs, {len(fams)} families, {x.shape[1]} features")

    # 2. Leave-one-pair-out
    rows = []
    for i, ((a, d), (n, m, z)) in enumerate(zip(pairs, data)):
        if not any(z[1:]) or max(abs(v) for v in z[1:]) < 0.25:
            continue  # controls carry no environment change to predict
        train = [p for j, p in enumerate(data) if j != i]
        env = fit_bd(x, train, LABELS, epochs=args.epochs)
        base = fit_bd(x, [(tn, tm, (1.0,)) for tn, tm, _ in train], ("base",), epochs=args.epochs)
        had = n > 0
        lost = (m == 0)[had]
        idx = np.flatnonzero(had)
        freq = np.array([np.mean([tm[j] == 0 for tn, tm, _ in train if tn[j] > 0])
                         if any(tn[j] > 0 for tn, _, _ in train) else 0.5 for j in idx])
        row = {"pair": f"{a} -> {d}", "design": list(z),
               "copies_only": auroc(-n[had].astype(float), lost),
               "memorisation": auroc(freq, lost),
               "no_environment": auroc(heldout_losses(base, None, (1.0,), n[had], x[had], lost.sum()), lost),
               "environment_law": auroc(heldout_losses(env, None, z, n[had], x[had], lost.sum()), lost)}
        rows.append(row)
        print(f"  {d:32s} copies {row['copies_only']:.3f}  no env {row['no_environment']:.3f}  "
              f"env law {row['environment_law']:.3f}  memorisation {row['memorisation']:.3f}", flush=True)
    keys = ("copies_only", "no_environment", "environment_law", "memorisation")
    mean = {k: float(np.mean([r[k] for r in rows])) for k in keys}
    gain = np.array([r["environment_law"] - r["no_environment"] for r in rows])
    print("leave-one-pair-out mean AUROC: " + ", ".join(f"{k}={v:.3f}" for k, v in mean.items()))
    print(f"environment axes vs none: {gain.mean():+.3f} (better in {(gain > 0).sum()}/{len(gain)})")

    # 1. Full law with bootstrap intervals
    law = fit_bd_bootstrap(x, data, LABELS, n_boot=args.n_boot, epochs=args.epochs)
    effects = {}
    for kind, W, SE in (("loss", law.w_mu, law.se["mu"]), ("duplication", law.w_lam, law.se["lam"]),
                        ("gain", law.w_nu, law.se["nu"])):
        for r, lab in enumerate(LABELS[1:], start=1):
            sig = [(names[j], round(float(W[r, j]), 3), round(float(SE[r, j]), 3)) for j in range(len(names))
                   if abs(W[r, j]) > 1.96 * SE[r, j]]
            effects[f"{kind}_{lab}"] = sorted(sig, key=lambda t: -abs(t[1]))[:10]
    for lab in AXES:
        print(f"  loss {lab}: " + ", ".join(f"{n_}={w:+.2f}" for n_, w, _ in effects[f'loss_{lab}'][:5]))

    # 3. Mars: intercepts from the environment, axes added
    Z = np.array([z for _, _, z in data])
    coef = {k: np.linalg.lstsq(Z, getattr(law, f"a_{k}"), rcond=None)[0] for k in ("lam", "mu", "nu")}
    fam_desc = lambda j: f"{fams[j]}: {meta.get(fams[j], {}).get('description', '')}"  # noqa: E731
    cats = [k for k, nm in enumerate(names) if nm.startswith(("go:", "kw:"))]

    def enrich(sel, weights=None):
        fr = X_cat[sel].mean(0) if weights is None else (X_cat[sel] * weights[:, None]).sum(0) / weights.sum()
        ratio = (fr + 0.01) / (X_cat.mean(0) + 0.01)
        return [(names[cats[k]], round(float(ratio[k]), 2)) for k in np.argsort(-ratio)[:6] if fr[k] >= 0.05]

    X_cat = x[:, cats]
    mars = {}
    for anc in ANCESTORS:
        if anc not in c:
            continue
        z = env_change(SPECIES[anc], MARS)
        wl, wm, wn = law.weights(z)
        a = {k: float(np.dot(z, coef[k])) for k in coef}
        n = c[anc]
        had = n > 0
        p_loss = np.zeros(len(fams))
        p_loss[had] = loss_probability(n[had], x[had], wl, wm, a["lam"], a["mu"])
        growth = np.exp(np.exp(a["lam"] + x @ wl) - np.exp(a["mu"] + x @ wm))  # E[m] / n
        p_gain = 1 - np.exp(-np.exp(a["nu"] + x @ wn))
        pool = (~had) & (np.array([sum(c[s][j] > 0 for s in c) for j in range(len(fams))]) >= 2)
        exp_lost = float(p_loss[had].sum())
        exp_gained = float(p_gain[pool].sum())
        lost_top = np.argsort(-p_loss * had)[:12]
        grow_top = np.argsort(-(growth * had * (1 - p_loss)))[:12]
        gain_top = np.argsort(-(p_gain * pool))[:12]
        mars[anc] = {
            "design": dict(zip(LABELS, map(float, z))),
            "families_today": int(had.sum()),
            "expected_lost": exp_lost, "expected_gained": exp_gained,
            "expected_families_on_mars": float(had.sum() - exp_lost + exp_gained),
            "most_likely_lost": [fam_desc(j) for j in lost_top],
            "lost_functions": enrich(np.flatnonzero(had), p_loss[had]),
            "most_expanded": [fam_desc(j) for j in grow_top],
            "expanded_functions": enrich(grow_top),
            "most_likely_gained": [fam_desc(j) for j in gain_top],
            "gained_functions": enrich(gain_top),
        }
        print(f"\n  Mars <- {anc}: {had.sum()} families today, ~{exp_lost:.0f} lost, ~{exp_gained:.0f} gained")
        print("    lost: " + "; ".join(mars[anc]["most_likely_lost"][:5]))
        print("    expanded: " + "; ".join(mars[anc]["most_expanded"][:5]))
        print("    gained: " + "; ".join(mars[anc]["most_likely_gained"][:5]))

    (out / "metrics.json").write_text(json.dumps(
        {"pairs": [f"{a} -> {d}" for a, d in pairs], "designs": {d: list(z) for (a, d), (_, _, z) in zip(pairs, data)},
         "mean_heldout_auroc": mean, "env_vs_none": {"mean": float(gain.mean()), "n_better": int((gain > 0).sum()),
                                                     "n": len(gain)},
         "heldout": rows, "significant_effects": effects, "mars": mars}, indent=2))
    save_law(
        LAWS_DIR / "environment_v1.json",
        id="environment_v1",
        scope=("Gene-family loss, duplication and gain in bacteria and archaea when a lineage moves to a "
               "colder, saltier, anoxic, radiation-exposed or nutrient-poor environment."),
        model="Linear birth-death per family; log rate = a_pair + x @ (environment change @ W).",
        feature_names=names,
        data={"pairs": [f"{a} -> {d}" for a, d in pairs], "n_families": len(fams)},
        validation={"leave_one_pair_out_auroc": mean, "env_vs_none": float(gain.mean())},
        caveats=["Environment optima are approximate literature values.",
                 "Few pairs per axis (radiation 4, oligotrophy 2, anoxia 4); wide intervals.",
                 "Mars forecast adds axes beyond any single observed environment (extrapolation)."],
        contexts={
            f"{kind}_{lab}": {f: {"weight": round(float(W[r, j]), 4),
                                  "ci95": [round(float(W[r, j] - 1.96 * SE[r, j]), 4),
                                           round(float(W[r, j] + 1.96 * SE[r, j]), 4)]}
                              for j, f in enumerate(names)}
            for kind, W, SE in (("loss", law.w_mu, law.se["mu"]), ("duplication", law.w_lam, law.se["lam"]),
                                ("gain", law.w_nu, law.se["nu"]))
            for r, lab in enumerate(LABELS)
        },
        mars=mars,
    )

    fig, ax = plt.subplots(figsize=(8, 4))
    labels = ["copies only", "law, no environment", "environment law", "memorisation"]
    ax.bar(labels, [mean[k] for k in keys], color=["#b0b0b0", "#8d99ae", "#e76f51", "#264653"])
    for i, k in enumerate(keys):
        ax.text(i, mean[k] + 0.004, f"{mean[k]:.3f}", ha="center")
    ax.set(ylim=(0.5, max(mean.values()) + 0.05), ylabel=f"mean AUROC ({len(rows)} held-out extremophiles)",
           title="Which families does an extremophile lose?")
    fig.tight_layout()
    fig.savefig(out / "fig_environment.png", dpi=130)
    print(f"Done -> {out}/ and laws/environment_v1.json")


if __name__ == "__main__":
    main()
