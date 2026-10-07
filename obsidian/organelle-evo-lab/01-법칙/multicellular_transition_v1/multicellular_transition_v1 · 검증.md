---
유형: 검증
법칙: multicellular_transition_v1
클러스터: 전환 경로
판정: 음성
tags:
  - 법칙/multicellular_transition_v1
  - 클러스터/전환 경로
  - 판정/음성
  - 유형/검증
---

# multicellular_transition_v1 · 검증

← [[multicellular_transition_v1]]

> [!warning] 이 프로젝트의 규칙
> 새 수치는 언제나 기준선(암기·희귀도·평균값)과 나란히 둡니다. 기준선을 못 넘으면 음성 결과로 기록합니다.

| 항목 | 값 | 95% 구간 |
| --- | --- | --- |
| law_plus_rarity_minus_control_plus_rarity | -0.0456 | [-0.0603, -0.0271] |
| leave_one_origin_out · metric | auroc | — |
| leave_one_origin_out · what | predict which candidate families the held-out origin gained | — |
| leave_one_origin_out · law | 0.6191 | — |
| leave_one_origin_out · control_baseline | 0.7298 | — |
| leave_one_origin_out · rarity_baseline | 0.8137 | — |
| per_origin · Volvocales · n_candidates | 14588 | — |
| per_origin · Volvocales · n_changed | 87 | — |
| per_origin · Volvocales · share_changed | 0.006 | — |
| per_origin · Volvocales · law | 0.6273 | — |
| per_origin · Volvocales · control_baseline | 0.7288 | — |
| per_origin · Volvocales · rarity_baseline | 0.7936 | — |
| per_origin · Volvocales · law+rarity | 0.7823 | — |
| per_origin · Volvocales · combined_minus_rarity | -0.0113 | — |
| per_origin · Volvocales · control_baseline+rarity | 0.8176 | — |
| per_origin · Volvocales · law_vs_control_combined | -0.0353 | — |
| per_origin · Metazoa · n_candidates | 13446 | — |
| per_origin · Metazoa · n_changed | 1032 | — |
| per_origin · Metazoa · share_changed | 0.0768 | — |
| per_origin · Metazoa · law | 0.5399 | — |
| per_origin · Metazoa · control_baseline | 0.5862 | — |
| per_origin · Metazoa · rarity_baseline | 0.7978 | — |
| per_origin · Metazoa · law+rarity | 0.7333 | — |
| per_origin · Metazoa · combined_minus_rarity | -0.0645 | — |
| per_origin · Metazoa · control_baseline+rarity | 0.746 | — |
| per_origin · Metazoa · law_vs_control_combined | -0.0127 | — |
| per_origin · Dictyostelia · n_candidates | 13868 | — |
| per_origin · Dictyostelia · n_changed | 353 | — |
| per_origin · Dictyostelia · share_changed | 0.0255 | — |
| per_origin · Dictyostelia · law | 0.6042 | — |
| per_origin · Dictyostelia · control_baseline | 0.7417 | — |
| per_origin · Dictyostelia · rarity_baseline | 0.7817 | — |
| per_origin · Dictyostelia · law+rarity | 0.7235 | — |
| per_origin · Dictyostelia · combined_minus_rarity | -0.0582 | — |
| per_origin · Dictyostelia · control_baseline+rarity | 0.7855 | — |
| per_origin · Dictyostelia · law_vs_control_combined | -0.062 | — |
| per_origin · Phaeophyceae · n_candidates | 14963 | — |
| per_origin · Phaeophyceae · n_changed | 691 | — |
| per_origin · Phaeophyceae · share_changed | 0.0462 | — |
| per_origin · Phaeophyceae · law | 0.6595 | — |
| per_origin · Phaeophyceae · control_baseline | 0.8042 | — |
| per_origin · Phaeophyceae · rarity_baseline | 0.8664 | — |
| per_origin · Phaeophyceae · law+rarity | 0.8125 | — |
| per_origin · Phaeophyceae · combined_minus_rarity | -0.0539 | — |
| per_origin · Phaeophyceae · control_baseline+rarity | 0.8721 | — |
| per_origin · Phaeophyceae · law_vs_control_combined | -0.0596 | — |
| per_origin · Rhodophyta (Bangiophyceae + Florideophyceae) · n_candidates | 15234 | — |
| per_origin · Rhodophyta (Bangiophyceae + Florideophyceae) · n_changed | 264 | — |
| per_origin · Rhodophyta (Bangiophyceae + Florideophyceae) · share_changed | 0.0173 | — |
| per_origin · Rhodophyta (Bangiophyceae + Florideophyceae) · law | 0.6647 | — |
| per_origin · Rhodophyta (Bangiophyceae + Florideophyceae) · control_baseline | 0.7883 | — |
| per_origin · Rhodophyta (Bangiophyceae + Florideophyceae) · rarity_baseline | 0.8288 | — |
| per_origin · Rhodophyta (Bangiophyceae + Florideophyceae) · law+rarity | 0.7879 | — |
| per_origin · Rhodophyta (Bangiophyceae + Florideophyceae) · combined_minus_rarity | -0.0409 | — |
| per_origin · Rhodophyta (Bangiophyceae + Florideophyceae) · control_baseline+rarity | 0.8464 | — |
| per_origin · Rhodophyta (Bangiophyceae + Florideophyceae) · law_vs_control_combined | -0.0585 | — |
| law_alone_minus_best_baseline | -0.1945 | [-0.2289, -0.1677] |
| law_plus_rarity_minus_rarity | -0.0458 | [-0.0599, -0.0266] |
| expansion_concordance · metric | spearman | — |
| expansion_concordance · what | mean pairwise rank correlation of log2 copy-number change over shared families | — |
| expansion_concordance · multicellular_origins | 0.008 | — |
| expansion_concordance · n_origin_pairs | 10 | — |
| expansion_concordance · control_baseline | 0.1564 | — |
| expansion_concordance · n_control_pairs | 10 | — |
| marker_panel · cell adhesion / extracellular matrix · Cadherin · share_of_derived_with_it | 0.214 | — |
| marker_panel · cell adhesion / extracellular matrix · Cadherin · share_of_relatives_with_it | 0.231 | — |
| marker_panel · cell adhesion / extracellular matrix · Cadherin · changed_in_origins | 0 | — |
| marker_panel · cell adhesion / extracellular matrix · Cadherin · changed_in_controls | 0.111 | — |
| marker_panel · cell adhesion / extracellular matrix · Integrin_beta · share_of_derived_with_it | 0.286 | — |
| marker_panel · cell adhesion / extracellular matrix · Integrin_beta · share_of_relatives_with_it | 0.077 | — |
| marker_panel · cell adhesion / extracellular matrix · Integrin_beta · changed_in_origins | 0.25 | — |
| marker_panel · cell adhesion / extracellular matrix · Integrin_beta · changed_in_controls | 0.143 | — |
| marker_panel · cell adhesion / extracellular matrix · Integrin_alpha · share_of_derived_with_it | 0 | — |
| marker_panel · cell adhesion / extracellular matrix · Integrin_alpha · share_of_relatives_with_it | 0 | — |
| marker_panel · cell adhesion / extracellular matrix · Integrin_alpha · changed_in_origins | 0 | — |
| marker_panel · cell adhesion / extracellular matrix · Integrin_alpha · changed_in_controls | 0 | — |
| marker_panel · cell adhesion / extracellular matrix · Laminin_G_1 · share_of_derived_with_it | 0.214 | — |
| marker_panel · cell adhesion / extracellular matrix · Laminin_G_1 · share_of_relatives_with_it | 0.154 | — |
| marker_panel · cell adhesion / extracellular matrix · Laminin_G_1 · changed_in_origins | 0 | — |
| marker_panel · cell adhesion / extracellular matrix · Laminin_G_1 · changed_in_controls | 0.111 | — |
| marker_panel · cell adhesion / extracellular matrix · Collagen · share_of_derived_with_it | 0.643 | — |
| marker_panel · cell adhesion / extracellular matrix · Collagen · share_of_relatives_with_it | 0.462 | — |
| marker_panel · cell adhesion / extracellular matrix · Collagen · changed_in_origins | 0.5 | — |
| marker_panel · cell adhesion / extracellular matrix · Collagen · changed_in_controls | 0.429 | — |
| marker_panel · cell adhesion / extracellular matrix · fn3 · share_of_derived_with_it | 0.5 | — |
| marker_panel · cell adhesion / extracellular matrix · fn3 · share_of_relatives_with_it | 0.769 | — |
| marker_panel · cell adhesion / extracellular matrix · fn3 · changed_in_origins | 0 | — |
| marker_panel · cell adhesion / extracellular matrix · fn3 · changed_in_controls | 1 | — |
| marker_panel · cell adhesion / extracellular matrix · EGF · share_of_derived_with_it | 0.286 | — |
| marker_panel · cell adhesion / extracellular matrix · EGF · share_of_relatives_with_it | 0.385 | — |
| marker_panel · cell adhesion / extracellular matrix · EGF · changed_in_origins | 0.5 | — |
| marker_panel · cell adhesion / extracellular matrix · EGF · changed_in_controls | 0.143 | — |
| marker_panel · developmental transcription factors · Homeobox_KN · share_of_derived_with_it | 1 | — |
| marker_panel · developmental transcription factors · Homeobox_KN · share_of_relatives_with_it | 0.923 | — |
| marker_panel · developmental transcription factors · Homeobox_KN · changed_in_origins | None | — |
| marker_panel · developmental transcription factors · Homeobox_KN · changed_in_controls | 0 | — |

## 방법
- [[잎 숨기기 검증]]
- [[알려진 정답 모의]]
- [[부트스트랩 신뢰구간]]
