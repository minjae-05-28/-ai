---
id: eukaryote_axes_v1
system: 자유생활 → 기생
status: 이전 버전
tags:
  - 법칙
  - 기생
---
# eukaryote_axes_v1

> 기생을 기생·세포 안·미토콘드리아 퇴화 세 축으로 나눔. 전자전달 유전자 소실은 미토콘드리아 퇴화에서 온다(+1.54).

**시스템**: 자유생활 → 기생  
**상태**: 이전 버전  
**주제**: [[생활 방식 축]]

![[eukaryote_axes_v1.png]]

## 적용 범위 (원문)
Gene-family (Pfam) loss and duplication in eukaryotes, split into a base law plus the additive effects of parasitism, intracellular life and reduced mitochondria.

## 모델
Linear birth-death per family with origination; log rate = a_pair + x @ (design @ W), design = [1, parasite, intracellular, reduced_mitochondria].

## 한계
- Extant free-living relatives stand in for ancestors.
- Few pairs per axis; bootstrap over pairs.
- Axis labels are coarse summaries of each species' biology.

원본: `laws/eukaryote_axes_v1.json`