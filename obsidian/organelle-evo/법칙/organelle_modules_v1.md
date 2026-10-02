---
id: organelle_modules_v1
system: 공생 → 소기관
status: 현역
tags:
  - 법칙
  - 공생소기관
---
# organelle_modules_v1

> 소기관이 함께 잃는 묶음의 정체: NDH 복합체(홍조류 계열 색소체), 광수확 안테나(녹색 계열), 리보솜 단백질 + 호흡 복합체 부단위(식물·동물 미토콘드리아), 보조인자 합성(부크네라).

**시스템**: 공생 → 소기관  
**상태**: 현역  
**주제**: [[소기관 묶음과 독립성]]

## 적용 범위 (원문)
Genes that organelles and insect endosymbionts lose together (co-loss modules).

## 모델
Logistic rank-2 factorisation of gene loss per lineage; modules named by top-loading genes.

## 검증
- hidden_half_auroc:
  - mitochondrion: `{"k0": 0.940909424514252, "k2": 0.9700009050910232, "n": 75}`
  - plastid: `{"k0": 0.8961833597818687, "k2": 0.9618011251469091, "n": 54}`
  - insect_endosymbiont: `{"k0": 0.9126341304685982, "k2": 0.92585790375942, "n": 25}`

## 한계
- Modules can reflect shared function (complexes, operons) or shared phylogeny.

## 관련 문헌 법칙
- [[lit_plastome_degradation_order]]

원본: `laws/organelle_modules_v1.json`