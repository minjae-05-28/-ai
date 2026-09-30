"""Synthetic alphaproteobacterial ancestor of mitochondria.

Each gene carries four biologically motivated features in [0, 1]:

- hydrophobicity         : membrane-embedded proteins are hard to re-import
                           after transfer to the nucleus (hydrophobicity hypothesis)
- redox_coupling         : genes whose expression must track local redox state
                           (CoRR hypothesis, Allen 1993/2003)
- host_redundancy        : how much the host already provides the same function
- symbiont_essentiality  : how much the endosymbiont still needs the function
"""

from dataclasses import dataclass

import numpy as np

FEATURES = (
    "hydrophobicity",
    "redox_coupling",
    "host_redundancy",
    "symbiont_essentiality",
)

# name: (n_genes, genes_per_pathway, feature means in FEATURES order)
CATEGORY_SPECS = {
    "respiratory_chain": (45, 9, (0.75, 0.85, 0.10, 0.90)),
    "atp_synthase": (12, 6, (0.60, 0.50, 0.10, 0.90)),
    "ribosome": (55, 11, (0.15, 0.10, 0.30, 0.80)),
    "rna_polymerase": (8, 4, (0.10, 0.20, 0.40, 0.70)),
    "fe_s_heme": (30, 10, (0.30, 0.50, 0.30, 0.70)),
    "tca_cycle": (25, 8, (0.15, 0.30, 0.50, 0.60)),
    "amino_acid_biosynthesis": (90, 10, (0.15, 0.05, 0.85, 0.20)),
    "cell_envelope": (70, 10, (0.45, 0.05, 0.70, 0.10)),
    "motility": (40, 10, (0.30, 0.02, 0.90, 0.05)),
    "transport": (70, 10, (0.70, 0.10, 0.60, 0.30)),
    "regulation": (60, 10, (0.10, 0.10, 0.70, 0.20)),
    "dna_replication_repair": (45, 9, (0.10, 0.10, 0.50, 0.50)),
    "protein_secretion": (25, 5, (0.55, 0.05, 0.40, 0.50)),
}


@dataclass(frozen=True)
class AncestorGenome:
    features: np.ndarray  # (G, F) float in [0, 1]
    category: np.ndarray  # (G,) index into `categories`
    pathway: np.ndarray  # (G,) pathway id; genes in a pathway are functionally coupled
    categories: tuple[str, ...]

    @property
    def n_genes(self) -> int:
        return len(self.category)

    @property
    def n_pathways(self) -> int:
        return int(self.pathway.max()) + 1

    @property
    def gene_names(self) -> list[str]:
        names, seen = [], {}
        for c in self.category:
            cat = self.categories[c]
            seen[cat] = seen.get(cat, 0) + 1
            names.append(f"{cat}_{seen[cat]:03d}")
        return names


def make_ancestor(
    seed: int = 0, concentration: float = 12.0, specs: dict | None = None
) -> AncestorGenome:
    """Sample gene features around each category's means from Beta distributions."""
    specs = CATEGORY_SPECS if specs is None else specs
    rng = np.random.default_rng(seed)
    features, category, pathway = [], [], []
    next_pathway = 0
    for ci, (n, per_pathway, means) in enumerate(specs.values()):
        m = np.clip(np.asarray(means), 0.02, 0.98)
        features.append(rng.beta(m * concentration, (1 - m) * concentration, size=(n, len(FEATURES))))
        category.append(np.full(n, ci))
        pathway.append(next_pathway + np.arange(n) // per_pathway)
        next_pathway = pathway[-1].max() + 1
    return AncestorGenome(
        features=np.concatenate(features),
        category=np.concatenate(category),
        pathway=np.concatenate(pathway),
        categories=tuple(specs),
    )
