"""Law card for the forward-evolution experiment (run_forward_evolution.py + run_function_level.py).

    python scripts/save_forward_evolution_law.py      -> laws/forward_evolution_v1.json
"""

import json
from pathlib import Path

from organelle_evo.laws import LAWS_DIR, save_law

R = Path("results/forward_evolution")
TAGS = ("extremophiles", "extremophiles_consensus", "parasites", "parasites_consensus")
KEEP = ("law.fate_accuracy", "no_change.fate_accuracy", "random_same_amount.fate_accuracy",
        "memorisation.fate_accuracy", "law.loss_auroc", "memorisation.loss_auroc", "law.jaccard", "no_change.jaccard",
        "fate_accuracy.law - no_change", "fate_accuracy.law - random_same_amount", "fate_accuracy.law - no_axes_law",
        "amount_error.law", "amount_error.mean_share", "gain_precision.law")
FKEEP = ("law.spearman", "memorisation.spearman", "law.top_hit", "uniform.top_hit", "memorisation.top_hit",
         "spearman.law - memorisation", "mae.law - uniform")


def main():
    val = {}
    for t in TAGS:
        s = json.loads((R / f"{t}.json").read_text())["summary"]
        f = json.loads((R / f"{t}_functions.json").read_text())["summary"]
        val[t] = {"n_pairs": s["n_pairs"], "n_lineages": s["n_lineages"],
                  "family_level": {k: s[k] for k in KEEP if k in s}, "function_level": {k: f[k] for k in FKEEP if k in f}}
    save_law(
        LAWS_DIR / "forward_evolution_v1.json",
        id="forward_evolution_v1",
        scope=("Evolving an ancestor proxy forward with the birth-death law alone (its lineage held out, the amount "
               "of loss predicted from the lifestyle/environment design) and comparing the result with the real "
               "descendant, for extremophile bacteria/archaea and eukaryote parasites, with the proxy as ancestor or a "
               "consensus ancestor (families shared with a close free-living relative)."),
        model="run_forward_evolution.py (200 stochastic replicates per pair) and run_function_level.py (GO-slim and "
              "keyword functions).",
        feature_names=[],
        data={t: {"pairs": v["n_pairs"], "lineages": v["n_lineages"]} for t, v in val.items()},
        validation=val,
        caveats=[
            "Family level: the law beats random choice of the same number of families (fate accuracy +0.06 to +0.08) "
            "but does not beat leaving the ancestor unchanged (extremophiles -0.04 [-0.075, -0.011]; consensus -0.07; "
            "parasites +0.03 and -0.02, intervals include 0).",
            "Function level: the law ranks which functions a lineage loses (Spearman 0.49-0.66, top-5 hits 0.60-0.71 "
            "against 0.14-0.21 for a uniform split), slightly below memorisation (0.56-0.72).",
            "With a consensus ancestor the law's AUROC falls (extremophiles 0.793 -> 0.764, parasites 0.774 -> 0.748): "
            "part of the score came from families only the proxy carried.",
            "The predicted amount of loss is no better than the mean share for extremophiles (0.10 vs 0.08-0.09) and "
            "better for parasites (0.17 vs 0.19-0.22).",
            "Predicted gains are mostly wrong (precision about 0.1-0.15).",
        ],
        contexts={},
    )
    print("law -> laws/forward_evolution_v1.json")


if __name__ == "__main__":
    main()
