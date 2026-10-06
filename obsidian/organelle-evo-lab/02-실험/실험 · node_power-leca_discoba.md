---
유형: 실험
실행: node_power/leca_discoba
산출: results/node_power/leca_discoba/summary.json
tags:
  - 유형/실험
  - 실험/node_power-leca_discoba
---

# 실험 · node_power-leca_discoba

**산출물** `results/node_power/leca_discoba/summary.json`

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
 "leca_discoba (표본이 도달한 마디)": {
  "recon_auroc": 0.6196,
  "freq_auroc": 0.5554,
  "recon_logloss": 0.7701,
  "freq_logloss": 1.0343,
  "prior_logloss": 0.6929,
  "recon_size_bias": 0.3428,
  "freq_size_bias": -0.6495,
  "n_tips": 256,
  "auroc_margin": 0.0642,
  "logloss_margin": 0.2642,
  "auroc_headroom": 0.4446,
  "verdict": "계통수가 도움이 됨"
 },
 "leca_discoba 뿌리 아래 큰 쪽 (232종)": {
  "recon_auroc": 0.7089,
  "freq_auroc": 0.6824,
  "recon_logloss": 0.6994,
  "freq_logloss": 0.7218,
  "prior_logloss": 0.6615,
  "recon_size_bias": 0.4708,
  "freq_size_bias": -0.5226,
  "n_tips": 232,
  "auroc_margin": 0.0265,
  "logloss_margin": 0.0224,
  "auroc_headroom": 0.3176,
  "verdict": "계통수가 도움이 됨"
 },
 "Alveolata": {
  "recon_auroc": 0.8122,
  "freq_auroc": 0.7548,
  "recon_logloss": 0.4446,
  "freq_logloss": 0.4809,
  "prior_logloss": 0.5519,
  "recon_size_bias": 0.3966,
  "freq_size_bias": -0.2454,
  "n_tips": 32,
  "auroc_margin": 0.0574,
  "logloss_margin": 0.0363,
  "auroc_headroom": 0.2452,
  "verdict": "계통수가 도움이 됨"
 },
 "Amoebozoa": {
  "recon_auroc": 0.8261,
  "freq_auroc": 0.7633,
  "recon_logloss": 0.4281,
  "freq_logloss": 0.5345,
  "prior_logloss": 0.5177,
  "recon_size_bias": 0.5745,
  "freq_size_bias": 0.0181,
  "n_tips": 9,
  "auroc_margin": 0.0628,
  "logloss_margin": 0.1064,
  "auroc_headroom": 0.2367,
  "verdict": "계통수가 도움이 됨"
 },
 "Discoba": {
  "recon_auroc": 0.7072,
  "freq_auroc": 0.6611,
  "recon_logloss": 0.6955,
  "freq_logloss": 1.1911,
  "prior_logloss": 0.6557,
  "recon_size_bias": 0.5142,
  "freq_size_bias": -0.5549,
  "n_tips": 24,
  "auroc_margin": 0.0
… (잘림 — 원본 파일 참조)
```

## runs

```json
[
 {
  "rep": 0,
  "node": "leca_discoba (표본이 도달한 마디)",
  "n_tips": 256,
  "recon_auroc": 0.6128003800855193,
  "freq_auroc": 0.5459478382636093,
  "recon_logloss": 0.7974933786540168,
  "freq_logloss": 1.0234046191904094,
  "prior_logloss": 0.6930346763408154,
  "recon_size_bias": 0.3741566614451142,
  "freq_size_bias": -0.6505889118020305,
  "true_share": 0.4925
 },
 {
  "rep": 0,
  "node": "leca_discoba 뿌리 아래 큰 쪽 (232종)",
  "n_tips": 232,
  "recon_auroc": 0.7047235890403593,
  "freq_auroc": 0.6549870936516899,
  "recon_logloss": 0.718358682696562,
  "freq_logloss": 0.7350626841146968,
  "prior_logloss": 0.6576117198466398,
  "recon_size_bias": 0.4843707441472683,
  "freq_size_bias": -0.5267417311752287,
  "true_share": 0.3675
 },
 {
  "rep": 0,
  "node": "Alveolata",
  "n_tips": 32,
  "recon_auroc": 0.7717980809345014,
  "freq_auroc": 0.7267417605340009,
  "recon_logloss": 0.4809714113091832,
  "freq_logloss": 0.48775924270672816,
  "prior_logloss": 0.5452476702809597,
  "recon_size_bias": 0.40525947733128326,
  "freq_size_bias": -0.23071808510638298,
  "true_share": 0.235
 },
 {
  "rep": 0,
  "node": "Amoebozoa",
  "n_tips": 9,
  "recon_auroc": 0.805578944240275,
  "freq_auroc": 0.7327267684322097,
  "recon_logloss": 0.4447813315833264,
  "freq_logloss": 0.5602743373073662,
  "prior_logloss": 0.4951596662623352,
  "recon_size_bias": 0.6580128274905453,
  "freq_size_bias": 0.09200283085633412,
  "true_share": 0.19625
 },
 {
  "rep": 0,
  "node": "Discoba",
  "n_tips": 24,
  "recon_auroc": 0.6815829098437794,
  "freq_auroc": 0.6682362668387513,
  "recon_logloss": 0.724541
… (잘림 — 원본 파일 참조)
```

## 연결
- [[실험 목록]]
