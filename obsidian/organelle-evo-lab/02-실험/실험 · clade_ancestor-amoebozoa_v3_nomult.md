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
  "description": "Ubiquitin carboxyl-terminal hydrolase",
  "posterior": 1.0,
  "model_sd": 0.0,
  "tree_sd": 0.0,
  "share_of_clade_tips_today": 1.0
 },
 {
  "family": "NUDIX",
  "description": "NUDIX domain",
  "posterior": 1.0,
  "model_sd": 0.0,
  "tree_sd": 0.0,
  "share_of_clade_tips_today": 1.0
 },
 {
  "family": "GTP_EFTU_D2",
  "description": "Elongation factor Tu domain 2",
  "posterior": 1.0,
  "model_sd": 0.0,
  "tree_sd": 0.0,
  "share_of_clade_tips_today": 1.0
 },
 {
  "family": "Toprim",
  "description": "Toprim domain",
  "posterior": 1.0,
  "model_sd": 0.0,
  "tree_sd": 0.0,
  "share_of_clade_tips_today": 1.0
 },
 {
  "family": "Beach",
  "description": "Beige/BEACH domain",
  "posterior": 1.0,
  "model_sd": 0.0,
  "tree_sd": 0.0,
  "share_of_clade_tips_today": 1.0
 },
 {
  "family": "PAP2",
  "description": "PAP2 superfamily",
  "posterior": 1.0,
  "model_sd": 0.0,
  "tree_sd": 0.0,
  "share_of_clade_tips_today": 1.0
 },
 {
  "family": "BPL_LplA_LipB",
  "description": "Biotin/lipoate A/B protein ligase family",
  "posterior": 1.0,
  "model_sd": 0.0,
  "tree_sd": 0.0,
  "share_of_clade_tips_today": 1.0
 },
 {
  "family": "Peptidase_M24",
  "description": "Metallopeptidase family M24",
  "posterior": 1.0,
  "model_sd": 0.0,
  "tree_sd": 0.0,
  "share_of_clade_tips_today": 1.0
 },
 {
  "family": "TrmO_N",
  "description": "tRNA-methyltransferase O N-terminal domain",
  "posterior": 1.0,
  "model_sd": 0.0,
  "tree_sd": 0.0,
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
  "family": "HSP90",
  "description": "Hsp90 protein",
  "posterior": 1.0,
  "model_sd": 0.0,
  "tree_sd": 0.0,
  "share_of_clade_tips_today": 1.0
 },
 {
  "family": "Thioredoxin",
  "description": "Thioredoxin",
  "posterior": 1.0,
  "model_sd": 0.0,
  "tree_sd": 0.0,
  "share_of_clade_tips_today": 1.0
 },
 {
  "family": "TTL",
  "description": "Tubulin-tyrosine ligase family",
  "posterior": 1.0,
  "model_sd": 0.0,
  "tree_sd": 0.0,
  "share_of_clade_tips_today": 1.0
 },
 {
  "family": "TatD_DNase",
  "description": "TatD related DNase",
  "posterior": 1.0,
  "model_sd": 0.0,
  "tree_sd": 0.0,
  "share_of_clade_tips_today": 1.0
 },
 {
  "family": "Topoisom_bac",
  "description": "DNA topoisomerase",
  "posterior": 1.0,
  "model_sd": 0.0,
  "tree_sd": 0.0,
  "share_of_clade_tips_today": 1.0
 },
 {
  "family": "Biotin_lipoyl",
  "description": "Biotin-requiring enzyme",
  "posterior": 1.0,
  "model_sd": 0.0,
  "tree_sd": 0.0,
  "share_of_clade_tips_today": 1.0
 },
 {
  "family": "Bromodomain",
  "description": "Bromodomain",
  "posterior": 1.0,
  "model_sd": 0.0,
  "tree_sd": 0.0,
  "share_of_clade_tips_today": 1.0
 },
 {
  "family": "PH",
  "description": "PH domain",
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
  "family": "M16C_assoc",
  "description": "Peptidase M16C associated",
  "posterior": 1.0,
  "model_sd": 0.0,
  "tree_sd": 0.0,
  "share_of_clade_tips_today": 1.0
 },
 {
  "family": "WD40",
  "description": "WD domain, G-beta repeat",
  "posterior": 1.0,
  "model_sd": 0.0,
  "tree_sd": 0.0,
  "share_of_clade_tips_today": 1.0
 },
 {
  "family": "HSP20",
  "description": "Hsp20/alpha crystallin family",
  "posterior": 1.0,
  "model_sd": 0.0,
  "tree_sd": 0.0,
  "share_of_clade_tips_today": 1.0
 },
 {
  "family": "CDP-OH_P_transf",
  "description": "CDP-alcohol phosphatidyltransferase",
  "posterior": 1.0,
  "model_sd": 0.0,
  "tree_sd": 0.0,
  "share_of_clade_tips_today": 1.0
 },
 {
  "family": "PseudoU_synth_2",
  "description": "RNA pseudouridylate synthase",
  "posterior": 1.0,
  "model_sd": 0.0,
  "tree_sd": 0.0,
  "share_of_clade_tips_today": 1.0
 },
 {
  "family": "Pyr_redox_2",
  "description": "Pyridine nucleotide-disulphide oxidoreductase",
  "posterior": 1.0,
  "model_sd": 0.0,
  "tree_sd": 0.0,
  "share_of_clade_tips_today": 1.0
 },
 {
  "family": "Pyrophosphatase",
  "description": "Inorganic pyrophosphatase",
  "posterior": 1.0,
  "model_sd": 0.0,
  "tree_sd": 0.0,
  "share_of_clade_tips_today": 1.0
 },
 {
  "family": "Lactamase_B",
  "description": "Metallo-beta-lactamase superfamily",
  
… (잘림, 원본 파일 참조)
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
  "description": "Chalcone and stilbene synthases, C-terminal domain",
  "posterior": 0.895,
  "model_sd": 0.0,
  "tree_sd": 0.047
 },
 {
  "family": "Glyco_hydro_39",
  "description": "Glycosyl hydrolases family 39",
  "posterior": 0.895,
  "model_sd": 0.0,
  "tree_sd": 0.047
 },
 {
  "family": "DUF4291",
  "description": "Domain of unknown function (DUF4291)",
  "posterior": 0.895,
  "model_sd": 0.0,
  "tree_sd": 0.047
 },
 {
  "family": "U-box_ZFPL1",
  "description": "ZFPL1-like, U-box domain",
  "posterior": 0.895,
  "model_sd": 0.0,
  "tree_sd": 0.065
 },
 {
  "family": "RNase_H",
  "description": "RNase H",
  "posterior": 0.895,
  "model_sd": 0.0,
  "tree_sd": 0.005
 },
 {
  "family": "NAD_kinase",
  "description": "ATP-NAD kinase N-terminal domain",
  "posterior": 0.895,
  "model_sd": 0.0,
  "tree_sd": 0.025
 },
 {
  "family": "tRNA_edit",
  "description": "Aminoacyl-tRNA editing domain",
  "posterior": 0.894,
  "model_sd": 0.0,
  "tree_sd": 0.018
 },
 {
  "family": "DUF4832",
  "description": "Domain of unknown function (DUF4832)",
  "posterior": 0.893,
  "model_sd": 0.0,
  "tree_sd": 0.023
 },
 {
  "family": "OsmC",
  "description": "OsmC-like protein",
  "posterior": 0.892,
  "model_sd": 0.0,
  "tree_sd": 0.05
 },
 {
  "family": "DHH",
  "description": "DHH family, N-terminal domain",
  "posterior": 0.892,
  "model_sd": 0.0,
  "tree_sd": 0.018
 },
 {
  "family": "RRM_5",
  "description": "RNA recognition motif. (a.k.a. RRM, RBD, or RNP domain)",
  "posterior": 0.89,
  "model_sd": 0.0,
  "tree_sd": 0.029
 },
 {
  "family": "Nop16",
  "description": "Ribosome biogenesis protein Nop16",
  "posterior": 0.889,
  "model_sd": 0.0,
  "tree_sd": 0.006
 },
 {
  "family": "SLBP_RNA_bind",
  "description": "Histone RNA hairpin-binding protein RNA-binding domain",
  "posterior": 0.889,
  "model_sd": 0.0,
  "tree_sd": 0.136
 },
 {
  "family": "BRCT_3",
  "description": "BRCA1 C Terminus (BRCT) domain",
  "posterior": 0.889,
  "model_sd": 0.0,
  "tree_sd": 0.051
 },
 {
  "family": "XLF",
  "description": "XLF N-terminal domain",
  "posterior": 0.888,
  "model_sd": 0.0,
  "tree_sd": 0.094
 },
 {
  "family": "PAS_3",
  "description": "PAS fold",
  "posterior": 0.888,
  "model_sd": 0.0,
  "tree_sd": 0.094
 },
 {
  "family": "TPR_DOCK",
  "description": "Dedicator of cytokinesis (DOCK) TPR region",
  "posterior": 0.888,
  "model_sd": 0.0,
  "tree_sd": 0.094
 },
 {
  "family": "Clathrin_propel",
  "description": "Clathrin propeller repeat",
  "posterior": 0.888,
  "model_sd": 0.0,
  "tree_sd": 0.094
 },
 {
  "family": "CNOT10_TPR",
  "description": "CNOT10 tetratricopeptide repeat domain",
  "posterior": 0.888,
  "model_sd": 0.0,
  "tree_sd": 0.094
 },
 {
  "family": "DCC1-like",
  "description": "DCC1-like thiol-disulfide oxidoreductase",
  "posterior": 0.888,
  "model_sd": 0.0,
  "tree_sd": 0.094
 },
 {
  "family": "THUMP",
  "description": "THUMP domain",
  "posterior": 0.887,
  "model_sd": 0.0,
  "tree_sd": 0.05
 },
 {
  "family": "RPN13_C",
  "description": "UCH-binding domain",
  "posterior": 0.884,
  "model_sd": 0.0,
  "tree_sd": 0.054
 },
 {
  "family": "Rep_fac-A_3",
  "description": "Replication factor A protein 3",
  "posterior": 0.884,
  "model_sd": 0.0,
  "tree_sd": 0.021
 },
 {
  "family": "HD_4",
  "description": "HD domain",
  "posterior": 0.883,
  "model_sd": 0.0,
  "tree_sd": 0.029
 },
 {
  "family": "Arginase",
  "description": "Arginase family",
  "posterior": 0.882,
  "model_sd": 0.0,
  "tree_sd": 0.01
 },
 {
  "family": "SH3BGR",
  "description": "SH3-binding, glutamic acid-rich protein",
  "posterior": 0.881,
  "model_sd": 0.0,
  "tree_sd": 0.026
 },
 {
  "family": "DHFR_1",
  "description": "Dihydrofolate reductase",
  "posterior": 0.881,
  "model_sd": 0.0,
  "tree_sd": 0.021
 },
 {
  "family": "5-FTHF_cyc-lig",
  "description": "5-formyltetrahydrofolate cyclo-ligase family",
  "posterior": 0.88,
  "model_sd": 0.0,
  "tree_sd": 0.022
 },
 {
  "family": "Zn_ribbon_PADR1",
  "description": "PADR1 domain, zinc ribbon fold",
  "posterior": 0.88,
  "model_sd": 0.0,
  "tree_sd": 0.042
 },
 {
  "family": "Ribosomal_S2",
  "description": "Ribosomal protein S2",
  "posterior": 0.879,
  "model_sd": 0.0,
  "tree_sd": 0.011
 }
]
```

## 연결
- [[실험 목록]]
