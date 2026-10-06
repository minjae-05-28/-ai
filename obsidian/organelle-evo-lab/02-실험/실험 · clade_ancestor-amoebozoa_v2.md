---
유형: 실험
실행: clade_ancestor/amoebozoa_v2
산출: results/clade_ancestor/amoebozoa_v2/summary.json
tags:
  - 유형/실험
  - 실험/clade_ancestor-amoebozoa_v2
---

# 실험 · clade_ancestor-amoebozoa_v2

**산출물** `results/clade_ancestor/amoebozoa_v2/summary.json`

## 한눈에

| 항목 | 값 |
| --- | --- |
| clade | amoebozoa_v2 |
| tips | 40 |
| clade_tips | 12 |
| families_considered | 5771 |
| node_reconstructed | most recent common ancestor of the sampled clade tips, which at this sample size is not the clade's root (see results/sample_size/summary.json) |
| n_models | 5 |
| n_bootstrap_trees | 20 |
| completeness_model | True |
| n_completeness_markers | 150 |
| n_confident_families | 2045 |
| n_uncertain_families | 1619 |
| size_not_reported | the simulation showed a 16-17% underestimate of ancestor size at this sample size, so no family count is quoted |

## clade_species

```json
[
 "Acanthamoeba castellanii (strain ATCC 30010 / Neff)",
 "Planoprotostelium fungivorum",
 "Heterostelium pallidum (strain ATCC 26659 / Pp 5 / PN500) (Cellular slime mold) (Polysphondylium pallidum)",
 "Cavenderia fasciculata (Slime mold) (Dictyostelium fasciculatum)",
 "Polysphondylium violaceum",
 "Tieghemostelium lacteum (Slime mold) (Dictyostelium lacteum)",
 "Dictyostelium purpureum (Slime mold)",
 "Dictyostelium discoideum (Social amoeba)",
 "Dictyostelium firmibasis",
 "Entamoeba invadens IP1",
 "Entamoeba dispar (strain ATCC PRA-260 / SAW760)",
 "Entamoeba nuttalli"
]
```

## dropped_tips

```json
[]
```

## reduced_lineages

```json
[
 "Entamoeba invadens IP1",
 "Entamoeba dispar (strain ATCC PRA-260 / SAW760)",
 "Entamoeba nuttalli"
]
```

## leave_tips_out_auroc

```json
{
 "reconstruction": 0.9262,
 "clade_frequency": 0.912
}
```

## tip_completeness

```json
{
 "Acanthamoeba castellanii (strain ATCC 30010 / Neff)": 1.0,
 "Planoprotostelium fungivorum": 1.0,
 "Heterostelium pallidum (strain ATCC 26659 / Pp 5 / PN500) (Cellular slime mold) (Polysphondylium pallidum)": 0.953,
 "Cavenderia fasciculata (Slime mold) (Dictyostelium fasciculatum)": 0.987,
 "Polysphondylium violaceum": 0.98,
 "Tieghemostelium lacteum (Slime mold) (Dictyostelium lacteum)": 0.96,
 "Dictyostelium purpureum (Slime mold)": 0.98,
 "Dictyostelium discoideum (Social amoeba)": 1.0,
 "Dictyostelium firmibasis": 0.973,
 "Entamoeba invadens IP1": 0.427,
 "Entamoeba dispar (strain ATCC PRA-260 / SAW760)": 0.5,
 "Entamoeba nuttalli": 0.507
}
```

## functions_of_confident_families

```json
[
 [
  "catalytic activity",
  359
 ],
 [
  "organelle",
  162
 ],
 [
  "transferase activity",
  117
 ],
 [
  "hydrolase activity",
  96
 ],
 [
  "helicase_nucleic",
  92
 ],
 [
  "structural molecule activity",
  65
 ],
 [
  "protease",
  65
 ],
 [
  "repeat_domain",
  62
 ],
 [
  "DNA binding",
  58
 ],
 [
  "methyl_glyco_transferase",
  57
 ],
 [
  "ribosome",
  57
 ],
 [
  "kinase",
  54
 ],
 [
  "catalytic activity, acting on RNA",
  52
 ],
 [
  "oxidoreductase activity",
  51
 ],
 [
  "nucleus",
  49
 ],
 [
  "catalytic activity, acting on a protein",
  47
 ],
 [
  "RNA binding",
  46
 ],
 [
  "zinc_finger",
  42
 ],
 [
  "transporter_channel",
  38
 ],
 [
  "uncharacterised",
  38
 ]
]
```

## top_families

```json
[
 {
  "family": "MMM1",
  "description": "Maintenance of mitochondrial morphology protein 1",
  "posterior": 1.0,
  "model_sd": 0.0,
  "tree_sd": 0.002,
  "share_of_clade_tips_today": 1.0
 },
 {
  "family": "Ribonuc_L-PSP",
  "description": "Endoribonuclease L-PSP",
  "posterior": 1.0,
  "model_sd": 0.0,
  "tree_sd": 0.002,
  "share_of_clade_tips_today": 1.0
 },
 {
  "family": "WH2",
  "description": "WH2 motif",
  "posterior": 1.0,
  "model_sd": 0.0,
  "tree_sd": 0.002,
  "share_of_clade_tips_today": 1.0
 },
 {
  "family": "FMN_red",
  "description": "NADPH-dependent FMN reductase",
  "posterior": 1.0,
  "model_sd": 0.0,
  "tree_sd": 0.002,
  "share_of_clade_tips_today": 1.0
 },
 {
  "family": "N_BRCA1_IG",
  "description": "Ig-like domain from next to BRCA1 gene",
  "posterior": 1.0,
  "model_sd": 0.0,
  "tree_sd": 0.002,
  "share_of_clade_tips_today": 1.0
 },
 {
  "family": "AAA_2",
  "description": "AAA domain (Cdc48 subfamily)",
  "posterior": 1.0,
  "model_sd": 0.0,
  "tree_sd": 0.0,
  "share_of_clade_tips_today": 1.0
 },
 {
  "family": "zf-RING_UBOX",
  "description": "RING-type zinc-finger",
  "posterior": 1.0,
  "model_sd": 0.0,
  "tree_sd": 0.0,
  "share_of_clade_tips_today": 1.0
 },
 {
  "family": "AAA",
  "description": "ATPase family associated with various cellular activities (AAA)",
  "posterior": 1.0,
  "model_sd": 0.0,
  "tree_sd": 0.0,
  "share_of_clade_tips_today": 1.0
 },
 {
  "family": "KOW",
  "description": "KOW motif",
  "posterior": 1.0,
  "model_sd": 0.0,
  "tree_sd": 0.0,
  "share_of_clade_tips_today": 1.0
 },
 {
  "family": "TAP42",
  "descripti
… (잘림 — 원본 파일 참조)
```

## uncertain_families

```json
[
 {
  "family": "ZnF_RZ-type",
  "description": "RZ type zinc finger domain",
  "posterior": 0.94,
  "model_sd": 0.001,
  "tree_sd": 0.248
 },
 {
  "family": "TFIID_NTD2",
  "description": "WD40 associated region in TFIID subunit, NTD2 domain",
  "posterior": 0.94,
  "model_sd": 0.001,
  "tree_sd": 0.248
 },
 {
  "family": "TM2",
  "description": "TM2 domain",
  "posterior": 0.94,
  "model_sd": 0.001,
  "tree_sd": 0.248
 },
 {
  "family": "THOC2_N",
  "description": "THO complex subunit 2 N-terminus",
  "posterior": 0.94,
  "model_sd": 0.001,
  "tree_sd": 0.248
 },
 {
  "family": "GPR180-TMEM145_TM",
  "description": "GPR180/TMEM145, transmembrane domain",
  "posterior": 0.94,
  "model_sd": 0.001,
  "tree_sd": 0.248
 },
 {
  "family": "GLE1",
  "description": "GLE1-like protein",
  "posterior": 0.94,
  "model_sd": 0.001,
  "tree_sd": 0.248
 },
 {
  "family": "Fy-3",
  "description": "Ferry endosomal RAB5 effector complex subunit 3",
  "posterior": 0.94,
  "model_sd": 0.001,
  "tree_sd": 0.248
 },
 {
  "family": "BTG",
  "description": "BTG family",
  "posterior": 0.94,
  "model_sd": 0.001,
  "tree_sd": 0.248
 },
 {
  "family": "Med27",
  "description": "Mediator complex subunit 27",
  "posterior": 0.94,
  "model_sd": 0.001,
  "tree_sd": 0.248
 },
 {
  "family": "BRAP2",
  "description": "BRCA1-associated protein 2",
  "posterior": 0.94,
  "model_sd": 0.001,
  "tree_sd": 0.248
 },
 {
  "family": "BRCA-2_helical",
  "description": "BRCA2, helical",
  "posterior": 0.94,
  "model_sd": 0.001,
  "tree_sd": 0.248
 },
 {
  "family": "GET4",
  "description": "Golgi to ER traffic pr
… (잘림 — 원본 파일 참조)
```

## 연결
- [[실험 목록]]
