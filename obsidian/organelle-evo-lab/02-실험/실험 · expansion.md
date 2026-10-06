---
유형: 실험
실행: expansion
산출: results/expansion/metrics.json
tags:
  - 유형/실험
  - 실험/expansion
---

# 실험 · expansion

**산출물** `results/expansion/metrics.json`

## 한눈에

| 항목 | 값 |
| --- | --- |
| n_parasite_pairs | 90 |
| familywise_threshold_clades | 6 |

## clades

```json
[
 "alveolata",
 "amoebozoa",
 "chelicerata",
 "chlorophyta",
 "cnidaria",
 "crustacea",
 "discoba",
 "fungi",
 "holozoa",
 "insecta",
 "metamonada",
 "nematoda",
 "platyhelminthes",
 "stramenopiles",
 "streptophyta"
]
```

## expansion_rate

```json
{
 "parasites": 0.0192793108656964,
 "controls": 0.029965292544625762
}
```

## convergent

```json
[
 {
  "family": "zf-CCHC",
  "description": "Zinc knuckle",
  "n_clades": 8,
  "p": 0.0,
  "clades": [
   "alveolata",
   "amoebozoa",
   "chelicerata",
   "fungi",
   "holozoa",
   "nematoda",
   "stramenopiles",
   "streptophyta"
  ]
 },
 {
  "family": "PNP_UDP_1",
  "description": "Phosphorylase superfamily",
  "n_clades": 7,
  "p": 0.0,
  "clades": [
   "alveolata",
   "amoebozoa",
   "discoba",
   "fungi",
   "metamonada",
   "nematoda",
   "stramenopiles"
  ]
 },
 {
  "family": "Peptidase_C13",
  "description": "Peptidase C13 family",
  "n_clades": 7,
  "p": 0.0,
  "clades": [
   "alveolata",
   "chelicerata",
   "cnidaria",
   "metamonada",
   "nematoda",
   "platyhelminthes",
   "stramenopiles"
  ]
 },
 {
  "family": "RNase_H",
  "description": "RNase H",
  "n_clades": 7,
  "p": 0.0,
  "clades": [
   "alveolata",
   "chelicerata",
   "crustacea",
   "discoba",
   "fungi",
   "nematoda",
   "stramenopiles"
  ]
 }
]
```

## enriched_functions_multi_clade

```json
[
 [
  "go:ribosome",
  3.18,
  0.037
 ],
 [
  "go:structural molecule activity",
  2.7,
  0.038
 ],
 [
  "go:hydrolase activity",
  2.37,
  0.069
 ],
 [
  "go:catalytic activity",
  2.18,
  0.209
 ],
 [
  "kw:protease",
  2.18,
  0.049
 ],
 [
  "go:oxidoreductase activity",
  2.01,
  0.035
 ],
 [
  "go:transferase activity",
  1.95,
  0.062
 ]
]
```

## 연결
- [[실험 목록]]
