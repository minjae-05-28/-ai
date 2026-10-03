---
id: eukaryote_lifestyle_v1
system: 자유생활 → 기생
status: 이전 버전
tags:
  - 법칙
  - 기생
---
# eukaryote_lifestyle_v1

> 진핵생물 유전자군의 복제·소실을 자유생활과 기생으로 나눠 학습. 기생이 법칙을 바꾼다(ΔAIC 213).

**시스템**: 자유생활 → 기생  
**상태**: 이전 버전  
**주제**: [[생활 방식 축]]

![[eukaryote_lifestyle_v1.png]]

## 적용 범위 (원문)
Gene-family (Pfam) duplication, loss and origination in eukaryotes, for free-living lineages and for lineages that became parasites. Learned from free-living-relative -> descendant pairs.

## 모델
Linear birth-death per family with origination: log rate = a_pair + x @ w[lifestyle]. Positive loss weight = family lost faster.

## 한계
- An extant free-living relative stands in for the ancestor; it has evolved too.
- Few pairs per lifestyle; bootstrap over pairs gives wide intervals.
- Pfam families, not orthologues: a family count sums paralogues.

원본: `laws/eukaryote_lifestyle_v1.json`