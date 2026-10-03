---
id: loss_order_v1
system: 자유생활 → 기생
status: 해석 수정됨 → loss_order_v2
tags:
  - 법칙
  - 기생
---
# loss_order_v1

> 잃는 순서가 계통을 넘어 같다. 더 줄어든 기생생물이 덜 줄어든 쪽의 소실을 무작위의 1.62배로 함께 잃음.

**시스템**: 자유생활 → 기생  
**상태**: 해석 수정됨 → loss_order_v2  
**주제**: [[유전자 소실 성향]]

![[loss_order_v1.png]]

## 적용 범위 (원문)
Gene-family loss across independent origins of parasitism in eukaryotes.

## 모델
Nestedness: a more reduced parasite loses what a less reduced one lost, plus more.

## 검증
- cross_clade_comparisons: 2567
- containment_over_random_median: 1.618
- share_above_random: 1.0
- mild_vs_harsh_spearman: 0.663

## 한계
- Ancestor proxies are extant free-living relatives.
- Order is a population tendency; single families can deviate.

원본: `laws/loss_order_v1.json`