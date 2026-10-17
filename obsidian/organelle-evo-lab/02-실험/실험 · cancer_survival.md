---
유형: 실험
실행: cancer_survival
산출: results/cancer_survival/summary.json
tags:
  - 유형/실험
  - 실험/cancer_survival
---

# 실험 · cancer_survival

**산출물** `results/cancer_survival/summary.json`

## 한눈에

| 항목 | 값 |
| --- | --- |
| min_patients | 50 |
| min_deaths | 10 |
| judged | 15 |
| overall | 지지하지 않음 |

## cohorts

```json
{
 "BLCA": {
  "patients_with_tilt_and_survival": 403,
  "deaths": 177,
  "patients_used": 401,
  "covariates": [
   "delta",
   "age",
   "stage"
  ],
  "primary": {
   "hr": 0.9512,
   "lo": 0.8231,
   "hi": 1.1108,
   "log_hr": -0.0501,
   "log_hr_se": 0.0758,
   "n_boot_ok": 2000,
   "verdict": "무승부"
  },
  "aux1_unadjusted": {
   "hr": 0.9069,
   "lo": 0.7924,
   "hi": 1.0457,
   "log_hr": -0.0977,
   "log_hr_se": 0.0713,
   "n_boot_ok": 2000,
   "verdict": "무승부"
  },
  "aux2_plus_proliferation_immune_stromal": {
   "hr": 0.9092,
   "lo": 0.6823,
   "hi": 1.193,
   "log_hr": -0.0952,
   "log_hr_se": 0.1454,
   "n_boot_ok": 2000,
   "verdict": "무승부"
  },
  "aux3_median_split_5y_survival": {
   "high_tilt": 0.4855,
   "low_tilt": 0.349,
   "difference_high_minus_low": 0.1365
  },
  "aux4_stage_1_2_only": {
   "hr": 0.8441,
   "lo": 0.6009,
   "hi": 1.2245,
   "log_hr": -0.1695,
   "log_hr_se": 0.1803,
   "n_boot_ok": 2000,
   "verdict": "무승부"
  },
  "aux5_concordance": {
   "tilt": 0.4872,
   "proliferation": 0.542
  },
  "aux6_corr_tilt_stage": -0.1573
 },
 "BRCA": {
  "patients_with_tilt_and_survival": 1080,
  "deaths": 151,
  "patients_used": 1058,
  "covariates": [
   "delta",
   "age",
   "stage"
  ],
  "primary": {
   "hr": 0.9475,
   "lo": 0.8025,
   "hi": 1.1327,
   "log_hr": -0.0539,
   "log_hr_se": 0.0877,
   "n_boot_ok": 2000,
   "verdict": "무승부"
  },
  "aux1_unadjusted": {
   "hr": 1.092,
   "lo": 0.925,
   "hi": 1.3035,
   "log_hr": 0.088,
   "log_hr_se": 0.0869,
   "n_boot_ok": 2000,
   "verdict": "무승부"
  },
  "aux2_plus_proliferation_immune_stromal": {
   
… (잘림 — 원본 파일 참조)
```

## positive

```json
[]
```

## negative

```json
[]
```

## undecided

```json
[
 "BLCA",
 "BRCA",
 "COAD",
 "ESCA",
 "HNSC",
 "KIRC",
 "KIRP",
 "LIHC",
 "LUAD",
 "LUSC",
 "PRAD",
 "READ",
 "STAD",
 "THCA",
 "UCEC"
]
```

## combined

```json
{
 "hr": 0.9949,
 "lo": 0.9433,
 "hi": 1.0492,
 "cohorts": 15
}
```

## 연결
- [[실험 목록]]
