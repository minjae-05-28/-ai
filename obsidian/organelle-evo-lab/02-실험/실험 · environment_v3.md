---
유형: 실험
실행: environment_v3
산출: results/environment_v3/metrics.json
tags:
  - 유형/실험
  - 실험/environment_v3
---

# 실험 · environment_v3

**산출물** `results/environment_v3/metrics.json`

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
 "Pseudomonas aeruginosa -> Pseudomonas putida",
 "Vibrio natriegens -> Photobacterium profundum",
 "Alteromonas macleodii -> Pseudoalteromonas haloplanktis",
 "Pseudomonas aeruginosa -> Halomonas elongata",
 "Pseudomonas aeruginosa -> Chromohalobacter salexigens",
 "Bacillus subtilis -> Halobacillus halophilus",
 "Methanosarcina acetivorans -> Haloarcula marismortui",
 "Methanosarcina acetivorans -> Natronomonas pharaonis",
 "Bacillus subtilis -> Clostridium acetobutylicum",
 "Myxococcus xanthu
… (잘림 — 원본 파일 참조)
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
 "copies_only": 0.6172579176865324,
 "no_environment": 0.8132686604717007,
 "environment_law": 0.8141681436768096,
 "memorisation": 0.849235234515775
}
```

## env_vs_none

```json
{
 "mean": 0.0008994832051090464,
 "n_better": 29,
 "n": 54
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
  "memorisation": 0.8866145843810137,
  "no_environment": 0.8248923822742542,
  "environment_law": 0.82860536144134
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
  "memorisation": 0.8580156685834409,
  "no_environment": 0.8404514376413548,
  "environment_law": 0.8464898527817891
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
  "memorisation": 0.8350832382747276,
  "no_environment": 0.8520937691150458,
  "environment_law": 0.8542908628015011
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
  "memorisation": 0.8797584805734374,
  "no_environment": 0.8592512441218098,
  "environment_law": 0.8624471533579875
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
  "memorisation": 0.8994774106882355,
  "no_environment": 0.8361332747106688,
  "environment_law": 0.8269300904463968
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
   1.353,
   0.068
  ],
  [
   "kw:cilium_flagellum",
   0.514,
   0.029
  ],
  [
   "go:structural molecule activity",
   -0.448,
   0.022
  ],
  [
   "kw:ubiquitin_system",
   -0.413,
   0.008
  ],
  [
   "go:isomerase activity",
   -0.397,
   0.031
  ],
  [
   "go:lyase activity",
   -0.346,
   0.01
  ],
  [
   "kw:gtpase_signalling",
   0.313,
   0.003
  ],
  [
   "go:catalytic activity, acting on RNA",
   -0.307,
   0.022
  ],
  [
   "kw:lipid_metabolism",
   -0.278,
   0.008
  ],
  [
   "redox_core",
   0.275,
   0.046
  ]
 ],
 "loss_saltier": [
  [
   "protein_targeting",
   -0.554,
   0.046
  ],
  [
   "kw:ubiquitin_system",
   0.457,
   0.018
  ],
  [
   "transcription",
   0.406,
   0.129
  ],
  [
   "go:ribosome",
   0.31,
   0.078
  ],
  [
   "kw:zinc_finger",
   0.259,
   0.019
  ],
  [
   "kw:cytoskeleton_motor",
   0.218,
   0.066
  ],
  [
   "go:catalytic activity",
   0.211,
   0.005
  ],
  [
   "kw:repeat_domain",
   0.205,
   0.018
  ],
  [
   "go:regulation of DNA-templated transcription",
   0.158,
   0.011
  ],
  [
   "has_go_annotation",
   -0.144,
   0.001
  ]
 ],
 "loss_anaerobic": [
  [
   "transcription",
   0.913,
   0.078
  ],
  [
   "go:ribosome",
   0.729,
   0.188
  ],
  [
   "atp_synthase",
   -0.72,
   0.219
  ],
  [
   "kw:cilium_flagellum",
   0.688,
   0.116
  ],
  [
   "kw:gtpase_signalling",
   -0.564,
   0.039
  ],
  [
   "go:carbohydrate metabolic process",
   -0.514,
   0.015
  ],
  [
   "redox_core",
   0.481,
   0.13
  ],
  [
   "go:organelle",
   0.359,
   0.132
  ],
  [
   "go:carbohydr
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
  "expected_lost": 2168.1138167655035,
  "expected_gained": 396.77168271467235,
  "expected_families_on_mars": 1364.6578659491688,
  "most_likely_lost": [
   "FlhF_N: Flagellar biosynthesis protein FlhF, N domain",
   "FliD_C: Flagellar hook-associated protein 2 C-terminus",
   "FliT: Flagellar protein FliT",
   "PilZNR: Flagellar protein YcgR",
   "FliL: Flagellar basal body-associated protein FliL",
   "Flagellin_IN: Flagellin hook IN motif",
   "FliD_N: Flagellar hook-associated protein 2 N-terminus",
   "FlbD: Flagellar and Swarming motility proteins",
   "DUF348: G5-linked-Ubiquitin-like domain",
   "FliJ: Flagellar FliJ protein",
   "FliH: Flagellar assembly protein FliH",
   "Flagellin_C: Bacterial flagellin C-terminal helical region"
  ],
  "lost_functions": [
   [
    "go:catalytic activity",
    1.4
   ]
  ],
  "most_expanded": [
   "CarbopepD_reg_2: CarboxypepD_reg-like domain",
   "Flagellin_N: Bacterial flagellin N-terminal helical region",
   "TEN_YD-shell: Teneurin YD-shell",
   "GGDEF: Diguanylate cyclase, GGDEF domain",
   "HisKA: His Kinase A (phospho-acceptor) domain",
   "LysR_substrate: LysR substrate binding domain",
   "FAD_binding_2: FAD binding domain",
   "TPR_15: Tetratricopeptide repeat",
   "Response_reg: Response regulator receiver domain",
   "Condensation: Condensation domain",
   "Methyltransf_11: Methyltransferase domain",
   "TP
… (잘림 — 원본 파일 참조)
```

## 연결
- [[실험 목록]]
