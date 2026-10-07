---
유형: 검증
법칙: anaerobic_transition_v1
클러스터: 전환 경로
판정: 양성
tags:
  - 법칙/anaerobic_transition_v1
  - 클러스터/전환 경로
  - 판정/양성
  - 유형/검증
---

# anaerobic_transition_v1 · 검증

← [[anaerobic_transition_v1]]

> [!warning] 이 프로젝트의 규칙
> 새 수치는 언제나 기준선(암기·희귀도·평균값)과 나란히 둡니다. 기준선을 못 넘으면 음성 결과로 기록합니다.

| 항목 | 값 | 95% 구간 |
| --- | --- | --- |
| law_plus_rarity_minus_control_plus_rarity | 0.0292 | [0.0118, 0.0459] |
| leave_one_origin_out · metric | auroc | — |
| leave_one_origin_out · what | predict which candidate families the held-out origin lost | — |
| leave_one_origin_out · law | 0.7769 | — |
| leave_one_origin_out · parasite_baseline | 0.6839 | — |
| leave_one_origin_out · rarity_baseline | 0.8007 | — |
| per_origin · Metamonada · n_candidates | 4453 | — |
| per_origin · Metamonada · n_changed | 2822 | — |
| per_origin · Metamonada · share_changed | 0.6337 | — |
| per_origin · Metamonada · law | 0.8148 | — |
| per_origin · Metamonada · parasite_baseline | 0.6733 | — |
| per_origin · Metamonada · rarity_baseline | 0.8095 | — |
| per_origin · Metamonada · law+rarity | 0.8403 | — |
| per_origin · Metamonada · combined_minus_rarity | 0.0308 | — |
| per_origin · Metamonada · parasite_baseline+rarity | 0.7734 | — |
| per_origin · Metamonada · law_vs_control_combined | 0.0669 | — |
| per_origin · Archamoebae (Entamoeba) · n_candidates | 4317 | — |
| per_origin · Archamoebae (Entamoeba) · n_changed | 2556 | — |
| per_origin · Archamoebae (Entamoeba) · share_changed | 0.5921 | — |
| per_origin · Archamoebae (Entamoeba) · law | 0.8065 | — |
| per_origin · Archamoebae (Entamoeba) · parasite_baseline | 0.6606 | — |
| per_origin · Archamoebae (Entamoeba) · rarity_baseline | 0.7942 | — |
| per_origin · Archamoebae (Entamoeba) · law+rarity | 0.8332 | — |
| per_origin · Archamoebae (Entamoeba) · combined_minus_rarity | 0.039 | — |
| per_origin · Archamoebae (Entamoeba) · parasite_baseline+rarity | 0.7619 | — |
| per_origin · Archamoebae (Entamoeba) · law_vs_control_combined | 0.0713 | — |
| per_origin · Neocallimastigomycota · n_candidates | 4459 | — |
| per_origin · Neocallimastigomycota · n_changed | 913 | — |
| per_origin · Neocallimastigomycota · share_changed | 0.2048 | — |
| per_origin · Neocallimastigomycota · law | 0.7421 | — |
| per_origin · Neocallimastigomycota · parasite_baseline | 0.6268 | — |
| per_origin · Neocallimastigomycota · rarity_baseline | 0.7058 | — |
| per_origin · Neocallimastigomycota · law+rarity | 0.7482 | — |
| per_origin · Neocallimastigomycota · combined_minus_rarity | 0.0424 | — |
| per_origin · Neocallimastigomycota · parasite_baseline+rarity | 0.6948 | — |
| per_origin · Neocallimastigomycota · law_vs_control_combined | 0.0534 | — |
| per_origin · Microsporidia · n_candidates | 3311 | — |
| per_origin · Microsporidia · n_changed | 2227 | — |
| per_origin · Microsporidia · share_changed | 0.6726 | — |
| per_origin · Microsporidia · law | 0.7868 | — |
| per_origin · Microsporidia · parasite_baseline | 0.7067 | — |
| per_origin · Microsporidia · rarity_baseline | 0.8526 | — |
| per_origin · Microsporidia · law+rarity | 0.855 | — |
| per_origin · Microsporidia · combined_minus_rarity | 0.0024 | — |
| per_origin · Microsporidia · parasite_baseline+rarity | 0.8211 | — |
| per_origin · Microsporidia · law_vs_control_combined | 0.0339 | — |
| per_origin · Cryptosporidium · n_candidates | 2731 | — |
| per_origin · Cryptosporidium · n_changed | 1002 | — |
| per_origin · Cryptosporidium · share_changed | 0.3669 | — |
| per_origin · Cryptosporidium · law | 0.7656 | — |
| per_origin · Cryptosporidium · parasite_baseline | 0.7106 | — |
| per_origin · Cryptosporidium · rarity_baseline | 0.8177 | — |
| per_origin · Cryptosporidium · law+rarity | 0.8323 | — |
| per_origin · Cryptosporidium · combined_minus_rarity | 0.0146 | — |
| per_origin · Cryptosporidium · parasite_baseline+rarity | 0.8059 | — |
| per_origin · Cryptosporidium · law_vs_control_combined | 0.0264 | — |
| per_origin · Blastocystis · n_candidates | 4996 | — |
| per_origin · Blastocystis · n_changed | 2450 | — |
| per_origin · Blastocystis · share_changed | 0.4904 | — |
| per_origin · Blastocystis · law | 0.7458 | — |
| per_origin · Blastocystis · parasite_baseline | 0.7257 | — |
| per_origin · Blastocystis · rarity_baseline | 0.8245 | — |
| per_origin · Blastocystis · law+rarity | 0.8229 | — |
| per_origin · Blastocystis · combined_minus_rarity | -0.0016 | — |
| per_origin · Blastocystis · parasite_baseline+rarity | 0.8134 | — |
| per_origin · Blastocystis · law_vs_control_combined | 0.0095 | — |
| law_alone_minus_best_baseline | -0.0238 | [-0.0574, 0.0101] |
| law_plus_rarity_minus_rarity | 0.0213 | [0.0078, 0.0347] |
| parasitism_matched_origins · Microsporidia · law | 0.7868 | — |
| parasitism_matched_origins · Microsporidia · parasite_baseline | 0.7067 | — |
| parasitism_matched_origins · Microsporidia · rarity_baseline | 0.8526 | — |
| parasitism_matched_origins · Microsporidia · share_lost | 0.6726 | — |
| parasitism_matched_origins · Cryptosporidium · law | 0.7656 | — |
| parasitism_matched_origins · Cryptosporidium · parasite_baseline | 0.7106 | — |
| parasitism_matched_origins · Cryptosporidium · rarity_baseline | 0.8177 | — |
| parasitism_matched_origins · Cryptosporidium · share_lost | 0.3669 | — |
| marker_panel · respiratory chain (expected LOST) · Complex1_51K · share_of_derived_with_it | 0.364 | — |
| marker_panel · respiratory chain (expected LOST) · Complex1_51K · share_of_relatives_with_it | 0.714 | — |
| marker_panel · respiratory chain (expected LOST) · Complex1_51K · changed_in_origins | 0.5 | — |
| marker_panel · respiratory chain (expected LOST) · Complex1_51K · changed_in_controls | 0 | — |
| marker_panel · respiratory chain (expected LOST) · Complex1_30kDa · share_of_derived_with_it | 0.091 | — |
| marker_panel · respiratory chain (expected LOST) · Complex1_30kDa · share_of_relatives_with_it | 0.286 | — |
| marker_panel · respiratory chain (expected LOST) · Complex1_30kDa · changed_in_origins | 1 | — |
| marker_panel · respiratory chain (expected LOST) · Complex1_30kDa · changed_in_controls | None | — |
| marker_panel · respiratory chain (expected LOST) · COX15-CtaA · share_of_derived_with_it | 0 | — |
| marker_panel · respiratory chain (expected LOST) · COX15-CtaA · share_of_relatives_with_it | 1 | — |
| marker_panel · respiratory chain (expected LOST) · COX15-CtaA · changed_in_origins | 1 | — |
| marker_panel · respiratory chain (expected LOST) · COX15-CtaA · changed_in_controls | 0 | — |
| marker_panel · respiratory chain (expected LOST) · COX4 · share_of_derived_with_it | 0 | — |
| marker_panel · respiratory chain (expected LOST) · COX4 · share_of_relatives_with_it | 0.357 | — |
| marker_panel · respiratory chain (expected LOST) · COX4 · changed_in_origins | 1 | — |
| marker_panel · respiratory chain (expected LOST) · COX4 · changed_in_controls | 0 | — |
| marker_panel · respiratory chain (expected LOST) · COX17 · share_of_derived_with_it | 0 | — |
| marker_panel · respiratory chain (expected LOST) · COX17 · share_of_relatives_with_it | 0.714 | — |
| marker_panel · respiratory chain (expected LOST) · COX17 · changed_in_origins | 1 | — |
| marker_panel · respiratory chain (expected LOST) · COX17 · changed_in_controls | 0 | — |
| marker_panel · respiratory chain (expected LOST) · Cytochrom_C1 · share_of_derived_with_it | 0 | — |
| marker_panel · respiratory chain (expected LOST) · Cytochrom_C1 · share_of_relatives_with_it | 1 | — |
| marker_panel · respiratory chain (expected LOST) · Cytochrom_C1 · changed_in_origins | 1 | — |
| marker_panel · respiratory chain (expected LOST) · Cytochrom_C1 · changed_in_controls | 0 | — |
| marker_panel · respiratory chain (expected LOST) · UCR_14kD · share_of_derived_with_it | 0 | — |
| marker_panel · respiratory chain (expected LOST) · UCR_14kD · share_of_relatives_with_it | 0.929 | — |
| marker_panel · respiratory chain (expected LOST) · UCR_14kD · changed_in_origins | 1 | — |
| marker_panel · respiratory chain (expected LOST) · UCR_14kD · changed_in_controls | 0 | — |
| marker_panel · respiratory chain (expected LOST) · UCR_hinge · share_of_derived_with_it | 0 | — |
| marker_panel · respiratory chain (expected LOST) · UCR_hinge · share_of_relatives_with_it | 0.643 | — |
| marker_panel · respiratory chain (expected LOST) · UCR_hinge · changed_in_origins | 1 | — |
| marker_panel · respiratory chain (expected LOST) · UCR_hinge · changed_in_controls | 0 | — |
| marker_panel · respiratory chain (expected LOST) · Rieske · share_of_derived_with_it | 0.045 | — |
| marker_panel · respiratory chain (expected LOST) · Rieske · share_of_relatives_with_it | 1 | — |
| marker_panel · respiratory chain (expected LOST) · Rieske · changed_in_origins | 1 | — |
| marker_panel · respiratory chain (expected LOST) · Rieske · changed_in_controls | 0 | — |
| marker_panel · respiratory chain (expected LOST) · SDH_C · share_of_derived_with_it | 0 | — |
| marker_panel · respiratory chain (expected LOST) · SDH_C · share_of_relatives_with_it | 0.286 | — |
| marker_panel · respiratory chain (expected LOST) · SDH_C · changed_in_origins | 1 | — |
| marker_panel · respiratory chain (expected LOST) · SDH_C · changed_in_controls | 1 | — |
| marker_panel · TCA cycle (expected mostly lost) · Citrate_synt · share_of_derived_with_it | 0.227 | — |
| marker_panel · TCA cycle (expected mostly lost) · Citrate_synt · share_of_relatives_with_it | 1 | — |
| marker_panel · TCA cycle (expected mostly lost) · Citrate_synt · changed_in_origins | 0.667 | — |
| marker_panel · TCA cycle (expected mostly lost) · Citrate_synt · changed_in_controls | 0 | — |
| marker_panel · TCA cycle (expected mostly lost) · SDH_beta · share_of_derived_with_it | 0.455 | — |
| marker_panel · TCA cycle (expected mostly lost) · SDH_beta · share_of_relatives_with_it | 0.286 | — |
| marker_panel · TCA cycle (expected mostly lost) · SDH_beta · changed_in_origins | 0.667 | — |
| marker_panel · TCA cycle (expected mostly lost) · SDH_beta · changed_in_controls | None | — |
| marker_panel · ATP synthase (expected lost in mitosomes) · ATP-synt_D · share_of_derived_with_it | 0.955 | — |
| marker_panel · ATP synthase (expected lost in mitosomes) · ATP-synt_D · share_of_relatives_with_it | 1 | — |
| marker_panel · ATP synthase (expected lost in mitosomes) · ATP-synt_D · changed_in_origins | 0 | — |
| marker_panel · ATP synthase (expected lost in mitosomes) · ATP-synt_D · changed_in_controls | 0 | — |
| marker_panel · ATP synthase (expected lost in mitosomes) · ATP-synt_DE · share_of_derived_with_it | 0.045 | — |
| marker_panel · ATP synthase (expected lost in mitosomes) · ATP-synt_DE · share_of_relatives_with_it | 0 | — |
| marker_panel · ATP synthase (expected lost in mitosomes) · ATP-synt_DE · changed_in_origins | None | — |
| marker_panel · ATP synthase (expected lost in mitosomes) · ATP-synt_DE · changed_in_controls | None | — |
| marker_panel · ATP synthase (expected lost in mitosomes) · ATP-synt_C · share_of_derived_with_it | 1 | — |
| marker_panel · ATP synthase (expected lost in mitosomes) · ATP-synt_C · share_of_relatives_with_it | 1 | — |
| marker_panel · ATP synthase (expected lost in mitosomes) · ATP-synt_C · changed_in_origins | 0 | — |
| marker_panel · ATP synthase (expected lost in mitosomes) · ATP-synt_C · changed_in_controls | 0 | — |
| marker_panel · anaerobic energy metabolism (expected GAINED/kept) · Fe_hyd_lg_C · share_of_derived_with_it | 1 | — |
| marker_panel · anaerobic energy metabolism (expected GAINED/kept) · Fe_hyd_lg_C · share_of_relatives_with_it | 0.857 | — |
| marker_panel · anaerobic energy metabolism (expected GAINED/kept) · Fe_hyd_lg_C · changed_in_origins | 0 | — |
| marker_panel · anaerobic energy metabolism (expected GAINED/kept) · Fe_hyd_lg_C · changed_in_controls | 0 | — |
| marker_panel · anaerobic energy metabolism (expected GAINED/kept) · Fe_hyd_SSU · share_of_derived_with_it | 0.591 | — |
| marker_panel · anaerobic energy metabolism (expected GAINED/kept) · Fe_hyd_SSU · share_of_relatives_with_it | 0.429 | — |
| marker_panel · anaerobic energy metabolism (expected GAINED/kept) · Fe_hyd_SSU · changed_in_origins | 0 | — |
| marker_panel · anaerobic energy metabolism (expected GAINED/kept) · Fe_hyd_SSU · changed_in_controls | 1 | — |
| marker_panel · anaerobic energy metabolism (expected GAINED/kept) · POR_N · share_of_derived_with_it | 0.864 | — |
| marker_panel · anaerobic energy metabolism (expected GAINED/kept) · POR_N · share_of_relatives_with_it | 0.286 | — |
| marker_panel · anaerobic energy metabolism (expected GAINED/kept) · POR_N · changed_in_origins | 0 | — |
| marker_panel · anaerobic energy metabolism (expected GAINED/kept) · POR_N · changed_in_controls | 1 | — |
| marker_panel · anaerobic energy metabolism (expected GAINED/kept) · PFOR_II · share_of_derived_with_it | 0.818 | — |
| marker_panel · anaerobic energy metabolism (expected GAINED/kept) · PFOR_II · share_of_relatives_with_it | 0.286 | — |
| marker_panel · anaerobic energy metabolism (expected GAINED/kept) · PFOR_II · changed_in_origins | 0 | — |
| marker_panel · anaerobic energy metabolism (expected GAINED/kept) · PFOR_II · changed_in_controls | 1 | — |
| marker_panel · anaerobic energy metabolism (expected GAINED/kept) · ADH_Fe_C · share_of_derived_with_it | 0.818 | — |
| marker_panel · anaerobic energy metabolism (expected GAINED/kept) · ADH_Fe_C · share_of_relatives_with_it | 0.643 | — |
| marker_panel · anaerobic energy metabolism (expected GAINED/kept) · ADH_Fe_C · changed_in_origins | 0 | — |
| marker_panel · anaerobic energy metabolism (expected GAINED/kept) · ADH_Fe_C · changed_in_controls | 1 | — |
| marker_panel · anaerobic energy metabolism (expected GAINED/kept) · Rubredoxin · share_of_derived_with_it | 0.045 | — |
| marker_panel · anaerobic energy metabolism (expected GAINED/kept) · Rubredoxin · share_of_relatives_with_it | 0 | — |
| marker_panel · anaerobic energy metabolism (expected GAINED/kept) · Rubredoxin · changed_in_origins | None | — |
| marker_panel · anaerobic energy metabolism (expected GAINED/kept) · Rubredoxin · changed_in_controls | 1 | — |
| marker_panel · anaerobic energy metabolism (expected GAINED/kept) · Hemerythrin · share_of_derived_with_it | 0.273 | — |
| marker_panel · anaerobic energy metabolism (expected GAINED/kept) · Hemerythrin · share_of_relatives_with_it | 0.643 | — |
| marker_panel · anaerobic energy metabolism (expected GAINED/kept) · Hemerythrin · changed_in_origins | 0.5 | — |
| marker_panel · anaerobic energy metabolism (expected GAINED/kept) · Hemerythrin · changed_in_controls | 1 | — |
| marker_panel · Fe-S cluster assembly (expected KEPT: the one job mitosomes still do) · NifU · share_of_derived_with_it | 0.636 | — |
| marker_panel · Fe-S cluster assembly (expected KEPT: the one job mitosomes still do) · NifU · share_of_relatives_with_it | 0.857 | — |
| marker_panel · Fe-S cluster assembly (expected KEPT: the one job mitosomes still do) · NifU · changed_in_origins | 0.333 | — |
| marker_panel · Fe-S cluster assembly (expected KEPT: the one job mitosomes still do) · NifU · changed_in_controls | 0 | — |
| marker_panel · Fe-S cluster assembly (expected KEPT: the one job mitosomes still do) · NifU_N · share_of_derived_with_it | 1 | — |
| marker_panel · Fe-S cluster assembly (expected KEPT: the one job mitosomes still do) · NifU_N · share_of_relatives_with_it | 0.929 | — |
| marker_panel · Fe-S cluster assembly (expected KEPT: the one job mitosomes still do) · NifU_N · changed_in_origins | 0 | — |
| marker_panel · Fe-S cluster assembly (expected KEPT: the one job mitosomes still do) · NifU_N · changed_in_controls | 0 | — |
| marker_panel · Fe-S cluster assembly (expected KEPT: the one job mitosomes still do) · Frataxin_Cyay · share_of_derived_with_it | 0.591 | — |
| marker_panel · Fe-S cluster assembly (expected KEPT: the one job mitosomes still do) · Frataxin_Cyay · share_of_relatives_with_it | 0.929 | — |
| marker_panel · Fe-S cluster assembly (expected KEPT: the one job mitosomes still do) · Frataxin_Cyay · changed_in_origins | 0.167 | — |
| marker_panel · Fe-S cluster assembly (expected KEPT: the one job mitosomes still do) · Frataxin_Cyay · changed_in_controls | 0.333 | — |

## 방법
- [[잎 숨기기 검증]]
- [[알려진 정답 모의]]
- [[부트스트랩 신뢰구간]]
