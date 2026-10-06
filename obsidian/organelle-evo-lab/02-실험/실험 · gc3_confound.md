---
유형: 실험
실행: gc3_confound
산출: results/gc3_confound/metrics.json
tags:
  - 유형/실험
  - 실험/gc3_confound
---

# 실험 · gc3_confound

**산출물** `results/gc3_confound/metrics.json`

## species

```json
{
 "ivywrel_vs_temperature": {
  "n": 86,
  "without_gc": {
   "coef": 0.0007846827969093175,
   "p_ols": 4.445318433615807e-25,
   "p_rank_gls": 1.4026427901225574e-29
  },
  "with_gc": {
   "coef": 0.0007650583083863832,
   "p_ols": 7.746521697116802e-25,
   "p_rank_gls": 2.21783090891188e-27,
   "gc_coef": 0.005761652745353064,
   "gc_p_rank_gls": 0.2841923741274591,
   "tree_pgls": [
    0.0006833226742151441,
    2.1430710457514176e-13,
    1.0,
    86
   ]
  },
  "corr_env_gc": 0.0822168597467676,
  "retained_share_of_effect": 0.9749905457336001,
  "survives": true,
  "survives_tree": true
 },
 "cvp_vs_temperature": {
  "n": 86,
  "without_gc": {
   "coef": 0.0011314911195783488,
   "p_ols": 1.2826360080756616e-15,
   "p_rank_gls": 2.7956914349351982e-14
  },
  "with_gc": {
   "coef": 0.0010238985159502707,
   "p_ols": 1.1794565029545345e-16,
   "p_rank_gls": 1.8217323928543403e-13,
   "gc_coef": 0.043793832493990645,
   "gc_p_rank_gls": 6.829795634288409e-05,
   "tree_pgls": [
    0.0009679781564405404,
    2.980979583367948e-09,
    1.0,
    86
   ]
  },
  "corr_env_gc": 0.0822168597467676,
  "retained_share_of_effect": 0.9049107838617658,
  "survives": true,
  "survives_tree": true
 },
 "acidic_vs_salt": {
  "n": 86,
  "without_gc": {
   "coef": 0.0016532843066467589,
   "p_ols": 2.8549288559408527e-21,
   "p_rank_gls": 9.102153725007249e-12
  },
  "with_gc": {
   "coef": 0.0016200549377106879,
   "p_ols": 2.5351249893404436e-21,
   "p_rank_gls": 1.5846581637390547e-12,
   "gc_coef": 0.015934217829399976,
   "gc_p_rank_gls": 0.0017340981522870572,
   "tree_pgls": [
… (잘림 — 원본 파일 참조)
```

## pairs

```json
{
 "ivywrel_colder": {
  "n": 57,
  "without_gc": {
   "coef": -0.017009680749822505,
   "p_ols": 1.3155166503670074e-10,
   "p_rank_gls": 2.4306774423716094e-24
  },
  "with_gc": {
   "coef": -0.017184961217512177,
   "p_ols": 2.3175793965297867e-09,
   "p_rank_gls": 3.997662452727659e-24,
   "gc_coef": -0.0028778199141844484,
   "gc_p_rank_gls": 0.6320235758197892,
   "tree_pgls": [
    -0.019270580178195277,
    2.9939632405208374e-07,
    1.0,
    57
   ]
  },
  "corr_env_gc": -0.29930936679351905,
  "retained_share_of_effect": 1.010304747647395,
  "survives": true,
  "survives_tree": true,
  "loo_r2_env": 0.5686674176506967,
  "loo_r2_env_gc": 0.5546038526688173,
  "loo_r2_gc_only": -0.014587356948127628
 },
 "cvp_colder": {
  "n": 57,
  "without_gc": {
   "coef": -0.03335808144228063,
   "p_ols": 6.614835738467015e-11,
   "p_rank_gls": 1.8305065944083973e-13
  },
  "with_gc": {
   "coef": -0.018439084437510113,
   "p_ols": 1.5922594804916433e-09,
   "p_rank_gls": 1.6535467045234573e-10,
   "gc_coef": 0.07837743305255795,
   "gc_p_rank_gls": 1.5316666286009045e-13,
   "tree_pgls": [
    -0.027060595405719666,
    9.611965011295996e-06,
    1.0,
    57
   ]
  },
  "corr_env_gc": -0.29930936679351905,
  "retained_share_of_effect": 0.5527621385964656,
  "survives": true,
  "survives_tree": true,
  "loo_r2_env": 0.6065368100307953,
  "loo_r2_env_gc": 0.6529000102494347,
  "loo_r2_gc_only": 0.07946193981175853
 },
 "acidic_excess_saltier": {
  "n": 57,
  "without_gc": {
   "coef": 0.01720806023615845,
   "p_ols": 1.08300918510543e-06,
   "p_rank_gls": 2.908775330088942e-07

… (잘림 — 원본 파일 참조)
```

## symbionts

```json
{
 "fymink": {
  "n": 25,
  "without_gc": {
   "coef": -0.08783153151544101,
   "p_ols": 2.240287806120025e-06,
   "p_rank_gls": 7.011868635315649e-10
  },
  "with_gc": {
   "coef": -0.039841167767608425,
   "p_ols": 0.11671718732638943,
   "p_rank_gls": 0.009770801919154581,
   "gc_coef": -0.3652472541102037,
   "gc_p_rank_gls": 1.4316883145145366e-05,
   "tree_pgls": [
    -0.0033061385699643397,
    0.7293928132060093,
    1.0,
    25
   ]
  },
  "corr_env_gc": 0.7915227389647932,
  "retained_share_of_effect": 0.45360893838682803,
  "survives": true,
  "survives_tree": false,
  "r_gc": -0.8793917831818262,
  "r_size_gc": 0.7915227389647932
 },
 "median_pi": {
  "n": 25,
  "without_gc": {
   "coef": -1.033058827127401,
   "p_ols": 3.0858241450494217e-07,
   "p_rank_gls": 2.8504147968063422e-12
  },
  "with_gc": {
   "coef": -0.448731711420695,
   "p_ols": 0.052406119067445904,
   "p_rank_gls": 0.0011072592034112442,
   "gc_coef": -4.45694781994961,
   "gc_p_rank_gls": 2.3007199715799356e-09,
   "tree_pgls": [
    -0.13538180205424633,
    0.32190950348198244,
    0.775,
    25
   ]
  },
  "corr_env_gc": 0.7915227389647932,
  "retained_share_of_effect": 0.4343718863217802,
  "survives": true,
  "survives_tree": false,
  "r_gc": -0.9330097743680901,
  "r_size_gc": 0.7915227389647932
 }
}
```

## summary

```json
{
 "adaptive_laws_tested": 10,
 "survive": [
  "pair:acidic_excess_saltier",
  "pair:cvp_colder",
  "pair:ivywrel_colder",
  "species:acidic_vs_salt",
  "species:cvp_vs_temperature",
  "species:fymink_vs_anoxia",
  "species:ivywrel_vs_temperature"
 ],
 "do_not_survive": [
  "pair:fymink_anaerobic",
  "pair:n_side_oligotrophic",
  "species:nitrogen_vs_oligotrophy"
 ]
}
```

## 연결
- [[실험 목록]]
