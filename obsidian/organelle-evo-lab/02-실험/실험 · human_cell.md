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

… (잘림 — 원본 파일 참조)
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
    "Arm-DNA-bind_1: Bacteriophage lambda integrase, Arm
… (잘림 — 원본 파일 참조)
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
   "Tct
… (잘림 — 원본 파일 참조)
```

## 연결
- [[실험 목록]]
