---
id: severity_environment_v1
system: 보통 → 극한 환경
status: 현역
tags:
  - 법칙
  - 극한환경
---
# severity_environment_v1

> 극한 환경에서 얼마나 잃나: 환경 변수로 예측되지 않음. 영양 부족(+0.80)만 확실히 더 많이 잃게 함.

**시스템**: 보통 → 극한 환경  
**상태**: 현역  
**주제**: [[환경과 서열]]

## 적용 범위 (원문)
Share of a relative's gene families lost when a bacterium or archaeon moves to an extreme environment.

## 모델
logit(share lost) = environment change @ b (base, colder, saltier, anaerobic, radiation, oligotrophic).

## 검증
- leave_one_pair_out_rmse_logit:
  - mean_only: 0.639
  - environment: 0.92

## 한계
- 21 pairs for 6 coefficients; intervals are wide.

## 관련 문헌 법칙
- [[lit_black_queen]]
- [[lit_streamlining]]

원본: `laws/severity_environment_v1.json`