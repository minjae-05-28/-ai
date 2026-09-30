"""Eukaryotes for the free-living vs parasitic comparison.

Evolution is read from *pairs*: an extant free-living relative stands in for the
ancestor, and its relative (free-living control, or parasite) is the descendant.
Controls measure how much gene-family content drifts without a lifestyle change.

Each species is described on three axes, so laws can be split instead of lumping all
parasites together:

- lifestyle : free-living or parasite
- location  : free, extracellular (in the host but outside its cells) or intracellular
- energy    : aerobic (respiring mitochondria) or reduced (mitosomes/hydrogenosomes,
              no oxidative phosphorylation)
"""

from typing import NamedTuple

FREE, PARASITE = "free_living", "parasite"
EXTRA, INTRA = "extracellular", "intracellular"
AEROBIC, REDUCED = "aerobic", "reduced"


class Species(NamedTuple):
    group: str
    lifestyle: str
    location: str
    energy: str


def _free(group, energy=AEROBIC):
    return Species(group, FREE, "free", energy)


def _par(group, location, energy):
    return Species(group, PARASITE, location, energy)


SPECIES = {
    # Amoebozoa
    "Dictyostelium discoideum": _free("amoebozoa"),
    "Dictyostelium purpureum": _free("amoebozoa"),
    "Acanthamoeba castellanii": _free("amoebozoa"),
    "Mastigamoeba balamuthi": _free("amoebozoa", REDUCED),  # free-living anaerobe, Entamoeba's relative
    "Entamoeba histolytica": _par("amoebozoa", EXTRA, REDUCED),
    # Alveolates
    "Tetrahymena thermophila": _free("alveolata"),
    "Chromera velia": _free("alveolata"),  # free-living photosynthetic relatives of apicomplexans
    "Vitrella brassicaformis": _free("alveolata"),
    "Ichthyophthirius multifiliis": _par("alveolata", EXTRA, AEROBIC),  # parasitic ciliate of fish skin
    "Perkinsus marinus": _par("alveolata", INTRA, AEROBIC),  # oyster parasite
    "Plasmodium falciparum": _par("alveolata", INTRA, AEROBIC),
    "Babesia bovis": _par("alveolata", INTRA, AEROBIC),
    "Toxoplasma gondii": _par("alveolata", INTRA, AEROBIC),
    "Eimeria tenella": _par("alveolata", INTRA, AEROBIC),
    "Cryptosporidium parvum": _par("alveolata", INTRA, REDUCED),  # mitosome, no respiratory chain
    # Kinetoplastids and Heterolobosea
    "Bodo saltans": _free("discoba"),
    "Leishmania major": _par("discoba", INTRA, AEROBIC),  # inside macrophages
    "Trypanosoma cruzi": _par("discoba", INTRA, AEROBIC),
    "Trypanosoma brucei": _par("discoba", EXTRA, AEROBIC),  # bloodstream, extracellular
    "Naegleria gruberi": _free("discoba"),
    "Naegleria fowleri": _free("discoba"),  # mostly free-living; opportunistic pathogen
    # Fungi: a free-living chytrid as the proxy for Rozella and microsporidia
    "Spizellomyces punctatus": _free("fungi"),
    "Rozella allomycis": _par("fungi", INTRA, AEROBIC),  # keeps mitochondria
    "Encephalitozoon cuniculi": _par("fungi", INTRA, REDUCED),  # microsporidia: mitosomes
    "Nosema ceranae": _par("fungi", INTRA, REDUCED),
    "Saccharomyces cerevisiae": _free("fungi"),
    "Kluyveromyces lactis": _free("fungi"),
    # Green algae
    "Chlamydomonas reinhardtii": _free("chlorophyta"),
    "Volvox carteri": _free("chlorophyta"),
    # Choanoflagellates and animals
    "Monosiga brevicollis": _free("holozoa"),
    "Salpingoeca rosetta": _free("holozoa"),
    "Drosophila melanogaster": _free("holozoa"),
    "Anopheles gambiae": _free("holozoa"),
}

# (ancestor proxy candidates, closest first; descendant)
_APICOMPLEXAN_PROXY = ("Chromera velia", "Vitrella brassicaformis", "Tetrahymena thermophila")
PAIR_SPECS = [
    # lifestyle or energy change
    (("Mastigamoeba balamuthi", "Dictyostelium discoideum"), "Entamoeba histolytica"),
    (("Dictyostelium discoideum",), "Mastigamoeba balamuthi"),  # free-living, mitochondria reduced
    (("Tetrahymena thermophila",), "Ichthyophthirius multifiliis"),
    (("Tetrahymena thermophila",), "Perkinsus marinus"),
    (_APICOMPLEXAN_PROXY, "Plasmodium falciparum"),
    (_APICOMPLEXAN_PROXY, "Babesia bovis"),
    (_APICOMPLEXAN_PROXY, "Toxoplasma gondii"),
    (_APICOMPLEXAN_PROXY, "Eimeria tenella"),
    (_APICOMPLEXAN_PROXY, "Cryptosporidium parvum"),
    (("Bodo saltans",), "Leishmania major"),
    (("Bodo saltans",), "Trypanosoma cruzi"),
    (("Bodo saltans",), "Trypanosoma brucei"),
    (("Spizellomyces punctatus",), "Rozella allomycis"),
    (("Spizellomyces punctatus",), "Encephalitozoon cuniculi"),
    (("Spizellomyces punctatus",), "Nosema ceranae"),
    # controls: free-living -> free-living
    (("Dictyostelium discoideum",), "Dictyostelium purpureum"),
    (("Dictyostelium discoideum",), "Acanthamoeba castellanii"),
    (("Chromera velia",), "Vitrella brassicaformis"),
    (("Naegleria gruberi",), "Naegleria fowleri"),
    (("Saccharomyces cerevisiae",), "Kluyveromyces lactis"),
    (("Chlamydomonas reinhardtii",), "Volvox carteri"),
    (("Monosiga brevicollis",), "Salpingoeca rosetta"),
    (("Drosophila melanogaster",), "Anopheles gambiae"),
]

# Design axes for splitting laws: every pair gets a base law plus the effect of each
# axis that applies to its descendant.
AXES = ("parasite", "intracellular", "reduced_mitochondria")


def design(species: str) -> tuple[float, ...]:
    s = SPECIES[species]
    return (1.0, float(s.lifestyle == PARASITE), float(s.location == INTRA), float(s.energy == REDUCED))


def resolve_pairs(available) -> list[tuple[str, str]]:
    """(proxy, descendant) pairs, using the closest proxy that was profiled."""
    out = []
    for proxies, desc in PAIR_SPECS:
        if desc not in available:
            continue
        proxy = next((p for p in proxies if p in available and p != desc), None)
        if proxy is not None:
            out.append((proxy, desc))
    return out


# Kept for code written against the original 14 pairs.
PAIRS = resolve_pairs(SPECIES)


def lifestyle(species: str) -> str:
    return SPECIES[species].lifestyle


def slug(name: str) -> str:
    import re

    return re.sub(r"[^A-Za-z0-9]+", "_", name).strip("_")
