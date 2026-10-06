---
유형: 환경
법칙: severity_v1
클러스터: 소기관
tags:
  - 법칙/severity_v1
  - 클러스터/소기관
  - 판정/양성
  - 유형/환경
---

# severity_v1 · 환경

← [[severity_v1]]

**카탈로그** eukaryotes · **종 수** 136

## 환경 범위

```json
{
 "생활 방식": {
  "parasite": 90,
  "free_living": 46
 },
 "위치": {
  "extracellular": 47,
  "free": 46,
  "intracellular": 43
 },
 "에너지(미토콘드리아)": {
  "aerobic": 115,
  "reduced": 21
 },
 "세포 온도 °C (동물 카탈로그에 있는 종만)": {
  "min": 20.0,
  "median": 25.0,
  "max": 37.0,
  "n": 11
 }
}
```

## 분류군 구성

```json
{
 "fungi": 29,
 "alveolata": 25,
 "discoba": 16,
 "nematoda": 9,
 "platyhelminthes": 8,
 "stramenopiles": 7,
 "chlorophyta": 7,
 "amoebozoa": 6,
 "holozoa": 6,
 "chelicerata": 5,
 "streptophyta": 4,
 "metamonada": 4,
 "cnidaria": 4,
 "insecta": 2,
 "rhodophyta": 2,
 "crustacea": 2
}
```

## GC 함량

```json
{
 "min": 0.16,
 "median": 0.425,
 "max": 0.67,
 "n": 135
}
```

## 축별 대비

```json
{
 "parasite": {
  "pairs_with_axis": 90
 },
 "intracellular": {
  "pairs_with_axis": 43
 },
 "reduced_mitochondria": {
  "pairs_with_axis": 21
 },
 "control_pairs": 22,
 "independent_parasite_clades": 15
}
```

## 요약 수치

```json
{
 "loss_share_coefficients": {
  "base": {
   "weight": -2.3183,
   "ci95": [
    -2.6561,
    -2.0306
   ],
   "verdict": "효과 있음"
  },
  "parasite": {
   "weight": 0.9286,
   "ci95": [
    0.3759,
    1.3762
   ],
   "verdict": "효과 있음"
  },
  "intracellular": {
   "weight": 0.7596,
   "ci95": [
    -0.0647,
    1.4249
   ],
   "verdict": "0과 구분 안 됨"
  },
  "reduced_mitochondria": {
   "weight": 1.7191,
   "ci95": [
    0.9818,
    2.4844
   ],
   "verdict": "효과 있음"
  }
 },
 "typical_share_lost": {
  "free_living": 0.09,
  "extracellular_parasite": 0.199,
  "intracellular_parasite": 0.348,
  "intracellular_reduced_mito": 0.748
 }
}
```

> [!note]
> envelope 밖의 환경에 이 법칙을 쓰면 외삽이다. 값은 문헌 근사치(카탈로그 주석 참조).
