---
id: phylo_check_v1
system: 공통
status: 현역
tags:
  - 법칙
  - 공통
---
# phylo_check_v1

> 계통 보정(분류 체계 기반 분산 성분 모델) 뒤에도 14개 법칙 중 13개 유지. 세포 안 효과는 탈락, 빈영양 질소 절약은 보정 후에야 드러남.

**시스템**: 공통  
**상태**: 현역  
**주제**: [[계통 보정]]

## 적용 범위 (원문)
Which species-level laws survive phylogenetic correction (taxonomy rank GLS).

## 모델
OLS vs PGLS (Pagel's lambda) vs rank GLS on NCBI taxonomy.

## 검증
- ivywrel_vs_temperature:
  - n: 86
  - ols: `[0.0009836340889355275, 4.445318433615807e-25]`
  - pgls_lambda: `[0.0007953410425981276, 6.753073158980977e-17, 1.0]`
  - rank_gls: `[0.0007846827969093175, 1.4026427901225574e-29]`
  - shared_history: 0.96
  - survives: True
  - tree_pgls: `[0.000699702987400929, 1.579688065266408e-14, 1.0, 86]`
  - survives_tree: True
  - bootstrap_trees: `{"n": 20, "share_surviving": 1.0, "median_p": 1.3477423840651523e-14, "max_p": 4.711857480199185e-14}`
- cvp_vs_temperature:
  - n: 86
  - ols: `[0.0015003773088000105, 1.2826360080756616e-15]`
  - pgls_lambda: `[0.0011644724078450966, 1.4192050565441594e-10, 1.0]`
  - rank_gls: `[0.0011314911195783488, 2.7956914349351982e-14]`
  - shared_history: 0.945
  - survives: True
  - tree_pgls: `[0.0010972296663107142, 1.249301689678215e-10, 1.0, 86]`
  - survives_tree: True
  - bootstrap_trees: `{"n": 20, "share_surviving": 1.0, "median_p": 1.524637541215002e-10, "max_p": 3.1814885205037154e-10}`
- acidic_vs_salt:
  - n: 86
  - ols: `[0.0026986995597669955, 2.8549288559408527e-21]`
  - pgls_lambda: `[0.0017338889753079228, 3.306686468250499e-10, 1.0]`
  - rank_gls: `[0.0016532843066467589, 9.102153725007249e-12]`
  - shared_history: 0.951
  - survives: True
  - tree_pgls: `[0.0013304907044416143, 2.545643941473514e-07, 1.0, 86]`
  - survives_tree: True
  - bootstrap_trees: `{"n": 20, "share_surviving": 1.0, "median_p": 2.72266529458503e-07, "max_p": 5.66047069593581e-07}`
- nitrogen_vs_oligotrophy:
  - n: 86
  - ols: `[-0.0023329240506329064, 0.8118705882493471]`
  - pgls_lambda: `[-0.018930623507242905, 0.007756787055000871, 1.0]`
  - rank_gls: `[-0.021897687755785544, 0.0006753135619025098]`
  - shared_history: 0.941
  - survives: True
  - tree_pgls: `[-0.019536432151458373, 0.0051578627056062575, 1.0, 86]`
  - survives_tree: True
  - bootstrap_trees: `{"n": 20, "share_surviving": 1.0, "median_p": 0.005731964641475554, "max_p": 0.007389965703554131}`
- fymink_vs_anoxia:
  - n: 86
  - ols: `[0.07102068892045449, 5.687965000989708e-06]`
  - pgls_lambda: `[0.07722317804568216, 0.0001799850783917852, 1.0]`
  - rank_gls: `[0.0805164234477487, 0.0003614792927730401]`
  - shared_history: 0.992
  - survives: True
  - tree_pgls: `[0.06670960514493034, 0.0011755087032298572, 1.0, 86]`
  - survives_tree: True
  - bootstrap_trees: `{"n": 20, "share_surviving": 1.0, "median_p": 0.0011485610138193404, "max_p": 0.003071519959223838}`
- regulator_scaling:
  - n: 86
  - ols: `[1.9181540991402375, 2.483464311417658e-29]`
  - pgls_lambda: `[1.732038770507751, 1.48191789373561e-33, 0.9750000000000001]`
  - rank_gls: `[1.7101659200308499, 1.0120340168470112e-105]`
  - shared_history: 0.914
  - survives: True
  - tree_pgls: `[1.6949941509944704, 1.2694845324678092e-35, 1.0, 86]`
  - survives_tree: True
  - bootstrap_trees: `{"n": 20, "share_surviving": 1.0, "median_p": 1.389003104261182e-35, "max_p": 3.6276312517674805e-34}`
- symbiont_fymink_vs_size:
  - n: 25
  - ols: `[-0.0846112973324131, 2.240287806120025e-06]`
  - pgls_lambda: `[-0.08228479482779738, 9.151436406188662e-06, 1.0]`
  - rank_gls: `[-0.08783153151544101, 7.011868635315649e-10]`
  - shared_history: 0.936
  - survives: True
  - tree_pgls: `[-0.026530996189244795, 0.08412135305420342, 0.9750000000000001, 24]`
  - survives_tree: False
  - bootstrap_trees: `{"n": 20, "share_surviving": 0.05, "median_p": 0.06917166690500745, "max_p": 0.10150903886655027}`
- severity_parasite:
  - n: 112
  - ols: `[0.9286313453495856, 0.0003062718464204821]`
  - pgls_lambda: `[0.8836001723865257, 0.00014106295062866892, 0.875]`
  - rank_gls: `[0.932038458525714, 5.2713013303056326e-06]`
  - shared_history: 0.973
  - survives: True
  - tree_pgls: `[0.8996226089194719, 1.1308531033314826e-06, 1.0, 112]`
  - survives_tree: True
  - bootstrap_trees: `{"n": 20, "share_surviving": 1.0, "median_p": 1.2368733470085743e-06, "max_p": 2.26344726803586e-06}`
- severity_intracellular:
  - n: 112
  - ols: `[0.7595963641727692, 0.00025821350519175695]`
  - pgls_lambda: `[0.5418713437316627, 0.016224188436780595, 0.875]`
  - rank_gls: `[0.4798653538938211, 0.02151995063808182]`
  - shared_history: 0.973
  - survives: True
  - tree_pgls: `[-0.017251982724174813, 0.918916175897096, 1.0, 112]`
  - survives_tree: False
  - bootstrap_trees: `{"n": 20, "share_surviving": 0.0, "median_p": 0.919833134440389, "max_p": 0.9775843470148862}`
- severity_reduced_mitochondria:
  - n: 112
  - ols: `[1.7190805569498997, 6.865224372571666e-11]`
  - pgls_lambda: `[1.3942601786804252, 3.4076420930738784e-07, 0.875]`
  - rank_gls: `[1.23960770768075, 7.018290443518591e-07]`
  - shared_history: 0.973
  - survives: True
  - tree_pgls: `[0.9549514586322134, 0.016546011647155783, 1.0, 112]`
  - survives_tree: True
  - bootstrap_trees: `{"n": 20, "share_surviving": 1.0, "median_p": 0.01737983037803762, "max_p": 0.03670845044290161}`
- pair_ivywrel_colder:
  - n: 57
  - ols: `[-0.02658101206765906, 1.3155166503670074e-10]`
  - pgls_lambda: `[-0.02079260617959002, 1.9463521482307834e-08, 1.0]`
  - rank_gls: `[-0.017009680749822505, 2.4306774423716094e-24]`
  - shared_history: 0.995
  - survives: True
  - tree_pgls: `[-0.019259135828574407, 8.007667284930708e-08, 1.0, 57]`
  - survives_tree: True
  - bootstrap_trees: `{"n": 20, "share_surviving": 1.0, "median_p": 8.078975236913248e-08, "max_p": 3.5251400425897624e-07}`
- pair_cvp_colder:
  - n: 57
  - ols: `[-0.04144075488029968, 6.614835738467015e-11]`
  - pgls_lambda: `[-0.03488394681244622, 2.0935306211085331e-07, 1.0]`
  - rank_gls: `[-0.03335808144228063, 1.8305065944083973e-13]`
  - shared_history: 0.898
  - survives: True
  - tree_pgls: `[-0.03543461205354881, 8.792935952240313e-08, 0.925, 57]`
  - survives_tree: True
  - bootstrap_trees: `{"n": 20, "share_surviving": 1.0, "median_p": 5.626255128007976e-08, "max_p": 1.8214495717159368e-07}`

## 한계
- Taxonomy is a coarse stand-in for a sequence-based phylogeny.

원본: `laws/phylo_check_v1.json`