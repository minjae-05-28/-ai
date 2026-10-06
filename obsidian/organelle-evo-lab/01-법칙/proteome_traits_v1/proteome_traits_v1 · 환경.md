---
유형: 환경
법칙: proteome_traits_v1
클러스터: 서열·조성
tags:
  - 법칙/proteome_traits_v1
  - 클러스터/서열·조성
  - 판정/양성
  - 유형/환경
---

# proteome_traits_v1 · 환경

← [[proteome_traits_v1]]

**카탈로그** UniProt reference proteomes + Madin 2020 (envelope shown for the GTDB-matched set) · **종 수** 11549

## 환경 범위

```json
{
 "서식 온도 °C": {
  "min": 3.0,
  "median": 30.0,
  "max": 104.3,
  "n": 9113
 },
 "산소": {
  "호기": 5295,
  "혐기": 1486
 },
 "숙주": {
  "환경": 4384,
  "숙주 관련": 3061
 },
 "GC": {
  "min": 0.135,
  "median": 0.552,
  "max": 0.771,
  "n": 11549
 },
 "유전체 크기 Mb": {
  "min": 0.21,
  "median": 4.01,
  "max": 13.53,
  "n": 11549
 }
}
```

## 분류군 구성

```json
{
 "Pseudomonadota": 4010,
 "Actinomycetota": 2585,
 "Bacillota": 2101,
 "Bacteroidota": 1157,
 "Halobacteriota": 238,
 "Bacillota_I": 225,
 "Desulfobacterota": 169,
 "Cyanobacteriota": 122,
 "Campylobacterota": 113,
 "Spirochaetota": 101,
 "Thermoproteota": 81,
 "Deinococcota": 75
}
```

## 요약 수치

```json
{
 "temperature": {
  "처음 보는 목": {
   "mean": 6.1993,
   "taxonomy": 5.5922,
   "composition": 5.0001,
   "pfam": 3.6522,
   "composition+pfam": 3.4673
  },
  "metric": "MAE (deg C)"
 },
 "oxygen": {
  "처음 보는 목": {
   "mean": 0.5,
   "taxonomy": 0.8297,
   "composition": 0.9232,
   "pfam": 0.9776,
   "composition+pfam": 0.9773
  },
  "metric": "AUROC"
 },
 "host": {
  "처음 보는 목": {
   "mean": 0.5,
   "taxonomy": 0.4849,
   "composition": 0.6739,
   "pfam": 0.8405,
   "composition+pfam": 0.8431
  },
  "metric": "AUROC"
 }
}
```

> [!note]
> envelope 밖의 환경에 이 법칙을 쓰면 외삽이다. 값은 문헌 근사치(카탈로그 주석 참조).
