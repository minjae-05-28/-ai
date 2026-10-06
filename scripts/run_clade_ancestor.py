"""Ancestral gene-family content of a clade, from a marker tree and UniProt proteomes.

    python scripts/run_clade_ancestor.py --tree results/phylo_tree/amoeba.nwk \
        --clade-genera Acanthamoeba,Balamuthia,Cavenderia,Dictyostelium,Entamoeba,Heterostelium,\
Pelomyxa,Planoprotostelium,Polysphondylium,Physarum,Vermamoeba,Mastigamoeba,Tieghemostelium \
        --name amoebozoa

Generalises scripts/run_mito_ancestor.py to any clade: the tree comes from
scripts/ribosomal_tree.py (tips are organism names), the gene families from the UniProt shards,
and the model from the search in results/mito_models (the top models are statistically
indistinguishable, so the ensemble of the leaders is used and their spread is the uncertainty).

What is reported, following the measured limits:
  - per-family posterior at the node the sampled tips actually reach, with the ensemble spread
  - the bootstrap trees' spread, so phylogenetic uncertainty is included
  - function summary of the families above a threshold
  - NOT the ancestor's gene-family count: at this sample size the simulation showed a 16-17%
    underestimate (results/sample_size/summary.json), and the node reached is not the clade's
    root (Jaccard 0.91 to it), so only the ranking and the functions are quoted.
Validation: leave-tips-out on the clade, against family frequency among the clade's tips.
"""

import argparse
import gzip
import json
import re
import sys
from collections import Counter
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
from mito_model_search import fit, posterior  # noqa: E402
from run_mito_ancestor import functions_of, parse_newick, postorder, prune  # noqa: E402

from organelle_evo.predict import auroc  # noqa: E402

# The round-4 leaders of the model search; their differences were inside the interval.
ENSEMBLE = [
    {"ratio": None, "root": "stationary", "min_busco": 0, "drop_mag": False, "mult": 10.0, "tip_mult": 2.0},
    {"ratio": None, "root": "stationary", "min_busco": 0, "drop_mag": False, "mult": 14.0, "tip_mult": 2.0},
    {"ratio": None, "root": "stationary", "min_busco": 0, "drop_mag": False, "mult": 14.0, "tip_mult": 1.0},
    {"ratio": None, "root": "stationary", "min_busco": 0, "drop_mag": False, "mult": 20.0, "tip_mult": 2.0},
    {"ratio": None, "root": "stationary", "min_busco": 0, "drop_mag": False, "mult": 10.0, "tip_mult": 3.0},
]


def load_profiles():
    """organism -> profile. Collections were re-run, so an organism can appear in several shards;
    the richest profile wins rather than whichever file sorted last."""
    out = {}
    for f in sorted(Path("data/uniprot/shards").glob("*.json.gz")):
        for v in json.loads(gzip.open(f, "rt").read()).values():
            if v["n_proteins"] > 0 and v["pfam"]:
                old = out.get(v["organism"])
                if old is None or len(v["pfam"]) > len(old["pfam"]):
                    out[v["organism"]] = v
    return out


def reroot(parent, length, label, tip):
    """The same unrooted tree, rooted at the midpoint of the branch above `tip` (root = node 0).

    FastTree trees are unrooted: the root it writes is an arbitrary trifurcation, which can sit
    inside the clade. Then the "common ancestor of the clade tips" is the whole tree's root and the
    outgroup is reconstructed as part of the clade."""
    n = len(parent)
    adj = [[] for _ in range(n)]
    for v in range(n):
        if parent[v] != -1:
            adj[v].append((parent[v], length[v]))
            adj[parent[v]].append((v, length[v]))
    up, half = parent[tip], length[tip] / 2
    new_parent, new_len, new_label, old = [-1], [0.0], [""], [-1]
    idx = {}
    stack = []
    for start in (tip, up):
        new_parent.append(0), new_len.append(half), new_label.append(label[start]), old.append(start)
        idx[start] = len(new_parent) - 1
        stack.append((start, tip if start == up else up))
    while stack:
        v, came = stack.pop()
        for w, bl in adj[v]:
            if w == came:
                continue
            new_parent.append(idx[v]), new_len.append(bl), new_label.append(label[w]), old.append(w)
            idx[w] = len(new_parent) - 1
            stack.append((w, v))
    # an old degree-2 root becomes a unary node: collapse it through prune's own rule
    P, L = np.array(new_parent), np.array(new_len)
    tips = [v for v in range(len(P)) if v not in set(P.tolist())]
    return prune(P, L, new_label, tips)[:3]


def farthest_outgroup_tip(parent, length, tips, is_clade):
    """The non-clade tip with the largest mean path length to the clade tips (two-pass tree sums)."""
    order, children = postorder(parent)
    n = len(parent)
    cnt, down = np.zeros(n), np.zeros(n)
    for v in order:
        if v in tips and is_clade[v]:
            cnt[v] = 1
        for c in children[v]:
            cnt[v] += cnt[c]
            down[v] += down[c] + cnt[c] * length[c]
    total = cnt[0]
    allsum = down.copy()
    for v in reversed(order):
        for c in children[v]:
            allsum[c] = allsum[v] + (total - 2 * cnt[c]) * length[c]
    out = [v for v in tips if not is_clade[v]]
    return max(out, key=lambda v: (allsum[v], -v)) if out and total else None


def build(tree_path, clade_genera, min_families, clade_kingdom=None, root_outgroup=False):
    txt = Path(tree_path).read_text()
    parent, length, label = parse_newick(txt)
    label = [lab.strip("'") for lab in label]
    prof = load_profiles()
    order, children = postorder(parent)
    tips = [v for v in range(len(parent)) if not children[v]]
    keep = [v for v in tips if label[v] in prof and len(prof[label[v]]["pfam"]) >= min_families]
    dropped = [label[v] for v in tips if v not in set(keep)]
    parent, length, label2, old = prune(parent, length, label, keep)
    rooted_on = None
    if root_outgroup:
        tips2 = [v for v in range(len(parent)) if v not in set(parent.tolist())]
        hit = {v: (prof[label2[v]].get("kingdom") == clade_kingdom if clade_kingdom
                   else label2[v].split()[0] in clade_genera) for v in tips2}
        t = farthest_outgroup_tip(parent, np.maximum(length, 1e-6), set(tips2), hit)
        if t is not None:
            rooted_on = label2[t]
            parent, length, label2 = reroot(parent, length, label2, t)
    order, children = postorder(parent)
    d = {"parent": parent, "length": np.maximum(length, 1e-6), "order": order, "children": children}
    d["tips"] = [v for v in range(len(parent)) if not children[v]]
    depth = np.zeros(len(parent))
    for v in reversed(order):
        if v:
            depth[v] = depth[parent[v]] + d["length"][v]
    d["depth"] = depth
    names = {v: label2[v] for v in d["tips"]}
    # Genus match alone is not enough: UniProt carries "Acanthamoeba polyphaga mimivirus", a virus
    # whose first word is an amoeba genus. Require the kingdom the matched tips mostly belong to.
    # With clade_kingdom the clade is that whole kingdom (fungi: hundreds of genera).
    byname = {v: (names[v].split()[0] in clade_genera) if not clade_kingdom else True for v in d["tips"]}
    kings = Counter(prof[names[v]].get("kingdom") for v, hit in byname.items() if hit)
    king = clade_kingdom or (kings.most_common(1)[0][0] if kings else None)
    in_clade = {v: bool(hit and prof[names[v]].get("kingdom") == king) for v, hit in byname.items()}
    wrong_kingdom = [names[v] for v, hit in byname.items() if hit and not in_clade[v]]
    if wrong_kingdom and not clade_kingdom:
        print(f"  dropped from the clade (kingdom is not {king}): {wrong_kingdom}")
    counts = Counter(f for v in d["tips"] for f in prof[names[v]]["pfam"])
    fams = sorted(f for f, c in counts.items() if c >= 3)
    col = {f: j for j, f in enumerate(fams)}
    X = np.zeros((len(parent), len(fams)), dtype=bool)
    for v in d["tips"]:
        X[v, [col[f] for f in prof[names[v]]["pfam"] if f in col]] = True
    d["X"] = X
    d["busco"] = np.full(len(parent), np.nan)
    for v in d["tips"]:
        m = re.search(r"C:([\d.]+)%", prof[names[v]].get("busco") or "")
        d["busco"][v] = float(m.group(1)) if m else np.nan
    d["mag"] = np.zeros(len(parent), dtype=bool)
    # Completeness per tip, from the families almost every in-clade tip carries (genome_quality.py).
    # An incomplete proteome misses genes it really has; with this vector the likelihood says so
    # directly, instead of accelerating loss on that tip's branch.
    from genome_quality import completeness_for
    comp = np.ones(len(parent))
    markers, unscored = {}, []
    # Scored separately inside and outside the clade: a marker set is only meaningful among
    # relatives, because across distant lineages "missing" and "never had it" look the same.
    for group in (True, False):
        name = "clade" if group else "outgroup"
        gp = {v: set(prof[names[v]]["pfam"]) for v in d["tips"] if in_clade[v] == group}
        scores, mk = completeness_for(gp) if len(gp) >= 8 else ({}, [])
        if not mk:
            unscored.append(name)   # left at 1.0: too few proteomes, or nothing near-universal
            continue
        markers[name] = len(mk)
        for v, c in scores.items():
            comp[v] = max(c, 0.05)
    d["completeness_vec"] = comp
    d["n_markers"] = markers
    d["unscored_groups"] = unscored
    # Loss acceleration applies inside the clade's reduced lineages: tips whose family count is far
    # below the clade median (here the Entamoeba parasites), AND the internal branches they span.
    # Only the tip branches were marked before, which did not match what this comment claimed.
    med = np.median([len(prof[names[v]]["pfam"]) for v in d["tips"] if in_clade[v]])
    reduced_tips = [v for v in d["tips"] if in_clade[v] and len(prof[names[v]]["pfam"]) < 0.6 * med]
    inside = np.zeros(len(parent), dtype=bool)
    inside[reduced_tips] = True
    if len(reduced_tips) > 1:
        anc = mrca(reduced_tips, parent, depth)
        stack = [anc]
        while stack:                      # every branch strictly below their common ancestor
            v = stack.pop()
            if v != anc:
                inside[v] = True
            stack.extend(children[v])
    d["reduced_branch"] = inside
    clade = [v for v in d["tips"] if in_clade[v]]
    top = mrca(clade, parent, depth) if clade else 0
    below, stack = [], [top]
    while stack:
        v = stack.pop()
        if not children[v] and not in_clade[v]:
            below.append(names[v])
        stack.extend(children[v])
    d["rooted_on"] = rooted_on
    d["non_clade_tips_inside_clade_node"] = sorted(below)
    return d, fams, names, in_clade, dropped, [names[v] for v in reduced_tips]


def mrca(nodes, parent, depth):
    common = None
    for u in nodes:
        s, w = set(), u
        while w != -1:
            s.add(w)
            w = parent[w]
        common = s if common is None else common & s
    return max(common, key=lambda x: depth[x])


def reconstruct(d, specs, use_completeness=False):
    """Ensemble mean posterior at every node, plus the spread across models."""
    vis = np.zeros(len(d["parent"]), dtype=bool)
    vis[d["tips"]] = True
    d = dict(d)
    d["completeness"] = d.get("completeness_vec") if use_completeness else None
    posts = []
    for spec in specs:
        g, lo, root, mult, _ = fit(d, d["X"], vis, spec)
        posts.append(posterior(d, d["X"], vis, g, lo, mult, root))
    P = np.stack(posts)
    return P.mean(0), P.std(0), vis


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--tree", required=True)
    ap.add_argument("--clade-genera", default="")
    ap.add_argument("--clade-kingdom", default="",
                    help="the clade is every tip of this UniProt kingdom (e.g. fungi), instead of a genus list")
    ap.add_argument("--name", required=True)
    ap.add_argument("--min-families", type=int, default=100,
                    help="drop a tip with fewer families than this. Low by default: an incomplete "
                         "proteome is handled by --completeness, not by throwing the species away "
                         "(at 500 this filter would have removed the most reduced genomes)")
    ap.add_argument("--root-outgroup", action="store_true",
                    help="root the (unrooted) FastTree tree on the outgroup tip farthest from the clade")
    ap.add_argument("--mask", type=int, default=3)
    ap.add_argument("--bootstrap-trees", default="")
    ap.add_argument("--out", default="results/clade_ancestor")
    ap.add_argument("--no-reduced-mult", action="store_true",
                    help="drop the loss acceleration on reduced lineages; with --completeness it is "
                         "partly a correction for the same thing (those genomes are also incomplete)")
    ap.add_argument("--completeness", action="store_true",
                    help="model incomplete proteomes as dropout in the likelihood instead of "
                         "accelerating loss on their branch (validated in results/quality_correction)")
    args = ap.parse_args()
    genera = set(g for g in args.clade_genera.split(",") if g)
    kingdom = args.clade_kingdom or None
    if not genera and not kingdom:
        raise SystemExit("give --clade-genera or --clade-kingdom")
    out = Path(args.out) / args.name
    out.mkdir(parents=True, exist_ok=True)

    d, fams, names, in_clade, dropped, reduced = build(args.tree, genera, args.min_families, kingdom, args.root_outgroup)
    clade_tips = [v for v in d["tips"] if in_clade[v]]
    print(f"{len(d['tips'])} tips with a usable proteome ({len(clade_tips)} in the clade), "
          f"{len(dropped)} dropped, {len(fams)} families in >= 3 tips")
    print(f"  reduced lineages (loss accelerated): {reduced}")
    node = mrca(clade_tips, d["parent"], d["depth"])
    specs = [{**sp, 'tip_mult': 1.0} for sp in ENSEMBLE] if args.completeness else list(ENSEMBLE)
    if args.no_reduced_mult:
        specs = [{**sp, 'mult': 1.0} for sp in specs]
    mean, spread, vis = reconstruct(d, specs, args.completeness)
    p, sd = mean[node], spread[node]

    # Leave-tips-out on the clade: hide `mask` clade tips, predict them, against family frequency.
    rng = np.random.default_rng(0)
    rows = []
    for rep in range(5):
        hid = list(rng.choice(clade_tips, min(args.mask, len(clade_tips) // 3), replace=False))
        v2 = vis.copy()
        v2[hid] = False
        dq = dict(d)
        dq["completeness"] = d.get("completeness_vec") if args.completeness else None
        g, lo, root, mult, _ = fit(dq, d["X"], v2, specs[0])
        ph = posterior(dq, d["X"], v2, g, lo, mult, root)
        freq = d["X"][[v for v in clade_tips if v not in set(hid)]].mean(0).astype(float)
        for v in hid:
            y = d["X"][v]
            rows.append({"tip": names[v], "reconstruction": float(auroc(ph[v], y)),
                         "clade_frequency": float(auroc(freq, y))})
    val = {k: round(float(np.mean([r[k] for r in rows])), 4) for k in ("reconstruction", "clade_frequency")}
    print(f"leave-tips-out AUROC: reconstruction {val['reconstruction']:.3f}, clade frequency "
          f"{val['clade_frequency']:.3f} ({len(rows)} hidden tips)")

    # Bootstrap trees: the same reconstruction on each, so tree uncertainty is included.
    boot = []
    if args.bootstrap_trees and Path(args.bootstrap_trees).exists():
        for i, line in enumerate(Path(args.bootstrap_trees).read_text().strip().split("\n")):
            tmp = out / "_boot.nwk"
            tmp.write_text(line)
            try:
                db, fb, nb, icb, _, _ = build(tmp, genera, args.min_families, kingdom, args.root_outgroup)
                ct = [v for v in db["tips"] if icb[v]]
                nb_node = mrca(ct, db["parent"], db["depth"])
                mb, _, _ = reconstruct(db, specs[:2], args.completeness)
                idx = {f: j for j, f in enumerate(fb)}
                boot.append(np.array([mb[nb_node][idx[f]] if f in idx else np.nan for f in fams]))
            except Exception as e:
                print(f"  bootstrap tree {i}: {e}")
            tmp.unlink(missing_ok=True)
        print(f"  {len(boot)} bootstrap trees")
    boot_sd = np.nanstd(np.stack(boot), axis=0) if boot else np.zeros_like(p)

    func, meta = functions_of(fams)
    clade_freq = d["X"][clade_tips].mean(0)
    order_idx = np.argsort(-p)
    confident = [j for j in order_idx if p[j] >= 0.9 and sd[j] < 0.1 and boot_sd[j] < 0.15]
    uncertain = [j for j in order_idx if 0.5 <= p[j] < 0.9 or (p[j] >= 0.9 and (sd[j] >= 0.1 or boot_sd[j] >= 0.15))]
    fcount = Counter(t for j in confident for t in func[j])
    summary = {
        "clade": args.name, "tips": len(d["tips"]), "clade_tips": len(clade_tips),
        "clade_species": [names[v] for v in clade_tips], "dropped_tips": dropped,
        "reduced_lineages": reduced, "families_considered": len(fams),
        "rooted_on": d.get("rooted_on"),
        "non_clade_tips_inside_clade_node": d.get("non_clade_tips_inside_clade_node"),
        "node_reconstructed": "most recent common ancestor of the sampled clade tips, which at this "
                              "sample size is not the clade's root (see results/sample_size/summary.json)",
        "leave_tips_out_auroc": val, "n_models": len(ENSEMBLE), "n_bootstrap_trees": len(boot),
        "completeness_model": bool(args.completeness),
        "reduced_branch_multiplier": not args.no_reduced_mult,
        "tip_completeness": ({names[v]: round(float(d["completeness_vec"][v]), 3)
                              for v in clade_tips} if args.completeness else None),
        "completeness_markers_per_group": d.get("n_markers") if args.completeness else None,
        "groups_without_a_completeness_score": d.get("unscored_groups") if args.completeness else None,
        "n_confident_families": len(confident), "n_uncertain_families": len(uncertain),
        "size_not_reported": "the simulation showed a 16-17% underestimate of ancestor size at this "
                             "sample size, so no family count is quoted",
        "functions_of_confident_families": fcount.most_common(20),
        "top_families": [{"family": fams[j], "description": meta.get(fams[j], {}).get("description", ""),
                          "posterior": round(float(p[j]), 3), "model_sd": round(float(sd[j]), 3),
                          "tree_sd": round(float(boot_sd[j]), 3),
                          "share_of_clade_tips_today": round(float(clade_freq[j]), 3)}
                         for j in confident[:60]],
        "uncertain_families": [{"family": fams[j], "description": meta.get(fams[j], {}).get("description", ""),
                                "posterior": round(float(p[j]), 3), "model_sd": round(float(sd[j]), 3),
                                "tree_sd": round(float(boot_sd[j]), 3)} for j in uncertain[:40]],
    }
    np.savez_compressed(out / "posterior.npz", families=np.array(fams), posterior=p, model_sd=sd, tree_sd=boot_sd,
                        clade_frequency=clade_freq)
    (out / "summary.json").write_text(json.dumps(summary, indent=1, ensure_ascii=False))
    print(f"\nconfident families {len(confident)}, uncertain {len(uncertain)}")
    print("functions:", fcount.most_common(10))
    print(f"Done -> {out}/summary.json")


if __name__ == "__main__":
    main()
