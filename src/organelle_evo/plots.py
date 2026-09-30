"""Figures for the README."""

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

from .ancestor import FEATURES, AncestorGenome
from .simulator import ORGANELLE, PARAM_NAMES, STATE_NAMES

STATE_COLORS = ("#2a9d8f", "#e9c46a", "#b0b0b0")


def plot_reduction(genome: AncestorGenome, counts: np.ndarray, states: np.ndarray, path):
    """Genome reduction curves + category composition of ancestor vs descendants."""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 4.8))
    t = np.linspace(0, 1, counts.shape[1])
    for c in counts:
        ax1.plot(t, c[:, ORGANELLE], color=STATE_COLORS[0], alpha=0.35, lw=1)
    ax1.set(xlabel="time since endosymbiosis (relative)", ylabel="genes kept in organelle",
            title="Genome reduction across lineages", yscale="log")

    cats = genome.categories
    by_size = np.argsort((states == ORGANELLE).sum(1))[::-1]
    picks = [by_size[0], by_size[len(by_size) // 2], by_size[-1]]
    labels = ["ancestor", "mildest", "median", "most reduced"]
    stacks = [np.bincount(genome.category, minlength=len(cats))]
    for i in picks:
        kept = states[i] == ORGANELLE
        stacks.append(np.bincount(genome.category[kept], minlength=len(cats)))
    stacks = np.array(stacks)
    cmap = plt.get_cmap("tab20")
    bottom = np.zeros(len(stacks))
    for ci, name in enumerate(cats):
        ax2.bar(labels, stacks[:, ci], bottom=bottom, color=cmap(ci), label=name)
        bottom += stacks[:, ci]
    ax2.set(ylabel="genes in organelle genome", title="What gets kept (by function)")
    ax2.legend(fontsize=7, bbox_to_anchor=(1.02, 1), loc="upper left")
    fig.tight_layout()
    fig.savefig(path, dpi=130)
    plt.close(fig)


def plot_rules(true_rules, fitted, path):
    fig, axes = plt.subplots(1, 2, figsize=(11, 4), sharey=True)
    x = np.arange(len(FEATURES))
    for ax, title, true_w, est, se in [
        (axes[0], "Transfer to nucleus", true_rules.transfer_weights, fitted.transfer_weights, fitted.transfer_se),
        (axes[1], "Gene loss", true_rules.loss_weights, fitted.loss_weights, fitted.loss_se),
    ]:
        ax.bar(x - 0.18, true_w, 0.36, label="true law", color="#264653")
        ax.bar(x + 0.18, est, 0.36, yerr=None if se is None else 1.96 * se, capsize=3,
               label="learned (95% CI)", color="#e76f51")
        ax.axhline(0, color="k", lw=0.6)
        ax.set_xticks(x, [f.replace("_", "\n") for f in FEATURES], fontsize=8)
        ax.set_title(title)
    axes[0].set_ylabel("effect on log hazard")
    axes[0].legend()
    fig.tight_layout()
    fig.savefig(path, dpi=130)
    plt.close(fig)


def plot_inference(true_params, posterior, path, n_show=300):
    fig, axes = plt.subplots(1, len(PARAM_NAMES), figsize=(13, 4))
    for i, (ax, name) in enumerate(zip(axes, PARAM_NAMES)):
        t, m, s = true_params[:n_show, i], posterior.mean[:n_show, i], posterior.std[:n_show, i]
        ax.errorbar(t, m, yerr=1.645 * s, fmt="o", ms=2.5, alpha=0.5, elinewidth=0.6, color="#457b9d")
        lo, hi = t.min(), t.max()
        ax.plot([lo, hi], [lo, hi], "k--", lw=1)
        ax.set(xlabel=f"true {name}", ylabel="inferred (90% interval)", title=name)
    fig.tight_layout()
    fig.savefig(path, dpi=130)
    plt.close(fig)


def plot_forecast(past_counts, forecast, true_future, snapshot_frac, aurocs, path):
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4.3), gridspec_kw={"width_ratios": [1.6, 1]})
    t_past = np.linspace(0, snapshot_frac, len(past_counts))
    t_future = np.linspace(snapshot_frac, 1, forecast.counts.shape[1])
    ax1.plot(t_past, past_counts[:, ORGANELLE], color="k", lw=2, label="observed history")
    q = np.quantile(forecast.counts[:, :, ORGANELLE], [0.05, 0.5, 0.95], axis=0)
    ax1.fill_between(t_future, q[0], q[2], color=STATE_COLORS[0], alpha=0.3, label="forecast 90%")
    ax1.plot(t_future, q[1], color=STATE_COLORS[0], lw=2, label="forecast median")
    ax1.plot(np.linspace(snapshot_frac, 1, len(true_future)), true_future[:, ORGANELLE],
             "--", color="#e76f51", lw=2, label="what actually happened")
    ax1.axvline(snapshot_frac, color="gray", lw=0.8, ls=":")
    ax1.set(xlabel="time (relative)", ylabel="genes kept in organelle",
            title="Forecasting an organelle genome")
    ax1.legend(fontsize=8)

    names, vals = list(aurocs), list(aurocs.values())
    ax2.bar(names, vals, color=["#b0b0b0", "#e76f51", "#264653"])
    for i, v in enumerate(vals):
        ax2.text(i, v + 0.01, f"{v:.3f}", ha="center")
    ax2.set(ylim=(0.5, 1.0), ylabel="AUROC", title="Which genes leave next?")
    fig.tight_layout()
    fig.savefig(path, dpi=130)
    plt.close(fig)
