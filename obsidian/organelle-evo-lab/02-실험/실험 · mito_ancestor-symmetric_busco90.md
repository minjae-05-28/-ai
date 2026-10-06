---
유형: 실험
실행: mito_ancestor/symmetric_busco90
산출: results/mito_ancestor/symmetric_busco90/summary.json
tags:
  - 유형/실험
  - 실험/mito_ancestor-symmetric_busco90
---

# 실험 · mito_ancestor-symmetric_busco90

**산출물** `results/mito_ancestor/symmetric_busco90/summary.json`

## 한눈에

| 항목 | 값 |
| --- | --- |
| tips | 2526 |
| alphaproteobacteria | 2226 |
| families | 9972 |
| n_masked | 300 |

## alpha_orders

```json
{
 "o__Rhizobiales": 748,
 "o__Rhodobacterales": 578,
 "o__Sphingomonadales": 398,
 "o__Acetobacterales": 193,
 "o__Caulobacterales": 122,
 "o__Rhodospirillales": 45,
 "o__Rickettsiales": 40,
 "o__Azospirillales": 33,
 "o__Kiloniellales": 16,
 "o__Sneathiellales": 7,
 "o__Dongiales": 6,
 "o__UBA8366": 4,
 "o__Thalassobaculales": 3,
 "o__Parvibaculales": 3,
 "o__Elsterales": 2,
 "o__Oceanibaculales": 2,
 "o__DSM-16000": 2,
 "o__Tistrellales": 2,
 "o__Geminicoccales": 2,
 "o__Ferrovibrionales": 2,
 "o__Zavarziniales": 2,
 "o__CGMCC-115125": 2,
 "o__Micropepsales": 2,
 "o__UBA2136": 1,
 "o__Rs-D84": 1,
 "o__RF32": 1,
 "o__Caedimonadales": 1,
 "o__Puniceispirillales": 1,
 "o__BOG-932": 1,
 "o__Reyranellales": 1,
 "o__ATCC43930": 1,
 "o__Minwuiales": 1,
 "o__Pelagibacterales": 1,
 "o__RS24": 1,
 "o__Futianiales": 1
}
```

## leave_tips_out_auroc

```json
{
 "reconstruction": 0.9852,
 "alpha_frequency": 0.9627,
 "nearest_tip": 0.9792
}
```

## nodes

```json
{
 "Alphaproteobacteria (common ancestor)": {
  "n_tips_below": 2226,
  "families_p_ge_0.9": 1044,
  "families_p_0.5_0.9": 871,
  "expected_families": 2288.1,
  "functions_top": [
   [
    "catalytic activity",
    300
   ],
   [
    "transferase activity",
    95
   ],
   [
    "helicase_nucleic",
    63
   ],
   [
    "DNA binding",
    58
   ],
   [
    "hydrolase activity",
    56
   ],
   [
    "oxidoreductase activity",
    55
   ],
   [
    "catalytic activity, acting on RNA",
    47
   ],
   [
    "structural molecule activity",
    43
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
    "amino acid metabolic process",
    39
   ],
   [
    "ligase activity",
    36
   ],
   [
    "kinase",
    35
   ],
   [
    "methyl_glyco_transferase",
    31
   ],
   [
    "RNA binding",
    30
   ]
  ],
  "present_but_rare_today": [
   [
    "CheZ",
    "Chemotaxis phosphatase, CheZ",
    0.996,
    0.216
   ],
   [
    "Fe-S_assembly",
    "Iron-sulphur cluster assembly",
    0.992,
    0.032
   ],
   [
    "DjlA_TM",
    "Co-chaperone DjlA transmembrane domain",
    0.99,
    0.197
   ],
   [
    "HSCB_C",
    "HSCB C-terminal oligomerisation domain",
    0.98,
    0.033
   ],
   [
    "Frataxin_Cyay",
    "Frataxin-like domain",
    0.973,
    0.035
   ],
   [
    "DUF6898",
    "Domain of unknown function (DUF6898)",
    0.971,
    0.135
   ],
   [
    "ATPase-cat_bd",
    "Putative metal-binding domain of cation transport ATPase",
    0.967,
    0.043
   ],
   [
    "DUF6867",
    "Domain of unknown function (DUF6867)",
    0.947,
    0.271
   ],
   [
    "MreD",
    "rod shape-determining protein MreD",
    0.936,
    0.197
   ],
   [
    "tRNA-synt_1c_C",
    "tRNA synthetases class I (E and Q), anti-codon binding domain",
    0.926,
    0.049
   ],
   [
    "tRNA-synt_1c_C2",
    "tRNA synthetases class I (E and Q), anti-codon binding domain",
    0.926,
    0.049
   ],
   [
    "Csd3_N2",
    "Csd3 second domain",
    0.908,
    0.171
   ]
  ],
  "positive_control": {
   "nad1": 0.986,
   "nad2/4/5": 0.98,
   "nad3": 0.986,
   "nad6": 0.986,
   "nad7": 0.986,
   "nad9": 0.962,
   "nad4L": 0.969,
   "nad8": 0.957,
   "cox1": 0.999,
   "cox2": 0.844,
   "cox3": 0.44,
   "cob": 0.964,
   "atp1/3": 1.0,
   "atp6": 1.0,
   "atp9": 0.999,
   "rpoB": 0.988,
   "rpoC": 0.988,
   "rpoA": 1.0,
   "secY": 0.999,
   "tatC": 0.982,
   "ccmB": 0.627,
   "ccmC": 0.982,
   "tufA": 1.0,
   "rps12": null,
   "rpl2": 1.0,
   "rpl14": 0.999
  }
 },
 "Rickettsiales (common ancestor)": {
  "n_tips_below": 40,
  "families_p_ge_0.9": 741,
  "families_p_0.5_0.9": 352,
  "expected_families": 1595.4,
  "functions_top": [
   [
    "catalytic activity",
    193
   ],
   [
    "transferase activity",
    63
   ],
   [
    "helicase_nucleic",
    58
   ],
   [
    "DNA binding",
    47
   ],
   [
    "structural molecule activity",
    44
   ],
   [
    "organelle",
    42
   ],
   [
    "catalytic activity, acting on RNA",
    41
   ],
   [
    "ribosome",
    41
   ],
   [
    "hydrolase activity",
    38
   ],
   [
    "oxidoreductase activity",
    37
   ],
   [
    "ligase activity",
    29
   ],
   [
    "RNA binding",
    28
   ],
   [
    "amino acid metabolic process",
    23
   ],
   [
    "catalytic activity, acting on DNA",
    23
   ],
   [
    "DNA-templated transcription",
    23
   ]
  ],
  "present_but_rare_today": [
   [
    "DUF5394",
    "Family of unknown function (DUF5394)",
    1.0,
    0.009
   ],
   [
    "Fe-S_assembly",
    "Iron-sulphur cluster assembly",
    1.0,
    0.032
   ],
   [
    "HSCB_C",
    "HSCB C-terminal oligomerisation domain",
    1.0,
    0.033
   ],
   [
    "RP005_N",
    "RP005 N-terminal alpha-helical domain",
    1.0,
    0.043
   ],
   [
    "DUF2610",
    "Domain of unknown function (DUF2610)",
    0.999,
    0.022
   ],
   [
    "LepB_N",
    "LepB N-terminal domain",
    0.999,
    0.01
   ],
   [
    "TLC",
    "TLC ATP/ADP transporter",
    0.999,
    0.011
   ],
   [
    "Frataxin_Cyay",
    "Frataxin-like domain",
    0.997,
    0.035
   ],
   [
    "RP252",
    "RP252-like transmembrane domain",
    0.997,
    0.009
   ],
   [
    "DUF5915",
    "Domain of unknown function (DUF5915)",
    0.996,
    0.032
   ],
   [
    "Csd3_N2",
    "Csd3 second domain",
    0.99,
    0.171
   ],
   [
    "Isocitrate_DH_C_bact",
    "Bacterial isocitrate dehydrogenase, C-terminal domain",
    0.99,
    0.059
   ],
   [
    "PDDEXK_2",
    "PD-(D/E)XK nuclease family transposase",
    0.985,
    0.011
   ],
   [
    "DUF2659",
    "Protein of unknown function (DUF2659)",
    0.984,
    0.011
   ],
   [
    "FliX",
    "Class II flagellar assembly regulator",
    0.974,
    0.271
   ],
   [
    "Band_7_C",
    "C-terminal region of band_7",
    0.964,
    0.053
   ],
   [
    "DUF6898",
    "Domain of unknown function (DUF6898)",
    0.947,
    0.135
   ]
  ],
  "positive_control": {
   "nad1": 0.999,
   "nad2/4/5": 0.989,
   "nad3": 0.999,
   "nad6": 0.999,
   "nad7": 0.999,
   "nad9": 0.976,
   "nad4L": 0.988,
   "nad8": 0.974,
   "cox1": 1.0,
   "cox2": 0.73,
   "cox3": 0.412,
   "cob": 0.976,
   "atp1/3": 1.0,
   "atp6": 1.0,
   "atp9": 1.0,
   "rpoB": 0.988,
   "rpoC": 0.991,
   "rpoA": 1.0,
   "secY": 1.0,
   "tatC": 0.989,
   "ccmB": 0.935,
   "ccmC": 0.99,
   "tufA": 1.0,
   "rps12": null,
   "rpl2": 1.0,
   "rpl14": 1.0
  }
 },
 "Rhodospirillales (common ancestor)": {
  "n_tips_below": 45,
  "families_p_ge_0.9": 1936,
  "families_p_0.5_0.9": 378,
  "expected_families": 2345.9,
  "functions_top": [
   [
    "catalytic activity",
    430
   ],
   [
    "transferase activity",
    129
   ],
   [
    "uncharacterised",
    129
   ],
   [
    "hydrolase activity",
    84
   ],
   [
    "oxidoreductase activity",
    81
   ],
   [
    "helicase_nucleic",
    78
   ],
   [
    "DNA binding",
    76
   ],
   [
    "transporter_channel",
    59
   ],
   [
    "kinase",
    53
   ],
   [
    "catalytic activity, acting on RNA",
    52
   ],
… (잘림, 원본 파일 참조)
```

## 연결
- [[실험 목록]]
