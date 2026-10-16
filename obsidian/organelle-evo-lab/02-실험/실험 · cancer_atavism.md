---
유형: 실험
실행: cancer_atavism
산출: results/cancer_atavism/summary.json
tags:
  - 유형/실험
  - 실험/cancer_atavism
---

# 실험 · cancer_atavism

**산출물** `results/cancer_atavism/summary.json`

## 한눈에

| 항목 | 값 |
| --- | --- |
| negative_age_slope_cohorts | 10 |

## overall_primary

```json
{
 "cohorts": 13,
 "positive": 10,
 "negative": 0,
 "draw": 3,
 "call": "지지"
}
```

## overall_unadjusted

```json
{
 "cohorts": 13,
 "positive": 9,
 "negative": 1,
 "draw": 3,
 "call": "지지"
}
```

## overall_sensitivity

```json
{
 "a_oldest_domain": {
  "cohorts": 13,
  "positive": 11,
  "negative": 0,
  "draw": 2,
  "call": "지지"
 },
 "b_grade_A_only": {
  "cohorts": 13,
  "positive": 10,
  "negative": 0,
  "draw": 3,
  "call": "지지"
 },
 "c_PS4_as_UC": {
  "cohorts": 13,
  "positive": 10,
  "negative": 0,
  "draw": 3,
  "call": "지지"
 },
 "d_no_mitosis_chromosome": {
  "cohorts": 13,
  "positive": 10,
  "negative": 0,
  "draw": 3,
  "call": "지지"
 }
}
```

## cohorts

```json
{
 "BLCA": {
  "pairs": 14,
  "genes": 14116,
  "uc_genes": 6941,
  "mc_genes": 7175,
  "primary": {
   "delta": 0.3472,
   "lo": 0.2709,
   "hi": 0.4257,
   "verdict": "양성"
  },
  "unadjusted": {
   "delta": 0.2589,
   "lo": 0.163,
   "hi": 0.3586,
   "verdict": "양성"
  },
  "age_slope_spearman": -0.0935,
  "sensitivity": {
   "a_oldest_domain": {
    "delta": 0.3513,
    "lo": 0.2422,
    "hi": 0.4595,
    "verdict": "양성"
   },
   "b_grade_A_only": {
    "delta": 0.3334,
    "lo": 0.2654,
    "hi": 0.4114,
    "verdict": "양성"
   },
   "c_PS4_as_UC": {
    "delta": 0.3368,
    "lo": 0.2643,
    "hi": 0.4107,
    "verdict": "양성"
   },
   "d_no_mitosis_chromosome": {
    "delta": 0.3436,
    "lo": 0.2677,
    "hi": 0.422,
    "verdict": "양성"
   }
  }
 },
 "BRCA": {
  "pairs": 112,
  "genes": 14117,
  "uc_genes": 6940,
  "mc_genes": 7177,
  "primary": {
   "delta": 0.285,
   "lo": 0.2531,
   "hi": 0.3184,
   "verdict": "양성"
  },
  "unadjusted": {
   "delta": 0.2635,
   "lo": 0.2285,
   "hi": 0.2988,
   "verdict": "양성"
  },
  "age_slope_spearman": -0.1125,
  "sensitivity": {
   "a_oldest_domain": {
    "delta": 0.3271,
    "lo": 0.2817,
    "hi": 0.3753,
    "verdict": "양성"
   },
   "b_grade_A_only": {
    "delta": 0.2751,
    "lo": 0.2438,
    "hi": 0.3058,
    "verdict": "양성"
   },
   "c_PS4_as_UC": {
    "delta": 0.2768,
    "lo": 0.2462,
    "hi": 0.3097,
    "verdict": "양성"
   },
   "d_no_mitosis_chromosome": {
    "delta": 0.2826,
    "lo": 0.2507,
    "hi": 0.316,
    "verdict": "양성"
   }
  }
 },
 "COAD": {
  "pairs": 26,
  "genes": 14097,
  "uc_genes": 6929,
  "mc_genes
… (잘림 — 원본 파일 참조)
```

## manifest

```json
{
 "BLCA": {
  "pairs_before": 19,
  "pairs_after": 14,
  "swapped_or_low_purity": 5,
  "extreme_lfc": 0,
  "genes_dropped_missing": 0
 },
 "BRCA": {
  "pairs_before": 114,
  "pairs_after": 112,
  "swapped_or_low_purity": 2,
  "extreme_lfc": 0,
  "genes_dropped_missing": 0
 },
 "COAD": {
  "pairs_before": 26,
  "pairs_after": 26,
  "swapped_or_low_purity": 0,
  "extreme_lfc": 0,
  "genes_dropped_missing": 0
 },
 "ESCA": {
  "pairs_before": 11,
  "pairs_after": 7,
  "swapped_or_low_purity": 2,
  "extreme_lfc": 2,
  "genes_dropped_missing": 0
 },
 "HNSC": {
  "pairs_before": 43,
  "pairs_after": 38,
  "swapped_or_low_purity": 2,
  "extreme_lfc": 3,
  "genes_dropped_missing": 0
 },
 "KICH": {
  "pairs_before": 25,
  "pairs_after": 23,
  "swapped_or_low_purity": 2,
  "extreme_lfc": 0,
  "genes_dropped_missing": 0
 },
 "KIRC": {
  "pairs_before": 72,
  "pairs_after": 63,
  "swapped_or_low_purity": 2,
  "extreme_lfc": 7,
  "genes_dropped_missing": 0
 },
 "KIRP": {
  "pairs_before": 32,
  "pairs_after": 30,
  "swapped_or_low_purity": 1,
  "extreme_lfc": 1,
  "genes_dropped_missing": 0
 },
 "LIHC": {
  "pairs_before": 50,
  "pairs_after": 45,
  "swapped_or_low_purity": 3,
  "extreme_lfc": 2,
  "genes_dropped_missing": 0
 },
 "LUAD": {
  "pairs_before": 58,
  "pairs_after": 54,
  "swapped_or_low_purity": 2,
  "extreme_lfc": 2,
  "genes_dropped_missing": 0
 },
 "LUSC": {
  "pairs_before": 51,
  "pairs_after": 50,
  "swapped_or_low_purity": 1,
  "extreme_lfc": 0,
  "genes_dropped_missing": 0
 },
 "PRAD": {
  "pairs_before": 52,
  "pairs_after": 40,
  "swapped_or_low_purity": 6,
  "ext
… (잘림 — 원본 파일 참조)
```

## 연결
- [[실험 목록]]
