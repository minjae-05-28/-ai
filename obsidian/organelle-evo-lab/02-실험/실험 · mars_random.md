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
    "share_shrank"
… (잘림 — 원본 파일 참조)
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
  "mars_grew": 0.815
… (잘림 — 원본 파일 참조)
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
  "kind": 
… (잘림 — 원본 파일 참조)
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
  "scenario": 
… (잘림 — 원본 파일 참조)
```

## 연결
- [[실험 목록]]
