---
유형: 실험
실행: mito_ancestor/loss_biased_busco90
산출: results/mito_ancestor/loss_biased_busco90/summary.json
tags:
  - 유형/실험
  - 실험/mito_ancestor-loss_biased_busco90
---

# 실험 · mito_ancestor-loss_biased_busco90

**산출물** `results/mito_ancestor/loss_biased_busco90/summary.json`

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
 "reconstruction": 0.9849,
 "alpha_frequency": 0.9627,
 "nearest_tip": 0.9792
}
```

## nodes

```json
{
 "Alphaproteobacteria (common ancestor)": {
  "n_tips_below": 2226,
  "families_p_ge_0.9": 1798,
  "families_p_0.5_0.9": 1632,
  "expected_families": 4122.2,
  "functions_top": [
   [
    "catalytic activity",
    447
   ],
   [
    "transferase activity",
    128
   ],
   [
    "uncharacterised",
    96
   ],
   [
    "hydrolase activity",
    93
   ],
   [
    "oxidoreductase activity",
    89
   ],
   [
    "helicase_nucleic",
    78
   ],
   [
    "DNA binding",
    70
   ],
   [
    "protease",
    59
   ],
   [
    "transporter_channel",
    52
   ],
   [
    "catalytic activity, acting on RNA",
    52
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
    46
   ],
   [
    "ligase activity",
    45
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
    0.135
   ],
   [
    "DjlA_TM",
    "Co-chaperone DjlA transmembrane domain",
    0.999,
    0.197
   ],
   [
    "DUF6867",
    "Domain of unknown function (DUF6867)",
    0.998,
    0.271
   ],
   [
    "Fe-S_assembly",
    "Iron-sulphur cluster assembly",
    0.998,
    0.032
   ],
   [
    "FliJ",
    "Flagellar FliJ protein",
    0.998,
    0.233
   ],
   [
    "tRNA-synt_1c_C",
    "tRNA synthetases class I (E and Q), anti-codon binding domain",
    0.998,
    0.049
   ],
   [
    "tRNA-synt_1c_C2",
    "tRNA synthetases class I (E and Q), anti-codon binding domain",
    0.998,
    0.049
   ],
   [
    "GshA",
    "Glutamate-cysteine ligase",
    0.997,
    0.012
   ],
   [
    "RP005_N",
    "RP005 N-terminal alpha-helical domain",
    0.997,
    0.043
   ],
   [
    "Frataxin_Cyay",
    "Frataxin-like domain",
    0.995,
    0.035
   ],
   [
    "HSCB_C",
    "HSCB C-terminal oligomerisation domain",
    0.995,
    0.033
   ],
   [
    "MreD",
    "rod shape-determining protein MreD",
    0.993,
    0.197
   ],
   [
    "DUF6111",
    "Family of unknown function (DUF6111)",
    0.992,
    0.179
   ],
   [
    "PFK",
    "Phosphofructokinase",
    0.991,
    0.221
   ],
   [
    "Glucosaminidase",
    "Mannosyl-glycoprotein endo-beta-N-acetylglucosaminidase",
    0.99,
    0.069
   ],
   [
    "PrcB_C",
    "PrcB C-terminal",
    0.989,
    0.015
   ],
   [
    "A24_N_bact",
    "Bacterial Peptidase A24 N-terminal domain",
    0.988,
    0.186
   ],
   [
    "Csd3_N2",
    "Csd3 second domain",
    0.988,
    0.171
   ],
   [
    "DUF3362",
    "Domain of unknown function (DUF3362)",
    0.988,
    0.101
   ],
   [
    "Radical_SAM_N",
    "Radical SAM N-terminal",
    0.988,
    0.101
   ],
   [
    "DUF7088",
    "Domain of unknown function (DUF7088)",
    0.986,
    0.075
   ],
   [
    "UPF0020",
    "RMKL-like, methyltransferase domain",
    0.986,
    0.299
   ],
   [
    "FliX",
    "Class II flagellar assembly regulator",
    0.982,
    0.271
   ],
   [
    "DUF6468",
    "Domain of unknown function (DUF6468)",
    0.981,
    0.298
   ],
   [
    "STR4_M",
    "STR4 middle domain",
    0.98,
    0.122
   ],
   [
    "Exop_C",
    "Galactose-binding domain-like",
    0.979,
    0.136
   ],
   [
    "ATPase-cat_bd",
    "Putative metal-binding domain of cation transport ATPase",
    0.97,
    0.043
   ],
   [
    "GDT1",
    "Divalent cation/proton antiporter GDT1",
    0.97,
    0.185
   ],
   [
    "Maf_flag10_N",
    "Glycosyltransferase Maf N-terminal domain",
    0.97,
    0.012
   ],
   [
    "Zn_ribbon_Nudix",
    "Nudix N-terminal",
    0.967,
    0.112
   ],
   [
    "RlmL_1st",
    "RlmL ferredoxin-like domain",
    0.965,
    0.288
   ],
   [
    "Aq_678",
    "Aq_678",
    0.961,
    0.02
   ],
   [
    "DUF5935",
    "Family of unknown function (DUF5935)",
    0.96,
    0.173
   ],
   [
    "DUF3369",
    "Domain of unknown function (DUF3369)",
    0.957,
    0.105
   ],
   [
    "DUF4340",
    "Domain of unknown function (DUF4340)",
    0.957,
    0.071
   ],
   [
    "YajQ",
    "Nucleotide-binding protein YajQ-like",
    0.952,
    0.048
   ],
   [
    "DUF4197",
    "Protein of unknown function (DUF4197)",
    0.95,
    0.134
   ],
   [
    "DUF4743",
    "Domain of unknown function (DUF4743)",
    0.948,
    0.082
   ],
   [
    "NonGDSL",
    "Non-GDSL lipase-like family",
    0.947,
    0.177
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
   "cox2": 0.995,
   "cox3": 1.0,
   "cob": 1.0,
   "atp1/3": 1.0,
   "atp6": 1.0,
   "atp9": 1.0,
   "rpoB": 1.0,
   "rpoC": 1.0,
   "rpoA": 1.0,
   "secY": 1.0,
   "tatC": 1.0,
   "ccmB": 1.0,
   "ccmC": 1.0,
   "tufA": 1.0,
   "rps12": null,
   "rpl2": 1.0,
   "rpl14": 1.0
  }
 },
 "Rickettsiales (common ancestor)": {
  "n_tips_below": 40,
  "families_p_ge_0.9": 1138,
  "families_p_0.5_0.9": 310,
  "expected_families": 2073.6,
  "functions_top": [
   [
    "catalytic activity",
    285
   ],
   [
    "transferase activity",
    91
   ],
   [
    "helicase_nucleic",
    68
   ],
   [
    "hydrolase activity",
    60
   ],
   [
    "DNA binding",
    57
   ],
   [
    "oxidoreductase activity",
    50
   ],
   [
    "structural molecule activity",
    48
   ],
   [
    "organelle",
    47
   ],
   [
    "catalytic activity, acting on RNA",
    42
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
    37
   ],
   [
    "transporter activity",
    36
   ],
   [
    "ligase activity",
    34
   ],
   [
    "methyl_glyco_transferase",
    31
   ]
  ],
  "present_but_rare_today": [
   [
    "Csd3_N2",
    "Csd3 second domain",
    1.0,
    0.171
   ],
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
   
… (잘림, 원본 파일 참조)
```

## 연결
- [[실험 목록]]
