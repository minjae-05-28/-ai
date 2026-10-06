---
유형: 환경
법칙: severity_endosymbiosis_v1
클러스터: 소기관
tags:
  - 법칙/severity_endosymbiosis_v1
  - 클러스터/소기관
  - 판정/규모 보고
  - 유형/환경
---

# severity_endosymbiosis_v1 · 환경

← [[severity_endosymbiosis_v1]]

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
  }
 },
 "plastid": {
  "lineages_in_catalogue": 54,
  "gc": {
   "min": 0.14216058394160583,
   "median": 0.329,
   "max": 0.5100431214355265,
   "n": 54
  }
 },
 "insect_endosymbiont": {
  "lineages_in_catalogue": 26,
  "gc": {
   "min": 0.17822396305953433,
   "median": 0.268,
   "max": 0.5469899639091991,
   "n": 26
  }
 },
 "환경": "의무적 세포 내 공생(숙주 세포질). 자유생활 생물과 유전자 획득에는 적용 범위 밖."
}
```

## 요약 수치

```json
{
 "loss_share_coefficients": {
  "mitochondrion": {
   "weight": 0.8231,
   "ci95": [
    0.5574,
    1.0696
   ],
   "verdict": "효과 있음"
  },
  "plastid": {
   "weight": 0.9514,
   "ci95": [
    0.6734,
    1.2326
   ],
   "verdict": "효과 있음"
  },
  "insect_endosymbiont": {
   "weight": 1.9655,
   "ci95": [
    1.6733,
    2.2377
   ],
   "verdict": "효과 있음"
  },
  "nonphotosynthetic_plastid": {
   "weight": 1.5454,
   "ci95": [
    1.2641,
    1.8233
   ],
   "verdict": "효과 있음"
  },
  "animal_mitochondrion": {
   "weight": 0.8403,
   "ci95": [
    0.5863,
    1.1035
   ],
   "verdict": "효과 있음"
  }
 },
 "typical_share_lost": {
  "mitochondrion": 0.6949034443407024,
  "plastid": 0.7213880259661092,
  "insect_endosymbiont": 0.8771308806596735,
  "plastid, non-photosynthetic": 0.923913043478261,
  "mitochondrion, animal": 0.8407016136469685
 }
}
```

> [!note]
> envelope 밖의 환경에 이 법칙을 쓰면 외삽이다. 값은 문헌 근사치(카탈로그 주석 참조).
