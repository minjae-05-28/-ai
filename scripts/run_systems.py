"""Simulate and learn several endosymbiotic systems side by side.

    python scripts/run_systems.py [--quick]
"""

import argparse
import json
from pathlib import Path

import numpy as np
import torch

from organelle_evo.ancestor import FEATURES
from organelle_evo.plots import plot_systems
from organelle_evo.rules import fit_rules_bootstrap
from organelle_evo.simulator import NUCLEUS, sample_prior, simulate
from organelle_evo.systems import SYSTEMS


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--quick", action="store_true")
    ap.add_argument("--out", default="results")
    ap.add_argument("--seed", type=int, default=0)
    args = ap.parse_args()
    torch.set_num_threads(1)
    out = Path(args.out)
    out.mkdir(exist_ok=True)
    rng = np.random.default_rng(args.seed)
    n_lineages, n_boot = (12, 3) if args.quick else (40, 10)

    results, metrics = {}, {}
    for name, spec in SYSTEMS.items():
        genome = spec.make_ancestor(args.seed)
        world = simulate(genome, spec.true_rules, sample_prior(n_lineages, rng), rng=rng)
        fitted = fit_rules_bootstrap(genome.features, world.states, n_boot=n_boot, seed=args.seed)
        results[name] = (spec, fitted)
        kept = (world.states == 0).sum(1)
        transferred = (world.states == NUCLEUS).mean()
        err_l = np.abs(fitted.loss_weights - spec.true_rules.loss_weights)
        err_t = np.abs(fitted.transfer_weights - spec.true_rules.transfer_weights)
        metrics[name] = {
            "ancestor_genes": genome.n_genes,
            "genes_kept_range": [int(kept.min()), int(kept.max())],
            "fraction_transferred": float(transferred),
            "loss_law_max_abs_error": float(err_l.max()),
            "transfer_law_max_abs_error": None if transferred < 0.01 else float(err_t.max()),
            "learned_loss": dict(zip(FEATURES, map(float, fitted.loss_weights))),
            "learned_transfer": dict(zip(FEATURES, map(float, fitted.transfer_weights))),
        }
        print(f"{name:20s} {spec.ancestor:22s} kept {kept.min()}-{kept.max()} of {genome.n_genes}, "
              f"transferred {transferred:.1%}, loss-law max err {err_l.max():.2f}"
              + ("" if transferred < 0.01 else f", transfer-law max err {err_t.max():.2f}"))
    plot_systems(results, out / "fig5_systems.png")
    (out / "systems_metrics.json").write_text(json.dumps(metrics, indent=2))


if __name__ == "__main__":
    main()
