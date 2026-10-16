---
유형: 실험
실행: cancer_depmap
산출: results/cancer_depmap/summary.json
tags:
  - 유형/실험
  - 실험/cancer_depmap
---

# 실험 · cancer_depmap

**산출물** `results/cancer_depmap/summary.json`

## source

```json
{
 "release": "DepMap 24Q4 Public (figshare 27993248)",
 "files": {
  "CRISPRGeneEffect.csv": "https://ndownloader.figshare.com/files/51064667",
  "Model.csv": "https://ndownloader.figshare.com/files/51065297",
  "CRISPRInferredCommonEssentials.csv": "https://ndownloader.figshare.com/files/51064916"
 },
 "lines": 1178,
 "genes": 17916,
 "common_essentials": 1523,
 "approved_drug_genes": 3425
}
```

## primary_up_genes

```json
{
 "odds_ratio": 2.91,
 "lo": 1.794,
 "hi": 5.018,
 "uc_selective_share": 0.0931,
 "mc_selective_share": 0.0338,
 "n_uc": 462,
 "n_mc": 711,
 "verdict": "양성"
}
```

## with_common_essentials

```json
{
 "odds_ratio": 4.471,
 "lo": 3.109,
 "hi": 6.586,
 "uc_selective_share": 0.2079,
 "mc_selective_share": 0.055,
 "n_uc": 529,
 "n_mc": 727,
 "verdict": "양성"
}
```

## control_not_up

```json
{
 "odds_ratio": 2.601,
 "lo": 2.21,
 "hi": 3.09,
 "uc_selective_share": 0.0959,
 "mc_selective_share": 0.0391,
 "n_uc": 4858,
 "n_mc": 5671,
 "verdict": "양성"
}
```

## selective_share_by_stratum

```json
{
 "PS1": [
  205,
  0.1317
 ],
 "PS2": [
  209,
  0.0622
 ],
 "PS3": [
  48,
  0.0625
 ],
 "PS4": [
  59,
  0.0339
 ],
 "PS5": [
  237,
  0.0338
 ],
 "PS6": [
  77,
  0.026
 ],
 "PS7": [
  64,
  0.0312
 ],
 "PS8": [
  78,
  0.0641
 ],
 "PS9": [
  36,
  0.0556
 ],
 "PS10": [
  78,
  0.0128
 ],
 "PS11": [
  40,
  0.0
 ],
 "PS12": [
  17,
  0.0588
 ],
 "PS13": [
  2,
  0.0
 ],
 "PS14": [
  9,
  0.1111
 ],
 "PS15": [
  10,
  0.0
 ],
 "PS16": [
  4,
  0.0
 ]
}
```

## candidates

```json
{
 "BRCA": {
  "lineage_lines": 53,
  "n_candidates": 4,
  "with_approved_drug": 2
 },
 "LUAD": {
  "lineage_lines": 126,
  "n_candidates": 6,
  "with_approved_drug": 4
 },
 "LUSC": {
  "lineage_lines": 126,
  "n_candidates": 12,
  "with_approved_drug": 7
 },
 "COAD": {
  "lineage_lines": 63,
  "n_candidates": 6,
  "with_approved_drug": 1
 },
 "LIHC": {
  "lineage_lines": 24,
  "n_candidates": 0,
  "with_approved_drug": 0
 },
 "KIRC": {
  "lineage_lines": 34,
  "n_candidates": 2,
  "with_approved_drug": 1
 },
 "KIRP": {
  "lineage_lines": 34,
  "n_candidates": 5,
  "with_approved_drug": 2
 },
 "KICH": {
  "lineage_lines": 34,
  "n_candidates": 4,
  "with_approved_drug": 2
 },
 "PRAD": {
  "lineage_lines": 10,
  "n_candidates": 2,
  "with_approved_drug": 0
 },
 "STAD": {
  "lineage_lines": 69,
  "n_candidates": 6,
  "with_approved_drug": 1
 },
 "BLCA": {
  "lineage_lines": 34,
  "n_candidates": 6,
  "with_approved_drug": 2
 },
 "HNSC": {
  "lineage_lines": 77,
  "n_candidates": 4,
  "with_approved_drug": 2
 },
 "THCA": {
  "lineage_lines": 11,
  "n_candidates": 4,
  "with_approved_drug": 2
 }
}
```

## candidates_total

```json
{
 "rows": 61,
 "unique_genes": 38,
 "with_approved_drug_rows": 26,
 "cohorts_with_candidate": 12
}
```

## 연결
- [[실험 목록]]
