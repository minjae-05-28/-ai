---
유형: 실험
실행: clade_ancestor/amoebozoa_v3_nomult
산출: results/clade_ancestor/amoebozoa_v3_nomult/summary.json
tags:
  - 유형/실험
  - 실험/clade_ancestor-amoebozoa_v3_nomult
---

# 실험 · clade_ancestor-amoebozoa_v3_nomult

**산출물** `results/clade_ancestor/amoebozoa_v3_nomult/summary.json`

## 한눈에

| 항목 | 값 |
| --- | --- |
| clade | amoebozoa_v3_nomult |
| tips | 40 |
| clade_tips | 12 |
| families_considered | 5771 |
| node_reconstructed | most recent common ancestor of the sampled clade tips, which at this sample size is not the clade's root (see results/sample_size/summary.json) |
| n_models | 5 |
| n_bootstrap_trees | 20 |
| completeness_model | True |
| reduced_branch_multiplier | False |
| n_completeness_markers | 150 |
| n_confident_families | 2706 |
| n_uncertain_families | 1082 |
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
 "reconstruction": 0.936,
 "clade_frequency": 0.912
}
```

## tip_completeness

```json
{
 "Acanthamoeba castellanii (strain ATCC 30010 / Neff)": 1.0,
 "Planoprotostelium fungivorum": 1.0,
 "Heterostelium pallidum (strain ATCC 26659 / Pp 5 / PN500) (Cellular slime mold) (Polysphondylium pallidum)": 0.967,
 "Cavenderia fasciculata (Slime mold) (Dictyostelium fasciculatum)": 0.953,
 "Polysphondylium violaceum": 0.987,
 "Tieghemostelium lacteum (Slime mold) (Dictyostelium lacteum)": 0.967,
 "Dictyostelium purpureum (Slime mold)": 0.98,
 "Dictyostelium discoideum (Social amoeba)": 1.0,
 "Dictyostelium firmibasis": 0.987,
 "Entamoeba invadens IP1": 0.413,
 "Entamoeba dispar (strain ATCC PRA-260 / SAW760)": 0.46,
 "Entamoeba nuttalli": 0.46
}
```

## groups_without_a_completeness_score

```json
[]
```

## functions_of_confident_families

```json
[
 [
  "catalytic activity",
  435
 ],
 [
  "organelle",
  201
 ],
 [
  "transferase activity",
  150
 ],
 [
  "hydrolase activity",
  112
 ],
 [
  "helicase_nucleic",
  112
 ],
 [
  "repeat_domain",
  92
 ],
 [
  "protease",
  79
 ],
 [
  "nucleus",
  73
 ],
 [
  "methyl_glyco_transferase",
  69
 ],
 [
  "structural molecule activity",
  67
 ],
 [
  "DNA binding",
  64
 ],
 [
  "kinase",
  63
 ],
 [
  "zinc_finger",
  62
 ],
 [
  "oxidoreductase activity",
  61
 ],
 [
  "uncharacterised",
  59
 ],
 [
  "catalytic activity, acting on RNA",
  58
 ],
 [
  "ribosome",
  58
 ],
 [
  "catalytic activity, acting on a protein",
  54
 ],
 [
  "RNA binding",
  54
 ],
 [
  "transporter_channel",
  48
 ]
]
```

## top_families

```json
[
 {
  "family": "Transket_pyr",
  "description": "Transketolase, pyrimidine binding domain",
  "posterior": 1.0,
  "model_sd": 0.0,
  "tree_sd": 0.0,
  "share_of_clade_tips_today": 1.0
 },
 {
  "family": "Peptidase_M3",
  "description": "Peptidase family M3",
  "posterior": 1.0,
  "model_sd": 0.0,
  "tree_sd": 0.0,
  "share_of_clade_tips_today": 1.0
 },
 {
  "family": "EF-hand_5",
  "description": "EF hand",
  "posterior": 1.0,
  "model_sd": 0.0,
  "tree_sd": 0.0,
  "share_of_clade_tips_today": 1.0
 },
 {
  "family": "EF-hand_7",
  "description": "EF-hand domain pair",
  "posterior": 1.0,
  "model_sd": 0.0,
  "tree_sd": 0.0,
  "share_of_clade_tips_today": 1.0
 },
 {
  "family": "Helicase_C",
  "description": "Helicase conserved C-terminal domain",
  "posterior": 1.0,
  "model_sd": 0.0,
  "tree_sd": 0.0,
  "share_of_clade_tips_today": 1.0
 },
 {
  "family": "GED",
  "description": "Dynamin GTPase effector domain",
  "posterior": 1.0,
  "model_sd": 0.0,
  "tree_sd": 0.0,
  "share_of_clade_tips_today": 1.0
 },
 {
  "family": "NIF",
  "description": "NLI interacting factor-like phosphatase",
  "posterior": 1.0,
  "model_sd": 0.0,
  "tree_sd": 0.0,
  "share_of_clade_tips_today": 1.0
 },
 {
  "family": "Tubulin",
  "description": "Tubulin/FtsZ family, GTPase domain",
  "posterior": 1.0,
  "model_sd": 0.0,
  "tree_sd": 0.0,
  "share_of_clade_tips_today": 1.0
 },
 {
  "family": "GTP_EFTU",
  "description": "Elongation factor Tu GTP binding domain",
  "posterior": 1.0,
  "model_sd": 0.0,
  "tree_sd": 0.0,
  "share_of_clade_tips_today": 1.0
 },
 {
  "family": "UCH",
  "description":
… (잘림 — 원본 파일 참조)
```

## uncertain_families

```json
[
 {
  "family": "AP_endonuc_2",
  "description": "Xylose isomerase-like TIM barrel",
  "posterior": 0.9,
  "model_sd": 0.0,
  "tree_sd": 0.093
 },
 {
  "family": "Zn_ribbon_RPB9",
  "description": "RNA polymerases M/15 Kd subunit",
  "posterior": 0.899,
  "model_sd": 0.0,
  "tree_sd": 0.022
 },
 {
  "family": "Nop25",
  "description": "Nucleolar protein 12 (25kDa)",
  "posterior": 0.899,
  "model_sd": 0.0,
  "tree_sd": 0.021
 },
 {
  "family": "DeoC",
  "description": "DeoC/LacD family aldolase",
  "posterior": 0.896,
  "model_sd": 0.0,
  "tree_sd": 0.018
 },
 {
  "family": "Rsm22",
  "description": "Mitochondrial small ribosomal subunit Rsm22",
  "posterior": 0.896,
  "model_sd": 0.0,
  "tree_sd": 0.023
 },
 {
  "family": "Glyco_hydro_3_C",
  "description": "Glycosyl hydrolase family 3 C-terminal domain",
  "posterior": 0.895,
  "model_sd": 0.0,
  "tree_sd": 0.024
 },
 {
  "family": "GKRP_SIS_N",
  "description": "Glucokinase regulatory protein N-terminal SIS domain",
  "posterior": 0.895,
  "model_sd": 0.0,
  "tree_sd": 0.047
 },
 {
  "family": "Glyco_transf_49",
  "description": "Glycosyl-transferase for dystroglycan",
  "posterior": 0.895,
  "model_sd": 0.0,
  "tree_sd": 0.047
 },
 {
  "family": "SGL_GH162",
  "description": "Endo-beta-1,2-glucanase SGL",
  "posterior": 0.895,
  "model_sd": 0.0,
  "tree_sd": 0.047
 },
 {
  "family": "Chal_sti_synt_N",
  "description": "Chalcone and stilbene synthases, N-terminal domain",
  "posterior": 0.895,
  "model_sd": 0.0,
  "tree_sd": 0.047
 },
 {
  "family": "Chal_sti_synt_C",
  "description": "Chalcone and stilbene synthases, C
… (잘림 — 원본 파일 참조)
```

## 연결
- [[실험 목록]]
