---
유형: 실험
실행: quality_correction
산출: results/quality_correction/summary.json
tags:
  - 유형/실험
  - 실험/quality_correction
---

# 실험 · quality_correction

**산출물** `results/quality_correction/summary.json`

## 한눈에

| 항목 | 값 |
| --- | --- |
| families | 600 |
| reps | 3 |
| best_by_logloss | estimated |
| completeness_median_error | 0.0186 |

## generator

```json
{
 "M": 5.0,
 "hgt": 0.02,
 "ratio": 0.1,
 "incomplete": true
}
```

## aggregate

```json
{
 "none": {
  "auroc": 0.9858,
  "logloss": 0.1661,
  "size_bias": -0.0961
 },
 "tip_mult": {
  "auroc": 0.9857,
  "logloss": 0.158,
  "size_bias": -0.0785
 },
 "emission": {
  "auroc": 0.9873,
  "logloss": 0.1548,
  "size_bias": -0.0698
 },
 "estimated": {
  "auroc": 0.987,
  "logloss": 0.1541,
  "size_bias": -0.0664
 }
}
```

## runs

```json
[
 {
  "rep": 0,
  "way": "none",
  "auroc": 0.9800126473643797,
  "logloss": 0.20391681426967503,
  "size_bias": -0.11574630154908158
 },
 {
  "rep": 0,
  "way": "tip_mult",
  "auroc": 0.9795609557793938,
  "logloss": 0.19642175528863542,
  "size_bias": -0.10006096526866651
 },
 {
  "rep": 0,
  "way": "emission",
  "auroc": 0.9832535344866525,
  "logloss": 0.1910970001291086,
  "size_bias": -0.09234986050438335
 },
 {
  "rep": 0,
  "way": "estimated",
  "auroc": 0.982192059261936,
  "logloss": 0.1926026659277583,
  "size_bias": -0.08774753017279938,
  "completeness_median_error": 0.016255813953488407
 },
 {
  "rep": 1,
  "way": "none",
  "auroc": 0.9928301292152537,
  "logloss": 0.12777789607661058,
  "size_bias": -0.08384830790354793
 },
 {
  "rep": 1,
  "way": "tip_mult",
  "auroc": 0.9927513394264104,
  "logloss": 0.1181996834115004,
  "size_bias": -0.0639515353324718
 },
 {
  "rep": 1,
  "way": "emission",
  "auroc": 0.9924699473233983,
  "logloss": 0.1161558340814372,
  "size_bias": -0.05602149676559563
 },
 {
  "rep": 1,
  "way": "estimated",
  "auroc": 0.9927963621628922,
  "logloss": 0.11250018036256128,
  "size_bias": -0.052140888414884866,
  "completeness_median_error": 0.019777777777777783
 },
 {
  "rep": 2,
  "way": "none",
  "auroc": 0.9845236357101944,
  "logloss": 0.16660226484735177,
  "size_bias": -0.08855599896172166
 },
 {
  "rep": 2,
  "way": "tip_mult",
  "auroc": 0.9847370253484428,
  "logloss": 0.1594919613180779,
  "size_bias": -0.07156099794522537
 },
 {
  "rep": 2,
  "way": "emission",
  "auroc": 0.9862981390177338,
  "logloss": 0.15708553800822606,
  "size_bias": -0.060885518013766265
 },
 {
  "rep": 2,
  "way": "estimated",
  "auroc": 0.9859836700771571,
  "logloss": 0.1571844589220806,
  "size_bias": -0.05923512965773118,
  "completeness_median_error": 0.01860396039603973
 }
]
```

## 연결
- [[실험 목록]]
