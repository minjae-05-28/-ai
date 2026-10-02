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
  - ivywrel_vs_temperature: `{"n": 86, "without_gc": {"coef": 0.0007846827969093175, "p_ols": 4.445318433615807e-25, "p_rank_gls": 1.4026427901225574e-29}, "with_gc": {"coef": 0.00076605669`
  - cvp_vs_temperature: `{"n": 86, "without_gc": {"coef": 0.0011314911195783488, "p_ols": 1.2826360080756616e-15, "p_rank_gls": 2.7956914349351982e-14}, "with_gc": {"coef": 0.0010651294`
  - acidic_vs_salt: `{"n": 86, "without_gc": {"coef": 0.0016532843066467589, "p_ols": 2.8549288559408527e-21, "p_rank_gls": 9.102153725007249e-12}, "with_gc": {"coef": 0.00158695368`
  - nitrogen_vs_oligotrophy: `{"n": 86, "without_gc": {"coef": -0.021897687755785544, "p_ols": 0.8118705882493471, "p_rank_gls": 0.0006753135619025098}, "with_gc": {"coef": 0.002744209232022`
  - fymink_vs_anoxia: `{"n": 86, "without_gc": {"coef": 0.0805164234477487, "p_ols": 5.687965000989708e-06, "p_rank_gls": 0.0003614792927730401}, "with_gc": {"coef": 0.018816203136428`
  - gc_explains: `{"fymink": -0.952078947641144, "garp": 0.9783488426958965, "ivywrel": 0.10541844628673738, "cvp": 0.2822756180870567, "acidic_excess": 0.2164818294700734, "n_si`
- pairs:
  - ivywrel_colder: `{"n": 57, "without_gc": {"coef": -0.017009680749822505, "p_ols": 1.3155166503670074e-10, "p_rank_gls": 2.4306774423716094e-24}, "with_gc": {"coef": -0.017132218`
  - cvp_colder: `{"n": 57, "without_gc": {"coef": -0.03335808144228063, "p_ols": 6.614835738467015e-11, "p_rank_gls": 1.8305065944083973e-13}, "with_gc": {"coef": -0.02709061200`
  - acidic_excess_saltier: `{"n": 57, "without_gc": {"coef": 0.01720806023615845, "p_ols": 1.08300918510543e-06, "p_rank_gls": 2.908775330088942e-07}, "with_gc": {"coef": 0.011101685044050`
  - n_side_oligotrophic: `{"n": 57, "without_gc": {"coef": -0.014979902483507293, "p_ols": 0.019935786879246412, "p_rank_gls": 0.00365956595022934}, "with_gc": {"coef": -0.00618505357672`
  - fymink_anaerobic: `{"n": 57, "without_gc": {"coef": 0.05476146791344761, "p_ols": 0.004980798902836206, "p_rank_gls": 0.003240480891754966}, "with_gc": {"coef": 0.0071090799139908`
- symbionts:
  - fymink: `{"n": 25, "without_gc": {"coef": -0.08783153151544101, "p_ols": 2.240287806120025e-06, "p_rank_gls": 7.011868635315649e-10}, "with_gc": {"coef": -0.007034479549`
  - median_pi: `{"n": 25, "without_gc": {"coef": -1.033058827127401, "p_ols": 3.0858241450494217e-07, "p_rank_gls": 2.8504147968063422e-12}, "with_gc": {"coef": -0.191074439333`
- summary:
  - adaptive_laws_tested: 10
  - survive: `["pair:acidic_excess_saltier", "pair:cvp_colder", "pair:ivywrel_colder", "species:acidic_vs_salt", "species:cvp_vs_temperature", "species:fymink_vs_anoxia", "sp`
  - do_not_survive: `["pair:fymink_anaerobic", "pair:n_side_oligotrophic", "species:nitrogen_vs_oligotrophy"]`

## 한계
- Genome GC from NCBI assembly stats (organelles and symbionts counted from GenBank records).
- GC is itself shaped by environment and lifestyle, so adding it can remove real effects (over-adjustment).
- Taxonomy is a coarse stand-in for a sequence-based phylogeny.

원본: `laws/gc_confound_v1.json`