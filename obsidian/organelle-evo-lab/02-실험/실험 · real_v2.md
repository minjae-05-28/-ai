---
유형: 실험
실행: real_v2
산출: results/real_v2/metrics.json
tags:
  - 유형/실험
  - 실험/real_v2
---

# 실험 · real_v2

**산출물** `results/real_v2/metrics.json`

## mitochondrion

```json
{
 "n_genomes": 75,
 "genes_added_by_homology": {
  "Acanthamoeba castellanii": 1,
  "Allomyces macrogynus": 2,
  "Amphimedon queenslandica": 0,
  "Andalucia godoyi": 0,
  "Anopheles gambiae": 0,
  "Apis mellifera": 0,
  "Arabidopsis thaliana": 1,
  "Ascaris suum": 0,
  "Aspergillus nidulans FGSC A4": 9,
  "Babesia bovis T2Bo": 0,
  "Branchiostoma floridae": 0,
  "Caenorhabditis elegans": 0,
  "Candida albicans": 1,
  "Chara vulgaris": 2,
  "Chlamydomonas reinhardtii": 0,
  "Chlorokybus atmophyticus": 2,
  "Chondrus crispus": 0,
  "Ciona intestinalis B CG-2006": 0,
  "Cyanidioschyzon merolae": 4,
  "Cyanophora paradoxa": 1,
  "Cycas taitungensis": 0,
  "Danio rerio": 0,
  "Daphnia pulex": 0,
  "Dictyostelium discoideum": 3,
  "Drosophila melanogaster": 0,
  "Ectocarpus siliculosus": 0,
  "Eimeria tenella": 0,
  "Emiliania huxleyi": 0,
  "Gallus gallus": 0,
  "Ginkgo biloba": 0,
  "Gracilaria vermiculophylla": 4,
  "Histiona aroides": 0,
  "Homo sapiens": 0,
  "Phlegmariurus squarrosus": 0,
  "Jakoba libera": 0,
  "Malawimonas jakobiformis": 0,
  "Marchantia polymorpha subsp. ruderalis": 1,
  "Mesostigma viride": 0,
  "Metridium senile": 0,
  "Micromonas commoda": 1,
  "Monosiga brevicollis": 0,
  "Mus musculus": 0,
  "Naegleria gruberi": 0,
  "Nematostella sp. JVK-2006": 0,
  "Nephroselmis olivacea": 2,
  "Neurospora crassa OR74A": 1,
  "Nicotiana tabacum": 7,
  "Oryza sativa": 4,
  "Ostreococcus tauri": 2,
  "Phaeodactylum tricornutum": 2,
  "Physcomitrium patens": 1,
  "Phytophthora infestans": 0,
  "Plasmodium falciparum": 0,
  "Podospora anserina": 3,
  "Heterostelium pallidum": 1,
  "Porphyra purpurea": 0,
  "Prototheca wickerhamii": 3,
  "Pycnococcus provasolii": 0,
  "Reclinomonas americana": 0,
  "Rhizopus arrhizus": 2,
  "Rhodomonas salina": 2,
  "Saccharomyces cerevisiae S288C": 1,
  "Saprolegnia ferax": 0,
  "Schistosoma mansoni": 0,
  "Schizosaccharomyces pombe": 1,
  "Seculamonas ecuadoriensis": 0,
  "Selaginella moellendorffii": 0,
  "Strongylocentrotus purpuratus": 0,
  "Tetrahymena thermophila": 1,
  "Thalassiosira pseudonana": 1,
  "Theileria parva": 0,
  "Trichoplax adhaerens": 1,
  "Xenopus laevis": 0,
  "Yarrowia lipolytica": 4,
  "Zea mays subsp. parviglumis": 1
 },
 "n_genes": 80,
 "law": {
  "hydrophobicity_gravy": {
   "weight": -0.2477779597271006,
   "se": 0.06801712764837119
  },
  "tm_helices": {
   "weight": -0.3384846191873112,
   "se": 0.08603023805355747
  },
  "protein_length": {
   "weight": -0.15799380537329447,
   "se": 0.03583796795836201
  },
  "redox_core": {
   "weight": -2.2397787446234947,
   "se": 0.1800555549397924
  },
  "atp_synthase": {
   "weight": -1.9254760193801765,
   "se": 0.18730236333538397
  },
  "translation": {
   "weight": -1.5548625696171203,
   "se": 0.19439706286464947
  },
  "transcription": {
   "weight": 0.3275547222356097,
   "se": 0.22120481447892812
  },
  "protein_targeting": {
   "weight": 0.11976287608774241,
   "se": 0.17784842991142907
  }
 },
 "lolo_auroc": {
  "law_features_only": 0.872667089552455,
  "gene_prevalence": 0.9457380734312791,
  "law_plus_prevalence": 0.9320868751225928
 }
}
```

## plastid

```json
{
 "n_genomes": 54,
 "genes_added_by_homology": {
  "Amborella trichopoda": 3,
  "Anthoceros angustus": 1,
  "Arabidopsis thaliana": 0,
  "Babesia bovis T2Bo": 14,
  "Bigelowiella natans": 0,
  "Chaetosphaeridium globosum": 0,
  "Chara vulgaris": 1,
  "Chlamydomonas reinhardtii": 1,
  "Chlorella vulgaris": 2,
  "Chromera velia": 0,
  "Conopholis americana": 0,
  "Cuscuta gronovii": 0,
  "Cuscuta reflexa": 0,
  "Cyanidioschyzon merolae strain 10D": 5,
  "Cyanidium caldarium": 2,
  "Cyanophora paradoxa": 4,
  "Ectocarpus siliculosus": 2,
  "Eimeria tenella": 0,
  "Emiliania huxleyi": 3,
  "Epifagus virginiana": 1,
  "Euglena gracilis": 0,
  "Euglena longa": 1,
  "Galdieria sulphuraria": 2,
  "Ginkgo biloba": 0,
  "Gracilaria tenuistipitata var. liui": 3,
  "Guillardia theta": 2,
  "Helicosporidium sp. ex Simulium jonesi": 0,
  "Heterosigma akashiwo": 2,
  "Huperzia lucidula": 0,
  "Marchantia polymorpha": 3,
  "Mesostigma viride": 0,
  "Micromonas commoda": 31,
  "Neottia nidus-avis": 0,
  "Nephroselmis olivacea": 0,
  "Nicotiana tabacum": 0,
  "Orobanche gracilis": 0,
  "Oryza sativa Japonica Group": 1,
  "Ostreococcus tauri": 0,
  "Paulinella chromatophora": 31,
  "Phaeodactylum tricornutum": 0,
  "Physcomitrium patens": 1,
  "Pinus thunbergii": 2,
  "Plasmodium falciparum 3D7": 2,
  "Porphyra purpurea": 18,
  "Prototheca wickerhamii": 0,
  "Rhizanthella gardneri": 0,
  "Rhodomonas salina": 5,
  "Selaginella moellendorffii": 1,
  "Thalassiosira pseudonana": 0,
  "Theileria parva strain Muguga": 1,
  "Toxoplasma gondii RH": 0,
  "Vaucheria litorea": 4,
  "Zea mays": 0,
  "Zygnema circumcarinatum": 0
 },
 "n_genes": 276,
 "law": {
  "hydrophobicity_gravy": {
   "weight": -0.014197318726414105,
   "se": 0.025076364712515543
  },
  "tm_helices": {
   "weight": -0.0057634363274628,
   "se": 0.02817873257321653
  },
  "protein_length": {
   "weight": -0.11164828908536151,
   "se": 0.02321204510414229
  },
  "redox_core": {
   "weight": -1.355772890591134,
   "se": 0.09310342654931084
  },
  "atp_synthase": {
   "weight": -1.6735981564377227,
   "se": 0.144829317780884
  },
  "translation": {
   "weight": -1.4786618321896716,
   "se": 0.04764838038741482
  },
  "transcription": {
   "weight": -1.8083128812622042,
   "se": 0.13251352999118984
  },
  "protein_targeting": {
   "weight": -0.6935638848137268,
   "se": 0.11417363983653203
  }
 },
 "lolo_auroc": {
  "law_features_only": 0.7840077523372281,
  "gene_prevalence": 0.9130412888363468,
  "law_plus_prevalence": 0.8916008537692987
 }
}
```

## insect_endosymbiont

```json
{
 "n_genomes": 25,
 "genes_added_by_homology": {
  "Arsenophonus nasoniae": 497,
  "Candidatus Palibaumannia cicadellinicola": 111,
  "Candidatus Blochmanniella floridana": 91,
  "Candidatus Blochmanniella pennsylvanica": 112,
  "Candidatus Blochmanniella vafra str. BVAF": 56,
  "Buchnera aphidicola str. Bp (Baizongia pistaciae)": 80,
  "Buchnera aphidicola (Cinara tujafilina)": 48,
  "Buchnera aphidicola BCc": 76,
  "Buchnera aphidicola (Myzus persicae)": 131,
  "Buchnera aphidicola (Schizaphis graminum)": 130,
  "Buchnera aphidicola (Uroleucon sonchi)": 122,
  "Buchnera aphidicola str. APS (Acyrthosiphon pisum)": 125,
  "Candidatus Annandia pinicola": 75,
  "Candidatus Carsonella ruddii": 51,
  "Candidatus Ishikawaella capsulata Mpkobe": 117,
  "Candidatus Portiera aleyrodidarum": 48,
  "Candidatus Purcelliella pentastirinorum": 103,
  "Candidatus Westeberhardia cardiocondylae": 4,
  "Candidatus Hamiltonella defensa (Bemisia tabaci)": 237,
  "Candidatus Moranella endobia PCIT": 101,
  "Candidatus Riesia pediculicola": 133,
  "Candidatus Riesia pediculischaeffi": 333,
  "Serratia symbiotica": 472,
  "Sodalis glossinidius str. 'morsitans'": 1439,
  "Wigglesworthia glossinidia endosymbiont of Glossina morsitans morsitans (Yale colony)": 71
 },
 "n_genes": 4277,
 "law": {
  "hydrophobicity_gravy": {
   "weight": -0.015053232267041881,
   "se": 0.006309993464297241
  },
  "tm_helices": {
   "weight": 0.16888656530476984,
   "se": 0.007958239536166634
  },
  "protein_length": {
   "weight": -0.12517208007859074,
   "se": 0.005787381852711644
  },
  "redox_core": {
   "weight": -2.0510965853413547,
   "se": 0.20821117628604466
  },
  "atp_synthase": {
   "weight": -1.8285855140498166,
   "se": 0.24671664989983136
  },
  "translation": {
   "weight": -2.7682091252021364,
   "se": 0.22077501950024878
  },
  "transcription": {
   "weight": -1.2944304473039303,
   "se": 0.06266022417633235
  },
  "protein_targeting": {
   "weight": -0.7730734668897684,
   "se": 0.03550674945311249
  }
 },
 "lolo_auroc": {
  "law_features_only": 0.6596591636146854,
  "gene_prevalence": 0.9652449872298233,
  "law_plus_prevalence": 0.9566041654845664
 }
}
```

## universality

```json
{
 "systems": [
  "mitochondrion",
  "plastid",
  "insect_endosymbiont"
 ],
 "delta_aic_shared_minus_separate": 1860.9368890570477,
 "shared_weights": {
  "hydrophobicity_gravy": -0.012581503292057246,
  "tm_helices": 0.13898822807060454,
  "protein_length": -0.134795836457965,
  "redox_core": -2.0047441129587362,
  "atp_synthase": -1.9597684634906127,
  "translation": -1.4632890558000844,
  "transcription": -1.0170026829754986,
  "protein_targeting": -0.7635682918103782
 }
}
```

## 연결
- [[실험 목록]]
