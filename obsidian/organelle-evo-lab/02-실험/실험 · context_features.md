---
유형: 실험
실행: context_features
산출: results/context_features/metrics.json
tags:
  - 유형/실험
  - 실험/context_features
---

# 실험 · context_features

**산출물** `results/context_features/metrics.json`

## extremophiles

```json
{
 "mean_auroc": {
  "copies_only": 0.6199392920234301,
  "memorisation": 0.8439985034182216,
  "law_base": 0.8191445774072861,
  "law_context": 0.8232006566776416,
  "combined_s1": 0.8580671753930625,
  "combined_s3": 0.8604717595469014,
  "combined_s10": 0.8599867802864807
 },
 "context_gain": {
  "mean": 0.00405607927035582,
  "n_better": 29,
  "n": 40
 },
 "heldout": [
  {
   "pair": "Shewanella oneidensis -> Shewanella frigidimarina",
   "copies_only": 0.6256721917137704,
   "memorisation": 0.8762157282803291,
   "law_base": 0.8308004613146125,
   "law_context": 0.8361444692535152,
   "combined_s1": 0.8801654832069412,
   "combined_s3": 0.8741266536586674,
   "combined_s10": 0.8669261561362219
  },
  {
   "pair": "Shewanella oneidensis -> Colwellia psychrerythraea",
   "copies_only": 0.6304542700437961,
   "memorisation": 0.8062263726386285,
   "law_base": 0.8466202524659187,
   "law_context": 0.8502835738247198,
   "combined_s1": 0.854541275139088,
   "combined_s3": 0.8710759550867098,
   "combined_s10": 0.8812889796497646
  },
  {
   "pair": "Acinetobacter baylyi -> Psychrobacter arcticus",
   "copies_only": 0.6140806592934253,
   "memorisation": 0.8216303790771876,
   "law_base": 0.8543826150209128,
   "law_context": 0.8558514771280729,
   "combined_s1": 0.8514415844203078,
   "combined_s3": 0.8619583725966705,
   "combined_s10": 0.8720073071136901
  },
  {
   "pair": "Bacillus subtilis -> Planococcus halocryophilus",
   "copies_only": 0.641160799890426,
   "memorisation": 0.8824857325480527,
   "law_base": 0.8629553029265398,
   "law_context": 0.8477564717162033,
   "combined_s1": 0.8883404099894991,
   "combined_s3": 0.893326941514861,
   "combined_s10": 0.8938451353695841
  },
  {
   "pair": "Bacillus subtilis -> Geobacillus kaustophilus",
   "copies_only": 0.625025833144228,
   "memorisation": 0.890414535854378,
   "law_base": 0.8352174644211755,
   "law_context": 0.8143468165461796,
   "combined_s1": 0.8914552063409732,
   "combined_s3": 0.8916279338347327,
   "combined_s10": 0.8831875871235453
  },
  {
   "pair": "Bacillus subtilis -> Lactiplantibacillus plantarum",
   "copies_only": 0.6513205313852461,
   "memorisation": 0.8408177003677069,
   "law_base": 0.842323712212424,
   "law_context": 0.8338989945006671,
   "combined_s1": 0.8530848329048843,
   "combined_s3": 0.8593419511242719,
   "combined_s10": 0.862202255051902
  },
  {
   "pair": "Flavobacterium johnsoniae -> Psychroflexus torquis",
   "copies_only": 0.6134243490031177,
   "memorisation": 0.8308179205822636,
   "law_base": 0.819184298410092,
   "law_context": 0.8278111859404644,
   "combined_s1": 0.8531093630382444,
   "combined_s3": 0.8542621295669637,
   "combined_s10": 0.8519355160821471
  },
  {
   "pair": "Rhodothermus marinus -> Salinibacter ruber",
   "copies_only": 0.6300849300067235,
   "memorisation": 0.8248829419319513,
   "law_base": 0.8264007713955577,
   "law_context": 0.8233087474484764,
   "combined_s1": 0.8472880373297474,
   "combined_s3": 0.8534267919043728,
   "combined_s10": 0.8567956083597377
  },
  {
   "pair": "Thermus thermophilus -> Deinococcus radiodurans",
   "copies_only": 0.6221328354041603,
   "memorisation": 0.9023794150495602,
   "law_base": 0.8393829401088929,
   "law_context": 0.8444489040904649,
   "combined_s1": 0.9027013821024711,
   "combined_s3": 0.9020836241798129,
   "combined_s10": 0.8985742705570292
  },
  {
   "pair": "Micrococcus luteus -> Kineococcus radiotolerans",
   "copies_only": 0.6025538779197316,
   "memorisation": 0.8260278745644599,
   "law_base": 0.7898283649503162,
   "law_context": 0.8005316815072913,
   "combined_s1": 0.8338082333204284,
   "combined_s3": 0.834618660472319,
   "combined_s10": 0.8346780229707059
  },
  {
   "pair": "Synechocystis sp. PCC 6803 -> Chroococcidiopsis thermalis",
   "copies_only": 0.6128082682613423,
   "memorisation": 0.8386788635465059,
   "law_base": 0.7957799990115647,
   "law_context": 0.8066635983987348,
   "combined_s1": 0.8283396757932193,
   "combined_s3": 0.8313296925966196,
   "combined_s10": 0.8350857467628744
  },
  {
   "pair": "Synechococcus elongatus -> Prochlorococcus marinus",
   "copies_only": 0.5774197206830628,
   "memorisation": 0.8273603145285852,
   "law_base": 0.7835788787718407,
   "law_context": 0.800236004450061,
   "combined_s1": 0.8431029454651502,
   "combined_s3": 0.8350642126524308,
   "combined_s10": 0.8267680531703084
  },
  {
   "pair": "Cereibacter sphaeroides -> Candidatus Pelagibacter ubique",
   "copies_only": 0.6059059693903209,
   "memorisation": 0.8194699463017495,
   "law_base": 0.8222755541648273,
   "law_context": 0.8350575258573001,
   "combined_s1": 0.865711348155764,
   "combined_s3": 0.8720735571039824,
   "combined_s10": 0.8726524477126557
  },
  {
   "pair": "Nitratidesulfovibrio vulgaris -> Desulfotalea psychrophila",
   "copies_only": 0.6445834877033273,
   "memorisation": 0.8086242105077449,
   "law_base": 0.8421269097773544,
   "law_context": 0.8419416657845524,
   "combined_s1": 0.8322196640908931,
   "combined_s3": 0.8424488814791292,
   "combined_s10": 0.8550443703468473
  },
  {
   "pair": "Myxococcus xanthus -> Geobacter sulfurreducens",
   "copies_only": 0.6153687586486739,
   "memorisation": 0.8974473189544252,
   "law_base": 0.8552905607635457,
   "law_context": 0.8528026038794613,
   "combined_s1": 0.8992132524563101,
   "combined_s3": 0.9003824491310576,
   "combined_s10": 0.8982135611207641
  },
  {
   "pair": "Methanosarcina acetivorans -> Methanococcoides burtonii",
   "copies_only": 0.5879022613611655,
   "memorisation": 0.7888057186344858,
   "law_base": 0.7408654055229398,
   "law_context": 0.7630441400304414,
   "combined_s1": 0.7962589693411611,
   "combined_s3": 0.7979539030223962,
   "combined_s10": 0.8004131332898456
  },
  {
   "pair": "Methanosarcina acetivorans -> Halobacterium salinarum",
   "copies_only": 0.5851809733772395,
   "memorisation": 0.9125581675224647,
   "law_base": 0.7868304194340571,
   "law_context": 0.7942544092202936,
   "combi
… (잘림, 원본 파일 참조)
```

## parasites

```json
{
 "mean_auroc": {
  "copies_only": 0.6438921622472106,
  "memorisation": 0.797798715194633,
  "law_base": 0.7606546179344121,
  "law_context": 0.766020699300282,
  "combined_s1": 0.8024944533929399,
  "combined_s3": 0.8079091820274272,
  "combined_s10": 0.8138726894330391
 },
 "context_gain": {
  "mean": 0.0053660813658698535,
  "n_better": 71,
  "n": 79
 },
 "heldout": [
  {
   "pair": "Tetrahymena thermophila -> Ichthyophthirius multifiliis",
   "clade": "alveolata",
   "copies_only": 0.6843729713573167,
   "memorisation": 0.7392574369943474,
   "law_base": 0.7518568161615784,
   "law_context": 0.7549107747488569,
   "combined_s1": 0.7440138986834547,
   "combined_s3": 0.749871957133272,
   "combined_s10": 0.7644120224857285
  },
  {
   "pair": "Tetrahymena thermophila -> Perkinsus marinus",
   "clade": "alveolata",
   "copies_only": 0.6243565597008711,
   "memorisation": 0.819617643210322,
   "law_base": 0.7652702825943005,
   "law_context": 0.769019306182816,
   "combined_s1": 0.8254521231249926,
   "combined_s3": 0.8304156638210303,
   "combined_s10": 0.8381762021260988
  },
  {
   "pair": "Chromera velia -> Plasmodium falciparum",
   "clade": "alveolata",
   "copies_only": 0.624691069050213,
   "memorisation": 0.841717835032901,
   "law_base": 0.8011262528435487,
   "law_context": 0.8028969240761181,
   "combined_s1": 0.850715784480607,
   "combined_s3": 0.8576469566453976,
   "combined_s10": 0.8631978117261814
  },
  {
   "pair": "Chromera velia -> Babesia bovis",
   "clade": "alveolata",
   "copies_only": 0.6090961112595233,
   "memorisation": 0.8535104596545061,
   "law_base": 0.8083942431634281,
   "law_context": 0.8099547610393136,
   "combined_s1": 0.8617542712303664,
   "combined_s3": 0.8675396710698866,
   "combined_s10": 0.8725959046989251
  },
  {
   "pair": "Chromera velia -> Toxoplasma gondii",
   "clade": "alveolata",
   "copies_only": 0.6233197287534065,
   "memorisation": 0.836097471322644,
   "law_base": 0.802895240509538,
   "law_context": 0.8076164522466569,
   "combined_s1": 0.8486203181443691,
   "combined_s3": 0.857145826731732,
   "combined_s10": 0.8654302554027505
  },
  {
   "pair": "Chromera velia -> Eimeria tenella",
   "clade": "alveolata",
   "copies_only": 0.6630382613043462,
   "memorisation": 0.8259324391891634,
   "law_base": 0.812259542902508,
   "law_context": 0.81240768165007,
   "combined_s1": 0.8370788661111981,
   "combined_s3": 0.8446561272666898,
   "combined_s10": 0.8528862962355106
  },
  {
   "pair": "Chromera velia -> Cryptosporidium parvum",
   "clade": "alveolata",
   "copies_only": 0.6330129445537315,
   "memorisation": 0.8667501045407436,
   "law_base": 0.8222629675551291,
   "law_context": 0.8218082944256783,
   "combined_s1": 0.8783028911661489,
   "combined_s3": 0.884137213924681,
   "combined_s10": 0.8876718837244058
  },
  {
   "pair": "Chromera velia -> Plasmodium vivax",
   "clade": "alveolata",
   "copies_only": 0.6212876672589477,
   "memorisation": 0.836971670709573,
   "law_base": 0.799381588012894,
   "law_context": 0.8018192601385976,
   "combined_s1": 0.8459705170021548,
   "combined_s3": 0.8530743105906333,
   "combined_s10": 0.8591486898884082
  },
  {
   "pair": "Chromera velia -> Plasmodium berghei",
   "clade": "alveolata",
   "copies_only": 0.6191111999759492,
   "memorisation": 0.8418921943321306,
   "law_base": 0.8011559639944702,
   "law_context": 0.803127745378697,
   "combined_s1": 0.8511240633203329,
   "combined_s3": 0.8580584634134819,
   "combined_s10": 0.8635724842011733
  },
  {
   "pair": "Chromera velia -> Plasmodium knowlesi",
   "clade": "alveolata",
   "copies_only": 0.6172615991923694,
   "memorisation": 0.8402925943030751,
   "law_base": 0.8000010019045729,
   "law_context": 0.8022855828794546,
   "combined_s1": 0.8494628837294514,
   "combined_s3": 0.8566935336124671,
   "combined_s10": 0.8627903614871699
  },
  {
   "pair": "Chromera velia -> Theileria annulata",
   "clade": "alveolata",
   "copies_only": 0.6151684992058313,
   "memorisation": 0.8504587709469692,
   "law_base": 0.808773040127067,
   "law_context": 0.8096120270386742,
   "combined_s1": 0.8588884100619328,
   "combined_s3": 0.8650147136683207,
   "combined_s10": 0.8707770540650357
  },
  {
   "pair": "Chromera velia -> Theileria parva",
   "clade": "alveolata",
   "copies_only": 0.6076658641801806,
   "memorisation": 0.8555567097239365,
   "law_base": 0.8117442471495435,
   "law_context": 0.8127306944970609,
   "combined_s1": 0.8639057058011218,
   "combined_s3": 0.8701797651199452,
   "combined_s10": 0.8756822153515258
  },
  {
   "pair": "Chromera velia -> Babesia microti",
   "clade": "alveolata",
   "copies_only": 0.596199045904687,
   "memorisation": 0.8494945595510186,
   "law_base": 0.8006102135089251,
   "law_context": 0.8020508126187805,
   "combined_s1": 0.8576212347867032,
   "combined_s3": 0.863505244989586,
   "combined_s10": 0.868283033003392
  },
  {
   "pair": "Chromera velia -> Neospora caninum",
   "clade": "alveolata",
   "copies_only": 0.6402126539997026,
   "memorisation": 0.8327382068468848,
   "law_base": 0.8140382873686299,
   "law_context": 0.8175961150620425,
   "combined_s1": 0.8452000535153784,
   "combined_s3": 0.8542464403072261,
   "combined_s10": 0.8638640391080041
  },
  {
   "pair": "Chromera velia -> Hammondia hammondi",
   "clade": "alveolata",
   "copies_only": 0.6259803786879641,
   "memorisation": 0.8353384856959098,
   "law_base": 0.8065602306402241,
   "law_context": 0.81105213828644,
   "combined_s1": 0.8480780659762929,
   "combined_s3": 0.8568438497297122,
   "combined_s10": 0.8656780704539534
  },
  {
   "pair": "Chromera velia -> Cyclospora cayetanensis",
   "clade": "alveolata",
   "copies_only": 0.6551266858529429,
   "memorisation": 0.8296351212149905,
   "law_base": 0.8106149077174548,
   "law_context": 0.812792970898264,
   "combined_s1": 0.8412127620299195,
   "combined_s3": 0.8489896120565564,
   "combined_s10": 0.8573632834356251
  },
  {
   "pair": "Chromera velia -> Cryptosp
… (잘림, 원본 파일 참조)
```

## 연결
- [[실험 목록]]
