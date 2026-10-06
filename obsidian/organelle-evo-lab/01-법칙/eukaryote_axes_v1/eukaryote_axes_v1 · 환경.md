---
유형: 환경
법칙: eukaryote_axes_v1
클러스터: 기생·극한
tags:
  - 법칙/eukaryote_axes_v1
  - 클러스터/기생·극한
  - 판정/검증 없음
  - 유형/환경
---

# eukaryote_axes_v1 · 환경

← [[eukaryote_axes_v1]]

**카탈로그** eukaryotes · **종 수** 32

## 환경 범위

```json
{
 "생활 방식": {
  "free_living": 18,
  "parasite": 14
 },
 "위치": {
  "free": 18,
  "intracellular": 11,
  "extracellular": 3
 },
 "에너지(미토콘드리아)": {
  "aerobic": 28,
  "reduced": 4
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
 "alveolata": 10,
 "discoba": 6,
 "fungi": 6,
 "amoebozoa": 4,
 "holozoa": 4,
 "chlorophyta": 2
}
```

## GC 함량

```json
{
 "min": 0.16,
 "median": 0.455,
 "max": 0.64,
 "n": 32
}
```

## 축별 대비

```json
{
 "parasite": {
  "pairs_with_axis": 14
 },
 "intracellular": {
  "pairs_with_axis": 11
 },
 "reduced_mitochondria": {
  "pairs_with_axis": 4
 },
 "control_pairs": 8,
 "independent_parasite_clades": 4
}
```

## 요약 수치

```json
{
 "loss_parasite": [
  {
   "feature": "atp_synthase",
   "weight": -1.3323,
   "direction": "덜 사라짐"
  },
  {
   "feature": "redox_core",
   "weight": -0.704,
   "direction": "덜 사라짐"
  },
  {
   "feature": "tm_helices",
   "weight": 0.0981,
   "direction": "더 잘 사라짐"
  }
 ],
 "loss_intracellular": [
  {
   "feature": "redox_core",
   "weight": 0.7072,
   "direction": "더 잘 사라짐"
  },
  {
   "feature": "tm_helices",
   "weight": -0.083,
   "direction": "덜 사라짐"
  },
  {
   "feature": "protein_length",
   "weight": 0.0655,
   "direction": "더 잘 사라짐"
  }
 ],
 "loss_reduced_mitochondria": [
  {
   "feature": "redox_core",
   "weight": 1.5424,
   "direction": "더 잘 사라짐"
  },
  {
   "feature": "atp_synthase",
   "weight": 0.7277,
   "direction": "더 잘 사라짐"
  },
  {
   "feature": "transcription",
   "weight": -0.4778,
   "direction": "덜 사라짐"
  },
  {
   "feature": "translation",
   "weight": 0.1792,
   "direction": "더 잘 사라짐"
  },
  {
   "feature": "tm_helices",
   "weight": -0.0528,
   "direction": "덜 사라짐"
  }
 ],
 "duplication_parasite": [
  {
   "feature": "translation",
   "weight": 0.752,
   "direction": "더 잘 사라짐"
  },
  {
   "feature": "protein_targeting",
   "weight": 0.721,
   "direction": "더 잘 사라짐"
  },
  {
   "feature": "redox_core",
   "weight": -0.6244,
   "direction": "덜 사라짐"
  },
  {
   "feature": "tm_helices",
   "weight": 0.227,
   "direction": "더 잘 사라짐"
  }
 ],
 "duplication_intracellular": [
  {
   "feature": "redox_core",
   "weight": 0.8404,
   "direction": "더 잘 사라짐"
  },
  {
   "feature": "tm_helices",
   "weight": -0.2139,
   "direction": "덜 사라짐"
  },
  {
   "feature": "hydrophobicity_gravy",
   "weight": 0.1459,
   "direction": "더 잘 사라짐"
  },
  {
   "feature": "protein_length",
   "weight": 0.1045,
   "direction": "더 잘 사라짐"
  }
 ],
 "duplication_reduced_mitochondria": [
  {
   "feature": "transcription",
   "weight": -1.7211,
   "direction": "덜 사라짐"
  },
  {
   "feature": "translation",
   "weight": -0.5417,
   "direction": "덜 사라짐"
  },
  {
   "feature": "redox_core",
   "weight": -0.1759,
   "direction": "덜 사라짐"
  },
  {
   "feature": "tm_helices",
   "weight": -0.1702,
   "direction": "덜 사라짐"
  },
  {
   "feature": "protein_length",
   "weight": 0.0315,
   "direction": "더 잘 사라짐"
  }
 ]
}
```

> [!note]
> envelope 밖의 환경에 이 법칙을 쓰면 외삽이다. 값은 문헌 근사치(카탈로그 주석 참조).
