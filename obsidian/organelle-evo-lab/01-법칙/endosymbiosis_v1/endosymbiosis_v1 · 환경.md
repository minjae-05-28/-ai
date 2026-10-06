---
유형: 환경
법칙: endosymbiosis_v1
클러스터: 소기관
tags:
  - 법칙/endosymbiosis_v1
  - 클러스터/소기관
  - 판정/검증 없음
  - 유형/환경
---

# endosymbiosis_v1 · 환경

← [[endosymbiosis_v1]]

**카탈로그** realdata · **종 수** —

## 환경 범위

```json
{
 "mitochondrion": {
  "lineages_in_catalogue": 75,
  "gc": {
   "min": 0.14014993208651133,
   "median": 0.322,
   "max": 0.6811623469771458,
   "n": 75
  },
  "lineages_in_law": 30
 },
 "plastid": {
  "lineages_in_catalogue": 54,
  "gc": {
   "min": 0.14216058394160583,
   "median": 0.329,
   "max": 0.5100431214355265,
   "n": 54
  },
  "lineages_in_law": 21
 },
 "insect_endosymbiont": {
  "lineages_in_catalogue": 26,
  "gc": {
   "min": 0.17822396305953433,
   "median": 0.268,
   "max": 0.5469899639091991,
   "n": 26
  },
  "lineages_in_law": 13
 },
 "환경": "의무적 세포 내 공생(숙주 세포질). 자유생활 생물과 유전자 획득에는 적용 범위 밖."
}
```

## 요약 수치

```json
{
 "mitochondrion": [
  {
   "feature": "redox_core",
   "weight": -1.5404,
   "direction": "덜 사라짐"
  },
  {
   "feature": "atp_synthase",
   "weight": -1.2993,
   "direction": "덜 사라짐"
  },
  {
   "feature": "translation",
   "weight": -1.1229,
   "direction": "덜 사라짐"
  },
  {
   "feature": "transcription",
   "weight": 1.0169,
   "direction": "더 잘 사라짐"
  },
  {
   "feature": "protein_targeting",
   "weight": 0.9043,
   "direction": "더 잘 사라짐"
  },
  {
   "feature": "tm_helices",
   "weight": -0.3672,
   "direction": "덜 사라짐"
  }
 ],
 "plastid": [
  {
   "feature": "transcription",
   "weight": -2.5516,
   "direction": "덜 사라짐"
  },
  {
   "feature": "atp_synthase",
   "weight": -1.8488,
   "direction": "덜 사라짐"
  },
  {
   "feature": "redox_core",
   "weight": -1.3648,
   "direction": "덜 사라짐"
  },
  {
   "feature": "translation",
   "weight": -1.3034,
   "direction": "덜 사라짐"
  },
  {
   "feature": "protein_targeting",
   "weight": -0.668,
   "direction": "덜 사라짐"
  }
 ],
 "insect_endosymbiont": [
  {
   "feature": "translation",
   "weight": -3.0736,
   "direction": "덜 사라짐"
  },
  {
   "feature": "redox_core",
   "weight": -2.0487,
   "direction": "덜 사라짐"
  },
  {
   "feature": "atp_synthase",
   "weight": -1.7473,
   "direction": "덜 사라짐"
  },
  {
   "feature": "transcription",
   "weight": -1.3994,
   "direction": "덜 사라짐"
  },
  {
   "feature": "protein_targeting",
   "weight": -0.7963,
   "direction": "덜 사라짐"
  },
  {
   "feature": "tm_helices",
   "weight": 0.1623,
   "direction": "더 잘 사라짐"
  }
 ]
}
```

> [!note]
> envelope 밖의 환경에 이 법칙을 쓰면 외삽이다. 값은 문헌 근사치(카탈로그 주석 참조).
