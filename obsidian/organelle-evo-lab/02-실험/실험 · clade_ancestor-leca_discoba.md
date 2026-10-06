---
유형: 실험
실행: clade_ancestor/leca_discoba
산출: results/clade_ancestor/leca_discoba/summary.json
tags:
  - 유형/실험
  - 실험/clade_ancestor-leca_discoba
---

# 실험 · clade_ancestor-leca_discoba

**산출물** `results/clade_ancestor/leca_discoba/summary.json`

## 한눈에

| 항목 | 값 |
| --- | --- |
| clade | leca_discoba |
| tips | 256 |
| clade_tips | 256 |
| families_considered | 14869 |
| rooted_on | split: Discoba | rest |
| node_reconstructed | most recent common ancestor of the sampled clade tips, which at this sample size is not the clade's root (see results/sample_size/summary.json) |
| n_models | 5 |
| n_bootstrap_trees | 6 |
| completeness_model | True |
| reduced_branch_multiplier | False |
| n_confident_families | 2949 |
| n_uncertain_families | 903 |
| size_not_reported | the simulation showed a 16-17% underestimate of ancestor size at this sample size, so no family count is quoted |

## clade_species

```json
[
 "Nematocida ausubeli (Nematode killer fungus)",
 "Nematocida displodere",
 "Encephalitozoon hellem (Microsporidian parasite)",
 "Encephalitozoon cuniculi (strain GB-M1) (Microsporidian parasite)",
 "Encephalitozoon intestinalis (strain ATCC 50506) (Microsporidian parasite) (Septata intestinalis)",
 "Anaeramoeba ignava (Anaerobic marine amoeba)",
 "Thecamonas trahens ATCC 50062",
 "Paratrimastix pyriformis",
 "Acanthamoeba castellanii (strain ATCC 30010 / Neff)",
 "Planoprotostelium fungivorum",
 "Heterostelium pallidum (strain ATCC 26659 / Pp 5 / PN500) (Cellular slime mold) (Polysphondylium pallidum)",
 "Cavenderia fasciculata (Slime mold) (Dictyostelium fasciculatum)",
 "Tieghemostelium lacteum (Slime mold) (Dictyostelium lacteum)",
 "Polysphondylium violaceum",
 "Dictyostelium purpureum (Slime mold)",
 "Dictyostelium discoideum (Social amoeba)",
 "Dictyostelium firmibasis",
 "Capsaspora owczarzaki (strain ATCC 30864)",
 "Mnemiopsis leidyi (Sea walnut) (Warty comb jellyfish)",
 "Caenorhabditis elegans",
 "Xylocopa violacea (Violet carpenter bee) (Apis violacea)",
 "Cimex lectularius (Bed bug) (Acanthia lectularia)",
 "Spodoptera frugiperda (Fall armyworm)",
 "Spodoptera litura (Asian cotton leafworm)",
 "Aedes aegypti (Yellowfever mosquito) (Culex aegypti)",
 "Drosophila lebanonensis (Fruit fly) (Scaptodrosophila lebanonensis)",
 "Drosophila rhopaloa (Fruit fly)",
 "Drosophila kikkawai (Fruit fly)",
 "Drosophila suzukii (Spotted-wing drosophila fruit fly)",
 "Drosophila mauritiana (Fruit fly)",
 "Drosophila melanogaster (Fruit fly)",
 "Drosophila ananassae (Fruit fly)"
… (잘림 — 원본 파일 참조)
```

## dropped_tips

```json
[
 "Gossypium darwinii (Darwins cotton) (Gossypium barbadense var. darwinii)",
 "Geodia barretti (Barretts horny sponge)",
 "Equus przewalskii (Przewalskis horse) (Equus caballus przewalskii)"
]
```

## reduced_lineages

```json
[
 "Nematocida ausubeli (Nematode killer fungus)",
 "Nematocida displodere",
 "Encephalitozoon hellem (Microsporidian parasite)",
 "Encephalitozoon cuniculi (strain GB-M1) (Microsporidian parasite)",
 "Encephalitozoon intestinalis (strain ATCC 50506) (Microsporidian parasite) (Septata intestinalis)",
 "Blastocystis hominis",
 "Cryptosporidium meleagridis",
 "Cryptosporidium ubiquitum",
 "Cryptosporidium andersoni",
 "Cryptosporidium muris (strain RN66)",
 "Plasmodium malariae",
 "Plasmodium gonderi",
 "Plasmodium knowlesi (strain H)",
 "Plasmodium falciparum (isolate 3D7)",
 "Plasmodium reichenowi",
 "Plasmodium berghei (strain Anka)",
 "Plasmodium chabaudi chabaudi",
 "Strigomonas culicis",
 "Trypanosoma equiperdum"
]
```

## misplaced_clade_tips_left_out

```json
[]
```

## root_split_intruders

```json
[]
```

## non_clade_tips_inside_clade_node

```json
[]
```

## leave_tips_out_auroc

```json
{
 "reconstruction": 0.9818,
 "clade_frequency": 0.9329
}
```

## tip_completeness

```json
{
 "Nematocida ausubeli (Nematode killer fungus)": 0.34,
 "Nematocida displodere": 0.367,
 "Encephalitozoon hellem (Microsporidian parasite)": 0.347,
 "Encephalitozoon cuniculi (strain GB-M1) (Microsporidian parasite)": 0.353,
 "Encephalitozoon intestinalis (strain ATCC 50506) (Microsporidian parasite) (Septata intestinalis)": 0.347,
 "Anaeramoeba ignava (Anaerobic marine amoeba)": 0.787,
 "Thecamonas trahens ATCC 50062": 0.967,
 "Paratrimastix pyriformis": 0.753,
 "Acanthamoeba castellanii (strain ATCC 30010 / Neff)": 0.967,
 "Planoprotostelium fungivorum": 0.987,
 "Heterostelium pallidum (strain ATCC 26659 / Pp 5 / PN500) (Cellular slime mold) (Polysphondylium pallidum)": 0.98,
 "Cavenderia fasciculata (Slime mold) (Dictyostelium fasciculatum)": 0.98,
 "Tieghemostelium lacteum (Slime mold) (Dictyostelium lacteum)": 0.98,
 "Polysphondylium violaceum": 0.98,
 "Dictyostelium purpureum (Slime mold)": 0.973,
 "Dictyostelium discoideum (Social amoeba)": 0.98,
 "Dictyostelium firmibasis": 0.98,
 "Capsaspora owczarzaki (strain ATCC 30864)": 0.98,
 "Mnemiopsis leidyi (Sea walnut) (Warty comb jellyfish)": 1.0,
 "Caenorhabditis elegans": 1.0,
 "Xylocopa violacea (Violet carpenter bee) (Apis violacea)": 1.0,
 "Cimex lectularius (Bed bug) (Acanthia lectularia)": 1.0,
 "Spodoptera frugiperda (Fall armyworm)": 1.0,
 "Spodoptera litura (Asian cotton leafworm)": 1.0,
 "Aedes aegypti (Yellowfever mosquito) (Culex aegypti)": 1.0,
 "Drosophila lebanonensis (Fruit fly) (Scaptodrosophila lebanonensis)": 1.0,
 "Drosophila rhopaloa (Fruit fly)": 1.0,
 "Drosophila kikkawai (Fruit fly)": 1.0,
 "Dr
… (잘림 — 원본 파일 참조)
```

## completeness_markers_per_group

```json
{
 "clade": 150
}
```

## groups_without_a_completeness_score

```json
[
 "outgroup"
]
```

## functions_of_confident_families

```json
[
 [
  "catalytic activity",
  453
 ],
 [
  "organelle",
  223
 ],
 [
  "transferase activity",
  149
 ],
 [
  "hydrolase activity",
  119
 ],
 [
  "helicase_nucleic",
  117
 ],
 [
  "repeat_domain",
  101
 ],
 [
  "protease",
  85
 ],
 [
  "nucleus",
  78
 ],
 [
  "methyl_glyco_transferase",
  73
 ],
 [
  "oxidoreductase activity",
  72
 ],
 [
  "structural molecule activity",
  72
 ],
 [
  "uncharacterised",
  70
 ],
 [
  "kinase",
  67
 ],
 [
  "zinc_finger",
  66
 ],
 [
  "DNA binding",
  65
 ],
 [
  "catalytic activity, acting on RNA",
  62
 ],
 [
  "ribosome",
  61
 ],
 [
  "catalytic activity, acting on a protein",
  58
 ],
 [
  "transporter_channel",
  57
 ],
 [
  "RNA binding",
  54
 ]
]
```

## top_families

```json
[
 {
  "family": "LNS2",
  "description": "LNS2 (Lipin/Ned1/Smp2)",
  "posterior": 1.0,
  "model_sd": 0.0,
  "tree_sd": 0.0,
  "share_of_clade_tips_today": 0.922
 },
 {
  "family": "DUF2428",
  "description": "THADA/TRM732, DUF2428",
  "posterior": 1.0,
  "model_sd": 0.0,
  "tree_sd": 0.0,
  "share_of_clade_tips_today": 0.871
 },
 {
  "family": "Zn_ribbon_CSL",
  "description": "CSL zinc finger",
  "posterior": 1.0,
  "model_sd": 0.0,
  "tree_sd": 0.0,
  "share_of_clade_tips_today": 0.926
 },
 {
  "family": "SLIDE",
  "description": "SLIDE",
  "posterior": 1.0,
  "model_sd": 0.0,
  "tree_sd": 0.0,
  "share_of_clade_tips_today": 0.93
 },
 {
  "family": "Clp_N",
  "description": "Clp repeat (R) N-terminal domain",
  "posterior": 1.0,
  "model_sd": 0.0,
  "tree_sd": 0.0,
  "share_of_clade_tips_today": 0.742
 },
 {
  "family": "MCM5_C",
  "description": "MCM5, C-terminal domain",
  "posterior": 1.0,
  "model_sd": 0.0,
  "tree_sd": 0.0,
  "share_of_clade_tips_today": 0.906
 },
 {
  "family": "ATG9",
  "description": "Autophagy protein ATG9",
  "posterior": 1.0,
  "model_sd": 0.0,
  "tree_sd": 0.0,
  "share_of_clade_tips_today": 0.852
 },
 {
  "family": "GCS",
  "description": "Glutamate-cysteine ligase",
  "posterior": 1.0,
  "model_sd": 0.0,
  "tree_sd": 0.0,
  "share_of_clade_tips_today": 0.797
 },
 {
  "family": "PDEase_I",
  "description": "3'5'-cyclic nucleotide phosphodiesterase",
  "posterior": 1.0,
  "model_sd": 0.0,
  "tree_sd": 0.0,
  "share_of_clade_tips_today": 0.871
 },
 {
  "family": "ELO",
  "description": "GNS1/SUR4 family",
  "posterior": 1.0,
  "model_sd": 0.0,
… (잘림 — 원본 파일 참조)
```

## uncertain_families

```json
[
 {
  "family": "IG_AIR9",
  "description": "AIR9 A9 domain",
  "posterior": 1.0,
  "model_sd": 0.0,
  "tree_sd": 0.355
 },
 {
  "family": "FERM_N",
  "description": "FERM N-terminal domain",
  "posterior": 1.0,
  "model_sd": 0.0,
  "tree_sd": 0.425
 },
 {
  "family": "DIL",
  "description": "DIL domain",
  "posterior": 1.0,
  "model_sd": 0.0,
  "tree_sd": 0.331
 },
 {
  "family": "TAP_C",
  "description": "TAP C-terminal domain",
  "posterior": 1.0,
  "model_sd": 0.0,
  "tree_sd": 0.318
 },
 {
  "family": "IQGAP_helical",
  "description": "IQGAP, helical domain",
  "posterior": 1.0,
  "model_sd": 0.0,
  "tree_sd": 0.3
 },
 {
  "family": "CFAP61_dimer",
  "description": "CFAP61 dimerisation domain",
  "posterior": 0.999,
  "model_sd": 0.0,
  "tree_sd": 0.199
 },
 {
  "family": "Piwi",
  "description": "Piwi domain",
  "posterior": 0.999,
  "model_sd": 0.0,
  "tree_sd": 0.218
 },
 {
  "family": "PAZ",
  "description": "PAZ domain",
  "posterior": 0.999,
  "model_sd": 0.0,
  "tree_sd": 0.225
 },
 {
  "family": "COMMD1_N",
  "description": "COMMD1 N-terminal domain",
  "posterior": 0.998,
  "model_sd": 0.0,
  "tree_sd": 0.249
 },
 {
  "family": "Keratin_assoc",
  "description": "Keratinocyte-associated protein 2",
  "posterior": 0.998,
  "model_sd": 0.0,
  "tree_sd": 0.152
 },
 {
  "family": "FNIP_C",
  "description": "Folliculin-interacting protein C-terminus",
  "posterior": 0.998,
  "model_sd": 0.0,
  "tree_sd": 0.287
 },
 {
  "family": "DUF4615",
  "description": "Domain of unknown function (DUF4615)",
  "posterior": 0.998,
  "model_sd": 0.0,
  "tree_sd": 0.314
 },
 {
  "
… (잘림 — 원본 파일 참조)
```

## clade_node_children

```json
[
 {
  "n_clade_tips": 24,
  "examples": [
   "Acrasis kona",
   "Bodo saltans (Flagellated protozoan)",
   "Leishmania braziliensis",
   "Leishmania enriettii",
   "Leishmania lindenbergi",
   "Leishmania martiniquensis"
  ],
  "n_confident": 3164,
  "sum_of_posteriors": 3871.5
 },
 {
  "n_clade_tips": 232,
  "examples": [
   "Absidia repens",
   "Acanthamoeba castellanii (strain ATCC 30010 / Neff)",
   "Achlya hypogyna (Oomycete) (Protoachlya hypogyna)",
   "Acropora cervicornis (Staghorn coral)",
   "Actinia tenebrosa (Australian red waratah sea anemone)",
   "Aedes aegypti (Yellowfever mosquito) (Culex aegypti)"
  ],
  "n_confident": 3242,
  "sum_of_posteriors": 3915.4
 }
]
```

## 연결
- [[실험 목록]]
