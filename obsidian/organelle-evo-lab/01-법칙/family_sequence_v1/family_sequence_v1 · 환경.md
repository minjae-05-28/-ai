---
유형: 환경
법칙: family_sequence_v1
클러스터: 서열·조성
tags:
  - 법칙/family_sequence_v1
  - 클러스터/서열·조성
  - 판정/구조 분석
  - 유형/환경
---

# family_sequence_v1 · 환경

← [[family_sequence_v1]]

**카탈로그** prokaryotes · **종 수** 81

## 환경 범위

```json
{
 "최적 온도 °C": {
  "min": 5,
  "median": 30,
  "max": 100,
  "n": 81
 },
 "최적 NaCl %": {
  "min": 0,
  "median": 1,
  "max": 25,
  "n": 81
 },
 "산소 호흡(1)": {
  "1": 59,
  "0": 22
 },
 "방사선 내성(1)": {
  "0": 69,
  "1": 12
 },
 "빈영양(1)": {
  "0": 74,
  "1": 7
 }
}
```

## 분류군 구성

```json
{
 "archaea": 16,
 "gamma": 14,
 "firmicutes": 11,
 "cyano": 7,
 "bacteroidetes": 6,
 "alpha": 6,
 "deinococcus": 6,
 "delta": 6,
 "beta": 4,
 "actino": 3,
 "thermotogae": 2
}
```

## GC 함량

```json
{
 "min": 0.295,
 "median": 0.475,
 "max": 0.74,
 "n": 81
}
```

## 축별 대비

```json
{
 "colder": {
  "pairs_changed": 31,
  "change_range": [
   -1.6,
   1.33
  ]
 },
 "saltier": {
  "pairs_changed": 20,
  "change_range": [
   -0.05,
   2.3
  ]
 },
 "anaerobic": {
  "pairs_changed": 10,
  "change_range": [
   -1.0,
   1.0
  ]
 },
 "radiation_resistant": {
  "pairs_changed": 12,
  "change_range": [
   0.0,
   1.0
  ]
 },
 "oligotrophic": {
  "pairs_changed": 7,
  "change_range": [
   0.0,
   1.0
  ]
 },
 "scale": "colder: (relative - descendant temperature)/30.0 C; saltier: change in NaCl/10.0%; others -1/0/1",
 "control_pairs": 3
}
```

## 요약 수치

```json
{
 "ivywrel": {
  "axis": "colder",
  "share_positive": 0.9056693663649357,
  "median_sensitivity": 0.0239712862814852,
  "families_tested": 2099
 },
 "acidic_excess": {
  "axis": "saltier",
  "share_positive": 0.8918532634587899,
  "median_sensitivity": 0.018933482848515305,
  "families_tested": 2099
 }
}
```

> [!note]
> envelope 밖의 환경에 이 법칙을 쓰면 외삽이다. 값은 문헌 근사치(카탈로그 주석 참조).
