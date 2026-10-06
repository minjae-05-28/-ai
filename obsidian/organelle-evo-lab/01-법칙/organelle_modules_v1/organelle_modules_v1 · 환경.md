---
유형: 환경
법칙: organelle_modules_v1
클러스터: 소기관
tags:
  - 법칙/organelle_modules_v1
  - 클러스터/소기관
  - 판정/구조 분석
  - 유형/환경
---

# organelle_modules_v1 · 환경

← [[organelle_modules_v1]]

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
  "value_in_law": 2
 },
 "plastid": {
  "lineages_in_catalogue": 54,
  "gc": {
   "min": 0.14216058394160583,
   "median": 0.329,
   "max": 0.5100431214355265,
   "n": 54
  },
  "value_in_law": 2
 },
 "insect_endosymbiont": {
  "lineages_in_catalogue": 26,
  "gc": {
   "min": 0.17822396305953433,
   "median": 0.268,
   "max": 0.5469899639091991,
   "n": 26
  },
  "value_in_law": 2
 },
 "환경": "의무적 세포 내 공생(숙주 세포질). 자유생활 생물과 유전자 획득에는 적용 범위 밖."
}
```

## 요약 수치

```json
{
 "mitochondrion": {
  "k0": 0.940909424514252,
  "k2": 0.9700009050910232,
  "n": 75
 },
 "plastid": {
  "k0": 0.8961833597818687,
  "k2": 0.9618011251469091,
  "n": 54
 },
 "insect_endosymbiont": {
  "k0": 0.9126341304685982,
  "k2": 0.92585790375942,
  "n": 25
 }
}
```

> [!note]
> envelope 밖의 환경에 이 법칙을 쓰면 외삽이다. 값은 문헌 근사치(카탈로그 주석 참조).
