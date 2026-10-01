---
id: loss_order_v2
system: 공통
status: 현역
tags:
  - 법칙
  - 공통
---
# loss_order_v2

> 네 시스템 공통: 순서는 유전자별 소실 성향만으로 설명된다(유전자별 소실률을 고정한 귀무모형보다 엄격하지 않음).

**시스템**: 공통  
**상태**: 현역  
**주제**: [[유전자 소실 성향]]

![[loss_order_v2.png]]

## 적용 범위 (원문)
Order of gene loss in genome reduction: organelles, insect endosymbionts and eukaryotic parasites.

## 모델
Nestedness (containment) against row-fixed and row-and-column-fixed (curveball) nulls.

## 검증
- n_null: 200
- results:
  - mitochondrion: `{"lineages": 30, "genes": 70, "containment": 0.9500880043358108, "row_null_mean": 0.7816549815079981, "row_null_z": 43.99355504017113, "fixed_null_mean": 0.9532`
  - plastid: `{"lineages": 21, "genes": 242, "containment": 0.8834475465415478, "row_null_mean": 0.7551460507804125, "row_null_z": 50.98432529952042, "fixed_null_mean": 0.899`
  - insect_endosymbiont: `{"lineages": 13, "genes": 1921, "containment": 0.9175135798322263, "row_null_mean": 0.8141304515021488, "row_null_z": 85.66423279655567, "fixed_null_mean": 0.92`
  - eukaryote_parasites: `{"lineages": 51, "genes": 1132, "containment": 0.49556884613643787, "row_null_mean": 0.2737480306631713, "row_null_z": 146.16585181042637, "fixed_null_mean": 0.`

## 한계
- Beating the fixed-fixed null means ordering beyond per-gene loss rates.
- Lineages are not independent (shared ancestry inflates nestedness).

## 관련 문헌 법칙
- [[lit_gene_loss_propensity]]
- [[lit_ordered_mito_loss]]

원본: `laws/loss_order_v2.json`