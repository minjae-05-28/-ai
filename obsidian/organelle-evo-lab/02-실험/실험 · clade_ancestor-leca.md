---
유형: 실험
실행: clade_ancestor/leca
산출: results/clade_ancestor/leca/summary.json
tags:
  - 유형/실험
  - 실험/clade_ancestor-leca
---

# 실험 · clade_ancestor-leca

**산출물** `results/clade_ancestor/leca/summary.json`

## 한눈에

| 항목 | 값 |
| --- | --- |
| clade | leca |
| tips | 256 |
| clade_tips | 256 |
| families_considered | 14828 |
| rooted_on | split: Discoba | rest / split: Opisthokonta | rest |
| n_bootstrap_trees | 5 |
| n_confident_families | 3048 |
| n_uncertain_families | 452 |
| n_robust_absent | 9512 |
| rule | present = posterior >= 0.9 under every root; absent = < 0.1 under every root; root-dependent = >= 0.9 under one root and < 0.1 or far lower under another (spread >= 0.5) |

## roots

```json
[
 "discoba",
 "opisthokonta"
]
```

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

## root_split_intruders

```json
{
 "discoba": [],
 "opisthokonta": []
}
```

## misplaced_clade_tips_left_out

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

## leave_tips_out_auroc_per_root

```json
{
 "discoba": {
  "reconstruction": 0.9818,
  "clade_frequency": 0.9329
 },
 "opisthokonta": {
  "reconstruction": 0.9828,
  "clade_frequency": 0.9141
 }
}
```

## sum_of_posteriors_per_root

```json
{
 "discoba": 3893.1,
 "opisthokonta": 4409.1
}
```

## n_present_per_root

```json
{
 "discoba": 3193,
 "opisthokonta": 3767
}
```

## functions_of_confident_families

```json
[
 [
  "catalytic activity",
  449
 ],
 [
  "organelle",
  235
 ],
 [
  "transferase activity",
  148
 ],
 [
  "helicase_nucleic",
  116
 ],
 [
  "hydrolase activity",
  115
 ],
 [
  "repeat_domain",
  113
 ],
 [
  "protease",
  88
 ],
 [
  "nucleus",
  86
 ],
 [
  "oxidoreductase activity",
  74
 ],
 [
  "methyl_glyco_transferase",
  74
 ],
 [
  "uncharacterised",
  72
 ],
 [
  "structural molecule activity",
  70
 ],
 [
  "zinc_finger",
  67
 ],
 [
  "DNA binding",
  63
 ],
 [
  "kinase",
  62
 ],
 [
  "transporter_channel",
  62
 ],
 [
  "catalytic activity, acting on RNA",
  62
 ],
 [
  "ribosome",
  59
 ],
 [
  "catalytic activity, acting on a protein",
  58
 ],
 [
  "cytoskeleton_motor",
  55
 ]
]
```

## functions_of_root_dependent_families

```json
[
 [
  "catalytic activity",
  75
 ],
 [
  "uncharacterised",
  27
 ],
 [
  "organelle",
  25
 ],
 [
  "transferase activity",
  23
 ],
 [
  "helicase_nucleic",
  17
 ],
 [
  "oxidoreductase activity",
  16
 ],
 [
  "hydrolase activity",
  14
 ],
 [
  "lyase activity",
  11
 ],
 [
  "kinase",
  11
 ],
 [
  "amino acid metabolic process",
  11
 ],
 [
  "carbohydrate derivative metabolic process",
  10
 ],
 [
  "repeat_domain",
  10
 ],
 [
  "methyl_glyco_transferase",
  10
 ],
 [
  "nucleobase-containing small molecule metabolic process",
  9
 ],
 [
  "nucleus",
  9
 ],
 [
  "transporter activity",
  8
 ],
 [
  "carbohydrate metabolic process",
  8
 ],
 [
  "DNA binding",
  8
 ],
 [
  "cytoskeleton_motor",
  7
 ],
 [
  "protease",
  7
 ]
]
```

## top_families

```json
[
 {
  "family": "LNS2",
  "description": "LNS2 (Lipin/Ned1/Smp2)",
  "posterior_discoba": 1.0,
  "posterior_opisthokonta": 1.0,
  "share_of_tips_today": 0.922
 },
 {
  "family": "SLIDE",
  "description": "SLIDE",
  "posterior_discoba": 1.0,
  "posterior_opisthokonta": 1.0,
  "share_of_tips_today": 0.93
 },
 {
  "family": "DUF2428",
  "description": "THADA/TRM732, DUF2428",
  "posterior_discoba": 1.0,
  "posterior_opisthokonta": 1.0,
  "share_of_tips_today": 0.871
 },
 {
  "family": "Zn_ribbon_CSL",
  "description": "CSL zinc finger",
  "posterior_discoba": 1.0,
  "posterior_opisthokonta": 1.0,
  "share_of_tips_today": 0.926
 },
 {
  "family": "MCM5_C",
  "description": "MCM5, C-terminal domain",
  "posterior_discoba": 1.0,
  "posterior_opisthokonta": 1.0,
  "share_of_tips_today": 0.906
 },
 {
  "family": "GCS",
  "description": "Glutamate-cysteine ligase",
  "posterior_discoba": 1.0,
  "posterior_opisthokonta": 1.0,
  "share_of_tips_today": 0.797
 },
 {
  "family": "PDEase_I",
  "description": "3'5'-cyclic nucleotide phosphodiesterase",
  "posterior_discoba": 1.0,
  "posterior_opisthokonta": 1.0,
  "share_of_tips_today": 0.871
 },
 {
  "family": "ELO",
  "description": "GNS1/SUR4 family",
  "posterior_discoba": 1.0,
  "posterior_opisthokonta": 1.0,
  "share_of_tips_today": 0.891
 },
 {
  "family": "ATG9",
  "description": "Autophagy protein ATG9",
  "posterior_discoba": 1.0,
  "posterior_opisthokonta": 1.0,
  "share_of_tips_today": 0.852
 },
 {
  "family": "Dopey_N",
  "description": "Dopey, N-terminal",
  "posterior_discoba": 1.0,
  "posterior_opisthokonta": 1.0,
  "share
… (잘림 — 원본 파일 참조)
```

## root_dependent_families

```json
[
 {
  "family": "Neurochondrin",
  "description": "Neurochondrin",
  "posterior_discoba": 0.498,
  "posterior_opisthokonta": 0.999,
  "share_of_tips_today": 0.559
 },
 {
  "family": "Citrate_synth_N",
  "description": "ATP-citrate synthase ATP-grasp domain",
  "posterior_discoba": 0.484,
  "posterior_opisthokonta": 0.998,
  "share_of_tips_today": 0.672
 },
 {
  "family": "MoeA_N",
  "description": "MoeA N-terminal region (domain I and II)",
  "posterior_discoba": 0.482,
  "posterior_opisthokonta": 1.0,
  "share_of_tips_today": 0.727
 },
 {
  "family": "NmrA",
  "description": "NmrA-like family",
  "posterior_discoba": 0.485,
  "posterior_opisthokonta": 0.991,
  "share_of_tips_today": 0.691
 },
 {
  "family": "DUF908",
  "description": "Domain of Unknown Function (DUF908)",
  "posterior_discoba": 0.483,
  "posterior_opisthokonta": 0.992,
  "share_of_tips_today": 0.645
 },
 {
  "family": "Gemin7",
  "description": "Gem-associated protein 7 (Gemin7)",
  "posterior_discoba": 0.472,
  "posterior_opisthokonta": 0.995,
  "share_of_tips_today": 0.246
 },
 {
  "family": "GNC1_N",
  "description": "Stalled ribosome sensor GCN1 N-terminal",
  "posterior_discoba": 0.467,
  "posterior_opisthokonta": 0.999,
  "share_of_tips_today": 0.605
 },
 {
  "family": "WHD_GTF3C1",
  "description": "GTF3C1, extended winged-helix domain",
  "posterior_discoba": 0.465,
  "posterior_opisthokonta": 0.996,
  "share_of_tips_today": 0.445
 },
 {
  "family": "AhpC-TSA_2",
  "description": "AhpC/TSA antioxidant enzyme",
  "posterior_discoba": 0.468,
  "posterior_opisthokonta": 0.991,
  "share_of_tips_today"
… (잘림 — 원본 파일 참조)
```

## 연결
- [[실험 목록]]
