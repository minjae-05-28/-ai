---
id: human_cell_v1
system: 보통 → 극한 환경
status: 현역
tags:
  - 법칙
  - 극한환경
---
# human_cell_v1

> 사람 몸(장·피부·혈액)에 맞춘 세포를 법칙으로 예측하고 실제 공생균 10종과 맞춰 봄(역예측 검증). 조성 오차 작음(장 IVYWREL 0.011), 유전자 수 2,324 vs 자유생활 3,215. 유전자 구성은 법칙 0.86이 희귀도 기준선 0.93에 짐.

**시스템**: 보통 → 극한 환경  
**상태**: 현역  
**주제**: [[사람 몸 세포]]

## 적용 범위 (원문)
What the laws predict for a cell living in the human body, tested against real human commensals.

## 모델
Sequence law for composition, severity law for genome size, environment birth-death law for gene content; commensals are never in a training pair.

## 검증
- composition:
  - gut lumen (anaerobic, nutrient-rich): `{"predicted": {"ivywrel": 0.3956, "cvp": 0.0254, "acidic_excess": 0.0024, "n_side": 0.3187}, "observed_commensals": {"ivywrel": 0.3851, "cvp": 0.0309, "acidic_e`
  - skin surface (aerobic, dry, nutrient-poor): `{"predicted": {"ivywrel": 0.3892, "cvp": 0.0469, "acidic_excess": 0.0045, "n_side": 0.3094}, "observed_commensals": {"ivywrel": 0.3924, "cvp": 0.019, "acidic_ex`
  - blood and tissue (aerobic, nutrient-rich): `{"predicted": {"ivywrel": 0.3962, "cvp": 0.0412, "acidic_excess": 0.0136, "n_side": 0.3267}, "observed_commensals": {"ivywrel": 0.3933, "cvp": 0.0143, "acidic_e`
- genome_size:
  - commensal_genes: `{"Bacteroides thetaiotaomicron": 4596, "Bifidobacterium longum": 1871, "Akkermansia muciniphila": 2344, "Faecalibacterium prausnitzii": 2848, "Escherichia coli"`
  - free_living_median: 3215.0
  - severity_reference: `{}`
- gene_content:
  - per_ancestor: `{"Bacillus subtilis": {"families_today": 3136, "most_likely_lost": ["CarbopepD_reg_2: CarboxypepD_reg-like domain", "TctC: Tripartite tricarboxylate transporter`
  - validation_auroc: `{"Bacteroides thetaiotaomicron": {"Bacillus subtilis": 0.8931925097845066, "Bacillus subtilis (memorisation)": 0.930595505137248, "Bacillus subtilis (rarity bas`
  - gut_commensals_tested: `["Bacteroides thetaiotaomicron", "Bifidobacterium longum", "Akkermansia muciniphila", "Faecalibacterium prausnitzii", "Streptococcus salivarius", "Lactobacillus`
- optimal_cell:
  - gut lumen (anaerobic, nutrient-rich): `{"pool_families": 3186, "kept_families": 2726, "share_of_pool_kept": 0.856, "functions_kept": [["go:catalytic activity, acting on RNA", 1.11], ["go:amino acid m`
  - skin surface (aerobic, dry, nutrient-poor): `{"pool_families": 3186, "kept_families": 2659, "share_of_pool_kept": 0.835, "functions_kept": [["kw:helicase_nucleic", 1.14], ["go:catalytic activity, acting on`
  - blood and tissue (aerobic, nutrient-rich): `{"pool_families": 3186, "kept_families": 2677, "share_of_pool_kept": 0.84, "functions_kept": [["kw:helicase_nucleic", 1.13], ["go:catalytic activity, acting on `
  - vs_real_commensals: `{"Bacteroides thetaiotaomicron": {"families": 2712, "shared_with_ideal": 1624, "ideal_only": 1102, "commensal_only": 1088, "jaccard": 0.426}, "Bifidobacterium l`

## 한계
- Body sites are coarse: temperature, salt, oxygen and nutrient level only.
- Host-specific pressures (immune system, mucus, host metabolites) are not in the model.
- Commensal genomes are real but their habitat values are approximate.

원본: `laws/human_cell_v1.json`