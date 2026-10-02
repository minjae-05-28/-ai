---
id: animal_temperature_v1
system: 보통 → 극한 환경
status: 현역
tags:
  - 법칙
  - 극한환경
---
# animal_temperature_v1

> 미생물 온도 법칙이 동물 세포에 통하는지. 통하지 않는다. 항온동물(37~42°C)은 변온동물(12~27°C)보다 IVYWREL이 +0.017 높아야 하는데 실제로는 0.021 낮다(부호 반대, p 0.006). °C당 기울기도 −0.00096 대 법칙 +0.00098. AT 편향 보정 후에도 유지. 사람 세포 조성을 온도로 예측할 수 없다는 뜻.

**시스템**: 보통 → 극한 환경  
**상태**: 현역  
**주제**: [[환경과 서열]], [[시간 규모]]

## 적용 범위 (원문)
Whether the prokaryote temperature-composition law transfers to animal cells, tested on mitochondrion-encoded proteomes of endotherms (cells at 36-42 C) against ectotherms (cells near ambient, 12-27 C).

## 모델
Predicted IVYWREL difference from the fitted law (+0.00098 per C) against the observed difference; continuous slope over all animals; AT bias (FYMINK) as the control.

## 검증
- law_per_degree_c:
  - ols: 0.001
  - tree_pgls: 0.001
  - rank_gls: 0.001
- n_animals: 19
- species: `[{"species": "Amphimedon queenslandica", "temperature_c": 25.0, "group": "ectotherm", "ivywrel": 0.449688, "fymink": 0.295381, "cvp": -0.054931, "n_proteins": 1`
- endotherm_vs_ectotherm:
  - n_endotherm: 3
  - n_ectotherm: 14
  - mean_ivywrel_endotherm: 0.399
  - mean_ivywrel_ectotherm: 0.42
  - delta_temperature_c: 17.0
  - predicted_delta_ivywrel: 0.017
  - observed_delta_ivywrel: -0.021
  - mannwhitney_p: 0.006
  - transfers: False
- all_animals:
  - n: 17
  - spearman_temperature_vs_ivywrel: -0.496
  - slope_per_degree_c: -0.001
  - spearman_ivywrel_vs_fymink: 0.078
  - partial_spearman_controlling_at_bias: -0.492
- parasites_of_endotherms: `[{"species": "Ascaris suum", "temperature_c": 39.0, "group": "parasite of an endotherm", "ivywrel": 0.421546, "fymink": 0.369145, "cvp": -0.099532, "n_proteins"`

## 한계
- Only three endotherms have a mitochondrial proteome here, so the group test is weak; the sign and magnitude of the mismatch carry the result, not the p-value.
- Ectotherm temperatures are typical habitat values, not measured cell temperatures.
- Mitochondrion-encoded proteins are few, membrane-bound and hydrophobic, and their composition is dominated by mitochondrial AT bias; nuclear proteomes would be the better test and are not in this dataset.
- A failure to transfer does not mean temperature has no effect on animal proteins, only that this law, fitted to microbes, does not predict it.

원본: `laws/animal_temperature_v1.json`