---
유형: 한계
법칙: multicellular_transition_v1
클러스터: 전환 경로
tags:
  - 법칙/multicellular_transition_v1
  - 클러스터/전환 경로
  - 판정/음성
  - 유형/한계
---

# multicellular_transition_v1 · 한계

← [[multicellular_transition_v1]]

### 한계 1
Leave-one-origin-out AUROC: law 0.6191 against control_baseline 0.7298, rarity_baseline 0.8137. Law minus the better baseline per origin: -0.1945 [-0.2289, -0.1677] — the law loses to the better baseline.

### 한계 2
Added to rarity, the law gains -0.0458 [-0.0599, -0.0266] AUROC; against the control signature added to rarity the same way: -0.0456 [-0.0603, -0.0271].

### 한계 3
5 independent origins; the interval is a bootstrap over origins, so it is wide and would narrow only with more origins, not more species per origin.

### 한계 4
Pairs are curated from taxonomy (scripts/transition_catalog.py); the relative stands in for the ancestor, so changes on the relative's own branch are counted as the transition's.

### 한계 5
Presence comes from UniProt Pfam cross-references with no completeness model: an incomplete proteome reads as losses. Reduced genomes (Microsporidia, Giardia, Cryptosporidium) are both incomplete-looking and genuinely reduced, which this design cannot separate.

### 한계 6
Copy-number expansion concordance (Spearman between origins): 0.008 against 0.1564 between unicellular control pairs.

### 한계 7
Dictyostelia are aggregative (cells gather), the others clonal (cells stay together after division): different routes to multicellularity are pooled.

