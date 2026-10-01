---
id: coloss_environment_endosymbiosis_v1
system: 공통
status: 현역
tags:
  - 법칙
  - 공통
---
# coloss_environment_endosymbiosis_v1

> 함께 잃는 묶음: 극한 세균에는 없고, 소기관에는 있다(미토콘드리아 0.923→0.964, 엽록체 0.832→0.915).

**시스템**: 공통  
**상태**: 현역  
**주제**: [[소기관 묶음과 독립성]]

## 적용 범위 (원문)
Whether genes are lost in modules (beyond per-gene propensity) in extremophiles, organelles and insect endosymbionts.

## 모델
Logistic rank-k factorisation; half of a held-out lineage revealed, the rest predicted.

## 검증
- environment:
  - k0: 0.82
  - k2: 0.814
  - n: 21
- mitochondrion:
  - k0: 0.923
  - k2: 0.964
  - n: 30
- plastid:
  - k0: 0.832
  - k2: 0.915
  - n: 21
- insect_endosymbiont:
  - k0: 0.854
  - k2: 0.882
  - n: 13

## 한계
- Held out one pair or lineage at a time; related lineages remain in training.

원본: `laws/coloss_environment_endosymbiosis_v1.json`