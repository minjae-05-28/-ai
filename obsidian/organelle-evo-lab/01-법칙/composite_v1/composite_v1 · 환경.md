---
유형: 환경
법칙: composite_v1
클러스터: 기생·극한
tags:
  - 법칙/composite_v1
  - 클러스터/기생·극한
  - 판정/무승부
  - 유형/환경
---

# composite_v1 · 환경

← [[composite_v1]]

**카탈로그** eukaryotes · **종 수** 23

## 환경 범위

```json
{
 "생활 방식": {
  "free_living": 15,
  "parasite": 8
 },
 "위치": {
  "free": 15,
  "intracellular": 5,
  "extracellular": 3
 },
 "에너지(미토콘드리아)": {
  "aerobic": 20,
  "reduced": 3
 },
 "세포 온도 °C (동물 카탈로그에 있는 종만)": {
  "min": 25.0,
  "median": 26.0,
  "max": 27.0,
  "n": 2
 }
}
```

## 분류군 구성

```json
{
 "discoba": 5,
 "alveolata": 5,
 "holozoa": 4,
 "fungi": 4,
 "amoebozoa": 3,
 "chlorophyta": 2
}
```

## GC 함량

```json
{
 "min": 0.16,
 "median": 0.42,
 "max": 0.64,
 "n": 23
}
```

## 축별 대비

```json
{
 "parasite": {
  "pairs_with_axis": 8
 },
 "intracellular": {
  "pairs_with_axis": 5
 },
 "reduced_mitochondria": {
  "pairs_with_axis": 3
 },
 "control_pairs": 6,
 "independent_parasite_clades": 4
}
```

## 요약 수치

```json
{
 "mean_auroc_recover_lost": {
  "prior only (no law)": 0.7739546991419038,
  "axis law": 0.776225239283262,
  "axis + mitochondrion law": 0.7628692597773826,
  "axis + plastid law": 0.7753902446765196,
  "axis + insect-endosymbiont law": 0.7737329154326886,
  "plastid law only": 0.7725787170512277,
  "axis law, wrong lifestyle (free-living)": 0.773170953858617
 }
}
```

> [!note]
> envelope 밖의 환경에 이 법칙을 쓰면 외삽이다. 값은 문헌 근사치(카탈로그 주석 참조).
