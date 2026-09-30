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
            "Thalassiosira pseudonana", "Tetrahymena thermophila",
            # amoebozoa
            "Dictyostelium discoideum", "Acanthamoeba castellanii",
            # fungi
            "Allomyces macrogynus", "Neurospora crassa", "Schizosaccharomyces pombe",
            "Saccharomyces cerevisiae",
            # animals and relatives
            "Monosiga brevicollis", "Trichoplax adhaerens", "Metridium senile",
            "Drosophila melanogaster", "Caenorhabditis elegans", "Danio rerio",
            "Gallus gallus", "Mus musculus", "Homo sapiens",
        ],  # fmt: skip
        # Search hits for its ~6 kb genome (3 proteins) are unannotated; use the RefSeq record.
        # "accession:" entries are fetched directly.
        "extra_queries": {"Plasmodium falciparum": "accession:NC_037526.1"},
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
            "Epifagus virginiana", "Toxoplasma gondii",
        ],  # fmt: skip
        # A second, independent primary endosymbiosis (~100 Myr old).
        "extra_queries": {
            "Plasmodium falciparum": "accession:NC_036769.1",  # apicoplast
            "Paulinella chromatophora": '"Paulinella chromatophora"[Organism] AND chromatophore[Title] AND complete[Title]',
        },
    },
    "insect_endosymbiont": {
        "query": BACTERIA_QUERY,
        # Free-living relative used as the proxy ancestor / gene universe.
        "ancestor": "Escherichia coli str. K-12 substr. MG1655",
        "species": [
            # Sodalis glossinidius (a recent symbiont) would fit here, but its only complete
            # record names ~7% of genes, which would read as massive false gene loss.
            "Hamiltonella defensa",
            "Serratia symbiotica",
            "Wigglesworthia glossinidia",
            "Blochmannia pennsylvanicus",
            "Baumannia cicadellinicola",
            "Riesia pediculicola",
            "Buchnera aphidicola str. APS (Acyrthosiphon pisum)",
        ],
        # Strains that are not separate taxa, and Candidatus names that NCBI lists
        # under renamed genera: search by the host in the title instead.
        "extra_queries": {
            name: f'"{org}"[All Fields] AND {host}[Title] AND complete genome[Title] NOT plasmid[Title]'
            for name, org, host in [
                ("Blochmannia floridanus", "Blochmannia", "floridanus"),
                ("Buchnera aphidicola Sg (Schizaphis graminum)", "Buchnera aphidicola", "Schizaphis"),
                ("Buchnera aphidicola Bp (Baizongia pistaciae)", "Buchnera aphidicola", "Baizongia"),
                ("Buchnera aphidicola (Cinara)", "Buchnera aphidicola", "Cinara"),
                ("Moranella endobia", "Moranella", "endobia"),
            ]
        },
    },
}
