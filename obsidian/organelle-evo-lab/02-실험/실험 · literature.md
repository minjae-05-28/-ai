---
유형: 실험
실행: literature
산출: results/literature/metrics.json
tags:
  - 유형/실험
  - 실험/literature
---

# 실험 · literature

**산출물** `results/literature/metrics.json`

## scaling

```json
{
 "transcription_regulation": [
  1.9456115120311346,
  [
   1.6333419076306863,
   2.2665489155137277
  ]
 ],
 "signal_transduction": [
  2.4650907919660856,
  [
   1.803552080748515,
   3.3559067195102217
  ]
 ],
 "metabolism": [
  0.6982112995787688,
  [
   0.5305209321926005,
   0.8852706482828286
  ]
 ],
 "translation": [
  0.012058993190634346,
  [
   -0.01834250040700745,
   0.044910144472728654
  ]
 ]
}
```

## black_queen

```json
[
 {
  "relative": "Synechococcus elongatus",
  "oligotroph": "Prochlorococcus marinus",
  "relative_detox_genes": 2,
  "oligotroph_detox_genes": 0
 },
 {
  "relative": "Cereibacter sphaeroides",
  "oligotroph": "Candidatus Pelagibacter ubique",
  "relative_detox_genes": 3,
  "oligotroph_detox_genes": 0
 }
]
```

## streamlining

```json
{
 "oligotrophs": [
  {
   "species": "Candidatus Pelagibacter ubique",
   "oligo": 1,
   "genes": 1341,
   "tf_per_1000_genes": 19.388516032811335
  },
  {
   "species": "Prochlorococcus marinus",
   "oligo": 1,
   "genes": 1855,
   "tf_per_1000_genes": 21.5633423180593
  }
 ],
 "median_genes": [
  1598.0,
  3327.0
 ],
 "median_tf_per_1000": [
  20.47592917543532,
  59.69271015647981
 ]
}
```

## plastid_order

```json
{
 "ndh": {
  "genes_in_tobacco": 11,
  "share_lost_in_epifagus": 1.0
 },
 "photosynthesis_and_PEP": {
  "genes_in_tobacco": 31,
  "share_lost_in_epifagus": 1.0
 },
 "atp_synthase": {
  "genes_in_tobacco": 6,
  "share_lost_in_epifagus": 1.0
 },
 "housekeeping": {
  "genes_in_tobacco": 26,
  "share_lost_in_epifagus": 0.23076923076923073
 },
 "monotone_with_stage": true
}
```

## krylov

```json
{
 "spearman_ubiquity_vs_loss_rate": -0.5770210672594679,
 "families": 8416,
 "loss_rate_least_ubiquitous_quartile": 0.680915903808228,
 "loss_rate_most_ubiquitous_quartile": 0.24390150546828884
}
```

## universal_retention

```json
{
 "mitochondrion->plastid": 0.43236073025901456,
 "plastid within": 0.4991434753770642,
 "plastid->mitochondrion": 0.35887125274381343,
 "mitochondrion within": 0.5489035375504145
}
```

## hydrophobicity

```json
{
 "mitochondrion:hydrophobicity_gravy": {
  "loss_weight": -0.3241,
  "ci95": [
   -0.4773,
   -0.171
  ]
 },
 "mitochondrion:tm_helices": {
  "loss_weight": -0.3672,
  "ci95": [
   -0.6005,
   -0.1338
  ]
 },
 "plastid:hydrophobicity_gravy": {
  "loss_weight": 0.0134,
  "ci95": [
   -0.0779,
   0.1047
  ]
 },
 "plastid:tm_helices": {
  "loss_weight": -0.0466,
  "ci95": [
   -0.1629,
   0.0696
  ]
 },
 "insect_endosymbiont:hydrophobicity_gravy": {
  "loss_weight": -0.0127,
  "ci95": [
   -0.0306,
   0.0052
  ]
 },
 "insect_endosymbiont:tm_helices": {
  "loss_weight": 0.1623,
  "ci95": [
   0.1423,
   0.1822
  ]
 }
}
```

## 연결
- [[실험 목록]]
