---
id: gc_confound_v1
system: 공통
status: 현역
tags:
  - 법칙
  - 공통
---
# gc_confound_v1

> GC 함량 교란 검증: 온도(IVYWREL, 전하−극성)와 염분(산성 과잉) 법칙은 GC를 넣어도 효과의 88–102%가 남는다. 빈영양 질소 절약과 무산소 FYMINK는 GC로 설명되고(쌍 단위 FYMINK는 ΔGC 하나로 R² 0.94), 공생세균 AT 편향도 크기가 아니라 GC가 원인(r −0.98).

**시스템**: 공통  
**상태**: 현역  
**주제**: [[환경과 서열]], [[GC 교란]]

## 적용 범위 (원문)
Whether the proteome-composition laws (temperature, salt, oxygen, nutrients, symbiont AT bias) survive genome GC content as a covariate.

## 모델
Environment effect with and without GC (or change in GC) as a covariate; OLS and taxonomy rank GLS; leave-one-pair-out R^2.

## 검증
- species:
  - ivywrel_vs_temperature: `{"n": 70, "without_gc": {"coef": 0.0008303391441150914, "p_ols": 2.7620234622711122e-18, "p_rank_gls": 1.564169822278961e-22}, "with_gc": {"coef": 0.00080629145`
  - cvp_vs_temperature: `{"n": 70, "without_gc": {"coef": 0.001104149552652472, "p_ols": 7.939292914853843e-12, "p_rank_gls": 7.26486650870933e-12}, "with_gc": {"coef": 0.00096665819071`
  - acidic_vs_salt: `{"n": 70, "without_gc": {"coef": 0.0021871446046727687, "p_ols": 2.4769459203940413e-18, "p_rank_gls": 3.502842017483026e-14}, "with_gc": {"coef": 0.00210375599`
  - nitrogen_vs_oligotrophy: `{"n": 70, "without_gc": {"coef": -0.02362844838904612, "p_ols": 0.702203192820845, "p_rank_gls": 0.002799713368396544}, "with_gc": {"coef": -0.00317041653126504`
  - fymink_vs_anoxia: `{"n": 70, "without_gc": {"coef": 0.07698278422301505, "p_ols": 0.004953320715856638, "p_rank_gls": 0.009685417336776954}, "with_gc": {"coef": 0.0148037917505820`
  - gc_explains: `{"fymink": -0.9576139040272919, "garp": 0.9779527951401329, "ivywrel": 0.2671800840872752, "cvp": 0.4559449301384153, "acidic_excess": 0.20110231284481386, "n_s`
- pairs:
  - ivywrel_colder: `{"n": 43, "without_gc": {"coef": -0.017704453069119833, "p_ols": 7.305808723462514e-09, "p_rank_gls": 2.04251375044595e-17}, "with_gc": {"coef": -0.017999433166`
  - cvp_colder: `{"n": 43, "without_gc": {"coef": -0.03411835138757162, "p_ols": 1.0244726907993878e-09, "p_rank_gls": 1.441275649135486e-09}, "with_gc": {"coef": -0.03328047210`
  - acidic_excess_saltier: `{"n": 43, "without_gc": {"coef": 0.01707879371379367, "p_ols": 1.2238567227377165e-06, "p_rank_gls": 3.1027483107363982e-06}, "with_gc": {"coef": 0.016093427610`
  - n_side_oligotrophic: `{"n": 43, "without_gc": {"coef": -0.017617056189328816, "p_ols": 0.017289942002837694, "p_rank_gls": 0.0027180121073696454}, "with_gc": {"coef": -0.001019386904`
  - fymink_anaerobic: `{"n": 43, "without_gc": {"coef": 0.06411596797918603, "p_ols": 0.003495246436783293, "p_rank_gls": 0.0025713326252818445}, "with_gc": {"coef": 0.004883303692205`
- symbionts:
  - fymink: `{"n": 13, "without_gc": {"coef": -0.05854398628687931, "p_ols": 0.0019898713808777536, "p_rank_gls": 0.000139932945956631}, "with_gc": {"coef": 0.00976490784957`
  - median_pi: `{"n": 13, "without_gc": {"coef": -0.6757401044269624, "p_ols": 0.0004918911770746727, "p_rank_gls": 1.3649765622131992e-07}, "with_gc": {"coef": -0.162038864150`
- summary:
  - adaptive_laws_tested: 10
  - survive: `["pair:acidic_excess_saltier", "pair:cvp_colder", "pair:ivywrel_colder", "species:acidic_vs_salt", "species:cvp_vs_temperature", "species:fymink_vs_anoxia", "sp`
  - do_not_survive: `["pair:fymink_anaerobic", "pair:n_side_oligotrophic", "species:nitrogen_vs_oligotrophy"]`

## 한계
- Genome GC from NCBI assembly stats (organelles and symbionts counted from GenBank records).
- GC is itself shaped by environment and lifestyle, so adding it can remove real effects (over-adjustment).
- Taxonomy is a coarse stand-in for a sequence-based phylogeny.

원본: `laws/gc_confound_v1.json`