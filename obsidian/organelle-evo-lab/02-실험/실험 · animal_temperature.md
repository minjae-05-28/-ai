---
유형: 실험
실행: animal_temperature
산출: results/animal_temperature/metrics.json
tags:
  - 유형/실험
  - 실험/animal_temperature
---

# 실험 · animal_temperature

**산출물** `results/animal_temperature/metrics.json`

## 한눈에

| 항목 | 값 |
| --- | --- |
| n_animals | 19 |

## law_per_degree_c

```json
{
 "ols": 0.0009836,
 "tree_pgls": 0.0006997,
 "rank_gls": 0.0007847
}
```

## species

```json
[
 {
  "species": "Amphimedon queenslandica",
  "temperature_c": 25.0,
  "group": "ectotherm",
  "ivywrel": 0.449688,
  "fymink": 0.295381,
  "cvp": -0.054931,
  "n_proteins": 13
 },
 {
  "species": "Anopheles gambiae",
  "temperature_c": 27.0,
  "group": "ectotherm",
  "ivywrel": 0.413073,
  "fymink": 0.367533,
  "cvp": -0.133941,
  "n_proteins": 13
 },
 {
  "species": "Apis mellifera",
  "temperature_c": 25.0,
  "group": "ectotherm",
  "ivywrel": 0.433679,
  "fymink": 0.498908,
  "cvp": -0.114083,
  "n_proteins": 13
 },
 {
  "species": "Ascaris suum",
  "temperature_c": 39.0,
  "group": "parasite of an endotherm",
  "ivywrel": 0.421546,
  "fymink": 0.369145,
  "cvp": -0.099532,
  "n_proteins": 12
 },
 {
  "species": "Branchiostoma floridae",
  "temperature_c": 22.0,
  "group": "ectotherm",
  "ivywrel": 0.434586,
  "fymink": 0.271516,
  "cvp": -0.089528,
  "n_proteins": 13
 },
 {
  "species": "Caenorhabditis elegans",
  "temperature_c": 20.0,
  "group": "ectotherm",
  "ivywrel": 0.411283,
  "fymink": 0.393452,
  "cvp": -0.127156,
  "n_proteins": 12
 },
 {
  "species": "Ciona intestinalis B CG-2006",
  "temperature_c": 18.0,
  "group": "ectotherm",
  "ivywrel": 0.401422,
  "fymink": 0.403063,
  "cvp": -0.093246,
  "n_proteins": 13
 },
 {
  "species": "Danio rerio",
  "temperature_c": 26.0,
  "group": "ectotherm",
  "ivywrel": 0.4048,
  "fymink": 0.279272,
  "cvp": -0.106804,
  "n_proteins": 13
 },
 {
  "species": "Daphnia pulex",
  "temperature_c": 20.0,
  "group": "ectotherm",
  "ivywrel": 0.414833,
  "fymink": 0.295572,
  "cvp": -0.114643,
  "n_proteins": 13
 },
 {
  "spe
… (잘림 — 원본 파일 참조)
```

## endotherm_vs_ectotherm

```json
{
 "n_endotherm": 3,
 "n_ectotherm": 14,
 "mean_ivywrel_endotherm": 0.3990316666666667,
 "mean_ivywrel_ectotherm": 0.4200577142857142,
 "delta_temperature_c": 17.0,
 "predicted_delta_ivywrel": 0.016721200000000002,
 "observed_delta_ivywrel": -0.021026047619047528,
 "mannwhitney_p": 0.0058823529411764705,
 "transfers": false
}
```

## all_animals

```json
{
 "n": 17,
 "spearman_temperature_vs_ivywrel": -0.496311455917058,
 "slope_per_degree_c": -0.0009584330312185284,
 "spearman_ivywrel_vs_fymink": 0.07843137254901962,
 "partial_spearman_controlling_at_bias": -0.49175749239225885
}
```

## parasites_of_endotherms

```json
[
 {
  "species": "Ascaris suum",
  "temperature_c": 39.0,
  "group": "parasite of an endotherm",
  "ivywrel": 0.421546,
  "fymink": 0.369145,
  "cvp": -0.099532,
  "n_proteins": 12
 },
 {
  "species": "Schistosoma mansoni",
  "temperature_c": 37.0,
  "group": "parasite of an endotherm",
  "ivywrel": 0.49835,
  "fymink": 0.325533,
  "cvp": -0.093009,
  "n_proteins": 12
 }
]
```

## 연결
- [[실험 목록]]
