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
    "tRNA synthetases class I (E and Q), anti-codon binding 
… (잘림 — 원본 파일 참조)
```

## 연결
- [[실험 목록]]
