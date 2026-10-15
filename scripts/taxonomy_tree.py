"""Species tree from the NCBI classification of every tip (pre-registration 16, deviation 2).

Gene-age studies (phylostratigraphy) use the taxonomy as the species tree. Two groups NCBI does not have are
added because the human strata need them: Amorphea (the LECA root split the learning loop uses) and Holozoa
(animals + their unicellular relatives). Branch lengths: a node's height is one more than its tallest child's
(tips 0), scaled so the root height equals the median root-to-tip depth of the learning-loop tree.

    python scripts/taxonomy_tree.py   -> results/human_gene_ages/tree_taxonomy.nwk
"""

import sys
from collections import defaultdict
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))

OUT = Path("results/human_gene_ages/tree_taxonomy.nwk")
AMORPHEA = {"Opisthokonta", "Amoebozoa", "Apusozoa", "Breviatea"}
HOLOZOA = {"Metazoa", "Choanoflagellata", "Filasterea", "Ichthyosporea"}


def augment(L):
    """Lineage below 'Eukaryota', with Amorphea and Holozoa inserted."""
    L = [t for t in L if t and t != "cellular organisms"]
    out = []
    for i, t in enumerate(L):
        if t in AMORPHEA and "Amorphea" not in out:
            out.append("Amorphea")
        if t in HOLOZOA and "Holozoa" not in out and "Opisthokonta" in out:
            out.append("Holozoa")
        out.append(t)
    return out


def build_tree(lineage, scale):
    """lineage: tip label -> list of taxa ending in the species name. Returns parent, length, label (root 0)."""
    # a node per lineage prefix (not per name): homonyms such as Morus (mulberry / gannet) stay apart
    idx = {(): 0}
    parent, label = [-1], [""]
    for lab in sorted(lineage):
        L = augment(lineage[lab][:-1])
        if L and L[0] == "Eukaryota":
            L = L[1:]
        key, p = (), 0
        for t in L:
            key = key + (t,)
            if key not in idx:
                idx[key] = len(parent)
                parent.append(p)
                label.append("")
            p = idx[key]
        parent.append(p)
        label.append(lab)
    parent = np.array(parent)
    # collapse single-child internal nodes
    kids = defaultdict(list)
    for v, p in enumerate(parent):
        if p >= 0:
            kids[p].append(v)
    height = np.zeros(len(parent))
    order = []
    stack = [0]
    while stack:
        v = stack.pop()
        order.append(v)
        stack.extend(kids[v])
    keep = [v for v in order if v == 0 or label[v] or len(kids[v]) != 1]
    newp = {}
    for v in keep:
        if v == 0:
            continue
        w = parent[v]
        while w != 0 and not (label[w] or len(kids[w]) != 1):
            w = parent[w]
        newp[v] = w
    kids2 = defaultdict(list)
    for v, w in newp.items():
        kids2[w].append(v)
    for v in reversed(keep):
        height[v] = 0 if not kids2[v] else 1 + max(height[c] for c in kids2[v])
    remap = {v: i for i, v in enumerate(keep)}
    P = np.full(len(keep), -1)
    Lg = np.zeros(len(keep))
    lab2 = [label[v] for v in keep]
    f = scale / height[0]
    for v in keep[1:]:
        P[remap[v]] = remap[newp[v]]
        Lg[remap[v]] = (height[newp[v]] - height[v]) * f
    return P, Lg, lab2


def main():
    import learning_loop as ll
    from human_gene_ages import load_tree
    d, fams, names, tip_name, tip_lin = load_tree()
    depth = np.median([d["depth"][v] for v in d["tips"]])
    lineage = {names[v]: tip_lin[v] for v in d["tips"]}
    P, Lg, lab = build_tree(lineage, float(depth))
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(ll.to_newick(P, Lg, lab))
    print(f"{len(lineage)} tips, {len(P)} nodes, root height {depth:.3f} -> {OUT}", flush=True)


if __name__ == "__main__":
    main()
