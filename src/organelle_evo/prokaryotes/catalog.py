"""Bacteria and archaea for environment laws (cold, salt, no oxygen, radiation, starvation).

Each pair is (ordinary close relative, extremophile). The pair's design is the change in
environment from the relative to the extremophile, so a pair can also move *away* from an
extreme (e.g. a methanogen proxy for aerobic haloarchaea). Environment values are each
organism's optimum or typical habitat, from the literature, and are approximate:

    temp      optimal growth temperature, deg C
    nacl      optimal NaCl, % w/v
    aerobic   1 respires oxygen (including facultative), 0 anaerobe
    radiation 1 exceptional radiation/desiccation resistance
    oligo     1 adapted to nutrient-poor habitats (streamlined oligotroph)
"""

from typing import NamedTuple


class Env(NamedTuple):
    group: str
    temp: float
    nacl: float
    aerobic: int
    radiation: int = 0
    oligo: int = 0


SPECIES = {
    # Gammaproteobacteria
    "Shewanella oneidensis": Env("gamma", 30, 1, 1),
    "Shewanella frigidimarina": Env("gamma", 20, 3, 1),
    "Colwellia psychrerythraea": Env("gamma", 8, 3, 1),  # Arctic sediment, psychrophile
    "Acinetobacter baylyi": Env("gamma", 30, 0.5, 1),
    "Psychrobacter arcticus": Env("gamma", 22, 2, 1),  # Siberian permafrost, grows to -10 C
    "Pseudomonas aeruginosa": Env("gamma", 37, 0.5, 1),
    "Pseudomonas putida": Env("gamma", 30, 0.5, 1),
    # Firmicutes
    "Bacillus subtilis": Env("firmicutes", 37, 0.5, 1),
    "Bacillus licheniformis": Env("firmicutes", 40, 0.5, 1),
    "Planococcus halocryophilus": Env("firmicutes", 25, 5, 1),  # permafrost, grows to -15 C in brine
    "Geobacillus kaustophilus": Env("firmicutes", 60, 0.5, 1),
    "Lactiplantibacillus plantarum": Env("firmicutes", 30, 0.5, 0),  # aerotolerant fermenter
    # Bacteroidetes
    "Flavobacterium johnsoniae": Env("bacteroidetes", 30, 0.5, 1),
    "Psychroflexus torquis": Env("bacteroidetes", 12, 4, 1),  # Antarctic sea ice
    "Rhodothermus marinus": Env("bacteroidetes", 65, 2, 1),
    "Salinibacter ruber": Env("bacteroidetes", 40, 25, 1),  # crystallizer ponds
    # Deinococcus-Thermus and Actinobacteria
    "Thermus thermophilus": Env("deinococcus", 70, 0.5, 1),
    "Deinococcus radiodurans": Env("deinococcus", 30, 0.5, 1, radiation=1),
    "Micrococcus luteus": Env("actino", 30, 1, 1),
    "Kineococcus radiotolerans": Env("actino", 28, 0.5, 1, radiation=1),
    # Cyanobacteria
    "Synechocystis sp. PCC 6803": Env("cyano", 30, 0.5, 1),
    "Chroococcidiopsis thermalis": Env("cyano", 30, 0.5, 1, radiation=1),  # desert/Mars-analog lineage
    "Synechococcus elongatus": Env("cyano", 30, 0, 1),
    "Prochlorococcus marinus": Env("cyano", 24, 3.5, 1, oligo=1),  # open ocean, streamlined
    # Alphaproteobacteria
    "Cereibacter sphaeroides": Env("alpha", 30, 0.5, 1),  # formerly Rhodobacter sphaeroides
    "Candidatus Pelagibacter ubique": Env("alpha", 20, 3.5, 1, oligo=1),  # SAR11
    # Deltaproteobacteria / Desulfobacterota and Myxococcota
    "Nitratidesulfovibrio vulgaris": Env("delta", 37, 0.5, 0),  # formerly Desulfovibrio vulgaris
    "Desulfotalea psychrophila": Env("delta", 10, 3, 0),  # Arctic sediment
    "Myxococcus xanthus": Env("delta", 30, 0.5, 1),
    "Geobacter sulfurreducens": Env("delta", 30, 0.5, 0),
    # Archaea
    "Methanosarcina acetivorans": Env("archaea", 37, 2, 0),
    "Methanococcoides burtonii": Env("archaea", 23, 2, 0),  # Antarctic lake
    "Halobacterium salinarum": Env("archaea", 42, 25, 1, radiation=1),
    "Haloferax volcanii": Env("archaea", 42, 15, 1),
    "Methanococcus maripaludis": Env("archaea", 37, 2, 0),
    "Methanocaldococcus jannaschii": Env("archaea", 85, 3, 0),
}

# Round 2: at least five pairs per environment axis.
SPECIES.update({
    # cold
    "Vibrio natriegens": Env("gamma", 37, 2, 1),
    "Photobacterium profundum": Env("gamma", 15, 3, 1),  # deep-sea, piezophile
    "Alteromonas macleodii": Env("gamma", 30, 3, 1),
    "Pseudoalteromonas haloplanktis": Env("gamma", 15, 3, 1),  # Antarctic seawater
    # salt
    "Halomonas elongata": Env("gamma", 30, 10, 1),
    "Chromohalobacter salexigens": Env("gamma", 37, 10, 1),
    "Halobacillus halophilus": Env("firmicutes", 35, 10, 1),
    "Haloarcula marismortui": Env("archaea", 40, 20, 1),  # Dead Sea
    "Natronomonas pharaonis": Env("archaea", 45, 20, 1),  # soda lakes
    # no oxygen
    "Clostridium acetobutylicum": Env("firmicutes", 37, 0.5, 0),
    "Geobacter metallireducens": Env("delta", 30, 0.5, 0),
    "Desulfuromonas acetoxidans": Env("delta", 30, 2, 0),
    # radiation
    "Deinococcus geothermalis": Env("deinococcus", 50, 0.5, 1, radiation=1),
    "Deinococcus deserti": Env("deinococcus", 30, 0.5, 1, radiation=1),  # Sahara
    "Truepera radiovictrix": Env("deinococcus", 50, 1, 1, radiation=1),
    "Rubrobacter xylanophilus": Env("actino", 60, 0.5, 1, radiation=1),
    "Hymenobacter swuensis": Env("bacteroidetes", 25, 0.5, 1, radiation=1),
    "Methylorubrum extorquens": Env("alpha", 30, 0.5, 1),
    "Methylobacterium radiotolerans": Env("alpha", 30, 0.5, 1, radiation=1),
    "Thermococcus kodakarensis": Env("archaea", 85, 3, 0),
    "Thermococcus gammatolerans": Env("archaea", 88, 3, 0, radiation=1),  # survives 30 kGy
    # nutrient-poor
    "Sphingobium japonicum": Env("alpha", 30, 0.5, 1),
    "Sphingopyxis alaskensis": Env("alpha", 22, 3, 1, oligo=1),
    "Nitrososphaera viennensis": Env("archaea", 42, 0.5, 1),  # soil ammonia oxidiser
    "Nitrosopumilus maritimus": Env("archaea", 28, 3.5, 1, oligo=1),  # ocean ammonia oxidiser
    "Synechococcus sp. WH 8102": Env("cyano", 25, 3.5, 1, oligo=1),  # open ocean
    "Cupriavidus necator": Env("beta", 30, 0.5, 1),
    "Polynucleobacter asymbioticus": Env("beta", 25, 0, 1, oligo=1),  # streamlined freshwater
    # control
    "Bacillus pumilus": Env("firmicutes", 37, 0.5, 1),
})

# Climate-sensitive pathogens: forecast targets only (not in any pair, so no law is fitted
# on them).
CLIMATE_TARGETS = {
    "Vibrio vulnificus": Env("gamma", 37, 2, 1),  # warming coastal seas
    "Vibrio parahaemolyticus": Env("gamma", 37, 3, 1),
    "Vibrio cholerae": Env("gamma", 37, 1, 1),
    "Legionella pneumophila": Env("gamma", 37, 0.5, 1),  # warm water systems
    "Burkholderia pseudomallei": Env("beta", 37, 0.5, 1),  # melioidosis
}
SPECIES.update(CLIMATE_TARGETS)

# (relative candidates, closest first; extremophile)
PAIR_SPECS = [
    (("Shewanella oneidensis",), "Shewanella frigidimarina"),
    (("Shewanella oneidensis",), "Colwellia psychrerythraea"),
    (("Acinetobacter baylyi",), "Psychrobacter arcticus"),
    (("Bacillus subtilis",), "Planococcus halocryophilus"),
    (("Bacillus subtilis",), "Geobacillus kaustophilus"),
    (("Bacillus subtilis",), "Lactiplantibacillus plantarum"),
    (("Flavobacterium johnsoniae",), "Psychroflexus torquis"),
    (("Rhodothermus marinus",), "Salinibacter ruber"),
    (("Thermus thermophilus",), "Deinococcus radiodurans"),
    (("Micrococcus luteus",), "Kineococcus radiotolerans"),
    (("Synechocystis sp. PCC 6803",), "Chroococcidiopsis thermalis"),
    (("Synechococcus elongatus",), "Prochlorococcus marinus"),
    (("Cereibacter sphaeroides",), "Candidatus Pelagibacter ubique"),
    (("Nitratidesulfovibrio vulgaris",), "Desulfotalea psychrophila"),
    (("Myxococcus xanthus",), "Geobacter sulfurreducens"),
    (("Methanosarcina acetivorans",), "Methanococcoides burtonii"),
    (("Methanosarcina acetivorans",), "Halobacterium salinarum"),
    (("Methanosarcina acetivorans",), "Haloferax volcanii"),
    (("Methanococcus maripaludis",), "Methanocaldococcus jannaschii"),
    # controls (little or no change in environment)
    (("Bacillus subtilis",), "Bacillus licheniformis"),
    (("Pseudomonas aeruginosa",), "Pseudomonas putida"),
]

PAIR_SPECS += [
    (("Vibrio natriegens",), "Photobacterium profundum"),
    (("Alteromonas macleodii",), "Pseudoalteromonas haloplanktis"),
    (("Pseudomonas aeruginosa",), "Halomonas elongata"),
    (("Pseudomonas aeruginosa",), "Chromohalobacter salexigens"),
    (("Bacillus subtilis",), "Halobacillus halophilus"),
    (("Methanosarcina acetivorans",), "Haloarcula marismortui"),
    (("Methanosarcina acetivorans",), "Natronomonas pharaonis"),
    (("Bacillus subtilis",), "Clostridium acetobutylicum"),
    (("Myxococcus xanthus",), "Geobacter metallireducens"),
    (("Myxococcus xanthus",), "Desulfuromonas acetoxidans"),
    (("Thermus thermophilus",), "Deinococcus geothermalis"),
    (("Thermus thermophilus",), "Deinococcus deserti"),
    (("Thermus thermophilus",), "Truepera radiovictrix"),
    (("Micrococcus luteus",), "Rubrobacter xylanophilus"),
    (("Flavobacterium johnsoniae",), "Hymenobacter swuensis"),
    (("Methylorubrum extorquens",), "Methylobacterium radiotolerans"),
    (("Thermococcus kodakarensis",), "Thermococcus gammatolerans"),
    (("Sphingobium japonicum",), "Sphingopyxis alaskensis"),
    (("Nitrososphaera viennensis",), "Nitrosopumilus maritimus"),
    (("Synechococcus elongatus",), "Synechococcus sp. WH 8102"),
    (("Cupriavidus necator",), "Polynucleobacter asymbioticus"),
    (("Bacillus subtilis",), "Bacillus pumilus"),
]

AXES = ("colder", "saltier", "anaerobic", "radiation_resistant", "oligotrophic")
TEMP_SCALE, NACL_SCALE = 30.0, 10.0


def env_change(proxy: Env, desc: Env) -> tuple[float, ...]:
    """(1, colder, saltier, anaerobic, radiation, oligo) for a move from proxy to desc."""
    return (1.0, (proxy.temp - desc.temp) / TEMP_SCALE, (desc.nacl - proxy.nacl) / NACL_SCALE,
            float(proxy.aerobic - desc.aerobic), float(desc.radiation - proxy.radiation),
            float(desc.oligo - proxy.oligo))


def design(proxy: str, desc: str) -> tuple[float, ...]:
    return env_change(SPECIES[proxy], SPECIES[desc])


def resolve_pairs(available) -> list[tuple[str, str]]:
    out = []
    for proxies, desc in PAIR_SPECS:
        if desc not in available:
            continue
        proxy = next((p for p in proxies if p in available and p != desc), None)
        if proxy is not None:
            out.append((proxy, desc))
    return out


# A habitable niche on Mars as an environment: subsurface perchlorate brine near 0 C,
# no free oxygen, high ionising radiation, very little organic carbon.
MARS = Env("mars", temp=0, nacl=20, aerobic=0, radiation=1, oligo=1)


def slug(name: str) -> str:
    import re

    return re.sub(r"[^A-Za-z0-9]+", "_", name).strip("_")
