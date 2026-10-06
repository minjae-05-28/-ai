---
유형: 실험
실행: sequence
산출: results/sequence/metrics.json
tags:
  - 유형/실험
  - 실험/sequence
---

# 실험 · sequence

**산출물** `results/sequence/metrics.json`

## temperature

```json
{
 "n": 86,
 "spearman_ivywrel": 0.6503418536324437,
 "pearson_ivywrel": 0.8497887914025964,
 "ogt_per_0.01_ivywrel": 7.341561238234158,
 "spearman_cvp": 0.6257737241651956,
 "rmse_mean_only": 17.961589930118638,
 "rmse_ivywrel_loo_group": 10.320447078832231,
 "rmse_20aa_ridge_loo_group": 11.288500013648383
}
```

## salt

```json
{
 "spearman_acidic_excess": 0.5629008502955345,
 "spearman_median_pi": -0.510548714340798,
 "halophiles_ge_15pct": {
  "Haloarcula marismortui": {
   "acidic_excess": 0.084855,
   "median_pi": 4.206884
  },
  "Halobacterium salinarum": {
   "acidic_excess": 0.078672,
   "median_pi": 4.26881
  },
  "Haloferax volcanii": {
   "acidic_excess": 0.079275,
   "median_pi": 4.272771
  },
  "Haloquadratum walsbyi": {
   "acidic_excess": 0.070832,
   "median_pi": 4.339017
  },
  "Halothece sp. PCC 7418": {
   "acidic_excess": 0.025868,
   "median_pi": 5.401764
  },
  "Natronomonas pharaonis": {
   "acidic_excess": 0.093704,
   "median_pi": 4.190665
  },
  "Salinibacter ruber": {
   "acidic_excess": 0.045201,
   "median_pi": 4.713526
  }
 },
 "others_median_pi": 6.648356
}
```

## environment_pairs

```json
{
 "n_pairs": 57,
 "by_statistic": {
  "ivywrel": {
   "loo_r2_environment": 0.5686674176506967,
   "coef": {
    "base": 0.003998825936436327,
    "colder": -0.02658101206765905,
    "saltier": -0.0062457141524740085,
    "anaerobic": -0.0006571969824258252,
    "radiation_resistant": -0.015625741623805128,
    "oligotrophic": -0.002747757602957949
   }
  },
  "cvp": {
   "loo_r2_environment": 0.6065368100307953,
   "coef": {
    "base": 0.0019542583997788415,
    "colder": -0.04144075488029967,
    "saltier": 0.00325518265976435,
    "anaerobic": -0.01579191112084569,
    "radiation_resistant": -0.02558616057644775,
    "oligotrophic": 0.01089178265507703
   }
  },
  "acidic_excess": {
   "loo_r2_environment": 0.5388751409066659,
   "coef": {
    "base": -0.0004035415366262374,
    "colder": 0.004966627807735196,
    "saltier": 0.018446693075596297,
    "anaerobic": -0.011164886580372577,
    "radiation_resistant": -0.0014734955945175548,
    "oligotrophic": -0.011740134445712928
   }
  },
  "median_pi": {
   "loo_r2_environment": 0.23598902879022743,
   "coef": {
    "base": 0.03798152087893734,
    "colder": -0.43671067458760443,
    "saltier": -0.7303652929219004,
    "anaerobic": 0.15423237767649042,
    "radiation_resistant": 0.0807346614108509,
    "oligotrophic": 0.8540274985986673
   }
  },
  "share_pi_below_5": {
   "loo_r2_environment": 0.6439767829584997,
   "coef": {
    "base": -0.003562643117780746,
    "colder": 0.07195906316938326,
    "saltier": 0.18052287782014406,
    "anaerobic": -0.061019453458169774,
    "radiation_resistant": -0.024517765230706128,

… (잘림 — 원본 파일 참조)
```

## oligotrophy

```json
[
 {
  "pair": "Synechococcus elongatus -> Prochlorococcus marinus",
  "n_side_change": -0.025682999999999956
 },
 {
  "pair": "Cereibacter sphaeroides -> Candidatus Pelagibacter ubique",
  "n_side_change": -0.03568699999999997
 },
 {
  "pair": "Sphingobium japonicum -> Sphingopyxis alaskensis",
  "n_side_change": -0.0067609999999999615
 },
 {
  "pair": "Nitrososphaera viennensis -> Nitrosopumilus maritimus",
  "n_side_change": -0.02932100000000004
 },
 {
  "pair": "Synechococcus elongatus -> Synechococcus sp. WH 8102",
  "n_side_change": 0.007765999999999995
 },
 {
  "pair": "Cupriavidus necator -> Polynucleobacter asymbioticus",
  "n_side_change": -0.03782399999999997
 },
 {
  "pair": "Methylobacillus flagellatus -> Candidatus Methylopumilus planktonicus",
  "n_side_change": -0.01929900000000001
 }
]
```

## endosymbionts

```json
{
 "spearman_size_fymink": -0.7962393162393162,
 "spearman_size_pi": -0.8276923076923076,
 "table": {
  "Arsenophonus nasoniae": {
   "n_proteins": 4221,
   "fymink": 0.293604,
   "median_pi": 8.466324,
   "n_side": 0.372428
  },
  "Buchnera aphidicola (Cinara tujafilina)": {
   "n_proteins": 359,
   "fymink": 0.429202,
   "median_pi": 10.209863,
   "n_side": 0.375721
  },
  "Buchnera aphidicola (Myzus persicae)": {
   "n_proteins": 578,
   "fymink": 0.399056,
   "median_pi": 9.884229,
   "n_side": 0.36666
  },
  "Buchnera aphidicola (Schizaphis graminum)": {
   "n_proteins": 567,
   "fymink": 0.406538,
   "median_pi": 9.992353,
   "n_side": 0.367233
  },
  "Buchnera aphidicola (Uroleucon sonchi)": {
   "n_proteins": 538,
   "fymink": 0.408111,
   "median_pi": 9.8372,
   "n_side": 0.37152
  },
  "Buchnera aphidicola BCc": {
   "n_proteins": 364,
   "fymink": 0.473183,
   "median_pi": 10.497503,
   "n_side": 0.384942
  },
  "Buchnera aphidicola str. APS (Acyrthosiphon pisum)": {
   "n_proteins": 569,
   "fymink": 0.394869,
   "median_pi": 9.885265,
   "n_side": 0.367507
  },
  "Buchnera aphidicola str. Bp (Baizongia pistaciae)": {
   "n_proteins": 504,
   "fymink": 0.399627,
   "median_pi": 9.99036,
   "n_side": 0.367974
  },
  "Candidatus Annandia pinicola": {
   "n_proteins": 315,
   "fymink": 0.510115,
   "median_pi": 10.386768,
   "n_side": 0.37476
  },
  "Candidatus Blochmanniella floridana": {
   "n_proteins": 583,
   "fymink": 0.366577,
   "median_pi": 9.170506,
   "n_side": 0.364004
  },
  "Candidatus Blochmanniella pennsylvanica": {
   "n_proteins": 574,
   "fymink"
… (잘림 — 원본 파일 참조)
```

## eukaryote_pairs

```json
{
 "n_pairs": 99,
 "by_statistic": {
  "fymink": {
   "loo_clade_r2": 0.06772146651298305,
   "coef": {
    "base": -0.0030539000000000087,
    "parasite": 0.0008898947149867734,
    "intracellular": 0.07267913892034733,
    "reduced_mitochondria": 0.04812702114005284
   }
  },
  "median_pi": {
   "loo_clade_r2": -0.010452988286512754,
   "coef": {
    "base": 0.021938150000000135,
    "parasite": 0.16688219226752182,
    "intracellular": 0.5205669080156041,
    "reduced_mitochondria": 0.11581918648546637
   }
  },
  "n_side": {
   "loo_clade_r2": -0.12886791640021067,
   "coef": {
    "base": 0.002470350000000001,
    "parasite": -0.000572783874418011,
    "intracellular": 0.0013101666037498411,
    "reduced_mitochondria": -0.013242375613439033
   }
  },
  "ivywrel": {
   "loo_clade_r2": -0.035736312667387304,
   "coef": {
    "base": 0.008708899999999993,
    "parasite": -0.003323460337234174,
    "intracellular": -0.0009570806593683225,
    "reduced_mitochondria": 0.021761796904492252
   }
  },
  "mean_length": {
   "loo_clade_r2": -0.213481765221623,
   "coef": {
    "base": -47.892053049999944,
    "parasite": 43.2378817214483,
    "intracellular": 33.49507496954828,
    "reduced_mitochondria": -157.9174484635712
   }
  }
 }
}
```

## 연결
- [[실험 목록]]
