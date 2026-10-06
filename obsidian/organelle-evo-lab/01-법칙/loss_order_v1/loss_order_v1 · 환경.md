---
유형: 환경
법칙: loss_order_v1
클러스터: 소기관
tags:
  - 법칙/loss_order_v1
  - 클러스터/소기관
  - 판정/구조 분석
  - 유형/환경
---

# loss_order_v1 · 환경

← [[loss_order_v1]]

**카탈로그** eukaryotes · **종 수** 94

## 환경 범위

```json
{
 "생활 방식": {
  "parasite": 79,
  "free_living": 15
 },
 "위치": {
  "intracellular": 43,
  "extracellular": 36,
  "free": 15
 },
 "에너지(미토콘드리아)": {
  "aerobic": 73,
  "reduced": 21
 },
 "세포 온도 °C (동물 카탈로그에 있는 종만)": {
  "min": 20.0,
  "median": 25.0,
  "max": 37.0,
  "n": 7
 }
}
```

## 분류군 구성

```json
{
 "fungi": 24,
 "alveolata": 23,
 "discoba": 15,
 "stramenopiles": 6,
 "platyhelminthes": 6,
 "nematoda": 5,
 "amoebozoa": 4,
 "metamonada": 4,
 "cnidaria": 3,
 "chlorophyta": 2,
 "holozoa": 2
}
```

## GC 함량

```json
{
 "min": 0.16,
 "median": 0.43,
 "max": 0.635,
 "n": 93
}
```

## 축별 대비

```json
{
 "parasite": {
  "pairs_with_axis": 79
 },
 "intracellular": {
  "pairs_with_axis": 43
 },
 "reduced_mitochondria": {
  "pairs_with_axis": 21
 },
 "control_pairs": 0,
 "independent_parasite_clades": 11
}
```

## 요약 수치

```json
{
 "containment_over_random_median": 1.618,
 "share_above_random": 1.0
}
```

> [!note]
> envelope 밖의 환경에 이 법칙을 쓰면 외삽이다. 값은 문헌 근사치(카탈로그 주석 참조).
