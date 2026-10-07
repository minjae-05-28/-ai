---
유형: 실험
실행: node_power/leca2_discoba
산출: results/node_power/leca2_discoba/summary.json
tags:
  - 유형/실험
  - 실험/node_power-leca2_discoba
---

# 실험 · node_power-leca2_discoba

**산출물** `results/node_power/leca2_discoba/summary.json`

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
 "leca2_discoba (표본이 도달한 마디)": {
  "recon_auroc": 0.8057,
  "freq_auroc": 0.7056,
  "recon_logloss": 0.5057,
  "freq_logloss": 0.9568,
  "prior_logloss": 0.6929,
  "recon_size_bias": 0.0805,
  "freq_size_bias": -0.6238,
  "n_tips": 250,
  "auroc_margin": 0.1001,
  "logloss_margin": 0.4511,
  "auroc_headroom": 0.2944,
  "verdict": "계통수가 도움이 됨"
 },
 "leca2_discoba 뿌리 아래 큰 쪽 (226종)": {
  "recon_auroc": 0.8619,
  "freq_auroc": 0.8105,
  "recon_logloss": 0.4098,
  "freq_logloss": 0.6509,
  "prior_logloss": 0.6747,
  "recon_size_bias": 0.0576,
  "freq_size_bias": -0.5268,
  "n_tips": 226,
  "auroc_margin": 0.0514,
  "logloss_margin": 0.2411,
  "auroc_headroom": 0.1895,
  "verdict": "계통수가 도움이 됨"
 },
 "Alveolata": {
  "recon_auroc": 0.9333,
  "freq_auroc": 0.8935,
  "recon_logloss": 0.2503,
  "freq_logloss": 0.4362,
  "prior_logloss": 0.5987,
  "recon_size_bias": 0.066,
  "freq_size_bias": -0.3947,
  "n_tips": 30,
  "auroc_margin": 0.0398,
  "logloss_margin": 0.1859,
  "auroc_headroom": 0.1065,
  "verdict": "계통수가 도움이 됨"
 },
 "Amoebozoa": {
  "recon_auroc": 0.9239,
  "freq_auroc": 0.8527,
  "recon_logloss": 0.2671,
  "freq_logloss": 0.6132,
  "prior_logloss": 0.6056,
  "recon_size_bias": 0.0835,
  "freq_size_bias": -0.376,
  "n_tips": 12,
  "auroc_margin": 0.0712,
  "logloss_margin": 0.3461,
  "auroc_headroom": 0.1473,
  "verdict": "계통수가 도움이 됨"
 },
 "Discoba": {
  "recon_auroc": 0.8212,
  "freq_auroc": 0.7379,
  "recon_logloss": 0.4738,
  "freq_logloss": 1.38,
  "prior_logloss": 0.6726,
  "recon_size_bias": 0.0964,
  "freq_size_bias": -0.5471,
  "n_tips": 24,
  "auroc_margin": 0.0
… (잘림 — 원본 파일 참조)
```

## runs

```json
[
 {
  "rep": 0,
  "node": "leca2_discoba (표본이 도달한 마디)",
  "n_tips": 250,
  "recon_auroc": 0.8041590607886775,
  "freq_auroc": 0.7082406041359306,
  "recon_logloss": 0.5019307444295464,
  "freq_logloss": 0.9438624258180487,
  "prior_logloss": 0.6930346763408154,
  "recon_size_bias": 0.09420404579433693,
  "freq_size_bias": -0.6336142131979695,
  "true_share": 0.4925
 },
 {
  "rep": 0,
  "node": "leca2_discoba 뿌리 아래 큰 쪽 (226종)",
  "n_tips": 226,
  "recon_auroc": 0.8602821682262588,
  "freq_auroc": 0.8107061413855469,
  "recon_logloss": 0.41619282704451505,
  "freq_logloss": 0.6519923149756595,
  "prior_logloss": 0.6698532416793879,
  "recon_size_bias": 0.07127263743406648,
  "freq_size_bias": -0.5398652838058734,
  "true_share": 0.3925
 },
 {
  "rep": 0,
  "node": "Alveolata",
  "n_tips": 30,
  "recon_auroc": 0.9109178743961353,
  "freq_auroc": 0.8816734299516908,
  "recon_logloss": 0.28728074327573266,
  "freq_logloss": 0.45359788664499434,
  "prior_logloss": 0.5941300227248386,
  "recon_size_bias": 0.05126736111111111,
  "freq_size_bias": -0.4174814814814815,
  "true_share": 0.28125
 },
 {
  "rep": 0,
  "node": "Amoebozoa",
  "n_tips": 12,
  "recon_auroc": 0.9052312070910068,
  "freq_auroc": 0.8337572193080062,
  "recon_logloss": 0.28754554320917125,
  "freq_logloss": 0.6809577131339134,
  "prior_logloss": 0.6032671215498728,
  "recon_size_bias": 0.04968864211708691,
  "freq_size_bias": -0.40772532188841204,
  "true_share": 0.29125
 },
 {
  "rep": 0,
  "node": "Discoba",
  "n_tips": 24,
  "recon_auroc": 0.8234155068019187,
  "freq_auroc": 0.7281919215747948,
  "recon_loglo
… (잘림 — 원본 파일 참조)
```

## 연결
- [[실험 목록]]
