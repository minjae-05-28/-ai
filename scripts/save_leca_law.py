"""Law card for LECA, from results/clade_ancestor/leca (scripts/combine_leca.py).

    python scripts/save_leca_law.py --id leca_ancestor_v1

The card reports what holds under every root tested and lists, with the reason, the root
positions that could not be tested on this tree.
"""

import argparse
import json
from pathlib import Path

import numpy as np

from organelle_evo.laws import LAWS_DIR, save_law
from save_clade_law import PANELS

# Root positions proposed in the literature that the tree could not represent, and why
# (filled from the attempt in this run; see run_clade_ancestor.py --root-split).
NOT_TESTED = {
    "Amorphea (Opisthokonta + Amoebozoa + Apusozoa | rest; the unikont-bikont root)":
        "not a split of this marker tree: 15 of 103 amorphean tips (all 9 Amoebozoa, Thecamonas, the "
        "Microsporidia) sit outside the largest amorphean-only subtree",
    "Metamonada | rest":
        "only 2 metamonads reached the tree (most metamonad proteomes had too few ribosomal markers) and they "
        "do not group together",
}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--id", required=True)
    ap.add_argument("--prefix", default="leca")
    ap.add_argument("--not-tested", default="",
                    help="JSON {root: reason} for this run; default: the v1 list in NOT_TESTED")
    ap.add_argument("--tree-note", default="", help="one sentence on how the tree was built")
    args = ap.parse_args()
    not_tested = json.loads(args.not_tested) if args.not_tested else NOT_TESTED
    pre = args.prefix
    dest = LAWS_DIR / f"{args.id}.json"
    if dest.exists():
        raise SystemExit(f"{dest} exists; laws are never overwritten — use a new id")
    R = Path(f"results/clade_ancestor/{pre}")
    s = json.loads((R / "summary.json").read_text())
    z = np.load(R / "posterior.npz", allow_pickle=False)
    roots = [str(r) for r in z["roots"]]
    col = {str(f): i for i, f in enumerate(z["families"])}
    P = z["per_root"]
    grades = {}
    pf = Path(f"results/node_power/{pre}/summary.json")
    if pf.exists():
        for k, v in json.loads(pf.read_text())["aggregate"].items():
            if k.startswith("뿌리 "):
                grades[k[3:]] = v
    hg = json.loads(Path(f"results/hgt_rate/{pre}/summary.json").read_text()) if Path(
        f"results/hgt_rate/{pre}/summary.json").exists() else {}
    panel = {}
    for group, fams in PANELS["leca"].items():
        panel[group] = {f: {**{f"posterior_{r}": round(float(P[k, col[f]]), 3) for k, r in enumerate(roots)},
                            "share_of_tips_today": round(float(z["clade_frequency"][col[f]]), 3)}
                        for f in fams if f in col}
    sizes = {r: s["sum_of_posteriors_per_root"][r] for r in roots}
    quote = bool(grades) and all(abs(grades[r]["recon_size_bias"]) <= 0.10 for r in roots if r in grades) \
        and len(grades) == len(roots)
    strays = {r: json.loads(Path(f"results/clade_ancestor/{pre}_{r}/summary.json").read_text()).get(
        "misplaced_clade_tips_left_out") for r in roots}
    cav = [
        f"{s['clade_tips']} eukaryote proteomes reached the tree out of 300 picked with an equal share per "
        f"supergroup (data/markers/{pre}_pick.json; pick_eukaryotes.py). UniProt has very few proteomes for "
        "Metamonada, Rhizaria, Haptista, Cryptista, CRuMs and Hemimastigophora, so those lineages are thin or "
        "absent, and the deepest-branching candidates are exactly the ones least sampled.",
        "No prokaryote outgroup: at this distance gene-content models cannot place the root, so the tree is "
        "rooted on a named split and the root position is treated as unknown. Root positions tested: "
        + ", ".join(roots) + ". A family is called present in LECA only if P >= 0.9 under every tested root; "
        f"the 'posterior' column of results/clade_ancestor/{pre} is the minimum over roots.",
        "Root positions NOT tested, with the reason: "
        + ("; ".join(f"{k}: {v}" for k, v in not_tested.items()) or "none") + ".",
        "Tips left out because the tree placed them outside their group (long-branch attraction): "
        + "; ".join(f"{r}: {', '.join(v) if v else 'none'}" for r, v in strays.items()) + ".",
        "Bootstrap trees used per root: " + ", ".join(
            f"{r} {json.loads(Path(f'results/clade_ancestor/{pre}_{r}/summary.json').read_text()).get('n_bootstrap_trees')}"
            for r in roots)
        + " of the 9 the time-capped build produced (a bootstrap tree on which the root split does not hold is "
        "skipped); the tree_sd of each root run includes them.",
        "Mitochondrion-encoded families (COX2, COX3, cytochrome b) come out low only because UniProt eukaryote "
        "proteomes hold nuclear proteins.",
        "Completeness is scored once across all sampled eukaryotes (no outgroup): near-universal families "
        "among the top-quartile proteomes. Reduced parasites (Microsporidia, Cryptosporidium, Giardia-like "
        "lineages) score low and their absences count as weak evidence.",
        f"Present under every root: {s['n_confident_families']} families; root-dependent: "
        f"{s['n_uncertain_families']}; absent under every root: {s['n_robust_absent']}. Families present per "
        f"root: {s['n_present_per_root']}.",
    ]
    for r, g in grades.items():
        cav.append(f"Known-truth grade with the {r} root: AUROC {g['recon_auroc']:.4f} against "
                   f"{g['freq_auroc']:.4f} for present-day frequency, log loss {g['recon_logloss']:.3f} against "
                   f"{g['freq_logloss']:.3f}, ancestor-size bias {g['recon_size_bias']:+.1%}. Verdict: {g['verdict']}.")
    if grades:
        worst = min(grades.values(), key=lambda g: g["recon_auroc"])
        cav.append(
            "Read the known-truth grades above as the main limit of this card. The tree beats the no-tree "
            "baseline under every root, but the absolute quality is far below the other ancestors in this project "
            f"(lowest AUROC {worst['recon_auroc']:.3f}; fungi 0.850, plastid 0.995), and the size bias runs in "
            "opposite directions under the two roots. So no family count is quoted, and the families are a "
            "ranking: the robust-present list (high under every root) and the expected-marker panel are what "
            "the data support. Deep eukaryote splits on a FastTree ribosomal tree of ~250 species are the weak "
            "link.")
    if hg:
        cav.append(f"Horizontal transfer is not modelled; measured per root at {hg.get('per_root')}. The estimator "
                   "cannot separate transfer from duplication or domain shuffling, so read it as an upper bound.")
    save_law(
        dest, id=args.id,
        scope=("Gene-family (Pfam) content of the last eukaryotic common ancestor (LECA), reconstructed on a "
               "ribosomal-marker tree of supergroup-balanced UniProt proteomes under several root positions; "
               "reported as what holds under every root. Family presence only; no sequences."),
        model=("Two-state gain/loss Markov chain per family, ensemble of the five leading models of the "
               "mitochondrial model search, incomplete proteomes as dropout in the likelihood, no reduced-lineage "
               "multiplier; one run per root position (rooted on the named split), combined by minimum."),
        feature_names=[],
        data={"tips": s["tips"], "families_considered": s["families_considered"], "roots_tested": roots,
              "roots_not_testable": not_tested, "tree": f"results/phylo_tree/{pre}.nwk",
              "tree_method": args.tree_note or "FastTree LG+gamma, unconstrained",
              "n_bootstrap_trees": s.get("n_bootstrap_trees")},
        validation={"leave_tips_out_auroc_per_root": s["leave_tips_out_auroc_per_root"],
                    "known_truth_per_root": grades,
                    "ancestor_size_per_root": ({r: {"sum_of_posteriors": sizes[r],
                                                    "known_truth_size_bias": grades[r]["recon_size_bias"]}
                                                for r in roots} if quote else None),
                    "n_present_every_root": s["n_confident_families"],
                    "n_root_dependent": s["n_uncertain_families"],
                    "n_absent_every_root": s["n_robust_absent"],
                    "marker_panel": panel},
        caveats=cav, contexts={},
    )
    print(f"law -> {dest}")


if __name__ == "__main__":
    import sys
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    main()
