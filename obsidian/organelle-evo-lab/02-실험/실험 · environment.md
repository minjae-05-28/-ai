---
유형: 실험
실행: environment
산출: results/environment/metrics.json
tags:
  - 유형/실험
  - 실험/environment
---

# 실험 · environment

**산출물** `results/environment/metrics.json`

## pairs

```json
[
 "Shewanella oneidensis -> Shewanella frigidimarina",
 "Shewanella oneidensis -> Colwellia psychrerythraea",
 "Acinetobacter baylyi -> Psychrobacter arcticus",
 "Bacillus subtilis -> Planococcus halocryophilus",
 "Bacillus subtilis -> Geobacillus kaustophilus",
 "Bacillus subtilis -> Lactiplantibacillus plantarum",
 "Flavobacterium johnsoniae -> Psychroflexus torquis",
 "Rhodothermus marinus -> Salinibacter ruber",
 "Thermus thermophilus -> Deinococcus radiodurans",
 "Micrococcus luteus -> Kineococcus radiotolerans",
 "Synechocystis sp. PCC 6803 -> Chroococcidiopsis thermalis",
 "Synechococcus elongatus -> Prochlorococcus marinus",
 "Cereibacter sphaeroides -> Candidatus Pelagibacter ubique",
 "Nitratidesulfovibrio vulgaris -> Desulfotalea psychrophila",
 "Myxococcus xanthus -> Geobacter sulfurreducens",
 "Methanosarcina acetivorans -> Methanococcoides burtonii",
 "Methanosarcina acetivorans -> Halobacterium salinarum",
 "Methanosarcina acetivorans -> Haloferax volcanii",
 "Methanococcus maripaludis -> Methanocaldococcus jannaschii",
 "Bacillus subtilis -> Bacillus licheniformis",
 "Pseudomonas aeruginosa -> Pseudomonas putida"
]
```

## designs

```json
{
 "Shewanella frigidimarina": [
  1.0,
  0.3333333333333333,
  0.2,
  0.0,
  0.0,
  0.0
 ],
 "Colwellia psychrerythraea": [
  1.0,
  0.7333333333333333,
  0.2,
  0.0,
  0.0,
  0.0
 ],
 "Psychrobacter arcticus": [
  1.0,
  0.26666666666666666,
  0.15,
  0.0,
  0.0,
  0.0
 ],
 "Planococcus halocryophilus": [
  1.0,
  0.4,
  0.45,
  0.0,
  0.0,
  0.0
 ],
 "Geobacillus kaustophilus": [
  1.0,
  -0.7666666666666667,
  0.0,
  0.0,
  0.0,
  0.0
 ],
 "Lactiplantibacillus plantarum": [
  1.0,
  0.23333333333333334,
  0.0,
  1.0,
  0.0,
  0.0
 ],
 "Psychroflexus torquis": [
  1.0,
  0.6,
  0.35,
  0.0,
  0.0,
  0.0
 ],
 "Salinibacter ruber": [
  1.0,
  0.8333333333333334,
  2.3,
  0.0,
  0.0,
  0.0
 ],
 "Deinococcus radiodurans": [
  1.0,
  1.3333333333333333,
  0.0,
  0.0,
  1.0,
  0.0
 ],
 "Kineococcus radiotolerans": [
  1.0,
  0.06666666666666667,
  -0.05,
  0.0,
  1.0,
  0.0
 ],
 "Chroococcidiopsis thermalis": [
  1.0,
  0.0,
  0.0,
  0.0,
  1.0,
  0.0
 ],
 "Prochlorococcus marinus": [
  1.0,
  0.2,
  0.35,
  0.0,
  0.0,
  1.0
 ],
 "Candidatus Pelagibacter ubique": [
  1.0,
  0.3333333333333333,
  0.3,
  0.0,
  0.0,
  1.0
 ],
 "Desulfotalea psychrophila": [
  1.0,
  0.9,
  0.25,
  0.0,
  0.0,
  0.0
 ],
 "Geobacter sulfurreducens": [
  1.0,
  0.0,
  0.0,
  1.0,
  0.0,
  0.0
 ],
 "Methanococcoides burtonii": [
  1.0,
  0.4666666666666667,
  0.0,
  0.0,
  0.0,
  0.0
 ],
 "Halobacterium salinarum": [
  1.0,
  -0.16666666666666666,
  2.3,
  -1.0,
  1.0,
  0.0
 ],
 "Haloferax volcanii": [
  1.0,
  -0.16666666666666666,
  1.3,
  -1.0,
  0.0,
  0.0
 ],
 "Methanocaldococcus jannaschii": [
  1.0,
  -1.6,
  0.1,
  0.0,
  0.0,
  0.0
 ],
 "Bacillus licheniformis": [
  1.0,
  -0.1,
  0.0,
  0.0,
  0.0,
  0.0
 ],
 "Pseudomonas putida": [
  1.0,
  0.23333333333333334,
  0.0,
  0.0,
  0.0,
  0.0
 ]
}
```

## mean_heldout_auroc

```json
{
 "copies_only": 0.6143217102181643,
 "no_environment": 0.8156591797831733,
 "environment_law": 0.8079995318827699,
 "memorisation": 0.8041923336615406
}
```

## env_vs_none

```json
{
 "mean": -0.007659647900403474,
 "n_better": 8,
 "n": 19
}
```

## heldout

```json
[
 {
  "pair": "Shewanella oneidensis -> Shewanella frigidimarina",
  "design": [
   1.0,
   0.3333333333333333,
   0.2,
   0.0,
   0.0,
   0.0
  ],
  "copies_only": 0.6256721917137704,
  "memorisation": 0.8545849006631397,
  "no_environment": 0.8199775042074843,
  "environment_law": 0.8246518348654611
 },
 {
  "pair": "Shewanella oneidensis -> Colwellia psychrerythraea",
  "design": [
   1.0,
   0.7333333333333333,
   0.2,
   0.0,
   0.0,
   0.0
  ],
  "copies_only": 0.6304542700437961,
  "memorisation": 0.77062361981032,
  "no_environment": 0.836432701329531,
  "environment_law": 0.8419543698147172
 },
 {
  "pair": "Acinetobacter baylyi -> Psychrobacter arcticus",
  "design": [
   1.0,
   0.26666666666666666,
   0.15,
   0.0,
   0.0,
   0.0
  ],
  "copies_only": 0.6140806592934253,
  "memorisation": 0.7826662699003124,
  "no_environment": 0.8553497330093075,
  "environment_law": 0.8570368166112847
 },
 {
  "pair": "Bacillus subtilis -> Planococcus halocryophilus",
  "design": [
   1.0,
   0.4,
   0.45,
   0.0,
   0.0,
   0.0
  ],
  "copies_only": 0.641160799890426,
  "memorisation": 0.8694044194859152,
  "no_environment": 0.8700588960416381,
  "environment_law": 0.8737620417294435
 },
 {
  "pair": "Bacillus subtilis -> Geobacillus kaustophilus",
  "design": [
   1.0,
   -0.7666666666666667,
   0.0,
   0.0,
   0.0,
   0.0
  ],
  "copies_only": 0.625025833144228,
  "memorisation": 0.8596953816416507,
  "no_environment": 0.8423175268259474,
  "environment_law": 0.8160224251953189
 },
 {
  "pair": "Bacillus subtilis -> Lactiplantibacillus plantarum",
  "design": [
   1.0,
   0.23333333333333334,
   0.0,
   1.0,
   0.0,
   0.0
  ],
  "copies_only": 0.6513205313852461,
  "memorisation": 0.7977138313104032,
  "no_environment": 0.8416240929354724,
  "environment_law": 0.8350403501350427
 },
 {
  "pair": "Flavobacterium johnsoniae -> Psychroflexus torquis",
  "design": [
   1.0,
   0.6,
   0.35,
   0.0,
   0.0,
   0.0
  ],
  "copies_only": 0.6134243490031177,
  "memorisation": 0.8033770289911352,
  "no_environment": 0.8280913337253553,
  "environment_law": 0.8349746480123376
 },
 {
  "pair": "Rhodothermus marinus -> Salinibacter ruber",
  "design": [
   1.0,
   0.8333333333333334,
   2.3,
   0.0,
   0.0,
   0.0
  ],
  "copies_only": 0.6300849300067235,
  "memorisation": 0.8177683679508497,
  "no_environment": 0.8345656471308192,
  "environment_law": 0.8013445070275101
 },
 {
  "pair": "Thermus thermophilus -> Deinococcus radiodurans",
  "design": [
   1.0,
   1.3333333333333333,
   0.0,
   0.0,
   1.0,
   0.0
  ],
  "copies_only": 0.6221328354041603,
  "memorisation": 0.7916471799525339,
  "no_environment": 0.8360097026385592,
  "environment_law": 0.822752338405696
 },
 {
  "pair": "Micrococcus luteus -> Kineococcus radiotolerans",
  "design": [
   1.0,
   0.06666666666666667,
   -0.05,
   0.0,
   1.0,
   0.0
  ],
  "copies_only": 0.6025538779197316,
  "memorisation": 0.786260162601626,
  "no_environment": 0.7923809523809524,
  "environment_law": 0.7885585236804749
 },
 {
  "pair": "Synechocystis sp. PCC 6803 -> Chroococcidiopsis thermalis",
  "design": [
   1.0,
   0.0,
   0.0,
   0.0,
   1.0,
   0.0
  ],
  "copies_only": 0.6128082682613423,
  "memorisation": 0.8115887862014431,
  "no_environment": 0.8059114609073836,
  "environment_law": 0.8001600029653059
 },
 {
  "pair": "Synechococcus elongatus -> Prochlorococcus marinus",
  "design": [
   1.0,
   0.2,
   0.35,
   0.0,
   0.0,
   1.0
  ],
  "copies_only": 0.5774197206830628,
  "memorisation": 0.7598321686126682,
  "no_environment": 0.7917994304209917,
  "environment_law": 0.7734366280346644
 },
 {
  "pair": "Cereibacter sphaeroides -> Candidatus Pelagibacter ubique",
  "design": [
   1.0,
   0.3333333333333333,
   0.3,
   0.0,
   0.0,
   1.0
  ],
  "copies_only": 0.6059059693903209,
  "memorisation": 0.8019856059632438,
  "no_environment": 0.8237177517140415,
  "environment_law": 0.831744550549555
 },
 {
  "pair": "Nitratidesulfovibrio vulgaris -> Desulfotalea psychrophila",
  "design": [
   1.0,
   0.9,
   0.25,
   0.0,
   0.0,
   0.0
  ],
  "copies_only": 0.6445834877033273,
  "memorisation": 0.7866468852545782,
  "no_environment": 0.844799715959211,
  "environment_law": 0.8521708831727886
 },
 {
  "pair": "Myxococcus xanthus -> Geobacter sulfurreducens",
  "design": [
   1.0,
   0.0,
   0.0,
   1.0,
   0.0,
   0.0
  ],
  "copies_only": 0.6153687586486739,
  "memorisation": 0.7772209968127795,
  "no_environment": 0.8559924255823874,
  "environment_law": 0.853099129843691
 },
 {
  "pair": "Methanosarcina acetivorans -> Methanococcoides burtonii",
  "design": [
   1.0,
   0.4666666666666667,
   0.0,
   0.0,
   0.0,
   0.0
  ],
  "copies_only": 0.5879022613611655,
  "memorisation": 0.7833501848227875,
  "no_environment": 0.7478451837355947,
  "environment_law": 0.7418634485757774
 },
 {
  "pair": "Methanosarcina acetivorans -> Halobacterium salinarum",
  "design": [
   1.0,
   -0.16666666666666666,
   2.3,
   -1.0,
   1.0,
   0.0
  ],
  "copies_only": 0.5851809733772395,
  "memorisation": 0.8841982300329296,
  "no_environment": 0.7890454945024279,
  "environment_law": 0.7396126932522186
 },
 {
  "pair": "Methanosarcina acetivorans -> Haloferax volcanii",
  "design": [
   1.0,
   -0.16666666666666666,
   1.3,
   -1.0,
   0.0,
   0.0
  ],
  "copies_only": 0.5955471194787872,
  "memorisation": 0.8935135140086917,
  "no_environment": 0.8053073997259089,
  "environment_law": 0.7720170610695415
 },
 {
  "pair": "Methanococcus maripaludis -> Methanocaldococcus jannaschii",
  "design": [
   1.0,
   -1.6,
   0.1,
   0.0,
   0.0,
   0.0
  ],
  "copies_only": 0.5914856574365777,
  "memorisation": 0.6475768055522657,
  "no_environment": 0.676297463107279,
  "environment_law": 0.6917888528317976
 }
]
```

## significant_effects

```json
{
 "loss_colder": [
  [
   "go:organelle",
   1.0,
   0.0
  ],
  [
   "go:structural molecule activity",
   -0.8,
   0.0
  ],
  [
   "redox_core",
   0.709,
   0.0
  ],
  [
   "transcription",
   0.671,
   0.0
  ],
  [
   "kw:zinc_finger",
   0.545,
   0.0
  ],
  [
   "kw:lipid_metabolism",
   -0.469,
   0.0
  ],
  [
   "kw:cilium_flagellum",
   0.465,
   0.0
  ],
  [
   "kw:cell_adhesion_surface",
   -0.382,
   0.0
  ],
  [
   "go:ligase activity",
   -0.368,
   0.0
  ],
  [
   "atp_synthase",
   0.323,
   0.0
  ]
 ],
 "loss_saltier": [
  [
   "transcription",
   0.692,
   0.0
  ],
  [
   "go:organelle",
   0.55,
   0.0
  ],
  [
   "protein_targeting",
   -0.447,
   0.0
  ],
  [
   "kw:cilium_flagellum",
   -0.444,
   0.0
  ],
  [
   "go:catalytic activity, acting on DNA",
   -0.4,
   0.0
  ],
  [
   "kw:transporter_channel",
   -0.308,
   0.0
  ],
  [
   "kw:zinc_finger",
   0.29,
   0.0
  ],
  [
   "kw:cytoskeleton_motor",
   0.274,
   0.0
  ],
  [
   "go:isomerase activity",
   0.175,
   0.0
  ],
  [
   "go:catalytic activity",
   0.169,
   0.0
  ]
 ],
 "loss_anaerobic": [
  [
   "kw:cilium_flagellum",
   1.449,
   0.0
  ],
  [
   "atp_synthase",
   -0.997,
   0.0
  ],
  [
   "go:ribosome",
   0.787,
   0.0
  ],
  [
   "transcription",
   0.743,
   0.0
  ],
  [
   "go:organelle",
   0.725,
   0.0
  ],
  [
   "kw:gtpase_signalling",
   -0.67,
   0.0
  ],
  [
   "go:carbohydrate metabolic process",
   -0.655,
   0.0
  ],
  [
   "kw:cell_adhesion_surface",
   -0.514,
   0.0
  ],
  [
   "redox_core",
   0.446,
   0.0
  ],
  [
   "kw:cytoskeleton_motor",
   -0.443,
   0.0
  ]
 ],
 "loss_radiation_resistant": [
  [
   "kw:cilium_flagellum",
   2.071,
   0.0
  ],
  [
   "kw:cell_adhesion_surface",
   1.106,
   0.0
  ],
  [
   "kw:ubiquitin_system",
   0.825,
   0.0
  ],
  [
   "go:structural molecule activity",
   -0.744,
   0.0
  ],
  [
   "protein_targeting",
   -0.742,
   0.0
  ],
  [
   "redox_core",
   -0.699,
   0.0
  ],
  [
   "kw:cytoskeleton_motor",
   -0.639,
   0.0
  ],
  [
   "transcription",
   -0.559,
   0.0
  ],
  [
   "kw:amino_acid_metabolism",
   -0.544,
   0.0
  ],
  [
   "go:ligase activity",
   -0.421,
   0.0
  ]
 ],
 "loss_oligotrophic": [
  [
   "kw:cilium_flagellum",
   3.336,
   0.0
  ],
  [
   "protein_targeting",
   -2.137,
   0.0
  ],
  [
   "go:ribosome",
   -1.574,
   0.0
  ],
  [
   "transcription",
   -1.113,
   0.0
  ],
  [
   "kw:gtpase_signalling",
   0.846,
   0.0
  ],
  [
   "go:catalytic activity, acting on DNA",
   0.639,
   0.0
  ],
  [
   "kw:repeat_domain",
   0.564,
   0.0
  ],
  [
   "kw:amino_acid_metabolism",
   -0.548,
   0.0
  ],
  [
   "go:organelle",
   -0.537,
   0.0
  ],
  [
   "kw:cell_adhesion_surface",
   -0.503,
   0.0
  ]
 ],
 "duplication_colder": [
  [
   "go:structural molecule activity",
   -0.866,
   0.0
  ],
  [
   "protein_targeting",
   -0.742,
   0.0
  ],
  [
   "go:organelle",
   0.722,
   0.0
  ],
  [
   "translation",
   0.528,
   0.0
  ],
  [
   "kw:cell_adhesion_surface",
   0.449,
   0.0
  ],
  [
   "go:hydrolase activity",
   -0.371,
   0.0
  ],
  [
   "redox_core",
   0.369,
   0.0
  ],
  [
   "go:isomerase activity",
   -0.344,
   0.0
  ],
  [
   "go:carbohydrate derivative metabolic process",
   0.341,
   0.0
  ],
  [
   "kw:gtpase_signalling",
   0.315,
   0.0
  ]
 ],
 "duplication_saltier": [
  [
   "kw:ubiquitin_system",
   -0.9,
   0.0
  ],
  [
   "atp_synthase",
   -0.884,
   0.0
  ],
  [
   "kw:cell_adhesion_surface",
   -0.858,
   0.0
  ],
  [
   "go:RNA binding",
   -0.719,
   0.0
  ],
  [
   "kw:repeat_domain",
   -0.701,
   0.0
  ],
  [
   "go:organelle",
   -0.664,
   0.0
  ],
  [
   "go:catalytic activity, acting on DNA",
   -0.461,
   0.0
  ],
  [
   "kw:cilium_flagellum",
   -0.454,
   0.0
  ],
  [
   "protein_targeting",
   0.343,
   0.0
  ],
  [
   "translation",
   0.335,
   0.0
  ]
 ],
 "duplication_anaerobic": [
  [
   "kw:lipid_metabolism",
   -0.947,
   0.0
  ],
  [
   "kw:cilium_flagellum",
   0.867,
   0.0
  ],
  [
   "atp_synthase",
   -0.792,
   0.0
  ],
  [
   "go:structural molecule activity",
   0.792,
   0.0
  ],
  [
   "kw:gtpase_signalling",
   -0.776,
   0.0
  ],
  [
   "transcription",
   -0.705,
   0.0
  ],
  [
   "kw:cytoskeleton_motor",
   -0.696,
   0.0
  ],
  [
   "kw:cell_adhesion_surface",
   0.676,
   0.0
  ],
  [
   "go:catalytic activity, acting on RNA",
   -0.63,
   0.0
  ],
  [
   "kw:zinc_finger",
   -0.582,
   0.0
  ]
 ],
 "duplication_radiation_resistant": [
  [
   "kw:ubiquitin_system",
   2.106,
   0.0
  ],
  [
   "kw:cilium_flagellum",
   1.935,
   0.0
  ],
  [
   "kw:cell_adhesion_surface",
   1.79,
   0.0
  ],
  [
   "protein_targeting",
   -1.373,
   0.0
  ],
  [
   "go:structural molecule activity",
   1.204,
   0.0
  ],
  [
   "redox_core",
   -1.174,
   0.0
  ],
  [
   "atp_synthase",
   -0.915,
   0.0
  ],
  [
   "go:ligase activity",
   -0.521,
   0.0
  ],
  [
   "go:organelle",
   0.499,
   0.0
  ],
  [
   "kw:cytoskeleton_motor",
   -0.493,
   0.0
  ]
 ],
 "duplication_oligotrophic": [
  [
   "go:lyase activity",
   -1.807,
   0.0
  ],
  [
   "go:carbohydrate derivative metabolic process",
   -1.542,
   0.0
  ],
  [
   "kw:gtpase_signalling",
   1.299,
   0.0
  ],
  [
   "protein_targeting",
   -1.098,
   0.0
  ],
  [
   "kw:lipid_metabolism",
   -1.006,
   0.0
  ],
  [
   "kw:zinc_finger",
   -0.836,
   0.0
  ],
  [
   "atp_synthase",
   -0.788,
   0.0
  ],
  [
   "redox_core",
   -0.699,
   0.0
  ],
  [
   "go:ligase activity",
   -0.672,
   0.0
  ],
  [
   "kw:repeat_domain",
   0.672,
   0.0
  ]
 ],
 "gain_colder": [
  [
   "kw:gtpase_signalling",
   -1.062,
   0.0
  ],
  [
   "transcription",
   -0.982,
   0.0
  ],
  [
   "atp_synthase",
   -0.925,
   0.0
  ],
  [
   "kw:repeat_domain",
   0.853,
   0.0
  ],
  [
   "go:ribosome",
   -0.811,
   0.0
  ],
  [
   "go:catalytic activity",
   -0.603,
   0.0
  ],
  [
   "go:organelle",
   -0.599,
   0.0
  ],
  [
   "go:catalytic activity, acting on DNA",
   0.569,
   0.0
  ],
  [
   "protein_targeting",
   0
… (잘림, 원본 파일 참조)
```

## mars

```json
{
 "Bacillus subtilis": {
  "design": {
   "base": 1.0,
   "colder": 1.2333333333333334,
   "saltier": 1.95,
   "anaerobic": 1.0,
   "radiation_resistant": 1.0,
   "oligotrophic": 1.0
  },
  "families_today": 3136,
  "expected_lost": 2289.416690117999,
  "expected_gained": 292.29660399511886,
  "expected_families_on_mars": 1138.8799138771196,
  "most_likely_lost": [
   "zf-C2HCIx2C: Zinc-finger",
   "FliH: Flagellar assembly protein FliH",
   "Flagellin_IN: Flagellin hook IN motif",
   "FlbD: Flagellar and Swarming motility proteins",
   "Zn_ribbon_Top1: Topoisomerase DNA binding C4 zinc finger",
   "YscJ_FliF_C: Flagellar M-ring protein C-terminal",
   "FlgK_D1: Flagellar hook-associated protein FlgK helical domain",
   "FlgD: Flagellar hook capping protein - N-terminal region",
   "PilZNR: Flagellar protein YcgR",
   "Flg_hook: Flagellar hook-length control protein FliK",
   "FliJ: Flagellar FliJ protein",
   "FliT: Flagellar protein FliT"
  ],
  "lost_functions": [
   [
    "go:catalytic activity",
    1.41
   ]
  ],
  "most_expanded": [
   "Methyltransf_11: Methyltransferase domain",
   "PrmA: Ribosomal protein L11 methyltransferase (PrmA)",
   "HisKA: His Kinase A (phospho-acceptor) domain",
   "FAD_binding_2: FAD binding domain",
   "Methyltransf_25: Methyltransferase domain",
   "BPD_transp_1: Binding-protein-dependent transport system inner membrane component",
   "Methyltransf_31: Methyltransferase domain",
   "MTS: Methyltransferase small domain",
   "Glycos_transf_1: Glycosyl transferases group 1",
   "GTP_EFTU_D2: Elongation factor Tu domain 2",
   "GTP_EFTU: Elongation factor Tu GTP binding domain",
   "AAA_21: AAA domain, putative AbiEii toxin, Type IV TA system"
  ],
  "expanded_functions": [
   [
    "kw:methyl_glyco_transferase",
    14.96
   ],
   [
    "go:transferase activity",
    8.33
   ],
   [
    "kw:gtpase_signalling",
    7.89
   ],
   [
    "go:transmembrane transport",
    4.85
   ],
   [
    "go:hydrolase activity",
    4.46
   ],
   [
    "go:catalytic activity, acting on a protein",
    4.35
   ]
  ],
  "most_likely_gained": [
   "Complex1_30kDa: Respiratory-chain NADH dehydrogenase, 30 Kd subunit",
   "IGPS: Indole-3-glycerol phosphate synthase",
   "Oxidored_q3: NADH-ubiquinone/plastoquinone oxidoreductase chain 6",
   "Thi4: Thi4 family",
   "Peptidase_M1: Peptidase family M1 domain",
   "Rib_5-P_isom_A: Ribose 5-phosphate isomerase A (phosphoriboisomerase A)",
   "Oxidored_q4: NADH-ubiquinone/plastoquinone oxidoreductase, chain 3",
   "LpxD: UDP-3-O-[3-hydroxymyristoyl] glucosamine N-acyltransferase, LpxD",
   "LpxB: Lipid-A-disaccharide synthetase",
   "Complex1_49kDa: Respiratory-chain NADH dehydrogenase, 49 Kd subunit",
   "Ppx-GppA: Ppx/GppA phosphatase family",
   "Pyrophosphatase: Inorganic pyrophosphatase"
  ],
  "gained_functions": [
   [
    "go:carbohydrate derivative metabolic process",
    16.18
   ],
   [
    "go:oxidoreductase activity",
    12.43
   ],
   [
    "kw:phosphatase",
    11.13
   ],
   [
    "go:transporter activity",
    10.98
   ],
   [
    "kw:lipid_metabolism",
    10.09
   ],
   [
    "go:catalytic activity",
    7.12
   ]
  ]
 },
 "Shewanella oneidensis": {
  "design": {
   "base": 1.0,
   "colder": 1.0,
   "saltier": 1.9,
   "anaerobic": 1.0,
   "radiation_resistant": 1.0,
   "oligotrophic": 1.0
  },
  "families_today": 3082,
  "expected_lost": 2243.188410672316,
  "expected_gained": 245.30507759205395,
  "expected_families_on_mars": 1084.116666919738,
  "most_likely_lost": [
   "YscJ_FliF_C: Flagellar M-ring protein C-terminal",
   "FliO: Flagellar biosynthesis protein, FliO",
   "FliS: Flagellar protein FliS",
   "FlgT_N: Flagellar assembly protein T, N-terminal domain",
   "FlgT_M: Flagellar assembly protein T, middle domain",
   "FapA: Flagellar Assembly Protein A beta solenoid domain",
   "FlgT_C: Flagellar assembly protein T, C-terminal domain",
   "FapA_N: Flagellar Assembly Protein A N-terminal region",
   "FliM: Flagellar motor switch protein FliM",
   "FliD_N: Flagellar hook-associated protein 2 N-terminus",
   "FlgI: Flagellar P-ring protein",
   "FlgK_D1: Flagellar hook-associated protein FlgK helical domain"
  ],
  "lost_functions": [
   [
    "go:catalytic activity",
    1.54
   ]
  ],
  "most_expanded": [
   "Methyltransf_11: Methyltransferase domain",
   "PrmA: Ribosomal protein L11 methyltransferase (PrmA)",
   "FAD_binding_2: FAD binding domain",
   "Methyltransf_25: Methyltransferase domain",
   "HisKA: His Kinase A (phospho-acceptor) domain",
   "Methyltransf_31: Methyltransferase domain",
   "BPD_transp_1: Binding-protein-dependent transport system inner membrane component",
   "MTS: Methyltransferase small domain",
   "Glycos_transf_1: Glycosyl transferases group 1",
   "GTP_EFTU: Elongation factor Tu GTP binding domain",
   "GTP_EFTU_D2: Elongation factor Tu domain 2",
   "AAA_21: AAA domain, putative AbiEii toxin, Type IV TA system"
  ],
  "expanded_functions": [
   [
    "kw:methyl_glyco_transferase",
    14.96
   ],
   [
    "go:transferase activity",
    8.33
   ],
   [
    "kw:gtpase_signalling",
    7.89
   ],
   [
    "go:transmembrane transport",
    4.85
   ],
   [
    "go:hydrolase activity",
    4.46
   ],
   [
    "go:catalytic activity, acting on a protein",
    4.35
   ]
  ],
  "most_likely_gained": [
   "GatB_Yqey: GatB domain",
   "GatB_N: GatB/GatE catalytic domain",
   "Glyco_tranf_2_2: Glycosyltransferase like family 2",
   "AdoHcyase_NAD: S-adenosyl-L-homocysteine hydrolase, NAD binding domain",
   "Anti-Pycsar_Apyc1: Anti-Pycsar protein Apyc1",
   "TPR_17: Tetratricopeptide repeat",
   "DHOase: Dihydro-orotase-like",
   "HxlR: HxlR-like helix-turn-helix",
   "TPR_11: TPR repeat",
   "Pyrophosphatase: Inorganic pyrophosphatase",
   "TPR_1: Tetratricopeptide repeat",
   "GatC: Glu-tRNAGln amidotransferase C subunit"
  ],
  "gained_functions": [
   [
    "kw:repeat_domain",
    15.89
   ],
   [
    "go:ligase activity",
    10.61
   ],
   [
    "kw:phosphatase",
    5.88
   ],
 
… (잘림, 원본 파일 참조)
```

## 연결
- [[실험 목록]]
