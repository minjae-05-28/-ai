---
유형: 실험
실행: mars_random
산출: results/mars_random/metrics.json
tags:
  - 유형/실험
  - 실험/mars_random
---

# 실험 · mars_random

**산출물** `results/mars_random/metrics.json`

## 한눈에

| 항목 | 값 |
| --- | --- |
| driver_scenario | isolated_abrupt |

## environments

```json
{
 "Earth soil": {
  "temp_c": 20.0,
  "salt_pct": 1.0,
  "o2_pal": 1.0,
  "radiation_x": 1.0,
  "organics": 1.0,
  "h2": 0.2,
  "perchlorate": 0.0,
  "light": 0.3
 },
 "early Mars lake (~3.8 Gya)": {
  "temp_c": 10.0,
  "salt_pct": 3.0,
  "o2_pal": 0.0,
  "radiation_x": 10.0,
  "organics": 0.3,
  "h2": 0.6,
  "perchlorate": 0.1,
  "light": 0.5
 },
 "present Mars subsurface brine": {
  "temp_c": -15.0,
  "salt_pct": 25.0,
  "o2_pal": 0.001,
  "radiation_x": 30.0,
  "organics": 0.01,
  "h2": 0.3,
  "perchlorate": 1.0,
  "light": 0.0
 }
}
```

## start_genome

```json
{
 "replication": 30,
 "transcription": 20,
 "translation": 120,
 "membrane": 20,
 "cell_division": 8,
 "chaperones": 10,
 "regulation": 10,
 "unknown": 30,
 "fermentation": 4,
 "aerobic_respiration": 0,
 "h2_oxidation": 8,
 "carbon_fixation": 15,
 "photosynthesis": 0,
 "perchlorate_reduction": 0,
 "transporters": 25,
 "amino_acid_synthesis": 30,
 "nucleotide_synthesis": 15,
 "cofactor_synthesis": 15,
 "cold_adaptation": 2,
 "osmoprotection": 1,
 "dna_repair": 15,
 "oxidative_stress": 2,
 "pigments_uv": 0,
 "dormancy": 0,
 "motility": 10
}
```

## summary

```json
{
 "gradual": {
  "n_laws": 200,
  "survived": 200,
  "survival_rate": 1.0,
  "median_genes": 480.2033333333333,
  "modules": {
   "replication": {
    "median": 23.445,
    "share_grew": 0.34,
    "share_shrank": 0.605
   },
   "transcription": {
    "median": 14.528333333333332,
    "share_grew": 0.37,
    "share_shrank": 0.58
   },
   "translation": {
    "median": 96.92,
    "share_grew": 0.38,
    "share_shrank": 0.585
   },
   "membrane": {
    "median": 14.123333333333333,
    "share_grew": 0.285,
    "share_shrank": 0.605
   },
   "cell_division": {
    "median": 5.968333333333334,
    "share_grew": 0.26,
    "share_shrank": 0.515
   },
   "chaperones": {
    "median": 6.425,
    "share_grew": 0.19,
    "share_shrank": 0.625
   },
   "regulation": {
    "median": 6.92,
    "share_grew": 0.315,
    "share_shrank": 0.56
   },
   "unknown": {
    "median": 6.543333333333333,
    "share_grew": 0.025,
    "share_shrank": 0.955
   },
   "fermentation": {
    "median": 5.073333333333334,
    "share_grew": 0.47,
    "share_shrank": 0.34
   },
   "aerobic_respiration": {
    "median": 1.0783333333333331,
    "share_grew": 0.405,
    "share_shrank": 0.0
   },
   "h2_oxidation": {
    "median": 9.055,
    "share_grew": 0.415,
    "share_shrank": 0.0
   },
   "carbon_fixation": {
    "median": 15.968333333333334,
    "share_grew": 0.425,
    "share_shrank": 0.0
   },
   "photosynthesis": {
    "median": 1.0266666666666668,
    "share_grew": 0.4,
    "share_shrank": 0.0
   },
   "perchlorate_reduction": {
    "median": 7.171666666666667,
    "share_grew": 1.0,
    "share_shrank": 0.0
   },
   "transporters": {
    "median": 17.748333333333335,
    "share_grew": 0.35,
    "share_shrank": 0.595
   },
   "amino_acid_synthesis": {
    "median": 25.911666666666665,
    "share_grew": 0.375,
    "share_shrank": 0.57
   },
   "nucleotide_synthesis": {
    "median": 13.671666666666667,
    "share_grew": 0.35,
    "share_shrank": 0.445
   },
   "cofactor_synthesis": {
    "median": 12.801666666666666,
    "share_grew": 0.325,
    "share_shrank": 0.525
   },
   "cold_adaptation": {
    "median": 9.8,
    "share_grew": 1.0,
    "share_shrank": 0.0
   },
   "osmoprotection": {
    "median": 11.116666666666667,
    "share_grew": 1.0,
    "share_shrank": 0.0
   },
   "dna_repair": {
    "median": 30.34166666666667,
    "share_grew": 0.8,
    "share_shrank": 0.125
   },
   "oxidative_stress": {
    "median": 9.158333333333333,
    "share_grew": 0.97,
    "share_shrank": 0.005
   },
   "pigments_uv": {
    "median": 6.093333333333334,
    "share_grew": 0.815,
    "share_shrank": 0.0
   },
   "dormancy": {
    "median": 15.399999999999999,
    "share_grew": 0.88,
    "share_shrank": 0.0
   },
   "motility": {
    "median": 5.965,
    "share_grew": 0.305,
    "share_shrank": 0.555
   }
  }
 },
 "abrupt": {
  "n_laws": 200,
  "survived": 200,
  "survival_rate": 1.0,
  "median_genes": 512.4933333333333,
  "modules": {
   "replication": {
    "median": 23.60333333333333,
    "share_grew": 0.335,
    "share_shrank": 0.59
   },
   "transcription": {
    "median": 15.27,
    "share_grew": 0.39,
    "share_shrank": 0.555
   },
   "translation": {
    "median": 107.16499999999999,
    "share_grew": 0.445,
    "share_shrank": 0.53
   },
   "membrane": {
    "median": 14.398333333333333,
    "share_grew": 0.33,
    "share_shrank": 0.595
   },
   "cell_division": {
    "median": 6.096666666666667,
    "share_grew": 0.3,
    "share_shrank": 0.485
   },
   "chaperones": {
    "median": 6.621666666666667,
    "share_grew": 0.23,
    "share_shrank": 0.6
   },
   "regulation": {
    "median": 7.995,
    "share_grew": 0.345,
    "share_shrank": 0.505
   },
   "unknown": {
    "median": 9.081666666666667,
    "share_grew": 0.07,
    "share_shrank": 0.855
   },
   "fermentation": {
    "median": 4.984999999999999,
    "share_grew": 0.46,
    "share_shrank": 0.29
   },
   "aerobic_respiration": {
    "median": 1.0066666666666666,
    "share_grew": 0.385,
    "share_shrank": 0.0
   },
   "h2_oxidation": {
    "median": 9.035,
    "share_grew": 0.41,
    "share_shrank": 0.0
   },
   "carbon_fixation": {
    "median": 16.781666666666666,
    "share_grew": 0.48,
    "share_shrank": 0.0
   },
   "photosynthesis": {
    "median": 1.0,
    "share_grew": 0.405,
    "share_shrank": 0.0
   },
   "perchlorate_reduction": {
    "median": 7.0649999999999995,
    "share_grew": 1.0,
    "share_shrank": 0.0
   },
   "transporters": {
    "median": 18.753333333333334,
    "share_grew": 0.355,
    "share_shrank": 0.59
   },
   "amino_acid_synthesis": {
    "median": 26.686666666666667,
    "share_grew": 0.395,
    "share_shrank": 0.54
   },
   "nucleotide_synthesis": {
    "median": 13.7,
    "share_grew": 0.395,
    "share_shrank": 0.445
   },
   "cofactor_synthesis": {
    "median": 12.998333333333333,
    "share_grew": 0.31,
    "share_shrank": 0.505
   },
   "cold_adaptation": {
    "median": 9.511666666666667,
    "share_grew": 1.0,
    "share_shrank": 0.0
   },
   "osmoprotection": {
    "median": 11.343333333333334,
    "share_grew": 1.0,
    "share_shrank": 0.0
   },
   "dna_repair": {
    "median": 30.321666666666665,
    "share_grew": 0.8,
    "share_shrank": 0.13
   },
   "oxidative_stress": {
    "median": 9.003333333333334,
    "share_grew": 0.955,
    "share_shrank": 0.005
   },
   "pigments_uv": {
    "median": 6.073333333333334,
    "share_grew": 0.83,
    "share_shrank": 0.0
   },
   "dormancy": {
    "median": 15.673333333333334,
    "share_grew": 0.91,
    "share_shrank": 0.0
   },
   "motility": {
    "median": 7.38,
    "share_grew": 0.355,
    "share_shrank": 0.515
   }
  }
 },
 "earth": {
  "n_laws": 100,
  "survived": 100,
  "survival_rate": 1.0,
  "median_genes": 403.03666666666663,
  "modules": {
   "replication": {
    "median": 22.431666666666665,
    "share_grew": 0.29,
    "share_shrank": 0.62
   },
   "transcription": {
    "median": 13.403333333333332,
    "share_grew": 0.19,
    "share_shrank": 0.74
   },
   "transl
… (잘림, 원본 파일 참조)
```

## modules

```json
[
 {
  "module": "dna_repair",
  "start": 15,
  "mars_median": 30.34166666666667,
  "earth_median": 9.723333333333333,
  "mars_grew": 0.8,
  "mars_shrank": 0.125,
  "earth_grew": 0.36,
  "earth_shrank": 0.61
 },
 {
  "module": "cold_adaptation",
  "start": 2,
  "mars_median": 9.8,
  "earth_median": 2.331666666666667,
  "mars_grew": 1.0,
  "mars_shrank": 0.0,
  "earth_grew": 0.39,
  "earth_shrank": 0.15
 },
 {
  "module": "fermentation",
  "start": 4,
  "mars_median": 5.073333333333334,
  "earth_median": 13.061666666666667,
  "mars_grew": 0.47,
  "mars_shrank": 0.34,
  "earth_grew": 0.9,
  "earth_shrank": 0.04
 },
 {
  "module": "perchlorate_reduction",
  "start": 0,
  "mars_median": 7.171666666666667,
  "earth_median": 0.7116666666666667,
  "mars_grew": 1.0,
  "mars_shrank": 0.0,
  "earth_grew": 0.31,
  "earth_shrank": 0.0
 },
 {
  "module": "carbon_fixation",
  "start": 15,
  "mars_median": 15.968333333333334,
  "earth_median": 11.188333333333333,
  "mars_grew": 0.425,
  "mars_shrank": 0.0,
  "earth_grew": 0.36,
  "earth_shrank": 0.56
 },
 {
  "module": "dormancy",
  "start": 0,
  "mars_median": 15.399999999999999,
  "earth_median": 0.7516666666666667,
  "mars_grew": 0.88,
  "mars_shrank": 0.0,
  "earth_grew": 0.31,
  "earth_shrank": 0.0
 },
 {
  "module": "h2_oxidation",
  "start": 8,
  "mars_median": 9.055,
  "earth_median": 7.506666666666667,
  "mars_grew": 0.415,
  "mars_shrank": 0.0,
  "earth_grew": 0.38,
  "earth_shrank": 0.42
 },
 {
  "module": "pigments_uv",
  "start": 0,
  "mars_median": 6.093333333333334,
  "earth_median": 0.7933333333333333,
  "mars_grew": 0.815,
  "mars_shrank": 0.0,
  "earth_grew": 0.36,
  "earth_shrank": 0.0
 },
 {
  "module": "cell_division",
  "start": 8,
  "mars_median": 5.968333333333334,
  "earth_median": 8.030000000000001,
  "mars_grew": 0.26,
  "mars_shrank": 0.515,
  "earth_grew": 0.41,
  "earth_shrank": 0.3
 },
 {
  "module": "transcription",
  "start": 20,
  "mars_median": 14.528333333333332,
  "earth_median": 13.403333333333332,
  "mars_grew": 0.37,
  "mars_shrank": 0.58,
  "earth_grew": 0.19,
  "earth_shrank": 0.74
 },
 {
  "module": "osmoprotection",
  "start": 1,
  "mars_median": 11.116666666666667,
  "earth_median": 6.62,
  "mars_grew": 1.0,
  "mars_shrank": 0.0,
  "earth_grew": 0.71,
  "earth_shrank": 0.0
 },
 {
  "module": "translation",
  "start": 120,
  "mars_median": 96.92,
  "earth_median": 82.37333333333333,
  "mars_grew": 0.38,
  "mars_shrank": 0.585,
  "earth_grew": 0.29,
  "earth_shrank": 0.7
 },
 {
  "module": "motility",
  "start": 10,
  "mars_median": 5.965,
  "earth_median": 8.048333333333334,
  "mars_grew": 0.305,
  "mars_shrank": 0.555,
  "earth_grew": 0.38,
  "earth_shrank": 0.48
 },
 {
  "module": "membrane",
  "start": 20,
  "mars_median": 14.123333333333333,
  "earth_median": 15.65,
  "mars_grew": 0.285,
  "mars_shrank": 0.605,
  "earth_grew": 0.37,
  "earth_shrank": 0.56
 },
 {
  "module": "chaperones",
  "start": 10,
  "mars_median": 6.425,
  "earth_median": 7.973333333333333,
  "mars_grew": 0.19,
  "mars_shrank": 0.625,
  "earth_grew": 0.21,
  "earth_shrank": 0.52
 },
 {
  "module": "transporters",
  "start": 25,
  "mars_median": 17.748333333333335,
  "earth_median": 21.388333333333335,
  "mars_grew": 0.35,
  "mars_shrank": 0.595,
  "earth_grew": 0.41,
  "earth_shrank": 0.53
 },
 {
  "module": "nucleotide_synthesis",
  "start": 15,
  "mars_median": 13.671666666666667,
  "earth_median": 13.068333333333333,
  "mars_grew": 0.35,
  "mars_shrank": 0.445,
  "earth_grew": 0.3,
  "earth_shrank": 0.48
 },
 {
  "module": "regulation",
  "start": 10,
  "mars_median": 6.92,
  "earth_median": 7.176666666666667,
  "mars_grew": 0.315,
  "mars_shrank": 0.56,
  "earth_grew": 0.36,
  "earth_shrank": 0.53
 },
 {
  "module": "replication",
  "start": 30,
  "mars_median": 23.445,
  "earth_median": 22.431666666666665,
  "mars_grew": 0.34,
  "mars_shrank": 0.605,
  "earth_grew": 0.29,
  "earth_shrank": 0.62
 },
 {
  "module": "aerobic_respiration",
  "start": 0,
  "mars_median": 1.0783333333333331,
  "earth_median": 1.0550000000000002,
  "mars_grew": 0.405,
  "mars_shrank": 0.0,
  "earth_grew": 0.36,
  "earth_shrank": 0.0
 },
 {
  "module": "oxidative_stress",
  "start": 2,
  "mars_median": 9.158333333333333,
  "earth_median": 9.57,
  "mars_grew": 0.97,
  "mars_shrank": 0.005,
  "earth_grew": 1.0,
  "earth_shrank": 0.0
 },
 {
  "module": "amino_acid_synthesis",
  "start": 30,
  "mars_median": 25.911666666666665,
  "earth_median": 25.685,
  "mars_grew": 0.375,
  "mars_shrank": 0.57,
  "earth_grew": 0.34,
  "earth_shrank": 0.57
 },
 {
  "module": "cofactor_synthesis",
  "start": 15,
  "mars_median": 12.801666666666666,
  "earth_median": 12.89,
  "mars_grew": 0.325,
  "mars_shrank": 0.525,
  "earth_grew": 0.35,
  "earth_shrank": 0.52
 },
 {
  "module": "unknown",
  "start": 30,
  "mars_median": 6.543333333333333,
  "earth_median": 7.223333333333333,
  "mars_grew": 0.025,
  "mars_shrank": 0.955,
  "earth_grew": 0.01,
  "earth_shrank": 0.95
 },
 {
  "module": "photosynthesis",
  "start": 0,
  "mars_median": 1.0266666666666668,
  "earth_median": 1.0,
  "mars_grew": 0.4,
  "mars_shrank": 0.0,
  "earth_grew": 0.4,
  "earth_shrank": 0.0
 }
]
```

## survival_drivers

```json
[
 {
  "kind": "dup",
  "module": "osmoprotection",
  "stress": "cold",
  "corr_with_survival": 0.29036283716451616
 },
 {
  "kind": "dup",
  "module": "cold_adaptation",
  "stress": "salt",
  "corr_with_survival": 0.24262711549561736
 },
 {
  "kind": "dup",
  "module": "osmoprotection",
  "stress": "radiation",
  "corr_with_survival": 0.24027890253979983
 },
 {
  "kind": "gain",
  "module": "transcription",
  "stress": "perchlorate",
  "corr_with_survival": 0.23561352463503865
 },
 {
  "kind": "loss",
  "module": "dormancy",
  "stress": "perchlorate",
  "corr_with_survival": 0.21199374705918378
 },
 {
  "kind": "loss",
  "module": "cofactor_synthesis",
  "stress": "perchlorate",
  "corr_with_survival": -0.1945889696996323
 },
 {
  "kind": "gain",
  "module": "nucleotide_synthesis",
  "stress": "salt",
  "corr_with_survival": -0.19269806940551365
 },
 {
  "kind": "gain",
  "module": "membrane",
  "stress": "radiation",
  "corr_with_survival": 0.18935144454016498
 },
 {
  "kind": "gain",
  "module": "transcription",
  "stress": "light",
  "corr_with_survival": 0.18777995126545077
 },
 {
  "kind": "dup",
  "module": "perchlorate_reduction",
  "stress": "radiation",
  "corr_with_survival": 0.18490243344203725
 },
 {
  "kind": "gain",
  "module": "cofactor_synthesis",
  "stress": "light",
  "corr_with_survival": 0.1803413453417155
 },
 {
  "kind": "dup",
  "module": "cold_adaptation",
  "stress": "cold",
  "corr_with_survival": 0.1744001500252967
 },
 {
  "kind": "loss",
  "module": "dna_repair",
  "stress": "light",
  "corr_with_survival": 0.17373871467072624
 },
 {
  "kind": "gain",
  "module": "cofactor_synthesis",
  "stress": "o2",
  "corr_with_survival": 0.17313542589092923
 },
 {
  "kind": "dup",
  "module": "regulation",
  "stress": "radiation",
  "corr_with_survival": 0.17144346429559912
 },
 {
  "kind": "dup",
  "module": "translation",
  "stress": "o2",
  "corr_with_survival": -0.1657895265730182
 },
 {
  "kind": "dup",
  "module": "pigments_uv",
  "stress": "h2",
  "corr_with_survival": 0.15798350173322917
 },
 {
  "kind": "gain",
  "module": "osmoprotection",
  "stress": "radiation",
  "corr_with_survival": 0.1575854435433286
 },
 {
  "kind": "gain",
  "module": "unknown",
  "stress": "light",
  "corr_with_survival": -0.15591100991728102
 },
 {
  "kind": "dup",
  "module": "nucleotide_synthesis",
  "stress": "salt",
  "corr_with_survival": -0.15374250241210857
 },
 {
  "kind": "dup",
  "module": "regulation",
  "stress": "organics",
  "corr_with_survival": 0.15079952655308673
 },
 {
  "kind": "dup",
  "module": "osmoprotection",
  "stress": "perchlorate",
  "corr_with_survival": 0.1505510085571555
 },
 {
  "kind": "loss",
  "module": "cell_division",
  "stress": "light",
  "corr_with_survival": -0.1501067043960787
 },
 {
  "kind": "dup",
  "module": "unknown",
  "stress": "h2",
  "corr_with_survival": -0.14865011060950453
 },
 {
  "kind": "loss",
  "module": "carbon_fixation",
  "stress": "organics",
  "corr_with_survival": 0.14736458434044078
 },
 {
  "kind": "gain",
  "module": "oxidative_stress",
  "stress": "radiation",
  "corr_with_survival": 0.14717781831825835
 },
 {
  "kind": "gain",
  "module": "photosynthesis",
  "stress": "h2",
  "corr_with_survival": -0.14598005331878725
 },
 {
  "kind": "gain",
  "module": "translation",
  "stress": "perchlorate",
  "corr_with_survival": -0.14588928389506337
 },
 {
  "kind": "dup",
  "module": "osmoprotection",
  "stress": "salt",
  "corr_with_survival": 0.14533164223026154
 },
 {
  "kind": "loss",
  "module": "oxidative_stress",
  "stress": "light",
  "corr_with_survival": -0.14521846593437246
 }
]
```

## extinctions

```json
[
 {
  "scenario": "isolated_gradual",
  "seed": 197,
  "at": 4894
 },
 {
  "scenario": "isolated_abrupt",
  "seed": 0,
  "at": 404
 },
 {
  "scenario": "isolated_abrupt",
  "seed": 4,
  "at": 484
 },
 {
  "scenario": "isolated_abrupt",
  "seed": 5,
  "at": 448
 },
 {
  "scenario": "isolated_abrupt",
  "seed": 6,
  "at": 485
 },
 {
  "scenario": "isolated_abrupt",
  "seed": 7,
  "at": 377
 },
 {
  "scenario": "isolated_abrupt",
  "seed": 9,
  "at": 486
 },
 {
  "scenario": "isolated_abrupt",
  "seed": 16,
  "at": 486
 },
 {
  "scenario": "isolated_abrupt",
  "seed": 18,
  "at": 402
 },
 {
  "scenario": "isolated_abrupt",
  "seed": 22,
  "at": 483
 },
 {
  "scenario": "isolated_abrupt",
  "seed": 23,
  "at": 598
 },
 {
  "scenario": "isolated_abrupt",
  "seed": 24,
  "at": 393
 },
 {
  "scenario": "isolated_abrupt",
  "seed": 29,
  "at": 452
 },
 {
  "scenario": "isolated_abrupt",
  "seed": 32,
  "at": 490
 },
 {
  "scenario": "isolated_abrupt",
  "seed": 35,
  "at": 477
 },
 {
  "scenario": "isolated_abrupt",
  "seed": 37,
  "at": 573
 },
 {
  "scenario": "isolated_abrupt",
  "seed": 38,
  "at": 505
 },
 {
  "scenario": "isolated_abrupt",
  "seed": 46,
  "at": 413
 },
 {
  "scenario": "isolated_abrupt",
  "seed": 47,
  "at": 588
 },
 {
  "scenario": "isolated_abrupt",
  "seed": 50,
  "at": 432
 },
 {
  "scenario": "isolated_abrupt",
  "seed": 55,
  "at": 399
 },
 {
  "scenario": "isolated_abrupt",
  "seed": 60,
  "at": 473
 },
 {
  "scenario": "isolated_abrupt",
  "seed": 61,
  "at": 398
 },
 {
  "scenario": "isolated_abrupt",
  "seed": 63,
  "at": 507
 },
 {
  "scenario": "isolated_abrupt",
  "seed": 69,
  "at": 541
 },
 {
  "scenario": "isolated_abrupt",
  "seed": 70,
  "at": 584
 },
 {
  "scenario": "isolated_abrupt",
  "seed": 71,
  "at": 585
 },
 {
  "scenario": "isolated_abrupt",
  "seed": 72,
  "at": 420
 },
 {
  "scenario": "isolated_abrupt",
  "seed": 73,
  "at": 495
 },
 {
  "scenario": "isolated_abrupt",
  "seed": 75,
  "at": 506
 },
 {
  "scenario": "isolated_abrupt",
  "seed": 76,
  "at": 553
 },
 {
  "scenario": "isolated_abrupt",
  "seed": 84,
  "at": 456
 },
 {
  "scenario": "isolated_abrupt",
  "seed": 90,
  "at": 432
 },
 {
  "scenario": "isolated_abrupt",
  "seed": 92,
  "at": 575
 },
 {
  "scenario": "isolated_abrupt",
  "seed": 93,
  "at": 522
 },
 {
  "scenario": "isolated_abrupt",
  "seed": 95,
  "at": 448
 },
 {
  "scenario": "isolated_abrupt",
  "seed": 96,
  "at": 494
 },
 {
  "scenario": "isolated_abrupt",
  "seed": 97,
  "at": 586
 },
 {
  "scenario": "isolated_abrupt",
  "seed": 99,
  "at": 388
 },
 {
  "scenario": "isolated_abrupt",
  "seed": 104,
  "at": 393
 },
 {
  "scenario": "isolated_abrupt",
  "seed": 105,
  "at": 599
 },
 {
  "scenario": "isolated_abrupt",
  "seed": 114,
  "at": 375
 },
 {
  "scenario": "isolated_abrupt",
  "seed": 118,
  "at": 477
 },
 {
  "scenario": "isolated_abrupt",
  "seed": 119,
  "at": 337
 },
 {
  "scenario": "isolated_abrupt",
  "seed": 121,
  "at": 582
 },
 {
  "scenario": "isolated_abrupt",
  "seed": 125,
  "at": 409
 },
 {
  "scenario": "isolated_abrupt",
  "seed": 126,
  "at": 523
 },
 {
  "scenario": "isolated_abrupt",
  "seed": 128,
  "at": 495
 },
 {
  "scenario": "isolated_abrupt",
  "seed": 133,
  "at": 543
 },
 {
  "scenario": "isolated_abrupt",
  "seed": 141,
  "at": 502
 },
 {
  "scenario": "isolated_abrupt",
  "seed": 142,
  "at": 391
 },
 {
  "scenario": "isolated_abrupt",
  "seed": 143,
  "at": 381
 },
 {
  "scenario": "isolated_abrupt",
  "seed": 144,
  "at": 491
 },
 {
  "scenario": "isolated_abrupt",
  "seed": 145,
  "at": 388
 },
 {
  "scenario": "isolated_abrupt",
  "seed": 147,
  "at": 351
 },
 {
  "scenario": "isolated_abrupt",
  "seed": 151,
  "at": 553
 },
 {
  "scenario": "isolated_abrupt",
  "seed": 154,
  "at": 502
 },
 {
  "scenario": "isolated_abrupt",
  "seed": 158,
  "at": 465
 },
 {
  "scenario": "isolated_abrupt",
  "seed": 166,
  "at": 504
 },
 {
  "scenario": "isolated_abrupt",
  "seed": 167,
  "at": 508
 },
 {
  "scenario": "isolated_abrupt",
  "seed": 169,
  "at": 532
 },
 {
  "scenario": "isolated_abrupt",
  "seed": 170,
  "at": 518
 },
 {
  "scenario": "isolated_abrupt",
  "seed": 182,
  "at": 357
 },
 {
  "scenario": "isolated_abrupt",
  "seed": 183,
  "at": 383
 },
 {
  "scenario": "isolated_abrupt",
  "seed": 186,
  "at": 360
 },
 {
  "scenario": "isolated_abrupt",
  "seed": 187,
  "at": 460
 },
 {
  "scenario": "isolated_abrupt",
  "seed": 188,
  "at": 462
 },
 {
  "scenario": "isolated_abrupt",
  "seed": 189,
  "at": 486
 },
 {
  "scenario": "isolated_abrupt",
  "seed": 191,
  "at": 477
 },
 {
  "scenario": "isolated_abrupt",
  "seed": 197,
  "at": 448
 },
 {
  "scenario": "isolated_abrupt",
  "seed": 198,
  "at": 512
 },
 {
  "scenario": "isolated_abrupt",
  "seed": 199,
  "at": 466
 }
]
```

## 연결
- [[실험 목록]]
