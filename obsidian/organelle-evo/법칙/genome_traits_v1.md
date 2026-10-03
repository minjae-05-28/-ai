---
id: genome_traits_v1
system: 공통
status: 현역
tags:
  - 법칙
  - 공통
---
# genome_traits_v1

> GTDB 1.2만 종 × 형질 DB: 유전체 특징 4개(GC·크기·코딩 밀도·단백질 밀도)로 온도·산소·숙주 관련 여부를 맞힘. 처음 보는 목에서 숙주 관련 여부는 법칙 0.652가 분류 암기 0.502를 이김. 온도는 암기(4.7°C)가 법칙(5.6°C)을 이김. 숙주 관련 세균은 유전체가 작고 GC·코딩 밀도가 낮음(축소 법칙 재현).

**시스템**: 공통  
**상태**: 현역  
**주제**: [[대규모 유전체 형질]]

## 적용 범위 (원문)
Bacterial and archaeal growth temperature, oxygen use and host association predicted from genome-level traits (GC, genome size, coding density, proteins per Mb), across GTDB species with a trait record. Says nothing about gene content or protein sequence.

## 모델
Ridge (temperature) / logistic (oxygen, host) on standardized genome features; gradient boosting on the same features reported next to it; taxonomy memorisation as the baseline.

## 검증
- temperature:
  - random_5fold: `{"n": 9113, "n_orders": 274, "metric": "MAE (deg C)", "scores": {"mean": 5.9711, "taxonomy": 2.5908, "law_linear": 5.3367, "law_nonlinear": 4.2011, "law+taxonom`
  - leave_order_out: `{"n": 9113, "n_orders": 274, "metric": "MAE (deg C)", "scores": {"mean": 5.9939, "taxonomy": 4.7026, "law_linear": 5.552, "law_nonlinear": 5.1771, "law+taxonomy`
  - coefficients: `{"gc": {"overall": 0.0549, "within_phylum": 1.2669, "same_sign": true}, "log10_genome_size": {"overall": -3.3506, "within_phylum": -2.6421, "same_sign": true}, `
- oxygen:
  - random_5fold: `{"n": 6781, "n_orders": 280, "metric": "AUROC", "scores": {"mean": 0.5, "taxonomy": 0.9681, "law_linear": 0.8378, "law_nonlinear": 0.8807, "law+taxonomy": 0.978`
  - leave_order_out: `{"n": 6781, "n_orders": 280, "metric": "AUROC", "scores": {"mean": 0.5, "taxonomy": 0.7552, "law_linear": 0.7883, "law_nonlinear": 0.7803, "law+taxonomy": 0.850`
  - coefficients: `{"gc": {"overall": 0.533, "within_phylum": 0.0889, "same_sign": true}, "log10_genome_size": {"overall": 1.1848, "within_phylum": 1.1845, "same_sign": true}, "co`
- host:
  - random_5fold: `{"n": 7445, "n_orders": 277, "metric": "AUROC", "scores": {"mean": 0.5, "taxonomy": 0.8434, "law_linear": 0.6731, "law_nonlinear": 0.7631, "law+taxonomy": 0.843`
  - leave_order_out: `{"n": 7445, "n_orders": 277, "metric": "AUROC", "scores": {"mean": 0.5, "taxonomy": 0.5021, "law_linear": 0.6518, "law_nonlinear": 0.6797, "law+taxonomy": 0.643`
  - coefficients: `{"gc": {"overall": -0.0965, "within_phylum": -0.3332, "same_sign": true}, "log10_genome_size": {"overall": -0.6659, "within_phylum": -0.634, "same_sign": true},`

## 한계
- Traits are literature compilations (Madin et al. 2020), not measurements made here.
- Leave-order-out is the honest test for an unseen lineage; random folds let taxonomy memorise.
- Coefficients are associations; within-phylum signs are reported to show what survives the coarsest phylogenetic control.
- Isolation source is where a strain was isolated, not necessarily its lifestyle.

원본: `laws/genome_traits_v1.json`