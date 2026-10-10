---
유형: 실험
실행: gene_trees
산출: results/gene_trees/summary.json
tags:
  - 유형/실험
  - 실험/gene_trees
---

# 실험 · gene_trees

**산출물** `results/gene_trees/summary.json`

## 한눈에

| 항목 | 값 |
| --- | --- |
| n_families_with_tree | 248 |
| n_skipped | 20 |
| verdict | 해석 1 지지: 세균에 흔할수록 '확실히 갈라진' 진핵 기원이 늘어남 (수평이동) |

## skipped

```json
{
 "DUF3825": "too few sequences (18 eukaryote, 2 prokaryote)",
 "CDPS": "too few sequences (21 eukaryote, 0 prokaryote)",
 "I-set": "too few sequences (90 eukaryote, 1 prokaryote)",
 "GlcNAc": "too few sequences (181 eukaryote, 1 prokaryote)",
 "MIOX": "too few sequences (200 eukaryote, 3 prokaryote)",
 "PAN_1": "too few sequences (201 eukaryote, 2 prokaryote)",
 "Mitofilin": "too few sequences (227 eukaryote, 3 prokaryote)",
 "Nse4_C": "too few sequences (233 eukaryote, 0 prokaryote)",
 "RyR": "too few sequences (75 eukaryote, 3 prokaryote)",
 "DUF3223": "too few sequences (110 eukaryote, 0 prokaryote)",
 "DUF4246": "too few sequences (91 eukaryote, 0 prokaryote)",
 "Urm1": "too few sequences (214 eukaryote, 1 prokaryote)",
 "LAGLIDADG_1": "too few sequences (30 eukaryote, 1 prokaryote)",
 "Pyr_redox": "too few sequences (32 eukaryote, 3 prokaryote)",
 "NIDO": "too few sequences (83 eukaryote, 3 prokaryote)",
 "Vps62": "too few sequences (152 eukaryote, 3 prokaryote)",
 "TMEM43": "too few sequences (140 eukaryote, 2 prokaryote)",
 "RGP": "too few sequences (53 eukaryote, 3 prokaryote)",
 "RNA_helicase": "too few sequences (38 eukaryote, 0 prokaryote)",
 "Peptidase_M11": "too few sequences (53 eukaryote, 3 prokaryote)"
}
```

## bact~Ksup2

```json
{
 "partial_spearman": 0.3669,
 "ci95": [
  0.2497,
  0.4738
 ]
}
```

## bact~Kraw2

```json
{
 "partial_spearman": 0.3231,
 "ci95": [
  0.2188,
  0.4196
 ]
}
```

## Q1_share_Ksup2

```json
{
 "vosseberg_leca": 0.8833,
 "vosseberg_not_leca": 0.9297,
 "not_minus_leca_ci95": [
  -0.0242,
  0.1202
 ]
}
```

## secondary_our_leca_like_vs_theirs

```json
{
 "agreement": 0.5685,
 "leca_like_share_in_their_leca": 0.8667,
 "leca_like_share_in_their_not": 0.7109
}
```

## secondary_prok_nearest_mean

```json
{
 "vosseberg_leca": 0.0333,
 "vosseberg_not_leca": 0.0549
}
```

## 연결
- [[실험 목록]]
