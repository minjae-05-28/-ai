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
 "Methanocaldococcus jannaschii":
… (잘림 — 원본 파일 참조)
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
   
… (잘림 — 원본 파일 참조)
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
  
… (잘림 — 원본 파일 참조)
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
   "GTP_EFTU: El
… (잘림 — 원본 파일 참조)
```

## 연결
- [[실험 목록]]
