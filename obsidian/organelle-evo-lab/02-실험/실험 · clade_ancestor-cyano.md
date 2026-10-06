---
유형: 실험
실행: clade_ancestor/cyano
산출: results/clade_ancestor/cyano/summary.json
tags:
  - 유형/실험
  - 실험/clade_ancestor-cyano
---

# 실험 · clade_ancestor-cyano

**산출물** `results/clade_ancestor/cyano/summary.json`

## 한눈에

| 항목 | 값 |
| --- | --- |
| clade | cyano |
| tips | 312 |
| clade_tips | 162 |
| families_considered | 10002 |
| rooted_on | Prevotella jejuni |
| root_split_intruders | None |
| node_reconstructed | most recent common ancestor of the sampled clade tips, which at this sample size is not the clade's root (see results/sample_size/summary.json) |
| n_models | 5 |
| n_bootstrap_trees | 0 |
| completeness_model | True |
| reduced_branch_multiplier | False |
| n_confident_families | 1716 |
| n_uncertain_families | 445 |
| size_not_reported | the simulation showed a 16-17% underestimate of ancestor size at this sample size, so no family count is quoted |

## clade_species

```json
[
 "Gloeobacter kilaueensis (strain ATCC BAA-2537 / CCAP 1431/1 / ULC 316 / JS1)",
 "Gloeobacter violaceus (strain ATCC 29082 / PCC 7421)",
 "Gloeobacter morelensis MG652769",
 "Gloeomargarita lithophora Alchichica-D10",
 "Tumidithrix elongata BACA0141",
 "Pseudanabaena cinerea FACHB-1277",
 "Pseudanabaena galeata UHCC 0370",
 "Pseudanabaena yagii GIHE-NHR1",
 "Pseudocalidococcus azoricus BACA0444",
 "Candidatus Synechococcus calcipolaris G9",
 "Parathermosynechococcus lividus PCC 6715",
 "Thermosynechococcus vestitus (strain NIES-2133 / IAM M-273 / BP-1)",
 "Thermosynechococcus sichuanensis E542",
 "Acaryochloris thomasi RCC1774",
 "Lyngbya confervoides BDU141951",
 "Neosynechococcus sphagnicola sy1",
 "Romeriopsis navalis LEGE 11480",
 "Leptolyngbya boryana NIES-2135",
 "Myxacorys almedinensis A",
 "Thermocoleostomius sinensis A174",
 "Thermoleptolyngbya sichuanensis A183",
 "Vacuolonema iberomarrocanum LEGE 07170",
 "Almyronema epifaneia S6",
 "Vasconcelosia minhoensis LEGE 07310",
 "Leptothoe kymatousa TAU-MAC 1615",
 "Leptothoe spongobia TAU-MAC 1115",
 "Adonisia turfae CCMR0081",
 "Leptolyngbya cf. ectocarpi LEGE 11479",
 "Leptolyngbya iicbica LK",
 "Leptolyngbya subtilissima DQ-A4",
 "Halomicronema hongdechloris C2206",
 "Limnothrix redekei LRLZ20PSL1",
 "Prochlorothrix hollandica PCC 9006 = CALU 1027",
 "Parasynechococcus marenigrum (strain WH8102)",
 "Aphanothece stagnina RSMan2012",
 "Aphanothece cf. minutissima CCALA 015",
 "Desertifilum tharense IPPAS B-1220",
 "Roseofilum casamattae BLCC-M143",
 "Roseofilum reptotaenium AO1-A",
 "Roseofilum acuticapitatum BLCC-
… (잘림 — 원본 파일 참조)
```

## dropped_tips

```json
[
 "Thermostichus vulcanus str. Rupite"
]
```

## reduced_lineages

```json
[
 "Atelocyanobacterium thalassa (isolate ALOHA)"
]
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
 "reconstruction": 0.9863,
 "clade_frequency": 0.9797
}
```

## tip_completeness

```json
{
 "Gloeobacter kilaueensis (strain ATCC BAA-2537 / CCAP 1431/1 / ULC 316 / JS1)": 0.94,
 "Gloeobacter violaceus (strain ATCC 29082 / PCC 7421)": 0.947,
 "Gloeobacter morelensis MG652769": 0.94,
 "Gloeomargarita lithophora Alchichica-D10": 0.893,
 "Tumidithrix elongata BACA0141": 0.973,
 "Pseudanabaena cinerea FACHB-1277": 0.96,
 "Pseudanabaena galeata UHCC 0370": 0.98,
 "Pseudanabaena yagii GIHE-NHR1": 0.973,
 "Pseudocalidococcus azoricus BACA0444": 0.94,
 "Candidatus Synechococcus calcipolaris G9": 0.933,
 "Parathermosynechococcus lividus PCC 6715": 0.867,
 "Thermosynechococcus vestitus (strain NIES-2133 / IAM M-273 / BP-1)": 0.927,
 "Thermosynechococcus sichuanensis E542": 0.9,
 "Acaryochloris thomasi RCC1774": 0.973,
 "Lyngbya confervoides BDU141951": 0.967,
 "Neosynechococcus sphagnicola sy1": 0.74,
 "Romeriopsis navalis LEGE 11480": 0.98,
 "Leptolyngbya boryana NIES-2135": 1.0,
 "Myxacorys almedinensis A": 0.987,
 "Thermocoleostomius sinensis A174": 0.98,
 "Thermoleptolyngbya sichuanensis A183": 0.987,
 "Vacuolonema iberomarrocanum LEGE 07170": 0.987,
 "Almyronema epifaneia S6": 0.9,
 "Vasconcelosia minhoensis LEGE 07310": 0.973,
 "Leptothoe kymatousa TAU-MAC 1615": 0.873,
 "Leptothoe spongobia TAU-MAC 1115": 0.887,
 "Adonisia turfae CCMR0081": 1.0,
 "Leptolyngbya cf. ectocarpi LEGE 11479": 0.98,
 "Leptolyngbya iicbica LK": 0.98,
 "Leptolyngbya subtilissima DQ-A4": 0.98,
 "Halomicronema hongdechloris C2206": 0.94,
 "Limnothrix redekei LRLZ20PSL1": 0.967,
 "Prochlorothrix hollandica PCC 9006 = CALU 1027": 0.907,
 "Parasynechococcus marenigrum (strain WH8102)": 0.84,
 "
… (잘림 — 원본 파일 참조)
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
  417
 ],
 [
  "uncharacterised",
  143
 ],
 [
  "transferase activity",
  123
 ],
 [
  "oxidoreductase activity",
  80
 ],
 [
  "hydrolase activity",
  79
 ],
 [
  "helicase_nucleic",
  74
 ],
 [
  "organelle",
  73
 ],
 [
  "DNA binding",
  53
 ],
 [
  "methyl_glyco_transferase",
  52
 ],
 [
  "kinase",
  51
 ],
 [
  "catalytic activity, acting on RNA",
  49
 ],
 [
  "protease",
  46
 ],
 [
  "structural molecule activity",
  44
 ],
 [
  "ligase activity",
  43
 ],
 [
  "amino acid metabolic process",
  41
 ],
 [
  "ribosome",
  41
 ],
 [
  "transporter_channel",
  38
 ],
 [
  "carbohydrate metabolic process",
  35
 ],
 [
  "carbohydrate derivative metabolic process",
  34
 ],
 [
  "RNA binding",
  33
 ]
]
```

## top_families

```json
[
 {
  "family": "LytR_cpsA_psr",
  "description": "LytR_cpsA_psr family",
  "posterior": 1.0,
  "model_sd": 0.0,
  "tree_sd": 0.0,
  "share_of_clade_tips_today": 0.981
 },
 {
  "family": "SecD_SecF_C",
  "description": "Protein export membrane protein SecD/SecF, C-terminal",
  "posterior": 1.0,
  "model_sd": 0.0,
  "tree_sd": 0.0,
  "share_of_clade_tips_today": 0.981
 },
 {
  "family": "Trigger_C",
  "description": "Bacterial trigger factor protein (TF) C-terminus",
  "posterior": 1.0,
  "model_sd": 0.0,
  "tree_sd": 0.0,
  "share_of_clade_tips_today": 0.988
 },
 {
  "family": "RecJ_OB",
  "description": "RecJ OB domain",
  "posterior": 1.0,
  "model_sd": 0.0,
  "tree_sd": 0.0,
  "share_of_clade_tips_today": 0.994
 },
 {
  "family": "Val_tRNA-synt_C",
  "description": "Valyl tRNA synthetase tRNA binding arm",
  "posterior": 1.0,
  "model_sd": 0.0,
  "tree_sd": 0.0,
  "share_of_clade_tips_today": 0.975
 },
 {
  "family": "RelA_SpoT",
  "description": "Region found in RelA / SpoT proteins",
  "posterior": 1.0,
  "model_sd": 0.0,
  "tree_sd": 0.0,
  "share_of_clade_tips_today": 0.981
 },
 {
  "family": "RelA_RIS",
  "description": "RelA/SpoT RIS domain",
  "posterior": 1.0,
  "model_sd": 0.0,
  "tree_sd": 0.0,
  "share_of_clade_tips_today": 0.981
 },
 {
  "family": "TrmE_N",
  "description": "GTP-binding protein TrmE N-terminus",
  "posterior": 1.0,
  "model_sd": 0.0,
  "tree_sd": 0.0,
  "share_of_clade_tips_today": 1.0
 },
 {
  "family": "Ribosomal_S21",
  "description": "Ribosomal protein S21",
  "posterior": 1.0,
  "model_sd": 0.0,
  "tree_sd": 0.0,
  "share_of_clade_tips_
… (잘림 — 원본 파일 참조)
```

## uncertain_families

```json
[
 {
  "family": "Alpha-E",
  "description": "A predicted alpha-helical domain with a conserved ER motif.",
  "posterior": 0.9,
  "model_sd": 0.0,
  "tree_sd": 0.0
 },
 {
  "family": "SHOCT",
  "description": "Short C-terminal domain",
  "posterior": 0.899,
  "model_sd": 0.0,
  "tree_sd": 0.0
 },
 {
  "family": "CheB_methylest",
  "description": "CheB methylesterase",
  "posterior": 0.899,
  "model_sd": 0.0,
  "tree_sd": 0.0
 },
 {
  "family": "Cas_Cas1",
  "description": "CRISPR associated protein Cas1",
  "posterior": 0.899,
  "model_sd": 0.0,
  "tree_sd": 0.0
 },
 {
  "family": "MgtC",
  "description": "MgtC family",
  "posterior": 0.898,
  "model_sd": 0.0,
  "tree_sd": 0.0
 },
 {
  "family": "HTH_24",
  "description": "Winged helix-turn-helix DNA-binding",
  "posterior": 0.898,
  "model_sd": 0.0,
  "tree_sd": 0.0
 },
 {
  "family": "AMP-dom_DIP2-like",
  "description": "Disco-interacting protein 2-like, AMP domain",
  "posterior": 0.898,
  "model_sd": 0.0,
  "tree_sd": 0.0
 },
 {
  "family": "CP_ATPgrasp_2",
  "description": "Circularly permuted ATP-grasp type 2",
  "posterior": 0.898,
  "model_sd": 0.0,
  "tree_sd": 0.0
 },
 {
  "family": "PIN_3",
  "description": "PIN domain",
  "posterior": 0.897,
  "model_sd": 0.0,
  "tree_sd": 0.0
 },
 {
  "family": "CRISPR_Cas2",
  "description": "CRISPR associated protein Cas2",
  "posterior": 0.897,
  "model_sd": 0.0,
  "tree_sd": 0.0
 },
 {
  "family": "HHH",
  "description": "Helix-hairpin-helix motif",
  "posterior": 0.896,
  "model_sd": 0.0,
  "tree_sd": 0.0
 },
 {
  "family": "Zn_ribbon_Top1",
  "description": "Topoisomeras
… (잘림 — 원본 파일 참조)
```

## clade_node_children

```json
[
 {
  "n_clade_tips": 159,
  "examples": [
   "Acaryochloris thomasi RCC1774",
   "Adonisia turfae CCMR0081",
   "Aerosakkonema funiforme FACHB-1375",
   "Aetokthonos hydrillicola (strain Thurmond2011)",
   "Aliterella atlantica CENA595",
   "Allocoleopsis franciscana PCC 7113"
  ],
  "n_confident": 1910,
  "sum_of_posteriors": 2498.5
 },
 {
  "n_clade_tips": 3,
  "examples": [
   "Gloeobacter kilaueensis (strain ATCC BAA-2537 / CCAP 1431/1 / ULC 316 / JS1)",
   "Gloeobacter morelensis MG652769",
   "Gloeobacter violaceus (strain ATCC 29082 / PCC 7421)"
  ],
  "n_confident": 2121,
  "sum_of_posteriors": 2398.9
 }
]
```

## extra_nodes

```json
{
 "g__Gloeomargarita": {
  "n_tips_below": 1,
  "examples": [
   "Gloeomargarita lithophora Alchichica-D10"
  ],
  "n_confident": 1979,
  "sum_of_posteriors": 2177.8
 },
 "^g__Gloeomargarita": {
  "n_tips_below": 159,
  "examples": [
   "Acaryochloris thomasi RCC1774",
   "Adonisia turfae CCMR0081",
   "Aerosakkonema funiforme FACHB-1375",
   "Aetokthonos hydrillicola (strain Thurmond2011)",
   "Aliterella atlantica CENA595",
   "Allocoleopsis franciscana PCC 7113",
   "Almyronema epifaneia S6",
   "Amazonocrinis nigriterrae CENA67"
  ],
  "n_confident": 1910,
  "sum_of_posteriors": 2498.5
 }
}
```

## 연결
- [[실험 목록]]
