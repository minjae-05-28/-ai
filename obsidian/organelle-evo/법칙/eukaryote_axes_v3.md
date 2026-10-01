---
id: eukaryote_axes_v3
system: 자유생활 → 기생
status: 현역
tags:
  - 법칙
  - 기생
---
# eukaryote_axes_v3

> 축별 법칙을 유전자군 특성 56개로 다시 학습. 처음 보는 기생생물 0.78, 처음 보는 계통 0.777로 계통을 넘어 통한다(수렴).

**시스템**: 자유생활 → 기생  
**상태**: 현역  
**주제**: [[생활 방식 축]], [[유전자 소실 성향]]

![[eukaryote_axes_v3.png]]

## 적용 범위 (원문)
Gene-family loss and duplication in eukaryotes (base law + parasite / intracellular / reduced-mitochondria effects), with families described by GO-slim functions, Pfam clans and cross-species statistics.

## 모델
Linear birth-death per family; log rate = a_pair + x @ (design @ W), enriched x.

## 검증
- folds: 5
- mean_heldout_auroc:
  - copies_only: 0.639
  - base: 0.669
  - enriched: 0.782
  - memorisation: 0.865
- leave_one_clade_out:
  - mean_auroc: `{"copies_only": 0.6389, "law": 0.7769, "memorisation": 0.8022}`
  - note: Law loses 0.005 AUROC on unseen clades; memorisation loses 0.063: the law transfers across independent origins of parasitism.

## 한계
- Ubiquity and copy-number features are computed from free-living species.
- Families never observed in the first 32 species are not counted in later ones.

## 관련 문헌 법칙
- [[lit_gene_loss_propensity]]

원본: `laws/eukaryote_axes_v3.json`