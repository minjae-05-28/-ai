---
유형: 실험
실행: new_species
산출: results/new_species/summary.json
tags:
  - 유형/실험
  - 실험/new_species
---

# 실험 · new_species

**산출물** `results/new_species/summary.json`

## 한눈에

| 항목 | 값 |
| --- | --- |
| preregistration | docs/preregistration/2026-10-10_new_species_prediction.md |
| n_new_species_fetched | 1000 |
| n_scored | 998 |

## skipped

```json
{
 "UP001732900": "proteome too small",
 "UP001301735": "proteome too small"
}
```

## mean_auroc

```json
{
 "model": 0.969,
 "relatives": 0.9495,
 "global": 0.7825
}
```

## model_minus_relatives

```json
{
 "mean": 0.0195,
 "ci95": [
  0.0185,
  0.0206
 ],
 "verdict": "양성",
 "share_positive": 0.994
}
```

## model_minus_global

```json
{
 "mean": 0.1865,
 "ci95": [
  0.1816,
  0.1912
 ],
 "verdict": "양성",
 "share_positive": 1.0
}
```

## relatives_minus_global

```json
{
 "mean": 0.1671,
 "ci95": [
  0.1622,
  0.1724
 ],
 "verdict": "양성",
 "share_positive": 0.991
}
```

## by_group

```json
{
 "Metazoa": {
  "n": 766,
  "model": 0.9632,
  "relatives": 0.9435,
  "global": 0.7603
 },
 "Viridiplantae": {
  "n": 150,
  "model": 0.9891,
  "relatives": 0.9786,
  "global": 0.8289
 },
 "Sar": {
  "n": 75,
  "model": 0.9868,
  "relatives": 0.952,
  "global": 0.9062
 },
 "Discoba": {
  "n": 6,
  "model": 0.9923,
  "relatives": 0.9668,
  "global": 0.8871
 },
 "Metamonada": {
  "n": 1,
  "model": 0.9705,
  "relatives": 0.9183,
  "global": 0.8919
 }
}
```

## by_number_of_relatives

```json
{
 "relatives_3-10": {
  "n": 404,
  "model_minus_relatives": 0.0221
 },
 "relatives_1-2": {
  "n": 539,
  "model_minus_relatives": 0.0177
 },
 "relatives_>10": {
  "n": 55,
  "model_minus_relatives": 0.0176
 }
}
```

## 연결
- [[실험 목록]]
