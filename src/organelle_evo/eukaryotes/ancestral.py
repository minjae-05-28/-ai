"""Ancestral gene-family content by Wagner parsimony.

Copy numbers change along branches at cost |i - j| (Wagner parsimony, as in the Count
software of Csurös). Given a rooted tree and per-leaf counts, dynamic programming
finds, for every family independently, the internal-node counts that minimise the
total change. Ties are broken towards the smaller count, the conservative choice.

Trees are nested tuples of leaf names, e.g. (("A", "B"), "C").
"""

import numpy as np


def leaves(tree) -> list[str]:
    return [tree] if isinstance(tree, str) else [x for sub in tree for x in leaves(sub)]


def prune(tree, drop: set[str]):
    """Tree without the given leaves (single-child nodes are collapsed)."""
    if isinstance(tree, str):
        return None if tree in drop else tree
    kids = [k for k in (prune(sub, drop) for sub in tree) if k is not None]
    if not kids:
        return None
    return kids[0] if len(kids) == 1 else tuple(kids)


def wagner_ancestor(tree, counts: dict[str, np.ndarray], max_count: int = 30) -> np.ndarray:
    """Most parsimonious family counts at the root of `tree`. counts: leaf -> (F,)."""
    states = np.arange(max_count + 1)
    step = np.abs(states[:, None] - states[None, :])  # (K+1, K+1) change cost

    def cost(node) -> np.ndarray:  # (F, K+1): min cost of the subtree given node state
        if isinstance(node, str):
            c = np.minimum(counts[node], max_count)
            return np.where(states[None, :] == c[:, None], 0.0, np.inf)
        total = 0.0
        for child in node:
            cc = cost(child)
            # min over child state j of cc[:, j] + |i - j|
            total = total + np.min(cc[:, None, :] + step[None, :, :], axis=2)
        return total

    root_cost = cost(tree)
    return np.argmin(root_cost, axis=1)  # argmin returns the smallest tying state
