---
유형: 실험
실행: clade_ancestor/fungi
산출: results/clade_ancestor/fungi/summary.json
tags:
  - 유형/실험
  - 실험/clade_ancestor-fungi
---

# 실험 · clade_ancestor-fungi

**산출물** `results/clade_ancestor/fungi/summary.json`

## 한눈에

| 항목 | 값 |
| --- | --- |
| clade | fungi |
| tips | 334 |
| clade_tips | 289 |
| families_considered | 9457 |
| rooted_on | Leishmania enriettii |
| root_split_intruders | None |
| node_reconstructed | most recent common ancestor of the sampled clade tips, which at this sample size is not the clade's root (see results/sample_size/summary.json) |
| n_models | 5 |
| n_bootstrap_trees | 0 |
| completeness_model | True |
| reduced_branch_multiplier | False |
| n_confident_families | 3659 |
| n_uncertain_families | 515 |
| size_not_reported | the simulation showed a 16-17% underestimate of ancestor size at this sample size, so no family count is quoted |

## clade_species

```json
[
 "Rozella allomycis (strain CSF55)",
 "Mitosporidium daphniae",
 "Paramicrosporidium saccamoebae",
 "Caulochytrium protostelioides",
 "Gonapodya prolifera (strain JEL478) (Monoblepharis prolifera)",
 "Clydaea vesicula",
 "Synchytrium endobioticum",
 "Synchytrium microbalum",
 "Polyrhizophydium stewartii",
 "Batrachochytrium dendrobatidis (strain JAM81 / FGSC 10211) (Frog chytrid fungus)",
 "Batrachochytrium salamandrivorans",
 "Blyttiomyces helicus",
 "Rhizophlyctis rosea",
 "Spizellomyces punctatus (strain DAOM BR117)",
 "Geranomyces variabilis",
 "Powellomyces hirtus",
 "Rhizoclosmatium globosum",
 "Chytriomyces confervae",
 "Physocladia obscura",
 "Anaeromyces robustus",
 "Piromyces finnis",
 "Allomyces macrogynus (strain ATCC 38327) (Allomyces javanicus var. macrogynus)",
 "Catenaria anguillulae PL171",
 "Bifiguratus adelaidae",
 "Lichtheimia ornata",
 "Rhizopus delemar",
 "Rhizopus oryzae (Mucormycosis agent) (Rhizopus arrhizus var. delemar)",
 "Mortierella isabellina (Filamentous fungus) (Umbelopsis isabellina)",
 "Umbelopsis ramanniana AG",
 "Umbelopsis vinacea",
 "Olpidium bornovanus",
 "Jimgerdemannia flammicorona",
 "Linnemannia elongata AG-77",
 "Linnemannia gamsii",
 "Basidiobolus meristosporus CBS 931.73",
 "Basidiobolus ranarum",
 "Glomus cerebriforme",
 "Funneliformis geosporum",
 "Rhizophagus clarus",
 "Gigaspora margarita",
 "Gigaspora rosea",
 "Ambispora gerdemannii",
 "Ambispora leptoticha",
 "Paraglomus brasilianum",
 "Paraglomus occultum",
 "Piptocephalis cylindrospora",
 "Syncephalis pseudoplumigaleata",
 "Thamnocephalis sphaerospora",
 "Conidiobolus
… (잘림 — 원본 파일 참조)
```

## dropped_tips

```json
[
 "Saccharomyces cerevisiae (strain ATCC 204508 / S288c) (Bakers yeast)"
]
```

## reduced_lineages

```json
[
 "Mitosporidium daphniae",
 "Paramicrosporidium saccamoebae",
 "Olpidium bornovanus",
 "Piptocephalis cylindrospora"
]
```

## misplaced_clade_tips_left_out

```json
[
 "Astathelohania contejeani",
 "Hamiltosporidium tvaerminnensis"
]
```

## non_clade_tips_inside_clade_node

```json
[]
```

## leave_tips_out_auroc

```json
{
 "reconstruction": 0.9721,
 "clade_frequency": 0.95
}
```

## tip_completeness

```json
{
 "Rozella allomycis (strain CSF55)": 0.707,
 "Mitosporidium daphniae": 0.52,
 "Paramicrosporidium saccamoebae": 0.6,
 "Caulochytrium protostelioides": 0.853,
 "Gonapodya prolifera (strain JEL478) (Monoblepharis prolifera)": 0.92,
 "Clydaea vesicula": 0.867,
 "Synchytrium endobioticum": 0.913,
 "Synchytrium microbalum": 0.947,
 "Polyrhizophydium stewartii": 0.96,
 "Batrachochytrium dendrobatidis (strain JAM81 / FGSC 10211) (Frog chytrid fungus)": 0.887,
 "Batrachochytrium salamandrivorans": 0.913,
 "Blyttiomyces helicus": 0.68,
 "Rhizophlyctis rosea": 0.913,
 "Spizellomyces punctatus (strain DAOM BR117)": 1.0,
 "Geranomyces variabilis": 0.973,
 "Powellomyces hirtus": 0.987,
 "Rhizoclosmatium globosum": 0.933,
 "Chytriomyces confervae": 0.94,
 "Physocladia obscura": 0.92,
 "Anaeromyces robustus": 0.767,
 "Piromyces finnis": 0.74,
 "Allomyces macrogynus (strain ATCC 38327) (Allomyces javanicus var. macrogynus)": 0.9,
 "Catenaria anguillulae PL171": 0.86,
 "Bifiguratus adelaidae": 0.88,
 "Lichtheimia ornata": 1.0,
 "Rhizopus delemar": 1.0,
 "Rhizopus oryzae (Mucormycosis agent) (Rhizopus arrhizus var. delemar)": 1.0,
 "Mortierella isabellina (Filamentous fungus) (Umbelopsis isabellina)": 0.987,
 "Umbelopsis ramanniana AG": 0.973,
 "Umbelopsis vinacea": 0.993,
 "Olpidium bornovanus": 0.587,
 "Jimgerdemannia flammicorona": 0.913,
 "Linnemannia elongata AG-77": 1.0,
 "Linnemannia gamsii": 1.0,
 "Basidiobolus meristosporus CBS 931.73": 0.987,
 "Basidiobolus ranarum": 0.973,
 "Glomus cerebriforme": 0.973,
 "Funneliformis geosporum": 0.967,
 "Rhizophagus clarus": 0.973,
 "Gigaspora
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
  508
 ],
 [
  "organelle",
  290
 ],
 [
  "transferase activity",
  167
 ],
 [
  "helicase_nucleic",
  131
 ],
 [
  "repeat_domain",
  121
 ],
 [
  "hydrolase activity",
  120
 ],
 [
  "nucleus",
  107
 ],
 [
  "uncharacterised",
  102
 ],
 [
  "protease",
  100
 ],
 [
  "oxidoreductase activity",
  83
 ],
 [
  "DNA binding",
  82
 ],
 [
  "structural molecule activity",
  82
 ],
 [
  "methyl_glyco_transferase",
  80
 ],
 [
  "zinc_finger",
  78
 ],
 [
  "kinase",
  77
 ],
 [
  "ribosome",
  69
 ],
 [
  "RNA binding",
  67
 ],
 [
  "catalytic activity, acting on RNA",
  64
 ],
 [
  "catalytic activity, acting on a protein",
  64
 ],
 [
  "transporter_channel",
  64
 ]
]
```

## top_families

```json
[
 {
  "family": "Biopterin_H",
  "description": "Biopterin-dependent aromatic amino acid hydroxylase",
  "posterior": 1.0,
  "model_sd": 0.0,
  "tree_sd": 0.0,
  "share_of_clade_tips_today": 0.173
 },
 {
  "family": "DTW",
  "description": "DTW domain",
  "posterior": 1.0,
  "model_sd": 0.0,
  "tree_sd": 0.0,
  "share_of_clade_tips_today": 0.194
 },
 {
  "family": "DUF2039",
  "description": "Uncharacterized conserved protein (DUF2039)",
  "posterior": 1.0,
  "model_sd": 0.0,
  "tree_sd": 0.0,
  "share_of_clade_tips_today": 0.187
 },
 {
  "family": "Pus10_C",
  "description": "Pus10, C-terminal",
  "posterior": 1.0,
  "model_sd": 0.0,
  "tree_sd": 0.0,
  "share_of_clade_tips_today": 0.173
 },
 {
  "family": "FancD2",
  "description": "Fanconi anaemia protein FancD2 nuclease",
  "posterior": 1.0,
  "model_sd": 0.0,
  "tree_sd": 0.0,
  "share_of_clade_tips_today": 0.18
 },
 {
  "family": "MCM_bind",
  "description": "Mini-chromosome maintenance replisome factor",
  "posterior": 1.0,
  "model_sd": 0.0,
  "tree_sd": 0.0,
  "share_of_clade_tips_today": 0.464
 },
 {
  "family": "WHD_MCM2",
  "description": "DNA replication licensing factor MCM2-like, winged-helix domain",
  "posterior": 1.0,
  "model_sd": 0.0,
  "tree_sd": 0.0,
  "share_of_clade_tips_today": 0.443
 },
 {
  "family": "tRNA_synt_1c_R1",
  "description": "Glutaminyl-tRNA synthetase, non-specific RNA binding region part 1",
  "posterior": 1.0,
  "model_sd": 0.0,
  "tree_sd": 0.0,
  "share_of_clade_tips_today": 0.592
 },
 {
  "family": "MCD",
  "description": "Malonyl-CoA decarboxylase C-terminal domain",
  "posterio
… (잘림 — 원본 파일 참조)
```

## uncertain_families

```json
[
 {
  "family": "PIG-H",
  "description": "GPI-GlcNAc transferase complex, PIG-H component",
  "posterior": 0.899,
  "model_sd": 0.0,
  "tree_sd": 0.0
 },
 {
  "family": "YBD",
  "description": "YAP binding domain",
  "posterior": 0.899,
  "model_sd": 0.0,
  "tree_sd": 0.0
 },
 {
  "family": "Hyccin",
  "description": "Hyccin",
  "posterior": 0.899,
  "model_sd": 0.0,
  "tree_sd": 0.0
 },
 {
  "family": "STI1-HOP_DP",
  "description": "STI1/HOP, DP domain",
  "posterior": 0.899,
  "model_sd": 0.0,
  "tree_sd": 0.0
 },
 {
  "family": "OB_RRP5_4th",
  "description": "RRP5 OB-fold domain",
  "posterior": 0.898,
  "model_sd": 0.0,
  "tree_sd": 0.0
 },
 {
  "family": "fn3",
  "description": "Fibronectin type III domain",
  "posterior": 0.898,
  "model_sd": 0.0,
  "tree_sd": 0.0
 },
 {
  "family": "XRN1_D1",
  "description": "Exoribonuclease Xrn1 D1 domain",
  "posterior": 0.898,
  "model_sd": 0.0,
  "tree_sd": 0.0
 },
 {
  "family": "CHIP_TPR_N",
  "description": "CHIP N-terminal tetratricopeptide repeat domain",
  "posterior": 0.897,
  "model_sd": 0.0,
  "tree_sd": 0.0
 },
 {
  "family": "WLM",
  "description": "WLM domain",
  "posterior": 0.897,
  "model_sd": 0.0,
  "tree_sd": 0.0
 },
 {
  "family": "Sec66",
  "description": "Preprotein translocase subunit Sec66",
  "posterior": 0.896,
  "model_sd": 0.0,
  "tree_sd": 0.0
 },
 {
  "family": "Glyco_trans_1_4",
  "description": "Glycosyl transferases group 1",
  "posterior": 0.896,
  "model_sd": 0.0,
  "tree_sd": 0.0
 },
 {
  "family": "Far-17a_AIG1",
  "description": "FAR-17a/AIG1-like protein",
  "posterior": 0.895,
  "model_s
… (잘림 — 원본 파일 참조)
```

## clade_node_children

```json
[
 {
  "n_clade_tips": 286,
  "examples": [
   "Acaromyces ingoldii",
   "Allomyces macrogynus (strain ATCC 38327) (Allomyces javanicus var. macrogynus)",
   "Ambispora gerdemannii",
   "Ambispora leptoticha",
   "Anaeromyces robustus",
   "Anthostomella pinea"
  ],
  "n_confident": 3885,
  "sum_of_posteriors": 4376.4
 },
 {
  "n_clade_tips": 3,
  "examples": [
   "Mitosporidium daphniae",
   "Paramicrosporidium saccamoebae",
   "Rozella allomycis (strain CSF55)"
  ],
  "n_confident": 3223,
  "sum_of_posteriors": 4142.5
 }
]
```

## 연결
- [[실험 목록]]
