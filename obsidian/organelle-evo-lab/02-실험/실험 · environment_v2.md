---
유형: 실험
실행: environment_v2
산출: results/environment_v2/metrics.json
tags:
  - 유형/실험
  - 실험/environment_v2
---

# 실험 · environment_v2

**산출물** `results/environment_v2/metrics.json`

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
 "copies_only": 0.6199392920234301,
 "no_environment": 0.8191445774072861,
 "environment_law": 0.818859437295026,
 "memorisation": 0.8439985034182216
}
```

## env_vs_none

```json
{
 "mean": -0.0002851401122600905,
 "n_better": 26,
 "n": 40
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
  "memorisation": 0.8762157282803291,
  "no_environment": 0.8308004613146125,
  "environment_law": 0.8326753900723486
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
  "memorisation": 0.8062263726386285,
  "no_environment": 0.8466202524659187,
  "environment_law": 0.8495885131828016
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
  "memorisation": 0.8216303790771876,
  "no_environment": 0.8543826150209128,
  "environment_law": 0.8544760204334673
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
  "memorisation": 0.8824857325480527,
  "no_environment": 0.8629553029265398,
  "environment_law": 0.8657622243528283
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
  "memorisation": 0.890414535854378,
  "no_environment": 0.8352174644211755,
  "environment_law": 0.8131579853794534
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
   1.188,
   0.103
  ],
  [
   "kw:cilium_flagellum",
   0.538,
   0.064
  ],
  [
   "kw:zinc_finger",
   0.448,
   0.03
  ],
  [
   "atp_synthase",
   0.42,
   0.038
  ],
  [
   "go:structural molecule activity",
   -0.386,
   0.081
  ],
  [
   "go:isomerase activity",
   -0.345,
   0.041
  ],
  [
   "kw:lipid_metabolism",
   -0.345,
   0.006
  ],
  [
   "go:ligase activity",
   -0.307,
   0.011
  ],
  [
   "redox_core",
   0.301,
   0.064
  ],
  [
   "kw:cell_adhesion_surface",
   -0.288,
   0.02
  ]
 ],
 "loss_saltier": [
  [
   "protein_targeting",
   -0.665,
   0.057
  ],
  [
   "go:organelle",
   0.425,
   0.066
  ],
  [
   "go:structural molecule activity",
   -0.334,
   0.046
  ],
  [
   "kw:zinc_finger",
   0.274,
   0.02
  ],
  [
   "kw:cilium_flagellum",
   -0.214,
   0.026
  ],
  [
   "kw:gtpase_signalling",
   -0.212,
   0.005
  ],
  [
   "go:catalytic activity",
   0.2,
   0.003
  ],
  [
   "kw:transporter_channel",
   -0.181,
   0.022
  ],
  [
   "kw:cytoskeleton_motor",
   0.171,
   0.015
  ],
  [
   "go:catalytic activity, acting on DNA",
   -0.14,
   0.014
  ]
 ],
 "loss_anaerobic": [
  [
   "atp_synthase",
   -1.099,
   0.046
  ],
  [
   "go:ribosome",
   1.053,
   0.069
  ],
  [
   "kw:gtpase_signalling",
   -0.788,
   0.028
  ],
  [
   "transcription",
   0.762,
   0.044
  ],
  [
   "kw:cilium_flagellum",
   0.735,
   0.09
  ],
  [
   "go:carbohydrate metabolic process",
   -0.529,
   0.015
  ],
  [
   "go:organelle",
   0.461,
   0.104
  ],
  [
   "redox_core",
   0.452,
   0.136
  ],
  [
   "go:structural mol
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
  "expected_lost": 2188.6034284801476,
  "expected_gained": 379.25543886218685,
  "expected_families_on_mars": 1326.6520103820392,
  "most_likely_lost": [
   "FliT: Flagellar protein FliT",
   "FliD_N: Flagellar hook-associated protein 2 N-terminus",
   "PilZNR: Flagellar protein YcgR",
   "Flagellin_IN: Flagellin hook IN motif",
   "FliD_C: Flagellar hook-associated protein 2 C-terminus",
   "FlbD: Flagellar and Swarming motility proteins",
   "Flg_hook: Flagellar hook-length control protein FliK",
   "FlhF_N: Flagellar biosynthesis protein FlhF, N domain",
   "FliJ: Flagellar FliJ protein",
   "FliL: Flagellar basal body-associated protein FliL",
   "FliH: Flagellar assembly protein FliH",
   "Flagellin_C: Bacterial flagellin C-terminal helical region"
  ],
  "lost_functions": [
   [
    "go:catalytic activity",
    1.41
   ]
  ],
  "most_expanded": [
   "CarbopepD_reg_2: CarboxypepD_reg-like domain",
   "HisKA: His Kinase A (phospho-acceptor) domain",
   "GGDEF: Diguanylate cyclase, GGDEF domain",
   "LysR_substrate: LysR substrate binding domain",
   "TEN_YD-shell: Teneurin YD-shell",
   "FAD_binding_2: FAD binding domain",
   "Methyltransf_11: Methyltransferase domain",
   "Acetyltransf_1: Acetyltransferase (GNAT) family",
   "Response_reg: Response regulator receiver domain",
   "Methyltransf_25: Methyltransferase domain",
   "Flagellin_N: Bacterial flagell
… (잘림 — 원본 파일 참조)
```

## 연결
- [[실험 목록]]
