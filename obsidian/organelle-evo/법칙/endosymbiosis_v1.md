---
id: endosymbiosis_v1
system: 공생 → 소기관
status: 현역
tags:
  - 법칙
  - 공생소기관
---
# endosymbiosis_v1

> 공생 소기관·공생세균에서 어떤 유전자가 남는가. 에너지·번역 유전자는 어디서나 남고, RNA 중합효소는 미토콘드리아는 버리고 엽록체는 지킨다.

**시스템**: 공생 → 소기관  
**상태**: 현역  
**주제**: [[유전자 소실 성향]], [[시스템별 법칙]]

![[endosymbiosis_v1.png]]

## 적용 범위 (원문)
Reductive genome evolution under obligate endosymbiosis: which genes an endosymbiont or organelle genome keeps versus loses/transfers. Not valid for free-living organisms, and it cannot describe gene gain.

## 모델
Retention hazard: P(gene still encoded) = exp(-exp(a_lineage + x @ w)). Positive weight = leaves the organelle/symbiont genome faster.

## 한계
- Lineages are treated as independent; phylogenetic non-independence makes the confidence intervals too narrow.
- Gene matching: annotation names plus reciprocal-best-hit homology; fast-evolving genes can still be missed, inflating loss.
- Associations, not demonstrated causes.

## 관련 문헌 법칙
- [[lit_universal_retention]]
- [[lit_hydrophobicity]]

원본: `laws/endosymbiosis_v1.json`