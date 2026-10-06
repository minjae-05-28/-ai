---
유형: 실험
실행: clade_ancestor/amoebozoa
산출: results/clade_ancestor/amoebozoa/summary.json
tags:
  - 유형/실험
  - 실험/clade_ancestor-amoebozoa
---

# 실험 · clade_ancestor-amoebozoa

**산출물** `results/clade_ancestor/amoebozoa/summary.json`

## 한눈에

| 항목 | 값 |
| --- | --- |
| clade | amoebozoa |
| tips | 40 |
| clade_tips | 12 |
| families_considered | 5771 |
| node_reconstructed | most recent common ancestor of the sampled clade tips, which at this sample size is not the clade's root (see results/sample_size/summary.json) |
| n_models | 5 |
| n_bootstrap_trees | 20 |
| n_confident_families | 2069 |
| n_uncertain_families | 1593 |
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
 "reconstruction": 0.9307,
 "clade_frequency": 0.912
}
```

## functions_of_confident_families

```json
[
 [
  "catalytic activity",
  357
 ],
 [
  "organelle",
  162
 ],
 [
  "transferase activity",
  116
 ],
 [
  "helicase_nucleic",
  94
 ],
 [
  "hydrolase activity",
  94
 ],
 [
  "structural molecule activity",
  65
 ],
 [
  "repeat_domain",
  65
 ],
 [
  "protease",
  65
 ],
 [
  "DNA binding",
  57
 ],
 [
  "ribosome",
  56
 ],
 [
  "kinase",
  56
 ],
 [
  "catalytic activity, acting on RNA",
  55
 ],
 [
  "methyl_glyco_transferase",
  54
 ],
 [
  "nucleus",
  51
 ],
 [
  "RNA binding",
  48
 ],
 [
  "catalytic activity, acting on a protein",
  48
 ],
 [
  "oxidoreductase activity",
  47
 ],
 [
  "zinc_finger",
  44
 ],
 [
  "uncharacterised",
  42
 ],
 [
  "transporter_channel",
  38
 ]
]
```

## top_families

```json
[
 {
  "family": "HMGL-like",
  "description": "HMGL-like",
  "posterior": 1.0,
  "model_sd": 0.0,
  "tree_sd": 0.0,
  "share_of_clade_tips_today": 1.0
 },
 {
  "family": "MMM1",
  "description": "Maintenance of mitochondrial morphology protein 1",
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
  "family": "Ribonuc_L-PSP",
  "description": "Endoribonuclease L-PSP",
  "posterior": 1.0,
  "model_sd": 0.0,
  "tree_sd": 0.002,
  "share_of_clade_tips_today": 1.0
 },
 {
  "family": "Ras",
  "description": "Ras family",
  "posterior": 1.0,
  "model_sd": 0.0,
  "tree_sd": 0.0,
  "share_of_clade_tips_today": 1.0
 },
 {
  "family": "Ribosomal_60s",
  "description": "60s Acidic ribosomal protein",
  "posterior": 1.0,
  "model_sd": 0.0,
  "tree_sd": 0.0,
  "share_of_clade_tips_today": 1.0
 },
 {
  "family": "Lyase_1",
  "description": "Lyase",
  "posterior": 1.0,
  "model_sd": 0.0,
  "tree_sd": 0.0,
  "share_of_clade_tips_today": 1.0
 },
 {
  "family": "MMR_HSR1",
  "description": "50S ribosome-binding GTPase",
  "posterior": 1.0,
 
… (잘림 — 원본 파일 참조)
```

## uncertain_families

```json
[
 {
  "family": "Act-Frag_cataly",
  "description": "Actin-fragmin kinase, catalytic",
  "posterior": 0.934,
  "model_sd": 0.014,
  "tree_sd": 0.159
 },
 {
  "family": "RPN6_C_helix",
  "description": "26S proteasome subunit RPN6 C-terminal helix domain",
  "posterior": 0.934,
  "model_sd": 0.014,
  "tree_sd": 0.159
 },
 {
  "family": "FANCL_d3",
  "description": "FANCL UBC-like domain 3",
  "posterior": 0.934,
  "model_sd": 0.014,
  "tree_sd": 0.159
 },
 {
  "family": "LisH_TPL",
  "description": "LisH-like dimerisation domain",
  "posterior": 0.934,
  "model_sd": 0.014,
  "tree_sd": 0.159
 },
 {
  "family": "Med18",
  "description": "Med18 protein",
  "posterior": 0.934,
  "model_sd": 0.014,
  "tree_sd": 0.159
 },
 {
  "family": "PI4KB-PIK1_PIK",
  "description": "PI4KB/PIK1, accessory (PIK) domain",
  "posterior": 0.934,
  "model_sd": 0.014,
  "tree_sd": 0.159
 },
 {
  "family": "DUF8412",
  "description": "Domain of unknown function (DUF8412)",
  "posterior": 0.934,
  "model_sd": 0.014,
  "tree_sd": 0.159
 },
 {
  "family": "RRM_2",
  "description": "RNA recognition motif 2",
  "posterior": 0.924,
  "model_sd": 0.017,
  "tree_sd": 0.155
 },
 {
  "family": "ING",
  "description": "Inhibitor of growth proteins N-terminal histone-binding",
  "posterior": 0.924,
  "model_sd": 0.017,
  "tree_sd": 0.152
 },
 {
  "family": "Bin3",
  "description": "Bicoid-interacting protein 3 (Bin3)",
  "posterior": 0.924,
  "model_sd": 0.017,
  "tree_sd": 0.158
 },
 {
  "family": "GFO_IDH_MocA_C",
  "description": "Oxidoreductase family, C-terminal alpha/beta domain",
  "posterior": 0.924,

… (잘림 — 원본 파일 참조)
```

## 연결
- [[실험 목록]]
