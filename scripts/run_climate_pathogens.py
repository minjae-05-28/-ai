"""Which gene families would climate-linked pathogens lose or expand as they adapt?

    python scripts/run_climate_pathogens.py [--warming 5]

Two pressures, each from a law fitted on other organisms (the targets are in no pair):
  warming      bacteria: the environment law's temperature axis (environment_v2), applied
               as a rise of --warming deg C
  host shift   fungi and amoebae: the parasite axis of the eukaryote law (eukaryote_axes_v3),
               free-living -> extracellular parasite
For each target, only the *extra* push from the pressure is used,
    delta_f = change in log loss (or duplication) rate for family f = (z_new - z_old) @ W @ x_f,
because the base propensity of each family would rank the same under any pressure.
Families are ranked by delta among those the target carries; functions are summarised.

Backtests on pairs that already happened:
  warming      the environment law's own held-out score on pairs that moved to hotter habitats
  host shift   Naegleria gruberi -> N. fowleri (thermotolerant, opportunistic brain pathogen):
               does the parasite push rank what N. fowleri lost better than chance?
"""

import argparse
import json
from pathlib import Path

import numpy as np

from organelle_evo.eukaryotes.features import enriched_features
from organelle_evo.eukaryotes.model import counts, family_features
from organelle_evo.laws import load_law
from organelle_evo.predict import auroc
from organelle_evo.prokaryotes import catalog as pro_cat
from organelle_evo.eukaryotes import catalog as euk_cat

ANN = Path("data/eukaryotes")


def load(dir_, free):
    meta = json.loads((ANN / "pfam_meta.json").read_text())
    ann = json.loads((ANN / "family_annotations.json").read_text())
    profiles = {}
    for f in Path(dir_).glob("*.json"):
        if f.name in ("pfam_meta.json", "family_annotations.json"):
            continue
        d = json.loads(f.read_text())
        profiles[d["species"]] = d
    fams, _ = family_features(list(profiles.values()), meta)
    c = {s: counts(p, fams) for s, p in profiles.items()}
    fams, names, x = enriched_features(profiles, meta, ann, c, free=free(profiles))
    return meta, fams, names, x, c


def align(law, names, x):
    """Columns of x in the order the law was fitted with (GO-slim columns can differ when the
    family set changes)."""
    missing = [f for f in law.feature_names if f not in names]
    if missing:
        raise SystemExit(f"features missing for {law.id}: {missing}")
    idx = [list(names).index(f) for f in law.feature_names]
    return list(law.feature_names), x[:, idx]


def weights(law, kind):
    """(labels, W) with W[label] over features, from a stored law's contexts."""
    out = {}
    for ctx, w in law.weights.items():
        if ctx.startswith(kind + "_"):
            out[ctx[len(kind) + 1:]] = w
    return out


def summarise(names, x, sel, cats):
    fr, base = x[sel][:, cats].mean(0), x[:, cats].mean(0)
    ratio = (fr + 0.01) / (base + 0.01)
    return [(names[cats[k]], round(float(ratio[k]), 2)) for k in np.argsort(-ratio)[:6] if fr[k] >= 0.08]


def forecast(target, n, x, names, fams, meta, d_loss, d_dup, top=15):
    had = n > 0
    idx = np.flatnonzero(had)
    cats = [k for k, nm in enumerate(names) if nm.startswith(("go:", "kw:"))]
    lose = idx[np.argsort(-d_loss[idx])][:top]
    keep = idx[np.argsort(d_loss[idx])][:top]
    grow = idx[np.argsort(-d_dup[idx])][:top]
    desc = lambda j: f"{fams[j]}: {meta.get(fams[j], {}).get('description', '')}"  # noqa: E731
    return {"families": int(had.sum()),
            "pushed_to_loss": [desc(j) for j in lose], "pushed_to_loss_functions": summarise(names, x, lose, cats),
            "protected": [desc(j) for j in keep], "protected_functions": summarise(names, x, keep, cats),
            "pushed_to_expand": [desc(j) for j in grow], "pushed_to_expand_functions": summarise(names, x, grow, cats)}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--warming", type=float, default=5.0)
    ap.add_argument("--env-law", default="environment_v2")
    args = ap.parse_args()
    out = {"warming_c": args.warming}

    # ---- Bacteria: warming ----
    law = load_law(args.env_law)
    meta, fams, names, x, c = load("data/prokaryotes", free=lambda p: [s for s in p if s not in pro_cat.CLIMATE_TARGETS])
    names, x = align(law, names, x)
    Wmu, Wlam = weights(law, "loss"), weights(law, "duplication")
    dz = -args.warming / pro_cat.TEMP_SCALE  # 'colder' axis goes the other way
    d_loss, d_dup = dz * (x @ Wmu["colder"]), dz * (x @ Wlam["colder"])
    out["bacteria"] = {}
    for t in pro_cat.CLIMATE_TARGETS:
        if t in c:
            out["bacteria"][t] = forecast(t, c[t], x, names, fams, meta, d_loss, d_dup)
            print(f"[warming +{args.warming:g} C] {t}: to lose {out['bacteria'][t]['pushed_to_loss_functions'][:3]}; "
                  f"to expand {out['bacteria'][t]['pushed_to_expand_functions'][:3]}")
    hot = {r["pair"]: r for r in json.loads(Path("results/environment/metrics.json").read_text())["heldout"]
           if r["design"][1] <= -0.5}
    out["warming_backtest"] = hot
    for p, r in hot.items():
        print(f"  backtest {p}: environment law {r['environment_law']:.3f} vs no environment {r['no_environment']:.3f}")

    # ---- Fungi and amoebae: host shift ----
    elaw = load_law("eukaryote_axes_v3")
    meta, fams, names, x, c = load("data/eukaryotes", free=lambda p: [s for s in p if s in euk_cat.SPECIES
                                                                      and euk_cat.SPECIES[s].lifestyle == euk_cat.FREE
                                                                      and s not in euk_cat.CLIMATE_TARGETS])
    Wmu, Wlam = weights(elaw, "loss"), weights(elaw, "duplication")
    names, x = align(elaw, names, x)
    d_loss, d_dup = x @ Wmu["parasite"], x @ Wlam["parasite"]
    out["fungi"] = {}
    for t in euk_cat.CLIMATE_TARGETS:
        if t in c:
            out["fungi"][t] = forecast(t, c[t], x, names, fams, meta, d_loss, d_dup)
            print(f"[host shift] {t}: to lose {out['fungi'][t]['pushed_to_loss_functions'][:3]}; "
                  f"to expand {out['fungi'][t]['pushed_to_expand_functions'][:3]}")
    a, d = "Naegleria gruberi", "Naegleria fowleri"
    had = c[a] > 0
    lost = (c[d] == 0)[had]
    out["host_shift_backtest"] = {"pair": f"{a} -> {d}", "families": int(had.sum()), "lost": int(lost.sum()),
                                  "auroc_parasite_push": auroc(d_loss[had], lost)}
    print(f"  backtest {a} -> {d}: parasite push ranks lost families with AUROC {out['host_shift_backtest']['auroc_parasite_push']:.3f}")

    Path("results/climate").mkdir(parents=True, exist_ok=True)
    Path("results/climate/metrics.json").write_text(json.dumps(out, indent=2))
    print("Done -> results/climate/")


if __name__ == "__main__":
    main()
