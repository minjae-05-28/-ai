---
유형: 실험
실행: transitions/multicellular
산출: results/transitions/multicellular/summary.json
tags:
  - 유형/실험
  - 실험/transitions-multicellular
---

# 실험 · transitions-multicellular

**산출물** `results/transitions/multicellular/summary.json`

## 한눈에

| 항목 | 값 |
| --- | --- |
| pathway | multicellular |
| n_reference_proteomes | 1751 |

## leave_one_origin_out

```json
{
 "metric": "auroc",
 "what": "predict which candidate families the held-out origin gained",
 "per_origin": {
  "Volvocales": {
   "n_candidates": 14588,
   "n_changed": 87,
   "share_changed": 0.006,
   "law": 0.6273,
   "control_baseline": 0.7288,
   "rarity_baseline": 0.7936,
   "law+rarity": 0.7823,
   "combined_minus_rarity": -0.0113,
   "control_baseline+rarity": 0.8176,
   "law_vs_control_combined": -0.0353
  },
  "Metazoa": {
   "n_candidates": 13446,
   "n_changed": 1032,
   "share_changed": 0.0768,
   "law": 0.5399,
   "control_baseline": 0.5862,
   "rarity_baseline": 0.7978,
   "law+rarity": 0.7333,
   "combined_minus_rarity": -0.0645,
   "control_baseline+rarity": 0.746,
   "law_vs_control_combined": -0.0127
  },
  "Dictyostelia": {
   "n_candidates": 13868,
   "n_changed": 353,
   "share_changed": 0.0255,
   "law": 0.6042,
   "control_baseline": 0.7417,
   "rarity_baseline": 0.7817,
   "law+rarity": 0.7235,
   "combined_minus_rarity": -0.0582,
   "control_baseline+rarity": 0.7855,
   "law_vs_control_combined": -0.062
  },
  "Phaeophyceae": {
   "n_candidates": 14963,
   "n_changed": 691,
   "share_changed": 0.0462,
   "law": 0.6595,
   "control_baseline": 0.8042,
   "rarity_baseline": 0.8664,
   "law+rarity": 0.8125,
   "combined_minus_rarity": -0.0539,
   "control_baseline+rarity": 0.8721,
   "law_vs_control_combined": -0.0596
  },
  "Rhodophyta (Bangiophyceae + Florideophyceae)": {
   "n_candidates": 15234,
   "n_changed": 264,
   "share_changed": 0.0173,
   "law": 0.6647,
   "control_baseline": 0.7883,
   "rarity_baseline": 0.8288,
   "law+rarity": 0.7879,

… (잘림 — 원본 파일 참조)
```

## law_minus_best_baseline

```json
{
 "mean": -0.1945,
 "ci95": [
  -0.2289,
  -0.1677
 ],
 "per_origin": {
  "Volvocales": -0.1663,
  "Metazoa": -0.2579,
  "Dictyostelia": -0.1775,
  "Phaeophyceae": -0.2069,
  "Rhodophyta (Bangiophyceae + Florideophyceae)": -0.1641
 },
 "note": "law minus the better baseline in each held-out origin; bootstrap over origins"
}
```

## law_adds_to_rarity

```json
{
 "mean": -0.0458,
 "ci95": [
  -0.0599,
  -0.0266
 ],
 "what": "AUROC of law+rarity (rank average) minus rarity alone, per origin: does the convergent signal carry information rarity does not"
}
```

## law_vs_control_signature

```json
{
 "mean": -0.0456,
 "ci95": [
  -0.0603,
  -0.0271
 ],
 "what": "law+rarity minus control+rarity, per origin: is the added information specific to this transition"
}
```

## share_gained

```json
{
 "multicellular_origins": {
  "Volvocales": 0.006,
  "Metazoa": 0.0768,
  "Dictyostelia": 0.0255,
  "Phaeophyceae": 0.0462,
  "Rhodophyta (Bangiophyceae + Florideophyceae)": 0.0173
 },
 "unicellular_controls": {
  "Trebouxiophyceae (a over b)": 0.0482,
  "Trebouxiophyceae (b over a)": 0.0291,
  "Mamiellales (a over b)": 0.0228,
  "Mamiellales (b over a)": 0.0505,
  "Diatoms (a over b)": 0.0324,
  "Diatoms (b over a)": 0.0335,
  "Chytrids (a over b)": 0.0652,
  "Chytrids (b over a)": 0.0337,
  "Holozoan protists (a over b)": 0.046,
  "Holozoan protists (b over a)": 0.0882
 }
}
```

## expansion_concordance

```json
{
 "metric": "spearman",
 "what": "mean pairwise rank correlation of log2 copy-number change over shared families",
 "multicellular_origins": 0.008,
 "n_origin_pairs": 10,
 "control_baseline": 0.1564,
 "n_control_pairs": 10
}
```

## panel

```json
{
 "cell adhesion / extracellular matrix": {
  "Cadherin": {
   "share_of_derived_with_it": 0.214,
   "share_of_relatives_with_it": 0.231,
   "changed_in_origins": 0.0,
   "changed_in_controls": 0.111
  },
  "Integrin_beta": {
   "share_of_derived_with_it": 0.286,
   "share_of_relatives_with_it": 0.077,
   "changed_in_origins": 0.25,
   "changed_in_controls": 0.143
  },
  "Integrin_alpha": {
   "share_of_derived_with_it": 0.0,
   "share_of_relatives_with_it": 0.0,
   "changed_in_origins": 0.0,
   "changed_in_controls": 0.0
  },
  "Laminin_G_1": {
   "share_of_derived_with_it": 0.214,
   "share_of_relatives_with_it": 0.154,
   "changed_in_origins": 0.0,
   "changed_in_controls": 0.111
  },
  "Collagen": {
   "share_of_derived_with_it": 0.643,
   "share_of_relatives_with_it": 0.462,
   "changed_in_origins": 0.5,
   "changed_in_controls": 0.429
  },
  "fn3": {
   "share_of_derived_with_it": 0.5,
   "share_of_relatives_with_it": 0.769,
   "changed_in_origins": 0.0,
   "changed_in_controls": 1.0
  },
  "EGF": {
   "share_of_derived_with_it": 0.286,
   "share_of_relatives_with_it": 0.385,
   "changed_in_origins": 0.5,
   "changed_in_controls": 0.143
  }
 },
 "developmental transcription factors": {
  "Homeobox_KN": {
   "share_of_derived_with_it": 1.0,
   "share_of_relatives_with_it": 0.923,
   "changed_in_origins": null,
   "changed_in_controls": 0.0
  }
 }
}
```

## 연결
- [[실험 목록]]
