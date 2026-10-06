---
유형: 실험
실행: modules
산출: results/modules/metrics.json
tags:
  - 유형/실험
  - 실험/modules
---

# 실험 · modules

**산출물** `results/modules/metrics.json`

## 한눈에

| 항목 | 값 |
| --- | --- |
| n_pairs | 90 |
| n_families | 8744 |
| reveal | 0.5 |
| best_k | 2 |

## ks

```json
[
 0,
 2,
 4,
 8
]
```

## mean_auroc_hidden

```json
{
 "k0": 0.8057457118932878,
 "k2": 0.8064437192820331,
 "k4": 0.8064259461138282,
 "k8": 0.8014734417844294
}
```

## by_clade

```json
{
 "alveolata": {
  "k0": 0.8461615981456221,
  "k2": 0.8440501952633737,
  "k4": 0.8438133075850841,
  "k8": 0.8381829220683641
 },
 "amoebozoa": {
  "k0": 0.8225142973964487,
  "k2": 0.8390614544242245,
  "k4": 0.8387133240456758,
  "k8": 0.8315935752574838
 },
 "chelicerata": {
  "k0": 0.7873363289926155,
  "k2": 0.7980455667450439,
  "k4": 0.7801836047212873,
  "k8": 0.7864425179267535
 },
 "chlorophyta": {
  "k0": 0.723998088119315,
  "k2": 0.7253033770304658,
  "k4": 0.7270791600922123,
  "k8": 0.7323926003702371
 },
 "cnidaria": {
  "k0": 0.8229793213511232,
  "k2": 0.8282563367270726,
  "k4": 0.8303024038381404,
  "k8": 0.8275912143760789
 },
 "crustacea": {
  "k0": 0.7803427203504684,
  "k2": 0.7852767544049203,
  "k4": 0.791639327752948,
  "k8": 0.8034224429242335
 },
 "discoba": {
  "k0": 0.7817489448564573,
  "k2": 0.7781046290837496,
  "k4": 0.7804524619131978,
  "k8": 0.7655232513407179
 },
 "fungi": {
  "k0": 0.8128560193284768,
  "k2": 0.8109526732690518,
  "k4": 0.80744205724236,
  "k8": 0.8015608458155489
 },
 "holozoa": {
  "k0": 0.7762447991574496,
  "k2": 0.7931546467387692,
  "k4": 0.803440341264427,
  "k8": 0.8146948732374589
 },
 "insecta": {
  "k0": 0.8107093409082581,
  "k2": 0.8178732417297585,
  "k4": 0.8248145001828481,
  "k8": 0.8215345421493435
 },
 "metamonada": {
  "k0": 0.8118495737406289,
  "k2": 0.8149391999541551,
  "k4": 0.8147891111555595,
  "k8": 0.8137623769889591
 },
 "nematoda": {
  "k0": 0.7596440076515506,
  "k2": 0.7663199589590391,
  "k4": 0.7710474102472823,
  "k8": 0.7624975822031579
 },
 "platyhelminthes": {
  "k0": 0.760718
… (잘림 — 원본 파일 참조)
```

## gain_vs_additive

```json
{
 "mean": 0.0006980073887451575,
 "n_better": 45,
 "n": 90
}
```

## heldout

```json
[
 {
  "pair": "Tetrahymena thermophila -> Ichthyophthirius multifiliis",
  "clade": "alveolata",
  "k0": 0.7540444166566217,
  "k2": 0.7582616984597647,
  "k4": 0.7515701779208724,
  "k8": 0.752100947975645
 },
 {
  "pair": "Tetrahymena thermophila -> Perkinsus marinus",
  "clade": "alveolata",
  "k0": 0.8287457078099038,
  "k2": 0.8184460800516314,
  "k4": 0.8174280467228017,
  "k8": 0.819305100936487
 },
 {
  "pair": "Chromera velia -> Plasmodium falciparum",
  "clade": "alveolata",
  "k0": 0.8473405666372695,
  "k2": 0.8442366034216141,
  "k4": 0.8439608325487994,
  "k8": 0.8388218583361571
 },
 {
  "pair": "Chromera velia -> Babesia bovis",
  "clade": "alveolata",
  "k0": 0.8605837480440823,
  "k2": 0.8590853229685615,
  "k4": 0.8618797643942085,
  "k8": 0.8591327449628238
 },
 {
  "pair": "Chromera velia -> Toxoplasma gondii",
  "clade": "alveolata",
  "k0": 0.8482983830503678,
  "k2": 0.8478584082809567,
  "k4": 0.846045621741966,
  "k8": 0.833912987754168
 },
 {
  "pair": "Chromera velia -> Eimeria tenella",
  "clade": "alveolata",
  "k0": 0.828641695782399,
  "k2": 0.8311133244273351,
  "k4": 0.8297227318729937,
  "k8": 0.8197897425274879
 },
 {
  "pair": "Chromera velia -> Cryptosporidium parvum",
  "clade": "alveolata",
  "k0": 0.8802674645092289,
  "k2": 0.8752595681322607,
  "k4": 0.875301828397526,
  "k8": 0.8687395298578515
 },
 {
  "pair": "Chromera velia -> Plasmodium vivax",
  "clade": "alveolata",
  "k0": 0.8429543212623819,
  "k2": 0.8422552081216365,
  "k4": 0.8389598887699581,
  "k8": 0.8349452535174215
 },
 {
  "pair": "Chromera velia -> Plasmodium be
… (잘림 — 원본 파일 참조)
```

## modules

```json
[
 {
  "strength": 296.1355285644531,
  "lost_together": [
   "VIT: Vault protein inter-alpha-trypsin domain",
   "Beta_helix: Right handed beta helix region",
   "SBF: Sodium Bile acid symporter family",
   "LacAB_rpiB: Ribose/Galactose Isomerase",
   "ASMase_C: Acid sphingomyelin phosphodiesterase C-terminal region",
   "UNC80_C: Protein UNC80 C-terminal region",
   "CNOT11: CCR4-NOT transcription complex subunit 11",
   "ANKRD13_C: ANKRD13 C-terminal"
  ],
  "lost_together_enriched": [
   [
    "kw:methyl_glyco_transferase",
    3.12
   ],
   [
    "go:hydrolase activity",
    2.7
   ]
  ],
  "kept_together": [
   "Cytidylate_kin: Cytidylate kinase",
   "MFS_3: Transmembrane secretion effector",
   "Bromo_TP_like: Histone-fold protein",
   "N6_Mtase: N-6 DNA Methylase",
   "HTH_Tnp_Tc3_2: Transposase",
   "Lipase_2: Lipase (class 2)",
   "PEPCK_PPi_lobe_2: PPi-type phosphoenolpyruvate carboxykinase lobe 2 domain",
   "PEPCK-like_mid: PEPCK-like middle domain"
  ],
  "kept_together_enriched": [
   [
    "go:DNA binding",
    5.79
   ],
   [
    "go:transferase activity",
    3.59
   ]
  ],
  "most_affected": [
   "Plasmodium vivax",
   "Plasmodium malariae",
   "Plasmodium knowlesi",
   "Plasmodium falciparum",
   "Plasmodium yoelii",
   "Plasmodium berghei"
  ],
  "least_affected": [
   "Leptomonas pyrrhocoris",
   "Saprolegnia parasitica",
   "Leishmania mexicana",
   "Leishmania major",
   "Leishmania infantum",
   "Leishmania donovani"
  ]
 },
 {
  "strength": 280.2524108886719,
  "lost_together": [
   "CDC37_C: Cdc37 C terminal domain",
   "SBP_bac_3: Bacterial extra
… (잘림 — 원본 파일 참조)
```

## 연결
- [[실험 목록]]
