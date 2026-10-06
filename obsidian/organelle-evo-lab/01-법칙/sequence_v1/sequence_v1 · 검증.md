---
유형: 검증
법칙: sequence_v1
클러스터: 서열·조성
판정: 양성
tags:
  - 법칙/sequence_v1
  - 클러스터/서열·조성
  - 판정/양성
  - 유형/검증
---

# sequence_v1 · 검증

← [[sequence_v1]]

> [!warning] 이 프로젝트의 규칙
> 새 수치는 언제나 기준선(암기·희귀도·평균값)과 나란히 둡니다. 기준선을 못 넘으면 음성 결과로 기록합니다.

| 항목 | 값 | 95% 구간 |
| --- | --- | --- |
| temperature · n | 86 | — |
| temperature · spearman_ivywrel | 0.6503 | — |
| temperature · pearson_ivywrel | 0.8498 | — |
| temperature · ogt_per_0.01_ivywrel | 7.342 | — |
| temperature · spearman_cvp | 0.6258 | — |
| temperature · rmse_mean_only | 17.96 | — |
| temperature · rmse_ivywrel_loo_group | 10.32 | — |
| temperature · rmse_20aa_ridge_loo_group | 11.29 | — |
| salt · spearman_acidic_excess | 0.5629 | — |
| salt · spearman_median_pi | -0.5105 | — |
| salt · halophiles_ge_15pct · Haloarcula marismortui · acidic_excess | 0.08485 | — |
| salt · halophiles_ge_15pct · Haloarcula marismortui · median_pi | 4.207 | — |
| salt · halophiles_ge_15pct · Halobacterium salinarum · acidic_excess | 0.07867 | — |
| salt · halophiles_ge_15pct · Halobacterium salinarum · median_pi | 4.269 | — |
| salt · halophiles_ge_15pct · Haloferax volcanii · acidic_excess | 0.07927 | — |
| salt · halophiles_ge_15pct · Haloferax volcanii · median_pi | 4.273 | — |
| salt · halophiles_ge_15pct · Haloquadratum walsbyi · acidic_excess | 0.07083 | — |
| salt · halophiles_ge_15pct · Haloquadratum walsbyi · median_pi | 4.339 | — |
| salt · halophiles_ge_15pct · Halothece sp. PCC 7418 · acidic_excess | 0.02587 | — |
| salt · halophiles_ge_15pct · Halothece sp. PCC 7418 · median_pi | 5.402 | — |
| salt · halophiles_ge_15pct · Natronomonas pharaonis · acidic_excess | 0.0937 | — |
| salt · halophiles_ge_15pct · Natronomonas pharaonis · median_pi | 4.191 | — |
| salt · halophiles_ge_15pct · Salinibacter ruber · acidic_excess | 0.0452 | — |
| salt · halophiles_ge_15pct · Salinibacter ruber · median_pi | 4.714 | — |
| salt · others_median_pi | 6.648 | — |
| environment_pairs · n_pairs | 57 | — |
| environment_pairs · by_statistic · ivywrel · loo_r2_environment | 0.5687 | — |
| environment_pairs · by_statistic · ivywrel · coef · base | 0.003999 | — |
| environment_pairs · by_statistic · ivywrel · coef · colder | -0.02658 | — |
| environment_pairs · by_statistic · ivywrel · coef · saltier | -0.006246 | — |
| environment_pairs · by_statistic · ivywrel · coef · anaerobic | -0.0006572 | — |
| environment_pairs · by_statistic · ivywrel · coef · radiation_resistant | -0.01563 | — |
| environment_pairs · by_statistic · ivywrel · coef · oligotrophic | -0.002748 | — |
| environment_pairs · by_statistic · cvp · loo_r2_environment | 0.6065 | — |
| environment_pairs · by_statistic · cvp · coef · base | 0.001954 | — |
| environment_pairs · by_statistic · cvp · coef · colder | -0.04144 | — |
| environment_pairs · by_statistic · cvp · coef · saltier | 0.003255 | — |
| environment_pairs · by_statistic · cvp · coef · anaerobic | -0.01579 | — |
| environment_pairs · by_statistic · cvp · coef · radiation_resistant | -0.02559 | — |
| environment_pairs · by_statistic · cvp · coef · oligotrophic | 0.01089 | — |
| environment_pairs · by_statistic · acidic_excess · loo_r2_environment | 0.5389 | — |
| environment_pairs · by_statistic · acidic_excess · coef · base | -0.0004035 | — |
| environment_pairs · by_statistic · acidic_excess · coef · colder | 0.004967 | — |
| environment_pairs · by_statistic · acidic_excess · coef · saltier | 0.01845 | — |
| environment_pairs · by_statistic · acidic_excess · coef · anaerobic | -0.01116 | — |
| environment_pairs · by_statistic · acidic_excess · coef · radiation_resistant | -0.001473 | — |
| environment_pairs · by_statistic · acidic_excess · coef · oligotrophic | -0.01174 | — |
| environment_pairs · by_statistic · median_pi · loo_r2_environment | 0.236 | — |
| environment_pairs · by_statistic · median_pi · coef · base | 0.03798 | — |
| environment_pairs · by_statistic · median_pi · coef · colder | -0.4367 | — |
| environment_pairs · by_statistic · median_pi · coef · saltier | -0.7304 | — |
| environment_pairs · by_statistic · median_pi · coef · anaerobic | 0.1542 | — |
| environment_pairs · by_statistic · median_pi · coef · radiation_resistant | 0.08073 | — |
| environment_pairs · by_statistic · median_pi · coef · oligotrophic | 0.854 | — |
| environment_pairs · by_statistic · share_pi_below_5 · loo_r2_environment | 0.644 | — |
| environment_pairs · by_statistic · share_pi_below_5 · coef · base | -0.003563 | — |
| environment_pairs · by_statistic · share_pi_below_5 · coef · colder | 0.07196 | — |
| environment_pairs · by_statistic · share_pi_below_5 · coef · saltier | 0.1805 | — |
| environment_pairs · by_statistic · share_pi_below_5 · coef · anaerobic | -0.06102 | — |
| environment_pairs · by_statistic · share_pi_below_5 · coef · radiation_resistant | -0.02452 | — |
| environment_pairs · by_statistic · share_pi_below_5 · coef · oligotrophic | -0.08218 | — |
| environment_pairs · by_statistic · n_side · loo_r2_environment | 0.3891 | — |
| environment_pairs · by_statistic · n_side · coef · base | 0.0001803 | — |
| environment_pairs · by_statistic · n_side · coef · colder | -0.01816 | — |
| environment_pairs · by_statistic · n_side · coef · saltier | -0.006009 | — |
| environment_pairs · by_statistic · n_side · coef · anaerobic | -0.008039 | — |
| environment_pairs · by_statistic · n_side · coef · radiation_resistant | 0.009483 | — |
| environment_pairs · by_statistic · n_side · coef · oligotrophic | -0.01429 | — |
| environment_pairs · by_statistic · c_side · loo_r2_environment | 0.4898 | — |
| environment_pairs · by_statistic · c_side · coef · base | 0.02019 | — |
| environment_pairs · by_statistic · c_side · coef · colder | -0.05114 | — |
| environment_pairs · by_statistic · c_side · coef · saltier | -0.06773 | — |
| environment_pairs · by_statistic · c_side · coef · anaerobic | 0.06889 | — |
| environment_pairs · by_statistic · c_side · coef · radiation_resistant | -0.08405 | — |
| environment_pairs · by_statistic · c_side · coef · oligotrophic | 0.1124 | — |
| environment_pairs · by_statistic · gravy · loo_r2_environment | 0.1062 | — |
| environment_pairs · by_statistic · gravy · coef · base | 0.0129 | — |
| environment_pairs · by_statistic · gravy · coef · colder | -0.006195 | — |
| environment_pairs · by_statistic · gravy · coef · saltier | -0.03225 | — |
| environment_pairs · by_statistic · gravy · coef · anaerobic | 0.0005926 | — |
| environment_pairs · by_statistic · gravy · coef · radiation_resistant | -0.0005786 | — |
| environment_pairs · by_statistic · gravy · coef · oligotrophic | -0.0797 | — |
| environment_pairs · by_statistic · fymink · loo_r2_environment | 0.3897 | — |
| environment_pairs · by_statistic · fymink · coef · base | 0.007312 | — |
| environment_pairs · by_statistic · fymink · coef · colder | 0.01286 | — |
| environment_pairs · by_statistic · fymink · coef · saltier | -0.02362 | — |
| environment_pairs · by_statistic · fymink · coef · anaerobic | 0.0515 | — |
| environment_pairs · by_statistic · fymink · coef · radiation_resistant | -0.02697 | — |
| environment_pairs · by_statistic · fymink · coef · oligotrophic | 0.07279 | — |
| environment_pairs · by_statistic · garp · loo_r2_environment | 0.3504 | — |
| environment_pairs · by_statistic · garp · coef · base | -0.006567 | — |
| environment_pairs · by_statistic · garp · coef · colder | -0.01816 | — |
| environment_pairs · by_statistic · garp · coef · saltier | 0.01048 | — |
| environment_pairs · by_statistic · garp · coef · anaerobic | -0.03889 | — |
| environment_pairs · by_statistic · garp · coef · radiation_resistant | 0.02111 | — |
| environment_pairs · by_statistic · garp · coef · oligotrophic | -0.05847 | — |
| environment_pairs · by_statistic · aromatic · loo_r2_environment | 0.3727 | — |
| environment_pairs · by_statistic · aromatic · coef · base | -0.0002707 | — |
| environment_pairs · by_statistic · aromatic · coef · colder | -0.002537 | — |
| environment_pairs · by_statistic · aromatic · coef · saltier | -0.004586 | — |
| environment_pairs · by_statistic · aromatic · coef · anaerobic | 0.007602 | — |
| environment_pairs · by_statistic · aromatic · coef · radiation_resistant | -0.004344 | — |
| environment_pairs · by_statistic · aromatic · coef · oligotrophic | 0.009162 | — |
| environment_pairs · by_statistic · cysteine · loo_r2_environment | 0.5314 | — |
| environment_pairs · by_statistic · cysteine · coef · base | -0.0003415 | — |
| environment_pairs · by_statistic · cysteine · coef · colder | 0.000423 | — |
| environment_pairs · by_statistic · cysteine · coef · saltier | -0.0006613 | — |
| environment_pairs · by_statistic · cysteine · coef · anaerobic | 0.003344 | — |
| environment_pairs · by_statistic · cysteine · coef · radiation_resistant | 0.001355 | — |
| environment_pairs · by_statistic · cysteine · coef · oligotrophic | 0.0009151 | — |
| environment_pairs · by_statistic · mean_length · loo_r2_environment | -0.1879 | — |
| environment_pairs · by_statistic · mean_length · coef · base | -0.8335 | — |
| environment_pairs · by_statistic · mean_length · coef · colder | 0.8309 | — |
| environment_pairs · by_statistic · mean_length · coef · saltier | -6.973 | — |
| environment_pairs · by_statistic · mean_length · coef · anaerobic | -8.116 | — |
| environment_pairs · by_statistic · mean_length · coef · radiation_resistant | 1.473 | — |
| environment_pairs · by_statistic · mean_length · coef · oligotrophic | -5.12 | — |
| endosymbionts · spearman_size_fymink | -0.7962 | — |
| endosymbionts · spearman_size_pi | -0.8277 | — |
| endosymbionts · table · Arsenophonus nasoniae · n_proteins | 4221 | — |
| endosymbionts · table · Arsenophonus nasoniae · fymink | 0.2936 | — |
| endosymbionts · table · Arsenophonus nasoniae · median_pi | 8.466 | — |
| endosymbionts · table · Arsenophonus nasoniae · n_side | 0.3724 | — |
| endosymbionts · table · Buchnera aphidicola (Cinara tujafilina) · n_proteins | 359 | — |
| endosymbionts · table · Buchnera aphidicola (Cinara tujafilina) · fymink | 0.4292 | — |
| endosymbionts · table · Buchnera aphidicola (Cinara tujafilina) · median_pi | 10.21 | — |
| endosymbionts · table · Buchnera aphidicola (Cinara tujafilina) · n_side | 0.3757 | — |
| endosymbionts · table · Buchnera aphidicola (Myzus persicae) · n_proteins | 578 | — |
| endosymbionts · table · Buchnera aphidicola (Myzus persicae) · fymink | 0.3991 | — |
| endosymbionts · table · Buchnera aphidicola (Myzus persicae) · median_pi | 9.884 | — |
| endosymbionts · table · Buchnera aphidicola (Myzus persicae) · n_side | 0.3667 | — |
| endosymbionts · table · Buchnera aphidicola (Schizaphis graminum) · n_proteins | 567 | — |
| endosymbionts · table · Buchnera aphidicola (Schizaphis graminum) · fymink | 0.4065 | — |
| endosymbionts · table · Buchnera aphidicola (Schizaphis graminum) · median_pi | 9.992 | — |
| endosymbionts · table · Buchnera aphidicola (Schizaphis graminum) · n_side | 0.3672 | — |
| endosymbionts · table · Buchnera aphidicola (Uroleucon sonchi) · n_proteins | 538 | — |
| endosymbionts · table · Buchnera aphidicola (Uroleucon sonchi) · fymink | 0.4081 | — |
| endosymbionts · table · Buchnera aphidicola (Uroleucon sonchi) · median_pi | 9.837 | — |
| endosymbionts · table · Buchnera aphidicola (Uroleucon sonchi) · n_side | 0.3715 | — |
| endosymbionts · table · Buchnera aphidicola BCc · n_proteins | 364 | — |
| endosymbionts · table · Buchnera aphidicola BCc · fymink | 0.4732 | — |
| endosymbionts · table · Buchnera aphidicola BCc · median_pi | 10.5 | — |
| endosymbionts · table · Buchnera aphidicola BCc · n_side | 0.3849 | — |
| endosymbionts · table · Buchnera aphidicola str. APS (Acyrthosiphon pisum) · n_proteins | 569 | — |
| endosymbionts · table · Buchnera aphidicola str. APS (Acyrthosiphon pisum) · fymink | 0.3949 | — |
| endosymbionts · table · Buchnera aphidicola str. APS (Acyrthosiphon pisum) · median_pi | 9.885 | — |
| endosymbionts · table · Buchnera aphidicola str. APS (Acyrthosiphon pisum) · n_side | 0.3675 | — |
| endosymbionts · table · Buchnera aphidicola str. Bp (Baizongia pistaciae) · n_proteins | 504 | — |
| endosymbionts · table · Buchnera aphidicola str. Bp (Baizongia pistaciae) · fymink | 0.3996 | — |
| endosymbionts · table · Buchnera aphidicola str. Bp (Baizongia pistaciae) · median_pi | 9.99 | — |
| endosymbionts · table · Buchnera aphidicola str. Bp (Baizongia pistaciae) · n_side | 0.368 | — |
| endosymbionts · table · Candidatus Annandia pinicola · n_proteins | 315 | — |
| endosymbionts · table · Candidatus Annandia pinicola · fymink | 0.5101 | — |
| endosymbionts · table · Candidatus Annandia pinicola · median_pi | 10.39 | — |
| endosymbionts · table · Candidatus Annandia pinicola · n_side | 0.3748 | — |
| endosymbionts · table · Candidatus Blochmanniella floridana · n_proteins | 583 | — |
| endosymbionts · table · Candidatus Blochmanniella floridana · fymink | 0.3666 | — |
| endosymbionts · table · Candidatus Blochmanniella floridana · median_pi | 9.171 | — |
| endosymbionts · table · Candidatus Blochmanniella floridana · n_side | 0.364 | — |
| endosymbionts · table · Candidatus Blochmanniella pennsylvanica · n_proteins | 574 | — |
| endosymbionts · table · Candidatus Blochmanniella pennsylvanica · fymink | 0.3405 | — |
| endosymbionts · table · Candidatus Blochmanniella pennsylvanica · median_pi | 9.086 | — |
| endosymbionts · table · Candidatus Blochmanniella pennsylvanica · n_side | 0.3724 | — |
| endosymbionts · table · Candidatus Blochmanniella vafra str. BVAF · n_proteins | 587 | — |
| endosymbionts · table · Candidatus Blochmanniella vafra str. BVAF · fymink | 0.3694 | — |
| endosymbionts · table · Candidatus Blochmanniella vafra str. BVAF · median_pi | 9.404 | — |
| endosymbionts · table · Candidatus Blochmanniella vafra str. BVAF · n_side | 0.3647 | — |
| endosymbionts · table · Candidatus Carsonella ruddii · n_proteins | 207 | — |
| endosymbionts · table · Candidatus Carsonella ruddii · fymink | 0.5692 | — |
| endosymbionts · table · Candidatus Carsonella ruddii · median_pi | 10.47 | — |
| endosymbionts · table · Candidatus Carsonella ruddii · n_side | 0.3589 | — |
| endosymbionts · table · Candidatus Hamiltonella defensa (Bemisia tabaci) · n_proteins | 1542 | — |
| endosymbionts · table · Candidatus Hamiltonella defensa (Bemisia tabaci) · fymink | 0.2866 | — |
| endosymbionts · table · Candidatus Hamiltonella defensa (Bemisia tabaci) · median_pi | 8.533 | — |
| endosymbionts · table · Candidatus Hamiltonella defensa (Bemisia tabaci) · n_side | 0.3717 | — |
| endosymbionts · table · Candidatus Ishikawaella capsulata Mpkobe · n_proteins | 597 | — |
| endosymbionts · table · Candidatus Ishikawaella capsulata Mpkobe · fymink | 0.3462 | — |
| endosymbionts · table · Candidatus Ishikawaella capsulata Mpkobe · median_pi | 9.002 | — |
| endosymbionts · table · Candidatus Ishikawaella capsulata Mpkobe · n_side | 0.3663 | — |
| endosymbionts · table · Candidatus Moranella endobia PCIT · n_proteins | 406 | — |
| endosymbionts · table · Candidatus Moranella endobia PCIT · fymink | 0.262 | — |
| endosymbionts · table · Candidatus Moranella endobia PCIT · median_pi | 7.889 | — |
| endosymbionts · table · Candidatus Moranella endobia PCIT · n_side | 0.3782 | — |
| endosymbionts · table · Candidatus Palibaumannia cicadellinicola · n_proteins | 655 | — |
| endosymbionts · table · Candidatus Palibaumannia cicadellinicola · fymink | 0.2787 | — |
| endosymbionts · table · Candidatus Palibaumannia cicadellinicola · median_pi | 8.315 | — |
| endosymbionts · table · Candidatus Palibaumannia cicadellinicola · n_side | 0.3745 | — |
| endosymbionts · table · Candidatus Portiera aleyrodidarum · n_proteins | 245 | — |
| endosymbionts · table · Candidatus Portiera aleyrodidarum · fymink | 0.4196 | — |
| endosymbionts · table · Candidatus Portiera aleyrodidarum · median_pi | 10.25 | — |
| endosymbionts · table · Candidatus Portiera aleyrodidarum · n_side | 0.3741 | — |
| endosymbionts · table · Candidatus Purcelliella pentastirinorum · n_proteins | 437 | — |
| endosymbionts · table · Candidatus Purcelliella pentastirinorum · fymink | 0.4631 | — |
| endosymbionts · table · Candidatus Purcelliella pentastirinorum · median_pi | 10.23 | — |
| endosymbionts · table · Candidatus Purcelliella pentastirinorum · n_side | 0.371 | — |
| endosymbionts · table · Candidatus Riesia pediculicola · n_proteins | 463 | — |
| endosymbionts · table · Candidatus Riesia pediculicola · fymink | 0.3931 | — |
| endosymbionts · table · Candidatus Riesia pediculicola · median_pi | 10.13 | — |
| endosymbionts · table · Candidatus Riesia pediculicola · n_side | 0.3914 | — |
| endosymbionts · table · Candidatus Riesia pediculischaeffi · n_proteins | 441 | — |
| endosymbionts · table · Candidatus Riesia pediculischaeffi · fymink | 0.3775 | — |
| endosymbionts · table · Candidatus Riesia pediculischaeffi · median_pi | 9.93 | — |
| endosymbionts · table · Candidatus Riesia pediculischaeffi · n_side | 0.3957 | — |
| endosymbionts · table · Candidatus Westeberhardia cardiocondylae · n_proteins | 372 | — |
| endosymbionts · table · Candidatus Westeberhardia cardiocondylae · fymink | 0.4154 | — |
| endosymbionts · table · Candidatus Westeberhardia cardiocondylae · median_pi | 10.11 | — |
| endosymbionts · table · Candidatus Westeberhardia cardiocondylae · n_side | 0.3775 | — |
| endosymbionts · table · Escherichia coli str. K-12 substr. MG1655 · n_proteins | 4210 | — |
| endosymbionts · table · Escherichia coli str. K-12 substr. MG1655 · fymink | 0.2386 | — |
| endosymbionts · table · Escherichia coli str. K-12 substr. MG1655 · median_pi | 6.629 | — |
| endosymbionts · table · Escherichia coli str. K-12 substr. MG1655 · n_side | 0.3541 | — |
| endosymbionts · table · Serratia symbiotica · n_proteins | 2848 | — |
| endosymbionts · table · Serratia symbiotica · fymink | 0.2319 | — |
| endosymbionts · table · Serratia symbiotica · median_pi | 7.302 | — |
| endosymbionts · table · Serratia symbiotica · n_side | 0.372 | — |
| endosymbionts · table · Sodalis glossinidius str. 'morsitans' · n_proteins | 2432 | — |
| endosymbionts · table · Sodalis glossinidius str. 'morsitans' · fymink | 0.2204 | — |
| endosymbionts · table · Sodalis glossinidius str. 'morsitans' · median_pi | 7.096 | — |
| endosymbionts · table · Sodalis glossinidius str. 'morsitans' · n_side | 0.378 | — |
| endosymbionts · table · Wigglesworthia glossinidia endosymbiont of Glossina morsitans morsitans (Yale colony) · n_proteins | 618 | — |
| endosymbionts · table · Wigglesworthia glossinidia endosymbiont of Glossina morsitans morsitans (Yale colony) · fymink | 0.4145 | — |
| endosymbionts · table · Wigglesworthia glossinidia endosymbiont of Glossina morsitans morsitans (Yale colony) · median_pi | 10.09 | — |
| endosymbionts · table · Wigglesworthia glossinidia endosymbiont of Glossina morsitans morsitans (Yale colony) · n_side | 0.3716 | — |
| eukaryote_pairs · n_pairs | 99 | — |
| eukaryote_pairs · by_statistic · fymink · loo_clade_r2 | 0.06772 | — |
| eukaryote_pairs · by_statistic · fymink · coef · base | -0.003054 | — |
| eukaryote_pairs · by_statistic · fymink · coef · parasite | 0.0008899 | — |
| eukaryote_pairs · by_statistic · fymink · coef · intracellular | 0.07268 | — |
| eukaryote_pairs · by_statistic · fymink · coef · reduced_mitochondria | 0.04813 | — |
| eukaryote_pairs · by_statistic · median_pi · loo_clade_r2 | -0.01045 | — |
| eukaryote_pairs · by_statistic · median_pi · coef · base | 0.02194 | — |
| eukaryote_pairs · by_statistic · median_pi · coef · parasite | 0.1669 | — |
| eukaryote_pairs · by_statistic · median_pi · coef · intracellular | 0.5206 | — |
| eukaryote_pairs · by_statistic · median_pi · coef · reduced_mitochondria | 0.1158 | — |
| eukaryote_pairs · by_statistic · n_side · loo_clade_r2 | -0.1289 | — |
| eukaryote_pairs · by_statistic · n_side · coef · base | 0.00247 | — |
| eukaryote_pairs · by_statistic · n_side · coef · parasite | -0.0005728 | — |
| eukaryote_pairs · by_statistic · n_side · coef · intracellular | 0.00131 | — |
| eukaryote_pairs · by_statistic · n_side · coef · reduced_mitochondria | -0.01324 | — |
| eukaryote_pairs · by_statistic · ivywrel · loo_clade_r2 | -0.03574 | — |
| eukaryote_pairs · by_statistic · ivywrel · coef · base | 0.008709 | — |
| eukaryote_pairs · by_statistic · ivywrel · coef · parasite | -0.003323 | — |
| eukaryote_pairs · by_statistic · ivywrel · coef · intracellular | -0.0009571 | — |
| eukaryote_pairs · by_statistic · ivywrel · coef · reduced_mitochondria | 0.02176 | — |
| eukaryote_pairs · by_statistic · mean_length · loo_clade_r2 | -0.2135 | — |
| eukaryote_pairs · by_statistic · mean_length · coef · base | -47.89 | — |
| eukaryote_pairs · by_statistic · mean_length · coef · parasite | 43.24 | — |
| eukaryote_pairs · by_statistic · mean_length · coef · intracellular | 33.5 | — |
| eukaryote_pairs · by_statistic · mean_length · coef · reduced_mitochondria | -157.9 | — |

## 방법
- [[잎 숨기기 검증]]
- [[알려진 정답 모의]]
- [[부트스트랩 신뢰구간]]
