"""Animals, for learning composition laws on animal cells directly.

The project's temperature law was fitted to bacteria and archaea, where the cell's
temperature is the habitat temperature. It does not transfer to animals: endotherms, whose
cells run 17 C warmer than ectotherms', carry *less* IVYWREL, not more
(laws/animal_temperature_v1.json, opposite sign, 2.3x the predicted effect). So the axes
have to be re-learned on animals, with the variables an animal cell actually experiences.

Axes (approximate, from the literature; the point is the contrast, not the third digit):

    tcell     temperature the cells normally operate at, deg C. For endotherms this is the
              core body temperature and is decoupled from climate; for ectotherms it is the
              typical habitat temperature; for parasites of warm-blooded hosts it is the
              host's temperature.
    osmol     intracellular osmolarity, mOsm. The honest analogue of the microbial salt
              axis. Marine invertebrates are osmoconformers and hold ~1000 mOsm, matching
              seawater; vertebrates, freshwater and terrestrial animals osmoregulate near
              300. Cartilaginous fishes conform to ~1000 but with urea and TMAO rather
              than inorganic ions, so they are flagged separately (urea=1).
    hypoxia   1 if the lineage routinely lives with little or no oxygen (host gut and
              blood, intertidal and burrowing sediment animals), else 0.
    endo      1 endotherm (holds its own cell temperature), 0 ectotherm. Kept apart from
              tcell so "warm cells" and "regulated cells" can be told apart.
    parasite  1 parasite. This project has already shown parasitism changes composition on
              its own, so it is an axis here rather than a confound.
    urea      1 osmoconformer using urea/TMAO instead of inorganic ions.

Temperature spans about -1 C (Antarctic notothenioid fishes) to 42 C (birds), and
osmolarity and temperature are deliberately crossed: there are cold and warm species at
both osmolarities, so the two axes are not confounded with each other or with one clade.
"""

from typing import NamedTuple


class Env(NamedTuple):
    group: str
    tcell: float
    osmol: float
    hypoxia: int = 0
    endo: int = 0
    parasite: int = 0
    urea: int = 0


def _mammal(t=37.0):
    return Env("mammal", t, 300, endo=1)


def _bird(t=41.0):
    return Env("bird", t, 300, endo=1)


SPECIES = {
    # --- Mammals: cells at 32-39 C, osmoregulated. Platypus and sloth run cool for mammals.
    "Homo sapiens": _mammal(37.0),
    "Mus musculus": _mammal(37.0),
    "Bos taurus": _mammal(38.5),
    "Canis lupus familiaris": _mammal(38.5),
    "Monodelphis domestica": _mammal(34.5),  # marsupial, lower core temperature
    "Ornithorhynchus anatinus": _mammal(32.0),  # platypus, lowest mammalian core temperature
    "Balaenoptera musculus": _mammal(36.0),  # marine, but osmoregulates like any mammal
    "Tursiops truncatus": _mammal(37.0),

    # --- Birds: the hottest cells in the set
    "Gallus gallus": _bird(41.5),
    "Taeniopygia guttata": _bird(41.0),
    "Anas platyrhynchos": _bird(41.5),
    "Aptenodytes forsteri": _bird(38.0),  # emperor penguin, Antarctic but endothermic

    # --- Reptiles: ectotherms, osmoregulated, active body temperatures
    "Anolis carolinensis": Env("reptile", 30.0, 300),
    "Python bivittatus": Env("reptile", 30.0, 300),
    "Chrysemys picta bellii": Env("reptile", 24.0, 300, hypoxia=1),  # overwinters anoxic under ice
    "Crocodylus porosus": Env("reptile", 30.0, 300),
    "Pogona vitticeps": Env("reptile", 35.0, 300),

    # --- Amphibians: ectotherms, freshwater
    "Xenopus tropicalis": Env("amphibian", 26.0, 300),
    "Xenopus laevis": Env("amphibian", 22.0, 300),
    "Nanorana parkeri": Env("amphibian", 12.0, 300),  # Tibetan plateau, cold
    "Bufo bufo": Env("amphibian", 15.0, 300),

    # --- Ray-finned fishes: osmoregulators (~300) across a huge temperature range
    "Danio rerio": Env("teleost", 26.0, 300),
    "Oryzias latipes": Env("teleost", 25.0, 300),
    "Takifugu rubripes": Env("teleost", 20.0, 300),
    "Oreochromis niloticus": Env("teleost", 28.0, 300),
    "Gadus morhua": Env("teleost", 5.0, 300),  # North Atlantic cod
    "Oncorhynchus mykiss": Env("teleost", 12.0, 300),
    "Salmo salar": Env("teleost", 10.0, 300),
    "Notothenia coriiceps": Env("teleost", -1.0, 300),  # Antarctic, below zero
    "Pseudochaenichthys georgianus": Env("teleost", -1.0, 300),  # Antarctic icefish
    "Astyanax mexicanus": Env("teleost", 22.0, 300),
    "Periophthalmus magnuspinnatus": Env("teleost", 27.0, 300, hypoxia=1),  # mudskipper, intertidal mud

    # --- Cartilaginous fishes: conform to seawater with urea and TMAO
    "Callorhinchus milii": Env("chondrichthyan", 12.0, 1000, urea=1),
    "Scyliorhinus canicula": Env("chondrichthyan", 12.0, 1000, urea=1),
    "Rhincodon typus": Env("chondrichthyan", 25.0, 1000, urea=1),
    "Chiloscyllium punctatum": Env("chondrichthyan", 26.0, 1000, urea=1),
    "Amblyraja radiata": Env("chondrichthyan", 4.0, 1000, urea=1),  # cold North Atlantic

    # --- Lancelet and tunicates: marine osmoconformers at the base of the chordates
    "Branchiostoma floridae": Env("cephalochordate", 22.0, 1000),
    "Ciona intestinalis": Env("tunicate", 18.0, 1000),

    # --- Marine invertebrates: osmoconformers near 1000 mOsm, cold to tropical
    "Strongylocentrotus purpuratus": Env("echinoderm", 14.0, 1000),
    "Lytechinus variegatus": Env("echinoderm", 26.0, 1000),
    "Acanthaster planci": Env("echinoderm", 27.0, 1000),
    "Octopus bimaculoides": Env("mollusc", 18.0, 1000),
    "Aplysia californica": Env("mollusc", 18.0, 1000),
    "Crassostrea gigas": Env("mollusc", 20.0, 1000, hypoxia=1),  # intertidal, tolerates anoxia
    "Mytilus edulis": Env("mollusc", 12.0, 1000, hypoxia=1),  # intertidal, cold
    "Pecten maximus": Env("mollusc", 12.0, 1000),
    "Lottia gigantea": Env("mollusc", 15.0, 1000, hypoxia=1),
    "Acropora millepora": Env("cnidarian", 27.0, 1000),  # tropical reef coral
    "Nematostella vectensis": Env("cnidarian", 20.0, 1000),
    "Hydra vulgaris": Env("cnidarian", 20.0, 300),  # freshwater cnidarian: the useful control
    "Amphimedon queenslandica": Env("sponge", 25.0, 1000),
    "Capitella teleta": Env("annelid", 18.0, 1000, hypoxia=1),  # organic-rich sediment
    "Penaeus vannamei": Env("crustacean", 27.0, 1000),
    "Eurytemora affinis": Env("crustacean", 15.0, 1000),

    # --- Freshwater and terrestrial invertebrates: osmoregulate near 300
    "Daphnia pulex": Env("crustacean", 20.0, 300),
    "Helobdella robusta": Env("annelid", 20.0, 300),
    "Schmidtea mediterranea": Env("flatworm", 20.0, 300),
    "Caenorhabditis elegans": Env("nematode", 20.0, 300),
    "Drosophila melanogaster": Env("insect", 25.0, 300),
    "Anopheles gambiae": Env("insect", 27.0, 300),
    "Apis mellifera": Env("insect", 35.0, 300),  # brood nest is held near 35 C
    "Bombyx mori": Env("insect", 25.0, 300),
    "Tribolium castaneum": Env("insect", 30.0, 300),
    "Acyrthosiphon pisum": Env("insect", 20.0, 300),
    "Belgica antarctica": Env("insect", 2.0, 300),  # Antarctic midge
    "Ixodes scapularis": Env("arachnid", 22.0, 300),
    "Tetranychus urticae": Env("arachnid", 27.0, 300),

    # --- Parasites of warm-blooded hosts: cells at host temperature, often little oxygen
    "Ascaris suum": Env("nematode", 39.0, 300, hypoxia=1, parasite=1),
    "Brugia malayi": Env("nematode", 37.0, 300, parasite=1),
    "Trichinella spiralis": Env("nematode", 37.0, 300, parasite=1),
    "Schistosoma mansoni": Env("flatworm", 37.0, 300, hypoxia=1, parasite=1),
    "Echinococcus granulosus": Env("flatworm", 37.0, 300, hypoxia=1, parasite=1),
    "Hymenolepis microstoma": Env("flatworm", 37.0, 300, hypoxia=1, parasite=1),
}


def slug(name: str) -> str:
    import re

    return re.sub(r"[^A-Za-z0-9]+", "_", name).strip("_")


def axes(species: str):
    """The design row for a species: the axes a law is fitted on."""
    e = SPECIES[species]
    return {"tcell": e.tcell, "osmol_high": 1.0 if e.osmol > 600 else 0.0,
            "hypoxia": float(e.hypoxia), "endo": float(e.endo),
            "parasite": float(e.parasite), "urea": float(e.urea)}
