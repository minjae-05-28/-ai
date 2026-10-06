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
  "k0": 0.760718905792286,
  "k2": 0.7669432955291745,
  "k4": 0.7800929739466959,
  "k8": 0.7804729012080406
 },
 "stramenopiles": {
  "k0": 0.832880893063398,
  "k2": 0.8375300706099219,
  "k4": 0.8304508899678351,
  "k8": 0.8349819835929523
 },
 "streptophyta": {
  "k0": 0.7331796112473159,
  "k2": 0.7085476295959003,
  "k4": 0.7004587221987053,
  "k8": 0.6990794094203578
 }
}
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
  "pair": "Chromera velia -> Plasmodium berghei",
  "clade": "alveolata",
  "k0": 0.8476317461598292,
  "k2": 0.8437791806147507,
  "k4": 0.8441001675739023,
  "k8": 0.8397221669387465
 },
 {
  "pair": "Chromera velia -> Plasmodium knowlesi",
  "clade": "alveolata",
  "k0": 0.8473988451101393,
  "k2": 0.8462048197304934,
  "k4": 0.8432084950846582,
  "k8": 0.8380598894887387
 },
 {
  "pair": "Chromera velia -> Theileria annulata",
  "clade": "alveolata",
  "k0": 0.859038107917062,
  "k2": 0.8576050285658344,
  "k4": 0.8629273441245022,
  "k8": 0.857479822801857
 },
 {
  "pair": "Chromera velia -> Theileria parva",
  "clade": "alveolata",
  "k0": 0.8621673836763537,
  "k2": 0.8622021695152303,
  "k4": 0.8658954519322634,
  "k8": 0.8633664018496869
 },
 {
  "pair": "Chromera velia -> Babesia microti",
  "clade": "alveolata",
  "k0": 0.8539132957446024,
  "k2": 0.8490506285845759,
  "k4": 0.8536215860706414,
  "k8": 0.8501057266405571
 },
 {
  "pair": "Chromera velia -> Neospora caninum",
  "clade": "alveolata",
  "k0": 0.8460295956934214,
  "k2": 0.8471018733287524,
  "k4": 0.8435989869840578,
  "k8": 0.8335454121085082
 },
 {
  "pair": "Chromera velia -> Hammondia hammondi",
  "clade": "alveolata",
  "k0": 0.8476733731250707,
  "k2": 0.8465295823969474,
  "k4": 0.8430879833861953,
  "k8": 0.8323829401286534
 },
 {
  "pair": "Chromera velia -> Cyclospora cayetanensis",
  "clade": "alveolata",
  "k0": 0.8393725582889643,
  "k2": 0.8364926691611351,
  "k4": 0.8377094698684365,
  "k8": 0.828484980798219
 },
 {
  "pair": "Chromera velia -> Cryptosporidium hominis",
  "clade": "alveolata",
  "k0": 0.8643301425795619,
  "k2": 0.8568958662852538,
  "k4": 0.8567236560134127,
  "k8": 0.8504003483318382
 },
 {
  "pair": "Chromera velia -> Gregarina niphandrodes",
  "clade": "alveolata",
  "k0": 0.8651563393325338,
  "k2": 0.8639580798182034,
  "k4": 0.8657835263720184,
  "k8": 0.8622149566400693
 },
 {
  "pair": "Chromera velia -> Besnoitia besnoiti",
  "clade": "alveolata",
  "k0": 0.8500489831268979,
  "k2": 0.8499721862228546,
  "k4": 0.8475776453366488,
  "k8": 0.840009944912322
 },
 {
  "pair": "Chromera velia -> Plasmodium yoelii",
  "clade": "alveolata",
  "k0": 0.84723553947026,
  "k2": 0.8434540754544981,
  "k4": 0.8454742387318591,
  "k8": 0.8394202171002106
 },
 {
  "pair": "Chromera velia -> Plasmodium malariae",
  "clade": "alveolata",
  "k0": 0.8485213470811136,
  "k2": 0.8452917269885566,
  "k4": 0.8455020154390422,
  "k8": 0.8399003898281961
 },
 {
  "pair": "Dictyostelium discoideum -> Entamoeba histolytica",
  "clade": "amoebozoa",
  "k0": 0.8241367465491837,
  "k2": 0.8380993531256872,
  "k4": 0.8407403499562154,
  "k8": 0.8321665926489413
 },
 {
  "pair": "Dictyostelium discoideum -> Entamoeba dispar",
  "clade": "amoebozoa",
  "k0": 0.8191497517298622,
  "k2": 0.8356466996535769,
  "k4": 0.834147468298733,
  "k8": 0.8285079181678329
 },
 {
  "pair": "Dictyostelium discoideum -> Entamoeba invadens",
  "clade": "amoebozoa",
  "k0": 0.8242563939103001,
  "k2": 0.8434383104934096,
  "k4": 0.8412521538820791,
  "k8": 0.834106214955677
 },
 {
  "pair": "Galendromus occidentalis -> Varroa destructor",
  "clade": "chelicerata",
  "k0": 0.7959501646389026,
  "k2": 0.7993441468607457,
  "k4": 0.7707865781206032,
  "k8": 0.7886027985471672
 },
 {
  "pair": "Galendromus occidentalis -> Ixodes scapularis",
  "clade": "chelicerata",
  "k0": 0.7959431791299604,
  "k2": 0.8151244185841281,
  "k4": 0.7874108199296775,
  "k8": 0.7922854125611155
 },
 {
  "pair": "Galendromus occidentalis -> Sarcoptes scabiei",
  "clade": "chelicerata",
  "k0": 0.7701156432089835,
  "k2": 0.7796681347902578,
  "k4": 0.7823534161135811,
  "k8": 0.7784393426719775
 },
 {
  "pair": "Auxenochlorella protothecoides -> Helicosporidium sp. ATCC 50920",
  "clade": "chlorophyta",
  "k0": 0.723998088119315,
  "k2": 0.7253033770304658,
  "k4": 0.7270791600922123,
  "k8": 0.7323926003702371
 },
 {
  "pair": "Nematostella vectensis -> Thelohanellus kitauei",
  "clade": "cnidaria",
  "k0": 0.8126079882845382,
  "k2": 0.8177727876783202,
  "k4": 0.8189326244487577,
  "k8": 0.8180131204695357
 },
 {
  "pair": "Nematostella vectensis -> Henneguya salminicola",
  "clade": "cnidaria",
  "k0": 0.8333506544177082,
  "k2": 0.8387398857758249,
  "k4": 0.8416721832275229,
  "k8": 0.8371693082826219
 },
 {
  "pair": "Tigriopus californicus -> Lepeophtheirus salmonis",
  "clade": "crustacea",
  "k0": 0.780342720
… (잘림, 원본 파일 참조)
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
   "SBP_bac_3: Bacterial extracellular solute-binding proteins, family 3",
   "Lig_chan: Ligand-gated ion channel",
   "Kinesin_assoc: Kinesin-associated",
   "KIF1B: Kinesin protein 1B",
   "DUF3694: Kinesin protein",
   "TraB_PrgY_gumN: TraB/PrgY/gumN family",
   "POPDC1-3: POPDC1-3"
  ],
  "lost_together_enriched": [
   [
    "kw:cell_adhesion_surface",
    4.0
   ],
   [
    "kw:transporter_channel",
    3.81
   ],
   [
    "kw:methyl_glyco_transferase",
    3.12
   ]
  ],
  "kept_together": [
   "EF_SSP120: SSP120-like, EF-hand pair",
   "DNA_alkylation: DNA alkylation repair enzyme",
   "Fe-S_assembly: Iron-sulphur cluster assembly",
   "BT1: BT1 family",
   "tRNA-synt_1e: tRNA synthetases class I (C) catalytic domain",
   "Inhibitor_I42: Chagasin family peptidase inhibitor I42",
   "DUF2921: Transmembrane E3 ligase/DUF2921 transmembrane domain",
   "TnsB_C: TnsB C-terminal domain"
  ],
  "kept_together_enriched": [
   [
    "kw:methyl_glyco_transferase",
    3.12
   ]
  ],
  "most_affected": [
   "Leishmania major",
   "Leishmania donovani",
   "Leishmania mexicana",
   "Leishmania infantum",
   "Leishmania braziliensis",
   "Leptomonas pyrrhocoris"
  ],
  "least_affected": [
   "Haemonchus contortus",
   "Ixodes scapularis",
   "Cuscuta australis",
   "Cuscuta campestris",
   "Necator americanus",
   "Pediculus humanus"
  ]
 }
]
```

## 연결
- [[실험 목록]]
