"""Independent origins of two lifestyle transitions, as curated pairs of collected UniProt proteomes.

Each origin: the lineage that made the transition and its closest relatives in the collected data
that did not. Relatives were picked from NCBI taxonomy and the phylogenetic literature, not from the
gene content (that would be circular). Organism strings are exactly as UniProt names them.

Anaerobic: lineages whose mitochondrion became a hydrogenosome or mitosome (anaerobic lifestyle).
Many are also parasites, so two origins are matched for parasitism (both sides parasitic, only the
mitochondrion differs) and a separate set of aerobic parasite pairs measures what parasitism alone
removes.

Multicellular: independent origins of multicellularity against unicellular relatives, and
unicellular-unicellular pairs at a comparable distance for the background rate of gene gain.
"""

ANAEROBIC = {
    # Anaerobiosis is thought to go back to the base of Metamonada, so the aerobic relatives are in
    # another supergroup (Discoba): the comparison spans a deep split, and its losses include
    # whatever separates the supergroups, not only oxygen.
    "Metamonada": {
        "anaerobes": ["Carpediemonas membranifera", "Kipferlia bialata", "Aduncisulcus paluster",
                      "Paratrimastix pyriformis", "Hexamita inflata", "Giardia muris", "Spironucleus salmonicida",
                      "Tritrichomonas foetus", "Blattamonas nauphoetae"],
        "relatives": ["Naegleria gruberi (Amoeba)", "Bodo saltans (Flagellated protozoan)"],
        "parasitism_matched": False, "free_living_anaerobes": True},
    "Archamoebae (Entamoeba)": {
        "anaerobes": ["Entamoeba dispar (strain ATCC PRA-260 / SAW760)", "Entamoeba invadens IP1",
                      "Entamoeba nuttalli"],
        "relatives": ["Acanthamoeba castellanii (strain ATCC 30010 / Neff)", "Dictyostelium discoideum (Social amoeba)",
                      "Planoprotostelium fungivorum"],
        "parasitism_matched": False, "free_living_anaerobes": False},
    # Anaerobic gut fungi of herbivores: symbionts, not parasites.
    "Neocallimastigomycota": {
        "anaerobes": ["Piromyces finnis", "Anaeromyces robustus"],
        "relatives": ["Spizellomyces punctatus (strain DAOM BR117)", "Rhizoclosmatium globosum",
                      "Gonapodya prolifera (strain JEL478) (Monoblepharis prolifera)"],
        "parasitism_matched": False, "free_living_anaerobes": True},
    # Both sides are intracellular parasites; Rozella and Mitosporidium keep a mitochondrion.
    "Microsporidia": {
        "anaerobes": ["Encephalitozoon cuniculi (strain GB-M1) (Microsporidian parasite)",
                      "Nematocida parisii (strain ERTm3) (Nematode killer fungus)",
                      "Vairimorpha ceranae (Microsporidian parasite) (Nosema ceranae)",
                      "Nosema bombycis (strain CQ1 / CVCC 102059) (Microsporidian parasite) (Pebrine of silkworm)"],
        "relatives": ["Rozella allomycis (strain CSF55)", "Mitosporidium daphniae"],
        "parasitism_matched": True, "free_living_anaerobes": False},
    # Both sides are apicomplexan parasites; Eimeria and Plasmodium keep a respiring mitochondrion.
    "Cryptosporidium": {
        "anaerobes": ["Cryptosporidium muris (strain RN66)", "Cryptosporidium andersoni"],
        "relatives": ["Eimeria tenella (Coccidian parasite)", "Plasmodium falciparum (isolate 3D7)"],
        "parasitism_matched": True, "free_living_anaerobes": False},
    "Blastocystis": {
        "anaerobes": ["Blastocystis hominis", "Blastocystis sp. subtype 1 (strain ATCC 50177 / NandII)"],
        "relatives": ["Hondaea fermentalgiana", "Saprolegnia diclina (strain VS20)"],
        "parasitism_matched": False, "free_living_anaerobes": False},
}

# Parasitism without loss of aerobic respiration: what being a parasite removes by itself.
AEROBIC_PARASITES = {
    "Trypanosomatida": {"derived": ["Leishmania major", "Trypanosoma rangeli"],
                        "relatives": ["Bodo saltans (Flagellated protozoan)"]},
    "Haemosporida + Piroplasmida": {"derived": ["Plasmodium falciparum (isolate 3D7)", "Babesia bovis",
                                                "Theileria parva (East coast fever infection agent)"],
                                    "relatives": ["Vitrella brassicaformis"]},
    "Pneumocystis": {"derived": ["Pneumocystis jirovecii (strain RU7) (Human pneumocystis pneumonia agent)",
                                 "Pneumocystis carinii (strain B80) (Rat pneumocystis pneumonia agent) (Pneumocystis carinii f. sp. carinii)"],
                     "relatives": ["Schizosaccharomyces japonicus (strain yFS275 / FY16936) (Fission yeast)",
                                   "Schizosaccharomyces octosporus (strain yFS286) (Fission yeast) (Octosporomyces octosporus)"]},
}

MULTICELLULAR = {
    "Volvocales": {"derived": ["Volvox carteri f. nagariensis", "Pleodorina starrii", "Gonium pectorale (Green alga)"],
                   "relatives": ["Chlamydomonas reinhardtii (Chlamydomonas smithii)", "Chlamydomonas incerta",
                                 "Chlamydomonas schloesseri"]},
    "Metazoa": {"derived": ["Amphimedon queenslandica (Sponge)", "Trichoplax adhaerens (Trichoplax reptans)",
                            "Nematostella vectensis (Starlet sea anemone)"],
                "relatives": ["Salpingoeca rosetta (Choanoflagellate)", "Monosiga brevicollis (Choanoflagellate)",
                              "Capsaspora owczarzaki (strain ATCC 30864)"]},
    # Aggregative multicellularity (fruiting bodies), a different kind from the clonal ones.
    "Dictyostelia": {"derived": ["Dictyostelium discoideum (Social amoeba)", "Dictyostelium purpureum (Slime mold)",
                                 "Polysphondylium violaceum"],
                     "relatives": ["Acanthamoeba castellanii (strain ATCC 30010 / Neff)", "Planoprotostelium fungivorum"]},
    "Phaeophyceae": {"derived": ["Ectocarpus siliculosus (Brown alga) (Conferva siliculosa)"],
                     "relatives": ["Aureococcus anophagefferens (Harmful bloom alga)", "Nannochloropsis gaditana"]},
    "Rhodophyta (Bangiophyceae + Florideophyceae)": {
        "derived": ["Chondrus crispus (Carrageen Irish moss) (Polymorpha crispa)", "Gracilariopsis chorda",
                    "Pyropia yezoensis (Susabi-nori) (Porphyra yezoensis)", "Porphyra umbilicalis (Purple laver) (Red alga)"],
        "relatives": ["Porphyridium purpureum (Red alga) (Porphyridium cruentum)", "Galdieria sulphuraria (Red alga)",
                      "Cyanidioschyzon merolae (strain NIES-3377 / 10D) (Unicellular red alga)"]},
}

# Unicellular-unicellular pairs at a comparable depth: the background rate at which a lineage
# carries a family its relative lacks, with no change in organisation.
UNICELLULAR_CONTROLS = {
    "Trebouxiophyceae": (["Chlorella sorokiniana (Freshwater green alga)"], ["Coccomyxa subellipsoidea (strain C-169) (Green microalga)"]),
    "Mamiellales": (["Ostreococcus tauri (Marine green alga)"], ["Micromonas commoda (Picoplanktonic green alga)"]),
    "Diatoms": (["Phaeodactylum tricornutum (strain CCAP 1055/1)"], ["Thalassiosira pseudonana (Marine diatom) (Cyclotella nana)"]),
    "Chytrids": (["Spizellomyces punctatus (strain DAOM BR117)"], ["Rhizoclosmatium globosum"]),
    "Holozoan protists": (["Sphaeroforma arctica JP610"], ["Capsaspora owczarzaki (strain ATCC 30864)"]),
}

# Families with an expectation from outside this data.
PANELS = {
    "anaerobic": {
        "respiratory chain (expected LOST)": ["Complex1_51K", "Complex1_30kDa", "COX15-CtaA", "COX4", "COX17",
                                              "Cytochrom_C1", "UCR_14kD", "UCR_hinge", "Rieske", "SDH_C"],
        "TCA cycle (expected mostly lost)": ["Citrate_synt", "SDH_beta"],
        "ATP synthase (expected lost in mitosomes)": ["ATP-synt_D", "ATP-synt_DE", "ATP-synt_C"],
        "anaerobic energy metabolism (expected GAINED/kept)": ["Fe_hyd_lg_C", "Fe_hyd_SSU", "POR_N", "PFOR_II",
                                                               "ADH_Fe_C", "Rubredoxin", "Hemerythrin"],
        "Fe-S cluster assembly (expected KEPT: the one job mitosomes still do)": ["NifU", "NifU_N", "Frataxin_Cyay"],
    },
    "multicellular": {
        "cell adhesion / extracellular matrix": ["Cadherin", "Integrin_beta", "Integrin_alpha", "Laminin_G_1",
                                                 "Collagen", "fn3", "EGF"],
        "developmental transcription factors": ["Homeobox_KN"],
    },
}
