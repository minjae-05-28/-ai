"""Different endosymbiotic systems: same machinery, different ancestors and laws.

- mitochondrion       : alphaproteobacterium inside an archaeal host
- plastid             : cyanobacterium inside a eukaryote (chloroplast, and by extension
                        cyanelles, apicoplasts and the Paulinella chromatophore)
- insect_endosymbiont : gammaproteobacterium inside insect bacteriocytes (Buchnera,
                        Blochmannia, Wigglesworthia...). No route to a host nucleus, so
                        genes are only ever lost; genes that make nutrients the host's
                        diet lacks (essential amino acids, vitamins) are what is kept.
"""

from dataclasses import dataclass

from .ancestor import CATEGORY_SPECS, AncestorGenome, make_ancestor
from .simulator import TRUE_RULES, Rules


@dataclass(frozen=True)
class SystemSpec:
    name: str
    host: str
    ancestor: str
    categories: dict
    true_rules: Rules

    def make_ancestor(self, seed: int = 0) -> AncestorGenome:
        return make_ancestor(seed, specs=self.categories)


PLASTID_CATEGORIES = {
    # name: (n_genes, genes_per_pathway, (hydrophobicity, redox, host_redundancy, essentiality))
    "photosystem_ii": (30, 10, (0.75, 0.95, 0.05, 0.90)),
    "photosystem_i": (15, 5, (0.65, 0.90, 0.05, 0.90)),
    "cytochrome_b6f": (8, 4, (0.70, 0.85, 0.05, 0.90)),
    "atp_synthase": (9, 9, (0.55, 0.50, 0.10, 0.90)),
    "rubisco_calvin": (20, 10, (0.10, 0.40, 0.30, 0.80)),
    "ribosome": (55, 11, (0.15, 0.10, 0.30, 0.80)),
    "rna_polymerase": (6, 3, (0.10, 0.20, 0.40, 0.80)),
    "ndh_complex": (15, 5, (0.70, 0.60, 0.30, 0.40)),
    "chlorophyll_biosynthesis": (25, 5, (0.30, 0.30, 0.40, 0.60)),
    "cell_envelope": (60, 10, (0.45, 0.05, 0.70, 0.10)),
    "nitrogen_metabolism": (40, 10, (0.15, 0.10, 0.80, 0.20)),
    "circadian_regulation": (40, 10, (0.10, 0.10, 0.80, 0.10)),
    "transport": (60, 10, (0.70, 0.10, 0.60, 0.30)),
    "dna_replication_repair": (40, 10, (0.10, 0.10, 0.50, 0.50)),
}

ENDOSYMBIONT_CATEGORIES = {
    "essential_aa_biosynthesis": (60, 10, (0.15, 0.05, 0.05, 0.90)),
    "nonessential_aa_biosynthesis": (40, 10, (0.15, 0.05, 0.80, 0.20)),
    "vitamin_biosynthesis": (30, 10, (0.15, 0.10, 0.20, 0.70)),
    "ribosome_translation": (80, 10, (0.15, 0.10, 0.20, 0.90)),
    "rna_polymerase": (6, 3, (0.10, 0.20, 0.20, 0.90)),
    "respiration": (35, 7, (0.70, 0.80, 0.30, 0.50)),
    "dna_repair_recombination": (45, 9, (0.10, 0.10, 0.50, 0.25)),
    "cell_envelope": (80, 10, (0.45, 0.05, 0.60, 0.15)),
    "motility_chemotaxis": (50, 10, (0.30, 0.02, 0.90, 0.05)),
    "regulation_signalling": (80, 10, (0.10, 0.10, 0.70, 0.10)),
    "transport": (90, 10, (0.70, 0.10, 0.50, 0.30)),
    "stress_response": (40, 10, (0.10, 0.10, 0.60, 0.20)),
}

SYSTEMS = {
    "mitochondrion": SystemSpec(
        "mitochondrion", "archaeon (Asgard)", "alphaproteobacterium", CATEGORY_SPECS, TRUE_RULES
    ),
    "plastid": SystemSpec(
        "plastid",
        "eukaryote",
        "cyanobacterium",
        PLASTID_CATEGORIES,
        # CoRR was first proposed for chloroplasts: redox coupling is the strongest brake.
        Rules(-1.0, (-2.5, -3.0, 0.5, 1.5), -1.5, (0.0, -0.5, 3.0, -3.0)),
    ),
    "insect_endosymbiont": SystemSpec(
        "insect_endosymbiont",
        "insect (bacteriocyte)",
        "gammaproteobacterium",
        ENDOSYMBIONT_CATEGORIES,
        # Effectively no gene transfer; loss is driven by redundancy and host service.
        Rules(-12.0, (0.0, 0.0, 0.0, 0.0), -1.0, (0.3, -0.3, 3.0, -3.5)),
    ),
}
