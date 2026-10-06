---
유형: 환경
법칙: animal_temperature_v1
클러스터: 동물
tags:
  - 법칙/animal_temperature_v1
  - 클러스터/동물
  - 판정/전이 검정
  - 유형/환경
---

# animal_temperature_v1 · 환경

← [[animal_temperature_v1]]

**카탈로그** animals · **종 수** 14

## 환경 범위

```json
{
 "세포 온도 °C": {
  "min": 14.0,
  "median": 25.5,
  "max": 41.5,
  "n": 14
 },
 "세포 내 삼투압 mOsm": {
  "min": 300,
  "median": 300.0,
  "max": 1000,
  "n": 14
 },
 "저산소(1)": {
  "0": 13,
  "1": 1
 },
 "항온(1)": {
  "0": 11,
  "1": 3
 },
 "기생(1)": {
  "0": 13,
  "1": 1
 },
 "요소 삼투(1)": {
  "0": 14
 },
 "세포 온도 °C (법칙에 기록된 값)": {
  "min": 12.0,
  "median": 25.0,
  "max": 41.5,
  "n": 19
 }
}
```

## 분류군 구성

```json
{
 "insect": 3,
 "mammal": 2,
 "sponge": 1,
 "cephalochordate": 1,
 "nematode": 1,
 "teleost": 1,
 "crustacean": 1,
 "bird": 1,
 "flatworm": 1,
 "echinoderm": 1,
 "amphibian": 1
}
```

## GC 함량

```json
{
 "min": 0.325,
 "median": 0.4,
 "max": 0.445,
 "n": 14
}
```

## 요약 수치

```json
{
 "law_per_degree_c": {
  "ols": 0.0009836,
  "tree_pgls": 0.0006997,
  "rank_gls": 0.0007847
 },
 "판정": "미생물 온도 법칙은 동물 세포에 전이되지 않음"
}
```

> [!note]
> envelope 밖의 환경에 이 법칙을 쓰면 외삽이다. 값은 문헌 근사치(카탈로그 주석 참조).
