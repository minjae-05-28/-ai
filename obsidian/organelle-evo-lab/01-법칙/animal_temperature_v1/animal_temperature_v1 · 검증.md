---
유형: 검증
법칙: animal_temperature_v1
클러스터: 동물
판정: 전이 검정
tags:
  - 법칙/animal_temperature_v1
  - 클러스터/동물
  - 판정/전이 검정
  - 유형/검증
---

# animal_temperature_v1 · 검증

← [[animal_temperature_v1]]

> [!warning] 이 프로젝트의 규칙
> 새 수치는 언제나 기준선(암기·희귀도·평균값)과 나란히 둡니다. 기준선을 못 넘으면 음성 결과로 기록합니다.

| 항목 | 값 | 95% 구간 |
| --- | --- | --- |
| law_per_degree_c · ols | 0.0009836 | — |
| law_per_degree_c · tree_pgls | 0.0006997 | — |
| law_per_degree_c · rank_gls | 0.0007847 | — |
| n_animals | 19 | — |
| endotherm_vs_ectotherm · n_endotherm | 3 | — |
| endotherm_vs_ectotherm · n_ectotherm | 14 | — |
| endotherm_vs_ectotherm · mean_ivywrel_endotherm | 0.399 | — |
| endotherm_vs_ectotherm · mean_ivywrel_ectotherm | 0.4201 | — |
| endotherm_vs_ectotherm · delta_temperature_c | 17 | — |
| endotherm_vs_ectotherm · predicted_delta_ivywrel | 0.01672 | — |
| endotherm_vs_ectotherm · observed_delta_ivywrel | -0.02103 | — |
| endotherm_vs_ectotherm · mannwhitney_p | 0.005882 | — |
| endotherm_vs_ectotherm · transfers | False | — |
| all_animals · n | 17 | — |
| all_animals · spearman_temperature_vs_ivywrel | -0.4963 | — |
| all_animals · slope_per_degree_c | -0.0009584 | — |
| all_animals · spearman_ivywrel_vs_fymink | 0.07843 | — |
| all_animals · partial_spearman_controlling_at_bias | -0.4918 | — |

## 방법
- [[잎 숨기기 검증]]
- [[알려진 정답 모의]]
- [[부트스트랩 신뢰구간]]
