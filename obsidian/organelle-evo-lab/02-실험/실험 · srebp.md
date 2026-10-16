---
유형: 실험
실행: srebp
산출: results/srebp/summary.json
tags:
  - 유형/실험
  - 실험/srebp
---

# 실험 · srebp

**산출물** `results/srebp/summary.json`

## 한눈에

| 항목 | 값 |
| --- | --- |
| tumours_positive | 8 / 13 |

## source

```json
{
 "score_zip": {
  "url": "https://cog.sanger.ac.uk/cmp/download/essentiality_matrices.zip",
  "files": [
   "EssentialityMatrices/",
   "EssentialityMatrices/_ReadMe.txt",
   "EssentialityMatrices/04_binaryDepScores.tsv",
   "EssentialityMatrices/02a_BayesianFactors.tsv",
   "EssentialityMatrices/00_logFCs.tsv",
   "EssentialityMatrices/02b_MageckFDRs.tsv",
   "EssentialityMatrices/01_corrected_logFCs.tsv",
   "EssentialityMatrices/03_scaledBayesianFactors.tsv",
   "EssentialityMatrices/01a_qnorm_corrected_logFCs.tsv"
  ]
 },
 "score_file": "EssentialityMatrices/00_logFCs.tsv",
 "score_lines_mapped": 316,
 "gdsc": {
  "url": "https://cog.sanger.ac.uk/cancerrxgene/GDSC_release8.5/GDSC2_fitted_dose_response_27Oct23.xlsx",
  "rows": 0
 }
}
```

## project_score

```json
{
 "lines": 249,
 "module": {
  "rho_partial": -0.1717,
  "lo": -0.2835,
  "hi": -0.0554,
  "n": 249,
  "verdict": "양성"
 },
 "genes": {
  "SCD": {
   "rho_partial": -0.2411,
   "lo": -0.3541,
   "hi": -0.1241,
   "n": 249,
   "verdict": "양성"
  },
  "SREBF1": {
   "rho_partial": -0.0799,
   "lo": -0.2058,
   "hi": 0.048,
   "n": 249,
   "verdict": "무승부"
  },
  "SCAP": {
   "rho_partial": -0.1691,
   "lo": -0.2831,
   "hi": -0.0483,
   "n": 249,
   "verdict": "양성"
  },
  "MBTPS1": {
   "rho_partial": -0.1664,
   "lo": -0.2749,
   "hi": -0.0512,
   "n": 249,
   "verdict": "양성"
  },
  "MBTPS2": {
   "rho_partial": -0.0511,
   "lo": -0.1717,
   "hi": 0.0632,
   "n": 249,
   "verdict": "무승부"
  }
 }
}
```

## depmap_partial_rho_for_comparison

```json
{
 "SCD": -0.2241,
 "SREBF1": -0.1707,
 "SCAP": -0.1566,
 "MBTPS1": -0.1385,
 "MBTPS2": -0.0666
}
```

## tumours

```json
{
 "BLCA": {
  "pairs": 14,
  "spearman_delta_vs_srebp_targets": 0.1209
 },
 "BRCA": {
  "pairs": 112,
  "spearman_delta_vs_srebp_targets": 0.2386
 },
 "COAD": {
  "pairs": 26,
  "spearman_delta_vs_srebp_targets": -0.2841
 },
 "HNSC": {
  "pairs": 38,
  "spearman_delta_vs_srebp_targets": 0.0137
 },
 "KICH": {
  "pairs": 23,
  "spearman_delta_vs_srebp_targets": -0.1087
 },
 "KIRC": {
  "pairs": 63,
  "spearman_delta_vs_srebp_targets": -0.1097
 },
 "KIRP": {
  "pairs": 30,
  "spearman_delta_vs_srebp_targets": -0.0981
 },
 "LIHC": {
  "pairs": 45,
  "spearman_delta_vs_srebp_targets": 0.5267
 },
 "LUAD": {
  "pairs": 54,
  "spearman_delta_vs_srebp_targets": 0.0696
 },
 "LUSC": {
  "pairs": 50,
  "spearman_delta_vs_srebp_targets": 0.0059
 },
 "PRAD": {
  "pairs": 40,
  "spearman_delta_vs_srebp_targets": 0.0833
 },
 "STAD": {
  "pairs": 26,
  "spearman_delta_vs_srebp_targets": 0.7313
 },
 "THCA": {
  "pairs": 43,
  "spearman_delta_vs_srebp_targets": -0.5445
 }
}
```

## gdsc_lipid_drugs

```json
{}
```

## 연결
- [[실험 목록]]
