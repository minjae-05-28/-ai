---
유형: 실험
실행: node_power/leca2_metamonada
산출: results/node_power/leca2_metamonada/summary.json
tags:
  - 유형/실험
  - 실험/node_power-leca2_metamonada
---

# 실험 · node_power-leca2_metamonada

**산출물** `results/node_power/leca2_metamonada/summary.json`

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
 "leca2_metamonada (표본이 도달한 마디)": {
  "recon_auroc": 0.8247,
  "freq_auroc": 0.7205,
  "recon_logloss": 0.5007,
  "freq_logloss": 0.935,
  "prior_logloss": 0.6929,
  "recon_size_bias": 0.0636,
  "freq_size_bias": -0.6169,
  "n_tips": 250,
  "auroc_margin": 0.1042,
  "logloss_margin": 0.4343,
  "auroc_headroom": 0.2795,
  "verdict": "계통수가 도움이 됨"
 },
 "leca2_metamonada 뿌리 아래 큰 쪽 (239종)": {
  "recon_auroc": 0.8291,
  "freq_auroc": 0.7463,
  "recon_logloss": 0.4992,
  "freq_logloss": 0.8563,
  "prior_logloss": 0.6922,
  "recon_size_bias": 0.0477,
  "freq_size_bias": -0.5923,
  "n_tips": 239,
  "auroc_margin": 0.0828,
  "logloss_margin": 0.3571,
  "auroc_headroom": 0.2537,
  "verdict": "계통수가 도움이 됨"
 },
 "Alveolata": {
  "recon_auroc": 0.9076,
  "freq_auroc": 0.8654,
  "recon_logloss": 0.3036,
  "freq_logloss": 0.5095,
  "prior_logloss": 0.611,
  "recon_size_bias": 0.0706,
  "freq_size_bias": -0.4362,
  "n_tips": 30,
  "auroc_margin": 0.0422,
  "logloss_margin": 0.2059,
  "auroc_headroom": 0.1346,
  "verdict": "계통수가 도움이 됨"
 },
 "Amoebozoa": {
  "recon_auroc": 0.9162,
  "freq_auroc": 0.8343,
  "recon_logloss": 0.3051,
  "freq_logloss": 0.7287,
  "prior_logloss": 0.6261,
  "recon_size_bias": 0.0787,
  "freq_size_bias": -0.4117,
  "n_tips": 12,
  "auroc_margin": 0.0819,
  "logloss_margin": 0.4236,
  "auroc_headroom": 0.1657,
  "verdict": "계통수가 도움이 됨"
 },
 "Discoba": {
  "recon_auroc": 0.8832,
  "freq_auroc": 0.7725,
  "recon_logloss": 0.373,
  "freq_logloss": 1.0244,
  "prior_logloss": 0.6344,
  "recon_size_bias": 0.1175,
  "freq_size_bias": -0.4562,
  "n_tips": 24,
  "auroc_margi
… (잘림 — 원본 파일 참조)
```

## runs

```json
[
 {
  "rep": 0,
  "node": "leca2_metamonada (표본이 도달한 마디)",
  "n_tips": 250,
  "recon_auroc": 0.8198500912705359,
  "freq_auroc": 0.7156516466204896,
  "recon_logloss": 0.5002369323052608,
  "freq_logloss": 0.9283416851281462,
  "prior_logloss": 0.6930346763408154,
  "recon_size_bias": 0.07392209435477474,
  "freq_size_bias": -0.6239695431472081,
  "true_share": 0.4925
 },
 {
  "rep": 0,
  "node": "leca2_metamonada 뿌리 아래 큰 쪽 (239종)",
  "n_tips": 239,
  "recon_auroc": 0.82271176234444,
  "freq_auroc": 0.7398007828181453,
  "recon_logloss": 0.4978672228566938,
  "freq_logloss": 0.8586109840266535,
  "prior_logloss": 0.6913460990017393,
  "recon_size_bias": 0.048499817543841424,
  "freq_size_bias": -0.6028109142704531,
  "true_share": 0.47
 },
 {
  "rep": 0,
  "node": "Alveolata",
  "n_tips": 30,
  "recon_auroc": 0.8947056361607143,
  "freq_auroc": 0.8482491629464286,
  "recon_logloss": 0.3213716090869002,
  "freq_logloss": 0.5214758264827077,
  "prior_logloss": 0.5929533174474746,
  "recon_size_bias": 0.09482785633632115,
  "freq_size_bias": -0.4360119047619047,
  "true_share": 0.28
 },
 {
  "rep": 0,
  "node": "Amoebozoa",
  "n_tips": 12,
  "recon_auroc": 0.9163035651986728,
  "freq_auroc": 0.8257669667975563,
  "recon_logloss": 0.30434952741126836,
  "freq_logloss": 0.7217441176374092,
  "prior_logloss": 0.6119197070867419,
  "recon_size_bias": 0.0965571106716805,
  "freq_size_bias": -0.41424619640387267,
  "true_share": 0.30125
 },
 {
  "rep": 0,
  "node": "Discoba",
  "n_tips": 24,
  "recon_auroc": 0.8765549283109357,
  "freq_auroc": 0.7780315303420664,
  "recon_logloss":
… (잘림 — 원본 파일 참조)
```

## 연결
- [[실험 목록]]
