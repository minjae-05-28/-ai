---
id: composite_v1
system: 자유생활 → 기생
status: 현역
tags:
  - 법칙
  - 기생
---
# composite_v1

> 조상 역추적용 복합 법칙. 여러 법칙 조합 중 검증 성능으로 선택했고 결과는 축 법칙.

**시스템**: 자유생활 → 기생  
**상태**: 현역  
**주제**: [[조상 역추적]]

![[composite_v1.png]]

## 적용 범위 (원문)
Composite loss law for reconstructing ancestors of eukaryotic parasites from their genomes (reverse inference). Chosen by leave-one-out validation among law mixes.

## 모델
loss weights = 1.0 x eukaryote_axes law(design); used inside a Bayesian reverse birth-death reconstruction.

## 검증
- mean_auroc_recover_lost:
  - prior only (no law): 0.774
  - axis law: 0.776
  - axis + mitochondrion law: 0.763
  - axis + plastid law: 0.775
  - axis + insect-endosymbiont law: 0.774
  - plastid law only: 0.773
  - axis law, wrong lifestyle (free-living): 0.773
- best: axis law

## 한계
- Point weights only (no intervals): a mix of separately fitted laws.
- Validated against extant free-living relatives, not true ancestors.

원본: `laws/composite_v1.json`