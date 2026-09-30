"""End-to-end experiment: learn rules -> infer history -> forecast evolution.

    python scripts/run_pipeline.py            # full run (~2-3 min on CPU)
    python scripts/run_pipeline.py --quick    # smoke test
"""

import argparse
import json
from pathlib import Path

import numpy as np
import torch

from organelle_evo.ancestor import FEATURES, make_ancestor
from organelle_evo.inference import EvolutionInferrer
from organelle_evo.plots import plot_forecast, plot_inference, plot_reduction, plot_rules
from organelle_evo.predict import auroc, category_baseline, forecast
from organelle_evo.rules import fit_rules_bootstrap
from organelle_evo.simulator import (
    ORGANELLE,
    PARAM_NAMES,
    TRUE_RULES,
    sample_prior,
    simulate,
)

SNAPSHOT_FRAC = 0.6
N_STEPS = 100


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--quick", action="store_true")
    ap.add_argument("--out", default="results")
    ap.add_argument("--seed", type=int, default=0)
    args = ap.parse_args()
    torch.set_num_threads(1)  # tiny models: threading overhead dominates
    out = Path(args.out)
    out.mkdir(exist_ok=True)
    rng = np.random.default_rng(args.seed)
    n_lineages, n_boot, n_sims, epochs, n_test = (
        (15, 3, 2000, 5, 20) if args.quick else (40, 20, 20000, 60, 200)
    )
    genome = make_ancestor(args.seed)
    metrics = {}

    # --- The "real" world: lineages evolve under hidden true laws ---------------
    print(f"[1/4] Simulating {n_lineages} observed lineages from a {genome.n_genes}-gene ancestor")
    world_params = sample_prior(n_lineages, rng)
    world = simulate(genome, TRUE_RULES, world_params, n_steps=N_STEPS, rng=rng)
    plot_reduction(genome, world.counts, world.states, out / "fig1_reduction.png")

    # --- AI 1: learn the laws of organelle evolution ----------------------------
    print("[2/4] Learning evolutionary rules from end states only")
    fitted = fit_rules_bootstrap(genome.features, world.states, n_boot=n_boot, seed=args.seed)
    plot_rules(TRUE_RULES, fitted, out / "fig2_rules.png")
    metrics["rules"] = {
        f"{kind}.{f}": {"true": float(t), "learned": float(e), "se": float(s)}
        for kind, tw, ew, sw in [
            ("transfer", TRUE_RULES.transfer_weights, fitted.transfer_weights, fitted.transfer_se),
            ("loss", TRUE_RULES.loss_weights, fitted.loss_weights, fitted.loss_se),
        ]
        for f, t, e, s in zip(FEATURES, tw, ew, sw)
    }
    for k, v in metrics["rules"].items():
        print(f"    {k:34s} true {v['true']:+.2f}  learned {v['learned']:+.2f} ± {1.96 * v['se']:.2f}")

    # --- AI 2: amortised inference of a lineage's hidden history ----------------
    # The learned rules have their biases folded into lineage offsets, so the prior
    # for the inferrer is set from the range of offsets seen in the observed lineages.
    learned = fitted.to_rules()
    low = np.array([fitted.lineage_log_transfer.min() - 1.0, fitted.lineage_log_loss.min() - 1.0, 0.0])
    high = np.array([fitted.lineage_log_transfer.max() + 0.5, fitted.lineage_log_loss.max() + 0.5, 3.0])
    print(f"[3/4] Training posterior network on {n_sims} simulations (learned rules)")
    inferrer = EvolutionInferrer(genome, learned, low, high)
    inferrer.train(n_sims=n_sims, epochs=epochs, seed=args.seed)
    val_params, val_states = inferrer.simulate_dataset(1000, rng)
    post = inferrer.infer(val_states)
    plot_inference(val_params, post, out / "fig3_inference.png")
    z = np.abs(post.mean - val_params) / post.std
    metrics["inference"] = {
        name: {
            "r2": float(1 - ((post.mean[:, i] - val_params[:, i]) ** 2).mean() / val_params[:, i].var()),
            "coverage_90": float((z[:, i] < 1.645).mean()),
        }
        for i, name in enumerate(PARAM_NAMES)
    }
    for k, v in metrics["inference"].items():
        print(f"    {k:14s} R² {v['r2']:.3f}   90% interval coverage {v['coverage_90']:.2f}")

    # --- AI 3: forecast the future from a present-day snapshot -------------------
    print(f"[4/4] Forecasting {n_test} unseen true-world lineages from a {SNAPSHOT_FRAC:.0%} snapshot")
    snap_step = int(SNAPSHOT_FRAC * N_STEPS)
    horizon = (1 - SNAPSHOT_FRAC) / SNAPSHOT_FRAC
    test_params = sample_prior(n_test, rng)
    test = simulate(genome, TRUE_RULES, test_params, n_steps=N_STEPS, snapshot_steps=(snap_step,), rng=rng)
    snaps = test.snapshots[snap_step]

    scores = {"category baseline": [], "ours": [], "oracle": []}
    labels, count_err, count_cover = [], [], []
    example = None
    for i in range(n_test):
        at_risk = snaps[i] == ORGANELLE
        leaves = test.states[i] != ORGANELLE
        samples = inferrer.infer(snaps[i]).sample(200, rng)
        fc = forecast(genome, learned, snaps[i], samples, horizon, rng=rng)
        oracle = forecast(genome, TRUE_RULES, snaps[i], np.repeat(test_params[i : i + 1], 200, 0),
                          1 - SNAPSHOT_FRAC, rng=rng)
        scores["category baseline"].append(category_baseline(genome, snaps[i])[at_risk])
        scores["ours"].append(fc.p_leaves_organelle[at_risk])
        scores["oracle"].append(oracle.p_leaves_organelle[at_risk])
        labels.append(leaves[at_risk])
        final = fc.counts[:, -1, ORGANELLE]
        truth = test.counts[i, -1, ORGANELLE]
        count_err.append(abs(np.median(final) - truth))
        lo, hi = np.quantile(final, [0.05, 0.95])
        count_cover.append(lo <= truth <= hi)
        if example is None and 60 < truth < 150:
            example = (i, fc)

    # Per-lineage AUROC (genes compete within a genome), averaged across lineages.
    aurocs = {
        k: float(np.nanmean([auroc(s, y) for s, y in zip(v, labels)])) for k, v in scores.items()
    }
    metrics["forecast"] = {
        "auroc_which_genes_leave": aurocs,
        "final_gene_count_mae": float(np.mean(count_err)),
        "final_gene_count_coverage_90": float(np.mean(count_cover)),
    }
    for k, v in aurocs.items():
        print(f"    AUROC {k:18s} {v:.3f}")
    print(f"    final organelle gene count: MAE {np.mean(count_err):.1f} genes, "
          f"90% interval coverage {np.mean(count_cover):.2f}")

    i, fc = example if example else (0, forecast(genome, learned, snaps[0],
                                                 inferrer.infer(snaps[0]).sample(200, rng), horizon, rng=rng))
    plot_forecast(test.counts[i, : snap_step + 1], fc, test.counts[i, snap_step:], SNAPSHOT_FRAC,
                  aurocs, out / "fig4_forecast.png")

    (out / "metrics.json").write_text(json.dumps(metrics, indent=2))
    print(f"Done. Figures and metrics written to {out}/")


if __name__ == "__main__":
    main()
