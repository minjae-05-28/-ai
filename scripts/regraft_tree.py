"""Rebuild the learning-loop tree with one-at-a-time, stem-aware grafting (pre-registration 16, deviation 2).

The learning loop grafted each round's batch at once against the tree as it was before the batch, so species
of a group new to the tree could not anchor on each other; and a species whose most specific shared taxon T
held only tips of one subgroup of T was hung inside that subgroup's crown (birds inside mammals). Here every
species is grafted in turn, and in that case it goes on the stem of the subgroup, as its sister.

    python scripts/regraft_tree.py    -> results/human_gene_ages/tree_regrafted.nwk
"""

import json
import sys
from collections import defaultdict
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))

OUT = Path("results/human_gene_ages/tree_regrafted.nwk")


def regraft(parent, length, label, tip_lin, new):
    """Graft `new` (label -> lineage, in the given order) one at a time. Returns parent, length, label, placed."""
    parent, length, label = list(parent), list(length), list(label)
    depth = [0.0] * len(parent)
    kids = defaultdict(list)
    for v, p in enumerate(parent):
        if p >= 0:
            kids[p].append(v)
    stack = [v for v, p in enumerate(parent) if p < 0]
    while stack:
        v = stack.pop()
        for c in kids[v]:
            depth[c] = depth[v] + length[c]
            stack.append(c)
    lin = {v: L for v, L in tip_lin.items()}
    by_taxon = defaultdict(list)
    for v, L in lin.items():
        for t in L[:-1]:
            if t:
                by_taxon[t].append(v)

    def mrca(A):
        anc = []
        w = A[0]
        while w != -1:
            anc.append(w)
            w = parent[w]
        pos = {w: i for i, w in enumerate(anc)}
        best = 0
        for a in A[1:]:
            w = a
            while w not in pos:
                w = parent[w]
            best = max(best, pos[w])
        return anc[best]

    def add(p, ln, lab):
        parent.append(p)
        length.append(ln)
        label.append(lab)
        depth.append((depth[p] if p >= 0 else 0.0) + ln)
        return len(parent) - 1

    placed = {}
    for lab, L in new.items():
        L = list(L)
        shared = [(len(by_taxon[t]), i, t) for i, t in enumerate(L[:-1]) if t and by_taxon.get(t)]
        if not shared:
            continue
        _, i, anchor = max(shared, key=lambda x: x[1])          # deepest (most specific) shared taxon
        A = by_taxon[anchor]
        own_child = L[i + 1] if i + 1 < len(L) else None
        child = {lin[a][lin[a].index(anchor) + 1] if lin[a].index(anchor) + 1 < len(lin[a]) else None for a in A}
        m = A[0] if len(A) == 1 else mrca(A)
        target_depth = float(np.mean([depth[a] for a in A]))
        if parent[m] >= 0 and (len(A) == 1 or (len(child) == 1 and own_child not in child)):
            # outside the only subgroup present: split the branch above it and hang the species there
            p = parent[m]
            half = length[m] / 2
            w = add(p, half, "")
            parent[m] = w
            length[m] = half
            depth[w] = depth[p] + half if p >= 0 else 0.0
            node = w
        else:
            node = m
        v = add(node, max(target_depth - depth[node], 1e-3), lab)
        lin[v] = L
        for t in L[:-1]:
            if t:
                by_taxon[t].append(v)
        placed[lab] = anchor
    return np.array(parent), np.array(length), label, placed


def main():
    import learning_loop as ll
    from human_gene_ages import load_tree
    ll.current_tree = lambda: None                          # start from the base tree, rooted as the loop does
    d, fams, names, tip_name, tip_lin = load_tree(base_only=True)
    held = ll.all_new_species()
    new = {k: held[k]["lineage"] for k in sorted(held)}
    label = [names.get(v, "") for v in range(len(d["parent"]))]
    parent, length, label, placed = regraft(d["parent"], d["length"], label, tip_lin, new)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(ll.to_newick(parent, length, label))
    print(f"base tips {len(d['tips'])}, grafted {len(placed)} of {len(new)} -> {OUT}", flush=True)


if __name__ == "__main__":
    main()
