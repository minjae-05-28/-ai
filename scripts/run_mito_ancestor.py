"""Ancestral gene-family content of the alphaproteobacterial ancestors of mitochondria.

    python scripts/run_mito_ancestor.py [--outgroup 300] [--mask 300]

Data: the GTDB bacterial tree (results/phylo_tree/gtdb_bac120.tree.gz, scripts/fetch_gtdb_tree.py),
UniProt reference proteomes (Pfam presence) matched to GTDB species representatives by species
name, all Alphaproteobacteria that match plus a sample of Gammaproteobacteria as outgroup.

Model: every Pfam family is a two-state (absent/present) continuous-time Markov chain along the
tree's branches, with its own rate r and stationary frequency pi chosen by maximum likelihood
over a grid (Felsenstein pruning). Posterior presence at every internal node comes from the
up-down (marginal) algorithm, with pi as the root prior (symmetric model) or a flat 0.5 root
prior (loss_biased model, where pi is held low and must not decide the root by itself).

Where mitochondria branch is disputed (inside Alphaproteobacteria, e.g. near Rickettsiales, or
as their sister; Martijn et al. 2018, Munoz-Gomez et al. 2022), so several candidate ancestors are
reported: the alphaproteobacterial common ancestor and the common ancestors of the deep orders
present in the data.

Validation, side by side:
    leave-tips-out   `mask` alphaproteobacterial tips are hidden; their families are predicted from
                     the reconstruction (posterior at the tip) and compared with the family's
                     frequency among alphaproteobacteria and with the nearest unmasked tip.
    positive control Pfam families of genes still encoded by the most bacteria-like mitochondrial
                     genome (Reclinomonas americana): the proto-mitochondrion must have had them.
Output: results/mito_ancestor/summary.json and per-node family posteriors (top families, function
summary). Gene-family content only; no sequences are reconstructed.
"""

import argparse
import csv
import gzip
import json
import re
from collections import Counter, defaultdict
from pathlib import Path

import numpy as np

from organelle_evo.predict import auroc

OUT = Path("results/mito_ancestor")

# Pfam families of core genes in the Reclinomonas americana mitochondrial genome (respiratory chain,
# ATP synthase, ribosome, bacterial-type RNA polymerase, protein translocation, cytochrome c
# maturation, translation factor). Universal bacterial families: a sanity check, not a discriminating test.
RECLINOMONAS_CORE = {
    "nad1": "NADHdh", "nad2/4/5": "Proton_antipo_M", "nad3": "Oxidored_q4", "nad6": "Oxidored_q3",
    "nad7": "Complex1_49kDa", "nad9": "Complex1_30kDa", "nad4L": "Oxidored_q2", "nad8": "Fer4",
    "cox1": "COX1", "cox2": "COX2", "cox3": "COX3", "cob": "Cytochrome_B",
    "atp1/3": "ATP-synt_ab", "atp6": "ATP-synt_A", "atp9": "ATP-synt_C",
    "rpoB": "RNA_pol_Rpb2_6", "rpoC": "RNA_pol_Rpb1_2", "rpoA": "RNA_pol_L",
    "secY": "SecY", "tatC": "TatC", "ccmB": "CcmB", "ccmC": "Cytochrom_C_asm",
    "tufA": "GTP_EFTU", "rps12": "Ribosomal_S12_S23", "rpl2": "Ribosomal_L2_C", "rpl14": "Ribosomal_L14",
}


# ---- tree ----------------------------------------------------------------------------------------

def parse_newick(text):
    """Iterative parser -> (parent, length, label) arrays; node 0 is the root."""
    parent, length, label = [-1], [0.0], [""]
    stack, cur, i, n = [], 0, 0, len(text)
    while i < n:
        c = text[i]
        if c == "(":
            parent.append(cur), length.append(0.0), label.append("")
            stack.append(cur)
            cur = len(parent) - 1
            i += 1
        elif c == ",":
            cur = stack[-1]
            parent.append(cur), length.append(0.0), label.append("")
            cur = len(parent) - 1
            i += 1
        elif c == ")":
            cur = stack.pop()
            i += 1
        elif c == ":":
            j = i + 1
            while j < n and text[j] not in ",();":
                j += 1
            length[cur] = float(text[i + 1:j] or 0)
            i = j
        elif c == ";":
            break
        else:
            if c == "'":
                j = text.index("'", i + 1)
                label[cur] = text[i + 1:j]
                i = j + 1
            else:
                j = i
                while j < n and text[j] not in ",():;":
                    j += 1
                label[cur] = text[i:j]
                i = j
    return np.array(parent), np.array(length), label


def prune(parent, length, label, keep_tips):
    """Subtree spanning keep_tips (node ids), unary nodes collapsed. Returns new arrays + tip map."""
    n = len(parent)
    keep = np.zeros(n, dtype=bool)
    for t in keep_tips:
        v = t
        while v != -1 and not keep[v]:
            keep[v] = True
            v = parent[v]
    children = defaultdict(list)
    for v in np.flatnonzero(keep):
        if parent[v] != -1:
            children[parent[v]].append(v)
    root = int(np.flatnonzero(keep & (parent == -1))[0])
    while len(children[root]) == 1:  # descend to the first branching node
        root = children[root][0]
    new_parent, new_len, new_label, old = [-1], [0.0], [label[root]], [root]
    stack = [(root, 0)]
    while stack:
        v, nv = stack.pop()
        for c in children[v]:
            bl = length[c]
            while len(children[c]) == 1:  # collapse unary chains
                c = children[c][0]
                bl += length[c]
            new_parent.append(nv), new_len.append(bl), new_label.append(label[c]), old.append(c)
            stack.append((c, len(new_parent) - 1))
    return np.array(new_parent), np.maximum(np.array(new_len), 1e-6), new_label, np.array(old)


def postorder(parent):
    n = len(parent)
    children = [[] for _ in range(n)]
    for v in range(1, n):
        children[parent[v]].append(v)
    order, stack = [], [(0, False)]
    while stack:
        v, done = stack.pop()
        if done:
            order.append(v)
        else:
            stack.append((v, True))
            stack.extend((c, False) for c in children[v])
    return order, children


# ---- model ---------------------------------------------------------------------------------------

def trans(t, r, pi):
    """2x2 transition matrices for all (grid/family) rate pairs: P[from][to], shapes broadcast."""
    e = np.exp(-r * t)
    p01, p10 = pi * (1 - e), (1 - pi) * (1 - e)
    return 1 - p01, p01, p10, 1 - p10  # P00, P01, P10, P11


def tip_pair(x, c):
    """What a tip's observation says about its true state.

    An incomplete proteome misses a share of the genes it really has, so an observed absence is
    only evidence of absence in proportion to how complete the proteome is: with completeness c,
    P(observed absent | present) = 1 - c. An observed presence is never a false positive.
    c = 1 returns the plain indicator, so runs without completeness are unchanged.
    """
    return 1 - x, x if c is None else x * np.float32(c) + (1 - x) * np.float32(1 - c)


def loglik_grid(order, children, length, tipX, r, pi, root=None, comp=None):
    """Log-likelihood per (grid point, family). tipX: node -> (F,) presence (bool) or None (internal)."""
    msg, logs = {}, 0.0
    for v in order:
        if tipX.get(v) is not None:
            x = tipX[v][None, :].astype(np.float32)
            m0, m1 = tip_pair(x, None if comp is None else comp.get(v))
            L0, L1 = (np.broadcast_to(m0, r.shape[:1] + x.shape[1:]).copy(),
                      np.broadcast_to(m1, r.shape[:1] + x.shape[1:]).copy())
        else:
            L0 = np.ones(r.shape[:1] + (pi.shape[-1],), dtype=np.float32)
            L1 = L0.copy()
            for c in children[v]:
                c0, c1 = msg.pop(c)
                P00, P01, P10, P11 = trans(length[c], r, pi)
                L0 *= P00 * c0 + P01 * c1
                L1 *= P10 * c0 + P11 * c1
            s = np.maximum(L0, L1)
            L0, L1 = L0 / s, L1 / s
            logs = logs + np.log(s)
        msg[v] = (L0, L1)
    L0, L1 = msg[0]
    rho = pi if root is None else root
    return logs + np.log((1 - rho) * L0 + rho * L1)


def marginals(order, children, parent, length, tipX, r, pi, root=None, comp=None):
    """Posterior P(present) at every node, per family (r, pi: (F,))."""
    n = len(parent)
    F = pi.shape[-1]
    down = np.zeros((n, 2, F), dtype=np.float32)
    for v in order:
        if tipX.get(v) is not None:
            x = tipX[v].astype(np.float32)
            down[v, 0], down[v, 1] = tip_pair(x, None if comp is None else comp.get(v))
        elif not children[v]:
            down[v] = 1.0  # masked tip: no data
        else:
            L0 = np.ones(F, dtype=np.float32)
            L1 = np.ones(F, dtype=np.float32)
            for c in children[v]:
                P00, P01, P10, P11 = trans(length[c], r, pi)
                L0 *= P00 * down[c, 0] + P01 * down[c, 1]
                L1 *= P10 * down[c, 0] + P11 * down[c, 1]
            s = np.maximum(np.maximum(L0, L1), 1e-30)
            down[v, 0], down[v, 1] = L0 / s, L1 / s
    up = np.zeros((n, 2, F), dtype=np.float32)  # likelihood of everything outside v's subtree, by v's parent state
    rho = pi if root is None else np.broadcast_to(np.float32(root), pi.shape)
    up[0, 0], up[0, 1] = 1 - rho, rho
    post = np.zeros((n, F), dtype=np.float32)
    for v in reversed(order):
        # state distribution at v given everything outside v's subtree
        if v == 0:
            a0, a1 = up[0, 0], up[0, 1]
        else:
            a0, a1 = up[v, 0], up[v, 1]
        p1 = a1 * down[v, 1]
        p0 = a0 * down[v, 0]
        post[v] = p1 / np.maximum(p0 + p1, 1e-30)
        for c in children[v]:
            # outside-of-c message at v: a * product of siblings' down messages
            s0, s1 = a0.copy(), a1.copy()
            for sib in children[v]:
                if sib == c:
                    continue
                P00, P01, P10, P11 = trans(length[sib], r, pi)
                s0 *= P00 * down[sib, 0] + P01 * down[sib, 1]
                s1 *= P10 * down[sib, 0] + P11 * down[sib, 1]
            P00, P01, P10, P11 = trans(length[c], r, pi)
            u0 = s0 * P00 + s1 * P10
            u1 = s0 * P01 + s1 * P11
            z = np.maximum(u0 + u1, 1e-30)
            up[c, 0], up[c, 1] = u0 / z, u1 / z
    return post


# ---- data ----------------------------------------------------------------------------------------

def key(name):
    w = re.sub(r"^Candidatus ", "", name.strip()).replace("[", "").replace("]", "").split()
    return " ".join(w[:2]).lower()


def load_tips(n_outgroup, seed=0, min_busco=0.0):
    csv.field_size_limit(10**8)
    reps = {}
    for r in csv.DictReader(gzip.open("data/gtdb/species_reps.tsv.gz", "rt"), delimiter="\t"):
        tax = r["gtdb_taxonomy"]
        if "c__Alphaproteobacteria" in tax or "c__Gammaproteobacteria" in tax:
            reps.setdefault(key(r["ncbi_organism_name"]), (r["accession"], tax))
    pfam = {}
    for f in sorted(Path("data/uniprot/shards").glob("*.json.gz")):
        for p in json.loads(gzip.open(f, "rt").read()).values():
            k = key(p["organism"])
            if p.get("kingdom") == "bacteria" and k in reps and k not in pfam:
                b = re.search(r"C:([\d.]+)%", p.get("busco") or "")
                if min_busco and (not b or float(b.group(1)) < min_busco):
                    continue  # incomplete proteomes read as gene loss
                if len(p["pfam"]) < 100:
                    continue  # UniProt keeps the record but not the sequences for some proteomes
                pfam[k] = set(p["pfam"])
    alpha = [k for k in pfam if "c__Alphaproteobacteria" in reps[k][1]]
    gamma = sorted(k for k in pfam if "c__Gammaproteobacteria" in reps[k][1])
    rng = np.random.default_rng(seed)
    gamma = list(rng.choice(gamma, min(n_outgroup, len(gamma)), replace=False))
    tips = {reps[k][0]: (k, reps[k][1], pfam[k]) for k in alpha + gamma}
    return tips


def functions_of(fams):
    from organelle_evo.eukaryotes.features import KEYWORD_CLASSES  # pulls in torch; only needed here

    meta = json.loads(Path("data/eukaryotes/pfam_meta.json").read_text())
    ann = json.loads(Path("data/eukaryotes/family_annotations.json").read_text())
    slims = ann["slims"]
    out = []
    for f in fams:
        tags = [slims[t]["name"] for t in ann["families"].get(f, {}).get("go_slim", ()) if t in slims]
        text = f"{f} {meta.get(f, {}).get('description', '')}"
        tags += [n for n, pat in KEYWORD_CLASSES if re.search(pat, text)]
        out.append(tags)
    return out, meta


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--outgroup", type=int, default=300)
    ap.add_argument("--mask", type=int, default=300)
    ap.add_argument("--min-tips", type=int, default=3)
    ap.add_argument("--model", choices=("symmetric", "loss_biased"), default="symmetric",
                    help="loss_biased: gain rate <= 0.1 x loss rate (genome reduction is loss-dominated)")
    ap.add_argument("--min-busco", type=float, default=0.0, help="drop proteomes below this BUSCO completeness")
    ap.add_argument("--tag", default="")
    ap.add_argument("--save-law", action="store_true")
    ap.add_argument("--completeness", action="store_true",
                    help="model incomplete proteomes as dropout in the likelihood "
                         "(validated in results/quality_correction/summary.json)")
    args = ap.parse_args()
    if args.save_law:
        save()
        return
    global OUT
    OUT = OUT / (args.tag or f"{args.model}_busco{int(args.min_busco)}")
    OUT.mkdir(parents=True, exist_ok=True)

    tips = load_tips(args.outgroup, min_busco=args.min_busco)
    print(f"{len(tips)} tips with a UniProt proteome "
          f"({sum('c__Alphaproteobacteria' in t[1] for t in tips.values())} alphaproteobacteria)", flush=True)
    parent, length, label = parse_newick(gzip.open("results/phylo_tree/gtdb_bac120.tree.gz", "rt").read())
    acc_node = {lab: i for i, lab in enumerate(label) if lab in tips}
    missing = [a for a in tips if a not in acc_node]
    print(f"tree: {len(parent)} nodes; {len(acc_node)} of our tips on it ({len(missing)} missing)", flush=True)
    parent, length, label, old = prune(parent, length, label, list(acc_node.values()))
    order, children = postorder(parent)
    tip_of = {i: label[i] for i in range(len(parent)) if not children[i]}
    print(f"pruned tree: {len(parent)} nodes, {len(tip_of)} tips", flush=True)

    counts = Counter(f for a in tip_of.values() for f in tips[a][2])
    fams = sorted(f for f, c in counts.items() if c >= args.min_tips)
    col = {f: j for j, f in enumerate(fams)}
    X = {}
    for v, a in tip_of.items():
        x = np.zeros(len(fams), dtype=bool)
        x[[col[f] for f in tips[a][2] if f in col]] = True
        X[v] = x
    print(f"{len(fams)} Pfam families in >= {args.min_tips} tips", flush=True)

    # Genome quality as an observation model: an incomplete proteome misses genes it really has.
    # Scored within the clade and within the outgroup separately, because a marker set only means
    # something among relatives (across distant lineages "missing" and "never had it" look alike).
    comp = None
    if args.completeness:
        from genome_quality import completeness_for

        comp, unscored = {}, []
        groups = {"alpha": [v for v in tip_of if "c__Alphaproteobacteria" in tips[tip_of[v]][1]]}
        groups["outgroup"] = [v for v in tip_of if v not in set(groups["alpha"])]
        for gname, vs in groups.items():
            scores, mk = completeness_for({v: tips[tip_of[v]][2] for v in vs}) if len(vs) >= 8 else ({}, [])
            if not mk:
                unscored.append(gname)
                continue
            comp.update({v: max(float(c), 0.05) for v, c in scores.items()})
            print(f"  completeness ({gname}): {len(mk)} markers, median "
                  f"{np.median([scores[v] for v in vs]):.3f}, lowest {min(scores.values()):.3f}", flush=True)
        if unscored:
            print(f"  ::warning:: no completeness score for {unscored}; those tips stay at 1.0", flush=True)

    # Per-family rate and stationary frequency by grid maximum likelihood.
    R = np.array([0.03, 0.1, 0.3, 1.0, 3.0, 10.0], dtype=np.float32)
    # pi = gain / (gain + loss); loss_biased keeps gain <= 0.1 x loss, i.e. pi <= 1/11.
    PI = (np.array([0.005, 0.01, 0.02, 0.04, 0.06, 0.09], dtype=np.float32) if args.model == "loss_biased"
          else np.array([0.02, 0.05, 0.15, 0.3, 0.5, 0.7, 0.85, 0.95, 0.98], dtype=np.float32))
    gr, gp = np.meshgrid(R, PI, indexing="ij")
    root_prior = 0.5 if args.model == "loss_biased" else None
    gr, gp = gr.ravel()[:, None], gp.ravel()[:, None]
    best_ll = np.full(len(fams), -np.inf)
    best_r = np.zeros(len(fams), dtype=np.float32)
    best_pi = np.zeros(len(fams), dtype=np.float32)
    for lo in range(0, len(fams), 1500):
        sl = slice(lo, lo + 1500)
        Xs = {v: x[sl] for v, x in X.items()}
        ll = loglik_grid(order, children, length, Xs, gr, np.broadcast_to(gp, (gp.shape[0], len(range(*sl.indices(len(fams)))))),
                         root=root_prior, comp=comp)
        k = np.argmax(ll, axis=0)
        best_ll[sl], best_r[sl], best_pi[sl] = ll[k, np.arange(ll.shape[1])], gr[k, 0], gp[k, 0]
        print(f"  rates fitted for families {lo}-{min(lo + 1500, len(fams))}", flush=True)

    # Leave-tips-out validation (alphaproteobacterial tips only).
    rng = np.random.default_rng(1)
    alpha_tips = [v for v, a in tip_of.items() if "c__Alphaproteobacteria" in tips[a][1]]
    masked = set(rng.choice(alpha_tips, min(args.mask, len(alpha_tips) // 5), replace=False).tolist())
    Xm = {v: (None if v in masked else x) for v, x in X.items()}
    post_m = marginals(order, children, parent, length, Xm, best_r, best_pi, root=root_prior, comp=comp)
    alpha_freq = np.mean([X[v] for v in alpha_tips if v not in masked], axis=0)
    # nearest unmasked tip by path length
    depth = np.zeros(len(parent))
    for v in reversed(order):
        if v:
            depth[v] = depth[parent[v]] + length[v]
    # Closest unmasked tip below every node (postorder), then the best over a masked tip's ancestors.
    best_tip = {}
    for v in order:
        if not children[v]:
            best_tip[v] = v if v not in masked else None
        else:
            cands = [best_tip[c] for c in children[v] if best_tip[c] is not None]
            best_tip[v] = min(cands, key=lambda u: depth[u]) if cands else None

    def nearest(v):
        best, bd, w = None, np.inf, parent[v]
        while w != -1:
            u = best_tip[w]
            if u is not None and depth[v] + depth[u] - 2 * depth[w] < bd:
                best, bd = u, depth[v] + depth[u] - 2 * depth[w]
            w = parent[w]
        return best

    rows = []
    for v in masked:
        truth = X[v]
        nb = nearest(v)
        rows.append({"tip": tips[tip_of[v]][0], "reconstruction": auroc(post_m[v], truth),
                     "alpha_frequency": auroc(alpha_freq, truth),
                     "nearest_tip": auroc(X[nb].astype(float) + 0.5 * alpha_freq, truth)})
    val = {k: round(float(np.nanmean([r[k] for r in rows])), 4) for k in ("reconstruction", "alpha_frequency", "nearest_tip")}
    print("leave-tips-out AUROC (presence of each family in a hidden species):", val, flush=True)

    # Full reconstruction.
    post = marginals(order, children, parent, length, X, best_r, best_pi, root=root_prior, comp=comp)

    def mrca(nodes):
        nodes = list(nodes)
        anc = []
        v = nodes[0]
        while v != -1:
            anc.append(v)
            v = parent[v]
        common = set(anc)
        for u in nodes[1:]:
            s, w = set(), u
            while w != -1:
                s.add(w)
                w = parent[w]
            common &= s
        return max(common, key=lambda x: depth[x])

    by_order = defaultdict(list)
    for v in alpha_tips:
        tax = tips[tip_of[v]][1]
        by_order[tax.split(";")[3]].append(v)
    targets = {"Alphaproteobacteria (common ancestor)": mrca(alpha_tips)}
    for o in ("o__Rickettsiales", "o__Holosporales", "o__Pelagibacterales", "o__Rhodospirillales", "o__Caulobacterales"):
        if len(by_order.get(o, [])) >= 2:
            targets[f"{o[3:]} (common ancestor)"] = mrca(by_order[o])
    # Each target node gets its OWN leave-tips-out score. Before this the orders inherited the
    # class-wide number, which says nothing about how well a 40-tip order is reconstructed.
    per_node = {}
    for name, members in [("Alphaproteobacteria (common ancestor)", alpha_tips)] + [
            (f"{o[3:]} (common ancestor)", by_order[o]) for o in by_order if f"{o[3:]} (common ancestor)" in targets]:
        pool = list(members)
        if len(pool) < 6:
            continue
        rng2 = np.random.default_rng(7)
        scores = []
        for rep in range(3):
            hid = set(rng2.choice(pool, max(2, len(pool) // 5), replace=False).tolist())
            Xh = {v: (None if v in hid else x) for v, x in X.items()}
            ph = marginals(order, children, parent, length, Xh, best_r, best_pi, root=root_prior, comp=comp)
            freq_h = np.mean([X[v] for v in pool if v not in hid], axis=0)
            for v in hid:
                scores.append((auroc(ph[v], X[v]), auroc(freq_h, X[v])))
        per_node[name] = {"reconstruction": round(float(np.nanmean([a for a, _ in scores])), 4),
                          "clade_frequency": round(float(np.nanmean([b for _, b in scores])), 4),
                          "n_hidden": len(scores), "n_tips": len(pool)}
        print(f"  per-node validation {name}: {per_node[name]}", flush=True)

    func, meta = functions_of(fams)
    summary = {"tips": len(tip_of), "alphaproteobacteria": len(alpha_tips),
               "alpha_orders": {o: len(v) for o, v in sorted(by_order.items(), key=lambda t: -len(t[1]))},
               "families": len(fams), "leave_tips_out_auroc": val, "n_masked": len(rows),
               "completeness_model": bool(args.completeness),
               "per_node_validation": per_node, "nodes": {}}
    for name, node in targets.items():
        p = post[node]
        present = np.flatnonzero(p >= 0.9)
        uncertain = np.flatnonzero((p > 0.5) & (p < 0.9))
        f_counts = Counter(t for j in present for t in func[j])
        alpha_share = alpha_freq  # families common at the root but rare today
        lost_since = [j for j in present if alpha_share[j] < 0.3]
        summary["nodes"][name] = {
            "n_tips_below": int(sum(1 for v in _desc(node, children) if not children[v])),
            "families_p_ge_0.9": int(len(present)), "families_p_0.5_0.9": int(len(uncertain)),
            "expected_families": round(float(p.sum()), 1),
            "functions_top": f_counts.most_common(15),
            "present_but_rare_today": sorted(((fams[j], meta.get(fams[j], {}).get("description", ""),
                                               round(float(p[j]), 3), round(float(alpha_share[j]), 3))
                                              for j in lost_since), key=lambda t: -t[2])[:40],
            "positive_control": {g: (round(float(p[col[f]]), 3) if f in col else None) for g, f in RECLINOMONAS_CORE.items()},
            "validation": per_node.get(name),
        }
        pc = [x for x in summary["nodes"][name]["positive_control"].values() if x is not None]
        print(f"\n{name}: ~{p.sum():.0f} families expected, {len(present)} with P>=0.9, {len(uncertain)} uncertain; "
              f"positive control {sum(x >= 0.9 for x in pc)}/{len(pc)} at P>=0.9", flush=True)
        print("   functions:", f_counts.most_common(8))
        np.save(OUT / f"posterior_{re.sub(r'[^A-Za-z]+', '_', name).strip('_')}.npy", p)
    (OUT / "families.json").write_text(json.dumps(fams))
    (OUT / "summary.json").write_text(json.dumps(summary, indent=1, ensure_ascii=False))
    print(f"Done -> {OUT}/summary.json")


def _desc(node, children):
    out, stack = [], [node]
    while stack:
        v = stack.pop()
        out.append(v)
        stack.extend(children[v])
    return out


def save(law_id="mito_ancestor_v1"):
    """Law card from the four variants in results/mito_ancestor/<model>_busco<n>/summary.json."""
    from organelle_evo.laws import LAWS_DIR, save_law

    variants = {p.parent.name: json.loads(p.read_text()) for p in sorted(OUT.glob("*/summary.json"))}
    val = {}
    for name, s in variants.items():
        val[name] = {"tips": s["tips"], "leave_tips_out_auroc": s["leave_tips_out_auroc"],
                     "nodes": {n: {k: v[k] for k in ("n_tips_below", "expected_families", "families_p_ge_0.9",
                                                     "families_p_0.5_0.9", "positive_control")}
                               for n, v in s["nodes"].items()}}
    save_law(
        LAWS_DIR / f"{law_id}.json",
        id=law_id,
        scope=("Gene-family (Pfam) content of the alphaproteobacterial ancestors from which mitochondria are "
               "thought to descend, reconstructed on the GTDB tree from UniProt reference proteomes. Candidate "
               "ancestors: the alphaproteobacterial common ancestor and deep orders (Rickettsiales, Holosporales, "
               "Pelagibacterales). Family presence only; no sequences."),
        model=("Two-state gain/loss Markov chain per Pfam family on the pruned GTDB bac120 tree, rates by grid "
               "maximum likelihood, marginal posteriors by the up-down algorithm. Variants: symmetric vs loss-biased "
               "(gain <= 0.1 x loss, flat root prior) x all proteomes vs BUSCO >= 90%."),
        feature_names=[],
        data={"tips": "2,623 (2,323 Alphaproteobacteria + 300 Gammaproteobacteria outgroup); 2,526 with BUSCO >= 90%",
              "families": "Pfam families in >= 3 tips (about 10,000)"},
        validation=val,
        caveats=[
            "The preferred variant is loss_biased_busco90: the only one with all 25 Reclinomonas core-gene families "
            "present at the alphaproteobacterial root. The symmetric model on all proteomes gave an ancestor without "
            "the TCA cycle or fatty-acid synthesis, because reduced or incomplete basal lineages (a long-branch MAG, "
            "endosymbiont-like MAGs, Holosporales) make one gain cheaper than several losses.",
            "Ancestor size depends on the model and data choices: about 1,900 to 4,100 expected families at the "
            "alphaproteobacterial root. Report the range, not one number.",
            "Leave-tips-out accuracy is the same (0.985) for every variant, so it cannot choose between them: it tests "
            "recent tips, not deep nodes. The positive control and agreement with the literature are the deep-node checks.",
            "Where mitochondria branch (inside Alphaproteobacteria or as their sister) is disputed; the deep orders "
            "closest to mitochondria are poorly sampled here (Rickettsiales 40-53, Holosporales 4, Pelagibacterales 3).",
            "Positive-control families are universal bacterial genes: necessary, not discriminating.",
            "Horizontal gene transfer is not modelled; families moved between lineages can look ancestral.",
        ],
        contexts={},
    )
    print(f"law -> laws/{law_id}.json")


if __name__ == "__main__":
    main()
