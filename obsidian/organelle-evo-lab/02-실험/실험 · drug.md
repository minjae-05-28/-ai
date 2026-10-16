---
유형: 실험
실행: drug
산출: results/drug/summary.json
tags:
  - 유형/실험
  - 실험/drug
---

# 실험 · drug

**산출물** `results/drug/summary.json`

## 한눈에

| 항목 | 값 |
| --- | --- |
| lines | 1673 |
| tilt_vs_proliferation_r | 0.319 |
| A_tilt_selective_compounds_fdr10 | 13 |

## source

```json
{
 "l1000cds2_reverse": "https://maayanlab.cloud/L1000CDS2/query",
 "l1000cds2_mimic": "https://maayanlab.cloud/L1000CDS2/query",
 "depmap": "DepMap 24Q4 Public (figshare 27993248)",
 "signature_genes_found": {
  "up": 150,
  "down": 150,
  "proliferation": 1263
 },
 "expression_lines": 1673,
 "prism": "not found"
}
```

## B_dependencies

```json
{
 "odds_ratio": 1.79,
 "lo": 1.439,
 "hi": 2.259,
 "n_selected": 322,
 "uc_share_selected": 0.6087,
 "uc_share_all": 0.4673,
 "verdict": "양성"
}
```

## B_top_dependencies

```json
[
 "SCD\t-0.2241\t9.08e-10\t-0.8158\t",
 "PCYT1A\t-0.1852\t2.06e-06\t-0.8154\tPS1",
 "ITGA3\t-0.1781\t6.62e-06\t-0.1040\tPS5",
 "YJU2B\t-0.1764\t8.23e-06\t-0.5738\tPS2",
 "SREBF1\t-0.1707\t2.09e-05\t-0.3364\tPS3",
 "SCAP\t-0.1566\t0.000257\t-1.0043\tPS8",
 "CYB5B\t-0.1541\t0.000346\t-0.3235\tPS1",
 "PKMYT1\t-0.1490\t0.0007\t-1.2399\tPS1",
 "OR10T2\t-0.1489\t0.00117\t-0.1895\tPS8",
 "RXRA\t-0.1459\t0.00107\t-0.0683\tPS10",
 "PRELID3B\t-0.1448\t0.00117\t-1.6686\tPS3",
 "GRHL2\t-0.1439\t0.0013\t-0.1154\tPS3",
 "MBTPS1\t-0.1385\t0.00266\t-0.5775\tPS2",
 "RAB10\t-0.1383\t0.00266\t-0.4440\tPS2",
 "VPS26A\t-0.1381\t0.00266\t-0.2702\tPS2",
 "NPM2\t-0.1357\t0.00353\t0.1410\tPS5",
 "CAP1\t-0.1354\t0.00356\t-0.3487\tPS9",
 "JUNB\t-0.1349\t0.00356\t-0.2649\tPS6",
 "GMNN\t-0.1334\t0.00425\t-0.5261\tPS5",
 "CMPK1\t-0.1291\t0.00762\t-0.8981\tPS1"
]
```

## A_reverse

```json
{
 "l1000_named": 30,
 "l1000_brd": 32,
 "matched_in_prism": 21,
 "matched_names": [
  "ALVOCIDIB",
  "AMINOPURVALANOL-A",
  "AT-7519",
  "BI-2536",
  "BMS-387032",
  "BMS-536924",
  "CGP-60474",
  "DORSOMORPHIN",
  "ENROFLOXACIN",
  "EPIRUBICIN",
  "FLUDROCORTISONE-ACETATE",
  "GDC-0980",
  "GELDANAMYCIN",
  "GSK2126458",
  "ISX-9",
  "LY294002",
  "NVP-AUY922",
  "PD-0325901",
  "PD-184352",
  "SELUMETINIB",
  "VEMURAFENIB"
 ],
 "partial_rho": {
  "difference": -0.0354,
  "lo": -0.0583,
  "hi": -0.012,
  "n_group": 21,
  "n_rest": 6588,
  "verdict": "양성"
 },
 "mean_viability_group": -1.8025,
 "mean_viability_rest": -0.2829
}
```

## A_mimic

```json
{
 "l1000_named": 31,
 "l1000_brd": 41,
 "matched_in_prism": 15,
 "matched_names": [
  "BELINOSTAT",
  "BUTEIN",
  "CERULENIN",
  "GELDANAMYCIN",
  "GF109203X",
  "GPP-78",
  "IKK-2-INHIBITOR-V",
  "LIOTHYRONINE",
  "PELITINIB",
  "PIFITHRIN-MU",
  "PIK-75",
  "PX-12",
  "SB-218078",
  "TRICHOSTATIN-A",
  "VORINOSTAT"
 ],
 "partial_rho": {
  "difference": -0.0084,
  "lo": -0.0354,
  "hi": 0.018,
  "n_group": 15,
  "n_rest": 6594,
  "verdict": "무승부"
 },
 "mean_viability_group": -1.4942,
 "mean_viability_rest": -0.285
}
```

## A_lineage_only_reverse

```json
{
 "difference": -0.0292,
 "lo": -0.0526,
 "hi": -0.0067,
 "n_group": 21,
 "n_rest": 6588,
 "verdict": "양성"
}
```

## A_top_tilt_selective

```json
[
 "BRD-K28907958\tCD-437\tRETINOID RECEPTOR AGONIST\tRARG\t-0.1990\t0.0054\t-1.9445\t552",
 "BRD-K58811567\tHKI-357\tEGFR INHIBITOR\tEGFR\t-0.1820\t0.0683\t-2.4528\t470",
 "BRD-A42571354\tCETIRIZINE\tHISTAMINE RECEPTOR ANTAGONIST\tHRH1\t-0.1769\t0.0429\t0.1611\t551",
 "BRD-K39171998\tSTF-118804\tNAMPT INHIBITOR\tNAMPT\t-0.1751\t0.0429\t-2.9167\t551",
 "BRD-K12343256\tTRAMETINIB\tMEK INHIBITOR\tMAP2K1, MAP2K2\t-0.1743\t0.0429\t-0.6161\t551",
 "BRD-K29220403\tESZOPICLONE\tBENZODIAZEPINE RECEPTOR AGONIST\tGABRA1, GABRA2, GABRA3, GABRA4, GABRA5, GABRA6, GABRB1, GABRB2, GABRB3, GABRD, GABRE, GABRG1, GABRG2, GABRG3, GABRP, GABRQ, TSPO\t-0.1680\t0.0724\t-0.2043\t532",
 "BRD-K81016934\tINC-280\tC-MET INHIBITOR\tMET\t-0.1671\t0.0724\t-0.5565\t532",
 "BRD-K00003331\tNIM811\tMITOCHONDRIAL PERMEABILITY TRANSITION INHIBITOR\t\t-0.1596\t0.0054\t-0.2332\t873",
 "BRD-A64173453\tOCTREOTIDE\tSOMATOSTATIN RECEPTOR AGONIST\tSSTR1, SSTR2, SSTR3, SSTR5\t-0.1583\t0.0927\t-0.0412\t534",
 "BRD-K73469236\tNEDAPLATIN\tDNA INHIBITOR\t\t-0.1580\t0.0927\t-0.0825\t539",
 "BRD-K21025364\tNVP-TAE226\tPROTEIN TYROSINE KINASE INHIBITOR\tPTK2\t-0.1556\t0.0927\t-1.5758\t549",
 "BRD-K31606909\tMETARRESTIN\t\t\t-0.1275\t0.0853\t-0.5535\t858",
 "BRD-K00003165\tSARDOMOZIDE\tS-ADENOSYLMETHIONINE DECARBOXYLASE INHIBITOR\t\t-0.1236\t0.0927\t-2.7519\t873"
]
```

## dependencies_with_tilt_selective_drug

```json
[
 "BRD-K58811567\tHKI-357\tEGFR INHIBITOR\tEGFR\t-0.1820\t0.0683\t-2.4528\t470"
]
```

## 연결
- [[실험 목록]]
