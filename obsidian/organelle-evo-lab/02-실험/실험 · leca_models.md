---
유형: 실험
실행: leca_models
산출: results/leca_models/summary.json
tags:
  - 유형/실험
  - 실험/leca_models
---

# 실험 · leca_models

**산출물** `results/leca_models/summary.json`

## 한눈에

| 항목 | 값 |
| --- | --- |
| preregistration | docs/preregistration/2026-10-08_leca_model_variants.md |
| n_calibration | 2688 |
| n_test | 2801 |
| lecas_calibration | 1905 |
| lecas_test | 1953 |
| best_tree_model_on_calibration | M7 |
| chosen_by_calibration_auroc | S2 |
| verdict_on_test | 무승부 |

## learned_coefficients

```json
{
 "S1": [
  3.1069,
  4.762
 ],
 "S2": [
  2.8013,
  0.0668,
  4.6369
 ],
 "S3": [
  2.5822,
  0.0802,
  4.3004
 ]
}
```

## fit

```json
{
 "M0 discoba": {
  "ratio": null,
  "root": "stationary",
  "loglik": -601679.6,
  "sum_posterior": 3951.3
 },
 "M1 discoba": {
  "ratio": null,
  "root": 0.5,
  "loglik": -602117.8,
  "sum_posterior": 5620.6
 },
 "M2 discoba": {
  "ratio": null,
  "root": "empirical",
  "loglik": -597439.9,
  "sum_posterior": 4422.5
 },
 "M3 discoba": {
  "ratio": 0.3,
  "root": "stationary",
  "loglik": -609686.9,
  "sum_posterior": 4394.3
 },
 "M4 discoba": {
  "ratio": 0.1,
  "root": "stationary",
  "loglik": -619877.8,
  "sum_posterior": 4868.8
 },
 "M5 discoba": {
  "ratio": 0.1,
  "root": 0.5,
  "loglik": -613995.1,
  "sum_posterior": 6918.1
 },
 "M6 discoba": {
  "ratio": 0.01,
  "root": 0.5,
  "loglik": -632239.0,
  "sum_posterior": 8467.3
 },
 "M7 discoba": {
  "ratio": [
   0.20000000298023224
  ],
  "root": "stationary",
  "loglik": -624164.2,
  "sum_posterior": 4369.7
 },
 "M8 discoba": {
  "ratio": null,
  "root": 0.3,
  "loglik": -601638.8,
  "sum_posterior": 4658.8
 },
 "M9 discoba": {
  "ratio": [
   0.10000000149011612
  ],
  "root": 0.3,
  "loglik": -621891.6,
  "sum_posterior": 5389.8
 },
 "M0 opisthokonta": {
  "ratio": null,
  "root": "stationary",
  "loglik": -601679.6,
  "sum_posterior": 4601.3
 },
 "M1 opisthokonta": {
  "ratio": null,
  "root": 0.5,
  "loglik": -600806.0,
  "sum_posterior": 6378.6
 },
 "M2 opisthokonta": {
  "ratio": null,
  "root": "empirical",
  "loglik": -596672.8,
  "sum_posterior": 5017.1
 },
 "M3 opisthokonta": {
  "ratio": 0.3,
  "root": "stationary",
  "loglik": -609686.8,
  "sum_posterior": 5035.8
 },
 "M4 opisthokonta": {
  "ratio": 0.1
… (잘림 — 원본 파일 참조)
```

## models

```json
{
 "M0": {
  "calibration_auroc": 0.8662,
  "test_auroc": 0.8649,
  "test_frequency_auroc": 0.9568,
  "test_minus_frequency": -0.0919,
  "test_minus_frequency_ci95": [
   -0.104,
   -0.0804
  ],
  "test_stratified_auroc": 0.5414,
  "test_size_ratio": 0.711
 },
 "M1": {
  "calibration_auroc": 0.7976,
  "test_auroc": 0.7944,
  "test_frequency_auroc": 0.9568,
  "test_minus_frequency": -0.1624,
  "test_minus_frequency_ci95": [
   -0.1788,
   -0.1467
  ],
  "test_stratified_auroc": 0.5185,
  "test_size_ratio": 0.853
 },
 "M2": {
  "calibration_auroc": 0.8567,
  "test_auroc": 0.8497,
  "test_frequency_auroc": 0.9568,
  "test_minus_frequency": -0.1071,
  "test_minus_frequency_ci95": [
   -0.1205,
   -0.0946
  ],
  "test_stratified_auroc": 0.506,
  "test_size_ratio": 0.793
 },
 "M3": {
  "calibration_auroc": 0.9011,
  "test_auroc": 0.8986,
  "test_frequency_auroc": 0.9568,
  "test_minus_frequency": -0.0582,
  "test_minus_frequency_ci95": [
   -0.0673,
   -0.0494
  ],
  "test_stratified_auroc": 0.5467,
  "test_size_ratio": 0.794
 },
 "M4": {
  "calibration_auroc": 0.9092,
  "test_auroc": 0.9035,
  "test_frequency_auroc": 0.9568,
  "test_minus_frequency": -0.0533,
  "test_minus_frequency_ci95": [
   -0.0616,
   -0.0449
  ],
  "test_stratified_auroc": 0.5368,
  "test_size_ratio": 0.868
 },
 "M5": {
  "calibration_auroc": 0.8941,
  "test_auroc": 0.8903,
  "test_frequency_auroc": 0.9568,
  "test_minus_frequency": -0.0665,
  "test_minus_frequency_ci95": [
   -0.0768,
   -0.0568
  ],
  "test_stratified_auroc": 0.5376,
  "test_size_ratio": 1.081
 },
 "M6": {
  "calibration_auroc": 0.8856,

… (잘림 — 원본 파일 참조)
```

## 연결
- [[실험 목록]]
