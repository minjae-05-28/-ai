---
유형: 실험
실행: animal_laws
산출: results/animal_laws/metrics.json
tags:
  - 유형/실험
  - 실험/animal_laws
---

# 실험 · animal_laws

**산출물** `results/animal_laws/metrics.json`

## 한눈에

| 항목 | 값 |
| --- | --- |
| n_species | 69 |
| n_clades | 18 |

## axes

```json
[
 "tcell",
 "osmol_high",
 "hypoxia",
 "endo",
 "parasite",
 "urea"
]
```

## traits

```json
{
 "ivywrel": {
  "r2": 0.2763395313426954,
  "coef": {
   "tcell": 0.00020303478990723627,
   "osmol_high": -0.00389131084817045,
   "hypoxia": 0.0018766144394684956,
   "endo": -0.00118383798394784,
   "parasite": 0.004439754439170312,
   "urea": 0.006727760053108077
  },
  "p": {
   "tcell": 0.038243604963832396,
   "osmol_high": 0.031176312365837594,
   "hypoxia": 0.41807075228845214,
   "endo": 0.6298414250404574,
   "parasite": 0.20664314972163583,
   "urea": 0.025705373912816503
  },
  "leave_one_clade_out": {
   "n_predicted": 69,
   "mae_law": 0.0052663543439131185,
   "mae_mean_baseline": 0.005078496479030528,
   "beats_baseline": false
  },
  "clade_level": {
   "n_clades": 18,
   "coef": {
    "tcell": 0.0004197778232459674,
    "osmol_high": -0.0032612949684985015,
    "hypoxia": -0.007859252255747518,
    "endo": -0.005931830151479967,
    "parasite": 0.004887890575306769,
    "urea": 0.006335742233773584
   },
   "p": {
    "tcell": 0.24958635300349827,
    "osmol_high": 0.3271127757140451,
    "hypoxia": 0.20251183078271193,
    "endo": 0.38912024049102073,
    "parasite": 0.5554519071536401,
    "urea": 0.28507987083279085
   },
   "r2": 0.4983760816532572
  },
  "survives_clade_level": [],
  "with_gc": {
   "n": 69,
   "coef": {
    "tcell": 0.00018018306763861673,
    "osmol_high": -0.004558064592967843,
    "hypoxia": 0.002017997962158545,
    "endo": -0.0002427793714519889,
    "parasite": 0.0035110131076199823,
    "urea": 0.00841571328629672
   },
   "p": {
    "tcell": 0.06592960763609529,
    "osmol_high": 0.014183900426251691,
    "hypoxia": 0.3800
… (잘림 — 원본 파일 참조)
```

## 연결
- [[실험 목록]]
