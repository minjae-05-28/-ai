---
유형: 실험
실행: mito_ancestor/symmetric_busco0
산출: results/mito_ancestor/symmetric_busco0/summary.json
tags:
  - 유형/실험
  - 실험/mito_ancestor-symmetric_busco0
---

# 실험 · mito_ancestor-symmetric_busco0

**산출물** `results/mito_ancestor/symmetric_busco0/summary.json`

## 한눈에

| 항목 | 값 |
| --- | --- |
| tips | 2623 |
| alphaproteobacteria | 2323 |
| families | 9961 |
| n_masked | 300 |

## alpha_orders

```json
{
 "o__Rhizobiales": 767,
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
 "reconstruction": 0.9847,
 "alpha_frequency": 0.9624,
 "nearest_tip": 0.9777
}
```

## nodes

```json
{
 "Alphaproteobacteria (common ancestor)": {
  "n_tips_below": 2323,
  "families_p_ge_0.9": 772,
  "families_p_0.5_0.9": 683,
  "expected_families": 1938.5,
  "functions_top": [
   [
    "catalytic activity",
    212
   ],
   [
    "transferase activity",
    71
   ],
   [
    "helicase_nucleic",
    60
   ],
   [
    "DNA binding",
    53
   ],
   [
    "hydrolase activity",
    48
   ],
   [
    "structural molecule activity",
    43
   ],
   [
    "catalytic activity, acting on RNA",
    42
   ],
   [
    "organelle",
    41
   ],
   [
    "ribosome",
    40
   ],
   [
    "ligase activity",
    31
   ],
   [
    "RNA binding",
    29
   ],
   [
    "kinase",
    27
   ],
   [
    "amino acid metabolic process",
    27
   ],
   [
    "oxidoreductase activity",
    26
   ],
   [
    "catalytic activity, acting on DNA",
    24
   ]
  ],
  "present_but_rare_today": [
   [
    "CheZ",
    "Chemotaxis phosphatase, CheZ",
    0.999,
    0.216
   ],
   [
    "Fe-S_assembly",
    "Iron-sulphur cluster assembly",
    0.986,
    0.036
   ],
   [
    "Frataxin_Cyay",
    "Frataxin-like domain",
    0.975,
    0.041
   ],
   [
    "DjlA_TM",
    "Co-chaperone DjlA transmembrane domain",
    0.971,
    0.197
   ],
   [
    "HSCB_C",
    "HSCB C-terminal oligomerisation domain",
    0.966,
    0.038
   ],
   [
    "Glucosaminidase",
    "Mannosyl-glycoprotein endo-beta-N-acetylglucosaminidase",
    0.936,
    0.074
   ]
  ],
  "positive_control": {
   "nad1": 0.654,
   "nad2/4/5": 0.913,
   "nad3": 0.652,
   "nad6": 0.651,
   "nad7": 0.654,
   "nad9": 0.654,
   "nad4L": 0.841,
   "nad8": 0.965,
   "cox1": 0.997,
   "cox2": 0.177,
   "cox3": 0.06,
   "cob": 0.684,
   "atp1/3": 1.0,
   "atp6": 0.989,
   "atp9": 0.983,
   "rpoB": 0.967,
   "rpoC": 0.967,
   "rpoA": 0.983,
   "secY": 0.989,
   "tatC": 0.812,
   "ccmB": 0.027,
   "ccmC": 0.949,
   "tufA": 1.0,
   "rps12": null,
   "rpl2": 0.989,
   "rpl14": 0.989
  }
 },
 "Rickettsiales (common ancestor)": {
  "n_tips_below": 53,
  "families_p_ge_0.9": 629,
  "families_p_0.5_0.9": 307,
  "expected_families": 1264.8,
  "functions_top": [
   [
    "catalytic activity",
    167
   ],
   [
    "transferase activity",
    55
   ],
   [
    "helicase_nucleic",
    44
   ],
   [
    "DNA binding",
    39
   ],
   [
    "catalytic activity, acting on RNA",
    33
   ],
   [
    "structural molecule activity",
    33
   ],
   [
    "hydrolase activity",
    32
   ],
   [
    "organelle",
    31
   ],
   [
    "ribosome",
    30
   ],
   [
    "oxidoreductase activity",
    28
   ],
   [
    "ligase activity",
    24
   ],
   [
    "RNA binding",
    23
   ],
   [
    "transporter_channel",
    19
   ],
   [
    "amino acid metabolic process",
    19
   ],
   [
    "protease",
    19
   ]
  ],
  "present_but_rare_today": [
   [
    "Fe-S_assembly",
    "Iron-sulphur cluster assembly",
    1.0,
    0.036
   ],
   [
    "Frataxin_Cyay",
    "Frataxin-like domain",
    1.0,
    0.041
   ],
   [
    "PDDEXK_2",
    "PD-(D/E)XK nuclease family transposase",
    1.0,
    0.014
   ],
   [
    "Trp_repressor",
    "Trp repressor protein",
    1.0,
    0.05
   ],
   [
    "HTH_Rpn_C",
    "Rpn/YhgA-like nuclease family, C-terminal HTH domain",
    0.999,
    0.01
   ],
   [
    "TLC",
    "TLC ATP/ADP transporter",
    0.999,
    0.021
   ],
   [
    "HSCB_C",
    "HSCB C-terminal oligomerisation domain",
    0.998,
    0.038
   ],
   [
    "DUF2610",
    "Domain of unknown function (DUF2610)",
    0.997,
    0.026
   ],
   [
    "FliW",
    "FliW protein",
    0.995,
    0.018
   ],
   [
    "RP005_N",
    "RP005 N-terminal alpha-helical domain",
    0.994,
    0.043
   ],
   [
    "YMF19",
    "Plant ATP synthase F0",
    0.994,
    0.016
   ],
   [
    "DUF5915",
    "Domain of unknown function (DUF5915)",
    0.991,
    0.037
   ],
   [
    "Transposase_31",
    "Putative transposase, YhgA-like",
    0.991,
    0.012
   ],
   [
    "DUF2608",
    "Protein of unknown function (DUF2608)",
    0.984,
    0.013
   ],
   [
    "DUF2671",
    "Protein of unknown function (DUF2671)",
    0.983,
    0.008
   ],
   [
    "ABC_sub_bind",
    "ABC transporter substrate binding protein",
    0.946,
    0.246
   ],
   [
    "CheZ",
    "Chemotaxis phosphatase, CheZ",
    0.945,
    0.216
   ],
   [
    "DUF2748",
    "Protein of unknown function (DUF2748)",
    0.931,
    0.006
   ],
   [
    "LRR_6",
    "Leucine Rich repeat",
    0.91,
    0.018
   ]
  ],
  "positive_control": {
   "nad1": 0.995,
   "nad2/4/5": 0.97,
   "nad3": 0.995,
   "nad6": 0.995,
   "nad7": 0.995,
   "nad9": 0.995,
   "nad4L": 0.95,
   "nad8": 0.981,
   "cox1": 1.0,
   "cox2": 0.015,
   "cox3": 0.002,
   "cob": 0.707,
   "atp1/3": 0.996,
   "atp6": 0.994,
   "atp9": 0.92,
   "rpoB": 0.903,
   "rpoC": 0.911,
   "rpoA": 0.92,
   "secY": 0.994,
   "tatC": 0.963,
   "ccmB": 0.008,
   "ccmC": 1.0,
   "tufA": 1.0,
   "rps12": null,
   "rpl2": 0.994,
   "rpl14": 0.994
  }
 },
 "Holosporales (common ancestor)": {
  "n_tips_below": 4,
  "families_p_ge_0.9": 534,
  "families_p_0.5_0.9": 386,
  "expected_families": 1537.8,
  "functions_top": [
   [
    "catalytic activity",
    152
   ],
   [
    "helicase_nucleic",
    55
   ],
   [
    "transferase activity",
    50
   ],
   [
    "DNA binding",
    48
   ],
   [
    "catalytic activity, acting on RNA",
    41
   ],
   [
    "structural molecule activity",
    40
   ],
   [
    "organelle",
    38
   ],
   [
    "ribosome",
    37
   ],
   [
    "hydrolase activity",
    36
   ],
   [
    "ligase activity",
    30
   ],
   [
    "RNA binding",
    27
   ],
   [
    "catalytic activity, acting on DNA",
    25
   ],
   [
    "amino acid metabolic process",
    23
   ],
   [
    "tRNA metabolic process",
    22
   ],
   [
    "DNA-templated transcription",
    22
   ]
  ],
  "present_but_rare_today": [
   [
    "TLC",
    "TLC ATP/ADP transporter",
    0.998,
    0.021
   ],
   [
    "Glucosaminidase",
    "Mannosyl-glycoprotein endo-beta-N-acetylglucosaminidase",
  
… (잘림, 원본 파일 참조)
```

## 연결
- [[실험 목록]]
