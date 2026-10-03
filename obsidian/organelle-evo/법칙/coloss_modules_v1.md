---
id: coloss_modules_v1
system: 자유생활 → 기생
status: 현역
tags:
  - 법칙
  - 기생
---
# coloss_modules_v1

> 기생생물에서 유전자군은 거의 독립적으로 사라진다(묶음 효과 +0.001). 예외: 편모 축사, B12 대사.

**시스템**: 자유생활 → 기생  
**상태**: 현역  
**주제**: [[소기관 묶음과 독립성]]

![[coloss_modules_v1.png]]

## 적용 범위 (원문)
Gene-family loss in eukaryotic parasites: which families are lost together (modules).

## 모델
Logistic: logit P(lost) = a_pair + b_family + u_pair . v_family, rank k.

## 검증
- scheme: leave-one-clade-out, half of each held-out parasite's families revealed
- mean_auroc_hidden:
  - k0: 0.806
  - k2: 0.806
  - k4: 0.806
  - k8: 0.801
- best_k: 2
- gain_vs_additive: 0.001

## 한계
- Modules are statistical: co-loss can reflect shared pathways or shared host niche.
- Pairs with the same ancestor proxy are not independent.

원본: `laws/coloss_modules_v1.json`