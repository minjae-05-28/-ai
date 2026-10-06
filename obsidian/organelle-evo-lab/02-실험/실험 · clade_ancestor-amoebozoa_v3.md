---
유형: 실험
실행: clade_ancestor/amoebozoa_v3
산출: results/clade_ancestor/amoebozoa_v3/summary.json
tags:
  - 유형/실험
  - 실험/clade_ancestor-amoebozoa_v3
---

# 실험 · clade_ancestor-amoebozoa_v3

**산출물** `results/clade_ancestor/amoebozoa_v3/summary.json`

## 한눈에

| 항목 | 값 |
| --- | --- |
| clade | amoebozoa_v3 |
| tips | 40 |
| clade_tips | 12 |
| families_considered | 5771 |
| node_reconstructed | most recent common ancestor of the sampled clade tips, which at this sample size is not the clade's root (see results/sample_size/summary.json) |
| n_models | 5 |
| n_bootstrap_trees | 20 |
| completeness_model | True |
| reduced_branch_multiplier | True |
| n_completeness_markers | 150 |
| n_confident_families | 2693 |
| n_uncertain_families | 1099 |
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
 "reconstruction": 0.9313,
 "clade_frequency": 0.912
}
```

## tip_completeness

```json
{
 "Acanthamoeba castellanii (strain ATCC 30010 / Neff)": 1.0,
 "Planoprotostelium fungivorum": 1.0,
 "Heterostelium pallidum (strain ATCC 26659 / Pp 5 / PN500) (Cellular slime mold) (Polysphondylium pallidum)": 0.993,
 "Cavenderia fasciculata (Slime mold) (Dictyostelium fasciculatum)": 0.98,
 "Polysphondylium violaceum": 1.0,
 "Tieghemostelium lacteum (Slime mold) (Dictyostelium lacteum)": 0.98,
 "Dictyostelium purpureum (Slime mold)": 0.967,
 "Dictyostelium discoideum (Social amoeba)": 1.0,
 "Dictyostelium firmibasis": 1.0,
 "Entamoeba invadens IP1": 0.487,
 "Entamoeba dispar (strain ATCC PRA-260 / SAW760)": 0.5,
 "Entamoeba nuttalli": 0.52
}
```

## functions_of_confident_families

```json
[
 [
  "catalytic activity",
  436
 ],
 [
  "organelle",
  203
 ],
 [
  "transferase activity",
  153
 ],
 [
  "helicase_nucleic",
  111
 ],
 [
  "hydrolase activity",
  111
 ],
 [
  "repeat_domain",
  93
 ],
 [
  "protease",
  78
 ],
 [
  "nucleus",
  73
 ],
 [
  "methyl_glyco_transferase",
  71
 ],
 [
  "structural molecule activity",
  69
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
  "oxidoreductase activity",
  61
 ],
 [
  "zinc_finger",
  61
 ],
 [
  "uncharacterised",
  60
 ],
 [
  "ribosome",
  59
 ],
 [
  "catalytic activity, acting on RNA",
  58
 ],
 [
  "RNA binding",
  54
 ],
 [
  "catalytic activity, acting on a protein",
  53
 ],
 [
  "transporter_channel",
  47
 ]
]
```

## top_families

```json
[
 {
  "family": "FMN_red",
  "description": "NADPH-dependent FMN reductase",
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
  "family": "Ribonuc_L-PSP",
  "description": "Endoribonuclease L-PSP",
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
  "family": "MMM1",
  "description": "Maintenance of mitochondrial morphology protein 1",
  "posterior": 1.0,
  "model_sd": 0.0,
  "tree_sd": 0.002,
  "share_of_clade_tips_today": 1.0
 },
 {
  "family": "HSP70",
  "description": "Hsp70 protein",
  "posterior": 1.0,
  "model_sd": 0.0,
  "tree_sd": 0.0,
  "share_of_clade_tips_today": 1.0
 },
 {
  "family": "HhH-GPD",
  "description": "HhH-GPD superfamily base excision DNA repair protein",
  "posterior": 1.0,
  "model_sd": 0.0,
  "tree_sd": 0.0,
  "share_of_clade_tips_today": 1.0
 },
 {
  "family": "Ribosomal_L18",
  "description": "Ribosomal protein 60S L18 and 50S L18e",
  "posterior": 1.0,
  "model_sd": 0.0,
  "tree_sd": 0.0,
  "share_of_clade_tips_today": 1.0
 },
 {
  "family": "Ribosomal_L21e",
  "description": "Ribosomal protein L21e",
  "posterior": 1.0,
  "model_sd": 0.0,
  "tree_sd": 0.0,
  "share_of_clade_tips_today": 1.0
 },
 {
  "family": "
… (잘림 — 원본 파일 참조)
```

## uncertain_families

```json
[
 {
  "family": "RS4NT",
  "description": "RS4NT (NUC023) domain",
  "posterior": 0.898,
  "model_sd": 0.021,
  "tree_sd": 0.013
 },
 {
  "family": "U-box_ZFPL1",
  "description": "ZFPL1-like, U-box domain",
  "posterior": 0.898,
  "model_sd": 0.001,
  "tree_sd": 0.066
 },
 {
  "family": "Glyco_hydro_39",
  "description": "Glycosyl hydrolases family 39",
  "posterior": 0.896,
  "model_sd": 0.002,
  "tree_sd": 0.046
 },
 {
  "family": "Chal_sti_synt_C",
  "description": "Chalcone and stilbene synthases, C-terminal domain",
  "posterior": 0.896,
  "model_sd": 0.002,
  "tree_sd": 0.046
 },
 {
  "family": "Chal_sti_synt_N",
  "description": "Chalcone and stilbene synthases, N-terminal domain",
  "posterior": 0.896,
  "model_sd": 0.002,
  "tree_sd": 0.046
 },
 {
  "family": "SGL_GH162",
  "description": "Endo-beta-1,2-glucanase SGL",
  "posterior": 0.896,
  "model_sd": 0.002,
  "tree_sd": 0.046
 },
 {
  "family": "Glyco_transf_49",
  "description": "Glycosyl-transferase for dystroglycan",
  "posterior": 0.896,
  "model_sd": 0.002,
  "tree_sd": 0.046
 },
 {
  "family": "GKRP_SIS_N",
  "description": "Glucokinase regulatory protein N-terminal SIS domain",
  "posterior": 0.896,
  "model_sd": 0.002,
  "tree_sd": 0.046
 },
 {
  "family": "DUF4291",
  "description": "Domain of unknown function (DUF4291)",
  "posterior": 0.896,
  "model_sd": 0.002,
  "tree_sd": 0.047
 },
 {
  "family": "Helicase_PWI",
  "description": "N-terminal helicase PWI domain",
  "posterior": 0.895,
  "model_sd": 0.0,
  "tree_sd": 0.013
 },
 {
  "family": "Slo-like_RCK",
  "description": "Calcium-activated pota
… (잘림 — 원본 파일 참조)
```

## 연결
- [[실험 목록]]
