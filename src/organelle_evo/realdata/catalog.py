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
            # --- expansion (October 2026): more independent lineages per supergroup ---
            # jakobids, malawimonads, excavates
            "Seculamonas ecuadoriensis", "Histiona aroides", "Malawimonas jakobiformis", "Naegleria gruberi",
            # green lineage
            "Ostreococcus tauri", "Micromonas commoda", "Chlorokybus atmophyticus", "Chara vulgaris",
            "Mesostigma viride", "Pycnococcus provasolii", "Zea mays", "Oryza sativa", "Nicotiana tabacum",
            "Cycas taitungensis", "Ginkgo biloba", "Selaginella moellendorffii", "Huperzia squarrosa",
            # red algae, cryptophytes, haptophytes, stramenopiles, alveolates
            "Porphyra purpurea", "Gracilaria vermiculophylla", "Cyanophora paradoxa", "Rhodomonas salina",
            "Emiliania huxleyi", "Ectocarpus siliculosus", "Phaeodactylum tricornutum", "Saprolegnia ferax",
            "Babesia bovis", "Theileria parva", "Eimeria tenella",  # Chromera and Toxoplasma: no complete annotated mtDNA
            # amoebozoa, fungi
            "Polysphondylium pallidum", "Rhizopus oryzae", "Yarrowia lipolytica",
            "Candida albicans", "Aspergillus nidulans", "Podospora anserina",
            # animals
            "Amphimedon queenslandica", "Schistosoma mansoni", "Ascaris suum",
            "Apis mellifera", "Anopheles gambiae", "Daphnia pulex", "Strongylocentrotus purpuratus",
            "Branchiostoma floridae", "Ciona intestinalis", "Xenopus laevis",
        ],  # fmt: skip
        # Search hits for its ~6 kb genome (3 proteins) are unannotated; use the RefSeq record.
        # "accession:" entries are fetched directly.
        "extra_queries": {"Plasmodium falciparum": "accession:NC_037526.1",
                          "Nematostella vectensis": "accession:NC_008164.1"},
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
            # --- expansion (October 2026) ---
            # green algae and early land plants
            "Ostreococcus tauri", "Micromonas commoda", "Chlorella vulgaris", "Chara vulgaris",
            "Chaetosphaeridium globosum", "Zygnema circumcarinatum", "Anthoceros angustus",
            "Selaginella moellendorffii", "Huperzia lucidula", "Ginkgo biloba", "Pinus thunbergii", "Zea mays",
            # heterotrophic and parasitic plants / algae: graded plastid reduction
            "Cuscuta reflexa", "Cuscuta gronovii", "Orobanche gracilis", "Conopholis americana",
            "Neottia nidus-avis", "Rhizanthella gardneri", "Euglena longa", "Helicosporidium sp. ex Simulium jonesi",
            "Prototheca wickerhamii",
            # red lineage, secondary and tertiary plastids
            "Gracilaria tenuistipitata", "Cyanidium caldarium", "Galdieria sulphuraria", "Ectocarpus siliculosus",
            "Vaucheria litorea", "Heterosigma akashiwo", "Rhodomonas salina", "Bigelowiella natans",
            "Chromera velia", "Eimeria tenella", "Theileria parva", "Babesia bovis",
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
            # Recent, still gene-rich. Its record names ~7% of genes; the rest are named
            # by homology to E. coli (realdata/homology.py).
            "Sodalis glossinidius",
            "Hamiltonella defensa",
            "Serratia symbiotica",
            "Wigglesworthia glossinidia",
            "Blochmannia pennsylvanicus",
            "Baumannia cicadellinicola",
            "Riesia pediculicola",
            "Buchnera aphidicola str. APS (Acyrthosiphon pisum)",
            # --- expansion (October 2026): more gammaproteobacterial symbionts, from
            # facultative (gene-rich) to the smallest bacterial genomes known ---
            "Arsenophonus nasoniae", "Candidatus Regiella insecticola",
            "Candidatus Ishikawaella capsulata", "Candidatus Portiera aleyrodidarum",
            "Candidatus Carsonella ruddii", "Candidatus Annandia pinicola", "Candidatus Purcelliella pentastirinorum",
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
                ("Blochmannia vafer", "Blochmannia", "vafer"),
                ("Buchnera aphidicola (Uroleucon)", "Buchnera aphidicola", "Uroleucon"),
                ("Buchnera aphidicola (Myzus persicae)", "Buchnera aphidicola", "Myzus"),
                ("Riesia pediculischaeffi", "Riesia", "pediculischaeffi"),
            ]
        } | {
            "Buchnera aphidicola (Cinara cedri)": "accession:NC_008513.1",  # 416 kb, among the smallest Buchnera
            "Candidatus Westeberhardia cardiocondylae": "accession:LN774881.1",
        },
    },
}
