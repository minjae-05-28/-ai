---
유형: 실험
실행: loss_order
산출: results/loss_order/metrics.json
tags:
  - 유형/실험
  - 실험/loss_order
---

# 실험 · loss_order

**산출물** `results/loss_order/metrics.json`

## 한눈에

| 항목 | 값 |
| --- | --- |
| n_cross_clade_comparisons | 2567 |
| mild_vs_harsh_spearman | 0.6633 |
| n_families | 6058 |

## containment_over_random

```json
{
 "median": 1.6182624645328165,
 "q25": 1.3596445933080368,
 "q75": 1.941122512083758,
 "share_above_1": 1.0
}
```

## severity

```json
{
 "Pyricularia oryzae": 0.04054350208196362,
 "Haemonchus contortus": 0.07273095623987035,
 "Brugia malayi": 0.0919773095623987,
 "Ustilago maydis": 0.11530299457675076,
 "Pediculus humanus": 0.11789749467823808,
 "Strongyloides ratti": 0.146677471636953,
 "Blumeria graminis": 0.14902476440937978,
 "Saprolegnia parasitica": 0.16666666666666666,
 "Puccinia graminis": 0.1671775524640415,
 "Aphanomyces astaci": 0.167779632721202,
 "Phytophthora infestans": 0.18753478018920422,
 "Trypanosoma cruzi": 0.18988132417239226,
 "Phytophthora sojae": 0.19671675013912077,
 "Trypanosoma grayi": 0.19706433479075577,
 "Leptomonas pyrrhocoris": 0.2061211742660837,
 "Leishmania major": 0.22361024359775142,
 "Clonorchis sinensis": 0.2246389730789802,
 "Leishmania infantum": 0.22517176764522173,
 "Leishmania mexicana": 0.22517176764522173,
 "Batrachochytrium dendrobatidis": 0.22520908004778972,
 "Pneumocystis jirovecii": 0.22531969309462915,
 "Trichinella spiralis": 0.22710696920583467,
 "Trypanosoma brucei": 0.23079325421611493,
 "Leishmania braziliensis": 0.23266708307307932,
 "Leishmania donovani": 0.23329169269206745,
 "Schistosoma mansoni": 0.24139775361026922,
 "Schistosoma japonicum": 0.2430023177036905,
 "Trypanosoma vivax": 0.24734540911930045,
 "Taphrina deformans": 0.24782608695652175,
 "Echinococcus multilocularis": 0.2583348190408272,
 "Angomonas deanei": 0.2598376014990631,
 "Malassezia globosa": 0.2758783305824098,
 "Helicosporidium sp. ATCC 50920": 0.300350498786735,
 "Perkinsus marinus": 0.312226437117012,
 "Ichthyophthirius multifiliis": 0.3233148526407937,
 "Strigomonas cul
… (잘림 — 원본 파일 참조)
```

## lost_first

```json
[
 "DUF2828: Domain of unknown function (DUF2828)",
 "DUF1499: Protein of unknown function (DUF1499)",
 "Toprim_4: Toprim domain",
 "AnmK: Anhydro-N-acetylmuramic acid kinase",
 "DUF5765: Family of unknown function (DUF5765)",
 "DUF5662: Family of unknown function (DUF5662)",
 "DUF4615: Domain of unknown function (DUF4615)",
 "DUF8771: Family of unknown function (DUF8771)",
 "DUF2854: Protein of unknown function (DUF2854)",
 "DUF1517: Protein of unknown function (DUF1517)",
 "DUF2678: Protein of unknown function (DUF2678)",
 "DUF2608: Protein of unknown function (DUF2608)"
]
```

## lost_only_by_harshest

```json
[
 "ABI: Abl interactor protein",
 "A2M_BRD: Alpha-2-macroglobulin bait region domain",
 "A2M: Alpha-2-macroglobulin family",
 "MVP_shoulder: Shoulder domain",
 "Mat89Bb: Cell cycle and development regulator Mat89Bb",
 "CLEC16A_helical: CLEC16A helical domain",
 "Mis12: Mis12 protein",
 "Mdm12: Mitochondrial distribution and morphology protein 12",
 "KilA-N: KilA-N domain",
 "LIS_MGM1: Dynamin-like GTPase MGM1-like, lipid interacting stalk",
 "Cep192_D4: Cep192 domain 4",
 "RHD_RETREG1-3: RETREG1-3/ARL6IP-like, N-terminal reticulon-homology domain"
]
```

## comparisons

```json
[
 {
  "milder": "Entamoeba histolytica",
  "harsher": "Encephalitozoon cuniculi",
  "containment": 0.8837075417386299,
  "null": 0.6756369882622387
 },
 {
  "milder": "Entamoeba histolytica",
  "harsher": "Nosema ceranae",
  "containment": 0.895797351755901,
  "null": 0.6908101918121958
 },
 {
  "milder": "Entamoeba histolytica",
  "harsher": "Enterocytozoon bieneusi",
  "containment": 0.9314910765687968,
  "null": 0.7646722015459491
 },
 {
  "milder": "Entamoeba histolytica",
  "harsher": "Nematocida parisii",
  "containment": 0.8877374784110535,
  "null": 0.6988262238763241
 },
 {
  "milder": "Entamoeba histolytica",
  "harsher": "Vavraia culicis",
  "containment": 0.8963730569948186,
  "null": 0.6979673632980247
 },
 {
  "milder": "Entamoeba histolytica",
  "harsher": "Encephalitozoon intestinalis",
  "containment": 0.8837075417386299,
  "null": 0.6722015459490409
 },
 {
  "milder": "Entamoeba histolytica",
  "harsher": "Theileria annulata",
  "containment": 0.6567524115755627,
  "null": 0.4573342736248237
 },
 {
  "milder": "Entamoeba histolytica",
  "harsher": "Theileria parva",
  "containment": 0.6430868167202572,
  "null": 0.4432299012693935
 },
 {
  "milder": "Entamoeba histolytica",
  "harsher": "Cryptosporidium hominis",
  "containment": 0.7411575562700965,
  "null": 0.4975317348377997
 },
 {
  "milder": "Entamoeba histolytica",
  "harsher": "Trypanosoma congolense",
  "containment": 0.7543859649122807,
  "null": 0.686536901865369
 },
 {
  "milder": "Entamoeba histolytica",
  "harsher": "Giardia intestinalis",
  "containment": 0.8819492107069321,
  "null": 0.6281
… (잘림 — 원본 파일 참조)
```

## 연결
- [[실험 목록]]
