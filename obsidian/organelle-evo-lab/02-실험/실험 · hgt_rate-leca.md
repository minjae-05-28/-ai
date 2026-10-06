---
유형: 실험
실행: hgt_rate/leca
산출: results/hgt_rate/leca/summary.json
tags:
  - 유형/실험
  - 실험/hgt_rate-leca
---

# 실험 · hgt_rate-leca

**산출물** `results/hgt_rate/leca/summary.json`

## sets

```json
{
 "leca": {
  "label": "진핵생물 전체 (뿌리별 가장 높은 값: discoba)",
  "families": 14869,
  "observed": {
   "median_q": 0.5,
   "mean_log10_q": -0.06315860851976457,
   "share_q_ge_1": 0.477570784854395,
   "share_q_ge_0.3": 0.7021319523841549
  },
  "calibration": [
   {
    "hgt": 0.0,
    "median_q": 0.1,
    "mean_log10_q": -1.0469,
    "share_q_ge_1": 0.0733,
    "share_q_ge_0.3": 0.2508
   },
   {
    "hgt": 0.02,
    "median_q": 3.0,
    "mean_log10_q": 0.3838,
    "share_q_ge_1": 0.9933,
    "share_q_ge_0.3": 1.0
   },
   {
    "hgt": 0.05,
    "median_q": 10.0,
    "mean_log10_q": 0.7847,
    "share_q_ge_1": 1.0,
    "share_q_ge_0.3": 1.0
   },
   {
    "hgt": 0.1,
    "median_q": 10.0,
    "mean_log10_q": 1.0,
    "share_q_ge_1": 1.0,
    "share_q_ge_0.3": 1.0
   },
   {
    "hgt": 0.2,
    "median_q": 10.0,
    "mean_log10_q": 1.0,
    "share_q_ge_1": 1.0,
    "share_q_ge_0.3": 1.0
   },
   {
    "hgt": 0.35,
    "median_q": 10.0,
    "mean_log10_q": 1.0,
    "share_q_ge_1": 1.0,
    "share_q_ge_0.3": 1.0
   },
   {
    "hgt": 0.5,
    "median_q": 10.0,
    "mean_log10_q": 1.0,
    "share_q_ge_1": 1.0,
    "share_q_ge_0.3": 1.0
   },
   {
    "hgt": 0.8,
    "median_q": 10.0,
    "mean_log10_q": 1.0,
    "share_q_ge_1": 1.0,
    "share_q_ge_0.3": 1.0
   }
  ],
  "estimated_hgt": 0.012,
  "estimated_hgt_by_median_q": 0.003,
  "how": "보간",
  "gates_passed": [
   "0.35 (크기(유전자군 수) 부풀기 시작)",
   "0.5 (확률 보정이 깨짐)",
   "0.8 (순위도 무너짐)"
  ],
  "gates_broken": []
 }
}
```

## per_root

```json
{
 "discoba": 0.012,
 "opisthokonta": 0.008
}
```

## 연결
- [[실험 목록]]
