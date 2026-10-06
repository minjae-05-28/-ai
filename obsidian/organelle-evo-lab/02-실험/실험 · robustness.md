---
유형: 실험
실행: robustness
산출: results/robustness/metrics.json
tags:
  - 유형/실험
  - 실험/robustness
---

# 실험 · robustness

**산출물** `results/robustness/metrics.json`

## bootstrap

```json
{
 "parasites_leave_one_clade_out": {
  "n_rows": 51,
  "n_units": 9,
  "unit": "clade",
  "stats": {
   "law": {
    "estimate": 0.7769,
    "ci95": [
     0.7449,
     0.7949
    ]
   },
   "memorisation": {
    "estimate": 0.8022,
    "ci95": [
     0.7683,
     0.8218
    ]
   },
   "copies_only": {
    "estimate": 0.6389,
    "ci95": [
     0.6302,
     0.6521
    ]
   },
   "memorisation - law": {
    "estimate": 0.0253,
    "ci95": [
     0.0106,
     0.0357
    ]
   }
  }
 },
 "parasites_5fold": {
  "n_rows": 51,
  "n_units": 51,
  "unit": "pair",
  "stats": {
   "enriched": {
    "estimate": 0.7823,
    "ci95": [
     0.7668,
     0.7958
    ]
   },
   "base": {
    "estimate": 0.6691,
    "ci95": [
     0.6605,
     0.6778
    ]
   },
   "memorisation": {
    "estimate": 0.8652,
    "ci95": [
     0.8425,
     0.8867
    ]
   },
   "enriched - base": {
    "estimate": 0.1132,
    "ci95": [
     0.0974,
     0.1253
    ]
   },
   "memorisation - enriched": {
    "estimate": 0.083,
    "ci95": [
     0.0674,
     0.0979
    ]
   }
  }
 },
 "extremophiles_leave_one_pair_out": {
  "n_rows": 40,
  "n_units": 40,
  "unit": "pair",
  "stats": {
   "no_environment": {
    "estimate": 0.8191,
    "ci95": [
     0.8054,
     0.8315
    ]
   },
   "environment_law": {
    "estimate": 0.8189,
    "ci95": [
     0.805,
     0.8315
    ]
   },
   "memorisation": {
    "estimate": 0.844,
    "ci95": [
     0.8241,
     0.8619
    ]
   },
   "environment_law - no_environment": {
    "estimate": -0.0003,
    "ci95": [
     -0.0039,
     0.0026
    ]
   },
   "memorisation - no_env
… (잘림 — 원본 파일 참조)
```

## fdr

```json
{
 "phylo:regulator_scaling": {
  "p": 1.0120340168470112e-105,
  "q": 2.631288443802229e-104,
  "significant_q05": true
 },
 "phylo:ivywrel_vs_temperature": {
  "p": 1.4026427901225574e-29,
  "q": 1.8234356271593247e-28,
  "significant_q05": true
 },
 "gc:species:ivywrel_vs_temperature": {
  "p": 9.571114001788203e-28,
  "q": 8.294965468216442e-27,
  "significant_q05": true
 },
 "phylo:pair_ivywrel_colder": {
  "p": 2.4306774423716094e-24,
  "q": 1.5799403375415462e-23,
  "significant_q05": true
 },
 "gc:pairs:ivywrel_colder": {
  "p": 3.299348957690763e-23,
  "q": 1.7156614579991969e-22,
  "significant_q05": true
 },
 "phylo:cvp_vs_temperature": {
  "p": 2.7956914349351982e-14,
  "q": 1.2114662884719193e-13,
  "significant_q05": true
 },
 "gc:species:cvp_vs_temperature": {
  "p": 5.397212641591788e-14,
  "q": 2.0046789811626643e-13,
  "significant_q05": true
 },
 "phylo:pair_cvp_colder": {
  "p": 1.8305065944083973e-13,
  "q": 5.949146431827292e-13,
  "significant_q05": true
 },
 "gc:species:acidic_vs_salt": {
  "p": 1.9427357306055544e-12,
  "q": 5.612347666193824e-12,
  "significant_q05": true
 },
 "phylo:acidic_vs_salt": {
  "p": 9.102153725007249e-12,
  "q": 2.3665599685018845e-11,
  "significant_q05": true
 },
 "phylo:symbiont_fymink_vs_size": {
  "p": 7.011868635315649e-10,
  "q": 1.6573507683473353e-09,
  "significant_q05": true
 },
 "gc:pairs:cvp_colder": {
  "p": 1.5693981932374546e-09,
  "q": 3.400362752014485e-09,
  "significant_q05": true
 },
 "phylo:pair_acidic_excess_saltier": {
  "p": 2.909561232130709e-07,
  "q": 5.819122464261418e-07,
  "significant_q05":
… (잘림 — 원본 파일 참조)
```

## 연결
- [[실험 목록]]
