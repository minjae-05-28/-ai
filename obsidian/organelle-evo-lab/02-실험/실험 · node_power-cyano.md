---
유형: 실험
실행: node_power/cyano
산출: results/node_power/cyano/summary.json
tags:
  - 유형/실험
  - 실험/node_power-cyano
---

# 실험 · node_power-cyano

**산출물** `results/node_power/cyano/summary.json`

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
 "cyano (표본이 도달한 마디)": {
  "recon_auroc": 0.9954,
  "freq_auroc": 0.9756,
  "recon_logloss": 0.0733,
  "freq_logloss": 0.1787,
  "prior_logloss": 0.6611,
  "recon_size_bias": -0.034,
  "freq_size_bias": -0.0627,
  "n_tips": 162,
  "auroc_margin": 0.0198,
  "logloss_margin": 0.1054,
  "auroc_headroom": 0.0244,
  "verdict": "계통수가 도움이 됨"
 },
 "cyano 뿌리 아래 큰 쪽 (159종)": {
  "recon_auroc": 0.9986,
  "freq_auroc": 0.9885,
  "recon_logloss": 0.0335,
  "freq_logloss": 0.1146,
  "prior_logloss": 0.6573,
  "recon_size_bias": -0.0168,
  "freq_size_bias": -0.0434,
  "n_tips": 159,
  "auroc_margin": 0.0101,
  "logloss_margin": 0.0811,
  "auroc_headroom": 0.0115,
  "verdict": "계통수가 도움이 됨"
 }
}
```

## runs

```json
[
 {
  "rep": 0,
  "node": "cyano (표본이 도달한 마디)",
  "n_tips": 162,
  "recon_auroc": 0.9979017467098701,
  "freq_auroc": 0.980809581794041,
  "recon_logloss": 0.0624307783180484,
  "freq_logloss": 0.1479227230329431,
  "prior_logloss": 0.6466694040658458,
  "recon_size_bias": -0.033750144384240593,
  "freq_size_bias": -0.04964821452276648,
  "true_share": 0.34875
 },
 {
  "rep": 0,
  "node": "cyano 뿌리 아래 큰 쪽 (159종)",
  "n_tips": 159,
  "recon_auroc": 0.997967142383007,
  "freq_auroc": 0.9905686469742229,
  "recon_logloss": 0.03270042844606905,
  "freq_logloss": 0.09201785441243623,
  "prior_logloss": 0.6442963757652279,
  "recon_size_bias": -0.025996774866961052,
  "freq_size_bias": -0.03887521647981021,
  "true_share": 0.345
 },
 {
  "rep": 1,
  "node": "cyano (표본이 도달한 마디)",
  "n_tips": 162,
  "recon_auroc": 0.9954836056876061,
  "freq_auroc": 0.9706600169779287,
  "recon_logloss": 0.07949954901010642,
  "freq_logloss": 0.2032816342829679,
  "prior_logloss": 0.664064126564108,
  "recon_size_bias": -0.046714180394222864,
  "freq_size_bias": -0.07395224171539976,
  "true_share": 0.38
 },
 {
  "rep": 1,
  "node": "cyano 뿌리 아래 큰 쪽 (159종)",
  "n_tips": 159,
  "recon_auroc": 0.9989259942943447,
  "freq_auroc": 0.9842121161268669,
  "recon_logloss": 0.038568633920722274,
  "freq_logloss": 0.13430243624002583,
  "prior_logloss": 0.658287056537548,
  "recon_size_bias": -0.0190196926310911,
  "freq_size_bias": -0.0449845432256687,
  "true_share": 0.36875
 },
 {
  "rep": 2,
  "node": "cyano (표본이 도달한 마디)",
  "n_tips": 162,
  "recon_auroc": 0.9929222687843378,
  "freq_auroc": 0.975205130
… (잘림 — 원본 파일 참조)
```

## 연결
- [[실험 목록]]
