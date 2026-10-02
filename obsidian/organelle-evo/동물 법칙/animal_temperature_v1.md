---
id: animal_temperature_v1
system: 동물 세포
status: 현역 (일부는 animal_axes_v1로 갱신)
tags:
  - 법칙
  - 동물세포
---
# animal_temperature_v1

> 미생물 온도 법칙이 동물 세포에 전이되는지. 전이되지 않는다. 미토콘드리아 단백질체에서 항온동물(세포 37~42°C)은 변온동물(12~27°C)보다 IVYWREL이 +0.017 높아야 하는데 실제로는 0.021 낮다(부호 반대, p 0.006). 다만 핵 단백질체로 다시 보면 부호는 같고 5배 약하다 — 부호 역전은 미토콘드리아 AT 편향의 성질이었다.

**저장소**: `laws/animals/` (미생물 법칙과 분리)  
**상태**: 현역 (일부는 animal_axes_v1로 갱신)  
**주제**: [[동물 세포 법칙]], [[시간 규모]]

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
- SUPERSEDED IN PART by animal_axes_v1, which uses nuclear proteomes (69 species, ~20k proteins each) instead of the 13 mitochondrion-encoded genes: there the temperature coefficient for IVYWREL is +0.0002 per C, the SAME sign as the microbial law but about five times weaker, and it does not survive leave-one-clade-out or the clade-level refit. So the reversed sign reported here is a property of mitochondrial proteomes, driven by mitochondrial AT bias, and not of animal cells in general. The conclusion that the microbial law must not be applied to animal cells stands on both datasets; the claim of an inverted law does not.
