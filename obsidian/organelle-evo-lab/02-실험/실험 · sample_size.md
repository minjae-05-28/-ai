---
유형: 실험
실행: sample_size
산출: results/sample_size/summary.json
tags:
  - 유형/실험
  - 실험/sample_size
---

# 실험 · sample_size

**산출물** `results/sample_size/summary.json`

## model

```json
{
 "ratio": null,
 "root": "stationary",
 "min_busco": 0,
 "drop_mag": false,
 "mult": 14.0,
 "tip_mult": 1.0
}
```

## aggregate

```json
{
 "spread_12": {
  "recon_auroc": 0.9646,
  "freq_auroc": 0.9315,
  "recon_logloss": 0.2856,
  "freq_logloss": 0.4804,
  "prior_logloss": 0.6875,
  "recon_size_bias": -0.1577,
  "recon_auroc_reached": 0.9911,
  "recon_logloss_reached": 0.1513,
  "recon_size_bias_reached": -0.1183,
  "reached_vs_true_root_jaccard": 0.9083,
  "reached_size_vs_true_root": -0.0448,
  "same_root_node_share": 0.0
 },
 "spread_50": {
  "recon_auroc": 0.9736,
  "freq_auroc": 0.9371,
  "recon_logloss": 0.2329,
  "freq_logloss": 0.389,
  "prior_logloss": 0.6875,
  "recon_size_bias": -0.1035,
  "recon_auroc_reached": 0.9954,
  "recon_logloss_reached": 0.0969,
  "recon_size_bias_reached": -0.0702,
  "reached_vs_true_root_jaccard": 0.9214,
  "reached_size_vs_true_root": -0.0358,
  "same_root_node_share": 0.0
 },
 "spread_300": {
  "recon_auroc": 0.9769,
  "freq_auroc": 0.9385,
  "recon_logloss": 0.2166,
  "freq_logloss": 0.3433,
  "prior_logloss": 0.6875,
  "recon_size_bias": -0.0993,
  "recon_auroc_reached": 0.9937,
  "recon_logloss_reached": 0.1023,
  "recon_size_bias_reached": -0.0766,
  "reached_vs_true_root_jaccard": 0.9323,
  "reached_size_vs_true_root": -0.0246,
  "same_root_node_share": 0.0
 },
 "spread_2323": {
  "recon_auroc": 0.9861,
  "freq_auroc": 0.9382,
  "recon_logloss": 0.1507,
  "freq_logloss": 0.3375,
  "prior_logloss": 0.6875,
  "recon_size_bias": -0.0864,
  "recon_auroc_reached": 0.9861,
  "recon_logloss_reached": 0.1507,
  "recon_size_bias_reached": -0.0864,
  "reached_vs_true_root_jaccard": 1.0,
  "reached_size_vs_true_root": 0.0,
  "same_root_node_share": 1.0
 },
 "clustered_12"
… (잘림 — 원본 파일 참조)
```

## runs

```json
[
 {
  "rep": 0,
  "n_alpha": 12,
  "pattern": "spread",
  "same_root_node": false,
  "reached_vs_true_root_jaccard": 0.9047619047619048,
  "reached_size_vs_true_root": -0.03571428571428571,
  "recon_auroc_reached": 0.9907896452790819,
  "recon_logloss_reached": 0.15112528433371336,
  "recon_size_bias_reached": -0.10816333912037036,
  "recon_auroc": 0.9598133410973085,
  "freq_auroc": 0.9302131858178054,
  "recon_logloss": 0.3040745577074267,
  "freq_logloss": 0.48683642186587495,
  "prior_logloss": 0.6877293893152671,
  "recon_size_bias": -0.1400146484375
 },
 {
  "rep": 0,
  "n_alpha": 12,
  "pattern": "clustered",
  "same_root_node": false,
  "reached_vs_true_root_jaccard": 0.9047619047619048,
  "reached_size_vs_true_root": -0.03571428571428571,
  "recon_auroc_reached": 0.9753928664580073,
  "recon_logloss_reached": 0.21499733680045757,
  "recon_size_bias_reached": -0.1278235117594401,
  "recon_auroc": 0.9479004917184265,
  "freq_auroc": 0.9000064699792961,
  "recon_logloss": 0.3232044492765708,
  "freq_logloss": 0.6816680649343198,
  "prior_logloss": 0.6877293893152671,
  "recon_size_bias": -0.15897267205374582
 },
 {
  "rep": 0,
  "n_alpha": 50,
  "pattern": "spread",
  "same_root_node": false,
  "reached_vs_true_root_jaccard": 0.9090909090909091,
  "reached_size_vs_true_root": -0.03125,
  "recon_auroc_reached": 0.9951148816987184,
  "recon_logloss_reached": 0.10455271813782747,
  "recon_size_bias_reached": -0.08010934574812788,
  "recon_auroc": 0.9669626682194618,
  "freq_auroc": 0.9391741071428571,
  "recon_logloss": 0.26698557438395804,
  "freq_logloss": 0.376590639
… (잘림 — 원본 파일 참조)
```

## 연결
- [[실험 목록]]
