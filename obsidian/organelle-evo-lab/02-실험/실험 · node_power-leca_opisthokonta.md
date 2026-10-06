---
유형: 실험
실행: node_power/leca_opisthokonta
산출: results/node_power/leca_opisthokonta/summary.json
tags:
  - 유형/실험
  - 실험/node_power-leca_opisthokonta
---

# 실험 · node_power-leca_opisthokonta

**산출물** `results/node_power/leca_opisthokonta/summary.json`

## 한눈에

| 항목 | 값 |
| --- | --- |
| families | 800 |
| reps | 3 |
| note | 알려진 정답으로 각 마디의 조상을 직접 채점. 잎 숨기기와 달리 꽉 짜인 분류군에서도 변별력이 있음. |

## generator

```json
{
 "M": 5.0,
 "hgt": 0.02,
 "ratio": 0.1,
 "incomplete": true
}
```

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
 "leca_opisthokonta (표본이 도달한 마디)": {
  "recon_auroc": 0.8227,
  "freq_auroc": 0.6721,
  "recon_logloss": 0.7027,
  "freq_logloss": 0.8105,
  "prior_logloss": 0.6929,
  "recon_size_bias": -0.3804,
  "freq_size_bias": -0.5087,
  "n_tips": 251,
  "auroc_margin": 0.1506,
  "logloss_margin": 0.1078,
  "auroc_headroom": 0.3279,
  "verdict": "계통수가 도움이 됨"
 },
 "leca_opisthokonta 뿌리 아래 큰 쪽 (163종)": {
  "recon_auroc": 0.8221,
  "freq_auroc": 0.615,
  "recon_logloss": 0.5721,
  "freq_logloss": 0.9069,
  "prior_logloss": 0.6902,
  "recon_size_bias": -0.2598,
  "freq_size_bias": -0.6015,
  "n_tips": 163,
  "auroc_margin": 0.2071,
  "logloss_margin": 0.3348,
  "auroc_headroom": 0.385,
  "verdict": "계통수가 도움이 됨"
 },
 "Alveolata": {
  "recon_auroc": 0.8515,
  "freq_auroc": 0.7785,
  "recon_logloss": 0.3614,
  "freq_logloss": 0.477,
  "prior_logloss": 0.5494,
  "recon_size_bias": -0.0373,
  "freq_size_bias": -0.2552,
  "n_tips": 32,
  "auroc_margin": 0.073,
  "logloss_margin": 0.1156,
  "auroc_headroom": 0.2215,
  "verdict": "계통수가 도움이 됨"
 },
 "Amoebozoa": {
  "recon_auroc": 0.8441,
  "freq_auroc": 0.7292,
  "recon_logloss": 0.3741,
  "freq_logloss": 0.6395,
  "prior_logloss": 0.5654,
  "recon_size_bias": -0.0081,
  "freq_size_bias": -0.163,
  "n_tips": 9,
  "auroc_margin": 0.1149,
  "logloss_margin": 0.2654,
  "auroc_headroom": 0.2708,
  "verdict": "계통수가 도움이 됨"
 },
 "Discoba": {
  "recon_auroc": 0.8138,
  "freq_auroc": 0.7205,
  "recon_logloss": 0.3887,
  "freq_logloss": 0.6721,
  "prior_logloss": 0.533,
  "recon_size_bias": -0.0099,
  "freq_size_bias": -0.2495,
  "n_tips": 24,
  "auroc_ma
… (잘림 — 원본 파일 참조)
```

## runs

```json
[
 {
  "rep": 0,
  "node": "leca_opisthokonta (표본이 도달한 마디)",
  "n_tips": 251,
  "recon_auroc": 0.8053999649921232,
  "freq_auroc": 0.6688223600310069,
  "recon_logloss": 0.7117711682817753,
  "freq_logloss": 0.7977783636992463,
  "prior_logloss": 0.6930346763408154,
  "recon_size_bias": -0.38098802905397366,
  "freq_size_bias": -0.5033369061823771,
  "true_share": 0.4925
 },
 {
  "rep": 0,
  "node": "leca_opisthokonta 뿌리 아래 큰 쪽 (163종)",
  "n_tips": 163,
  "recon_auroc": 0.8087350539700194,
  "freq_auroc": 0.6081138299754797,
  "recon_logloss": 0.5860795244895144,
  "freq_logloss": 0.8899620790545311,
  "prior_logloss": 0.6876245064056857,
  "recon_size_bias": -0.2559766716131285,
  "freq_size_bias": -0.5980566884875073,
  "true_share": 0.4475
 },
 {
  "rep": 0,
  "node": "Alveolata",
  "n_tips": 32,
  "recon_auroc": 0.8306048387096774,
  "freq_auroc": 0.7544041218637992,
  "recon_logloss": 0.3714308694395004,
  "freq_logloss": 0.4815764646529448,
  "prior_logloss": 0.5331638407372986,
  "recon_size_bias": -0.019455464680989583,
  "freq_size_bias": -0.23541666666666666,
  "true_share": 0.225
 },
 {
  "rep": 0,
  "node": "Amoebozoa",
  "n_tips": 9,
  "recon_auroc": 0.8249594539802676,
  "freq_auroc": 0.6872465873766725,
  "recon_logloss": 0.38519363795860045,
  "freq_logloss": 0.7074982879151085,
  "prior_logloss": 0.5567751167156652,
  "recon_size_bias": -0.023107723313934948,
  "freq_size_bias": -0.15759637188208614,
  "true_share": 0.245
 },
 {
  "rep": 0,
  "node": "Discoba",
  "n_tips": 24,
  "recon_auroc": 0.7939080491559957,
  "freq_auroc": 0.6860866037927188,
  "recon
… (잘림 — 원본 파일 참조)
```

## 연결
- [[실험 목록]]
