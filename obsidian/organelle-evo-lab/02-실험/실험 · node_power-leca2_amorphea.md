---
유형: 실험
실행: node_power/leca2_amorphea
산출: results/node_power/leca2_amorphea/summary.json
tags:
  - 유형/실험
  - 실험/node_power-leca2_amorphea
---

# 실험 · node_power-leca2_amorphea

**산출물** `results/node_power/leca2_amorphea/summary.json`

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
 "leca2_amorphea (표본이 도달한 마디)": {
  "recon_auroc": 0.8509,
  "freq_auroc": 0.7335,
  "recon_logloss": 0.5017,
  "freq_logloss": 0.9055,
  "prior_logloss": 0.6929,
  "recon_size_bias": 0.0405,
  "freq_size_bias": -0.6081,
  "n_tips": 250,
  "auroc_margin": 0.1174,
  "logloss_margin": 0.4038,
  "auroc_headroom": 0.2665,
  "verdict": "계통수가 도움이 됨"
 },
 "leca2_amorphea 뿌리 아래 큰 쪽 (156종)": {
  "recon_auroc": 0.8534,
  "freq_auroc": 0.7515,
  "recon_logloss": 0.4939,
  "freq_logloss": 0.8648,
  "prior_logloss": 0.6922,
  "recon_size_bias": 0.0252,
  "freq_size_bias": -0.5975,
  "n_tips": 156,
  "auroc_margin": 0.1019,
  "logloss_margin": 0.3709,
  "auroc_headroom": 0.2485,
  "verdict": "계통수가 도움이 됨"
 },
 "Alveolata": {
  "recon_auroc": 0.9016,
  "freq_auroc": 0.8567,
  "recon_logloss": 0.3346,
  "freq_logloss": 0.5589,
  "prior_logloss": 0.6289,
  "recon_size_bias": 0.0334,
  "freq_size_bias": -0.4567,
  "n_tips": 30,
  "auroc_margin": 0.0449,
  "logloss_margin": 0.2243,
  "auroc_headroom": 0.1433,
  "verdict": "계통수가 도움이 됨"
 },
 "Amoebozoa": {
  "recon_auroc": 0.8697,
  "freq_auroc": 0.7908,
  "recon_logloss": 0.4239,
  "freq_logloss": 1.0555,
  "prior_logloss": 0.6678,
  "recon_size_bias": 0.0556,
  "freq_size_bias": -0.5029,
  "n_tips": 12,
  "auroc_margin": 0.0789,
  "logloss_margin": 0.6316,
  "auroc_headroom": 0.2092,
  "verdict": "계통수가 도움이 됨"
 },
 "Discoba": {
  "recon_auroc": 0.9041,
  "freq_auroc": 0.7956,
  "recon_logloss": 0.3233,
  "freq_logloss": 0.8728,
  "prior_logloss": 0.6169,
  "recon_size_bias": 0.0396,
  "freq_size_bias": -0.4123,
  "n_tips": 24,
  "auroc_margin
… (잘림 — 원본 파일 참조)
```

## runs

```json
[
 {
  "rep": 0,
  "node": "leca2_amorphea (표본이 도달한 마디)",
  "n_tips": 250,
  "recon_auroc": 0.8482908654447251,
  "freq_auroc": 0.7237409667175114,
  "recon_logloss": 0.512074453510404,
  "freq_logloss": 0.9000610571755597,
  "prior_logloss": 0.6930346763408154,
  "recon_size_bias": 0.06355324372422272,
  "freq_size_bias": -0.6145583756345177,
  "true_share": 0.4925
 },
 {
  "rep": 0,
  "node": "leca2_amorphea 뿌리 아래 큰 쪽 (156종)",
  "n_tips": 156,
  "recon_auroc": 0.850260024118179,
  "freq_auroc": 0.7404092553512209,
  "recon_logloss": 0.5044661059947156,
  "freq_logloss": 0.8536792429891578,
  "prior_logloss": 0.6906951757946529,
  "recon_size_bias": 0.05607670609669019,
  "freq_size_bias": -0.6008064516129032,
  "true_share": 0.465
 },
 {
  "rep": 0,
  "node": "Alveolata",
  "n_tips": 30,
  "recon_auroc": 0.8949636363636364,
  "freq_auroc": 0.8487490909090909,
  "recon_logloss": 0.34559914896841293,
  "freq_logloss": 0.5679619186035013,
  "prior_logloss": 0.6210863745552453,
  "recon_size_bias": 0.041825927734375,
  "freq_size_bias": -0.4635999999999999,
  "true_share": 0.3125
 },
 {
  "rep": 0,
  "node": "Amoebozoa",
  "n_tips": 12,
  "recon_auroc": 0.8554862933080833,
  "freq_auroc": 0.7846546860513286,
  "recon_logloss": 0.45035401046124207,
  "freq_logloss": 1.113607561377461,
  "prior_logloss": 0.6681856613667344,
  "recon_size_bias": 0.03319409729200161,
  "freq_size_bias": -0.5468917470525188,
  "true_share": 0.38875
 },
 {
  "rep": 0,
  "node": "Discoba",
  "n_tips": 24,
  "recon_auroc": 0.885393948932407,
  "freq_auroc": 0.7575413509604215,
  "recon_logloss": 0.35
… (잘림 — 원본 파일 참조)
```

## 연결
- [[실험 목록]]
