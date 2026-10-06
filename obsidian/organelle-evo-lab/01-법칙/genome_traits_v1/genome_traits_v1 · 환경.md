---
유형: 환경
법칙: genome_traits_v1
클러스터: 서열·조성
tags:
  - 법칙/genome_traits_v1
  - 클러스터/서열·조성
  - 판정/무승부
  - 유형/환경
---

# genome_traits_v1 · 환경

← [[genome_traits_v1]]

**카탈로그** GTDB + Madin 2020 · **종 수** 11549

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
   "mean": 5.9939,
   "taxonomy": 4.7026,
   "law_linear": 5.552,
   "law_nonlinear": 5.1771,
   "law+taxonomy": 4.6625
  },
  "metric": "MAE (deg C)",
  "법칙 - 분류 암기": {
   "mean": 0.8494,
   "ci95": [
    0.256,
    1.4403
   ]
  },
  "계수(표준화, 전체/문 안)": {
   "gc": {
    "overall": 0.0549,
    "within_phylum": 1.2669,
    "same_sign": true
   },
   "log10_genome_size": {
    "overall": -3.3506,
    "within_phylum": -2.6421,
    "same_sign": true
   },
   "coding_density": {
    "overall": 0.2061,
    "within_phylum": 0.1644,
    "same_sign": true
   },
   "proteins_per_mb": {
    "overall": 2.2393,
    "within_phylum": 0.3077,
    "same_sign": true
   }
  }
 },
 "oxygen": {
  "처음 보는 목": {
   "mean": 0.5,
   "taxonomy": 0.7552,
   "law_linear": 0.7883,
   "law_nonlinear": 0.7803,
   "law+taxonomy": 0.8505
  },
  "metric": "AUROC",
  "법칙 - 분류 암기": {
   "mean": 0.0331,
   "ci95": [
    -0.1108,
    0.179
   ]
  },
  "계수(표준화, 전체/문 안)": {
   "gc": {
    "overall": 0.533,
    "within_phylum": 0.0889,
    "same_sign": true
   },
   "log10_genome_size": {
    "overall": 1.1848,
    "within_phylum": 1.1845,
    "same_sign": true
   },
   "coding_density": {
    "overall": 0.1597,
    "within_phylum": -0.1487,
    "same_sign": false
   },
   "proteins_per_mb": {
    "overall": 0.2866,
    "within_phylum": 0.9559,
    "same_sign": true
   }
  }
 },
 "host": {
  "처음 보는 목": {
   "mean": 0.5,
   "taxonomy": 0.5021,
   "law_linear": 0.6518,
   "law_nonlinear": 0.6797,
   "law+taxonomy": 0.6434
  },
  "metric": "AUROC",
  "법칙 - 분류 암기": {
   "mean": 0.1497,
   "ci95": [
    0.046,
    0.2443
   ]
  },
  "계수(표준화, 전체/문 안)": {
   "gc": {
    "overall": -0.0965,
    "within_phylum": -0.3332,
    "same_sign": true
   },
   "log10_genome_size": {
    "overall": -0.6659,
    "within_phylum": -0.634,
    "same_sign": true
   },
   "coding_density": {
    "overall": -0.3123,
    "within_phylum": -0.3762,
    "same_sign": true
   },
   "proteins_per_mb": {
    "overall": -0.3099,
    "within_phylum": -0.2775,
    "same_sign": true
   }
  }
 }
}
```

> [!note]
> envelope 밖의 환경에 이 법칙을 쓰면 외삽이다. 값은 문헌 근사치(카탈로그 주석 참조).
