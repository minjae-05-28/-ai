---
id: loss_prediction_v1
system: 보통 → 극한 환경
status: 현역
tags:
  - 법칙
  - 극한환경
---
# loss_prediction_v1

> 어떤 유전자를 잃나: 극한 세균 54쌍에서 UniProt 1.8만 단백질체로 만든 유전자군 성향(0.825)이 법칙(0.793)과 암기(0.813)를 이기고, 가까운 친척(0.924, 같은 속 빼면 0.896)은 처음으로 '진화 안 함'을 이긴다. 친척은 법칙이 아니라 예측 도구.

**시스템**: 보통 → 극한 환경  
**상태**: 현역  
**주제**: [[유전자 소실 성향]], [[대규모 유전체 형질]]

## 적용 범위 (원문)
Which ancestral gene families a bacterial/archaeal lineage loses when it moves to an extreme environment, scored on held-out lineages: the birth-death law against a per-family propensity estimated from ~18,000 UniProt reference proteomes, and against close relatives of the descendant.

## 모델
propensity20k = rank average of rarity across ~18,000 proteomes and within-genus absence rate, with the evaluated pair's genera removed (a law: properties of the family). relatives = share of the descendant's genus (or family) lacking the family, without its own and the proxy's species (a predictor, not a law: it reads the lineage's relatives). Combinations are rank averages.

## 검증
- extremophiles:
  - n_pairs: 54
  - n_lineages: 26
  - pairs_with_relatives: 48
  - pairs_with_other_genera: 39
  - copies.auroc: `{"mean": 0.6173, "ci95": [0.6078, 0.6271]}`
  - copies.fate: `{"mean": 0.6361, "ci95": [0.6115, 0.6606]}`
  - memorisation.auroc: `{"mean": 0.8131, "ci95": [0.799, 0.8248]}`
  - memorisation.fate: `{"mean": 0.764, "ci95": [0.745, 0.7825]}`
  - law.auroc: `{"mean": 0.793, "ci95": [0.7708, 0.8134]}`
  - law.fate: `{"mean": 0.7453, "ci95": [0.7204, 0.7692]}`
  - no_axes_law.auroc: `{"mean": 0.7979, "ci95": [0.7801, 0.8141]}`
  - no_axes_law.fate: `{"mean": 0.7469, "ci95": [0.7249, 0.7689]}`
- extremophiles_consensus:
  - n_pairs: 54
  - n_lineages: 26
  - pairs_with_relatives: 48
  - pairs_with_other_genera: 39
  - copies.auroc: `{"mean": 0.6054, "ci95": [0.5916, 0.6175]}`
  - copies.fate: `{"mean": 0.676, "ci95": [0.65, 0.7009]}`
  - memorisation.auroc: `{"mean": 0.7878, "ci95": [0.772, 0.8003]}`
  - memorisation.fate: `{"mean": 0.7756, "ci95": [0.7564, 0.7937]}`
  - law.auroc: `{"mean": 0.7642, "ci95": [0.7376, 0.7872]}`
  - law.fate: `{"mean": 0.7555, "ci95": [0.732, 0.7776]}`
  - no_axes_law.auroc: `{"mean": 0.7701, "ci95": [0.7498, 0.7882]}`
  - no_axes_law.fate: `{"mean": 0.7559, "ci95": [0.7345, 0.7764]}`

## 한계
- relatives is not a law: it uses the descendant lineage's close relatives, the information the sibling ceiling showed cross-lineage laws cannot reach. Reported apart from the laws.
- Some genus relatives are near-identical sister species split from the same species (e.g. Lactiplantibacillus argentoratensis, Bacteroides hominis agree with the truth almost as well as the descendant's own UniProt proteome, 0.94 vs 0.93 median). relatives_other_genera removes the descendant's and the proxy's genera and is the stricter number.
- UniProt Pfam misses weak domains HMMER finds; families UniProt never annotates take the median score.
- Fate accuracy removes the top-k families with k = the law's own predicted amount; this deterministic rule beats the stochastic forward simulation of run_forward_evolution.py.
- With a consensus ancestor (proxy's own gains removed) the law falls from 0.793 to 0.764 AUROC while relatives stay at 0.919: part of the law's score came from families only the proxy carried.
- Extremophiles only: the eukaryote parasites are mostly protists, which the UniProt layer (bacteria, archaea, fungi) does not cover.

원본: `laws/loss_prediction_v1.json`