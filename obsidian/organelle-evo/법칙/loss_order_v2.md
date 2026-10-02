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
  - mitochondrion: `{"lineages": 75, "genes": 80, "containment": 0.9619958263945191, "row_null_mean": 0.7870677302414206, "row_null_z": 185.145322681353, "fixed_null_mean": 0.96423`
  - plastid: `{"lineages": 54, "genes": 271, "containment": 0.9347197126501351, "row_null_mean": 0.8129280567509973, "row_null_z": 211.12466287680363, "fixed_null_mean": 0.94`
  - insect_endosymbiont: `{"lineages": 25, "genes": 2206, "containment": 0.9464332813407622, "row_null_mean": 0.8279762255987513, "row_null_z": 264.02354903687086, "fixed_null_mean": 0.9`
  - eukaryote_parasites: `{"lineages": 79, "genes": 1238, "containment": 0.46820053928809835, "row_null_mean": 0.24848250962748422, "row_null_z": 164.7504720231406, "fixed_null_mean": 0.`

## 한계
- Beating the fixed-fixed null means ordering beyond per-gene loss rates.
- Lineages are not independent (shared ancestry inflates nestedness).

## 관련 문헌 법칙
- [[lit_gene_loss_propensity]]
- [[lit_ordered_mito_loss]]

원본: `laws/loss_order_v2.json`