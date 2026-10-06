---
유형: 실험
실행: human_cell
산출: results/human_cell/metrics.json
tags:
  - 유형/실험
  - 실험/human_cell
---

# 실험 · human_cell

**산출물** `results/human_cell/metrics.json`

## 한눈에

| 항목 | 값 |
| --- | --- |
| note | Prediction from laws trained on other systems; human commensals are held out. |

## sites

```json
{
 "gut lumen (anaerobic, nutrient-rich)": {
  "group": "human",
  "temp": 37,
  "nacl": 0.9,
  "aerobic": 0,
  "radiation": 0,
  "oligo": 0
 },
 "skin surface (aerobic, dry, nutrient-poor)": {
  "group": "human",
  "temp": 33,
  "nacl": 2.0,
  "aerobic": 1,
  "radiation": 0,
  "oligo": 1
 },
 "blood and tissue (aerobic, nutrient-rich)": {
  "group": "human",
  "temp": 37,
  "nacl": 0.9,
  "aerobic": 1,
  "radiation": 0,
  "oligo": 0
 }
}
```

## composition

```json
{
 "gut lumen (anaerobic, nutrient-rich)": {
  "predicted": {
   "ivywrel": 0.3956,
   "cvp": 0.0254,
   "acidic_excess": 0.0024,
   "n_side": 0.3187
  },
  "observed_commensals": {
   "ivywrel": 0.3851,
   "cvp": 0.0309,
   "acidic_excess": 0.0123,
   "n_side": 0.3381
  },
  "n_commensals": 6,
  "commensals": [
   "Bacteroides thetaiotaomicron",
   "Bifidobacterium longum",
   "Akkermansia muciniphila",
   "Faecalibacterium prausnitzii",
   "Streptococcus salivarius",
   "Lactobacillus crispatus"
  ],
  "errors": {
   "ivywrel": 0.0105,
   "cvp": -0.0055,
   "acidic_excess": -0.0099,
   "n_side": -0.0194
  }
 },
 "skin surface (aerobic, dry, nutrient-poor)": {
  "predicted": {
   "ivywrel": 0.3892,
   "cvp": 0.0469,
   "acidic_excess": 0.0045,
   "n_side": 0.3094
  },
  "observed_commensals": {
   "ivywrel": 0.3924,
   "cvp": 0.019,
   "acidic_excess": 0.0234,
   "n_side": 0.3322
  },
  "n_commensals": 2,
  "commensals": [
   "Staphylococcus epidermidis",
   "Corynebacterium glutamicum"
  ],
  "errors": {
   "ivywrel": -0.0032,
   "cvp": 0.0279,
   "acidic_excess": -0.0189,
   "n_side": -0.0228
  }
 },
 "blood and tissue (aerobic, nutrient-rich)": {
  "predicted": {
   "ivywrel": 0.3962,
   "cvp": 0.0412,
   "acidic_excess": 0.0136,
   "n_side": 0.3267
  },
  "observed_commensals": {
   "ivywrel": 0.3933,
   "cvp": 0.0143,
   "acidic_excess": 0.0111,
   "n_side": 0.3497
  },
  "n_commensals": 2,
  "commensals": [
   "Escherichia coli",
   "Staphylococcus epidermidis"
  ],
  "errors": {
   "ivywrel": 0.0029,
   "cvp": 0.0269,
   "acidic_excess": 0.0025,
   "n_side": -0.023
  }
 }
}
```

## genome_size

```json
{
 "commensal_genes": {
  "Bacteroides thetaiotaomicron": 4596,
  "Bifidobacterium longum": 1871,
  "Akkermansia muciniphila": 2344,
  "Faecalibacterium prausnitzii": 2848,
  "Escherichia coli": 5098,
  "Cutibacterium acnes": 2304,
  "Staphylococcus epidermidis": 2189,
  "Corynebacterium glutamicum": 2925,
  "Streptococcus salivarius": 1917,
  "Lactobacillus crispatus": 1860
 },
 "free_living_median": 3215.0,
 "severity_reference": {}
}
```

## gene_content

```json
{
 "per_ancestor": {
  "Bacillus subtilis": {
   "families_today": 3136,
   "most_likely_lost": [
    "CarbopepD_reg_2: CarboxypepD_reg-like domain",
    "TctC: Tripartite tricarboxylate transporter family receptor",
    "CarboxypepD_reg: Carboxypeptidase regulatory-like domain",
    "DUF4181: Domain of unknown function (DUF4181)",
    "TEN_YD-shell: Teneurin YD-shell",
    "DUF5344: Family of unknown function (DUF5344)",
    "LCAT: Lecithin:cholesterol acyltransferase",
    "DUF6044: Protein of unknown function (DUF6044)",
    "4HB_MCP_1: Four helix bundle sensory module for signal transduction",
    "ECF_trnsprt: ECF transporter, substrate-specific component"
   ],
   "most_likely_kept": [
    "MarR: MarR family",
    "BPD_transp_1: Binding-protein-dependent transport system inner membrane component",
    "MarR_2: MarR family",
    "MMR_HSR1: 50S ribosome-binding GTPase",
    "Acetyltransf_7: Acetyltransferase (GNAT) domain",
    "HTH_27: Winged helix DNA-binding domain",
    "FR47: FR47-like protein",
    "PP-binding: Phosphopantetheine attachment site",
    "Acetyltransf_10: Acetyltransferase (GNAT) domain",
    "tRNA-synt_2b: tRNA synthetase class II core domain (G, H, P, S and T)"
   ]
  },
  "Pseudomonas putida": {
   "families_today": 3156,
   "most_likely_lost": [
    "Fimbrial: Fimbrial protein",
    "TctC: Tripartite tricarboxylate transporter family receptor",
    "FecR_C: FecR, C-terminal",
    "PapD_C: Pili assembly chaperone PapD, C-terminal domain",
    "DUF3077: Protein of unknown function (DUF3077)",
    "Arm-DNA-bind_1: Bacteriophage lambda integrase, Arm DNA-binding domain",
    "NEL: C-terminal novel E3 ligase, LRR-interacting",
    "PTS_EIIC: Phosphotransferase system, EIIC",
    "KshA_C: 3-Ketosteroid 9alpha-hydroxylase C-terminal domain",
    "LIP: Secretory lipase"
   ],
   "most_likely_kept": [
    "AAA_5: AAA domain (dynein-related subfamily)",
    "BPD_transp_1: Binding-protein-dependent transport system inner membrane component",
    "SBP_bac_3: Bacterial extracellular solute-binding proteins, family 3",
    "Cupin_2: Cupin domain",
    "Sigma54_activat: Sigma-54 interaction domain",
    "Sigma70_r4_2: Sigma-70, region 4",
    "Sigma70_r4: Sigma-70, region 4",
    "Gln-synt_C: Glutamine synthetase, catalytic domain",
    "AraC_binding: AraC-like ligand binding domain",
    "MMR_HSR1: 50S ribosome-binding GTPase"
   ]
  },
  "Micrococcus luteus": {
   "families_today": 1821,
   "most_likely_lost": [
    "TctC: Tripartite tricarboxylate transporter family receptor",
    "MULE: MULE transposase domain",
    "HisKA_2: Histidine kinase",
    "WXG100: Proteins of 100 residues with WXG",
    "LIP: Secretory lipase",
    "HWE_HK: HWE histidine kinase",
    "GST_N_2: Glutathione S-transferase, N-terminal domain",
    "Lsr2_DNA-bd: Lsr2 DNA-binding domain",
    "DUF885: Bacterial protein of unknown function (DUF885)",
    "Peripla_BP_1: Periplasmic binding proteins and sugar binding domain of LacI family"
   ],
   "most_likely_kept": [
    "BPD_transp_1: Binding-protein-dependent transport system inner membrane component",
    "MMR_HSR1: 50S ribosome-binding GTPase",
    "tRNA-synt_1g: tRNA synthetases class I (M)",
    "tRNA-synt_2b: tRNA synthetase class II core domain (G, H, P, S and T)",
    "tRNA-synt_1: tRNA synthetases class I (I, L, M and V)",
    "GTP_EFTU: Elongation factor Tu GTP binding domain",
    "ATP-synt_ab: ATP synthase alpha/beta family, nucleotide-binding domain",
    "tRNA-synt_2d: tRNA synthetases class II core domain (F)",
    "AAA_19: AAA domain",
    "GTP_EFTU_D2: Elongation factor Tu domain 2"
   ]
  }
 },
 "validation_auroc": {
  "Bacteroides thetaiotaomicron": {
   "Bacillus subtilis": 0.8931925097845066,
   "Bacillus subtilis (memorisation)": 0.930595505137248,
   "Bacillus subtilis (rarity baseline)": 0.93714526706966,
   "Pseudomonas putida": 0.8571700535137367,
   "Pseudomonas putida (memorisation)": 0.91462643202663,
   "Pseudomonas putida (rarity baseline)": 0.9229027065323387,
   "Micrococcus luteus": 0.882926809409172,
   "Micrococcus luteus (memorisation)": 0.9197846920469319,
   "Micrococcus luteus (rarity baseline)": 0.9281630564881436
  },
  "Bifidobacterium longum": {
   "Bacillus subtilis": 0.8644835480947145,
   "Bacillus subtilis (memorisation)": 0.8981436143846482,
   "Bacillus subtilis (rarity baseline)": 0.9105100994435287,
   "Pseudomonas putida": 0.8426511576773593,
   "Pseudomonas putida (memorisation)": 0.901305876443998,
   "Pseudomonas putida (rarity baseline)": 0.9144491413075578,
   "Micrococcus luteus": 0.8104706450377073,
   "Micrococcus luteus (memorisation)": 0.8130120127842475,
   "Micrococcus luteus (rarity baseline)": 0.8318761250505124
  },
  "Akkermansia muciniphila": {
   "Bacillus subtilis": 0.8900544048465158,
   "Bacillus subtilis (memorisation)": 0.9313202270958134,
   "Bacillus subtilis (rarity baseline)": 0.9378282905201881,
   "Pseudomonas putida": 0.8547787335696343,
   "Pseudomonas putida (memorisation)": 0.9105571293905791,
   "Pseudomonas putida (rarity baseline)": 0.9179785720412209,
   "Micrococcus luteus": 0.8616520166547504,
   "Micrococcus luteus (memorisation)": 0.9082207471877173,
   "Micrococcus luteus (rarity baseline)": 0.9171901169939314
  },
  "Faecalibacterium prausnitzii": {
   "Bacillus subtilis": 0.858665481948387,
   "Bacillus subtilis (memorisation)": 0.8808200410478703,
   "Bacillus subtilis (rarity baseline)": 0.8917089356639883,
   "Pseudomonas putida": 0.8595414298929562,
   "Pseudomonas putida (memorisation)": 0.9096556181445752,
   "Pseudomonas putida (rarity baseline)": 0.9199387554513017,
   "Micrococcus luteus": 0.8451052882988676,
   "Micrococcus luteus (memorisation)": 0.89245267997532,
   "Micrococcus luteus (rarity baseline)": 0.9070200077622753
  },
  "Streptococcus salivarius": {
   "Bacillus subtilis": 0.8552973945736523,
   "Bacillus subtilis (memorisation)": 0.8626295057861064,
   "Bacillus subtilis (rarity baseline)": 0.8779825016743438,
   "Pseudomonas puti
… (잘림, 원본 파일 참조)
```

## optimal_cell

```json
{
 "gut lumen (anaerobic, nutrient-rich)": {
  "pool_families": 3186,
  "kept_families": 2726,
  "share_of_pool_kept": 0.856,
  "functions_kept": [
   [
    "go:catalytic activity, acting on RNA",
    1.11
   ],
   [
    "go:amino acid metabolic process",
    1.11
   ],
   [
    "kw:helicase_nucleic",
    1.11
   ]
  ],
  "functions_dropped": [
   [
    "go:oxidoreductase activity",
    2.06
   ],
   [
    "kw:repeat_domain",
    2.0
   ],
   [
    "kw:lipid_metabolism",
    1.82
   ],
   [
    "kw:protease",
    1.46
   ],
   [
    "kw:uncharacterised",
    1.41
   ],
   [
    "go:transmembrane transport",
    1.39
   ],
   [
    "kw:transporter_channel",
    1.38
   ]
  ],
  "most_favoured": [
   "vATP-synt_E: ATP synthase (E/31 kDa) subunit",
   "ATP-synt_ab_Xtn: ATPsynthase alpha/beta subunit barrel-sandwich domain",
   "ATP-synt_I: ATP synthase I chain",
   "vATP-synt_AC39: ATP synthase (C/AC39) subunit",
   "ATP-synt_D: ATP synthase subunit D",
   "ATP-synt_DE: ATP synthase, Delta/Epsilon chain, long alpha-helix domain",
   "ATP-synt_ab: ATP synthase alpha/beta family, nucleotide-binding domain",
   "ATP-synt_F: ATP synthase (F/14-kDa) subunit",
   "Bac_DNA_binding: Bacterial DNA-binding protein",
   "ATP-synt_B: ATP synthase B/B' CF(0)",
   "OSCP: ATP synthase delta (OSCP) subunit",
   "ATP-synt_ab_N: ATP synthase alpha/beta family, beta-barrel domain",
   "ATP-synt_A: ATP synthase A chain",
   "ATP-synt: ATP synthase",
   "ATP-synt_VA_C: C-terminal domain of V and A type ATP synthase"
  ],
  "most_disfavoured": [
   "Uma2: Putative restriction endonuclease",
   "TctC: Tripartite tricarboxylate transporter family receptor",
   "TonB_dep_Rec_b-barrel: TonB dependent receptor-like, beta-barrel",
   "CarbopepD_reg_2: CarboxypepD_reg-like domain",
   "CarboxypepD_reg: Carboxypeptidase regulatory-like domain",
   "Plug: TonB-dependent Receptor Plug Domain",
   "Oxidored_nitro: Nitrogenase component 1 type Oxidoreductase",
   "Porin_4: Gram-negative porin",
   "Transposase_mut: Transposase, Mutator family",
   "OMP_b-brl_3: Outer membrane protein beta-barrel family",
   "TauD: Taurine catabolism dioxygenase TauD, TfdA family",
   "ABC_tran: ABC transporter",
   "HisKA_2: Histidine kinase",
   "Arabinose_bd: Arabinose-binding domain of AraC transcription regulator, N-term",
   "OrfB_IS605: Probable transposase"
  ],
  "kept_in_most_free_living_too": 1600,
  "kept_though_rare_in_free_living": []
 },
 "skin surface (aerobic, dry, nutrient-poor)": {
  "pool_families": 3186,
  "kept_families": 2659,
  "share_of_pool_kept": 0.835,
  "functions_kept": [
   [
    "kw:helicase_nucleic",
    1.14
   ],
   [
    "go:catalytic activity, acting on RNA",
    1.13
   ],
   [
    "go:amino acid metabolic process",
    1.13
   ],
   [
    "go:organelle",
    1.12
   ],
   [
    "go:ligase activity",
    1.12
   ]
  ],
  "functions_dropped": [
   [
    "kw:cilium_flagellum",
    2.65
   ],
   [
    "kw:repeat_domain",
    2.11
   ],
   [
    "go:regulation of DNA-templated transcription",
    1.93
   ],
   [
    "go:transmembrane transport",
    1.78
   ],
   [
    "go:carbohydrate metabolic process",
    1.77
   ],
   [
    "kw:methyl_glyco_transferase",
    1.64
   ],
   [
    "kw:transporter_channel",
    1.58
   ]
  ],
  "most_favoured": [
   "CarbopepD_reg_2: CarboxypepD_reg-like domain",
   "ABC_tran: ABC transporter",
   "adh_short: short chain dehydrogenase",
   "Methyltransf_25: Methyltransferase domain",
   "FAD_binding_2: FAD binding domain",
   "Epimerase: NAD dependent epimerase/dehydratase family",
   "TPR_8: Tetratricopeptide repeat",
   "Methyltransf_31: Methyltransferase domain",
   "TPR_16: Tetratricopeptide repeat",
   "Pyr_redox_2: Pyridine nucleotide-disulphide oxidoreductase",
   "TPR_19: Tetratricopeptide repeat",
   "NAD_binding_8: NAD(P)-binding Rossmann-like domain",
   "BPD_transp_1: Binding-protein-dependent transport system inner membrane component",
   "Aminotran_1_2: Aminotransferase class I and II",
   "Methyltransf_12: Methyltransferase domain"
  ],
  "most_disfavoured": [
   "Transposase_mut: Transposase, Mutator family",
   "Flagellin_N: Bacterial flagellin N-terminal helical region",
   "Glyco_hydro_43: Glycosyl hydrolases family 43",
   "Glyco_hydro_20: Glycosyl hydrolase family 20, catalytic domain",
   "Porin_4: Gram-negative porin",
   "TctC: Tripartite tricarboxylate transporter family receptor",
   "Glyco_hydro_2: Glycosyl hydrolases family 2",
   "FleQ: Flagellar regulatory protein FleQ",
   "FapA: Flagellar Assembly Protein A beta solenoid domain",
   "OprB: Carbohydrate-selective porin, OprB family",
   "Glyco_hydro_18: Glycosyl hydrolases family 18",
   "HisKA_2: Histidine kinase",
   "Glyco_hydro_2_N: Glycosyl hydrolases family 2, sugar binding domain",
   "Flagellin_IN: Flagellin hook IN motif",
   "Glyco_hydro_2_C: Glycosyl hydrolases family 2, TIM barrel domain"
  ],
  "kept_in_most_free_living_too": 1607,
  "kept_though_rare_in_free_living": []
 },
 "blood and tissue (aerobic, nutrient-rich)": {
  "pool_families": 3186,
  "kept_families": 2677,
  "share_of_pool_kept": 0.84,
  "functions_kept": [
   [
    "kw:helicase_nucleic",
    1.13
   ],
   [
    "go:catalytic activity, acting on RNA",
    1.13
   ],
   [
    "go:amino acid metabolic process",
    1.12
   ],
   [
    "go:organelle",
    1.12
   ],
   [
    "go:ligase activity",
    1.12
   ]
  ],
  "functions_dropped": [
   [
    "kw:repeat_domain",
    3.51
   ],
   [
    "kw:transporter_channel",
    2.17
   ],
   [
    "go:transmembrane transport",
    2.1
   ],
   [
    "kw:methyl_glyco_transferase",
    1.96
   ],
   [
    "go:transporter activity",
    1.66
   ],
   [
    "go:carbohydrate metabolic process",
    1.61
   ],
   [
    "go:regulation of DNA-templated transcription",
    1.49
   ]
  ],
  "most_favoured": [
   "AAA_5: AAA domain (dynein-related subfamily)",
   "ATP-synt_ab: ATP synthase alpha/beta family, nucleotide-binding domain",
   "RNA_pol_Rpb2_6: RNA polymerase Rpb2, domain 6",
… (잘림, 원본 파일 참조)
```

## 연결
- [[실험 목록]]
