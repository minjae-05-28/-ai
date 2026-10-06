---
유형: 실험
실행: features
산출: results/features/metrics.json
tags:
  - 유형/실험
  - 실험/features
---

# 실험 · features

**산출물** `results/features/metrics.json`

## n_features

```json
{
 "base": 8,
 "enriched": 56
}
```

## feature_names

```json
[
 "hydrophobicity_gravy",
 "tm_helices",
 "protein_length",
 "redox_core",
 "atp_synthase",
 "translation",
 "transcription",
 "protein_targeting",
 "ubiquity_free_living",
 "copies_free_living",
 "hmm_length",
 "clan_size",
 "in_clan",
 "has_go_annotation",
 "go:DNA binding",
 "go:RNA binding",
 "go:catalytic activity",
 "go:structural molecule activity",
 "go:transporter activity",
 "go:nucleus",
 "go:mitochondrion",
 "go:ribosome",
 "go:carbohydrate metabolic process",
 "go:DNA-templated transcription",
 "go:regulation of DNA-templated transcription",
 "go:lipid metabolic process",
 "go:oxidoreductase activity",
 "go:transferase activity",
 "go:hydrolase activity",
 "go:lyase activity",
 "go:isomerase activity",
 "go:ligase activity",
 "go:signaling",
 "go:organelle",
 "go:transmembrane transport",
 "go:nucleobase-containing small molecule metabolic process",
 "go:molecular function regulator activity",
 "go:catalytic activity, acting on a protein",
 "go:catalytic activity, acting on RNA",
 "go:carbohydrate derivative metabolic process",
 "kw:kinase",
 "kw:phosphatase",
 "kw:transporter_channel",
 "kw:zinc_finger",
 "kw:repeat_domain",
 "kw:ubiquitin_system",
 "kw:protease",
 "kw:helicase_nucleic",
 "kw:gtpase_signalling",
 "kw:methyl_glyco_transferase",
 "kw:cytoskeleton_motor",
 "kw:cilium_flagellum",
 "kw:cell_adhesion_surface",
 "kw:lipid_metabolism",
 "kw:amino_acid_metabolism",
 "kw:uncharacterised"
]
```

## mean_heldout_auroc

```json
{
 "copies_only": 0.6466693047031259,
 "base": 0.67057666758796,
 "enriched": 0.769860430012379,
 "memorisation": 0.8516556973408791
}
```

## heldout

```json
[
 {
  "pair": "Chromera velia -> Plasmodium falciparum",
  "copies_only": 0.624691069050213,
  "memorisation": 0.9448367074152495,
  "base": 0.6674359220303379,
  "enriched": 0.8092974436575324
 },
 {
  "pair": "Coprinopsis cinerea -> Ustilago maydis",
  "copies_only": 0.5771335042578518,
  "memorisation": 0.7754909719587862,
  "base": 0.5896290894345102,
  "enriched": 0.7076912763090769
 },
 {
  "pair": "Spizellomyces punctatus -> Encephalitozoon intestinalis",
  "copies_only": 0.6854698940477216,
  "memorisation": 0.9458492333534326,
  "base": 0.7084613231113791,
  "enriched": 0.8408082091480747
 },
 {
  "pair": "Chromera velia -> Theileria parva",
  "copies_only": 0.6076658641801806,
  "memorisation": 0.9424179691796307,
  "base": 0.6675332706008872,
  "enriched": 0.8219450317124736
 },
 {
  "pair": "Chromera velia -> Neospora caninum",
  "copies_only": 0.6402126539997026,
  "memorisation": 0.9294701132029303,
  "base": 0.6819284137315687,
  "enriched": 0.8199451218693379
 },
 {
  "pair": "Chromera velia -> Hammondia hammondi",
  "copies_only": 0.6259803786879641,
  "memorisation": 0.9351870084749903,
  "base": 0.6676207136576788,
  "enriched": 0.8123608363455777
 },
 {
  "pair": "Thalassiosira pseudonana -> Phytophthora infestans",
  "copies_only": 0.611587689524816,
  "memorisation": 0.8667917462704768,
  "base": 0.6386849111824723,
  "enriched": 0.7548178935815617
 },
 {
  "pair": "Caenorhabditis elegans -> Brugia malayi",
  "copies_only": 0.6088821757907794,
  "memorisation": 0.8268944598757242,
  "base": 0.6427589948634479,
  "enriched": 0.7088171580104068
 },
 {
  "pair": "Macrostomum lignano -> Schistosoma mansoni",
  "copies_only": 0.6535623221963213,
  "memorisation": 0.8574847212506964,
  "base": 0.67044366953814,
  "enriched": 0.7552107434645486
 },
 {
  "pair": "Spizellomyces punctatus -> Pseudoloma neurophilia",
  "copies_only": 0.7062293431669652,
  "memorisation": 0.9383986301415065,
  "base": 0.7391291214990467,
  "enriched": 0.8253062370341528
 },
 {
  "pair": "Thalassiosira pseudonana -> Aphanomyces astaci",
  "copies_only": 0.6048227601544268,
  "memorisation": 0.8747253368729738,
  "base": 0.6363695841532336,
  "enriched": 0.7572335580539297
 },
 {
  "pair": "Bodo saltans -> Angomonas deanei",
  "copies_only": 0.6600586254462837,
  "memorisation": 0.8352358710645894,
  "base": 0.6642009493670886,
  "enriched": 0.7430445675105485
 },
 {
  "pair": "Bodo saltans -> Trypanosoma grayi",
  "copies_only": 0.6324923673227102,
  "memorisation": 0.8753018089737971,
  "base": 0.6358308353382017,
  "enriched": 0.7233515851867194
 },
 {
  "pair": "Bodo saltans -> Leishmania mexicana",
  "copies_only": 0.6185548308615659,
  "memorisation": 0.9081594319323391,
  "base": 0.6279200425312821,
  "enriched": 0.7498419332278996
 },
 {
  "pair": "Chromera velia -> Gregarina niphandrodes",
  "copies_only": 0.6840790247222995,
  "memorisation": 0.9005049857644307,
  "base": 0.7141941174708277,
  "enriched": 0.78069954427515
 },
 {
  "pair": "Macrostomum lignano -> Fasciola hepatica",
  "copies_only": 0.8134964491107427,
  "memorisation": 0.660833282167782,
  "base": 0.7743721986860687,
  "enriched": 0.3315901230019852
 },
 {
  "pair": "Macrostomum lignano -> Clonorchis sinensis",
  "copies_only": 0.6558319372816959,
  "memorisation": 0.840778394595364,
  "base": 0.6654083952888276,
  "enriched": 0.7524774898079106
 },
 {
  "pair": "Galendromus occidentalis -> Ixodes scapularis",
  "copies_only": 0.6613540313307349,
  "memorisation": 0.8049470105381579,
  "base": 0.7059781770032206,
  "enriched": 0.797502600938827
 },
 {
  "pair": "Dictyostelium discoideum -> Entamoeba histolytica",
  "copies_only": 0.6538274396929824,
  "memorisation": 0.8543143100167698,
  "base": 0.6775418843524251,
  "enriched": 0.8007715750773994
 },
 {
  "pair": "Tetrahymena thermophila -> Ichthyophthirius multifiliis",
  "copies_only": 0.6843729713573167,
  "memorisation": 0.7340637225369456,
  "base": 0.6963928495258911,
  "enriched": 0.7548068615409045
 },
 {
  "pair": "Tetrahymena thermophila -> Perkinsus marinus",
  "copies_only": 0.6243565597008711,
  "memorisation": 0.8178164861874948,
  "base": 0.6467261963766708,
  "enriched": 0.7645307871958256
 },
 {
  "pair": "Bodo saltans -> Trypanosoma cruzi",
  "copies_only": 0.6282412855577649,
  "memorisation": 0.8996545672199002,
  "base": 0.6382466623381894,
  "enriched": 0.7518393915107738
 },
 {
  "pair": "Spizellomyces punctatus -> Rozella allomycis",
  "copies_only": 0.6630970516017967,
  "memorisation": 0.8483853058203017,
  "base": 0.6917938346406854,
  "enriched": 0.8137917935491499
 },
 {
  "pair": "Spizellomyces punctatus -> Encephalitozoon cuniculi",
  "copies_only": 0.6851860894847471,
  "memorisation": 0.9441961661987996,
  "base": 0.711158325151423,
  "enriched": 0.8379540960256658
 },
 {
  "pair": "Schizosaccharomyces pombe -> Pneumocystis jirovecii",
  "copies_only": 0.5885882177917663,
  "memorisation": 0.7874579031526121,
  "base": 0.6232327006174516,
  "enriched": 0.7298299562796111
 },
 {
  "pair": "Spizellomyces punctatus -> Nematocida parisii",
  "copies_only": 0.6793454871052335,
  "memorisation": 0.9320798806263016,
  "base": 0.7078230256655275,
  "enriched": 0.8323575484807482
 },
 {
  "pair": "Chromera velia -> Theileria annulata",
  "copies_only": 0.6151684992058313,
  "memorisation": 0.9330737407193075,
  "base": 0.6743996946452098,
  "enriched": 0.8203703658101137
 },
 {
  "pair": "Chromera velia -> Babesia microti",
  "copies_only": 0.596199045904687,
  "memorisation": 0.9328274054544382,
  "base": 0.6574461987047038,
  "enriched": 0.814403748920952
 },
 {
  "pair": "Naegleria gruberi -> Spironucleus salmonicida",
  "copies_only": 0.6778121200430228,
  "memorisation": 0.857229119902731,
  "base": 0.7108103605499438,
  "enriched": 0.7667198606434718
 },
 {
  "pair": "Caenorhabditis elegans -> Trichinella spiralis",
  "copies_only": 0.6382975788094088,
  "memorisation": 0.7545538936752548,
  "base": 0.6603764893496376,
  "enriched": 0.71
… (잘림, 원본 파일 참조)
```

## significant_loss_effects

```json
{
 "base": [
  [
   "go:ligase activity",
   -0.4181332896428694,
   0.06937946946370828
  ],
  [
   "ubiquity_free_living",
   -0.3898159552835325,
   0.020769427870173628
  ],
  [
   "copies_free_living",
   0.3554355079959326,
   0.017987160938131002
  ],
  [
   "transcription",
   -0.35023590762999884,
   0.07567327698887324
  ],
  [
   "kw:gtpase_signalling",
   -0.31912036062649324,
   0.016835187142015814
  ],
  [
   "go:DNA-templated transcription",
   -0.2964930781486783,
   0.040377639552412685
  ],
  [
   "translation",
   -0.2822083146743135,
   0.05044623230768332
  ],
  [
   "go:carbohydrate metabolic process",
   0.24722290945122383,
   0.049912569996669875
  ],
  [
   "go:nucleus",
   -0.24483378185990834,
   0.08879717945674553
  ],
  [
   "kw:helicase_nucleic",
   0.2248011862067602,
   0.06878979361537937
  ],
  [
   "in_clan",
   0.2051584512951919,
   0.011964983760817376
  ],
  [
   "go:oxidoreductase activity",
   0.20365843323512753,
   0.06803401748186431
  ]
 ],
 "parasite": [
  [
   "go:mitochondrion",
   -0.30605091761797837,
   0.09275820386087337
  ],
  [
   "kw:cell_adhesion_surface",
   -0.3037860861615432,
   0.05840752523530052
  ],
  [
   "go:ribosome",
   0.2579275683874966,
   0.0887804675763376
  ],
  [
   "go:DNA-templated transcription",
   0.2560919349049485,
   0.03809321178299638
  ],
  [
   "go:organelle",
   0.21582762235482036,
   0.014325073143185438
  ],
  [
   "go:ligase activity",
   0.1759084693935091,
   0.06266231081807752
  ],
  [
   "kw:helicase_nucleic",
   -0.17343760629532698,
   0.08580872224877907
  ],
  [
   "in_clan",
   0.15211429844577143,
   0.01102512219651768
  ],
  [
   "clan_size",
   -0.11194031142382156,
   0.013521011756016298
  ],
  [
   "kw:ubiquitin_system",
   0.09204056826124443,
   0.022895439381407697
  ],
  [
   "kw:repeat_domain",
   -0.08297637477178908,
   0.03635735753174618
  ],
  [
   "go:catalytic activity, acting on a protein",
   -0.07609946459410698,
   0.019312611222391144
  ]
 ],
 "intracellular": [
  [
   "go:DNA-templated transcription",
   -0.48184890787938106,
   0.07518583505079939
  ],
  [
   "atp_synthase",
   -0.47907361974279233,
   0.05053355456410374
  ],
  [
   "kw:gtpase_signalling",
   -0.4790143180577309,
   0.09564681906749903
  ],
  [
   "go:carbohydrate derivative metabolic process",
   -0.38013491791363835,
   0.0878312868904079
  ],
  [
   "go:ribosome",
   -0.3575211320431827,
   0.06280813885009028
  ],
  [
   "translation",
   -0.31729988181035,
   0.05148545588284638
  ],
  [
   "go:DNA binding",
   -0.306465671179979,
   0.04186327894103327
  ],
  [
   "protein_targeting",
   -0.2962887003434233,
   0.025367796977016174
  ],
  [
   "go:molecular function regulator activity",
   -0.25869921640340326,
   0.058195002851429124
  ],
  [
   "kw:protease",
   -0.23551998035920324,
   0.04874116128417689
  ],
  [
   "kw:amino_acid_metabolism",
   0.2339701597653856,
   0.0844607768859704
  ],
  [
   "kw:ubiquitin_system",
   -0.2315303957516519,
   0.06498780206439322
  ]
 ],
 "reduced_mitochondria": [
  [
   "go:mitochondrion",
   0.9776563733742636,
   0.10592838391166072
  ],
  [
   "redox_core",
   0.7989374878119574,
   0.1259251092293361
  ],
  [
   "go:DNA-templated transcription",
   -0.5185906430468795,
   0.0596122472712338
  ],
  [
   "go:carbohydrate metabolic process",
   -0.34613623967110235,
   0.06799351701839297
  ],
  [
   "kw:cytoskeleton_motor",
   0.34546524302781273,
   0.039116684911450976
  ],
  [
   "go:ribosome",
   -0.3287842656743301,
   0.07552187467829696
  ],
  [
   "kw:cilium_flagellum",
   0.3186370432068805,
   0.015355632871137169
  ],
  [
   "go:catalytic activity, acting on RNA",
   -0.2895943869176254,
   0.07386927709558866
  ],
  [
   "protein_targeting",
   -0.27773724866786204,
   0.06448434470963456
  ],
  [
   "go:transmembrane transport",
   -0.2745472839808126,
   0.029850973587880813
  ],
  [
   "go:lyase activity",
   0.2720795310756158,
   0.0686481280019427
  ],
  [
   "kw:repeat_domain",
   0.2658214668088575,
   0.019699606646898817
  ]
 ]
}
```

## 연결
- [[실험 목록]]
