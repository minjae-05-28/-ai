"""Learning, validating and forecasting on real gene-content data."""

from dataclasses import dataclass

import numpy as np

from ..ancestor import AncestorGenome
from ..predict import auroc
from ..rules import RetentionLaw, fit_retention, offset_for_count
from ..simulator import ORGANELLE, LOST, Rules, simulate
from .dataset import GeneContentDataset


@dataclass
class LoloResult:
    """Leave-one-lineage-out: predict which genes an unseen lineage keeps, given how many."""

    lineages: list[str]
    auroc_law: np.ndarray  # features-only law (generalises to genes never seen before)
    auroc_prevalence: np.ndarray  # how often the gene is kept elsewhere (memorisation)
    auroc_combined: np.ndarray  # law hazard + gene prevalence


def leave_one_lineage_out(ds: GeneContentDataset, **fit_kwargs) -> LoloResult:
    law_scores, prev_scores, comb_scores = [], [], []
    for i in range(len(ds.lineages)):
        train = np.delete(ds.present, i, axis=0)
        truth = ds.present[i]
        law = fit_retention([(ds.features, train)], **fit_kwargs)
        base = ds.features @ law.weights[0]
        a = offset_for_count(base, truth.sum())
        p_law = np.exp(-np.exp(a + base))
        prevalence = (train.sum(0) + 0.5) / (len(train) + 1)
        law_scores.append(auroc(p_law, truth))
        prev_scores.append(auroc(prevalence, truth))
        comb_scores.append(auroc(np.log(p_law + 1e-12) + np.log(prevalence), truth))
    return LoloResult(ds.lineages, np.array(law_scores), np.array(prev_scores), np.array(comb_scores))


def universality_test(datasets: list[GeneContentDataset], **fit_kwargs) -> dict:
    """Does one law explain every system, or does each system have its own?

    Compares a shared-weight model with per-system weights by AIC (NLL is per
    observation inside the fitter, so rescale to totals).
    """
    blocks = [(d.features, d.present) for d in datasets]
    n_obs = sum(p.size for _, p in blocks)
    n_offsets = sum(len(p) for _, p in blocks)
    n_feat = blocks[0][0].shape[1]
    shared = fit_retention(blocks, groups=[0] * len(blocks), **fit_kwargs)
    separate = fit_retention(blocks, groups=list(range(len(blocks))), **fit_kwargs)
    aic_shared = 2 * shared.final_nll * n_obs + 2 * (n_feat + n_offsets)
    aic_separate = 2 * separate.final_nll * n_obs + 2 * (n_feat * len(blocks) + n_offsets)
    return {
        "aic_shared": aic_shared,
        "aic_separate": aic_separate,
        "delta_aic": aic_shared - aic_separate,  # > 10: strong evidence laws differ
        "shared_weights": shared.weights[0],
        "separate_weights": separate.weights,
    }


@dataclass
class LineageForecast:
    lineage: str
    n_now: int
    at_risk: list[tuple[str, float]]  # (gene, P(gone after horizon)) highest first
    count_quantiles: np.ndarray  # 5/50/95% of genes left after horizon


def forecast_lineages(
    ds: GeneContentDataset,
    law: RetentionLaw,
    offsets: np.ndarray,
    horizon: float = 0.5,
    n_samples: int = 500,
    top: int = 5,
    rng: np.random.Generator | None = None,
) -> list[LineageForecast]:
    """Continue each lineage's evolution under the learned law with the simulator.

    `horizon` is relative to the lineage's elapsed history (0.5 = half as long again).
    """
    rng = rng or np.random.default_rng(0)
    genome = AncestorGenome(
        features=ds.features,
        category=np.zeros(len(ds.genes), dtype=int),
        pathway=np.arange(len(ds.genes)),
        categories=("all",),
    )
    # Combined hazard only: route every departure through the "loss" channel.
    rules = Rules(-50.0, (0.0,) * ds.features.shape[1], 0.0, tuple(law.weights[0]))
    out = []
    for i, name in enumerate(ds.lineages):
        now = np.where(ds.present[i], ORGANELLE, LOST).astype(np.int8)
        params = np.tile([0.0, offsets[i], 0.0], (n_samples, 1))
        res = simulate(genome, rules, params, horizon=horizon, n_steps=20, initial_states=now, rng=rng)
        p_gone = (res.states != ORGANELLE).mean(0)
        kept = np.flatnonzero(ds.present[i])
        order = kept[np.argsort(-p_gone[kept])][:top]
        out.append(
            LineageForecast(
                lineage=name,
                n_now=int(ds.present[i].sum()),
                at_risk=[(ds.genes[g], float(p_gone[g])) for g in order],
                count_quantiles=np.quantile(res.counts[:, -1, ORGANELLE], [0.05, 0.5, 0.95]),
            )
        )
    return out
