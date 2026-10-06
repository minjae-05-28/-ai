---
유형: 실험
실행: node_power/fungi
산출: results/node_power/fungi/summary.json
tags:
  - 유형/실험
  - 실험/node_power-fungi
---

# 실험 · node_power-fungi

**산출물** `results/node_power/fungi/summary.json`

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
 "fungi (표본이 도달한 마디)": {
  "recon_auroc": 0.8499,
  "freq_auroc": 0.7453,
  "recon_logloss": 0.4524,
  "freq_logloss": 0.7242,
  "prior_logloss": 0.6668,
  "recon_size_bias": -0.0567,
  "freq_size_bias": -0.5506,
  "n_tips": 289,
  "auroc_margin": 0.1046,
  "logloss_margin": 0.2718,
  "auroc_headroom": 0.2547,
  "verdict": "계통수가 도움이 됨"
 },
 "fungi 뿌리 아래 큰 쪽 (286종)": {
  "recon_auroc": 0.8904,
  "freq_auroc": 0.8098,
  "recon_logloss": 0.3382,
  "freq_logloss": 0.5427,
  "prior_logloss": 0.6162,
  "recon_size_bias": -0.1231,
  "freq_size_bias": -0.4342,
  "n_tips": 286,
  "auroc_margin": 0.0806,
  "logloss_margin": 0.2045,
  "auroc_headroom": 0.1902,
  "verdict": "계통수가 도움이 됨"
 },
 "Ascomycota": {
  "recon_auroc": 0.8317,
  "freq_auroc": 0.7678,
  "recon_logloss": 0.3282,
  "freq_logloss": 0.4425,
  "prior_logloss": 0.5311,
  "recon_size_bias": -0.1054,
  "freq_size_bias": -0.2496,
  "n_tips": 153,
  "auroc_margin": 0.0639,
  "logloss_margin": 0.1143,
  "auroc_headroom": 0.2322,
  "verdict": "계통수가 도움이 됨"
 },
 "Basidiomycota": {
  "recon_auroc": 0.8475,
  "freq_auroc": 0.8143,
  "recon_logloss": 0.3105,
  "freq_logloss": 0.3956,
  "prior_logloss": 0.5362,
  "recon_size_bias": -0.0824,
  "freq_size_bias": -0.2404,
  "n_tips": 77,
  "auroc_margin": 0.0332,
  "logloss_margin": 0.0851,
  "auroc_headroom": 0.1857,
  "verdict": "계통수가 도움이 됨"
 },
 "Chytridiomycota": {
  "recon_auroc": 0.8862,
  "freq_auroc": 0.7933,
  "recon_logloss": 0.31,
  "freq_logloss": 0.5653,
  "prior_logloss": 0.5692,
  "recon_size_bias": -0.0854,
  "freq_size_bias": -0.2818,
  "n_tips": 15,
  "auroc_margin"
… (잘림 — 원본 파일 참조)
```

## runs

```json
[
 {
  "rep": 0,
  "node": "fungi (표본이 도달한 마디)",
  "n_tips": 289,
  "recon_auroc": 0.8437533707259195,
  "freq_auroc": 0.731727294790206,
  "recon_logloss": 0.45424440505623354,
  "freq_logloss": 0.7022503575654846,
  "prior_logloss": 0.6562408706276683,
  "recon_size_bias": -0.0422823135166952,
  "freq_size_bias": -0.5315684694506327,
  "true_share": 0.365
 },
 {
  "rep": 0,
  "node": "fungi 뿌리 아래 큰 쪽 (286종)",
  "n_tips": 286,
  "recon_auroc": 0.8856796189445847,
  "freq_auroc": 0.7787481968986657,
  "recon_logloss": 0.3462408509807119,
  "freq_logloss": 0.553101724773414,
  "prior_logloss": 0.6065680978792408,
  "recon_size_bias": -0.1411069449731859,
  "freq_size_bias": -0.4205582553040181,
  "true_share": 0.295
 },
 {
  "rep": 0,
  "node": "Ascomycota",
  "n_tips": 153,
  "recon_auroc": 0.810099663556148,
  "freq_auroc": 0.7418224193124212,
  "recon_logloss": 0.34378013270548763,
  "freq_logloss": 0.46216851633563893,
  "prior_logloss": 0.5284854978302385,
  "recon_size_bias": -0.14129035216940325,
  "freq_size_bias": -0.2611424984306341,
  "true_share": 0.22125
 },
 {
  "rep": 0,
  "node": "Basidiomycota",
  "n_tips": 77,
  "recon_auroc": 0.8280744336569579,
  "freq_auroc": 0.810892990504641,
  "recon_logloss": 0.32592755979901994,
  "freq_logloss": 0.40001765173924064,
  "prior_logloss": 0.5362378729718903,
  "recon_size_bias": -0.09540608165028332,
  "freq_size_bias": -0.2452547452547452,
  "true_share": 0.2275
 },
 {
  "rep": 0,
  "node": "Chytridiomycota",
  "n_tips": 15,
  "recon_auroc": 0.8916700932017544,
  "freq_auroc": 0.7836528577302632,
  "recon_logloss": 0.
… (잘림 — 원본 파일 참조)
```

## 연결
- [[실험 목록]]
