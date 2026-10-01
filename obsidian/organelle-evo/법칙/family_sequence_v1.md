---
id: family_sequence_v1
system: 보통 → 극한 환경
status: 현역
tags:
  - 법칙
  - 극한환경
---
# family_sequence_v1

> 유전자군 단위 서열 적응: 온도·염분 적응 때 유전자군의 90%가 같은 방향으로 바뀐다(단백질 전체 적응). 막·수송 단백질은 덜 바뀌고, 흔한 핵심 세포질 단백질(번역 등)은 염분에 더 많이 산성화된다.

**시스템**: 보통 → 극한 환경  
**상태**: 현역  
**주제**: [[환경과 서열]]

## 적용 범위 (원문)
Which protein families carry temperature (IVYWREL) and salt (acidic excess) adaptation in bacteria and archaea.

## 모델
Per-family change in domain composition across relative -> extremophile pairs, regressed on the environment change.

## 검증
- n_pairs: 43
- ivywrel:
  - axis: colder
  - uniform_share_of_family_variance: 0.24
  - families_tested: 1797
  - median_sensitivity: 0.028
  - share_positive: 0.9
  - most_sensitive: `[["LpqE-like: Putative lipoprotein LpqE-like", 0.1337], ["DciA: Dna[CI] antecedent, DciA", 0.1271], ["SpoIID: Stage II sporulation protein", 0.1179], ["PspA_IM3`
  - least_sensitive: `[["RDD: RDD family", -0.048], ["Sigma70_r1_1: Sigma-70 factor, region 1.1", -0.0482], ["TetR_C_13: Tetracyclin repressor-like, C-terminal domain", -0.0602], ["A`
  - feature_correlations: `[["hydrophobicity_gravy", -0.1650210988021524], ["tm_helices", -0.11248096099097678], ["kw:transporter_channel", -0.1012335374791002], ["go:transmembrane transp`
- acidic_excess:
  - axis: saltier
  - uniform_share_of_family_variance: 0.354
  - families_tested: 1797
  - median_sensitivity: 0.022
  - share_positive: 0.903
  - most_sensitive: `[["SbcC_Walker_B: SbcC/RAD50-like, Walker B motif", 0.3626], ["Lipoprotein_9: NlpA lipoprotein", 0.154], ["Sortase: Sortase domain", 0.1312], ["PBP5_C: Penicill`
  - least_sensitive: `[["CobU: Cobinamide kinase / cobinamide phosphate guanyltransferase", -0.0451], ["HTH_17: Helix-turn-helix domain", -0.0458], ["HTH_AsnC-type: AsnC-type helix-t`
  - feature_correlations: `[["ubiquity_free_living", 0.2540366754428382], ["tm_helices", -0.18186385354470141], ["hydrophobicity_gravy", -0.1774686130805182], ["kw:transporter_channel", -`

## 한계
- Composition is over Pfam domain regions only.
- Families need >= 12 pairs.

원본: `laws/family_sequence_v1.json`