---
유형: 환경
법칙: animal_axes_v1
클러스터: 동물
tags:
  - 법칙/animal_axes_v1
  - 클러스터/동물
  - 판정/음성
  - 유형/환경
---

# animal_axes_v1 · 환경

← [[animal_axes_v1]]

**카탈로그** animals · **종 수** 69

## 환경 범위

```json
{
 "세포 온도 °C": {
  "min": -1.0,
  "median": 25.0,
  "max": 41.5,
  "n": 69
 },
 "세포 내 삼투압 mOsm": {
  "min": 300,
  "median": 300,
  "max": 1000,
  "n": 69
 },
 "저산소(1)": {
  "0": 61,
  "1": 8
 },
 "항온(1)": {
  "0": 57,
  "1": 12
 },
 "기생(1)": {
  "0": 65,
  "1": 4
 },
 "요소 삼투(1)": {
  "0": 64,
  "1": 5
 }
}
```

## 분류군 구성

```json
{
 "teleost": 11,
 "mammal": 8,
 "insect": 6,
 "mollusc": 6,
 "chondrichthyan": 5,
 "reptile": 5,
 "bird": 4,
 "amphibian": 4,
 "echinoderm": 3,
 "cnidarian": 3,
 "nematode": 3,
 "annelid": 2,
 "crustacean": 2,
 "flatworm": 2,
 "arachnid": 2,
 "sponge": 1,
 "cephalochordate": 1,
 "tunicate": 1
}
```

## GC 함량

```json
{
 "min": 0.27,
 "median": 0.405,
 "max": 0.475,
 "n": 69
}
```

## 요약 수치

```json
{
 "ivywrel": {
  "p<0.05 (종 수준)": [
   "tcell",
   "osmol_high",
   "urea"
  ],
  "분류군 수준 통과": [],
  "GC 보정 통과": [
   "osmol_high",
   "urea"
  ],
  "분류군 빼고 평균 기준선을 이김": false
 },
 "cvp": {
  "p<0.05 (종 수준)": [
   "endo",
   "parasite"
  ],
  "분류군 수준 통과": [],
  "GC 보정 통과": [],
  "분류군 빼고 평균 기준선을 이김": false
 },
 "acidic_excess": {
  "p<0.05 (종 수준)": [
   "osmol_high"
  ],
  "분류군 수준 통과": [],
  "GC 보정 통과": [
   "osmol_high",
   "urea"
  ],
  "분류군 빼고 평균 기준선을 이김": false
 },
 "median_pi": {
  "p<0.05 (종 수준)": [],
  "분류군 수준 통과": [],
  "GC 보정 통과": [
   "osmol_high",
   "urea"
  ],
  "분류군 빼고 평균 기준선을 이김": false
 },
 "n_side": {
  "p<0.05 (종 수준)": [
   "osmol_high",
   "parasite",
   "urea"
  ],
  "분류군 수준 통과": [
   "osmol_high"
  ],
  "GC 보정 통과": [
   "osmol_high",
   "parasite"
  ],
  "분류군 빼고 평균 기준선을 이김": false
 },
 "gravy": {
  "p<0.05 (종 수준)": [
   "parasite"
  ],
  "분류군 수준 통과": [],
  "GC 보정 통과": [
   "parasite"
  ],
  "분류군 빼고 평균 기준선을 이김": false
 },
 "fymink": {
  "p<0.05 (종 수준)": [
   "endo"
  ],
  "분류군 수준 통과": [],
  "GC 보정 통과": [],
  "분류군 빼고 평균 기준선을 이김": false
 },
 "aromatic": {
  "p<0.05 (종 수준)": [
   "endo"
  ],
  "분류군 수준 통과": [],
  "GC 보정 통과": [],
  "분류군 빼고 평균 기준선을 이김": false
 },
 "cysteine": {
  "p<0.05 (종 수준)": [],
  "분류군 수준 통과": [],
  "GC 보정 통과": [],
  "분류군 빼고 평균 기준선을 이김": false
 }
}
```

> [!note]
> envelope 밖의 환경에 이 법칙을 쓰면 외삽이다. 값은 문헌 근사치(카탈로그 주석 참조).
