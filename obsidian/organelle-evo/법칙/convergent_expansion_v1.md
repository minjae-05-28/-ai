---
id: convergent_expansion_v1
system: 자유생활 → 기생
status: 현역
tags:
  - 법칙
  - 기생
---
# convergent_expansion_v1

> 기생생물은 유전자군을 덜 늘리지만, 아미노산 수송체와 퓨린 재활용 효소는 여러 계통에서 독립적으로 늘린다(숙주에게서 영양을 빼온다).

**시스템**: 자유생활 → 기생  
**상태**: 현역  
**주제**: [[생활 방식 축]]

![[convergent_expansion_v1.png]]

## 적용 범위 (원문)
Gene-family copy-number expansion in eukaryotic parasites, across independent lineages.

## 모델
Family expanded in a pair: parasite copies >= 2x and >= ancestor + 3. Convergent: expanded in more clades than a family-wise 95% permutation threshold.

## 검증
- null: 2000 permutations of expanded families within each clade
- familywise_threshold_clades: 5.0
- n_convergent: 7
- expansion_rate:
  - parasites: 0.02
  - controls: 0.032

## 한계
- Copy number is Pfam-domain gene counts; assembly and annotation quality affect it.
- Clades are coarse; fungi merges several independent parasitic origins.

원본: `laws/convergent_expansion_v1.json`