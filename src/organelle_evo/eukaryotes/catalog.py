"""Eukaryotes for the free-living vs parasitic comparison.

Evolution is read from *pairs*: an extant free-living relative stands in for the
ancestor, and its relative (free-living control, or parasite) is the descendant.
Controls measure how much gene-family content drifts without a lifestyle change.
"""

FREE, PARASITE = "free_living", "parasite"

SPECIES = {
    # Amoebozoa
    "Dictyostelium discoideum": ("amoebozoa", FREE),
    "Dictyostelium purpureum": ("amoebozoa", FREE),
    "Entamoeba histolytica": ("amoebozoa", PARASITE),  # parasitic amoeba (amoebic dysentery)
    # Alveolates: a free-living ciliate as the proxy for ciliate and apicomplexan parasites
    "Tetrahymena thermophila": ("alveolata", FREE),
    "Ichthyophthirius multifiliis": ("alveolata", PARASITE),  # parasitic ciliate of fish
    "Plasmodium falciparum": ("alveolata", PARASITE),
    "Toxoplasma gondii": ("alveolata", PARASITE),
    "Cryptosporidium parvum": ("alveolata", PARASITE),
    # Kinetoplastids
    "Bodo saltans": ("discoba", FREE),
    "Leishmania major": ("discoba", PARASITE),
    "Trypanosoma brucei": ("discoba", PARASITE),
    # Heterolobosea
    "Naegleria gruberi": ("discoba", FREE),
    "Naegleria fowleri": ("discoba", FREE),  # mostly free-living; opportunistic pathogen
    # Fungi: a free-living chytrid as the proxy for microsporidia
    "Spizellomyces punctatus": ("fungi", FREE),
    "Encephalitozoon cuniculi": ("fungi", PARASITE),
    "Saccharomyces cerevisiae": ("fungi", FREE),
    "Kluyveromyces lactis": ("fungi", FREE),
    # Green algae
    "Chlamydomonas reinhardtii": ("chlorophyta", FREE),
    "Volvox carteri": ("chlorophyta", FREE),
    # Choanoflagellates and animals
    "Monosiga brevicollis": ("holozoa", FREE),
    "Salpingoeca rosetta": ("holozoa", FREE),
    "Drosophila melanogaster": ("holozoa", FREE),
    "Anopheles gambiae": ("holozoa", FREE),
}

# (ancestor proxy, descendant)
PAIRS = [
    # lifestyle change: free-living -> parasite
    ("Dictyostelium discoideum", "Entamoeba histolytica"),
    ("Tetrahymena thermophila", "Ichthyophthirius multifiliis"),
    ("Tetrahymena thermophila", "Plasmodium falciparum"),
    ("Tetrahymena thermophila", "Toxoplasma gondii"),
    ("Tetrahymena thermophila", "Cryptosporidium parvum"),
    ("Bodo saltans", "Leishmania major"),
    ("Bodo saltans", "Trypanosoma brucei"),
    ("Spizellomyces punctatus", "Encephalitozoon cuniculi"),
    # controls: free-living -> free-living
    ("Dictyostelium discoideum", "Dictyostelium purpureum"),
    ("Naegleria gruberi", "Naegleria fowleri"),
    ("Saccharomyces cerevisiae", "Kluyveromyces lactis"),
    ("Chlamydomonas reinhardtii", "Volvox carteri"),
    ("Monosiga brevicollis", "Salpingoeca rosetta"),
    ("Drosophila melanogaster", "Anopheles gambiae"),
]


def lifestyle(species: str) -> str:
    return SPECIES[species][1]


def slug(name: str) -> str:
    import re

    return re.sub(r"[^A-Za-z0-9]+", "_", name).strip("_")
