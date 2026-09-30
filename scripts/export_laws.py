"""Freeze the laws learned from real endosymbiont genomes into laws/.

    python scripts/export_laws.py [--metrics results/real/metrics.json]
"""

import argparse
import json
from pathlib import Path

from organelle_evo.laws import LAWS_DIR, save_law
from organelle_evo.realdata.genes import FEATURE_NAMES


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--metrics", default="results/real/metrics.json")
    ap.add_argument("--id", default="endosymbiosis_v1")
    args = ap.parse_args()
    m = json.loads(Path(args.metrics).read_text())
    systems = [s for s in m if s != "universality"]
    contexts = {
        s: {
            f: {
                "weight": round(m[s]["law"][f]["weight"], 4),
                "ci95": [round(m[s]["law"][f]["weight"] - 1.96 * m[s]["law"][f]["se"], 4),
                         round(m[s]["law"][f]["weight"] + 1.96 * m[s]["law"][f]["se"], 4)],
            }
            for f in FEATURE_NAMES
        }
        for s in systems
    }
    save_law(
        LAWS_DIR / f"{args.id}.json",
        id=args.id,
        scope=(
            "Reductive genome evolution under obligate endosymbiosis: which genes an "
            "endosymbiont or organelle genome keeps versus loses/transfers. Not valid for "
            "free-living organisms, and it cannot describe gene gain."
        ),
        model=(
            "Retention hazard: P(gene still encoded) = exp(-exp(a_lineage + x @ w)). "
            "Positive weight = leaves the organelle/symbiont genome faster."
        ),
        feature_names=list(FEATURE_NAMES),
        feature_definitions={
            "hydrophobicity_gravy": "Kyte-Doolittle GRAVY of the protein, z-scored within system",
            "tm_helices": "log(1 + predicted TM helices), z-scored within system",
            "protein_length": "log protein length, z-scored within system",
            "redox_core": "respiratory/photosynthetic electron-transport subunit (0/1)",
            "atp_synthase": "ATP synthase subunit (0/1)",
            "translation": "ribosomal protein, translation factor or aa-tRNA synthetase (0/1)",
            "transcription": "RNA polymerase subunit or sigma factor (0/1)",
            "protein_targeting": "Sec/Tat/SRP translocation or cytochrome c maturation (0/1)",
        },
        data={
            s: {"n_genomes": m[s]["n_genomes"], "n_genes": m[s]["n_genes"],
                "heldout_auroc_features_only": round(m[s]["lolo_auroc"]["law_features_only"], 3)}
            for s in systems
        },
        universality_delta_aic=round(m["universality"]["delta_aic_shared_minus_separate"], 1),
        caveats=[
            "Lineages are treated as independent; phylogenetic non-independence makes "
            "the confidence intervals too narrow.",
            "Gene matching: annotation names plus reciprocal-best-hit homology; fast-evolving "
            "genes can still be missed, inflating loss.",
            "Associations, not demonstrated causes.",
        ],
        contexts=contexts,
    )
    print(f"wrote {LAWS_DIR / (args.id + '.json')}")


if __name__ == "__main__":
    main()
