---
id: mito_ancestor_v1
system: 공생 → 소기관
status: 현역
tags:
  - 법칙
  - 공생소기관
---
# mito_ancestor_v1

> 미토콘드리아 조상 복원: 알파프로테오박테리아 공통 조상은 약 4,100개 유전자군(확실 1,798)을 가진 호기성·저산소 호흡 가능, 편모로 헤엄치는 세균. 모형 선택에 따라 크기가 1,900–4,100개로 달라지고, 축소된 공생 계통이 조상을 작아 보이게 끌어당긴다.

**시스템**: 공생 → 소기관  
**상태**: 현역  
**주제**: [[조상 역추적]]

## 적용 범위 (원문)
Gene-family (Pfam) content of the alphaproteobacterial ancestors from which mitochondria are thought to descend, reconstructed on the GTDB tree from UniProt reference proteomes. Candidate ancestors: the alphaproteobacterial common ancestor and deep orders (Rickettsiales, Holosporales, Pelagibacterales). Family presence only; no sequences.

## 모델
Two-state gain/loss Markov chain per Pfam family on the pruned GTDB bac120 tree, rates by grid maximum likelihood, marginal posteriors by the up-down algorithm. Variants: symmetric vs loss-biased (gain <= 0.1 x loss, flat root prior) x all proteomes vs BUSCO >= 90%.

## 검증
- loss_biased_busco0:
  - tips: 2623
  - leave_tips_out_auroc: `{"reconstruction": 0.9846, "alpha_frequency": 0.9624, "nearest_tip": 0.9777}`
  - nodes: `{"Alphaproteobacteria (common ancestor)": {"n_tips_below": 2323, "expected_families": 3945.1, "families_p_ge_0.9": 1710, "families_p_0.5_0.9": 1575, "positive_c`
- loss_biased_busco90:
  - tips: 2526
  - leave_tips_out_auroc: `{"reconstruction": 0.9849, "alpha_frequency": 0.9627, "nearest_tip": 0.9792}`
  - nodes: `{"Alphaproteobacteria (common ancestor)": {"n_tips_below": 2226, "expected_families": 4122.2, "families_p_ge_0.9": 1798, "families_p_0.5_0.9": 1632, "positive_c`
- symmetric_busco0:
  - tips: 2623
  - leave_tips_out_auroc: `{"reconstruction": 0.9847, "alpha_frequency": 0.9624, "nearest_tip": 0.9777}`
  - nodes: `{"Alphaproteobacteria (common ancestor)": {"n_tips_below": 2323, "expected_families": 1938.5, "families_p_ge_0.9": 772, "families_p_0.5_0.9": 683, "positive_con`
- symmetric_busco90:
  - tips: 2526
  - leave_tips_out_auroc: `{"reconstruction": 0.9852, "alpha_frequency": 0.9627, "nearest_tip": 0.9792}`
  - nodes: `{"Alphaproteobacteria (common ancestor)": {"n_tips_below": 2226, "expected_families": 2288.1, "families_p_ge_0.9": 1044, "families_p_0.5_0.9": 871, "positive_co`

## 한계
- The preferred variant is loss_biased_busco90: the only one with all 25 Reclinomonas core-gene families present at the alphaproteobacterial root. The symmetric model on all proteomes gave an ancestor without the TCA cycle or fatty-acid synthesis, because reduced or incomplete basal lineages (a long-branch MAG, endosymbiont-like MAGs, Holosporales) make one gain cheaper than several losses.
- Ancestor size depends on the model and data choices: about 1,900 to 4,100 expected families at the alphaproteobacterial root. Report the range, not one number.
- Leave-tips-out accuracy is the same (0.985) for every variant, so it cannot choose between them: it tests recent tips, not deep nodes. The positive control and agreement with the literature are the deep-node checks.
- Where mitochondria branch (inside Alphaproteobacteria or as their sister) is disputed; the deep orders closest to mitochondria are poorly sampled here (Rickettsiales 40-53, Holosporales 4, Pelagibacterales 3).
- Positive-control families are universal bacterial genes: necessary, not discriminating.
- Horizontal gene transfer is not modelled; families moved between lineages can look ancestral.

원본: `laws/mito_ancestor_v1.json`