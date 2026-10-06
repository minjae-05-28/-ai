---
유형: 실험
실행: node_power/leca
산출: results/node_power/leca/summary.json
tags:
  - 유형/실험
  - 실험/node_power-leca
---

# 실험 · node_power-leca

**산출물** `results/node_power/leca/summary.json`

## 한눈에

| 항목 | 값 |
| --- | --- |
| note | 세 뿌리 위치 각각의 알려진 정답 채점과 그중 가장 나쁜 값 |

## aggregate

```json
{
 "leca (표본이 도달한 마디, 세 뿌리 중 가장 나쁜 값: discoba)": {
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
 "뿌리 discoba": {
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
 "뿌리 opisthokonta": {
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
 }
}
```

## 연결
- [[실험 목록]]
