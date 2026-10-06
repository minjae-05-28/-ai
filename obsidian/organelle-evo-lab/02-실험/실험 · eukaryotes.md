---
유형: 실험
실행: eukaryotes
산출: results/eukaryotes/metrics.json
tags:
  - 유형/실험
  - 실험/eukaryotes
---

# 실험 · eukaryotes

**산출물** `results/eukaryotes/metrics.json`

## 한눈에

| 항목 | 값 |
| --- | --- |
| n_families | 10746 |
| delta_aic_lifestyle_vs_shared | 213.1 |

## species

```json
[
 "Dictyostelium discoideum",
 "Dictyostelium purpureum",
 "Entamoeba histolytica",
 "Tetrahymena thermophila",
 "Ichthyophthirius multifiliis",
 "Plasmodium falciparum",
 "Toxoplasma gondii",
 "Cryptosporidium parvum",
 "Bodo saltans",
 "Leishmania major",
 "Trypanosoma brucei",
 "Naegleria gruberi",
 "Naegleria fowleri",
 "Spizellomyces punctatus",
 "Encephalitozoon cuniculi",
 "Saccharomyces cerevisiae",
 "Kluyveromyces lactis",
 "Chlamydomonas reinhardtii",
 "Volvox carteri",
 "Monosiga brevicollis",
 "Salpingoeca rosetta",
 "Drosophila melanogaster",
 "Anopheles gambiae"
]
```

## pairs

```json
[
 "Dictyostelium discoideum -> Entamoeba histolytica",
 "Tetrahymena thermophila -> Ichthyophthirius multifiliis",
 "Tetrahymena thermophila -> Plasmodium falciparum",
 "Tetrahymena thermophila -> Toxoplasma gondii",
 "Tetrahymena thermophila -> Cryptosporidium parvum",
 "Bodo saltans -> Leishmania major",
 "Bodo saltans -> Trypanosoma brucei",
 "Spizellomyces punctatus -> Encephalitozoon cuniculi",
 "Dictyostelium discoideum -> Dictyostelium purpureum",
 "Naegleria gruberi -> Naegleria fowleri",
 "Saccharomyces cerevisiae -> Kluyveromyces lactis",
 "Chlamydomonas reinhardtii -> Volvox carteri",
 "Monosiga brevicollis -> Salpingoeca rosetta",
 "Drosophila melanogaster -> Anopheles gambiae"
]
```

## loss_law

```json
{
 "free_living": {
  "hydrophobicity_gravy": {
   "weight": 0.06276279275965253,
   "se": 0.022619823636836633
  },
  "tm_helices": {
   "weight": -0.007976730799261863,
   "se": 0.0193241899985692
  },
  "protein_length": {
   "weight": -0.12929744826103526,
   "se": 0.027006182131776545
  },
  "redox_core": {
   "weight": 0.13091190828480218,
   "se": 0.18284607661297186
  },
  "atp_synthase": {
   "weight": -0.15199660327321332,
   "se": 0.28789321150377284
  },
  "translation": {
   "weight": -0.6248424612836618,
   "se": 0.24853069987231424
  },
  "transcription": {
   "weight": -1.4261055539690226,
   "se": 0.38350456128003946
  },
  "protein_targeting": {
   "weight": 0.055026687719785215,
   "se": 0.27036335924730454
  }
 },
 "parasite": {
  "hydrophobicity_gravy": {
   "weight": 0.05186706055540507,
   "se": 0.012478334782633467
  },
  "tm_helices": {
   "weight": 0.05556061013533742,
   "se": 0.02608781965964912
  },
  "protein_length": {
   "weight": -0.052079716956102334,
   "se": 0.013423651725293188
  },
  "redox_core": {
   "weight": -0.19753973580385503,
   "se": 0.2378141393650445
  },
  "atp_synthase": {
   "weight": -1.2763349095442915,
   "se": 0.13188115101806552
  },
  "translation": {
   "weight": -1.0859609059402517,
   "se": 0.0662812968926967
  },
  "transcription": {
   "weight": -1.5412938163638332,
   "se": 0.11663317449692852
  },
  "protein_targeting": {
   "weight": -0.5199409803994385,
   "se": 0.08438992018399964
  }
 }
}
```

## duplication_law

```json
{
 "free_living": {
  "hydrophobicity_gravy": {
   "weight": 0.14818658345189206,
   "se": 0.04302000507965556
  },
  "tm_helices": {
   "weight": -0.09304553277385688,
   "se": 0.025385064068566398
  },
  "protein_length": {
   "weight": -0.1921678802279893,
   "se": 0.026107910005717806
  },
  "redox_core": {
   "weight": -0.7819444619725027,
   "se": 0.35483973914643924
  },
  "atp_synthase": {
   "weight": -1.5337880390141048,
   "se": 0.2552816469936668
  },
  "translation": {
   "weight": -0.759523766760204,
   "se": 0.18329148667221323
  },
  "transcription": {
   "weight": -0.9383669988057781,
   "se": 0.4671607577879508
  },
  "protein_targeting": {
   "weight": -0.8838998462571052,
   "se": 0.20715389632747194
  }
 },
 "parasite": {
  "hydrophobicity_gravy": {
   "weight": 0.16057366687232938,
   "se": 0.060752687987858954
  },
  "tm_helices": {
   "weight": 0.023110888874818266,
   "se": 0.06643251195995901
  },
  "protein_length": {
   "weight": -0.09178003021080265,
   "se": 0.027252811329012794
  },
  "redox_core": {
   "weight": -1.8103321719029823,
   "se": 0.17765927799136907
  },
  "atp_synthase": {
   "weight": -1.30746934257585,
   "se": 0.3041634452307252
  },
  "translation": {
   "weight": -0.701731123329558,
   "se": 0.19461972953264317
  },
  "transcription": {
   "weight": -1.600723228463899,
   "se": 0.46277701291240464
  },
  "protein_targeting": {
   "weight": -0.8566410660990516,
   "se": 0.2523361157513379
  }
 }
}
```

## origination_law

```json
{
 "free_living": {
  "hydrophobicity_gravy": {
   "weight": 0.04479342203543355,
   "se": 0.03593507718266907
  },
  "tm_helices": {
   "weight": -0.021430547144357697,
   "se": 0.026612256669596254
  },
  "protein_length": {
   "weight": 0.027415883281141955,
   "se": 0.030336855863113268
  },
  "redox_core": {
   "weight": 0.875980066565689,
   "se": 0.26810185415960547
  },
  "atp_synthase": {
   "weight": 0.3578230825818077,
   "se": 0.3035218292220218
  },
  "translation": {
   "weight": 0.5599477943124046,
   "se": 0.08050415799537915
  },
  "transcription": {
   "weight": 0.062129443432448354,
   "se": 0.8121646009386664
  },
  "protein_targeting": {
   "weight": 0.4073140521492827,
   "se": 0.1393780158335782
  }
 },
 "parasite": {
  "hydrophobicity_gravy": {
   "weight": 0.05576170630799706,
   "se": 0.048508831067639355
  },
  "tm_helices": {
   "weight": -0.030291628427076493,
   "se": 0.05246391085056594
  },
  "protein_length": {
   "weight": 0.05060217875916438,
   "se": 0.046089807574348114
  },
  "redox_core": {
   "weight": 0.02894899573997083,
   "se": 0.3788010360152938
  },
  "atp_synthase": {
   "weight": 0.017517237903261738,
   "se": 0.22944048522340174
  },
  "translation": {
   "weight": 0.9552350489145639,
   "se": 0.10407013271110377
  },
  "transcription": {
   "weight": 0.9990593313779278,
   "se": 0.17353828391410095
  },
  "protein_targeting": {
   "weight": 0.5024112303248851,
   "se": 0.20283309585170556
  }
 }
}
```

## heldout_parasites

```json
[
 {
  "pair": "Dictyostelium discoideum -> Entamoeba histolytica",
  "n_lost": 2584,
  "copies_only": 0.6538274396929824,
  "learned_law": 0.6721158652605779,
  "loss_frequency_elsewhere": 0.7829968274316306,
  "reference_mitochondrion": 0.6271125596620227,
  "reference_plastid": 0.6718872952141383,
  "reference_insect_endosymbiont": 0.6623153702270382
 },
 {
  "pair": "Tetrahymena thermophila -> Ichthyophthirius multifiliis",
  "n_lost": 1108,
  "copies_only": 0.6843729713573167,
  "learned_law": 0.7025731556767747,
  "loss_frequency_elsewhere": 0.731079817797725,
  "reference_mitochondrion": 0.6877400317266094,
  "reference_plastid": 0.7022353404539178,
  "reference_insect_endosymbiont": 0.7122024462803742
 },
 {
  "pair": "Tetrahymena thermophila -> Plasmodium falciparum",
  "n_lost": 1575,
  "copies_only": 0.586142480030169,
  "learned_law": 0.6140303061469368,
  "loss_frequency_elsewhere": 0.8693085124618601,
  "reference_mitochondrion": 0.5961342521169735,
  "reference_plastid": 0.6207658815866159,
  "reference_insect_endosymbiont": 0.6206606328636566
 },
 {
  "pair": "Tetrahymena thermophila -> Toxoplasma gondii",
  "n_lost": 1175,
  "copies_only": 0.5947059823891765,
  "learned_law": 0.622996863308265,
  "loss_frequency_elsewhere": 0.8837549601300027,
  "reference_mitochondrion": 0.595445750349571,
  "reference_plastid": 0.6252110653414459,
  "reference_insect_endosymbiont": 0.6252333623067912
 },
 {
  "pair": "Tetrahymena thermophila -> Cryptosporidium parvum",
  "n_lost": 1754,
  "copies_only": 0.5945160953939455,
  "learned_law": 0.6243013152074568,
  "loss_frequency_elsewhere": 0.8760130546114048,
  "reference_mitochondrion": 0.5923507774220789,
  "reference_plastid": 0.6246472072032775,
  "reference_insect_endosymbiont": 0.6225636765013587
 },
 {
  "pair": "Bodo saltans -> Leishmania major",
  "n_lost": 716,
  "copies_only": 0.6183900794168011,
  "learned_law": 0.634380463556812,
  "loss_frequency_elsewhere": 0.8633756859643051,
  "reference_mitochondrion": 0.6074986404311069,
  "reference_plastid": 0.6312214321990859,
  "reference_insect_endosymbiont": 0.6450648772792442
 },
 {
  "pair": "Bodo saltans -> Trypanosoma brucei",
  "n_lost": 739,
  "copies_only": 0.6070646653008505,
  "learned_law": 0.6231753634439227,
  "loss_frequency_elsewhere": 0.8644611426376956,
  "reference_mitochondrion": 0.5909144101305547,
  "reference_plastid": 0.6219386569400331,
  "reference_insect_endosymbiont": 0.6339623450065022
 },
 {
  "pair": "Spizellomyces punctatus -> Encephalitozoon cuniculi",
  "n_lost": 3806,
  "copies_only": 0.6851860894847471,
  "learned_law": 0.7092126006029261,
  "loss_frequency_elsewhere": 0.8191473340224577,
  "reference_mitochondrion": 0.6270345299665349,
  "reference_plastid": 0.7061394145670271,
  "reference_insect_endosymbiont": 0.6901892268440413
 }
]
```

## comparison_with_endosymbiosis_v1

```json
{
 "free_living_loss_vs_mitochondrion": {
  "correlation": -0.41464990417391595,
  "sign_agreement": 0.625
 },
 "parasite_loss_vs_mitochondrion": {
  "correlation": -0.127836468559092,
  "sign_agreement": 0.5
 },
 "free_living_loss_vs_plastid": {
  "correlation": 0.7092043276266634,
  "sign_agreement": 0.75
 },
 "parasite_loss_vs_plastid": {
  "correlation": 0.9043441488310411,
  "sign_agreement": 0.875
 },
 "free_living_loss_vs_insect_endosymbiont": {
  "correlation": 0.3614724983320247,
  "sign_agreement": 0.5
 },
 "parasite_loss_vs_insect_endosymbiont": {
  "correlation": 0.6612436637765676,
  "sign_agreement": 0.875
 }
}
```

## scenario_dictyostelium

```json
{
 "stay_free_living": {
  "families_now": 4504,
  "families_after": [
   4144.95,
   4189.0,
   4225.0
  ],
  "p_family_lost_by_class": {
   "redox_core": 0.238,
   "atp_synthase": 0.14775,
   "translation": 0.08553672316384181,
   "transcription": 0.037222222222222226,
   "protein_targeting": 0.16642857142857143,
   "other": 0.13444179957153057
  }
 },
 "become_parasite": {
  "families_now": 4504,
  "families_after": [
   2266.0,
   2318.0,
   2363.1
  ],
  "p_family_lost_by_class": {
   "redox_core": 0.7112499999999999,
   "atp_synthase": 0.25375000000000003,
   "translation": 0.24966101694915252,
   "transcription": 0.14866666666666667,
   "protein_targeting": 0.4573809523809524,
   "other": 0.5280516543680076
  }
 },
 "actual_Entamoeba_families": 2124
}
```

## 연결
- [[실험 목록]]
