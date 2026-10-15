---
유형: 실험
실행: human_gene_ages
산출: results/human_gene_ages/summary.json
tags:
  - 유형/실험
  - 실험/human_gene_ages
---

# 실험 · human_gene_ages

**산출물** `results/human_gene_ages/summary.json`

## 한눈에

| 항목 | 값 |
| --- | --- |
| gate_pass | True |

## families

```json
{
 "n": 18067,
 "lecio_by_stratum": {
  "PS16": 8263,
  "PS1": 1718,
  "PS2": 2702,
  "PS12": 247,
  "PS7": 302,
  "PS3": 491,
  "PS8": 781,
  "PS5": 943,
  "PS10": 558,
  "PS9": 301,
  "PS4": 651,
  "PS6": 441,
  "PS11": 327,
  "PS15": 177,
  "PS14": 104,
  "PS13": 61
 },
 "grade_at_age_node": {
  "A": 10417,
  "B": 1285,
  "C": 2796,
  "D": 3569
 },
 "lecio_minus_classic_mean_index": 7.255,
 "lecio_younger_share": 0.7253,
 "lecio_older_share": 0.0185,
 "spearman_lecio_classic": 0.0456
}
```

## genes

```json
{
 "uniprot_reviewed": 20416,
 "with_age": 19437,
 "lecio_by_stratum": {
  "PS1": 3534,
  "PS2": 4384,
  "PS3": 817,
  "PS4": 1173,
  "PS5": 3024,
  "PS6": 886,
  "PS7": 705,
  "PS8": 1585,
  "PS9": 462,
  "PS10": 1022,
  "PS11": 553,
  "PS12": 541,
  "PS13": 97,
  "PS14": 248,
  "PS15": 299,
  "PS16": 107
 },
 "grade_at_age_node": {
  "A": 7156,
  "D": 4686,
  "B": 3195,
  "C": 4400
 },
 "lecio_minus_classic_mean_index": 2.041,
 "spearman_lecio_classic": 0.6049
}
```

## litman_stein

```json
{
 "primary_youngest_domain": {
  "n": 18586,
  "uc_mc_agreement": 0.7498,
  "ours_uc_share": 0.4586,
  "litman_uc_share": 0.4862,
  "spearman_6_bins": 0.5749
 },
 "secondary_oldest_domain": {
  "n": 18586,
  "uc_mc_agreement": 0.7506,
  "ours_uc_share": 0.6473,
  "litman_uc_share": 0.4862,
  "spearman_6_bins": 0.565
 },
 "classic_baseline": {
  "n": 18586,
  "uc_mc_agreement": 0.6394,
  "ours_uc_share": 0.7817,
  "litman_uc_share": 0.4862,
  "spearman_6_bins": 0.367
 },
 "sensitivity_PS4_as_UC": {
  "n": 18586,
  "uc_mc_agreement": 0.7415,
  "ours_uc_share": 0.5194,
  "litman_uc_share": 0.4862,
  "spearman_6_bins": 0.5749
 }
}
```

## sanity

```json
{
 "ribosomal RPL/RPS": {
  "PS1": 67,
  "PS2": 22,
  "PS4": 1,
  "PS6": 1,
  "PS7": 2,
  "PS16": 1
 },
 "MHC I (HLA-A/B/C)": {
  "PS15": 3
 }
}
```

## strata_nodes

```json
{
 "PS1": 0,
 "PS2": 0,
 "PS3": 8,
 "PS4": 926,
 "PS5": 930,
 "PS6": 932,
 "PS7": 936,
 "PS8": 938,
 "PS9": 940,
 "PS10": 942,
 "PS11": 946,
 "PS12": 952,
 "PS13": 954,
 "PS14": 956,
 "PS15": 960,
 "PS16": 1319
}
```

## fit

```json
{
 "m": 1.0,
 "plastid_enriched": 3930,
 "tips": 3493,
 "dropped": 0
}
```

## notes

```json
[]
```

## 연결
- [[실험 목록]]
