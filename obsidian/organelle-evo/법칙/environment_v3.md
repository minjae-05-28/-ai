---
id: environment_v3
system: 보통 → 극한 환경
status: 현역
tags:
  - 법칙
  - 극한환경
---
# environment_v3

> 세균·고세균 54쌍으로 다시 학습: 환경 축을 넣어도 무엇을 잃는지 예측이 그대로(0.813 vs 0.814, 암기 0.849). 환경은 유전자 구성이 아니라 서열에 남는다.

**시스템**: 보통 → 극한 환경  
**상태**: 현역  
**주제**: [[환경과 서열]]

## 적용 범위 (원문)
Gene-family loss, duplication and gain in bacteria and archaea when a lineage moves to a colder, saltier, anoxic, radiation-exposed or nutrient-poor environment.

## 모델
Linear birth-death per family; log rate = a_pair + x @ (environment change @ W).

## 검증
- leave_one_pair_out_auroc:
  - copies_only: 0.617
  - no_environment: 0.813
  - environment_law: 0.814
  - memorisation: 0.849
- env_vs_none: 0.001

## 한계
- Environment optima are approximate literature values.
- Few pairs per axis (radiation 4, oligotrophy 2, anoxia 4); wide intervals.
- Mars forecast adds axes beyond any single observed environment (extrapolation).

원본: `laws/environment_v3.json`