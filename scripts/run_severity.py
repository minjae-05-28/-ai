"""Law search: how much of its gene-family repertoire does a lineage lose?

    python scripts/run_severity.py

Severity = share of the ancestor proxy's families absent from the descendant. Model:
logit(severity) = design @ b, design = (1, parasite, intracellular, reduced mitochondria).
Checked leave-one-clade-out against the mean-only and parasite-only models.
"""

import json
import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
from run_modules import clade, load  # noqa: E402

from organelle_evo.eukaryotes.catalog import AXES, design, resolve_pairs  # noqa: E402
from organelle_evo.eukaryotes.modules import loss_matrix  # noqa: E402
from organelle_evo.laws import LAWS_DIR, save_law  # noqa: E402

N_BOOT = 2000


def fit(Z, y):
    return np.linalg.lstsq(Z, y, rcond=None)[0]


def main():
    out = Path("results/severity")
    out.mkdir(parents=True, exist_ok=True)
    profiles, meta, ann, fams, c = load()
    pairs = resolve_pairs(profiles)
    sev = np.nanmean(loss_matrix(pairs, c), 1)
    y = np.log(sev / (1 - sev))
    Z = np.array([design(d) for _, d in pairs])
    cl = np.array([clade(d) for _, d in pairs])
    labels = ("base", *AXES)

    b = fit(Z, y)
    rng = np.random.default_rng(0)
    groups = np.unique(cl)
    boot = []
    for _ in range(N_BOOT):  # resample clades, not pairs
        pick = np.concatenate([np.flatnonzero(cl == g) for g in rng.choice(groups, len(groups))])
        if np.linalg.matrix_rank(Z[pick]) == Z.shape[1]:
            boot.append(fit(Z[pick], y[pick]))
    ci = np.percentile(boot, [2.5, 97.5], axis=0)
    rmse = {}
    for name, cols in [("mean_only", [0]), ("parasite_only", [0, 1]), ("all_axes", [0, 1, 2, 3])]:
        err = []
        for g in groups:
            tr = cl != g
            err += list((Z[~tr][:, cols] @ fit(Z[tr][:, cols], y[tr]) - y[~tr]) ** 2)
        rmse[name] = float(np.sqrt(np.mean(err)))
    expit = lambda v: 1 / (1 + np.exp(-v))  # noqa: E731
    typical = {"free_living": expit(b[0]), "extracellular_parasite": expit(b[0] + b[1]),
               "intracellular_parasite": expit(b[0] + b[1] + b[2]),
               "intracellular_reduced_mito": expit(b.sum())}
    for lab, w, lo, hi in zip(labels, b, *ci):
        print(f"  {lab:22s} {w:+.2f}  [{lo:+.2f}, {hi:+.2f}]")
    print("leave-one-clade-out RMSE (logit): " + ", ".join(f"{k} {v:.3f}" for k, v in rmse.items()))
    print("typical share lost: " + ", ".join(f"{k} {v:.0%}" for k, v in typical.items()))
    resid = y - Z @ b
    outliers = sorted(zip(resid, [d for _, d in pairs], sev), reverse=True)

    (out / "metrics.json").write_text(json.dumps({
        "coefficients": {lab: {"weight": float(w), "ci95": [float(lo), float(hi)]} for lab, w, lo, hi in zip(labels, b, *ci)},
        "loco_rmse_logit": rmse, "typical_share_lost": {k: float(v) for k, v in typical.items()},
        "severity": {d: float(s) for (_, d), s in zip(pairs, sev)},
        "more_lost_than_predicted": [(d, float(s)) for _, d, s in outliers[:5]],
        "less_lost_than_predicted": [(d, float(s)) for _, d, s in outliers[-5:]]}, indent=2))
    save_law(
        LAWS_DIR / "severity_v1.json",
        id="severity_v1",
        scope="Share of ancestral gene families lost by a eukaryotic lineage, from its lifestyle axes.",
        model="logit(share lost) = b0 + b_parasite + b_intracellular + b_reduced_mitochondria (additive).",
        feature_names=list(labels),
        data={"pairs": [f"{a} -> {d}" for a, d in pairs]},
        validation={"loco_rmse_logit": rmse, "bootstrap": f"{N_BOOT} clade resamples"},
        caveats=["Assembly/annotation completeness inflates apparent loss (e.g. Trypanosoma congolense).",
                 "Free-living controls measure drift between relatives, not zero change."],
        contexts={"loss": {lab: {"weight": round(float(w), 4), "ci95": [round(float(lo), 4), round(float(hi), 4)]}
                           for lab, w, lo, hi in zip(labels, b, *ci)},
                  "typical_share_lost": {k: round(float(v), 3) for k, v in typical.items()}},
    )

    fig, ax = plt.subplots(figsize=(7, 4.5))
    ax.scatter(expit(Z @ b), sev, c=["#e76f51" if z[1] else "#2a9d8f" for z in Z], s=22)
    ax.plot([0, 1], [0, 1], "k--", lw=1)
    ax.set(xlabel="predicted share lost (lifestyle axes only)", ylabel="observed share lost",
           title="Loss severity follows the lifestyle axes additively")
    fig.tight_layout()
    fig.savefig(out / "fig_severity.png", dpi=130)
    print(f"Done -> {out}/")


if __name__ == "__main__":
    main()
