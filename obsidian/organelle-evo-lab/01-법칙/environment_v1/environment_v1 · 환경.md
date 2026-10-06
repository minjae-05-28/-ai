---
유형: 환경
법칙: environment_v1
클러스터: 기생·극한
tags:
  - 법칙/environment_v1
  - 클러스터/기생·극한
  - 판정/무승부
  - 유형/환경
---

# environment_v1 · 환경

← [[environment_v1]]

**카탈로그** prokaryotes · **종 수** 36

## 환경 범위

```json
{
 "최적 온도 °C": {
  "min": 8,
  "median": 30.0,
  "max": 85,
  "n": 36
 },
 "최적 NaCl %": {
  "min": 0,
  "median": 0.75,
  "max": 25,
  "n": 36
 },
 "산소 호흡(1)": {
  "1": 28,
  "0": 8
 },
 "방사선 내성(1)": {
  "0": 32,
  "1": 4
 },
 "빈영양(1)": {
  "0": 34,
  "1": 2
 }
}
```

## 분류군 구성

```json
{
 "gamma": 7,
 "archaea": 6,
 "firmicutes": 5,
 "cyano": 4,
 "delta": 4,
 "bacteroidetes": 4,
 "alpha": 2,
 "deinococcus": 2,
 "actino": 2
}
```

## GC 함량

```json
{
 "min": 0.295,
 "median": 0.463,
 "max": 0.74,
 "n": 36
}
```

## 축별 대비

```json
{
 "colder": {
  "pairs_changed": 12,
  "change_range": [
   -1.6,
   1.33
  ]
 },
 "saltier": {
  "pairs_changed": 8,
  "change_range": [
   -0.05,
   2.3
  ]
 },
 "anaerobic": {
  "pairs_changed": 4,
  "change_range": [
   -1.0,
   1.0
  ],
  "warning": "표본 적음 (5쌍 미만)"
 },
 "radiation_resistant": {
  "pairs_changed": 4,
  "change_range": [
   0.0,
   1.0
  ],
  "warning": "표본 적음 (5쌍 미만)"
 },
 "oligotrophic": {
  "pairs_changed": 2,
  "change_range": [
   0.0,
   1.0
  ],
  "warning": "표본 적음 (5쌍 미만)"
 },
 "scale": "colder: (relative - descendant temperature)/30.0 C; saltier: change in NaCl/10.0%; others -1/0/1",
 "control_pairs": 2
}
```

## 요약 수치

```json
{
 "loss_colder": "신뢰구간이 0을 벗어나는 효과 없음 (또는 구간 미계산)",
 "loss_saltier": "신뢰구간이 0을 벗어나는 효과 없음 (또는 구간 미계산)",
 "loss_anaerobic": "신뢰구간이 0을 벗어나는 효과 없음 (또는 구간 미계산)",
 "loss_radiation_resistant": "신뢰구간이 0을 벗어나는 효과 없음 (또는 구간 미계산)",
 "loss_oligotrophic": "신뢰구간이 0을 벗어나는 효과 없음 (또는 구간 미계산)",
 "duplication_colder": "신뢰구간이 0을 벗어나는 효과 없음 (또는 구간 미계산)",
 "duplication_saltier": "신뢰구간이 0을 벗어나는 효과 없음 (또는 구간 미계산)",
 "duplication_anaerobic": "신뢰구간이 0을 벗어나는 효과 없음 (또는 구간 미계산)",
 "duplication_radiation_resistant": "신뢰구간이 0을 벗어나는 효과 없음 (또는 구간 미계산)",
 "duplication_oligotrophic": "신뢰구간이 0을 벗어나는 효과 없음 (또는 구간 미계산)",
 "summary": {
  "leave_one_pair_out_auroc": {
   "copies_only": 0.6143217102181643,
   "no_environment": 0.8156591797831733,
   "environment_law": 0.8079995318827699,
   "memorisation": 0.8041923336615406
  },
  "환경 축 효과": -0.007659647900403474,
  "주의": "축별 계수가 0과 구분돼도 환경 축은 처음 보는 쌍의 소실 예측을 개선하지 못함. 계수는 '이 데이터에서 이 환경일 때 이런 경향'이지 예측 규칙이 아님"
 }
}
```

> [!note]
> envelope 밖의 환경에 이 법칙을 쓰면 외삽이다. 값은 문헌 근사치(카탈로그 주석 참조).
