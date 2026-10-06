---
유형: 한계
법칙: loss_prediction_v1
클러스터: 예측
tags:
  - 법칙/loss_prediction_v1
  - 클러스터/예측
  - 판정/양성
  - 유형/한계
---

# loss_prediction_v1 · 한계

← [[loss_prediction_v1]]

### 한계 1
relatives is not a law: it uses the descendant lineage's close relatives, the information the sibling ceiling showed cross-lineage laws cannot reach. Reported apart from the laws.

### 한계 2
Some genus relatives are near-identical sister species split from the same species (e.g. Lactiplantibacillus argentoratensis, Bacteroides hominis agree with the truth almost as well as the descendant's own UniProt proteome, 0.94 vs 0.93 median). relatives_other_genera removes the descendant's and the proxy's genera and is the stricter number.

### 한계 3
UniProt Pfam misses weak domains HMMER finds; families UniProt never annotates take the median score.

### 한계 4
Fate accuracy removes the top-k families with k = the law's own predicted amount; this deterministic rule beats the stochastic forward simulation of run_forward_evolution.py.

### 한계 5
With a consensus ancestor (proxy's own gains removed) the law falls from 0.793 to 0.764 AUROC while relatives stay at 0.919: part of the law's score came from families only the proxy carried.

### 한계 6
Extremophiles only: the eukaryote parasites are mostly protists, which the UniProt layer (bacteria, archaea, fungi) does not cover.

