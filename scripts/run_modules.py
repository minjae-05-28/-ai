"""Law search: are gene families lost in modules?

    python scripts/run_modules.py [--ks 0 2 4 8] [--reveal 0.5]

Held-out test, one clade at a time: every parasite pair of that clade is removed from
training (so shared ancestry cannot leak), the model is fit on the rest, then for each
held-out parasite half of its families' fates are revealed and the other half predicted.
k = 0 knows only how reduced the parasite is and how loss-prone each family is; k > 0
adds modules. The final model (all pairs) is interpreted by the functions of the
families at each module's two ends.
"""

import argparse
import json
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import torch

from organelle_evo.eukaryotes.catalog import SPECIES, resolve_pairs
from organelle_evo.eukaryotes.features import KEYWORD_CLASSES, enriched_features
from organelle_evo.eukaryotes.model import counts, family_features
from organelle_evo.eukaryotes.modules import fit_modules, loss_matrix, predict_hidden
from organelle_evo.laws import LAWS_DIR, save_law
from organelle_evo.predict import auroc

DATA = Path("data/eukaryotes")
MIN_ANCESTORS = 5


def clade(species: str) -> str:
    return SPECIES[species].group.split("_")[0]


def load():
    meta = json.loads((DATA / "pfam_meta.json").read_text())
    ann = json.loads((DATA / "family_annotations.json").read_text())
    profiles = {}
    for f in DATA.glob("*.json"):
        if f.name not in ("pfam_meta.json", "family_annotations.json"):
            d = json.loads(f.read_text())
            profiles[d["species"]] = d
    fams, _ = family_features(list(profiles.values()), meta)
    c = {s: counts(p, fams) for s, p in profiles.items()}
    return profiles, meta, ann, fams, c


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--ks", type=int, nargs="+", default=[0, 2, 4, 8])
    ap.add_argument("--reveal", type=float, default=0.5)
    ap.add_argument("--repeats", type=int, default=3)
    ap.add_argument("--out", default="results/modules")
    args = ap.parse_args()
    torch.set_num_threads(1)
    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)

    profiles, meta, ann, fams, c = load()
    pairs = [(a, d) for a, d in resolve_pairs(profiles) if SPECIES[d].lifestyle == "parasite"]
    L = loss_matrix(pairs, c)
    keep = (~np.isnan(L)).sum(0) >= MIN_ANCESTORS
    L, fams_k = L[:, keep], [f for f, k in zip(fams, keep) if k]
    clades = sorted({clade(d) for _, d in pairs})
    print(f"{len(pairs)} parasite pairs, {len(fams_k)} families (in >= {MIN_ANCESTORS} ancestors), "
          f"{len(clades)} clades: {', '.join(clades)}")

    rows = []
    for cl in clades:
        test = [i for i, (_, d) in enumerate(pairs) if clade(d) == cl]
        train = [i for i in range(len(pairs)) if i not in test]
        models = {k: fit_modules(L[train], k) for k in args.ks}
        for i in test:
            row = {"pair": f"{pairs[i][0]} -> {pairs[i][1]}", "clade": cl}
            for k, mdl in models.items():
                vals = []
                for r in range(args.repeats):
                    s, y = predict_hidden(mdl, L[i], args.reveal, np.random.default_rng(r))
                    vals.append(auroc(s, y))
                row[f"k{k}"] = float(np.nanmean(vals))
            rows.append(row)
            print(f"  {cl:14s} {pairs[i][1]:34s} " + "  ".join(f"k={k} {row[f'k{k}']:.3f}" for k in args.ks))
    mean = {f"k{k}": float(np.nanmean([r[f"k{k}"] for r in rows])) for k in args.ks}
    by_clade = {cl: {f"k{k}": float(np.nanmean([r[f"k{k}"] for r in rows if r["clade"] == cl])) for k in args.ks}
                for cl in clades}
    best = max(args.ks[1:], key=lambda k: mean[f"k{k}"])
    gain = np.array([r[f"k{best}"] - r["k0"] for r in rows])
    print("mean AUROC on hidden families: " + ", ".join(f"{k}={v:.3f}" for k, v in mean.items()))
    print(f"k={best} vs k=0: {gain.mean():+.3f} (better in {(gain > 0).sum()}/{len(gain)} parasites)")

    # Interpret the final model: functions at each module's ends.
    _, names, X = enriched_features(profiles, meta, ann, c)
    X = X[keep]
    cats = [j for j, n in enumerate(names) if n.startswith(("go:", "kw:"))]
    final = fit_modules(L, best)
    # Orient each module so that positive u means the module is lost.
    modules = []
    order = np.argsort(-np.abs(final.u).sum(0))
    for m in order:
        v, u = final.v[:, m], final.u[:, m]
        sign = 1.0 if (u.mean() >= 0) else -1.0
        v, u = v * sign, u * sign
        top = np.argsort(-v)[:40]
        bottom = np.argsort(v)[:40]

        def enrich(sel):
            fr, base = X[sel][:, cats].mean(0), X[:, cats].mean(0)
            ratio = (fr + 0.01) / (base + 0.01)
            return [(names[cats[j]], round(float(ratio[j]), 2)) for j in np.argsort(-ratio)[:5] if fr[j] >= 0.1]

        def label(sel):
            return [f"{fams_k[j]}: {meta.get(fams_k[j], {}).get('description', '')}" for j in sel[:8]]

        par = sorted(zip(u, [d for _, d in pairs]), reverse=True)
        modules.append({
            "strength": float(np.abs(final.u[:, m]).sum()),
            "lost_together": label(top), "lost_together_enriched": enrich(top),
            "kept_together": label(bottom), "kept_together_enriched": enrich(bottom),
            "most_affected": [d for _, d in par[:6]], "least_affected": [d for _, d in par[-6:]],
        })
        print(f"\n  module (strength {modules[-1]['strength']:.1f}); most in: {', '.join(modules[-1]['most_affected'][:4])}")
        print("    lost together: " + "; ".join(modules[-1]["lost_together"][:5]))
        print("    enriched: " + ", ".join(f"{n} x{r}" for n, r in modules[-1]["lost_together_enriched"]))

    (out / "metrics.json").write_text(json.dumps(
        {"n_pairs": len(pairs), "n_families": len(fams_k), "reveal": args.reveal, "ks": args.ks,
         "mean_auroc_hidden": mean, "by_clade": by_clade, "best_k": best,
         "gain_vs_additive": {"mean": float(gain.mean()), "n_better": int((gain > 0).sum()), "n": len(gain)},
         "heldout": rows, "modules": modules}, indent=2))

    save_law(
        LAWS_DIR / "coloss_modules_v1.json",
        id="coloss_modules_v1",
        scope="Gene-family loss in eukaryotic parasites: which families are lost together (modules).",
        model="Logistic: logit P(lost) = a_pair + b_family + u_pair . v_family, rank k.",
        feature_names=[],
        data={"pairs": [f"{a} -> {d}" for a, d in pairs], "n_families": len(fams_k)},
        validation={"scheme": "leave-one-clade-out, half of each held-out parasite's families revealed",
                    "mean_auroc_hidden": mean, "best_k": best,
                    "gain_vs_additive": float(gain.mean())},
        caveats=["Modules are statistical: co-loss can reflect shared pathways or shared host niche.",
                 "Pairs with the same ancestor proxy are not independent."],
        contexts={"modules": modules},
    )

    fig, axes = plt.subplots(1, 2, figsize=(11, 4.2))
    ks = args.ks
    axes[0].bar([f"k={k}" for k in ks], [mean[f"k{k}"] for k in ks],
                color=["#8d99ae"] + ["#e76f51"] * (len(ks) - 1))
    for i, k in enumerate(ks):
        axes[0].text(i, mean[f"k{k}"] + 0.003, f"{mean[f'k{k}']:.3f}", ha="center")
    axes[0].set(ylim=(0.5, max(mean.values()) + 0.05), ylabel="AUROC on hidden half",
                title="Knowing half the losses: do modules help?")
    x = np.arange(len(clades))
    axes[1].bar(x - 0.2, [by_clade[cl]["k0"] for cl in clades], 0.4, label="k=0 (no modules)", color="#8d99ae")
    axes[1].bar(x + 0.2, [by_clade[cl][f"k{best}"] for cl in clades], 0.4, label=f"k={best}", color="#e76f51")
    axes[1].set_xticks(x, clades, rotation=40, ha="right", fontsize=8)
    axes[1].set(ylim=(0.5, 1), title="Held-out clade")
    axes[1].legend(fontsize=8)
    fig.tight_layout()
    fig.savefig(out / "fig_modules.png", dpi=130)
    print(f"Done -> {out}/ and laws/coloss_modules_v1.json")


if __name__ == "__main__":
    main()
