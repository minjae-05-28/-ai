---
유형: 실험
실행: mito_ancestor/loss_biased_busco0
산출: results/mito_ancestor/loss_biased_busco0/summary.json
tags:
  - 유형/실험
  - 실험/mito_ancestor-loss_biased_busco0
---

# 실험 · mito_ancestor-loss_biased_busco0

**산출물** `results/mito_ancestor/loss_biased_busco0/summary.json`

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
 "reconstruction": 0.9846,
 "alpha_frequency": 0.9624,
 "nearest_tip": 0.9777
}
```

## nodes

```json
{
 "Alphaproteobacteria (common ancestor)": {
  "n_tips_below": 2323,
  "families_p_ge_0.9": 1710,
  "families_p_0.5_0.9": 1575,
  "expected_families": 3945.1,
  "functions_top": [
   [
    "catalytic activity",
    431
   ],
   [
    "transferase activity",
    128
   ],
   [
    "hydrolase activity",
    90
   ],
   [
    "oxidoreductase activity",
    83
   ],
   [
    "helicase_nucleic",
    76
   ],
   [
    "DNA binding",
    70
   ],
   [
    "uncharacterised",
    66
   ],
   [
    "protease",
    57
   ],
   [
    "transporter_channel",
    52
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
    "amino acid metabolic process",
    44
   ],
   [
    "ligase activity",
    43
   ]
  ],
  "present_but_rare_today": [
   [
    "CheZ",
    "Chemotaxis phosphatase, CheZ",
    1.0,
    0.216
   ],
   [
    "DUF6898",
    "Domain of unknown function (DUF6898)",
    1.0,
    0.129
   ],
   [
    "DjlA_TM",
    "Co-chaperone DjlA transmembrane domain",
    0.997,
    0.197
   ],
   [
    "Fe-S_assembly",
    "Iron-sulphur cluster assembly",
    0.996,
    0.036
   ],
   [
    "Frataxin_Cyay",
    "Frataxin-like domain",
    0.995,
    0.041
   ],
   [
    "YMF19",
    "Plant ATP synthase F0",
    0.995,
    0.016
   ],
   [
    "DUF6111",
    "Family of unknown function (DUF6111)",
    0.994,
    0.18
   ],
   [
    "FliJ",
    "Flagellar FliJ protein",
    0.994,
    0.23
   ],
   [
    "Glucosaminidase",
    "Mannosyl-glycoprotein endo-beta-N-acetylglucosaminidase",
    0.993,
    0.074
   ],
   [
    "DUF6867",
    "Domain of unknown function (DUF6867)",
    0.992,
    0.268
   ],
   [
    "PFK",
    "Phosphofructokinase",
    0.992,
    0.229
   ],
   [
    "HSCB_C",
    "HSCB C-terminal oligomerisation domain",
    0.991,
    0.038
   ],
   [
    "Exop_C",
    "Galactose-binding domain-like",
    0.99,
    0.13
   ],
   [
    "Glyco_transf_9",
    "Glycosyltransferase family 9 (heptosyltransferase)",
    0.988,
    0.297
   ],
   [
    "Hpre_diP_synt_I",
    "Heptaprenyl diphosphate synthase component I",
    0.988,
    0.001
   ],
   [
    "MreD",
    "rod shape-determining protein MreD",
    0.988,
    0.196
   ],
   [
    "NusG_II",
    "NusG domain II",
    0.988,
    0.001
   ],
   [
    "Peptidase_S66",
    "LD-carboxypeptidase N-terminal domain",
    0.988,
    0.221
   ],
   [
    "Peptidase_S66C",
    "LD-carboxypeptidase C-terminal domain",
    0.988,
    0.223
   ],
   [
    "tRNA-synt_1c_C",
    "tRNA synthetases class I (E and Q), anti-codon binding domain",
    0.981,
    0.048
   ],
   [
    "tRNA-synt_1c_C2",
    "tRNA synthetases class I (E and Q), anti-codon binding domain",
    0.981,
    0.048
   ],
   [
    "DUF1207",
    "Protein of unknown function (DUF1207)",
    0.98,
    0.003
   ],
   [
    "A24_N_bact",
    "Bacterial Peptidase A24 N-terminal domain",
    0.979,
    0.183
   ],
   [
    "Csd3_N2",
    "Csd3 second domain",
    0.979,
    0.172
   ],
   [
    "PrcB_C",
    "PrcB C-terminal",
    0.978,
    0.015
   ],
   [
    "DUF1848",
    "Domain of unknown function (DUF1848)",
    0.977,
    0.029
   ],
   [
    "FliW",
    "FliW protein",
    0.977,
    0.018
   ],
   [
    "PDDEXK_2",
    "PD-(D/E)XK nuclease family transposase",
    0.974,
    0.014
   ],
   [
    "DUF6468",
    "Domain of unknown function (DUF6468)",
    0.969,
    0.294
   ],
   [
    "FliX",
    "Class II flagellar assembly regulator",
    0.966,
    0.263
   ],
   [
    "DUF2608",
    "Protein of unknown function (DUF2608)",
    0.961,
    0.013
   ],
   [
    "DUF3335",
    "Peptidase_C39 like family",
    0.96,
    0.081
   ],
   [
    "Trp_repressor",
    "Trp repressor protein",
    0.96,
    0.05
   ],
   [
    "TMEM164",
    "TMEM164 family",
    0.959,
    0.004
   ],
   [
    "RP005_N",
    "RP005 N-terminal alpha-helical domain",
    0.958,
    0.043
   ],
   [
    "hDGE_amylase",
    "Glycogen debranching enzyme, glucanotransferase domain",
    0.958,
    0.044
   ],
   [
    "STR4_M",
    "STR4 middle domain",
    0.956,
    0.121
   ],
   [
    "Maf_flag10_N",
    "Glycosyltransferase Maf N-terminal domain",
    0.955,
    0.012
   ],
   [
    "Transposase_31",
    "Putative transposase, YhgA-like",
    0.955,
    0.012
   ],
   [
    "DUF2232",
    "Predicted membrane protein (DUF2232)",
    0.946,
    0.174
   ]
  ],
  "positive_control": {
   "nad1": 1.0,
   "nad2/4/5": 1.0,
   "nad3": 1.0,
   "nad6": 1.0,
   "nad7": 1.0,
   "nad9": 1.0,
   "nad4L": 1.0,
   "nad8": 1.0,
   "cox1": 1.0,
   "cox2": 0.879,
   "cox3": 0.877,
   "cob": 0.999,
   "atp1/3": 1.0,
   "atp6": 1.0,
   "atp9": 1.0,
   "rpoB": 1.0,
   "rpoC": 1.0,
   "rpoA": 1.0,
   "secY": 1.0,
   "tatC": 1.0,
   "ccmB": 0.999,
   "ccmC": 1.0,
   "tufA": 1.0,
   "rps12": null,
   "rpl2": 1.0,
   "rpl14": 1.0
  }
 },
 "Rickettsiales (common ancestor)": {
  "n_tips_below": 53,
  "families_p_ge_0.9": 1139,
  "families_p_0.5_0.9": 285,
  "expected_families": 1902.7,
  "functions_top": [
   [
    "catalytic activity",
    285
   ],
   [
    "transferase activity",
    90
   ],
   [
    "helicase_nucleic",
    70
   ],
   [
    "hydrolase activity",
    61
   ],
   [
    "DNA binding",
    59
   ],
   [
    "organelle",
    49
   ],
   [
    "oxidoreductase activity",
    48
   ],
   [
    "structural molecule activity",
    48
   ],
   [
    "catalytic activity, acting on RNA",
    43
   ],
   [
    "ribosome",
    42
   ],
   [
    "protease",
    39
   ],
   [
    "transporter_channel",
    39
   ],
   [
    "ligase activity",
    33
   ],
   [
    "transporter activity",
    32
   ],
   [
    "catalytic activity, acting on DNA",
    32
   ]
  ],
  "present_but_rare_today": [
   [
    "A24_N_bact",
    "Bacterial Peptidase A24 N-terminal domain",
    1.0,
    0.183
   ],
   [
    "Fe-S_assembly",
    "Iron-sulphur cluster assembly",
    1.0,
    0.036
   ],
   [
    "Frataxi
… (잘림, 원본 파일 참조)
```

## 연결
- [[실험 목록]]
