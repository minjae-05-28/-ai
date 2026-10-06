---
유형: 실험
실행: reverse
산출: results/reverse/metrics.json
tags:
  - 유형/실험
  - 실험/reverse
---

# 실험 · reverse

**산출물** `results/reverse/metrics.json`

## 한눈에

| 항목 | 값 |
| --- | --- |
| best_mix | axis law |

## mixes

```json
[
 "prior only (no law)",
 "axis law",
 "axis + mitochondrion law",
 "axis + plastid law",
 "axis + insect-endosymbiont law",
 "plastid law only",
 "axis law, wrong lifestyle (free-living)"
]
```

## mean_auroc_recover_lost

```json
{
 "prior only (no law)": 0.7739546991419038,
 "axis law": 0.776225239283262,
 "axis + mitochondrion law": 0.7628692597773826,
 "axis + plastid law": 0.7753902446765196,
 "axis + insect-endosymbiont law": 0.7737329154326886,
 "plastid law only": 0.7725787170512277,
 "axis law, wrong lifestyle (free-living)": 0.773170953858617
}
```

## per_pair

```json
[
 {
  "pair": "Dictyostelium discoideum -> Entamoeba histolytica",
  "proxy_families": 4504,
  "descendant_families": 2124,
  "mixes": {
   "prior only (no law)": {
    "auroc_recover_lost": 0.8271177377218726,
    "estimated_families": 4111.700114900543
   },
   "axis law": {
    "auroc_recover_lost": 0.8260383557464543,
    "estimated_families": 4074.8380973452277
   },
   "axis + mitochondrion law": {
    "auroc_recover_lost": 0.8163000529587334,
    "estimated_families": 4037.591719779583
   },
   "axis + plastid law": {
    "auroc_recover_lost": 0.8252052990393555,
    "estimated_families": 4132.511477469981
   },
   "axis + insect-endosymbiont law": {
    "auroc_recover_lost": 0.8236338061883047,
    "estimated_families": 4104.016483654026
   },
   "plastid law only": {
    "auroc_recover_lost": 0.8204853039514698,
    "estimated_families": 4076.550414471629
   },
   "axis law, wrong lifestyle (free-living)": {
    "auroc_recover_lost": 0.8265582891450907,
    "estimated_families": 4135.296953336081
   }
  }
 },
 {
  "pair": "Tetrahymena thermophila -> Ichthyophthirius multifiliis",
  "proxy_families": 3427,
  "descendant_families": 2406,
  "mixes": {
   "prior only (no law)": {
    "auroc_recover_lost": 0.8307346343821277,
    "estimated_families": 4129.976502092314
   },
   "axis law": {
    "auroc_recover_lost": 0.8273552322024682,
    "estimated_families": 4109.6306676199965
   },
   "axis + mitochondrion law": {
    "auroc_recover_lost": 0.8257859585290697,
    "estimated_families": 4064.950564030154
   },
   "axis + plastid law": {
    "auroc_recover_lost": 0.8279792598145099,
    "estimated_families": 4114.597635774201
   },
   "axis + insect-endosymbiont law": {
    "auroc_recover_lost": 0.8258998364877724,
    "estimated_families": 4099.4967510855295
   },
   "plastid law only": {
    "auroc_recover_lost": 0.8274345337446943,
    "estimated_families": 4107.330609529014
   },
   "axis law, wrong lifestyle (free-living)": {
    "auroc_recover_lost": 0.829108952766491,
    "estimated_families": 4154.355358617861
   }
  }
 },
 {
  "pair": "Tetrahymena thermophila -> Perkinsus marinus",
  "proxy_families": 3427,
  "descendant_families": 3123,
  "mixes": {
   "prior only (no law)": {
    "auroc_recover_lost": 0.8137951381485162,
    "estimated_families": 4180.210745440713
   },
   "axis law": {
    "auroc_recover_lost": 0.8132803081202066,
    "estimated_families": 4220.9244160205335
   },
   "axis + mitochondrion law": {
    "auroc_recover_lost": 0.8081207429966889,
    "estimated_families": 4175.909967798944
   },
   "axis + plastid law": {
    "auroc_recover_lost": 0.8127783521952358,
    "estimated_families": 4218.146755523894
   },
   "axis + insect-endosymbiont law": {
    "auroc_recover_lost": 0.8111151789701522,
    "estimated_families": 4191.693086874402
   },
   "plastid law only": {
    "auroc_recover_lost": 0.8114177203986144,
    "estimated_families": 4187.577006860491
   },
   "axis law, wrong lifestyle (free-living)": {
    "auroc_recover_lost": 0.8122250339621528,
    "estimated_families": 4207.355141084134
   }
  }
 },
 {
  "pair": "Chromera velia -> Plasmodium falciparum",
  "proxy_families": 4095,
  "descendant_families": 2383,
  "mixes": {
   "prior only (no law)": {
    "auroc_recover_lost": 0.7466850757009498,
    "estimated_families": 4161.8773727562875
   },
   "axis law": {
    "auroc_recover_lost": 0.7522140256071187,
    "estimated_families": 4190.253531350563
   },
   "axis + mitochondrion law": {
    "auroc_recover_lost": 0.7359177844553678,
    "estimated_families": 4118.908061096561
   },
   "axis + plastid law": {
    "auroc_recover_lost": 0.7507401123160513,
    "estimated_families": 4186.520722041376
   },
   "axis + insect-endosymbiont law": {
    "auroc_recover_lost": 0.7490250053897418,
    "estimated_families": 4173.917707609457
   },
   "plastid law only": {
    "auroc_recover_lost": 0.7471414286896637,
    "estimated_families": 4170.4615598103355
   },
   "axis law, wrong lifestyle (free-living)": {
    "auroc_recover_lost": 0.747308392347958,
    "estimated_families": 4184.1448799081345
   }
  }
 },
 {
  "pair": "Chromera velia -> Babesia bovis",
  "proxy_families": 4095,
  "descendant_families": 1999,
  "mixes": {
   "prior only (no law)": {
    "auroc_recover_lost": 0.7649259490280563,
    "estimated_families": 4185.546324912662
   },
   "axis law": {
    "auroc_recover_lost": 0.7703078496201052,
    "estimated_families": 4220.558809936287
   },
   "axis + mitochondrion law": {
    "auroc_recover_lost": 0.754707637660499,
    "estimated_families": 4133.206238206275
   },
   "axis + plastid law": {
    "auroc_recover_lost": 0.769041198989691,
    "estimated_families": 4218.510341502535
   },
   "axis + insect-endosymbiont law": {
    "auroc_recover_lost": 0.76789620052493,
    "estimated_families": 4210.061182664975
   },
   "plastid law only": {
    "auroc_recover_lost": 0.7652076186503874,
    "estimated_families": 4201.933606471124
   },
   "axis law, wrong lifestyle (free-living)": {
    "auroc_recover_lost": 0.7658613029793927,
    "estimated_families": 4212.240376379988
   }
  }
 },
 {
  "pair": "Chromera velia -> Toxoplasma gondii",
  "proxy_families": 4095,
  "descendant_families": 2912,
  "mixes": {
   "prior only (no law)": {
    "auroc_recover_lost": 0.6928289841116996,
    "estimated_families": 4015.602428992677
   },
   "axis law": {
    "auroc_recover_lost": 0.7011922965816081,
    "estimated_families": 4040.072768665863
   },
   "axis + mitochondrion law": {
    "auroc_recover_lost": 0.6780927298988927,
    "estimated_families": 3990.76127987491
   },
   "axis + plastid law": {
    "auroc_recover_lost": 0.6987510832932113,
    "estimated_families": 4034.614525851802
   },
   "axis + insect-endosymbiont law": {
    "auroc_recover_lost": 0.6970297544535388,
    "estimated_families": 4022.7761533818884
   },
   "plastid law only": {
    "auroc_recover_lost": 0.6927212325469427,
    "estimated_families": 4019.3674012910606
  
… (잘림, 원본 파일 참조)
```

## reconstructions

```json
{
 "Entamoeba histolytica": {
  "proxy": "Dictyostelium discoideum",
  "families_today": 2124,
  "estimated_ancestor_families": 4144.684947949594,
  "proxy_families": 4504,
  "estimated_lost": 2028.0340922630705,
  "top_recovered": [
   {
    "family": "COX15-CtaA",
    "description": "Cytochrome oxidase assembly protein",
    "class": "redox_core",
    "p_ancestral": 0.9671041807630966
   },
   {
    "family": "Cmc1",
    "description": "Cytochrome c oxidase biogenesis protein Cmc1 like",
    "class": "redox_core",
    "p_ancestral": 0.9649646464517977
   },
   {
    "family": "Rieske",
    "description": "Rieske [2Fe-2S] domain",
    "class": "redox_core",
    "p_ancestral": 0.9599849177440175
   },
   {
    "family": "RPN7_PSMD6_C",
    "description": "26S proteasome regulatory subunit RPN7/PSMD6 C-terminal helix",
    "class": "other",
    "p_ancestral": 0.953061826679111
   },
   {
    "family": "HEAT_PBS",
    "description": "PBS lyase HEAT-like repeat",
    "class": "other",
    "p_ancestral": 0.9516996451950113
   },
   {
    "family": "CRM1_repeat_3",
    "description": "CRM1 / Exportin repeat 3",
    "class": "other",
    "p_ancestral": 0.9513755616130708
   },
   {
    "family": "zf-DPOE",
    "description": "Zinc finger domain of DNA polymerase-epsilon",
    "class": "other",
    "p_ancestral": 0.95086295020508
   },
   {
    "family": "TPR_SYVN1_N",
    "description": "E3 ubiquitin-protein ligase synoviolin-like, TPR repeats",
    "class": "other",
    "p_ancestral": 0.9507017072750894
   }
  ],
  "by_class": {
   "redox_core": {
    "ancestor": 32.72822010438208,
    "today": 0
   },
   "atp_synthase": {
    "ancestor": 15.867432702676437,
    "today": 9
   },
   "translation": {
    "ancestor": 162.02113727040134,
    "today": 133
   },
   "transcription": {
    "ancestor": 36.91068610823244,
    "today": 32
   },
   "protein_targeting": {
    "ancestor": 19.594898800164724,
    "today": 11
   }
  }
 },
 "Ichthyophthirius multifiliis": {
  "proxy": "Tetrahymena thermophila",
  "families_today": 2406,
  "estimated_ancestor_families": 4139.341214808561,
  "proxy_families": 3427,
  "estimated_lost": 1740.0186280482499,
  "top_recovered": [
   {
    "family": "UPF0220",
    "description": "Uncharacterised protein family (UPF0220)",
    "class": "other",
    "p_ancestral": 0.9504068845087832
   },
   {
    "family": "ORMDL",
    "description": "ORMDL family",
    "class": "other",
    "p_ancestral": 0.9490141492969583
   },
   {
    "family": "SYS1",
    "description": "Integral membrane protein S linking to the trans Golgi network",
    "class": "other",
    "p_ancestral": 0.948994545456277
   },
   {
    "family": "ATG9",
    "description": "Autophagy protein ATG9",
    "class": "other",
    "p_ancestral": 0.9479572784169013
   },
   {
    "family": "Clp1",
    "description": "Pre-mRNA cleavage complex II protein Clp1",
    "class": "other",
    "p_ancestral": 0.9451347123706548
   },
   {
    "family": "Vac14_Fig4_bd",
    "description": "Vacuolar protein 14 C-terminal Fig4p binding",
    "class": "other",
    "p_ancestral": 0.9442229974072609
   },
   {
    "family": "ARM_TBCD",
    "description": "Tubulin-specific chaperone D-like, ARM repeat",
    "class": "other",
    "p_ancestral": 0.9439676820250927
   },
   {
    "family": "RRP40_S1",
    "description": "Exosome complex component RRP40, S1 domain",
    "class": "other",
    "p_ancestral": 0.9438808291750459
   }
  ],
  "by_class": {
   "redox_core": {
    "ancestor": 27.250288662642937,
    "today": 13
   },
   "atp_synthase": {
    "ancestor": 15.477232554062285,
    "today": 13
   },
   "translation": {
    "ancestor": 162.5222904923966,
    "today": 143
   },
   "transcription": {
    "ancestor": 35.94015888374123,
    "today": 27
   },
   "protein_targeting": {
    "ancestor": 19.353094924258244,
    "today": 13
   }
  }
 },
 "Perkinsus marinus": {
  "proxy": "Tetrahymena thermophila",
  "families_today": 3123,
  "estimated_ancestor_families": 4223.467451518414,
  "proxy_families": 3427,
  "estimated_lost": 1109.6677068199215,
  "top_recovered": [
   {
    "family": "Rft-1",
    "description": "Rft protein",
    "class": "other",
    "p_ancestral": 0.929554957054332
   },
   {
    "family": "UPF0220",
    "description": "Uncharacterised protein family (UPF0220)",
    "class": "other",
    "p_ancestral": 0.9276666791999387
   },
   {
    "family": "ORMDL",
    "description": "ORMDL family",
    "class": "other",
    "p_ancestral": 0.9269653039611347
   },
   {
    "family": "Clp1",
    "description": "Pre-mRNA cleavage complex II protein Clp1",
    "class": "other",
    "p_ancestral": 0.9238633872455739
   },
   {
    "family": "TPR_ANAPC2",
    "description": "ANAPC2-like, TPR repeats",
    "class": "other",
    "p_ancestral": 0.9231598421821109
   },
   {
    "family": "zf-DPOE",
    "description": "Zinc finger domain of DNA polymerase-epsilon",
    "class": "other",
    "p_ancestral": 0.9209187868389337
   },
   {
    "family": "VPS11_N",
    "description": "VPS11-like, N-terminal beta-propeller",
    "class": "other",
    "p_ancestral": 0.9208656056453518
   },
   {
    "family": "Thioredoxin_13",
    "description": "Thioredoxin-like domain",
    "class": "other",
    "p_ancestral": 0.9205145822857006
   }
  ],
  "by_class": {
   "redox_core": {
    "ancestor": 29.703224397894715,
    "today": 17
   },
   "atp_synthase": {
    "ancestor": 16.191112341816478,
    "today": 15
   },
   "translation": {
    "ancestor": 169.08197002810988,
    "today": 158
   },
   "transcription": {
    "ancestor": 37.665341779619425,
    "today": 35
   },
   "protein_targeting": {
    "ancestor": 19.79029406266334,
    "today": 16
   }
  }
 },
 "Plasmodium falciparum": {
  "proxy": "Chromera velia",
  "families_today": 2383,
  "estimated_ancestor_families": 4190.355849042582,
  "proxy_families": 4095,
  "estimated_lost": 1913.7959151776022,
  "top_recovered": [
   {
    "family": "UPF0220",
    "description": "Uncharacterised prot
… (잘림, 원본 파일 참조)
```

## 연결
- [[실험 목록]]
