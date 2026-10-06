---
유형: 검증
법칙: genome_traits_v1
클러스터: 서열·조성
판정: 양성
tags:
  - 법칙/genome_traits_v1
  - 클러스터/서열·조성
  - 판정/양성
  - 유형/검증
---

# genome_traits_v1 · 검증

← [[genome_traits_v1]]

> [!warning] 이 프로젝트의 규칙
> 새 수치는 언제나 기준선(암기·희귀도·평균값)과 나란히 둡니다. 기준선을 못 넘으면 음성 결과로 기록합니다.

| 항목 | 값 | 95% 구간 |
| --- | --- | --- |
| temperature · random_5fold · n | 9113 | — |
| temperature · random_5fold · n_orders | 274 | — |
| temperature · random_5fold · metric | MAE (deg C) | — |
| temperature · random_5fold · scores | 5.971 | [—, —] |
| temperature · random_5fold · r2 | -0.0002 | [—, —] |
| temperature · leave_order_out · n | 9113 | — |
| temperature · leave_order_out · n_orders | 274 | — |
| temperature · leave_order_out · metric | MAE (deg C) | — |
| temperature · leave_order_out · scores | 5.994 | [—, —] |
| temperature · leave_order_out · r2 | -0.0061 | [—, —] |
| temperature · leave_order_out · law_linear - taxonomy | 0.8494 | [0.256, 1.44] |
| temperature · leave_order_out · law_nonlinear - law_linear | -0.3749 | [-0.8099, 0.0097] |
| temperature · leave_order_out · law_linear - mean | -0.4419 | [-0.9567, 0.0771] |
| temperature · coefficients · gc · overall | 0.0549 | — |
| temperature · coefficients · gc · within_phylum | 1.267 | — |
| temperature · coefficients · gc · same_sign | True | — |
| temperature · coefficients · log10_genome_size · overall | -3.351 | — |
| temperature · coefficients · log10_genome_size · within_phylum | -2.642 | — |
| temperature · coefficients · log10_genome_size · same_sign | True | — |
| temperature · coefficients · coding_density · overall | 0.2061 | — |
| temperature · coefficients · coding_density · within_phylum | 0.1644 | — |
| temperature · coefficients · coding_density · same_sign | True | — |
| temperature · coefficients · proteins_per_mb · overall | 2.239 | — |
| temperature · coefficients · proteins_per_mb · within_phylum | 0.3077 | — |
| temperature · coefficients · proteins_per_mb · same_sign | True | — |
| oxygen · random_5fold · n | 6781 | — |
| oxygen · random_5fold · n_orders | 280 | — |
| oxygen · random_5fold · metric | AUROC | — |
| oxygen · random_5fold · scores | 0.5 | [—, —] |
| oxygen · random_5fold · note | mean = 0.5 by definition (pooled per-fold constants are not a meaningful AUROC) | — |
| oxygen · leave_order_out · n | 6781 | — |
| oxygen · leave_order_out · n_orders | 280 | — |
| oxygen · leave_order_out · metric | AUROC | — |
| oxygen · leave_order_out · scores | 0.5 | [—, —] |
| oxygen · leave_order_out · note | mean = 0.5 by definition (pooled per-fold constants are not a meaningful AUROC) | — |
| oxygen · leave_order_out · law_linear - taxonomy | 0.0331 | [-0.1108, 0.179] |
| oxygen · leave_order_out · law_nonlinear - law_linear | -0.008 | [-0.0411, 0.0191] |
| oxygen · coefficients · gc · overall | 0.533 | — |
| oxygen · coefficients · gc · within_phylum | 0.0889 | — |
| oxygen · coefficients · gc · same_sign | True | — |
| oxygen · coefficients · log10_genome_size · overall | 1.185 | — |
| oxygen · coefficients · log10_genome_size · within_phylum | 1.185 | — |
| oxygen · coefficients · log10_genome_size · same_sign | True | — |
| oxygen · coefficients · coding_density · overall | 0.1597 | — |
| oxygen · coefficients · coding_density · within_phylum | -0.1487 | — |
| oxygen · coefficients · coding_density · same_sign | False | — |
| oxygen · coefficients · proteins_per_mb · overall | 0.2866 | — |
| oxygen · coefficients · proteins_per_mb · within_phylum | 0.9559 | — |
| oxygen · coefficients · proteins_per_mb · same_sign | True | — |
| host · random_5fold · n | 7445 | — |
| host · random_5fold · n_orders | 277 | — |
| host · random_5fold · metric | AUROC | — |
| host · random_5fold · scores | 0.5 | [—, —] |
| host · random_5fold · note | mean = 0.5 by definition (pooled per-fold constants are not a meaningful AUROC) | — |
| host · leave_order_out · n | 7445 | — |
| host · leave_order_out · n_orders | 277 | — |
| host · leave_order_out · metric | AUROC | — |
| host · leave_order_out · scores | 0.5 | [—, —] |
| host · leave_order_out · note | mean = 0.5 by definition (pooled per-fold constants are not a meaningful AUROC) | — |
| host · leave_order_out · law_linear - taxonomy | 0.1497 | [0.046, 0.2443] |
| host · leave_order_out · law_nonlinear - law_linear | 0.0279 | [-0.0199, 0.0699] |
| host · coefficients · gc · overall | -0.0965 | — |
| host · coefficients · gc · within_phylum | -0.3332 | — |
| host · coefficients · gc · same_sign | True | — |
| host · coefficients · log10_genome_size · overall | -0.6659 | — |
| host · coefficients · log10_genome_size · within_phylum | -0.634 | — |
| host · coefficients · log10_genome_size · same_sign | True | — |
| host · coefficients · coding_density · overall | -0.3123 | — |
| host · coefficients · coding_density · within_phylum | -0.3762 | — |
| host · coefficients · coding_density · same_sign | True | — |
| host · coefficients · proteins_per_mb · overall | -0.3099 | — |
| host · coefficients · proteins_per_mb · within_phylum | -0.2775 | — |
| host · coefficients · proteins_per_mb · same_sign | True | — |

## 방법
- [[잎 숨기기 검증]]
- [[알려진 정답 모의]]
- [[부트스트랩 신뢰구간]]
