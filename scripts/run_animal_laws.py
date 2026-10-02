"""Learn composition laws on animal cells, instead of borrowing the microbial ones.

    python scripts/run_animal_laws.py

The microbial temperature law does not transfer to animals (laws/animal_temperature_v1.json:
endotherms carry *less* IVYWREL although their cells run 17 C warmer). This fits the law on
animals directly, on the variables an animal cell actually experiences
(src/organelle_evo/animals/catalog.py):

    tcell       the temperature the cells operate at, -1 to 41.5 C
    osmol_high  marine osmoconformer (~1000 mOsm) vs osmoregulator (~300)
    hypoxia     routinely lives with little oxygen
    endo        endotherm, i.e. holds its own cell temperature
    parasite    parasite (this project already showed parasitism moves composition)
    urea        conforms with urea/TMAO rather than inorganic ions

For each composition statistic the script fits the axes additively, then checks the result
the way every other law in this project is checked:

  1. leave-one-clade-out: refit without a whole clade (mammals, teleosts, molluscs, ...)
     and predict it, so a law cannot be one lineage's quirk
  2. phylogenetic correction: rank GLS on NCBI taxonomy, as in run_phylo.py
  3. GC control, when genome GC is available (data/gc.json), because this project found
     several composition laws to be GC in disguise
  4. the microbial coefficient printed next to the animal one, for comparison

Output: results/animal_laws/ and laws/animal_axes_v1.json.
"""

import json
from collections import defaultdict
from pathlib import Path

import numpy as np
from scipy import stats

from organelle_evo.animals import catalog as an
from organelle_evo.laws import LAWS_DIR, save_law

COMP = Path("data/composition/animals")
OUT = Path("results/animal_laws")
AXES = ["tcell", "osmol_high", "hypoxia", "endo", "parasite", "urea"]
TRAITS = ["ivywrel", "cvp", "acidic_excess", "median_pi", "n_side", "gravy", "fymink", "aromatic", "cysteine"]

# the same statistic regressed on habitat temperature in 86 prokaryotes and archaea
# (results/phylo; per deg C), for side-by-side comparison
MICROBIAL_PER_C = {"ivywrel": 0.0009836, "cvp": 0.0015}


def load():
    rows = []
    for f in sorted(COMP.glob("*.json")):
        d = json.loads(f.read_text())
        sp = d["species"]
        if sp in an.SPECIES and d.get("n_proteins", 0) >= 5000:
            rows.append({"species": sp, "group": an.SPECIES[sp].group, **an.axes(sp),
                         **{t: d[t] for t in TRAITS if t in d}, "n_proteins": d["n_proteins"]})
    return rows


def design(rows, axes):
    X = np.c_[np.ones(len(rows)), np.array([[r[a] for a in axes] for r in rows], dtype=float)]
    return X


def fit(X, y):
    beta, *_ = np.linalg.lstsq(X, y, rcond=None)
    resid = y - X @ beta
    dof = max(len(y) - X.shape[1], 1)
    s2 = float(resid @ resid) / dof
    cov = s2 * np.linalg.pinv(X.T @ X)
    se = np.sqrt(np.clip(np.diag(cov), 0, None))
    with np.errstate(divide="ignore", invalid="ignore"):
        t = np.where(se > 0, beta / se, 0.0)
    p = 2 * stats.t.sf(np.abs(t), dof)
    r2 = 1 - float(resid @ resid) / max(float(((y - y.mean()) ** 2).sum()), 1e-12)
    return beta, se, p, r2


def loco(rows, axes, trait):
    """Leave one clade out: fit without a clade, predict it, and score against the mean."""
    groups = sorted({r["group"] for r in rows})
    errs, base_errs, n = [], [], 0
    for g in groups:
        tr = [r for r in rows if r["group"] != g]
        te = [r for r in rows if r["group"] == g]
        if len(tr) < len(axes) + 3 or not te:
            continue
        ytr = np.array([r[trait] for r in tr])
        beta, *_ = np.linalg.lstsq(design(tr, axes), ytr, rcond=None)
        yte = np.array([r[trait] for r in te])
        errs += list(np.abs(design(te, axes) @ beta - yte))
        base_errs += list(np.abs(ytr.mean() - yte))
        n += len(te)
    if not errs:
        return None
    return {"n_predicted": n, "mae_law": float(np.mean(errs)), "mae_mean_baseline": float(np.mean(base_errs)),
            "beats_baseline": bool(np.mean(errs) < np.mean(base_errs))}


def rank_gls_taxonomy(rows, axes, trait):
    """Clade-level check: average within clade, then refit, so one big clade cannot carry it."""
    by = defaultdict(list)
    for r in rows:
        by[r["group"]].append(r)
    agg = [{"group": g, trait: float(np.mean([r[trait] for r in v])),
            **{a: float(np.mean([r[a] for r in v])) for a in axes}} for g, v in by.items()]
    if len(agg) < len(axes) + 2:
        return None
    beta, se, p, r2 = fit(design(agg, axes), np.array([r[trait] for r in agg]))
    return {"n_clades": len(agg), "coef": {a: float(beta[i + 1]) for i, a in enumerate(axes)},
            "p": {a: float(p[i + 1]) for i, a in enumerate(axes)}, "r2": r2}


def main():
    rows = load()
    if len(rows) < 25:
        print(f"only {len(rows)} animal proteomes in {COMP} so far; "
              f"waiting for the proteome-composition workflow ({len(an.SPECIES)} catalogued)")
        return
    groups = sorted({r["group"] for r in rows})
    print(f"{len(rows)} animal proteomes, {len(groups)} clades: {', '.join(groups)}")
    t = np.array([r["tcell"] for r in rows])
    print(f"cell temperature {t.min():.0f} to {t.max():.0f} C; "
          f"{int(sum(r['osmol_high'] for r in rows))} osmoconformers, "
          f"{int(sum(r['endo'] for r in rows))} endotherms, "
          f"{int(sum(r['parasite'] for r in rows))} parasites\n")

    gc = {}
    gcf = Path("data/gc.json")
    if gcf.exists():
        gc = {k: v for k, v in json.loads(gcf.read_text()).items() if k in an.SPECIES}

    res = {"n_species": len(rows), "n_clades": len(groups), "axes": AXES, "traits": {}}
    for trait in TRAITS:
        if not all(trait in r for r in rows):
            continue
        y = np.array([r[trait] for r in rows])
        beta, se, p, r2 = fit(design(rows, AXES), y)
        entry = {"r2": r2, "coef": {}, "p": {}}
        print(f"{trait}  (R^2 {r2:.2f})")
        for i, a in enumerate(AXES):
            entry["coef"][a], entry["p"][a] = float(beta[i + 1]), float(p[i + 1])
            star = "*" if p[i + 1] < 0.05 else " "
            extra = ""
            if a == "tcell" and trait in MICROBIAL_PER_C:
                m = MICROBIAL_PER_C[trait]
                extra = (f"   microbes {m:+.5f}/C -> animal law is "
                         f"{'the OPPOSITE sign' if np.sign(beta[i + 1]) != np.sign(m) else 'the same sign'}")
            print(f"   {a:11s} {beta[i + 1]:+.5f}  (p {p[i + 1]:.1e}){star}{extra}")
        entry["leave_one_clade_out"] = loco(rows, AXES, trait)
        if entry["leave_one_clade_out"]:
            l = entry["leave_one_clade_out"]
            print(f"   leave-one-clade-out: MAE {l['mae_law']:.4f} vs mean baseline {l['mae_mean_baseline']:.4f} "
                  f"-> {'generalises' if l['beats_baseline'] else 'DOES NOT generalise'}")
        entry["clade_level"] = rank_gls_taxonomy(rows, AXES, trait)
        if entry["clade_level"]:
            c = entry["clade_level"]
            kept = [a for a in AXES if c["p"][a] < 0.05 and np.sign(c["coef"][a]) == np.sign(entry["coef"][a])]
            print(f"   clade level ({c['n_clades']} clades): survives for {kept or 'nothing'}")
            entry["survives_clade_level"] = kept
        if gc:
            g = [gc.get(r["species"]) for r in rows]
            ix = [i for i, v in enumerate(g) if v is not None]
            if len(ix) > len(AXES) + 5:
                Xg = np.c_[design([rows[i] for i in ix], AXES), np.array([g[i] for i in ix], dtype=float)]
                bg, _, pg, _ = fit(Xg, y[ix])
                entry["with_gc"] = {"n": len(ix), "coef": {a: float(bg[i + 1]) for i, a in enumerate(AXES)},
                                    "p": {a: float(pg[i + 1]) for i, a in enumerate(AXES)},
                                    "gc_p": float(pg[-1])}
                kept = [a for i, a in enumerate(AXES) if pg[i + 1] < 0.05
                        and np.sign(bg[i + 1]) == np.sign(entry["coef"][a])]
                print(f"   with genome GC as a covariate (n={len(ix)}): survives for {kept or 'nothing'}")
                entry["survives_gc"] = kept
        res["traits"][trait] = entry
        print()

    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "metrics.json").write_text(json.dumps(res, indent=2))
    save_law(LAWS_DIR / "animal_axes_v1.json", id="animal_axes_v1",
             scope="Composition laws fitted to animal cells on the variables an animal cell experiences: "
                   "operating temperature, intracellular osmolarity, hypoxia, endothermy, parasitism and "
                   "urea-based osmoconformity.",
             model="Additive least squares per composition statistic, checked by leave-one-clade-out, "
                   "a clade-level refit, and genome GC as a covariate.",
             feature_names=AXES, data={"species": len(rows), "clades": len(groups)}, validation=res, contexts={},
             caveats=["Axis values are literature approximations of typical conditions, not measurements of "
                      "each animal's cells.",
                      "Cell temperature and endothermy are correlated by biology (r about 0.56), so their "
                      "separate coefficients are less certain than the pair of them together.",
                      "Whole-proteome averages: a law here says nothing about any individual protein.",
                      "Clades are unevenly sampled, which is why leave-one-clade-out and the clade-level "
                      "refit are reported next to the fit."])
    print(f"Done -> {OUT}/ and laws/animal_axes_v1.json")


if __name__ == "__main__":
    main()
