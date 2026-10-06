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
  "family": "Ribosomal_L1",
  "description": "Ribosomal protein L1p/L10e family",
  "posterior": 1.0,
  "model_sd": 0.0,
  "tree_sd": 0.0,
  "share_of_clade_tips_today": 1.0
 },
 {
  "family": "Ribosomal_L10",
  "description": "Ribosomal protein L10",
  "posterior": 1.0,
  "model_sd": 0.0,
  "tree_sd": 0.0,
  "share_of_clade_tips_today": 1.0
 },
 {
  "family": "Ribosomal_L29",
  "description": "Ribosomal L29 protein",
  "posterior": 1.0,
  "model_sd": 0.0,
  "tree_sd": 0.0,
  "share_of_clade_tips_today": 1.0
 },
 {
  "family": "Rhodanese",
  "description": "Rhodanese-like domain",
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
  "family": "Lactamase_B",
  "description": "Metallo-beta-lactamase superfamily",
  "posterior": 1.0,
  "model_sd": 0.0,
  "tree_sd": 0.0,
  "share_of_clade_tips_today": 1.0
 },
 {
  "family": "Ribosomal_L15e",
  "description": "Ribosomal L15",
  "posterior": 1.0,
  "model_sd": 0.0,
  "tree_sd": 0.0,
  "share_of_clade_tips_today": 1.0
 },
 {
  "family": "Ribosomal_L16",
  "description": "Ribosomal protein L16p/L10e",
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
  "family": "Ribosomal_L14e",
  "description": "Ribosomal protein L14",
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
  "family": "MutS_III",
  "description": "MutS domain III",
  "posterior": 1.0,
  "model_sd": 0.0,
  "tree_sd": 0.0,
  "share_of_clade_tips_today": 1.0
 },
 {
  "family": "MutS_IV",
  "description": "MutS family domain IV",
  "posterior": 1.0,
  "model_sd": 0.0,
  "tree_sd": 0.0,
  "share_of_clade_tips_today": 1.0
 },
 {
  "family": "MutS_V",
  "description": "MutS domain V",
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
  "family": "Lactamase_B_2",
  "description": "Beta-lactamase superfamily domain",
  "posterior": 1.0,
  "model_sd": 0.0,
  "tree_sd": 0.0,
  "share_of_clade_tips_today": 1.0
 },
 {
  "family": "Ldh_1_C",
  "description": "lactate/malate dehydrogenase, alpha/beta C-terminal domain",
  "posterior": 1.0,
  "model_sd": 0.0,
  "tree_sd": 0.0,
  "share_of_clade_tips_today": 1.0
 },
 {
  "family": "Mito_carr",
  "description": "Mitochondrial carrier protein",
  "posterior": 1.0,
  "model_sd": 0.0,
  "tree_sd": 0.0,
  "share_of_clade_tips_today": 1.0
 },
 {
  "family": "Metallophos_2",
  "description": "Calcineurin-like phosphoesterase superfamily domain",
  "posterior
… (잘림, 원본 파일 참조)
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
  "description": "Calcium-activated potassium channel slowpoke-like RCK domain",
  "posterior": 0.894,
  "model_sd": 0.007,
  "tree_sd": 0.02
 },
 {
  "family": "NCA2",
  "description": "ATP synthase regulation protein NCA2",
  "posterior": 0.894,
  "model_sd": 0.018,
  "tree_sd": 0.008
 },
 {
  "family": "AP_endonuc_2",
  "description": "Xylose isomerase-like TIM barrel",
  "posterior": 0.894,
  "model_sd": 0.002,
  "tree_sd": 0.094
 },
 {
  "family": "OsmC",
  "description": "OsmC-like protein",
  "posterior": 0.893,
  "model_sd": 0.002,
  "tree_sd": 0.049
 },
 {
  "family": "Zn_ribbon_RPB9",
  "description": "RNA polymerases M/15 Kd subunit",
  "posterior": 0.893,
  "model_sd": 0.001,
  "tree_sd": 0.023
 },
 {
  "family": "Rep_fac-A_C",
  "description": "Replication factor-A C terminal domain",
  "posterior": 0.892,
  "model_sd": 0.0,
  "tree_sd": 0.018
 },
 {
  "family": "YbjQ_2",
  "description": "C2 domain-containing protein 5, YbjQ-like domain",
  "posterior": 0.892,
  "model_sd": 0.002,
  "tree_sd": 0.02
 },
 {
  "family": "Peptidase_C78",
  "description": "Peptidase family C78",
  "posterior": 0.892,
  "model_sd": 0.002,
  "tree_sd": 0.02
 },
 {
  "family": "TRAPPC-Trs85",
  "description": "ER-Golgi trafficking TRAPP I complex 85 kDa subunit",
  "posterior": 0.892,
  "model_sd": 0.002,
  "tree_sd": 0.02
 },
 {
  "family": "Mcl1_mid",
  "description": "Minichromosome loss protein, Mcl1, middle region",
  "posterior": 0.892,
  "model_sd": 0.002,
  "tree_sd": 0.02
 },
 {
  "family": "CLASP_N",
  "description": "CLASP N terminal",
  "posterior": 0.892,
  "model_sd": 0.002,
  "tree_sd": 0.02
 },
 {
  "family": "RNase_H",
  "description": "RNase H",
  "posterior": 0.891,
  "model_sd": 0.0,
  "tree_sd": 0.007
 },
 {
  "family": "PhosphMutase",
  "description": "2,3-bisphosphoglycerate-independent phosphoglycerate mutase",
  "posterior": 0.89,
  "model_sd": 0.023,
  "tree_sd": 0.012
 },
 {
  "family": "Arginase",
  "description": "Arginase family",
  "posterior": 0.89,
  "model_sd": 0.016,
  "tree_sd": 0.016
 },
 {
  "family": "BRCT_3",
  "description": "BRCA1 C Terminus (BRCT) domain",
  "posterior": 0.89,
  "model_sd": 0.001,
  "tree_sd": 0.051
 },
 {
  "family": "DeoC",
  "description": "DeoC/LacD family aldolase",
  "posterior": 0.89,
  "model_sd": 0.0,
  "tree_sd": 0.019
 },
 {
  "family": "RRM_5",
  "description": "RNA recognition motif. (a.k.a. RRM, RBD, or RNP domain)",
  "posterior": 0.89,
  "model_sd": 0.0,
  "tree_sd": 0.014
 },
 {
  "family": "Nop16",
  "description": "Ribosome biogenesis protein Nop16",
  "posterior": 0.889,
  "model_sd": 0.0,
  "tree_sd": 0.006
 },
 {
  "family": "Clathrin_propel",
  "description": "Clathrin propeller repeat",
  "posterior": 0.889,
  "model_sd": 0.003,
  "tree_sd": 0.093
 },
 {
  "family": "XLF",
  "description": "XLF N-terminal domain",
  "posterior": 0.889,
  "model_sd": 0.003,
  "tree_sd": 0.093
 },
 {
  "family": "TPR_DOCK",
  "description": "Dedicator of cytokinesis (DOCK) TPR region",
  "posterior": 0.889,
  "model_sd": 0.003,
  "tree_sd": 0.093
 },
 {
  "family": "PAS_3",
  "description": "PAS fold",
  "posterior": 0.889,
  "model_sd": 0.003,
  "tree_sd": 0.093
 },
 {
  "family": "CNOT10_TPR",
  "description": "CNOT10 tetratricopeptide repeat domain",
  "posterior": 0.889,
  "model_sd": 0.003,
  "tree_sd": 0.093
 },
 {
  "family": "DCC1-like",
  "description": "DCC1-like thiol-disulfide oxidoreductase",
  "posterior": 0.889,
  "model_sd": 0.003,
  "tree_sd": 0.093
 },
 {
  "family": "DFP",
  "description": "DNA/pantothenate metabolism flavoprotein C-terminal domain",
  "posterior": 0.888,
  "model_sd": 0.017,
  "tree_sd": 0.009
 },
 {
  "family": "tRNA_edit",
  "description": "Aminoacyl-tRNA editing domain",
  "posterior": 0.887,
  "model_sd": 0.0,
  "tree_sd": 0.019
 },
 {
  "family": "DHH",
  "description": "DHH family, N-terminal domain",
  "posterior": 0.887,
  "model_sd": 0.0,
  "tree_sd": 0.019
 },
 {
  "family": "Rep_fac-A_3",
  "description": "Replication factor A protein 3",
  "posterior": 0.886,
  "model_sd": 0.003,
  "tree_sd": 0.021
 },
 {
  "family": "SYY_C-terminal",
  "description": "Tyrosine--tRNA ligase SYY-like C-terminal domain",
  "posterior": 0.885,
  "model_sd": 0.11,
  "tree_sd": 0.093
 },
 {
  "family": "COG2_N",
  "description": "COG2 N-terminal",
  "posterior": 0.884,
  "model_sd": 0.02,
  "tree_sd": 0.014
 }
]
```

## 연결
- [[실험 목록]]
