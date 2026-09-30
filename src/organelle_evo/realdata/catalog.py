"""Species chosen to span each endosymbiotic system, from gene-rich to extremely reduced.

Queries go to NCBI nuccore. `{org}` is substituted with the organism name.
"""

MITO_QUERY = (
    '"{org}"[Organism] AND mitochondrion[filter] AND refseq[filter] '
    "AND (complete genome[Title] OR complete sequence[Title])"
)
PLASTID_QUERY = (
    '"{org}"[Organism] AND plastid[filter] AND refseq[filter] '
    "AND (complete genome[Title] OR complete sequence[Title])"
)
BACTERIA_QUERY = '"{org}"[Organism] AND refseq[filter] AND complete genome[Title] NOT plasmid[Title]'

CATALOG = {
    "mitochondrion": {
        "query": MITO_QUERY,
        "ancestor": None,  # gene universe = union over lineages
        "species": [
            # jakobids: the most bacteria-like mitochondrial genomes known
            "Reclinomonas americana", "Andalucia godoyi", "Jakoba libera",
            # plants and green algae
            "Marchantia polymorpha", "Physcomitrium patens", "Arabidopsis thaliana",
            "Nephroselmis olivacea", "Prototheca wickerhamii", "Chlamydomonas reinhardtii",
            # red algae, stramenopiles, alveolates
            "Chondrus crispus", "Cyanidioschyzon merolae", "Phytophthora infestans",
            "Thalassiosira pseudonana", "Tetrahymena thermophila", "Plasmodium falciparum",
            # amoebozoa
            "Dictyostelium discoideum", "Acanthamoeba castellanii",
            # fungi
            "Allomyces macrogynus", "Neurospora crassa", "Schizosaccharomyces pombe",
            "Saccharomyces cerevisiae",
            # animals and relatives
            "Monosiga brevicollis", "Trichoplax adhaerens", "Nematostella vectensis",
            "Drosophila melanogaster", "Caenorhabditis elegans", "Danio rerio",
            "Gallus gallus", "Mus musculus", "Homo sapiens",
        ],  # fmt: skip
    },
    "plastid": {
        "query": PLASTID_QUERY,
        "ancestor": None,
        "species": [
            # glaucophyte and red lineage: the most gene-rich plastids
            "Cyanophora paradoxa", "Porphyra purpurea", "Cyanidioschyzon merolae",
            "Guillardia theta", "Thalassiosira pseudonana", "Phaeodactylum tricornutum",
            "Emiliania huxleyi",
            # green lineage
            "Mesostigma viride", "Nephroselmis olivacea", "Chlamydomonas reinhardtii",
            "Marchantia polymorpha", "Physcomitrium patens", "Amborella trichopoda",
            "Oryza sativa", "Nicotiana tabacum", "Arabidopsis thaliana", "Euglena gracilis",
            # non-photosynthetic plastids: parasitic plant, apicomplexans
            "Epifagus virginiana", "Toxoplasma gondii", "Plasmodium falciparum",
        ],  # fmt: skip
        # A second, independent primary endosymbiosis (~100 Myr old).
        "extra_queries": {
            "Paulinella chromatophora": '"Paulinella chromatophora"[Organism] AND chromatophore[Title] AND complete[Title]',
        },
    },
    "insect_endosymbiont": {
        "query": BACTERIA_QUERY,
        # Free-living relative used as the proxy ancestor / gene universe.
        "ancestor": "Escherichia coli str. K-12 substr. MG1655",
        "species": [
            "Sodalis glossinidius",  # recent, still gene-rich
            "Hamiltonella defensa",
            "Serratia symbiotica",
            "Wigglesworthia glossinidia",
            "Blochmannia floridanus",
            "Blochmannia pennsylvanicus",
            "Baumannia cicadellinicola",
            "Riesia pediculicola",
            "Buchnera aphidicola str. APS (Acyrthosiphon pisum)",
            "Buchnera aphidicola str. Sg (Schizaphis graminum)",
            "Buchnera aphidicola str. Bp (Baizongia pistaciae)",
            "Buchnera aphidicola BCc",
            "Moranella endobia",
        ],
    },
}
