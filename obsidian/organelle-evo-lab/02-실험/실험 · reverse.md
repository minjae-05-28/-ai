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
    "auroc_recover_lost": 0.8
… (잘림 — 원본 파일 참조)
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
    "ancestor": 32.728220104382
… (잘림 — 원본 파일 참조)
```

## 연결
- [[실험 목록]]
