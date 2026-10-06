---
유형: 환경
법칙: eukaryote_axes_v3
클러스터: 기생·극한
tags:
  - 법칙/eukaryote_axes_v3
  - 클러스터/기생·극한
  - 판정/음성
  - 유형/환경
---

# eukaryote_axes_v3 · 환경

← [[eukaryote_axes_v3]]

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
 "loss_parasite": [
  {
   "feature": "go:mitochondrion",
   "weight": -0.3061,
   "direction": "덜 사라짐"
  },
  {
   "feature": "kw:cell_adhesion_surface",
   "weight": -0.3038,
   "direction": "덜 사라짐"
  },
  {
   "feature": "go:ribosome",
   "weight": 0.2579,
   "direction": "더 잘 사라짐"
  },
  {
   "feature": "go:DNA-templated transcription",
   "weight": 0.2561,
   "direction": "더 잘 사라짐"
  },
  {
   "feature": "go:organelle",
   "weight": 0.2158,
   "direction": "더 잘 사라짐"
  },
  {
   "feature": "go:ligase activity",
   "weight": 0.1759,
   "direction": "더 잘 사라짐"
  }
 ],
 "loss_intracellular": [
  {
   "feature": "go:DNA-templated transcription",
   "weight": -0.4818,
   "direction": "덜 사라짐"
  },
  {
   "feature": "atp_synthase",
   "weight": -0.4791,
   "direction": "덜 사라짐"
  },
  {
   "feature": "kw:gtpase_signalling",
   "weight": -0.479,
   "direction": "덜 사라짐"
  },
  {
   "feature": "go:carbohydrate derivative metabolic process",
   "weight": -0.3801,
   "direction": "덜 사라짐"
  },
  {
   "feature": "go:ribosome",
   "weight": -0.3575,
   "direction": "덜 사라짐"
  },
  {
   "feature": "translation",
   "weight": -0.3173,
   "direction": "덜 사라짐"
  }
 ],
 "loss_reduced_mitochondria": [
  {
   "feature": "go:mitochondrion",
   "weight": 0.9777,
   "direction": "더 잘 사라짐"
  },
  {
   "feature": "redox_core",
   "weight": 0.7989,
   "direction": "더 잘 사라짐"
  },
  {
   "feature": "go:DNA-templated transcription",
   "weight": -0.5186,
   "direction": "덜 사라짐"
  },
  {
   "feature": "go:carbohydrate metabolic process",
   "weight": -0.3461,
   "direction": "덜 사라짐"
  },
  {
   "feature": "kw:cytoskeleton_motor",
   "weight": 0.3455,
   "direction": "더 잘 사라짐"
  },
  {
   "feature": "go:ribosome",
   "weight": -0.3288,
   "direction": "덜 사라짐"
  }
 ],
 "duplication_parasite": [
  {
   "feature": "kw:cilium_flagellum",
   "weight": -0.6404,
   "direction": "덜 사라짐"
  },
  {
   "feature": "kw:cell_adhesion_surface",
   "weight": -0.3361,
   "direction": "덜 사라짐"
  },
  {
   "feature": "go:structural molecule activity",
   "weight": -0.3098,
   "direction": "덜 사라짐"
  },
  {
   "feature": "kw:protease",
   "weight": 0.2612,
   "direction": "더 잘 사라짐"
  },
  {
   "feature": "in_clan",
   "weight": 0.2498,
   "direction": "더 잘 사라짐"
  },
  {
   "feature": "go:regulation of DNA-templated transcription",
   "weight": -0.2273,
   "direction": "덜 사라짐"
  }
 ],
 "duplication_intracellular": [
  {
   "feature": "kw:gtpase_signalling",
   "weight": -0.4691,
   "direction": "덜 사라짐"
  },
  {
   "feature": "go:molecular function regulator activity",
   "weight": -0.4005,
   "direction": "덜 사라짐"
  },
  {
   "feature": "kw:phosphatase",
   "weight": -0.3489,
   "direction": "덜 사라짐"
  },
  {
   "feature": "protein_targeting",
   "weight": -0.3258,
   "direction": "덜 사라짐"
  },
  {
   "feature": "go:carbohydrate derivative metabolic process",
   "weight": -0.3255,
   "direction": "덜 사라짐"
  },
  {
   "feature": "kw:ubiquitin_system",
   "weight": -0.3077,
   "direction": "덜 사라짐"
  }
 ],
 "duplication_reduced_mitochondria": [
  {
   "feature": "kw:cilium_flagellum",
   "weight": 0.8068,
   "direction": "더 잘 사라짐"
  },
  {
   "feature": "go:catalytic activity, acting on RNA",
   "weight": -0.6255,
   "direction": "덜 사라짐"
  },
  {
   "feature": "go:DNA-templated transcription",
   "weight": -0.5169,
   "direction": "덜 사라짐"
  },
  {
   "feature": "protein_targeting",
   "weight": -0.473,
   "direction": "덜 사라짐"
  },
  {
   "feature": "transcription",
   "weight": -0.4495,
   "direction": "덜 사라짐"
  },
  {
   "feature": "go:carbohydrate metabolic process",
   "weight": -0.4077,
   "direction": "덜 사라짐"
  }
 ]
}
```

> [!note]
> envelope 밖의 환경에 이 법칙을 쓰면 외삽이다. 값은 문헌 근사치(카탈로그 주석 참조).
