"""Richer per-family features: GO-slim functions, Pfam clans and cross-species statistics.

The base features (hydrophobicity, TM helices, length and five coarse classes) describe
a family too thinly to predict its fate. This adds
  - GO-slim functional categories (from pfam2go, mapped up the GO graph),
  - Pfam clan membership and clan size,
  - HMM model length,
  - ubiquity (share of free-living species carrying the family) and its typical copy
    number among free-living species.
Ubiquity uses free-living species only; descendants in the evaluation are parasites, so
a held-out parasite never informs its own features.
"""

import re

import numpy as np

from .catalog import FREE, SPECIES
from .model import FAMILY_FEATURES, family_features

MIN_FAMILIES_PER_SLIM = 60


def enriched_features(profiles: dict, meta: dict, annotations: dict, counts_by_species: dict):
    """(family names, feature names, X). profiles: species -> profile JSON."""
    fams, base = family_features(list(profiles.values()), meta)
    ann = annotations["families"]
    slim_names = annotations["slims"]

    free = [s for s in counts_by_species if SPECIES.get(s) and SPECIES[s].lifestyle == FREE]
    free_counts = np.array([counts_by_species[s] for s in free])  # (S, F)
    present = free_counts > 0
    ubiquity = present.mean(0)
    mean_copies = np.where(present.any(0), free_counts.sum(0) / np.maximum(present.sum(0), 1), 0.0)

    hmm_len = np.array([meta.get(f, {}).get("length", 100) for f in fams], dtype=float)
    clan = [ann.get(f, {}).get("clan") for f in fams]
    clan_size: dict[str, int] = {}
    for c in clan:
        if c:
            clan_size[c] = clan_size.get(c, 0) + 1
    in_clan = np.array([c is not None for c in clan], dtype=float)
    log_clan = np.array([np.log1p(clan_size[c]) if c else 0.0 for c in clan])

    fam_slims = [set(ann.get(f, {}).get("go_slim", ())) for f in fams]
    slim_counts: dict[str, int] = {}
    for s in fam_slims:
        for t in s:
            if t in slim_names:
                slim_counts[t] = slim_counts.get(t, 0) + 1
    slims = sorted(t for t, n in slim_counts.items() if n >= MIN_FAMILIES_PER_SLIM)
    go = np.array([[t in s for t in slims] for s in fam_slims], dtype=float)
    has_go = np.array([bool(s) for s in fam_slims], dtype=float)

    kw = np.array([[bool(re.search(pat, f"{f} {meta.get(f, {}).get('description', '')}"))
                    for _, pat in KEYWORD_CLASSES] for f in fams], dtype=float)

    cont = np.stack([ubiquity, np.log1p(mean_copies), np.log(hmm_len), log_clan], 1)
    cont = (cont - cont.mean(0)) / np.where(cont.std(0) > 0, cont.std(0), 1)
    names = [*FAMILY_FEATURES, "ubiquity_free_living", "copies_free_living", "hmm_length", "clan_size",
             "in_clan", "has_go_annotation", *[f"go:{slim_names[t]['name']}" for t in slims],
             *[f"kw:{name}" for name, _ in KEYWORD_CLASSES]]
    x = np.concatenate([base, cont, in_clan[:, None], has_go[:, None], go, kw], axis=1)
    return fams, names, x


# Function keywords in Pfam names/descriptions: much wider coverage than pfam2go.
KEYWORD_CLASSES = [
    # (?i:...) for ordinary words; gene-style abbreviations stay case-sensitive with word
    # boundaries so that e.g. "Ras" does not match "transferase".
    ("kinase", r"(?i:kinase)"),
    ("phosphatase", r"(?i:phosphatase)"),
    ("transporter_channel", r"(?i:transporter|channel|permease|carrier|symporter|antiporter)|\bABC_|\bMFS"),
    ("zinc_finger", r"(?i:zinc.finger)|\bzf-|\bRING\b"),
    ("repeat_domain", r"(?i:ankyrin|tetratricopeptide|leucine.rich|kelch|armadillo|WD40|WD domain)|\b(ANK|TPR|LRR|HEAT)"),
    ("ubiquitin_system", r"(?i:ubiquitin|F-box)|\b(UBA|UBX|SCF)\b"),
    ("protease", r"(?i:peptidase|protease|proteasome)"),
    ("helicase_nucleic", r"(?i:helicase|nuclease|polymerase)|\b(DEAD|DEAH|RNase)"),
    ("gtpase_signalling", r"(?i:GTPase|G-protein|guanine nucleotide)|\b(Ras|Rab|Arf|Ran|Rho)\b"),
    ("methyl_glyco_transferase", r"(?i:methyltransferase|glycosyl.?transferase|glycosyl hydrolase)|\bGlyco_"),
    ("cytoskeleton_motor", r"(?i:\bactin|tubulin|kinesin|dynein|myosin|microtubule)"),
    ("cilium_flagellum", r"(?i:flagell|\bcili|axonem|intraflagellar)|\bIFT"),
    ("cell_adhesion_surface", r"(?i:adhesion|cadherin|integrin|lectin|fibronectin|immunoglobulin|Ig-like)|\bEGF"),
    ("lipid_metabolism", r"(?i:lipase|fatty acid|acyl.?transferase|sterol|lipid)"),
    ("amino_acid_metabolism", r"(?i:amino.?acid|aminotransferase|dehydratase)"),
    ("uncharacterised", r"(?i:uncharacteri[sz]ed|unknown function)|\b(DUF|UPF)\d"),
]
