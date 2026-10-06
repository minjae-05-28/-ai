---
유형: 실험
실행: family_sequence
산출: results/family_sequence/metrics.json
tags:
  - 유형/실험
  - 실험/family_sequence
---

# 실험 · family_sequence

**산출물** `results/family_sequence/metrics.json`

## 한눈에

| 항목 | 값 |
| --- | --- |
| n_pairs | 57 |

## ivywrel

```json
{
 "axis": "colder",
 "uniform_share_of_family_variance": 0.2429368648126074,
 "families_tested": 2099,
 "median_sensitivity": 0.0239712862814852,
 "share_positive": 0.9056693663649357,
 "most_sensitive": [
  [
   "LpqE-like: Putative lipoprotein LpqE-like",
   0.1356
  ],
  [
   "UVR: UvrB/uvrC motif",
   0.108
  ],
  [
   "FtsX_ECD: FtsX extracellular domain",
   0.1016
  ],
  [
   "Smr: Smr domain",
   0.1008
  ],
  [
   "CcmH: Cytochrome C biogenesis protein",
   0.0971
  ],
  [
   "DUF3108: Protein of unknown function (DUF3108)",
   0.0946
  ],
  [
   "LTXXQ: LTXXQ motif family protein",
   0.0944
  ],
  [
   "Secretin_N: Bacterial type II/III secretion system short domain",
   0.0935
  ],
  [
   "Pyridox_oxase_2: Pyridoxamine 5'-phosphate oxidase, FMN-binding domain",
   0.0924
  ],
  [
   "GSHPx: Glutathione peroxidase",
   0.0914
  ],
  [
   "PspA_IM30: PspA/IM30 family",
   0.0907
  ],
  [
   "TPR_14: Tetratricopeptide repeat",
   0.0897
  ]
 ],
 "least_sensitive": [
  [
   "UPF0093: Protoporphyrinogen oxidase HemJ",
   -0.0464
  ],
  [
   "MAPEG: MAPEG family",
   -0.0469
  ],
  [
   "GST_C_3: Glutathione S-transferase, C-terminal domain",
   -0.0482
  ],
  [
   "FKBP_N: Domain amino terminal to FKBP-type peptidyl-prolyl isomerase",
   -0.0511
  ],
  [
   "Cons_hypoth698: Conserved hypothetical protein 698",
   -0.0536
  ],
  [
   "TetR_C_13: Tetracyclin repressor-like, C-terminal domain",
   -0.0545
  ],
  [
   "Rimk_N: RimK PreATP-grasp domain",
   -0.0563
  ],
  [
   "PolyA_pol_arg_C: Polymerase A arginine-rich C-terminus",
   -0.0581
  ],
  [
   "sCache_2: Single Cache domain 2",
   -0.0604
  ],
  [
   "PolyA_pol_RNAbd: Probable RNA and SrmB- binding site of polymerase A",
   -0.0829
  ],
  [
   "DUF493: Protein of unknown function (DUF493)",
   -0.0944
  ],
  [
   "Copper-bind: Copper binding proteins, plastocyanin/azurin family",
   -0.0956
  ]
 ],
 "feature_correlations": [
  [
   "hydrophobicity_gravy",
   -0.16312864689105405
  ],
  [
   "tm_helices",
   -0.12985374798727495
  ],
  [
   "kw:transporter_channel",
   -0.11448278597817009
  ],
  [
   "go:transporter activity",
   -0.08431938069382701
  ],
  [
   "hmm_length",
   -0.06542390544939804
  ],
  [
   "go:transmembrane transport",
   -0.06148036647724844
  ],
  [
   "protein_length",
   -0.05839410702202965
  ],
  [
   "ubiquity_free_living",
   0.05646643136721691
  ],
  [
   "kw:repeat_domain",
   0.04730885024798392
  ],
  [
   "kw:cilium_flagellum",
   0.044886511743429856
  ]
 ]
}
```

## acidic_excess

```json
{
 "axis": "saltier",
 "uniform_share_of_family_variance": 0.3091491903385355,
 "families_tested": 2099,
 "median_sensitivity": 0.018933482848515305,
 "share_positive": 0.8918532634587899,
 "most_sensitive": [
  [
   "Sortase: Sortase domain",
   0.1312
  ],
  [
   "Lipoprotein_9: NlpA lipoprotein",
   0.1297
  ],
  [
   "Ribosomal_L26: Ribosomal proteins L26 eukaryotic, L24P archaeal",
   0.1151
  ],
  [
   "Prefoldin_2: Prefoldin subunit",
   0.1125
  ],
  [
   "Lig_chan-Glu_bd: Ligated ion channel L-glutamate- and glycine-binding site",
   0.1112
  ],
  [
   "CAP: Cysteine-rich secretory protein family",
   0.1039
  ],
  [
   "PCB_OB: Penicillin-binding protein OB-like domain",
   0.0926
  ],
  [
   "sCache_3_2: Single cache domain 3",
   0.0905
  ],
  [
   "PolyA_pol_RNAbd: Probable RNA and SrmB- binding site of polymerase A",
   0.0899
  ],
  [
   "Prefoldin: Prefoldin subunit",
   0.0892
  ],
  [
   "ATP-synt_ab_Xtn: ATPsynthase alpha/beta subunit barrel-sandwich domain",
   0.0886
  ],
  [
   "Ribosomal_L19e_C: Ribosomal protein L19e, C-terminal domain",
   0.087
  ]
 ],
 "least_sensitive": [
  [
   "PolyA_pol_arg_C: Polymerase A arginine-rich C-terminus",
   -0.0427
  ],
  [
   "HTH_AsnC-type: AsnC-type helix-turn-helix domain",
   -0.0428
  ],
  [
   "PNK3P: Polynucleotide kinase 3 phosphatase",
   -0.0443
  ],
  [
   "UDPGT: UDP-glucoronosyl and UDP-glucosyl transferase",
   -0.0447
  ],
  [
   "DUF493: Protein of unknown function (DUF493)",
   -0.048
  ],
  [
   "rve: Integrase core domain",
   -0.0637
  ],
  [
   "SbcD_C: Type 5 capsule protein repressor C-terminal domain",
   -0.0661
  ],
  [
   "DUF402: Protein of unknown function (DUF402)",
   -0.0664
  ],
  [
   "PSP1: PSP1 C-terminal conserved region",
   -0.0691
  ],
  [
   "MotA_N: Motility protein A N-terminal",
   -0.0701
  ],
  [
   "HD_assoc: Phosphohydrolase-associated domain",
   -0.132
  ],
  [
   "HRDC: HRDC domain",
   -0.1437
  ]
 ],
 "feature_correlations": [
  [
   "tm_helices",
   -0.184424926806161
  ],
  [
   "hydrophobicity_gravy",
   -0.1711561564727651
  ],
  [
   "translation",
   0.13298573931332688
  ],
  [
   "ubiquity_free_living",
   0.1301399696336436
  ],
  [
   "kw:transporter_channel",
   -0.12751654971276252
  ],
  [
   "protein_length",
   -0.07381031172266964
  ],
  [
   "redox_core",
   -0.07252579007083933
  ],
  [
   "kw:protease",
   -0.06795946091260197
  ],
  [
   "hmm_length",
   -0.06597327796061334
  ],
  [
   "go:transporter activity",
   -0.06457652596765283
  ]
 ]
}
```

## 연결
- [[실험 목록]]
