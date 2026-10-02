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
- n_pairs: 57
- ivywrel:
  - axis: colder
  - uniform_share_of_family_variance: 0.243
  - families_tested: 2099
  - median_sensitivity: 0.024
  - share_positive: 0.906
  - most_sensitive: `[["LpqE-like: Putative lipoprotein LpqE-like", 0.1356], ["UVR: UvrB/uvrC motif", 0.108], ["FtsX_ECD: FtsX extracellular domain", 0.1016], ["Smr: Smr domain", 0.`
  - least_sensitive: `[["UPF0093: Protoporphyrinogen oxidase HemJ", -0.0464], ["MAPEG: MAPEG family", -0.0469], ["GST_C_3: Glutathione S-transferase, C-terminal domain", -0.0482], ["`
  - feature_correlations: `[["hydrophobicity_gravy", -0.16312864689105405], ["tm_helices", -0.12985374798727495], ["kw:transporter_channel", -0.11448278597817009], ["go:transporter activi`
- acidic_excess:
  - axis: saltier
  - uniform_share_of_family_variance: 0.309
  - families_tested: 2099
  - median_sensitivity: 0.019
  - share_positive: 0.892
  - most_sensitive: `[["Sortase: Sortase domain", 0.1312], ["Lipoprotein_9: NlpA lipoprotein", 0.1297], ["Ribosomal_L26: Ribosomal proteins L26 eukaryotic, L24P archaeal", 0.1151], `
  - least_sensitive: `[["PolyA_pol_arg_C: Polymerase A arginine-rich C-terminus", -0.0427], ["HTH_AsnC-type: AsnC-type helix-turn-helix domain", -0.0428], ["PNK3P: Polynucleotide kin`
  - feature_correlations: `[["tm_helices", -0.184424926806161], ["hydrophobicity_gravy", -0.1711561564727651], ["translation", 0.13298573931332688], ["ubiquity_free_living", 0.13013996963`

## 한계
- Composition is over Pfam domain regions only.
- Families need >= 12 pairs.

원본: `laws/family_sequence_v1.json`