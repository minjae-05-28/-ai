---
id: lab_evolution_v1
system: 공통
status: 현역
tags:
  - 법칙
  - 공통
---
# lab_evolution_v1

> 짧은 세대 검증: 비교진화(수억 년)로 만든 소실 법칙이 대장균 5만 세대 실험(LTEE)의 결실을 맞히는지. AUROC 0.59로 거의 못 맞히고, 선택압 없는 돌연변이 축적 대조군(0.60)과 차이가 없다(−0.005 [−0.067, +0.056]). 우리 법칙은 짧은 세대에 쓸 수 없다는 뜻. 속도도 1,000세대당 4개로, 축소 유전체와 규모가 다르다.

**시스템**: 공통  
**상태**: 현역  
**주제**: [[유전자 소실 성향]], [[시간 규모]]

## 적용 범위 (원문)
Whether the comparative loss law, fitted to genomes that diverged over millions of years, predicts which genes are deleted in 50,000 generations of experimental evolution in E. coli (LTEE), with mutation accumulation as the no-selection control.

## 모델
Per gene: mean comparative loss rate of its Pfam families across the project's prokaryote pairs, scored against whether the gene falls inside a deletion in a sequenced clone. Rarity, expression proxy and lab essentiality as baselines.

## 검증
- n_ancestor_genes: 4386
- n_comparative_pairs: 57
- LTEE (50,000 generations, 12 populations, selection):
  - n_clones: 303
  - n_genes_deleted: 856
  - n_scored: 3099
  - n_deleted_scored: 493
  - auroc_comparative_loss_rate: 0.59
  - auroc_ci: `[0.5619434554392145, 0.6170032962547248]`
  - auroc_rarity_baseline: 0.566
  - auroc_low_expression: 0.556
  - deleted_genes_with_knockout_data: 551
  - deleted_that_are_essential: 24
  - essential_share_overall: 0.105
  - essential_share_deleted: 0.044
- MAE (mutation accumulation, almost no selection):
  - n_clones: 15
  - n_genes_deleted: 210
  - n_scored: 3099
  - n_deleted_scored: 95
  - auroc_comparative_loss_rate: 0.595
  - auroc_ci: `[0.5394798570710152, 0.649327464148067]`
  - auroc_rarity_baseline: 0.56
  - auroc_low_expression: 0.601
  - deleted_genes_with_knockout_data: 118
  - deleted_that_are_essential: 4
  - essential_share_overall: 0.105
  - essential_share_deleted: 0.034
- LTEE (50,000 generations, 12 populations, selection), dispensable genes:
  - n_clones: 303
  - n_genes_deleted: 856
  - n_scored: 2749
  - n_deleted_scored: 470
  - auroc_comparative_loss_rate: 0.565
  - auroc_ci: `[0.5354114757077931, 0.5933444461023335]`
  - auroc_rarity_baseline: 0.548
  - auroc_low_expression: 0.528
  - deleted_genes_with_knockout_data: 527
  - deleted_that_are_essential: 0
  - essential_share_overall: 0.0
  - essential_share_deleted: 0.0
- MAE (mutation accumulation, almost no selection), dispensable genes:
  - n_clones: 15
  - n_genes_deleted: 210
  - n_scored: 2749
  - n_deleted_scored: 92
  - auroc_comparative_loss_rate: 0.562
  - auroc_ci: `[0.5065264095017328, 0.6176639147819011]`
  - auroc_rarity_baseline: 0.535
  - auroc_low_expression: 0.58
  - deleted_genes_with_knockout_data: 114
  - deleted_that_are_essential: 0
  - essential_share_overall: 0.0
  - essential_share_deleted: 0.0
- genes_lost_per_1000_generations:
  - mean: 4.05
  - min: 2.14
  - max: 7.64
  - n_populations: 12
- parallelism:
  - 1: 446
  - 2: 121
  - 3: 86
  - 4: 34
  - 5: 23
  - 6: 42
  - 7: 25
  - 8: 2
  - 9: 12
  - 10: 45
  - 11: 8
  - 12: 12
- by_first_generation:
  - deleted by 5,000 generations: `{"n_genes": 134, "mean_comparative_loss_rate": 0.17507336294790682}`
  - first deleted after 20,000: `{"n_genes": 455, "mean_comparative_loss_rate": 0.27297411735620575}`
- spearman_first_generation_vs_comparative_loss_rate: 0.07

## 한계
- One species in one constant medium: a lab regime, not a model of any natural environment.
- LTEE deletions are largely IS150-mediated, so mutation bias shapes which genes are reachable.
- Gene-to-family mapping uses Keio gene names, so unnamed and unmatched genes are left out.
- 50,000 generations removes tens of genes; the reduced genomes in this project lost hundreds to thousands, so the regimes differ in scale by orders of magnitude.

원본: `laws/lab_evolution_v1.json`