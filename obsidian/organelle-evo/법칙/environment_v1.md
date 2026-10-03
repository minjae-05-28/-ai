---
id: environment_v1
system: 보통 → 극한 환경
status: 이전 버전 → environment_v3
tags:
  - 법칙
  - 극한환경
---
# environment_v1

> 세균·고세균 환경 법칙(36종). 환경 축을 넣어도 무엇을 잃는지 예측이 나아지지 않음(0.808 vs 0.816). 일관된 효과는 편모 소실.

**시스템**: 보통 → 극한 환경  
**상태**: 이전 버전 → environment_v3  
**주제**: [[환경과 서열]]

![[environment_v1.png]]

## 적용 범위 (원문)
Gene-family loss, duplication and gain in bacteria and archaea when a lineage moves to a colder, saltier, anoxic, radiation-exposed or nutrient-poor environment.

## 모델
Linear birth-death per family; log rate = a_pair + x @ (environment change @ W).

## 검증
- leave_one_pair_out_auroc:
  - copies_only: 0.614
  - no_environment: 0.816
  - environment_law: 0.808
  - memorisation: 0.804
- env_vs_none: -0.008

## 한계
- Environment optima are approximate literature values.
- Few pairs per axis (radiation 4, oligotrophy 2, anoxia 4); wide intervals.
- Mars forecast adds axes beyond any single observed environment (extrapolation).
- Mars forecast loses ~73% of families, beyond the largest observed loss (53%, Pelagibacter): the count is an extrapolation; use the ranking of families, not the total.

원본: `laws/environment_v1.json`