---
id: forward_evolution_v1
system: 공통
status: 현역
tags:
  - 법칙
  - 공통
---
# forward_evolution_v1

> 조상을 법칙만으로 진화시켜 실제 후손과 비교: 유전자군 단위로는 '진화 안 함'을 못 이기지만, 어떤 기능을 잃을지는 맞힌다(순위 상관 0.5–0.66).

**시스템**: 공통  
**상태**: 현역  
**주제**: [[유전자 소실 성향]]

## 적용 범위 (원문)
Evolving an ancestor proxy forward with the birth-death law alone (its lineage held out, the amount of loss predicted from the lifestyle/environment design) and comparing the result with the real descendant, for extremophile bacteria/archaea and eukaryote parasites, with the proxy as ancestor or a consensus ancestor (families shared with a close free-living relative).

## 모델
run_forward_evolution.py (200 stochastic replicates per pair) and run_function_level.py (GO-slim and keyword functions).

## 검증
- extremophiles:
  - n_pairs: 54
  - n_lineages: 26
  - family_level: `{"law.fate_accuracy": {"mean": 0.6799, "ci95": [0.6626, 0.6984]}, "no_change.fate_accuracy": {"mean": 0.7202, "ci95": [0.6822, 0.7635]}, "random_same_amount.fat`
  - function_level: `{"law.spearman": {"mean": 0.6623, "ci95": [0.6102, 0.7098]}, "memorisation.spearman": {"mean": 0.7234, "ci95": [0.6875, 0.752]}, "law.top_hit": {"mean": 0.7074,`
- extremophiles_consensus:
  - n_pairs: 54
  - n_lineages: 26
  - family_level: `{"law.fate_accuracy": {"mean": 0.7058, "ci95": [0.6856, 0.7263]}, "no_change.fate_accuracy": {"mean": 0.7772, "ci95": [0.7416, 0.8152]}, "random_same_amount.fat`
  - function_level: `{"law.spearman": {"mean": 0.6055, "ci95": [0.5602, 0.6502]}, "memorisation.spearman": {"mean": 0.6811, "ci95": [0.6378, 0.7121]}, "law.top_hit": {"mean": 0.6296`
- parasites:
  - n_pairs: 90
  - n_lineages: 15
  - family_level: `{"law.fate_accuracy": {"mean": 0.6464, "ci95": [0.6324, 0.6626]}, "no_change.fate_accuracy": {"mean": 0.6161, "ci95": [0.5387, 0.7491]}, "random_same_amount.fat`
  - function_level: `{"law.spearman": {"mean": 0.5399, "ci95": [0.4148, 0.6066]}, "memorisation.spearman": {"mean": 0.5962, "ci95": [0.4661, 0.6695]}, "law.top_hit": {"mean": 0.5956`
- parasites_consensus:
  - n_pairs: 90
  - n_lineages: 15
  - family_level: `{"law.fate_accuracy": {"mean": 0.6398, "ci95": [0.6287, 0.6581]}, "no_change.fate_accuracy": {"mean": 0.6574, "ci95": [0.5936, 0.7699]}, "random_same_amount.fat`
  - function_level: `{"law.spearman": {"mean": 0.4916, "ci95": [0.3613, 0.5534]}, "memorisation.spearman": {"mean": 0.5576, "ci95": [0.4287, 0.6358]}, "law.top_hit": {"mean": 0.5978`

## 한계
- Family level: the law beats random choice of the same number of families (fate accuracy +0.06 to +0.08) but does not beat leaving the ancestor unchanged (extremophiles -0.04 [-0.075, -0.011]; consensus -0.07; parasites +0.03 and -0.02, intervals include 0).
- Function level: the law ranks which functions a lineage loses (Spearman 0.49-0.66, top-5 hits 0.60-0.71 against 0.14-0.21 for a uniform split), slightly below memorisation (0.56-0.72).
- With a consensus ancestor the law's AUROC falls (extremophiles 0.793 -> 0.764, parasites 0.774 -> 0.748): part of the score came from families only the proxy carried.
- The predicted amount of loss is no better than the mean share for extremophiles (0.10 vs 0.08-0.09) and better for parasites (0.17 vs 0.19-0.22).
- Predicted gains are mostly wrong (precision about 0.1-0.15).

원본: `laws/forward_evolution_v1.json`