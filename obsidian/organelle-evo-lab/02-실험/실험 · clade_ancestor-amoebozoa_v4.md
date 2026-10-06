---
유형: 실험
실행: clade_ancestor/amoebozoa_v4
산출: results/clade_ancestor/amoebozoa_v4/summary.json
tags:
  - 유형/실험
  - 실험/clade_ancestor-amoebozoa_v4
---

# 실험 · clade_ancestor-amoebozoa_v4

**산출물** `results/clade_ancestor/amoebozoa_v4/summary.json`

## 한눈에

| 항목 | 값 |
| --- | --- |
| clade | amoebozoa_v4 |
| tips | 40 |
| clade_tips | 12 |
| families_considered | 5771 |
| node_reconstructed | most recent common ancestor of the sampled clade tips, which at this sample size is not the clade's root (see results/sample_size/summary.json) |
| n_models | 5 |
| n_bootstrap_trees | 20 |
| completeness_model | True |
| reduced_branch_multiplier | False |
| n_confident_families | 2697 |
| n_uncertain_families | 1087 |
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
 "reconstruction": 0.9345,
 "clade_frequency": 0.912
}
```

## tip_completeness

```json
{
 "Acanthamoeba castellanii (strain ATCC 30010 / Neff)": 1.0,
 "Planoprotostelium fungivorum": 1.0,
 "Heterostelium pallidum (strain ATCC 26659 / Pp 5 / PN500) (Cellular slime mold) (Polysphondylium pallidum)": 0.967,
 "Cavenderia fasciculata (Slime mold) (Dictyostelium fasciculatum)": 0.973,
 "Polysphondylium violaceum": 0.987,
 "Tieghemostelium lacteum (Slime mold) (Dictyostelium lacteum)": 0.973,
 "Dictyostelium purpureum (Slime mold)": 0.993,
 "Dictyostelium discoideum (Social amoeba)": 1.0,
 "Dictyostelium firmibasis": 0.993,
 "Entamoeba invadens IP1": 0.32,
 "Entamoeba dispar (strain ATCC PRA-260 / SAW760)": 0.393,
 "Entamoeba nuttalli": 0.38
}
```

## completeness_markers_per_group

```json
{
 "clade": 150,
 "outgroup": 150
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
  203
 ],
 [
  "transferase activity",
  151
 ],
 [
  "hydrolase activity",
  111
 ],
 [
  "helicase_nucleic",
  111
 ],
 [
  "repeat_domain",
  91
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
  68
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
  62
 ],
 [
  "zinc_finger",
  61
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
  "uncharacterised",
  57
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
  48
 ]
]
```

## top_families

```json
[
 {
  "family": "zf-RING_UBOX",
  "description": "RING-type zinc-finger",
  "posterior": 1.0,
  "model_sd": 0.0,
  "tree_sd": 0.0,
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
  "family": "Peptidase_S9",
  "description": "Prolyl oligopeptidase family",
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
  "family": "ADH_zinc_N",
  "description": "Zinc-binding dehydrogenase",
  "posterior": 1.0,
  "model_sd": 0.0,
  "tree_sd": 0.0,
  "share_of_clade_tips_today": 1.0
 },
 {
  "family": "ADK",
  "description": "Adenylate kinase",
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
  "family": "Sod_Fe_C",
  "description": "Iron/manganese superoxide dismutases, C-terminal domain",
  "posterior": 1.0,
  "model_sd": 0.0,
  "tree_sd": 0.0,
  "share_of_clade_tips_today": 1.0
 },
 {
  "family": "tRNA-synt_1c",
  "description": "tRNA synthetases class I (E and Q), catalytic domain",
  "posterior": 1.0,
  "model_sd": 0.0,
  "tree_sd": 0.0,
  "share_of_clade_tips_today": 1.0
 },
 {
  "family": "tRNA-synt_1g",
  "description": "tRNA synthetases class I (M)",
  "posterior": 1.0,
  "model_sd": 0.0,
  "tree_sd": 0.0,
  "share_of_clade_tips_today": 1.0
 },
 {
  "family": "ADH_N",
  "description": "Alcohol dehydrogenase GroES-like domain",
  "posterior": 1.0,
  "model_sd": 0.0,
  "tree_sd": 0.0,
  "share_of_clade_tips_today": 1.0
 },
 {
  "family": "RCC1",
  "description": "Regulator of chromosome condensation (RCC1) repeat",
  "posterior": 1.0,
  "model_sd": 0.0,
  "tree_sd": 0.0,
  "share_of_clade_tips_today": 1.0
 },
 {
  "family": "PhoLip_ATPase_C",
  "description": "Phospholipid-translocating P-type ATPase C-terminal",
  "posterior": 1.0,
  "model_sd": 0.0,
  "tree_sd": 0.0,
  "share_of_clade_tips_today": 1.0
 },
 {
  "family": "tRNA-synt_His",
  "description": "Histidyl-tRNA synthetase",
  "posterior": 1.0,
  "model_sd": 0.0,
  "tree_sd": 0.0,
  "share_of_clade_tips_today": 1.0
 },
 {
  "family": "tRNA-synt_2d",
  "description": "tRNA synthetases class II core domain (F)",
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
  "family": "IPPT",
  "description": "IPP transferase",
  "posterior": 1.0,
  "model_sd": 0.0,
  "tree_sd": 0.0,
  "share_of_clade_tips_today": 1.0
 },
 {
  "family": "malic",
  "description": "Malic enzyme, N-terminal domain",
  "posterior": 1.0,
  "model_sd": 0.0,
  "tree_sd": 0.0,
  "share_of_clade_tips_today": 1.0
 },
 {
  "family": "polyprenyl_synt",
  "description": "Polyprenyl synthetase",
  "posterior": 1.0,
  "model_sd": 0.0,
  "tree_sd": 0.0,
  "share_of_clade_tips_today": 1.0
 },
 {
  "family": "tRNA-synt_1",
  "description": "tRNA synthetases class I (I, L, M and V)",
  "posterior": 1.0,
  "model_sd": 0.0,
  "tree_sd": 0.0,
  "share_of_clade_tips_today": 1.0
 },
 {
  "family": "tRNA-synt_1b",
  "description": "tRNA synthetases class I (W and Y)",
  "posterior": 1.0,
  "model_sd": 0.0,
  "tree_sd": 0.0,
  "share_of_clade_tips_today": 1.0
 },
 {
  "family": "AAA_lid_9",
  "description": "AAA lid domain",
  "posterior": 1.0,
  "model_sd": 0.0,
  "tree_sd": 0.0,
  "share_of_clade_tips_today": 1.0
 },
 {
  "family": "40S_S4_C",
  "description": "40S ribosomal protein S4 C-terminus",
  "posterior": 1.0,
  "model_sd": 0.0,
  "tree_sd": 0.0,
  "share_of_clade_tips_today": 1.0
 },
 {
  "family": "AAA_28",
  "description": "AAA domain",
  "posterior": 1.0,
  "model_sd": 0.0,
  "tree_sd": 0.0,
  "share_of_clade_tips_today": 1.0
 },
 {
  "family": "AAA_23",
  "description": "AAA domain",
  "posterior": 1.0,
  "model_sd": 0.0,
  "tree_sd": 0.0,
  "share_of_clade_tips_today": 1.0
 },
 {
  "family": "tRNA_anti-codon",
  "description": "OB-fold nucleic acid binding domain",
  "posterior": 1.0,
  "model_sd": 0.0,
  "tree_sd": 0.0,
  "share_of_clade_tips_today": 1.0
 },
 {
  "family": "tRNA_U5-meth_tr",
  "description": "tRNA (Uracil-5-)-methyltransferase",
  "posterior": 1.0,
  "model_sd": 0.0,
  "tree_sd": 0.0,
  "share_of_clade_tips_today": 1.0
 },
 {
  "family": "tRNA_SAD",
  "description": "Threonyl and Alanyl tRNA synthetase second additional domain",
  "posterior": 1.0,
  "model_sd": 0.0,
  "tree_sd": 0.0,
  "share_of_clade_tips_today": 1.0
 },
 {
  "family": "adh_short",
  "description": "short chain dehydrogenase",
  "posterior": 1.0,
  "model_sd": 0.0,
  "tree_sd": 0.0,
  "share_of_clade_tips_today": 1.0
 },
 {
  "family": "Ribosomal_L22",
  "description": "Ribosomal protein L22p/L17e",
  "posterior": 1.0,
  "model_sd": 0.0,
  "tree_sd": 0.0,
  "share_of_clade_tips_today": 1.0
 },
 {
  "family": "Ribosomal_L23",
  "description": "Ribosomal protein L23",
  "posterior": 1.0,
  "model_sd": 0.0,
  "tree_sd": 0.0,
  "share_of_clade_tips_today": 1.0
 },
 {
  "family": "Ribosomal_L24e",
  "description": "Ribosomal protein L24e",
  "posterior": 1.0,
  "model_sd": 0.0,
  "tree_sd": 0.0,
  "share_of_clade_tips_today": 1.0
 },
 {
  "family": "Ribosomal_L27A",
  "description": "Ribosomal proteins 50S-L15, 50S-L18e, 60S-L27A",
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
  "family
… (잘림, 원본 파일 참조)
```

## uncertain_families

```json
[
 {
  "family": "Big_2",
  "description": "Bacterial Ig-like domain (group 2)",
  "posterior": 0.9,
  "model_sd": 0.0,
  "tree_sd": 0.031
 },
 {
  "family": "EDR1_CTR1_ARMC3_pept",
  "description": "EDR1/CTR1/ARMC3, peptidase-like",
  "posterior": 0.9,
  "model_sd": 0.0,
  "tree_sd": 0.019
 },
 {
  "family": "Golgin_A5",
  "description": "Golgin subfamily A member 5",
  "posterior": 0.9,
  "model_sd": 0.0,
  "tree_sd": 0.019
 },
 {
  "family": "HAT_Syf1_M",
  "description": "Pre-mRNA-splicing factor SYF1 middle HAT repeat",
  "posterior": 0.9,
  "model_sd": 0.0,
  "tree_sd": 0.008
 },
 {
  "family": "AP_endonuc_2",
  "description": "Xylose isomerase-like TIM barrel",
  "posterior": 0.898,
  "model_sd": 0.0,
  "tree_sd": 0.09
 },
 {
  "family": "C1_1",
  "description": "Phorbol esters/diacylglycerol binding domain (C1 domain)",
  "posterior": 0.898,
  "model_sd": 0.0,
  "tree_sd": 0.036
 },
 {
  "family": "GKRP_SIS_N",
  "description": "Glucokinase regulatory protein N-terminal SIS domain",
  "posterior": 0.896,
  "model_sd": 0.0,
  "tree_sd": 0.046
 },
 {
  "family": "Chal_sti_synt_N",
  "description": "Chalcone and stilbene synthases, N-terminal domain",
  "posterior": 0.896,
  "model_sd": 0.0,
  "tree_sd": 0.046
 },
 {
  "family": "Glyco_hydro_39",
  "description": "Glycosyl hydrolases family 39",
  "posterior": 0.896,
  "model_sd": 0.0,
  "tree_sd": 0.046
 },
 {
  "family": "Glyco_transf_49",
  "description": "Glycosyl-transferase for dystroglycan",
  "posterior": 0.896,
  "model_sd": 0.0,
  "tree_sd": 0.046
 },
 {
  "family": "SGL_GH162",
  "description": "Endo-beta-1,2-glucanase SGL",
  "posterior": 0.896,
  "model_sd": 0.0,
  "tree_sd": 0.046
 },
 {
  "family": "Chal_sti_synt_C",
  "description": "Chalcone and stilbene synthases, C-terminal domain",
  "posterior": 0.896,
  "model_sd": 0.0,
  "tree_sd": 0.046
 },
 {
  "family": "DUF4291",
  "description": "Domain of unknown function (DUF4291)",
  "posterior": 0.895,
  "model_sd": 0.0,
  "tree_sd": 0.046
 },
 {
  "family": "Succ_DH_flav_C",
  "description": "Fumarate reductase flavoprotein C-term",
  "posterior": 0.895,
  "model_sd": 0.0,
  "tree_sd": 0.014
 },
 {
  "family": "RRF",
  "description": "Ribosome recycling factor",
  "posterior": 0.895,
  "model_sd": 0.0,
  "tree_sd": 0.014
 },
 {
  "family": "Peptidase_M76",
  "description": "Peptidase M76 family",
  "posterior": 0.895,
  "model_sd": 0.0,
  "tree_sd": 0.014
 },
 {
  "family": "Alba",
  "description": "Alba",
  "posterior": 0.895,
  "model_sd": 0.0,
  "tree_sd": 0.014
 },
 {
  "family": "RsfS",
  "description": "Ribosomal silencing factor during starvation",
  "posterior": 0.895,
  "model_sd": 0.0,
  "tree_sd": 0.014
 },
 {
  "family": "BAG",
  "description": "BAG domain",
  "posterior": 0.895,
  "model_sd": 0.0,
  "tree_sd": 0.026
 },
 {
  "family": "OsmC",
  "description": "OsmC-like protein",
  "posterior": 0.893,
  "model_sd": 0.0,
  "tree_sd": 0.049
 },
 {
  "family": "Zn_ribbon_RPB9",
  "description": "RNA polymerases M/15 Kd subunit",
  "posterior": 0.892,
  "model_sd": 0.0,
  "tree_sd": 0.023
 },
 {
  "family": "RNase_H",
  "description": "RNase H",
  "posterior": 0.892,
  "model_sd": 0.0,
  "tree_sd": 0.006
 },
 {
  "family": "Rep_fac-A_C",
  "description": "Replication factor-A C terminal domain",
  "posterior": 0.892,
  "model_sd": 0.0,
  "tree_sd": 0.02
 },
 {
  "family": "U-box_ZFPL1",
  "description": "ZFPL1-like, U-box domain",
  "posterior": 0.892,
  "model_sd": 0.0,
  "tree_sd": 0.071
 },
 {
  "family": "RRM_5",
  "description": "RNA recognition motif. (a.k.a. RRM, RBD, or RNP domain)",
  "posterior": 0.889,
  "model_sd": 0.0,
  "tree_sd": 0.064
 },
 {
  "family": "DeoC",
  "description": "DeoC/LacD family aldolase",
  "posterior": 0.889,
  "model_sd": 0.0,
  "tree_sd": 0.019
 },
 {
  "family": "Nop16",
  "description": "Ribosome biogenesis protein Nop16",
  "posterior": 0.889,
  "model_sd": 0.0,
  "tree_sd": 0.006
 },
 {
  "family": "CNOT10_TPR",
  "description": "CNOT10 tetratricopeptide repeat domain",
  "posterior": 0.888,
  "model_sd": 0.0,
  "tree_sd": 0.092
 },
 {
  "family": "TPR_DOCK",
  "description": "Dedicator of cytokinesis (DOCK) TPR region",
  "posterior": 0.888,
  "model_sd": 0.0,
  "tree_sd": 0.092
 },
 {
  "family": "DCC1-like",
  "description": "DCC1-like thiol-disulfide oxidoreductase",
  "posterior": 0.888,
  "model_sd": 0.0,
  "tree_sd": 0.092
 },
 {
  "family": "PAS_3",
  "description": "PAS fold",
  "posterior": 0.888,
  "model_sd": 0.0,
  "tree_sd": 0.092
 },
 {
  "family": "XLF",
  "description": "XLF N-terminal domain",
  "posterior": 0.888,
  "model_sd": 0.0,
  "tree_sd": 0.092
 },
 {
  "family": "Clathrin_propel",
  "description": "Clathrin propeller repeat",
  "posterior": 0.888,
  "model_sd": 0.0,
  "tree_sd": 0.092
 },
 {
  "family": "PhosphMutase",
  "description": "2,3-bisphosphoglycerate-independent phosphoglycerate mutase",
  "posterior": 0.888,
  "model_sd": 0.0,
  "tree_sd": 0.007
 },
 {
  "family": "Glyco_hydro_3_C",
  "description": "Glycosyl hydrolase family 3 C-terminal domain",
  "posterior": 0.888,
  "model_sd": 0.0,
  "tree_sd": 0.026
 },
 {
  "family": "NAD_kinase",
  "description": "ATP-NAD kinase N-terminal domain",
  "posterior": 0.887,
  "model_sd": 0.0,
  "tree_sd": 0.026
 },
 {
  "family": "Vault",
  "description": "Major Vault Protein repeat domain",
  "posterior": 0.887,
  "model_sd": 0.0,
  "tree_sd": 0.016
 },
 {
  "family": "tRNA_edit",
  "description": "Aminoacyl-tRNA editing domain",
  "posterior": 0.886,
  "model_sd": 0.0,
  "tree_sd": 0.019
 },
 {
  "family": "Rep_fac-A_3",
  "description": "Replication factor A protein 3",
  "posterior": 0.886,
  "model_sd": 0.0,
  "tree_sd": 0.021
 },
 {
  "family": "DHH",
  "description": "DHH family, N-terminal domain",
  "posterior": 0.885,
  "model_sd": 0.0,
  "tree_sd": 0.019
 }
]
```

## 연결
- [[실험 목록]]
