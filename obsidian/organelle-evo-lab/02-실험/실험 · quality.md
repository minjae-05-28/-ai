---
유형: 실험
실행: quality
산출: results/quality/summary.json
tags:
  - 유형/실험
  - 실험/quality
---

# 실험 · quality

**산출물** `results/quality/summary.json`

## 한눈에

| 항목 | 값 |
| --- | --- |
| high_busco | 97 |
| universal_share | 0.95 |

## kingdoms

```json
{
 "archaea": {
  "proteomes": 684,
  "reference_proteomes": 416,
  "basis": "BUSCO C>=97%",
  "markers": 150,
  "marker_examples": [
   "Ribosomal_L13",
   "HTH_24",
   "Ribosomal_L22",
   "Ribosomal_L19e_C",
   "Ribosomal_L19e",
   "2-Hacid_dh_C",
   "Ribosomal_L1",
   "AsnC_trans_reg",
   "Ribosomal_L10",
   "NTP_transf_3",
   "Ribosomal_L44",
   "HHH_5"
  ],
  "score_percentiles": {
   "5": 0.0,
   "25": 0.993,
   "50": 1.0,
   "75": 1.0,
   "95": 1.0
  },
  "share_below_0.9": 0.142,
  "share_below_0.5": 0.102,
  "agreement_with_busco": {
   "n": 680,
   "pearson": 0.518,
   "spearman": 0.474,
   "median_abs_diff": 0.021,
   "median_score_where_busco_below_90": 0.72,
   "median_score_where_busco_at_least_97": 1.0
  },
  "markers_full": [
   "Ribosomal_L13",
   "HTH_24",
   "Ribosomal_L22",
   "Ribosomal_L19e_C",
   "Ribosomal_L19e",
   "2-Hacid_dh_C",
   "Ribosomal_L1",
   "AsnC_trans_reg",
   "Ribosomal_L10",
   "NTP_transf_3",
   "Ribosomal_L44",
   "HHH_5",
   "Ribosomal_L3",
   "Ribosomal_L15e",
   "RL10P_insert",
   "MFS_1",
   "Ribosomal_L21e",
   "Ribosomal_L5_C",
   "Ribosomal_L14",
   "Ribosomal_L4",
   "Ribosomal_L26",
   "Ribosomal_L23",
   "AIRS_C",
   "tRNA_int_endo",
   "PNP_UDP_1",
   "OMPdecase",
   "OTCace",
   "EFG_IV",
   "POR",
   "AA_kinase",
   "POR_N",
   "tRNA_NucTransf2",
   "dsDNA_bind",
   "IF5A-like_N",
   "TFIIB",
   "TIM",
   "Peptidase_M24",
   "EIF_2_alpha",
   "Pyr_redox_2",
   "KOW",
   "TPP_enzyme_C",
   "Proteasome_A_N",
   "Prenyltransf",
   "TP_methylase",
   "Hydrolase",
   "TGT",
   "RtcB",
   "Ribosomal_S19e",
   "Lactamase_B",
 
… (잘림 — 원본 파일 참조)
```

## 연결
- [[실험 목록]]
