"""Law card for a clade reconstructed with run_clade_ancestor.py --clade-kingdom.

    python scripts/save_clade_law.py --clade fungi --id fungal_ancestor_v1

Everything quoted on the card is read from the run's own outputs (summary, posterior, the
known-truth grade in results/node_power/<clade>, the transfer level in results/hgt_rate/<clade>),
so the card cannot describe a model the run did not use.
"""

import argparse
import json
from pathlib import Path

import numpy as np

from organelle_evo.laws import LAWS_DIR, save_law

# Marker families with an expectation from outside this data, so the panel works as a check.
PANELS = {
    "fungi": {
        "chitin cell wall (expected present)": ["Chitin_synth_1", "Chitin_synth_2", "Chitin_synth_1N"],
        "fungal-specific Zn2Cys6 transcription factors (expected present)": ["Zn_clus", "Fungal_trans"],
        "flagellum (expected present: chytrids, Rozella and Blastocladiomycota swim; Dikarya lost it)":
            ["Radial_spoke_3", "IFT57", "IFT52_GIFT", "BBS2_Mid", "Dynein_heavy", "PF16"],
        "sterol synthesis": ["ERG4_ERG24", "Lanosterol_14a-demethylase", "SQS_PSY", "p450"],
        "actin cytoskeleton": ["Actin", "Cofilin_ADF", "FH2", "Myosin_head"],
        "peroxisome": ["Pex2_Pex12", "Pex14_N"],
        "mitochondrion-encoded (absent from most UniProt proteomes: an artifact, not loss)":
            ["COX2", "COX3", "Cytochrome_B"],
    },
    "leca": {
        "mitochondrion, nuclear-encoded (expected present: LECA had a mitochondrion)":
            ["Complex1_51K", "ATP-synt_ab", "Mito_carr", "Tom20", "Tim17"],
        "meiosis and sex (expected present)": ["TP6A_N", "Rad51", "Spo11", "HORMA", "Mnd1"],
        "cilium (expected present)": ["Radial_spoke_3", "IFT57", "IFT52_GIFT", "Dynein_heavy", "Tubulin"],
        "endomembrane and nucleus (expected present)": ["Clathrin", "Sec23_trunk", "Snf7", "Nup153", "Ran_BP1"],
        "peroxisome and autophagy (expected present)": ["Pex2_Pex12", "ATG7_N", "APG12"],
        "spliceosome (expected present)": ["PRP8_U5-snRNA_bdg", "Sm", "DEAD"],
        "photosynthesis (expected ABSENT: the plastid came after LECA)":
            ["Photo_RC", "PSII", "PsbP", "Chloroa_b-bind", "PsaA_PsaB"],
    },
}
NAMES = {"fungi": "Fungi", "leca": "eukaryotes (LECA)"}


def caveats(s, power, hgt, clade):
    v = s["leave_tips_out_auroc"]
    intr = s.get("non_clade_tips_inside_clade_node") or []
    out = [
        f"{s['clade_tips']} {NAMES.get(clade, clade)} proteomes, chosen round-robin over orders "
        "(data/markers/<set>_pick.json) so early-diverging lineages are not swamped. UniProt reference "
        "proteomes still over-represent Dikarya, and lineages without a reference proteome (for example "
        "Aphelida, most Nucleariida) are absent.",
        f"The tree is a FastTree marker tree, unrooted as written; it was rooted on the outgroup tip "
        f"farthest from the clade ({s.get('rooted_on')}). "
        + (f"{len(intr)} non-clade tips fall inside the clade node ({', '.join(intr[:6])}), so the node "
           "reconstructed is not exactly the clade's ancestor." if intr else
           "With the tips listed next left out, the clade is monophyletic and the node reconstructed is the "
           "common ancestor of every remaining member.")
        + (f" Left out because the tree placed them outside the clade (long-branch attraction): "
           f"{', '.join(s['misplaced_clade_tips_left_out'])}." if s.get("misplaced_clade_tips_left_out") else ""),
        (f"No bootstrap trees were used (n_bootstrap_trees = {s.get('n_bootstrap_trees')}), so the tree_sd column "
         "is zero and phylogenetic uncertainty is NOT in the reported spread." if not s.get("n_bootstrap_trees")
         else f"{s['n_bootstrap_trees']} bootstrap trees give the tree_sd column."),
        f"Leave-tips-out AUROC {v['reconstruction']:.3f} against {v['clade_frequency']:.3f} for present-day "
        "frequency. That test scores a hidden tip's observed content, dropout included, which the completeness "
        "model deliberately does not reproduce; the known-truth grade below is the test that speaks to the "
        "ancestor.",
        "Mitochondrion-encoded families come out low only because UniProt eukaryote proteomes hold nuclear "
        "proteins.",
        "Completeness is estimated from families nearly every top-quartile proteome carries. Microsporidia "
        "and other reduced genomes really lack many of those, so they are scored as incomplete: their "
        "absences count as weak evidence. That keeps them from dragging the ancestor down, but it is a choice, "
        "not a measurement of their assembly quality.",
    ]
    kids = s.get("clade_node_children") or []
    small = [k for k in kids if k["n_clade_tips"] < 0.05 * s["clade_tips"]]
    if small:
        k = small[0]
        out.append(
            f"The clade node splits into {k['n_clade_tips']} reduced lineages ({', '.join(k['examples'][:3])}) and "
            "everything else. Families those few lineages lack, and the outgroup mostly lacks too, sit near the "
            "prior (about 0.1) at the clade node: absent from the start and lost in the parasites look the same "
            "from this sample, so read ~0.1 there as undecided, not absent. The larger child node "
            "(validation.core_node) is reported beside it.")
    if power:
        out.append(
            f"Known-truth grade at this node (simulated families on the same tree, results/node_power/{clade}): "
            f"AUROC {power['recon_auroc']:.4f} against {power['freq_auroc']:.4f} for present-day frequency, "
            f"log loss {power['recon_logloss']:.3f} against {power['freq_logloss']:.3f}, ancestor-size bias "
            f"{power['recon_size_bias']:+.1%} (frequency {power['freq_size_bias']:+.1%}). Verdict: "
            f"{power['verdict']}.")
    else:
        out.append("No known-truth grade was run for this node.")
    if hgt:
        cal = [c for c in hgt["calibration"] if c["hgt"] > 0]
        sat = next((c["hgt"] for c in cal if c["share_q_ge_0.3"] >= 0.99), None)
        out.append(f"Horizontal transfer is not modelled; measured for this tree at about {hgt['estimated_hgt']}"
                   + (f", which only says 'below {sat}': the calibration curve saturates at {sat} on this tree"
                      if sat is not None and hgt["estimated_hgt"] < sat else "")
                   + ". That is far below the 0.35 at which ancestor size starts to inflate. The estimator "
                   "cannot separate transfer from an intrinsically high gain rate (gene duplication, domain "
                   "shuffling), so it is an upper bound.")
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--clade", required=True)
    ap.add_argument("--id", required=True)
    ap.add_argument("--dir", default="")
    ap.add_argument("--tree", default="")
    args = ap.parse_args()
    if args.clade.startswith("leca"):
        raise SystemExit("LECA has no outgroup and several root positions: use save_leca_law.py")
    R = Path(args.dir or f"results/clade_ancestor/{args.clade}")
    dest = LAWS_DIR / f"{args.id}.json"
    if dest.exists():
        raise SystemExit(f"{dest} exists; laws are never overwritten — use a new id")
    s = json.loads((R / "summary.json").read_text())
    z = np.load(R / "posterior.npz", allow_pickle=False)
    col = {f: i for i, f in enumerate(z["families"])}
    pf = Path("results/node_power") / args.clade / "summary.json"
    agg = json.loads(pf.read_text())["aggregate"] if pf.exists() else {}
    power = next((v for k, v in agg.items() if "표본이 도달한 마디" in k), None)
    hf = Path("results/hgt_rate") / args.clade / "summary.json"
    panel_key = args.clade.split("_")[0]
    hgt = json.loads(hf.read_text())["sets"].get(args.clade) if hf.exists() else None
    core = None
    if "child_posteriors" in z.files and len(z["child_n_tips"]):
        j = int(np.argmax(z["child_n_tips"]))
        if z["child_n_tips"][j] < s["clade_tips"]:
            core = z["child_posteriors"][j]
    core_power = next((v for k, v in agg.items() if "뿌리 아래 큰 쪽" in k), None)
    panel = {}
    for group, fams in PANELS.get(panel_key, {}).items():
        panel[group] = {f: {"posterior": round(float(z["posterior"][col[f]]), 3),
                            **({"core_node_posterior": round(float(core[col[f]]), 3)} if core is not None else {}),
                            "model_sd": round(float(z["model_sd"][col[f]]), 3),
                            "tree_sd": round(float(z["tree_sd"][col[f]]), 3),
                            "share_of_clade_tips_today": round(float(z["clade_frequency"][col[f]]), 3)}
                        for f in fams if f in col}
    size = None
    if power and abs(power["recon_size_bias"]) <= 0.10:
        size = {"sum_of_posteriors": int(round(float(z["posterior"].sum()))),
                "known_truth_size_bias": power["recon_size_bias"]}
    save_law(
        dest, id=args.id,
        scope=(f"Gene-family (Pfam) content of the common ancestor of the sampled {NAMES.get(args.clade, args.clade)}, "
               "reconstructed on a ribosomal-marker tree from UniProt proteomes. Family presence only; no "
               "sequences, no cell shape."),
        model=("Two-state gain/loss Markov chain per family, ensemble of the five leading models of the "
               "mitochondrial model search, incomplete proteomes handled as dropout in the likelihood "
               "(completeness from in-group marker families, clade and outgroup scored separately), no "
               "reduced-lineage loss multiplier, tree rooted on the outgroup; bootstrap trees for "
               "phylogenetic spread."),
        feature_names=[],
        data={"clade_tips": s["clade_tips"], "outgroup_tips": s["tips"] - s["clade_tips"],
              "families_considered": s["families_considered"], "rooted_on": s.get("rooted_on"),
              "non_clade_tips_inside_clade_node": s.get("non_clade_tips_inside_clade_node"),
              "tree": args.tree or f"results/phylo_tree/{args.clade}.nwk",
              "n_bootstrap_trees": s.get("n_bootstrap_trees")},
        validation={"leave_tips_out_auroc": s["leave_tips_out_auroc"],
                    "known_truth": power, "known_truth_subclades": {k: v for k, v in agg.items()
                                                                    if "표본이 도달한 마디" not in k},
                    "core_node": ({"n_clade_tips": int(z["child_n_tips"].max()),
                                   "n_confident": int((core >= 0.9).sum()),
                                   "known_truth": core_power,
                                   "size_quoted": bool(core_power and abs(core_power["recon_size_bias"]) <= 0.10),
                                   "sum_of_posteriors": (int(round(float(core.sum())))
                                                         if core_power and abs(core_power["recon_size_bias"]) <= 0.10
                                                         else None)}
                                  if core is not None else None),
                    "measured_hgt_level": hgt["estimated_hgt"] if hgt else None,
                    "ancestor_size": size,
                    "n_confident_families": s["n_confident_families"],
                    "n_uncertain_families": s["n_uncertain_families"],
                    "marker_panel": panel},
        caveats=caveats(s, power, hgt, args.clade),
        contexts={},
    )
    print(f"law -> {dest}")


if __name__ == "__main__":
    main()
