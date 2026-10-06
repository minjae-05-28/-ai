---
유형: 실험
실행: mito_ancestor/completeness
산출: results/mito_ancestor/completeness/summary.json
tags:
  - 유형/실험
  - 실험/mito_ancestor-completeness
---

# 실험 · mito_ancestor-completeness

**산출물** `results/mito_ancestor/completeness/summary.json`

## 한눈에

| 항목 | 값 |
| --- | --- |
| tips | 2622 |
| alphaproteobacteria | 2322 |
| families | 9934 |
| n_masked | 300 |
| completeness_model | True |

## alpha_orders

```json
{
 "o__Rhizobiales": 766,
 "o__Rhodobacterales": 589,
 "o__Sphingomonadales": 416,
 "o__Acetobacterales": 200,
 "o__Caulobacterales": 124,
 "o__Rickettsiales": 53,
 "o__Rhodospirillales": 46,
 "o__Azospirillales": 34,
 "o__Kiloniellales": 16,
 "o__Sneathiellales": 7,
 "o__Dongiales": 6,
 "o__Reyranellales": 5,
 "o__Holosporales": 4,
 "o__Thalassobaculales": 4,
 "o__UBA8366": 4,
 "o__CAJXXZ01": 3,
 "o__Caedimonadales": 3,
 "o__Elsterales": 3,
 "o__Geminicoccales": 3,
 "o__Zavarziniales": 3,
 "o__Parvibaculales": 3,
 "o__Pelagibacterales": 3,
 "o__Paracaedibacterales": 2,
 "o__Oceanibaculales": 2,
 "o__DSM-16000": 2,
 "o__Tistrellales": 2,
 "o__Ferrovibrionales": 2,
 "o__CGMCC-115125": 2,
 "o__Micropepsales": 2,
 "o__UBA2136": 1,
 "o__CASFRQ01": 1,
 "o__Rs-D84": 1,
 "o__RF32": 1,
 "o__UBA9655": 1,
 "o__UBA6184": 1,
 "o__Puniceispirillales": 1,
 "o__Micavibrionales": 1,
 "o__BOG-932": 1,
 "o__ATCC43930": 1,
 "o__Minwuiales": 1,
 "o__RS24": 1,
 "o__Futianiales": 1
}
```

## leave_tips_out_auroc

```json
{
 "reconstruction": 0.9841,
 "alpha_frequency": 0.962,
 "nearest_tip": 0.9777
}
```

## per_node_validation

```json
{
 "Alphaproteobacteria (common ancestor)": {
  "reconstruction": 0.9835,
  "clade_frequency": 0.9621,
  "n_hidden": 1392,
  "n_tips": 2322
 },
 "Rickettsiales (common ancestor)": {
  "reconstruction": 0.988,
  "clade_frequency": 0.9875,
  "n_hidden": 30,
  "n_tips": 53
 },
 "Rhodospirillales (common ancestor)": {
  "reconstruction": 0.9805,
  "clade_frequency": 0.9735,
  "n_hidden": 27,
  "n_tips": 46
 },
 "Caulobacterales (common ancestor)": {
  "reconstruction": 0.9826,
  "clade_frequency": 0.9758,
  "n_hidden": 72,
  "n_tips": 124
 }
}
```

## nodes

```json
{
 "Alphaproteobacteria (common ancestor)": {
  "n_tips_below": 2322,
  "families_p_ge_0.9": 1792,
  "families_p_0.5_0.9": 1586,
  "expected_families": 4037.8,
  "functions_top": [
   [
    "catalytic activity",
    446
   ],
   [
    "transferase activity",
    129
   ],
   [
    "hydrolase activity",
    92
   ],
   [
    "oxidoreductase activity",
    88
   ],
   [
    "uncharacterised",
    83
   ],
   [
    "helicase_nucleic",
    80
   ],
   [
    "DNA binding",
    73
   ],
   [
    "protease",
    57
   ],
   [
    "transporter_channel",
    56
   ],
   [
    "catalytic activity, acting on RNA",
    51
   ],
   [
    "organelle",
    49
   ],
   [
    "structural molecule activity",
    48
   ],
   [
    "kinase",
    47
   ],
   [
    "ligase activity",
    45
   ],
   [
    "amino acid metabolic process",
    44
   ]
  ],
  "present_but_rare_today": [
   [
    "CheZ",
    "Chemotaxis phosphatase, CheZ",
    1.0,
    0.218
   ],
   [
    "DUF6898",
    "Domain of unknown function (DUF6898)",
    1.0,
    0.131
   ],
   [
    "DjlA_TM",
    "Co-chaperone DjlA transmembrane domain",
    0.998,
    0.197
   ],
   [
    "Fe-S_assembly",
    "Iron-sulphur cluster assembly",
    0.997,
    0.037
   ],
   [
    "FliJ",
    "Flagellar FliJ protein",
    0.997,
    0.23
   ],
   [
    "DUF6111",
    "Family of unknown function (DUF6111)",
    0.996,
    0.181
   ],
   [
    "Frataxin_Cyay",
    "Frataxin-like domain",
    0.996,
    0.041
   ],
   [
    "RP005_N",
    "RP005 N-terminal alpha-helical domain",
    0.996,
    0.044
   ],
   [
    "DUF6867",
    "Domain of unkn
… (잘림 — 원본 파일 참조)
```

## 연결
- [[실험 목록]]
