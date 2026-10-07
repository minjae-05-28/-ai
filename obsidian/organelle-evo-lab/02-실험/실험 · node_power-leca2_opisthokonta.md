---
유형: 실험
실행: node_power/leca2_opisthokonta
산출: results/node_power/leca2_opisthokonta/summary.json
tags:
  - 유형/실험
  - 실험/node_power-leca2_opisthokonta
---

# 실험 · node_power-leca2_opisthokonta

**산출물** `results/node_power/leca2_opisthokonta/summary.json`

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
 "leca2_opisthokonta (표본이 도달한 마디)": {
  "recon_auroc": 0.863,
  "freq_auroc": 0.7404,
  "recon_logloss": 0.4554,
  "freq_logloss": 0.9042,
  "prior_logloss": 0.6929,
  "recon_size_bias": 0.0431,
  "freq_size_bias": -0.6091,
  "n_tips": 250,
  "auroc_margin": 0.1226,
  "logloss_margin": 0.4488,
  "auroc_headroom": 0.2596,
  "verdict": "계통수가 도움이 됨"
 },
 "leca2_opisthokonta 뿌리 아래 큰 쪽 (169종)": {
  "recon_auroc": 0.8645,
  "freq_auroc": 0.7301,
  "recon_logloss": 0.4506,
  "freq_logloss": 0.9175,
  "prior_logloss": 0.693,
  "recon_size_bias": 0.035,
  "freq_size_bias": -0.6129,
  "n_tips": 169,
  "auroc_margin": 0.1344,
  "logloss_margin": 0.4669,
  "auroc_headroom": 0.2699,
  "verdict": "계통수가 도움이 됨"
 },
 "Alveolata": {
  "recon_auroc": 0.9295,
  "freq_auroc": 0.8882,
  "recon_logloss": 0.2626,
  "freq_logloss": 0.4739,
  "prior_logloss": 0.6075,
  "recon_size_bias": 0.049,
  "freq_size_bias": -0.4177,
  "n_tips": 30,
  "auroc_margin": 0.0413,
  "logloss_margin": 0.2113,
  "auroc_headroom": 0.1118,
  "verdict": "계통수가 도움이 됨"
 },
 "Amoebozoa": {
  "recon_auroc": 0.8913,
  "freq_auroc": 0.8031,
  "recon_logloss": 0.3745,
  "freq_logloss": 0.9456,
  "prior_logloss": 0.6625,
  "recon_size_bias": 0.0321,
  "freq_size_bias": -0.4806,
  "n_tips": 12,
  "auroc_margin": 0.0882,
  "logloss_margin": 0.5711,
  "auroc_headroom": 0.1969,
  "verdict": "계통수가 도움이 됨"
 },
 "Discoba": {
  "recon_auroc": 0.9048,
  "freq_auroc": 0.7913,
  "recon_logloss": 0.3145,
  "freq_logloss": 0.8512,
  "prior_logloss": 0.6046,
  "recon_size_bias": 0.0069,
  "freq_size_bias": -0.4061,
  "n_tips": 24,
  "auroc_ma
… (잘림 — 원본 파일 참조)
```

## runs

```json
[
 {
  "rep": 0,
  "node": "leca2_opisthokonta (표본이 도달한 마디)",
  "n_tips": 250,
  "recon_auroc": 0.8681422069965742,
  "freq_auroc": 0.7403853367007577,
  "recon_logloss": 0.41698442384608825,
  "freq_logloss": 0.8949610315763921,
  "prior_logloss": 0.6930346763408154,
  "recon_size_bias": 0.0538567092818052,
  "freq_size_bias": -0.6221827411167512,
  "true_share": 0.4925
 },
 {
  "rep": 0,
  "node": "leca2_opisthokonta 뿌리 아래 큰 쪽 (169종)",
  "n_tips": 169,
  "recon_auroc": 0.8695653534045336,
  "freq_auroc": 0.7357677797173264,
  "recon_logloss": 0.4128425068194065,
  "freq_logloss": 0.911724629515295,
  "prior_logloss": 0.6926189625486372,
  "recon_size_bias": 0.04173472007731751,
  "freq_size_bias": -0.6294512484136814,
  "true_share": 0.48375
 },
 {
  "rep": 0,
  "node": "Alveolata",
  "n_tips": 30,
  "recon_auroc": 0.9214492753623188,
  "freq_auroc": 0.858768115942029,
  "recon_logloss": 0.2685353253636913,
  "freq_logloss": 0.5223502692245587,
  "prior_logloss": 0.5998980192621342,
  "recon_size_bias": 0.02361768639605978,
  "freq_size_bias": -0.42217391304347823,
  "true_share": 0.2875
 },
 {
  "rep": 0,
  "node": "Amoebozoa",
  "n_tips": 12,
  "recon_auroc": 0.8948601566886815,
  "freq_auroc": 0.777056204711356,
  "recon_logloss": 0.36085691727472297,
  "freq_logloss": 1.000517361087268,
  "prior_logloss": 0.6602728288381041,
  "recon_size_bias": 0.011387972223678692,
  "freq_size_bias": -0.4924496644295302,
  "true_share": 0.3725
 },
 {
  "rep": 0,
  "node": "Discoba",
  "n_tips": 24,
  "recon_auroc": 0.8912128146453089,
  "freq_auroc": 0.7632875667429443,
  "recon_lo
… (잘림 — 원본 파일 참조)
```

## 연결
- [[실험 목록]]
