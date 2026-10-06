---
유형: 실험
실행: node_power
산출: results/node_power/summary.json
tags:
  - 유형/실험
  - 실험/node_power
---

# 실험 · node_power

**산출물** `results/node_power/summary.json`

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
 "Alphaproteobacteria": {
  "recon_auroc": 0.9914,
  "freq_auroc": 0.9448,
  "recon_logloss": 0.1333,
  "freq_logloss": 0.3459,
  "prior_logloss": 0.6922,
  "recon_size_bias": -0.0892,
  "freq_size_bias": -0.2144,
  "n_tips": 2323,
  "auroc_margin": 0.0466,
  "logloss_margin": 0.2126,
  "auroc_headroom": 0.0552,
  "verdict": "계통수가 도움이 됨"
 },
 "Rickettsiales": {
  "recon_auroc": 0.9749,
  "freq_auroc": 0.9075,
  "recon_logloss": 0.3384,
  "freq_logloss": 0.5169,
  "prior_logloss": 0.6598,
  "recon_size_bias": -0.368,
  "freq_size_bias": -0.4224,
  "n_tips": 53,
  "auroc_margin": 0.0674,
  "logloss_margin": 0.1785,
  "auroc_headroom": 0.0925,
  "verdict": "계통수가 도움이 됨"
 },
 "Rhodospirillales": {
  "recon_auroc": 1.0,
  "freq_auroc": 0.9989,
  "recon_logloss": 0.005,
  "freq_logloss": 0.0895,
  "prior_logloss": 0.6863,
  "recon_size_bias": -0.0025,
  "freq_size_bias": -0.0741,
  "n_tips": 46,
  "auroc_margin": 0.0011,
  "logloss_margin": 0.0845,
  "auroc_headroom": 0.0011,
  "verdict": "계통수가 도움이 됨"
 },
 "Caulobacterales": {
  "recon_auroc": 0.9994,
  "freq_auroc": 0.992,
  "recon_logloss": 0.0253,
  "freq_logloss": 0.1477,
  "prior_logloss": 0.6801,
  "recon_size_bias": -0.005,
  "freq_size_bias": -0.0923,
  "n_tips": 124,
  "auroc_margin": 0.0074,
  "logloss_margin": 0.1224,
  "auroc_headroom": 0.008,
  "verdict": "계통수가 도움이 됨"
 },
 "Rhizobiales": {
  "recon_auroc": 0.9999,
  "freq_auroc": 0.9869,
  "recon_logloss": 0.0134,
  "freq_logloss": 0.1549,
  "prior_logloss": 0.6818,
  "recon_size_bias": -0.0085,
  "freq_size_bias": -0.0879,
  "n_tips": 767,
  "auroc_margin": 0.013,

… (잘림 — 원본 파일 참조)
```

## runs

```json
[
 {
  "rep": 0,
  "node": "Alphaproteobacteria",
  "n_tips": 2323,
  "recon_auroc": 0.9939093235648334,
  "freq_auroc": 0.9448702830188679,
  "recon_logloss": 0.11411988731872952,
  "freq_logloss": 0.33737846006970956,
  "prior_logloss": 0.6913460990017393,
  "recon_size_bias": -0.08301203301612367,
  "freq_size_bias": -0.2056458999276431,
  "true_share": 0.47
 },
 {
  "rep": 0,
  "node": "Rickettsiales",
  "n_tips": 53,
  "recon_auroc": 0.9715256709250889,
  "freq_auroc": 0.9183194711025805,
  "recon_logloss": 0.3209563717690253,
  "freq_logloss": 0.46333633104260824,
  "prior_logloss": 0.6466694040658457,
  "recon_size_bias": -0.34784788726478494,
  "freq_size_bias": -0.4111043484141475,
  "true_share": 0.34875
 },
 {
  "rep": 0,
  "node": "Rhodospirillales",
  "n_tips": 46,
  "recon_auroc": 0.9999429281655844,
  "freq_auroc": 0.9990424614448052,
  "recon_logloss": 0.007170066936087096,
  "freq_logloss": 0.09389908332936288,
  "prior_logloss": 0.6859298002523728,
  "recon_size_bias": 0.00035806135697798294,
  "freq_size_bias": -0.07868083003952574,
  "true_share": 0.44
 },
 {
  "rep": 0,
  "node": "Caulobacterales",
  "n_tips": 124,
  "recon_auroc": 0.9985387519146837,
  "freq_auroc": 0.9905948176964834,
  "recon_logloss": 0.031446376816029444,
  "freq_logloss": 0.1615824944021168,
  "prior_logloss": 0.6806922607045869,
  "recon_size_bias": -0.009026320822514837,
  "freq_size_bias": -0.10309179668804444,
  "true_share": 0.42125
 },
 {
  "rep": 0,
  "node": "Rhizobiales",
  "n_tips": 767,
  "recon_auroc": 0.9998205484807506,
  "freq_auroc": 0.9886528958988919,
  "recon_lo
… (잘림 — 원본 파일 참조)
```

## 연결
- [[실험 목록]]
