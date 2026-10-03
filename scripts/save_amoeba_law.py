"""Law card for the amoebozoan ancestral reconstruction (scripts/run_clade_ancestor.py)."""

import argparse
import json
from pathlib import Path

import numpy as np

from organelle_evo.laws import LAWS_DIR, save_law

R = Path("results/clade_ancestor/amoebozoa")
# Marker families, split by what the data can and cannot support.
PANEL = {
    "pseudopodia and phagocytosis": ["Actin", "ARPC4", "FH2", "Cofilin_ADF", "Gelsolin", "Myosin_head", "PX", "SNARE"],
    "aerobic respiration (nuclear-encoded)": ["Complex1_51K", "ATP-synt_D", "NDUFA12", "ATP-synt_ab"],
    "sex and genome upkeep": ["TP6A_N", "Histone", "Telomerase_RBD", "Proteasome", "Cyclin_N"],
    "organelles": ["Pex2_Pex12", "Thioredoxin"],
    "signalling": ["PDEase_I"],
    "flagellum (not supported by this sample)": ["Radial_spoke_3", "IFT57", "IFT52_GIFT", "BBS2_Mid"],
    "mitochondrion-encoded (absent from most UniProt proteomes: an artifact, not loss)":
        ["Complex1_49kDa", "COX2", "COX3", "Cytochrome_B", "NADHdh"],
    "multicellular fruiting body (not supported)": ["Chitin_bind_1", "Lectin_C"],
}


def caveats(s):
    """Written from the run, so the card cannot describe a model the run did not use."""
    v = s["leave_tips_out_auroc"]
    comp, mult = s.get("completeness_model"), s.get("reduced_branch_multiplier", True)
    hgt = json.loads(Path("results/hgt_rate/summary.json").read_text())["sets"]["amoebozoa"]
    out = [
        "Twelve amoebozoan species, eight of them social amoebae. The subsampling experiment "
        "(results/sample_size/summary.json) showed that at this size the node reached is NOT the clade's root "
        "(Jaccard about 0.91 to it) and the ancestor's size is underestimated by 16-17%, so no family count is "
        "quoted and the node is named as the ancestor of the sampled species, not of Amoebozoa.",
        "Mitochondrion-encoded families (COX2, COX3, cytochrome b, complex I 49 kDa) come out low only because "
        "UniProt eukaryote proteomes hold nuclear proteins; the nuclear-encoded respiratory families are high, "
        "so the ancestor respired aerobically.",
        "Flagellar families are low (radial spoke, IFT) but only 1 of the 12 sampled species has them: nearly "
        "every sampled lineage is non-flagellate, so this sample cannot resolve whether the true Amoebozoa root "
        "was flagellate. The published view is that it was.",
        f"Leave-tips-out AUROC {v['reconstruction']:.3f} against {v['clade_frequency']:.3f} for the clade's "
        "present-day family frequency: the margin over the no-tree baseline is small, much smaller than in the "
        "2,623-tip bacterial case."
        + (" This test scores predicting a hidden tip's OBSERVED content, dropout included, which the "
           "completeness model deliberately stops reproducing, so it is not the test that speaks to the "
           "ancestor; the known-truth simulation (results/quality_correction/summary.json) is." if comp else ""),
        f"Horizontal transfer is not modelled. It was measured for this clade at about {hgt['estimated_hgt']} "
        f"(results/hgt_rate/summary.json), below the 0.35 at which ancestor size starts to inflate; the "
        "estimator cannot separate transfer from an intrinsically high gain rate, so read it as an upper bound.",
    ]
    if comp:
        out.append(
            "Entamoeba proteomes are incomplete (BUSCO 37-53%, completeness score 0.43-0.51). That is modelled "
            "as dropout in the likelihood, not as loss."
            + (" The reduced-lineage loss multiplier is ALSO applied on those branches, so the two corrections "
               "overlap; results/clade_ancestor/amoebozoa_v3_nomult holds the run without it."
               if mult else " The reduced-lineage loss multiplier is switched off here, so incompleteness is "
                            "corrected once."))
    else:
        out.append("Entamoeba proteomes are incomplete (BUSCO 37-53%), which is why loss is accelerated on their "
                   "branches; that is a modelling assumption, not a measurement. amoeba_ancestor_v2 replaces it "
                   "with a dropout term fitted from the data.")
    return out


def main():
    global R
    ap = argparse.ArgumentParser()
    ap.add_argument("--dir", default="results/clade_ancestor/amoebozoa")
    ap.add_argument("--id", default="amoeba_ancestor_v1")
    args = ap.parse_args()
    R = Path(args.dir)
    s = json.loads((R / "summary.json").read_text())
    z = np.load(R / "posterior.npz", allow_pickle=False)
    col = {f: i for i, f in enumerate(z["families"])}
    panel = {}
    for group, fams in PANEL.items():
        panel[group] = {f: {"posterior": round(float(z["posterior"][col[f]]), 3),
                            "model_sd": round(float(z["model_sd"][col[f]]), 3),
                            "tree_sd": round(float(z["tree_sd"][col[f]]), 3),
                            "share_of_clade_tips_today": round(float(z["clade_frequency"][col[f]]), 3)}
                        for f in fams if f in col}
    save_law(
        LAWS_DIR / f"{args.id}.json",
        id=args.id,
        scope=("Gene-family (Pfam) content of the common ancestor of the sampled Amoebozoa (social amoebae, "
               "Entamoeba, Acanthamoeba, Planoprotostelium), reconstructed on a ribosomal-marker tree from "
               "UniProt proteomes. Family presence only; no sequences, no cell size or shape."),
        model=("Two-state gain/loss Markov chain per family, ensemble of the five leading models of the "
               "mitochondrial model search (their differences were inside the interval), with loss accelerated on "
               "the reduced Entamoeba branches; 20 bootstrap trees for phylogenetic spread."
               + (" Incomplete proteomes are handled as dropout in the likelihood (completeness estimated from "
                  "in-clade marker families) rather than as accelerated loss on their branch."
                  if s.get("completeness_model") else "")),
        feature_names=[],
        data={"clade_tips": s["clade_tips"], "clade_species": s["clade_species"], "outgroup_tips":
              s["tips"] - s["clade_tips"], "families_considered": s["families_considered"],
              "tree": "results/phylo_tree/amoeba.nwk (40 species, 34 ribosomal families, 23,907 columns)"},
        validation={"leave_tips_out_auroc": s["leave_tips_out_auroc"],
                    "tip_completeness": s.get("tip_completeness"),
                    "measured_hgt_level": json.loads(
                        Path("results/hgt_rate/summary.json").read_text())["sets"]["amoebozoa"]["estimated_hgt"],
                    "n_confident_families": s["n_confident_families"],
                    "n_uncertain_families": s["n_uncertain_families"],
                    "marker_panel": panel},
        caveats=caveats(s),
        contexts={},
    )
    print("law -> laws/amoeba_ancestor_v1.json")


if __name__ == "__main__":
    main()
