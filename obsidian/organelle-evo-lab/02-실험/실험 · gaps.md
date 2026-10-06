---
유형: 실험
실행: gaps
산출: results/gaps/metrics.json
tags:
  - 유형/실험
  - 실험/gaps
---

# 실험 · gaps

**산출물** `results/gaps/metrics.json`

## environment_how_much

```json
{
 "coef": {
  "base": [
   -1.2556797174460166,
   -1.4650917228204299,
   -1.0414697069029786
  ],
  "colder": [
   -0.07135462085258126,
   -0.2558279319855224,
   0.14060207046481987
  ],
  "saltier": [
   0.4831973215300567,
   0.12759393088465454,
   0.9279083325904202
  ],
  "anaerobic": [
   0.5652016929353253,
   0.07410267915251936,
   1.0190936057240823
  ],
  "radiation_resistant": [
   -0.17510253188528946,
   -0.5505633887522944,
   0.14442509176532933
  ],
  "oligotrophic": [
   0.482888955351056,
   0.012854249691112613,
   0.9115895007632585
  ]
 },
 "loo_rmse": {
  "mean_only": 0.5694864655645425,
  "environment": 0.5371899462177124
 },
 "share_lost": {
  "Shewanella frigidimarina": 0.1473069435431538,
  "Colwellia psychrerythraea": 0.2235561323815704,
  "Psychrobacter arcticus": 0.29120198265179675,
  "Planococcus halocryophilus": 0.33482142857142855,
  "Geobacillus kaustophilus": 0.2780612244897959,
  "Lactiplantibacillus plantarum": 0.5038265306122449,
  "Psychroflexus torquis": 0.3261173184357542,
  "Salinibacter ruber": 0.23210504023718764,
  "Deinococcus radiodurans": 0.20127118644067796,
  "Kineococcus radiotolerans": 0.13509060955518945,
  "Chroococcidiopsis thermalis": 0.12346688470973018,
  "Prochlorococcus marinus": 0.34324324324324323,
  "Candidatus Pelagibacter ubique": 0.5318910854158896,
  "Desulfotalea psychrophila": 0.2596685082872928,
  "Geobacter sulfurreducens": 0.42021449463763405,
  "Methanococcoides burtonii": 0.27049559981472904,
  "Halobacterium salinarum": 0.4367762853172765,
  "Haloferax volcanii": 0.3742473367299676,
  "Methanoc
… (잘림 — 원본 파일 참조)
```

## environment_order

```json
{
 "lineages": 57,
 "genes": 112,
 "containment": 0.08505701615457711,
 "row_null_mean": 0.07256924667165798,
 "row_null_z": 2.558603572801192,
 "fixed_null_mean": 0.07986840390762232,
 "fixed_null_z": 1.306914426817087,
 "fixed_null_p": 0.09
}
```

## environment_together

```json
{
 "k0": 0.8546624912167193,
 "k2": 0.8725363396740217,
 "n": 57
}
```

## endosymbiosis_how_much

```json
{
 "coef": {
  "mitochondrion": [
   0.8231446044671326,
   0.5573908468319876,
   1.0695756704195563
  ],
  "plastid": [
   0.9513571302781946,
   0.6734050250596927,
   1.2326159425555148
  ],
  "insect_endosymbiont": [
   1.9655364995778626,
   1.6732699246889327,
   2.23773696867851
  ],
  "nonphotosynthetic_plastid": [
   1.5453839771568085,
   1.264125164879489,
   1.8233360823753106
  ],
  "animal_mitochondrion": [
   0.8403131058269661,
   0.5862812870108138,
   1.103501140683941
  ]
 },
 "loo_rmse": {
  "system_only": 1.010661752461697,
  "with_covariates": 0.9946994775424071
 },
 "typical_share_lost": {
  "mitochondrion": 0.6949034443407024,
  "plastid": 0.7213880259661092,
  "insect_endosymbiont": 0.8771308806596735,
  "plastid, non-photosynthetic": 0.923913043478261,
  "mitochondrion, animal": 0.8407016136469685
 }
}
```

## endosymbiosis_together

```json
{
 "mitochondrion": {
  "k0": 0.940909424514252,
  "k2": 0.9700009050910232,
  "n": 75
 },
 "plastid": {
  "k0": 0.8961833597818687,
  "k2": 0.9618011251469091,
  "n": 54
 },
 "insect_endosymbiont": {
  "k0": 0.9126341304685982,
  "k2": 0.92585790375942,
  "n": 25
 }
}
```

## 연결
- [[실험 목록]]
