"""Fill the remaining cells of the law map with the methods already used for parasites.

    python scripts/run_gaps.py

Environment (bacteria and archaea, relative -> extremophile pairs):
  how much   logit(share of the relative's families lost) = environment change @ b,
             leave-one-pair-out RMSE against the mean
  order      nestedness against row-fixed and fixed-fixed (curveball) nulls, on the
             families every relative has
  together   co-loss modules: leave-one-pair-out, half of each pair's families revealed,
             rank 0 (additive) vs rank 2
Endosymbiosis (organelles and insect endosymbionts, gene presence per lineage):
  how much   logit(share of the gene universe lost) = system + non-photosynthetic plastid
             + animal host, leave-one-lineage-out RMSE against system means
  together   co-loss modules, leave-one-lineage-out within each system
"""

import json
import sys
from pathlib import Path

import numpy as np
import torch

sys.path.insert(0, str(Path(__file__).resolve().parent))
from run_environment import load as load_prokaryotes  # noqa: E402
from run_nestedness import load_system, test as nested_test  # noqa: E402
from run_realdata import CATALOG  # noqa: E402

from organelle_evo.eukaryotes.modules import fit_modules, loss_matrix, predict_hidden  # noqa: E402
from organelle_evo.laws import LAWS_DIR, save_law  # noqa: E402
from organelle_evo.predict import auroc  # noqa: E402
from organelle_evo.prokaryotes.catalog import AXES, design, resolve_pairs  # noqa: E402

NONPHOTO = {"Epifagus virginiana", "Toxoplasma gondii", "Plasmodium falciparum"}
ANIMALS = {"Trichoplax adhaerens", "Metridium senile", "Drosophila melanogaster", "Caenorhabditis elegans",
           "Danio rerio", "Gallus gallus", "Mus musculus", "Homo sapiens"}
OUT = Path("results/gaps")


def logit(p):
    p = np.clip(p, 1e-3, 1 - 1e-3)
    return np.log(p / (1 - p))


def loo_rmse(Z, y, groups=None):
    groups = np.arange(len(y)) if groups is None else np.asarray(groups)
    err = []
    for g in np.unique(groups):
        tr = groups != g
        b = np.linalg.lstsq(Z[tr], y[tr], rcond=None)[0]
        err += list((Z[~tr] @ b - y[~tr]) ** 2)
    return float(np.sqrt(np.mean(err)))


def boot_ci(Z, y, n=2000, seed=0):
    rng = np.random.default_rng(seed)
    bs = []
    for _ in range(n):
        i = rng.integers(0, len(y), len(y))
        if np.linalg.matrix_rank(Z[i]) == Z.shape[1]:
            bs.append(np.linalg.lstsq(Z[i], y[i], rcond=None)[0])
    return np.percentile(bs, [2.5, 97.5], axis=0)


def module_test(L, rows_out, reveal=0.5, repeats=3, k=2):
    """rows_out: list of index lists, each held out together. Returns mean AUROC k0, k."""
    res = {0: [], k: []}
    for out in rows_out:
        tr = [i for i in range(len(L)) if i not in out]
        models = {kk: fit_modules(L[tr], kk) for kk in res}
        for i in out:
            if np.isnan(L[i]).all() or np.nansum(L[i]) in (0, np.sum(~np.isnan(L[i]))):
                continue
            for kk, mdl in models.items():
                vals = [auroc(*predict_hidden(mdl, L[i], reveal, np.random.default_rng(r))) for r in range(repeats)]
                res[kk].append(float(np.nanmean(vals)))
    return {f"k{kk}": float(np.nanmean(v)) for kk, v in res.items()}, len(res[0])


def main():
    torch.set_num_threads(2)
    OUT.mkdir(parents=True, exist_ok=True)
    rng = np.random.default_rng(0)
    out = {}

    # ---------- Environment ----------
    profiles, meta, fams, names, x, c = load_prokaryotes()
    pairs = resolve_pairs(profiles)
    L = loss_matrix(pairs, c)
    sev = np.nanmean(L, 1)
    Z = np.array([design(a, d) for a, d in pairs])
    y = logit(sev)
    b = np.linalg.lstsq(Z, y, rcond=None)[0]
    ci = boot_ci(Z, y)
    rm = {"mean_only": loo_rmse(Z[:, :1], y), "environment": loo_rmse(Z, y)}
    labels = ("base", *AXES)
    print("environment / how much: " + ", ".join(f"{l} {w:+.2f} [{lo:+.2f},{hi:+.2f}]" for l, w, lo, hi in zip(labels, b, *ci)))
    print(f"  leave-one-pair-out RMSE (logit): mean {rm['mean_only']:.3f}, environment {rm['environment']:.3f}")
    out["environment_how_much"] = {"coef": {l: [float(w), float(lo), float(hi)] for l, w, lo, hi in zip(labels, b, *ci)},
                                   "loo_rmse": rm, "share_lost": {d: float(s) for (_, d), s in zip(pairs, sev)}}

    core = np.all([c[a] > 0 for a, _ in pairs], 0)
    M = np.array([(c[d] == 0)[core] for _, d in pairs])
    nt = nested_test(M, rng)
    print(f"environment / order: containment {nt['containment']:.3f}, row null {nt['row_null_mean']:.3f} "
          f"(z {nt['row_null_z']:+.1f}), fixed-fixed {nt['fixed_null_mean']:.3f} (z {nt['fixed_null_z']:+.1f})")
    out["environment_order"] = nt

    keep = (~np.isnan(L)).sum(0) >= 5
    mt, n = module_test(L[:, keep], [[i] for i in range(len(pairs))])
    print(f"environment / together: hidden-half AUROC additive {mt['k0']:.3f}, modules {mt['k2']:.3f} ({n} pairs)")
    out["environment_together"] = {**mt, "n": n}

    # ---------- Endosymbiosis ----------
    cache = json.loads(Path("data/processed/homology.json").read_text()) if Path("data/processed/homology.json").exists() else {}
    rows, mats = [], {}
    for system in CATALOG:
        ds, _ = load_system(system, Path("data/raw"), cache)
        mats[system] = (~ds.present).astype(float)
        for lin, pres in zip(ds.lineages, ds.present):
            rows.append((system, lin, 1 - pres.mean()))
    systems = list(CATALOG)
    Zs = np.array([[s == sy for sy in systems] + [lin in NONPHOTO and s == "plastid", lin in ANIMALS and s == "mitochondrion"]
                   for s, lin, _ in rows], dtype=float)
    ys = logit(np.array([r[2] for r in rows]))
    bs = np.linalg.lstsq(Zs, ys, rcond=None)[0]
    cis = boot_ci(Zs, ys)
    lab = [*systems, "nonphotosynthetic_plastid", "animal_mitochondrion"]
    rms = {"system_only": loo_rmse(Zs[:, :len(systems)], ys), "with_covariates": loo_rmse(Zs, ys)}
    exp = lambda v: 1 / (1 + np.exp(-v))  # noqa: E731
    typical = {f"{s}": float(exp(bs[i])) for i, s in enumerate(systems)}
    typical["plastid, non-photosynthetic"] = float(exp(bs[systems.index("plastid")] + bs[-2]))
    typical["mitochondrion, animal"] = float(exp(bs[systems.index("mitochondrion")] + bs[-1]))
    print("endosymbiosis / how much: " + ", ".join(f"{l} {w:+.2f} [{lo:+.2f},{hi:+.2f}]" for l, w, lo, hi in zip(lab, bs, *cis)))
    print(f"  leave-one-lineage-out RMSE (logit): system only {rms['system_only']:.3f}, with covariates {rms['with_covariates']:.3f}")
    print("  typical share lost: " + ", ".join(f"{k} {v:.0%}" for k, v in typical.items()))
    out["endosymbiosis_how_much"] = {"coef": {l: [float(w), float(lo), float(hi)] for l, w, lo, hi in zip(lab, bs, *cis)},
                                     "loo_rmse": rms, "typical_share_lost": typical}

    together = {}
    for system, Ls in mats.items():
        Ls = Ls[:, (Ls.sum(0) > 0) & (Ls.sum(0) < len(Ls))]
        mt, n = module_test(Ls, [[i] for i in range(len(Ls))])
        together[system] = {**mt, "n": n}
        print(f"endosymbiosis / together / {system}: additive {mt['k0']:.3f}, modules {mt['k2']:.3f} ({n} lineages)")
    out["endosymbiosis_together"] = together
    (OUT / "metrics.json").write_text(json.dumps(out, indent=2))

    # ---------- Laws ----------
    save_law(LAWS_DIR / "severity_environment_v1.json", id="severity_environment_v1",
             scope="Share of a relative's gene families lost when a bacterium or archaeon moves to an extreme environment.",
             model="logit(share lost) = environment change @ b (base, colder, saltier, anaerobic, radiation, oligotrophic).",
             feature_names=list(labels), data={"pairs": [f"{a} -> {d}" for a, d in pairs]},
             validation={"leave_one_pair_out_rmse_logit": rm},
             caveats=["21 pairs for 6 coefficients; intervals are wide."],
             contexts={"loss": {l: {"weight": round(float(w), 4), "ci95": [round(float(lo), 4), round(float(hi), 4)]}
                                for l, w, lo, hi in zip(labels, b, *ci)}})
    save_law(LAWS_DIR / "severity_endosymbiosis_v1.json", id="severity_endosymbiosis_v1",
             scope="Share of the ancestral gene set lost by organelles and insect endosymbionts.",
             model="logit(share lost) = system + non-photosynthetic plastid + animal host (mitochondria).",
             feature_names=lab, data={"lineages": [f"{s}: {l}" for s, l, _ in rows]},
             validation={"leave_one_lineage_out_rmse_logit": rms, "typical_share_lost": typical},
             caveats=["Mitochondrial and plastid universes are the union over lineages, not a true ancestor."],
             contexts={"loss": {l: {"weight": round(float(w), 4), "ci95": [round(float(lo), 4), round(float(hi), 4)]}
                                for l, w, lo, hi in zip(lab, bs, *cis)}})
    save_law(LAWS_DIR / "loss_order_environment_v1.json", id="loss_order_environment_v1",
             scope="Order of gene-family loss when bacteria and archaea move to extreme environments.",
             model="Nestedness against row-fixed and fixed-fixed (curveball) nulls.", feature_names=[],
             data={"pairs": len(pairs), "families": int(core.sum())}, validation=nt, contexts={},
             caveats=["Uses only families present in every relative."])
    save_law(LAWS_DIR / "coloss_environment_endosymbiosis_v1.json", id="coloss_environment_endosymbiosis_v1",
             scope="Whether genes are lost in modules (beyond per-gene propensity) in extremophiles, organelles and insect endosymbionts.",
             model="Logistic rank-k factorisation; half of a held-out lineage revealed, the rest predicted.",
             feature_names=[], data={}, validation={"environment": out["environment_together"], **together}, contexts={},
             caveats=["Held out one pair or lineage at a time; related lineages remain in training."])
    print(f"Done -> {OUT}/ and four laws")


if __name__ == "__main__":
    main()
