---
id: severity_v1
system: 자유생활 → 기생
status: 현역
tags:
  - 법칙
  - 기생
---
# severity_v1

> 얼마나 잃나: 자유생활 10%, 세포 밖 기생 26%, 세포 안 36%, 세포 안 + 미토콘드리아 퇴화 72%. 세포 안 효과는 계통 보정 후 유지되지 않음.

**시스템**: 자유생활 → 기생  
**상태**: 현역  
**주제**: [[생활 방식 축]], [[계통 보정]]

![[severity_v1.png]]

## 적용 범위 (원문)
Share of ancestral gene families lost by a eukaryotic lineage, from its lifestyle axes.

## 모델
logit(share lost) = b0 + b_parasite + b_intracellular + b_reduced_mitochondria (additive).

## 검증
- loco_rmse_logit:
  - mean_only: 1.437
  - parasite_only: 1.264
  - all_axes: 1.041
- bootstrap: 2000 clade resamples

## 한계
- Assembly/annotation completeness inflates apparent loss (e.g. Trypanosoma congolense).
- Free-living controls measure drift between relatives, not zero change.

원본: `laws/severity_v1.json`