---
id: severity_endosymbiosis_v1
system: 공생 → 소기관
status: 현역
tags:
  - 법칙
  - 공생소기관
---
# severity_endosymbiosis_v1

> 공생에서 얼마나 잃나: 광합성 안 하는 색소체 92%, 동물 미토콘드리아 82%, 곤충 공생세균 85%.

**시스템**: 공생 → 소기관  
**상태**: 현역  
**주제**: [[시스템별 법칙]]

## 적용 범위 (원문)
Share of the ancestral gene set lost by organelles and insect endosymbionts.

## 모델
logit(share lost) = system + non-photosynthetic plastid + animal host (mitochondria).

## 검증
- leave_one_lineage_out_rmse_logit:
  - system_only: 1.011
  - with_covariates: 0.995
- typical_share_lost:
  - mitochondrion: 0.695
  - plastid: 0.721
  - insect_endosymbiont: 0.877
  - plastid, non-photosynthetic: 0.924
  - mitochondrion, animal: 0.841

## 한계
- Mitochondrial and plastid universes are the union over lineages, not a true ancestor.

## 관련 문헌 법칙
- [[lit_deletional_bias]]

원본: `laws/severity_endosymbiosis_v1.json`