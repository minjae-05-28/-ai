"""AI part 3: forecast future evolution from a present-day organelle genome.

Pipeline: posterior samples of the lineage's hidden parameters (from the inferrer)
-> continue the simulator forward from the current state under the learned rules
-> per-gene probabilities of each future state and gene-count trajectories.
"""

from dataclasses import dataclass

import numpy as np

from .ancestor import AncestorGenome
from .simulator import ORGANELLE, Rules, simulate


@dataclass
class Forecast:
    state_probs: np.ndarray  # (G, 3) probability of each state at the horizon
    counts: np.ndarray  # (n_samples, n_steps + 1, 3) trajectories

    @property
    def p_leaves_organelle(self) -> np.ndarray:
        return 1.0 - self.state_probs[:, ORGANELLE]


def forecast(
    genome: AncestorGenome,
    rules: Rules,
    current_states: np.ndarray,
    param_samples: np.ndarray,
    horizon: float,
    *,
    n_steps: int = 50,
    rng: np.random.Generator | None = None,
) -> Forecast:
    """`horizon` is relative to the elapsed history (0.5 = half as long again)."""
    result = simulate(
        genome,
        rules,
        param_samples,
        horizon=horizon,
        n_steps=n_steps,
        initial_states=current_states,
        rng=rng,
    )
    probs = np.stack([(result.states == s).mean(0) for s in range(3)], axis=1)
    return Forecast(state_probs=probs, counts=result.counts)


def category_baseline(genome: AncestorGenome, current_states: np.ndarray) -> np.ndarray:
    """Naive baseline: a gene's risk = fraction of its category already gone."""
    gone = current_states != ORGANELLE
    score = np.zeros(genome.n_genes)
    for c in np.unique(genome.category):
        mask = genome.category == c
        score[mask] = gone[mask].mean()
    return score


def auroc(scores: np.ndarray, labels: np.ndarray) -> float:
    """Rank-based AUROC (Mann-Whitney U), ties get average rank."""
    scores, labels = np.asarray(scores, float), np.asarray(labels, bool)
    n_pos, n_neg = labels.sum(), (~labels).sum()
    if n_pos == 0 or n_neg == 0:
        return float("nan")
    order = np.argsort(scores, kind="mergesort")
    ranks = np.empty(len(scores))
    sorted_scores = scores[order]
    i = 0
    while i < len(scores):
        j = i
        while j + 1 < len(scores) and sorted_scores[j + 1] == sorted_scores[i]:
            j += 1
        ranks[order[i : j + 1]] = (i + j) / 2 + 1
        i = j + 1
    return float((ranks[labels].sum() - n_pos * (n_pos + 1) / 2) / (n_pos * n_neg))
