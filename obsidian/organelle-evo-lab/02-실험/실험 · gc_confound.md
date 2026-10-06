---
유형: 실험
실행: gc_confound
산출: results/gc_confound/metrics.json
tags:
  - 유형/실험
  - 실험/gc_confound
---

# 실험 · gc_confound

**산출물** `results/gc_confound/metrics.json`

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
   "coef": 0.0007660566981552037,
   "p_ols": 4.740580333363116e-25,
   "p_rank_gls": 9.571114001788203e-28,
   "gc_coef": 0.011373588116987353,
   "gc_p_rank_gls": 0.27147246122021895,
   "tree_pgls": [
    0.0006841471365288159,
    1.5832932565065236e-13,
    1.0,
    86
   ]
  },
  "corr_env_gc": 0.026358433625965717,
  "retained_share_of_effect": 0.9762628939649529,
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
   "coef": 0.001065129499124187,
   "p_ols": 7.182419488515516e-17,
   "p_rank_gls": 5.397212641591788e-14,
   "gc_coef": 0.07478647859250324,
   "gc_p_rank_gls": 0.0005422398235305031,
   "tree_pgls": [
    0.0009913228480991796,
    1.811333531065445e-09,
    1.0,
    86
   ]
  },
  "corr_env_gc": 0.026358433625965717,
  "retained_share_of_effect": 0.9413502949286147,
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
   "coef": 0.0015869536875293948,
   "p_ols": 2.646504071709722e-21,
   "p_rank_gls": 1.9427357306055544e-12,
   "gc_coef": 0.03479157674995703,
   "gc_p_rank_gls": 0.00035217485990633474,
   "tree_pgls": 
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
   "coef": -0.01713221841650287,
   "p_ols": 1.4704984178667016e-09,
   "p_rank_gls": 3.299348957690763e-23,
   "gc_coef": -0.0036421115511516026,
   "gc_p_rank_gls": 0.7816968629889638,
   "tree_pgls": [
    -0.019204731802040083,
    2.796454736289544e-07,
    1.0,
    57
   ]
  },
  "corr_env_gc": -0.26243147005387857,
  "retained_share_of_effect": 1.007203995682379,
  "survives": true,
  "survives_tree": true,
  "loo_r2_env": 0.5686674176506967,
  "loo_r2_env_gc": 0.5517460678983483,
  "loo_r2_gc_only": -0.027502003607676517
 },
 "cvp_colder": {
  "n": 57,
  "without_gc": {
   "coef": -0.03335808144228063,
   "p_ols": 6.614835738467015e-11,
   "p_rank_gls": 1.8305065944083973e-13
  },
  "with_gc": {
   "coef": -0.02709061200719634,
   "p_ols": 9.695517650142405e-10,
   "p_rank_gls": 1.5693981932374546e-09,
   "gc_coef": 0.11191472157505133,
   "gc_p_rank_gls": 3.398848288546425e-05,
   "tree_pgls": [
    -0.029450728402549736,
    3.1529883785389706e-06,
    0.9750000000000001,
    57
   ]
  },
  "corr_env_gc": -0.26243147005387857,
  "retained_share_of_effect": 0.8121154105961139,
  "survives": true,
  "survives_tree": true,
  "loo_r2_env": 0.6065368100307953,
  "loo_r2_env_gc": 0.6338457149440149,
  "loo_r2_gc_only": 0.050801759667425395
 },
 "acidic_excess_saltier": {
  "n": 57,
  "without_gc": {
   "coef": 0.01720806023615845,
   "p_ols": 1.08300918510543e-06,
   "p_rank_gls": 2.90877533
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
   "coef": -0.0070344795491337556,
   "p_ols": 0.5630706028199636,
   "p_rank_gls": 0.5722938340358343,
   "gc_coef": -0.8441966309208004,
   "gc_p_rank_gls": 4.3759728586956576e-16,
   "tree_pgls": [
    -5.043038452601581e-05,
    0.9945269033356605,
    1.0,
    25
   ]
  },
  "corr_env_gc": 0.8144555864370934,
  "retained_share_of_effect": 0.08009059420644482,
  "survives": false,
  "survives_tree": false,
  "r_gc": -0.9407307185423358,
  "r_size_gc": 0.8144555864370934
 },
 "median_pi": {
  "n": 25,
  "without_gc": {
   "coef": -1.033058827127401,
   "p_ols": 3.0858241450494217e-07,
   "p_rank_gls": 2.8504147968063422e-12
  },
  "with_gc": {
   "coef": -0.19107443933300816,
   "p_ols": 0.20580671896708647,
   "p_rank_gls": 0.11101176652958632,
   "gc_coef": -8.960763943221751,
   "gc_p_rank_gls": 3.9800855365754345e-19,
   "tree_pgls": [
    -0.09541068273641662,
    0.4075684919723651,
    0.7000000000000001,
    25
   ]
  },
  "corr_env_gc": 0.8144555864370934,
  "retained_share_of_effect": 0.18495988255027423,
  "survives": false,
  "survives_tree": false,
  "r_gc": -0.9619177697637328,
  "r_size_gc": 0.8144555864370934
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
