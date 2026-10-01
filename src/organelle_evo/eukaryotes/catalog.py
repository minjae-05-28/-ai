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
    # Mastigamoeba balamuthi (free-living anaerobe, Entamoeba's relative) would separate
    # "reduced mitochondria" from parasitism, but NCBI has no annotated assembly for it.
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

# Expansion toward ~90 species: more parasites, each with a free-living relative, plus
# free-living controls in new groups. Lifestyle labels follow the standard literature.
SPECIES.update({
    # Fungi
    "Schizosaccharomyces pombe": _free("fungi_tapho"),
    "Pneumocystis jirovecii": _par("fungi_tapho", EXTRA, AEROBIC),  # lung parasite
    "Taphrina deformans": _par("fungi_tapho", EXTRA, AEROBIC),  # peach leaf curl
    "Neurospora crassa": _free("fungi"),
    "Aspergillus nidulans": _free("fungi"),
    "Coprinopsis cinerea": _free("fungi_basidio"),
    "Schizophyllum commune": _free("fungi_basidio"),
    "Ustilago maydis": _par("fungi_basidio", INTRA, AEROBIC),  # corn smut, intracellular hyphae
    "Malassezia globosa": _par("fungi_basidio", EXTRA, AEROBIC),  # skin
    "Batrachochytrium dendrobatidis": _par("fungi", INTRA, AEROBIC),  # amphibian chytrid
    "Enterocytozoon bieneusi": _par("fungi", INTRA, REDUCED),  # microsporidia
    "Nematocida parisii": _par("fungi", INTRA, REDUCED),
    "Vavraia culicis": _par("fungi", INTRA, REDUCED),
    "Encephalitozoon intestinalis": _par("fungi", INTRA, REDUCED),
    # Alveolates
    "Plasmodium vivax": _par("alveolata", INTRA, AEROBIC),
    "Plasmodium berghei": _par("alveolata", INTRA, AEROBIC),
    "Plasmodium knowlesi": _par("alveolata", INTRA, AEROBIC),
    "Theileria annulata": _par("alveolata", INTRA, AEROBIC),
    "Theileria parva": _par("alveolata", INTRA, AEROBIC),
    "Babesia microti": _par("alveolata", INTRA, AEROBIC),
    "Neospora caninum": _par("alveolata", INTRA, AEROBIC),
    "Hammondia hammondi": _par("alveolata", INTRA, AEROBIC),
    "Cyclospora cayetanensis": _par("alveolata", INTRA, AEROBIC),
    "Cryptosporidium hominis": _par("alveolata", INTRA, REDUCED),
    # Kinetoplastids
    "Leishmania infantum": _par("discoba", INTRA, AEROBIC),
    "Leishmania donovani": _par("discoba", INTRA, AEROBIC),
    "Trypanosoma vivax": _par("discoba", EXTRA, AEROBIC),
    "Trypanosoma congolense": _par("discoba", EXTRA, AEROBIC),
    "Leptomonas pyrrhocoris": _par("discoba", EXTRA, AEROBIC),
    # Amoebozoa
    "Entamoeba dispar": _par("amoebozoa", EXTRA, REDUCED),
    "Entamoeba invadens": _par("amoebozoa", EXTRA, REDUCED),
    # Metamonads (anaerobic gut parasites; the nearest annotated free-living proxy is distant)
    "Giardia intestinalis": _par("metamonada", EXTRA, REDUCED),
    "Spironucleus salmonicida": _par("metamonada", EXTRA, REDUCED),
    # Stramenopiles
    "Thalassiosira pseudonana": _free("stramenopiles"),
    "Phaeodactylum tricornutum": _free("stramenopiles"),
    "Phytophthora infestans": _par("stramenopiles", EXTRA, AEROBIC),  # potato blight
    "Saprolegnia parasitica": _par("stramenopiles", EXTRA, AEROBIC),  # fish pathogen
    "Blastocystis hominis": _par("stramenopiles", EXTRA, REDUCED),  # gut, anaerobic MROs
    # Rhizaria
    # Bigelowiella natans (free-living proxy for Plasmodiophora) has no annotated assembly in NCBI.
    "Plasmodiophora brassicae": _par("rhizaria", INTRA, AEROBIC),  # clubroot
    # Animals: cnidarians that became parasites (Myxozoa), nematodes, flatworms
    "Nematostella vectensis": _free("cnidaria"),
    "Hydra vulgaris": _free("cnidaria"),
    "Thelohanellus kitauei": _par("cnidaria", EXTRA, AEROBIC),
    "Henneguya salminicola": _par("cnidaria", EXTRA, REDUCED),  # lost its mitochondrial genome
    "Caenorhabditis elegans": _free("nematoda"),
    "Brugia malayi": _par("nematoda", EXTRA, AEROBIC),
    "Trichinella spiralis": _par("nematoda", INTRA, AEROBIC),  # inside muscle cells
    "Schistosoma mansoni": _par("platyhelminthes", EXTRA, AEROBIC),  # blood fluke
    "Capsaspora owczarzaki": _free("holozoa"),
    # Green and red algae
    "Auxenochlorella protothecoides": _free("chlorophyta"),
    "Helicosporidium sp. ATCC 50920": _par("chlorophyta", EXTRA, AEROBIC),  # non-photosynthetic insect parasite
    "Chlorella variabilis": _free("chlorophyta"),
    "Ostreococcus lucimarinus": _free("chlorophyta"),
    "Ostreococcus tauri": _free("chlorophyta"),
    "Cyanidioschyzon merolae": _free("rhodophyta"),
    "Galdieria sulphuraria": _free("rhodophyta"),
})

# No annotated NCBI assembly (failed twice, removed): Melampsora larici-populina,
# Hyaloperonospora arabidopsidis, Albugo laibachii, Pythium ultimum, Paratrypanosoma confusum,
# Sarcocystis neurona, Ascaris suum, Onchocerca volvulus, Schmidtea mediterranea,
# Hymenolepis microstoma.
# Round 3 (public repo, Actions minutes unlimited): species chosen to test the laws where
# they are weakest — extracellular vs intracellular within a clade, a microsporidian
# relative that kept its mitochondria, new origins of plant parasitism, flatworms with a
# free-living flatworm proxy, and free-living controls inside parasite-rich clades.
SPECIES.update({
    # Fungi: plant biotrophs (haustoria inside host cells), microsporidia and a relative
    "Blumeria graminis": _par("fungi", INTRA, AEROBIC),  # powdery mildew, obligate
    "Pyricularia oryzae": _par("fungi", INTRA, AEROBIC),  # rice blast, invasive hyphae
    "Puccinia graminis": _par("fungi_basidio", INTRA, AEROBIC),  # stem rust, obligate
    "Laccaria bicolor": _free("fungi_basidio"),  # ectomycorrhizal mutualist
    "Mitosporidium daphniae": _par("fungi", INTRA, AEROBIC),  # early microsporidian, keeps mitochondria
    "Edhazardia aedis": _par("fungi", INTRA, REDUCED),
    "Anncaliia algerae": _par("fungi", INTRA, REDUCED),
    "Nosema bombycis": _par("fungi", INTRA, REDUCED),
    "Pseudoloma neurophilia": _par("fungi", INTRA, REDUCED),
    # Oomycetes
    "Phytophthora sojae": _par("stramenopiles", EXTRA, AEROBIC),
    "Aphanomyces astaci": _par("stramenopiles", EXTRA, AEROBIC),  # crayfish plague
    # Kinetoplastids: extracellular insect and vertebrate parasites vs intracellular Leishmania
    "Angomonas deanei": _par("discoba", EXTRA, AEROBIC),  # insect gut
    "Strigomonas culicis": _par("discoba", EXTRA, AEROBIC),
    "Trypanosoma grayi": _par("discoba", EXTRA, AEROBIC),
    "Leishmania braziliensis": _par("discoba", INTRA, AEROBIC),
    "Leishmania mexicana": _par("discoba", INTRA, AEROBIC),
    # Alveolates: an extracellular gut gregarine, more intracellular coccidia and Plasmodium,
    # and a free-living ciliate control
    "Gregarina niphandrodes": _par("alveolata", EXTRA, AEROBIC),
    "Besnoitia besnoiti": _par("alveolata", INTRA, AEROBIC),
    "Plasmodium yoelii": _par("alveolata", INTRA, AEROBIC),
    "Plasmodium malariae": _par("alveolata", INTRA, AEROBIC),
    "Paramecium tetraurelia": _free("alveolata"),
    # Nematodes
    "Haemonchus contortus": _par("nematoda", EXTRA, AEROBIC),
    "Strongyloides ratti": _par("nematoda", EXTRA, AEROBIC),
    "Caenorhabditis briggsae": _free("nematoda"),
    "Pristionchus pacificus": _free("nematoda"),
    # Flatworms, with free-living flatworms as proxies
    "Macrostomum lignano": _free("platyhelminthes"),
    "Echinococcus multilocularis": _par("platyhelminthes", EXTRA, AEROBIC),
    "Fasciola hepatica": _par("platyhelminthes", EXTRA, AEROBIC),
    "Clonorchis sinensis": _par("platyhelminthes", EXTRA, AEROBIC),
    "Schistosoma japonicum": _par("platyhelminthes", EXTRA, AEROBIC),
    # Parabasalids (anaerobic, hydrogenosomes)
    "Trichomonas vaginalis": _par("metamonada", EXTRA, REDUCED),
    "Tritrichomonas foetus": _par("metamonada", EXTRA, REDUCED),
    # An insect ectoparasite
    "Pediculus humanus": _par("holozoa", EXTRA, AEROBIC),  # body louse
})

# (ancestor proxy candidates, closest first; descendant)
_APICOMPLEXAN_PROXY = ("Chromera velia", "Vitrella brassicaformis", "Tetrahymena thermophila")
_FLATWORM_PROXY = ("Macrostomum lignano", "Caenorhabditis elegans")
PAIR_SPECS = [
    # lifestyle or energy change
    (("Dictyostelium discoideum",), "Entamoeba histolytica"),
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

PAIR_SPECS += [
    (("Schizosaccharomyces pombe",), "Pneumocystis jirovecii"),
    (("Schizosaccharomyces pombe",), "Taphrina deformans"),
    (("Coprinopsis cinerea",), "Ustilago maydis"),
    (("Coprinopsis cinerea",), "Malassezia globosa"),
    (("Spizellomyces punctatus",), "Batrachochytrium dendrobatidis"),
    (("Spizellomyces punctatus",), "Enterocytozoon bieneusi"),
    (("Spizellomyces punctatus",), "Nematocida parisii"),
    (("Spizellomyces punctatus",), "Vavraia culicis"),
    (("Spizellomyces punctatus",), "Encephalitozoon intestinalis"),
    *[(_APICOMPLEXAN_PROXY, sp) for sp in (
        "Plasmodium vivax", "Plasmodium berghei", "Plasmodium knowlesi", "Theileria annulata",
        "Theileria parva", "Babesia microti", "Neospora caninum", "Hammondia hammondi",
        "Cyclospora cayetanensis", "Cryptosporidium hominis")],
    *[(("Bodo saltans",), sp) for sp in (
        "Leishmania infantum", "Leishmania donovani", "Trypanosoma vivax", "Trypanosoma congolense",
        "Leptomonas pyrrhocoris")],
    (("Dictyostelium discoideum",), "Entamoeba dispar"),
    (("Dictyostelium discoideum",), "Entamoeba invadens"),
    (("Naegleria gruberi",), "Giardia intestinalis"),
    (("Naegleria gruberi",), "Spironucleus salmonicida"),
    (("Thalassiosira pseudonana",), "Phytophthora infestans"),
    (("Thalassiosira pseudonana",), "Saprolegnia parasitica"),
    (("Thalassiosira pseudonana",), "Blastocystis hominis"),
    (("Nematostella vectensis",), "Thelohanellus kitauei"),
    (("Nematostella vectensis",), "Henneguya salminicola"),
    (("Caenorhabditis elegans",), "Brugia malayi"),
    (("Caenorhabditis elegans",), "Trichinella spiralis"),
    (_FLATWORM_PROXY, "Schistosoma mansoni"),
    (("Auxenochlorella protothecoides", "Chlamydomonas reinhardtii"), "Helicosporidium sp. ATCC 50920"),
    # controls
    (("Neurospora crassa",), "Aspergillus nidulans"),
    (("Coprinopsis cinerea",), "Schizophyllum commune"),
    (("Thalassiosira pseudonana",), "Phaeodactylum tricornutum"),
    (("Nematostella vectensis",), "Hydra vulgaris"),
    (("Salpingoeca rosetta",), "Capsaspora owczarzaki"),
    (("Chlamydomonas reinhardtii",), "Chlorella variabilis"),
    (("Ostreococcus lucimarinus",), "Ostreococcus tauri"),
    (("Cyanidioschyzon merolae",), "Galdieria sulphuraria"),
]

PAIR_SPECS += [
    *[(("Neurospora crassa", "Aspergillus nidulans"), sp) for sp in ("Blumeria graminis", "Pyricularia oryzae")],
    *[(("Coprinopsis cinerea", "Schizophyllum commune"), sp) for sp in ("Puccinia graminis",)],
    *[(("Spizellomyces punctatus",), sp) for sp in (
        "Mitosporidium daphniae", "Edhazardia aedis", "Anncaliia algerae", "Nosema bombycis", "Pseudoloma neurophilia")],
    *[(("Thalassiosira pseudonana",), sp) for sp in (
        "Phytophthora sojae", "Aphanomyces astaci")],
    *[(("Bodo saltans",), sp) for sp in (
        "Angomonas deanei", "Strigomonas culicis", "Trypanosoma grayi",
        "Leishmania braziliensis", "Leishmania mexicana")],
    *[(_APICOMPLEXAN_PROXY, sp) for sp in (
        "Gregarina niphandrodes", "Besnoitia besnoiti", "Plasmodium yoelii", "Plasmodium malariae")],
    *[(("Caenorhabditis elegans",), sp) for sp in (
        "Haemonchus contortus", "Strongyloides ratti")],
    *[(_FLATWORM_PROXY, sp) for sp in (
        "Echinococcus multilocularis", "Fasciola hepatica", "Clonorchis sinensis",
        "Schistosoma japonicum")],
    *[(("Naegleria gruberi",), sp) for sp in ("Trichomonas vaginalis", "Tritrichomonas foetus")],
    (("Drosophila melanogaster", "Anopheles gambiae"), "Pediculus humanus"),
    # controls
    (("Coprinopsis cinerea",), "Laccaria bicolor"),
    (("Tetrahymena thermophila",), "Paramecium tetraurelia"),
    (("Caenorhabditis elegans",), "Caenorhabditis briggsae"),
    (("Caenorhabditis elegans",), "Pristionchus pacificus"),
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
