---
유형: 실험
실행: hgt_rate
산출: results/hgt_rate/summary.json
tags:
  - 유형/실험
  - 실험/hgt_rate
---

# 실험 · hgt_rate

**산출물** `results/hgt_rate/summary.json`

## 한눈에

| 항목 | 값 |
| --- | --- |
| estimator | 유전자군별 적합된 획득/손실 비 (상한 없는 격자) |

## gates

```json
[
 [
  0.35,
  "크기(유전자군 수) 부풀기 시작"
 ],
 [
  0.5,
  "확률 보정이 깨짐"
 ],
 [
  0.8,
  "순위도 무너짐"
 ]
]
```

## limits

```json
[
 "이 추정량은 전달과 '원래 획득이 잦은 것'(유전자 중복·신규 생성·수렴 획득)을 구분하지 못합니다. 둘 다 모형에게는 획득률을 올리라는 신호이므로, 나온 값은 전달의 상한으로 읽어야 합니다.",
 "보정 곡선이 전달 0.1 위에서 포화합니다(통계량이 0.99에 붙음). 따라서 이 측정은 '0.35 아래인가'에만 답하고, 그보다 높은 값들끼리는 구분하지 못합니다.",
 "모의 자료는 reduced_x5 생성기(획득 <= 0.1 x 손실)로 만들었습니다. 실제 분류군의 바탕 획득률이 이보다 높으면 전달이 과대평가됩니다.",
 "불완전한 프로테옴은 실제로 있는 유전자군을 없는 것으로 만들어 손실 쪽 신호를 키우므로, 이 추정을 낮추는 쪽으로 작용합니다. 품질 보정(genome_quality.py)은 여기 적용하지 않았습니다.",
 "두 분류군의 유전자군 표본이 다릅니다. 알파프로테오박테리아는 모형 탐색 캐시의 1,500개로, 빈도 십분위마다 같은 수를 뽑은 층화 표본입니다(드문 유전자군이 자연 분포보다 많이 들어 있음). 아메보조아는 5,771개 전부입니다. 드문 유전자군일수록 가짜 획득 신호가 많으므로 층화 표본은 전달을 높게 보이게 하는 쪽입니다 — 세균 값 0.005는 그런 의미에서 보수적인 상한입니다. 두 수치를 서로 직접 비교하지 마세요.",
 "획득/손실 비는 격자값(0.01, 0.03, 0.1, 0.2, 0.3, 0.5, 1, 3, 10)에서만 나오므로 중앙값으로 읽은 값은 거칠고, 비율 통계량(q>=0.3)이 주 판독값입니다."
]
```

## sets

```json
{
 "alphaproteobacteria": {
  "label": "알파프로테오박테리아 (GTDB 종 대표 2,526종, 유전자군 1,500개 표본)",
  "families": 1500,
  "observed": {
   "median_q": 0.1,
   "mean_log10_q": -0.908597310421692,
   "share_q_ge_1": 0.222,
   "share_q_ge_0.3": 0.3566666666666667
  },
  "calibration": [
   {
    "hgt": 0.0,
    "median_q": 0.1,
    "mean_log10_q": -0.9678,
    "share_q_ge_1": 0.2,
    "share_q_ge_0.3": 0.272
   },
   {
    "hgt": 0.02,
    "median_q": 0.3,
    "mean_log10_q": -0.3339,
    "share_q_ge_1": 0.294,
    "share_q_ge_0.3": 0.58
   },
   {
    "hgt": 0.05,
    "median_q": 0.5,
    "mean_log10_q": -0.0732,
    "share_q_ge_1": 0.411,
    "share_q_ge_0.3": 0.855
   },
   {
    "hgt": 0.1,
    "median_q": 1.0,
    "mean_log10_q": 0.1909,
    "share_q_ge_1": 0.741,
    "share_q_ge_0.3": 0.999
   },
   {
    "hgt": 0.2,
    "median_q": 3.0,
    "mean_log10_q": 0.512,
    "share_q_ge_1": 0.995,
    "share_q_ge_0.3": 1.0
   },
   {
    "hgt": 0.35,
    "median_q": 3.0,
    "mean_log10_q": 0.6509,
    "share_q_ge_1": 1.0,
    "share_q_ge_0.3": 1.0
   },
   {
    "hgt": 0.5,
    "median_q": 10.0,
    "mean_log10_q": 0.8541,
    "share_q_ge_1": 1.0,
    "share_q_ge_0.3": 1.0
   },
   {
    "hgt": 0.8,
    "median_q": 10.0,
    "mean_log10_q": 0.8965,
    "share_q_ge_1": 1.0,
    "share_q_ge_0.3": 1.0
   }
  ],
  "estimated_hgt": 0.005,
  "estimated_hgt_by_median_q": 0.0,
  "how": "보간",
  "gates_passed": [
   "0.35 (크기(유전자군 수) 부풀기 시작)",
   "0.5 (확률 보정이 깨짐)",
   "0.8 (순위도 무너짐)"
  ],
  "gates_broken": []
 },
 "amoebozoa": {
  "label": "아메보조아 + 외군 (40종)",
  "families": 5771,
  "observed": {
   "median_q": 1.0,
   "mean_log10_q": 0.15123577286917572,
   "share_q_ge_1": 0.6258880609946283,
   "share_q_ge_0.3": 0.909894299081615
  },
  "calibration": [
   {
    "hgt": 0.0,
    "median_q": 0.1,
    "mean_log10_q": -0.9769,
    "share_q_ge_1": 0.209,
    "share_q_ge_0.3": 0.33
   },
   {
    "hgt": 0.02,
    "median_q": 0.5,
    "mean_log10_q": -0.3326,
    "share_q_ge_1": 0.352,
    "share_q_ge_0.3": 0.653
   },
   {
    "hgt": 0.05,
    "median_q": 1.0,
    "mean_log10_q": 0.057,
    "share_q_ge_1": 0.607,
    "share_q_ge_0.3": 0.923
   },
   {
    "hgt": 0.1,
    "median_q": 3.0,
    "mean_log10_q": 0.376,
    "share_q_ge_1": 0.902,
    "share_q_ge_0.3": 0.994
   },
   {
    "hgt": 0.2,
    "median_q": 3.0,
    "mean_log10_q": 0.6501,
    "share_q_ge_1": 0.997,
    "share_q_ge_0.3": 1.0
   },
   {
    "hgt": 0.35,
    "median_q": 10.0,
    "mean_log10_q": 0.7975,
    "share_q_ge_1": 1.0,
    "share_q_ge_0.3": 1.0
   },
   {
    "hgt": 0.5,
    "median_q": 10.0,
    "mean_log10_q": 0.8662,
    "share_q_ge_1": 1.0,
    "share_q_ge_0.3": 1.0
   },
   {
    "hgt": 0.8,
    "median_q": 10.0,
    "mean_log10_q": 0.9273,
    "share_q_ge_1": 1.0,
    "share_q_ge_0.3": 1.0
   }
  ],
  "estimated_hgt": 0.049,
  "estimated_hgt_by_median_q": 0.05,
  "how": "보간",
  "gates_passed": [
   "0.35 (크기(유전자군 수) 부풀기 시작)",
   "0.5 (확률 보정이 깨짐)",
   "0.8 (순위도 무너짐)"
  ],
  "gates_broken": []
 }
}
```

## 연결
- [[실험 목록]]
