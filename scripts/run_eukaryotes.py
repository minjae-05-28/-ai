"""Free-living vs parasitic eukaryotes: learn gene-family birth-death laws.

    python scripts/run_eukaryotes.py [--n-boot 10] [--out results/eukaryotes]

The stored endosymbiosis law (laws/endosymbiosis_v1.json) is used only as a reference:
it is compared with the new laws and evaluated as a predictor, never fitted to.
"""

import argparse
import json
from pathlib import Path

import numpy as np
import torch

from organelle_evo.eukaryotes.birthdeath import simulate
from organelle_evo.eukaryotes.catalog import FREE, PAIRS, PARASITE, SPECIES, lifestyle, slug
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
LIFESTYLES = (FREE, PARASITE)


def load():
    meta = json.loads((DATA / "pfam_meta.json").read_text()) if (DATA / "pfam_meta.json").exists() else {}
    profiles = {}
    for sp in SPECIES:
        f = DATA / f"{slug(sp)}.json"
        if f.exists():
            profiles[sp] = json.loads(f.read_text())
    return profiles, meta


def reference_scores(n, x, law, context):
    """Endosymbiosis law as a predictor: P(all n copies lost) with its retention hazard.
    Its offset is matched to the observed number of losses, like the new model's."""
    w = law.weights[context]
    base = x @ w

    def p_lost(a):
        return (-np.expm1(-np.exp(a + base))) ** n

    return lambda n_lost: p_lost(_bisect(lambda a: p_lost(a).sum(), n_lost))


def _bisect(f, target, lo=-15.0, hi=10.0):
    for _ in range(60):
        mid = (lo + hi) / 2
        lo, hi = (mid, hi) if f(mid) < target else (lo, mid)
    return (lo + hi) / 2


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--n-boot", type=int, default=10)
    ap.add_argument("--epochs", type=int, default=400)
    ap.add_argument("--out", default="results/eukaryotes")
    args = ap.parse_args()
    torch.set_num_threads(4)
    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)

    profiles, meta = load()
    pairs = [(a, d) for a, d in PAIRS if a in profiles and d in profiles]
    missing = sorted(set(SPECIES) - set(profiles))
    print(f"{len(profiles)} species profiled, {len(pairs)} pairs usable; missing: {missing}")
    fams, x = family_features([profiles[s] for s in profiles], meta)
    print(f"{len(fams)} Pfam families; classes: "
          + ", ".join(f"{c}={int(x[:, i].sum())}" for i, c in enumerate(FAMILY_FEATURES) if i >= 3))

    data = [(counts(profiles[a], fams), counts(profiles[d], fams), LIFESTYLES.index(lifestyle(d)))
            for a, d in pairs]
    for (a, d), (n, m, s) in zip(pairs, data):
        print(f"  {a:26s} -> {d:30s} [{LIFESTYLES[s]:11s}] families {int((n > 0).sum()):5d} -> "
              f"{int((m > 0).sum()):5d}, lost {int(((n > 0) & (m == 0)).sum()):5d}, "
              f"gained {int(((n == 0) & (m > 0)).sum()):4d}")

    # 1. Laws, per lifestyle, with bootstrap SEs over pairs
    law = fit_bd_bootstrap(x, data, LIFESTYLES, n_boot=args.n_boot, epochs=args.epochs)
    shared = fit_bd(x, [(n, m, 0) for n, m, _ in data], LIFESTYLES, epochs=args.epochs)
    delta_aic = 2 * (shared.nll - law.nll) - 2 * (law.n_params - shared.n_params)
    print(f"lifestyle-specific vs shared law: ΔAIC = {delta_aic:.1f} (>10: parasitism changes the laws)")

    # 2. Held-out parasites: which of the ancestor's families are lost?
    ref = load_law("endosymbiosis_v1")
    heldout = []
    for i, ((a, d), (n, m, s)) in enumerate(zip(pairs, data)):
        if s != 1:
            continue
        train = data[:i] + data[i + 1:]
        fit = fit_bd(x, train, LIFESTYLES, epochs=args.epochs)
        par = [j for j, (_, _, sj) in enumerate(train) if sj == 1]
        a_lam = fit.a_lam[par].mean()
        had = n > 0
        lost = had & (m == 0)
        a_mu = offset_for_losses(n[had], x[had], fit.w_lam[1], fit.w_mu[1], a_lam, lost.sum())
        ours = loss_probability(n[had], x[had], fit.w_lam[1], fit.w_mu[1], a_lam, a_mu)
        others = [(tn, tm) for tn, tm, ts in train if ts == 1]
        freq = np.array([
            np.mean([tm[k] == 0 for tn, tm in others if tn[k] > 0]) if any(tn[k] > 0 for tn, _ in others) else 0.5
            for k in np.flatnonzero(had)
        ])
        row = {
            "pair": f"{a} -> {d}",
            "n_lost": int(lost.sum()),
            "copies_only": auroc(-n[had].astype(float), lost[had]),
            "learned_law": auroc(ours, lost[had]),
            "loss_frequency_elsewhere": auroc(freq, lost[had]),
        }
        for ctx in ref.weights:
            row[f"reference_{ctx}"] = auroc(reference_scores(n[had], x[had], ref, ctx)(lost.sum()), lost[had])
        heldout.append(row)
        print("  held-out " + ", ".join(f"{k}={v:.3f}" if isinstance(v, float) else f"{k}={v}" for k, v in row.items()))

    # 3. Compare with the stored endosymbiosis laws (reference only)
    comparison = {}
    for ctx in ref.weights:
        w_ref = ref.weights[ctx]
        for s, name in enumerate(LIFESTYLES):
            w_new = law.w_mu[s]
            comparison[f"{name}_loss_vs_{ctx}"] = {
                "correlation": float(np.corrcoef(w_new, w_ref)[0, 1]),
                "sign_agreement": float(np.mean(np.sign(w_new) == np.sign(w_ref))),
            }

    # 4. Simulation: a free-living amoeba switching to parasitism
    anc = "Dictyostelium discoideum"
    scenario = {}
    if anc in profiles:
        n0 = counts(profiles[anc], fams)
        par = [j for j, (_, _, s) in enumerate(data) if s == 1]
        free = [j for j, (_, _, s) in enumerate(data) if s == 0]
        rng = np.random.default_rng(0)
        for label, s, idx in [("stay_free_living", 0, free), ("become_parasite", 1, par)]:
            sims = simulate(
                np.tile(n0, (200, 1)),
                law.a_lam[idx].mean() + x @ law.w_lam[s],
                law.a_mu[idx].mean() + x @ law.w_mu[s],
                law.a_nu[idx].mean() + x @ law.w_nu[s],
                n_steps=100, rng=rng,
            )
            fam_present = (sims > 0).sum(1)
            p_lost = ((sims == 0) & (n0 > 0)).mean(0)
            by_class = {
                c: float(p_lost[(x[:, i] == 1) & (n0 > 0)].mean())
                for i, c in enumerate(FAMILY_FEATURES) if i >= 3
            }
            by_class["other"] = float(p_lost[(x[:, 3:].sum(1) == 0) & (n0 > 0)].mean())
            scenario[label] = {
                "families_now": int((n0 > 0).sum()),
                "families_after": np.quantile(fam_present, [0.05, 0.5, 0.95]).tolist(),
                "p_family_lost_by_class": by_class,
            }
        if "Entamoeba histolytica" in profiles:
            scenario["actual_Entamoeba_families"] = int((counts(profiles["Entamoeba histolytica"], fams) > 0).sum())

    def coef_table(w, se):
        return {
            name: {f: {"weight": float(w[s, i]), "se": float(se[s, i])} for i, f in enumerate(FAMILY_FEATURES)}
            for s, name in enumerate(LIFESTYLES)
        }

    metrics = {
        "species": list(profiles),
        "pairs": [f"{a} -> {d}" for a, d in pairs],
        "n_families": len(fams),
        "delta_aic_lifestyle_vs_shared": float(delta_aic),
        "loss_law": coef_table(law.w_mu, law.se["mu"]),
        "duplication_law": coef_table(law.w_lam, law.se["lam"]),
        "origination_law": coef_table(law.w_nu, law.se["nu"]),
        "heldout_parasites": heldout,
        "comparison_with_endosymbiosis_v1": comparison,
        "scenario_dictyostelium": scenario,
    }
    (out / "metrics.json").write_text(json.dumps(metrics, indent=2))
    save_law(
        LAWS_DIR / "eukaryote_lifestyle_v1.json",
        id="eukaryote_lifestyle_v1",
        scope=(
            "Gene-family (Pfam) duplication, loss and origination in eukaryotes, for "
            "free-living lineages and for lineages that became parasites. Learned from "
            "free-living-relative -> descendant pairs."
        ),
        model=("Linear birth-death per family with origination: log rate = a_pair + x @ w[lifestyle]. "
               "Positive loss weight = family lost faster."),
        feature_names=list(FAMILY_FEATURES),
        data={"pairs": metrics["pairs"], "n_families": len(fams)},
        caveats=[
            "An extant free-living relative stands in for the ancestor; it has evolved too.",
            "Few pairs per lifestyle; bootstrap over pairs gives wide intervals.",
            "Pfam families, not orthologues: a family count sums paralogues.",
        ],
        contexts={
            f"{kind}_{name}": {
                f: {"weight": round(float(w[s, i]), 4),
                    "ci95": [round(float(w[s, i] - 1.96 * se[s, i]), 4), round(float(w[s, i] + 1.96 * se[s, i]), 4)]}
                for i, f in enumerate(FAMILY_FEATURES)
            }
            for kind, w, se in [("loss", law.w_mu, law.se["mu"]), ("duplication", law.w_lam, law.se["lam"])]
            for s, name in enumerate(LIFESTYLES)
        },
    )
    print(f"Done -> {out}/ and laws/eukaryote_lifestyle_v1.json")


if __name__ == "__main__":
    main()
