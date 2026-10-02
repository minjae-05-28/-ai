---
id: sequence_v1
system: 공통
status: 현역
tags:
  - 법칙
  - 공통
---
# sequence_v1

> 단백질 서열 수준: 환경은 유전자 소실이 아니라 아미노산 조성 변화를 설명한다(R² 0.53–0.63). 고온 IVYWREL, 고염 산성, 빈영양 질소 절약, 공생 AT 편향.

**시스템**: 공통  
**상태**: 현역  
**주제**: [[환경과 서열]]

## 적용 범위 (원문)
Proteome amino-acid composition: temperature, salt, nutrient and genome-reduction signals.

## 모델
Correlations and least-squares axis laws on proteome statistics (scripts/run_sequence_laws.py).

## 검증
- temperature:
  - n: 86
  - spearman_ivywrel: 0.65
  - pearson_ivywrel: 0.85
  - ogt_per_0.01_ivywrel: 7.342
  - spearman_cvp: 0.626
  - rmse_mean_only: 17.962
  - rmse_ivywrel_loo_group: 10.32
  - rmse_20aa_ridge_loo_group: 11.289
- salt:
  - spearman_acidic_excess: 0.563
  - spearman_median_pi: -0.511
  - halophiles_ge_15pct: `{"Haloarcula marismortui": {"acidic_excess": 0.084855, "median_pi": 4.206884}, "Halobacterium salinarum": {"acidic_excess": 0.078672, "median_pi": 4.26881}, "Ha`
  - others_median_pi: 6.648
- environment_pairs:
  - n_pairs: 57
  - by_statistic: `{"ivywrel": {"loo_r2_environment": 0.5686674176506967, "coef": {"base": 0.003998825936436327, "colder": -0.02658101206765905, "saltier": -0.0062457141524740085,`
- oligotrophy: `[{"pair": "Synechococcus elongatus -> Prochlorococcus marinus", "n_side_change": -0.025682999999999956}, {"pair": "Cereibacter sphaeroides -> Candidatus Pelagib`
- endosymbionts:
  - spearman_size_fymink: -0.796
  - spearman_size_pi: -0.828
  - table: `{"Arsenophonus nasoniae": {"n_proteins": 4221, "fymink": 0.293604, "median_pi": 8.466324, "n_side": 0.372428}, "Buchnera aphidicola (Cinara tujafilina)": {"n_pr`
- eukaryote_pairs:
  - n_pairs: 99
  - by_statistic: `{"fymink": {"loo_clade_r2": 0.06772146651298305, "coef": {"base": -0.0030539000000000087, "parasite": 0.0008898947149867734, "intracellular": 0.0726791389203473`

## 한계
- Optimal temperatures and salinities are approximate literature values.
- Species are treated as independent (no phylogenetic correction).

## 관련 문헌 법칙
- [[lit_ivywrel_temperature]]
- [[lit_halophile_acidic_proteome]]
- [[lit_nitrogen_economy]]
- [[lit_symbiont_at_bias]]

원본: `laws/sequence_v1.json`