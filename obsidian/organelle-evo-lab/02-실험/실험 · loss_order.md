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
 "Strigomonas culicis": 0.3297938788257339,
 "Hammondia hammondi": 0.3750915750915751,
 "Toxoplasma gondii": 0.3785103785103785,
 "Rozella allomycis": 0.38211867781760256,
 "Besnoitia besnoiti": 0.3831501831501832,
 "Neospora caninum": 0.39902319902319905,
 "Trichomonas vaginalis": 0.46588935747953364,
 "Blastocystis hominis": 0.4666110183639399,
 "Tritrichomonas foetus": 0.46985859588191514,
 "Cyclospora cayetanensis": 0.47545787545787543,
 "Plasmodium knowlesi": 0.49621489621489623,
 "Plasmodium malariae": 0.503052503052503,
 "Eimeria tenella": 0.5037851037851038,
 "Plasmodium yoelii": 0.5042735042735043,
 "Plasmodium vivax": 0.5057387057387057,
 "Plasmodium berghei": 0.5081807081807082,
 "Plasmodium falciparum": 0.5084249084249084,
 "Babesia bovis": 0.5699633699633699,
 "Cryptosporidium parvum": 0.5706959706959707,
 "Babesia microti": 0.5728937728937729,
 "Entamoeba histolytica": 0.5737122557726465,
 "Theileria parva": 0.5775335775335775,
 "Entamoeba dispar": 0.5783747779751333,
 "Entamoeba invadens": 0.5801509769094139,
 "Gregarina niphandrodes": 0.5846153846153846,
 "Theileria annulata": 0.5885225885225885,
 "Henneguya salminicola": 0.6120176910172335,
 "Cryptosporidium hominis": 0.6192918192918193,
 "Mitosporidium daphniae": 0.6270410195141378,
 "Thelohanellus kitauei": 0.6641756901021809,
 "Giardia intestinalis": 0.672041677003225,
 "Spironucleus salmonicida": 0.6985859588191515,
 "Trypanosoma congolense": 0.7117426608369769,
 "Encephalitozoon intestinalis": 0.7566706491437675,
 "Encephalitozoon cuniculi": 0.7578653922739944,
 "Edhazardia aedis": 0.7682198327359617,
 "Nosema ceranae": 0.7702110712863401,
 "Vavraia culicis": 0.7737953006770211,
 "Nematocida parisii": 0.7757865392273995,
 "Nosema bombycis": 0.781162883313421,
 "Anncaliia algerae": 0.7863401035444046,
 "Pseudoloma neurophilia": 0.806252489048188,
 "Enterocytozoon bieneusi": 0.8245718837116687,
 "Fasciola hepatica": 0.9679087181315743
}
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
  "null": 0.6281486146095718
 },
 {
  "milder": "Entamoeba histolytica",
  "harsher": "Spironucleus salmonicida",
  "containment": 0.8991077556623198,
  "null": 0.6580604534005038
 },
 {
  "milder": "Entamoeba histolytica",
  "harsher": "Thelohanellus kitauei",
  "containment": 0.6908284023668639,
  "null": 0.5187483837600206
 },
 {
  "milder": "Entamoeba histolytica",
  "harsher": "Henneguya salminicola",
  "containment": 0.6301775147928994,
  "null": 0.44065166795965865
 },
 {
  "milder": "Entamoeba histolytica",
  "harsher": "Mitosporidium daphniae",
  "containment": 0.7202072538860104,
  "null": 0.5127397652447753
 },
 {
  "milder": "Entamoeba histolytica",
  "harsher": "Edhazardia aedis",
  "containment": 0.8911917098445595,
  "null": 0.6905239049527626
 },
 {
  "milder": "Entamoeba histolytica",
  "harsher": "Anncaliia algerae",
  "containment": 0.9107656879677605,
  "null": 0.7148582880045806
 },
 {
  "milder": "Entamoeba histolytica",
  "harsher": "Nosema bombycis",
  "containment": 0.899251583189407,
  "null": 0.706269682221586
 },
 {
  "milder": "Entamoeba histolytica",
  "harsher": "Pseudoloma neurophilia",
  "containment": 0.9251583189407023,
  "null": 0.740051531634698
 },
 {
  "milder": "Entamoeba histolytica",
  "harsher": "Gregarina niphandrodes",
  "containment": 0.7057877813504824,
  "null": 0.45557122708039494
 },
 {
  "milder": "Entamoeba histolytica",
  "harsher": "Fasciola hepatica",
  "containment": 0.970554926387316,
  "null": 0.9588616511693435
 },
 {
  "milder": "Ichthyophthirius multifiliis",
  "harsher": "Entamoeba histolytica",
  "containment": 0.5753246753246753,
  "null": 0.4033798677443057
 },
 {
  "milder": "Ichthyophthirius multifiliis",
  "harsher": "Rozella allomycis",
  "containment": 0.359375,
  "null": 0.20254506892895016
 },
 {
  "milder": "Ichthyophthirius multifiliis",
  "harsher": "Encephalitozoon cuniculi",
  "containment": 0.7955729166666666,
  "null": 0.632378932484977
 },
 {
  "milder": "Ichthyophthirius multifiliis",
  "harsher": "Nosema ceranae",
  "containment": 0.80859375,
  "null": 0.6447507953340403
 },
 {
  "milder": "Ichthyophthirius multifiliis",
  "harsher": "Enterocytozoon bieneusi",
  "containment": 0.8854166666666666,
  "null": 0.7299399080947331
 },
 {
  "milder": "Ichthyophthirius multifiliis",
  "harsher": "Nematocida parisii",
  "containment": 0.8033854166666666,
  "null": 0.6557087310003534
 },
 {
  "milder": "Ichthyophthirius multifiliis",
  "harsher": "Vavraia culicis",
  "containment": 0.8125,
  "null": 0.6528808766348533
 },
 {
  "milder": "Ichthyophthirius multifiliis",
  "harsher": "Encephalitozoon intestinalis",
  "containment": 0.7994791666666666,
  "null": 0.6288441145281018
 },
 {
  "milder": "Ichthyophthirius multifiliis",
  "harsher": "Trypanosoma congolense",
  "containment": 0.7934990439770554,
  "null": 0.6675246675246675
 },
 {
  "milder": "Ichthyophthirius multifiliis",
  "harsher": "Entamoeba dispar",
  "containment": 0.5935064935064935,
  "null": 0.4118295371050698
 },
 {
  "milder": "Ichthyophthirius multifiliis",
  "harsher": "Entamoeba invadens",
  "containment": 0.5974025974025974,
  "null": 0.4136664217487142
 },
 {
  "milder": "Ichthyophthirius multifiliis",
  "harsher": "Giardia intestinalis",
  "containment": 0.7933042212518195,
  "null": 0.5475299401197605
 },
 {
  "milder": "Ichthyophthirius multifiliis",
  "harsher": "Spironucleus salmonicida",
  "containment": 0.8311499272197962,
  "null": 0.5812125748502994
 },
 {
  "milder": "Ichthyophthirius multifiliis",
  "harsher": "Blastocystis hominis",
  "containment": 0.5332167832167832,
  "null": 0.31395842172252864
 },
 {
  "milder": "Ichthyophthirius multifiliis",
  "harsher": "Thelohanellus kitauei",
  "containment": 0.6472491909385113,
  "null": 0.4764971023824855
 },
 {
  "milder": "Ichthyophthirius multifiliis",
  "harsher": "Henneguya salminicola",
  "containment": 0.5685005393743258,
  "null": 0.4040566645202833
 },
 {
  "milder": "Ichthyophthirius multifiliis",
  "harsher": "Mitosporidium daphniae",
  "containment": 0.64453125,
  "null": 0.45811240721102864
 },
 {
  "milder": "Ichthyophthirius multifiliis",
  "harsher": "Edhazardia aedis",
  "containment": 0.8138020833333334,
  "null": 0.6443973135383527
 },
 {
  "milder": "Ichthyophthirius multifiliis",
  "harsher": "Anncaliia algerae",
  "containment": 0.8255208333333334,
  "null": 0.6698480028278544
 },
 {
  "milder": "Ichthyophthiriu
… (잘림, 원본 파일 참조)
```

## 연결
- [[실험 목록]]
