---
유형: 실험
실행: context_features_v2
산출: results/context_features_v2/metrics.json
tags:
  - 유형/실험
  - 실험/context_features_v2
---

# 실험 · context_features_v2

**산출물** `results/context_features_v2/metrics.json`

## extremophiles

```json
{
 "mean_auroc": {
  "copies_only": 0.6172579176865324,
  "memorisation": 0.849235234515775,
  "law_base": 0.8132686604717007,
  "law_context": 0.8178732595435612,
  "combined_s1": 0.8596954810622316,
  "combined_s3": 0.8615463752219165,
  "combined_s10": 0.8606810305907693
 },
 "context_gain": {
  "mean": 0.004604599071860593,
  "n_better": 40,
  "n": 54
 },
 "heldout": [
  {
   "pair": "Shewanella oneidensis -> Shewanella frigidimarina",
   "copies_only": 0.6256721917137704,
   "memorisation": 0.8866145843810137,
   "law_base": 0.8248923822742542,
   "law_context": 0.8298969417791456,
   "combined_s1": 0.8870935838378962,
   "combined_s3": 0.8838491273241741,
   "combined_s10": 0.874311883544881
  },
  {
   "pair": "Shewanella oneidensis -> Colwellia psychrerythraea",
   "copies_only": 0.6304542700437961,
   "memorisation": 0.8580156685834409,
   "law_base": 0.8404514376413548,
   "law_context": 0.8442281763998406,
   "combined_s1": 0.8724563722080063,
   "combined_s3": 0.8800147018062479,
   "combined_s10": 0.8846229659923689
  },
  {
   "pair": "Acinetobacter baylyi -> Psychrobacter arcticus",
   "copies_only": 0.6140806592934253,
   "memorisation": 0.8350832382747276,
   "law_base": 0.8520937691150458,
   "law_context": 0.8531170956702872,
   "combined_s1": 0.8554844682504257,
   "combined_s3": 0.8632569558101473,
   "combined_s10": 0.871539453454347
  },
  {
   "pair": "Bacillus subtilis -> Planococcus halocryophilus",
   "copies_only": 0.641160799890426,
   "memorisation": 0.8797584805734374,
   "law_base": 0.8592512441218098,
   "law_context": 0.8428685568187007,
   "combined_s1": 0.8841154179792723,
   "combined_s3": 0.8881075651737205,
   "combined_s10": 0.8890266173583528
  },
  {
   "pair": "Bacillus subtilis -> Geobacillus kaustophilus",
   "copies_only": 0.625025833144228,
   "memorisation": 0.8994774106882355,
   "law_base": 0.8361332747106688,
   "law_context": 0.8150205044250657,
   "combined_s1": 0.8993530570233734,
   "combined_s3": 0.8986793691444873,
   "combined_s10": 0.8894695999610983
  },
  {
   "pair": "Bacillus subtilis -> Lactiplantibacillus plantarum",
   "copies_only": 0.6513205313852461,
   "memorisation": 0.8384162165240311,
   "law_base": 0.8434170707103577,
   "law_context": 0.8336866681852201,
   "combined_s1": 0.8486707233737919,
   "combined_s3": 0.8564649702255052,
   "combined_s10": 0.8620537893332466
  },
  {
   "pair": "Flavobacterium johnsoniae -> Psychroflexus torquis",
   "copies_only": 0.6134243490031177,
   "memorisation": 0.8499930656488889,
   "law_base": 0.8167178884068744,
   "law_context": 0.8258079905914724,
   "combined_s1": 0.8576277862222764,
   "combined_s3": 0.8583300973028148,
   "combined_s10": 0.8553050559740821
  },
  {
   "pair": "Rhodothermus marinus -> Salinibacter ruber",
   "copies_only": 0.6300849300067235,
   "memorisation": 0.8379777438692976,
   "law_base": 0.8230923460329092,
   "law_context": 0.8191709510791888,
   "combined_s1": 0.8477600943711475,
   "combined_s3": 0.8522813741791844,
   "combined_s10": 0.8547332525434715
  },
  {
   "pair": "Thermus thermophilus -> Deinococcus radiodurans",
   "copies_only": 0.6221328354041603,
   "memorisation": 0.903568686304621,
   "law_base": 0.8350010470473266,
   "law_context": 0.8390286890967472,
   "combined_s1": 0.9043888733770766,
   "combined_s3": 0.9044150495602401,
   "combined_s10": 0.9017415887198101
  },
  {
   "pair": "Micrococcus luteus -> Kineococcus radiotolerans",
   "copies_only": 0.6025538779197316,
   "memorisation": 0.8283146212414505,
   "law_base": 0.7883623693379791,
   "law_context": 0.7992128016518261,
   "combined_s1": 0.8340482642921667,
   "combined_s3": 0.8346496322106078,
   "combined_s10": 0.8345644599303136
  },
  {
   "pair": "Synechocystis sp. PCC 6803 -> Chroococcidiopsis thermalis",
   "copies_only": 0.6128082682613423,
   "memorisation": 0.8492103328555896,
   "law_base": 0.7993754324404467,
   "law_context": 0.8079640085993872,
   "combined_s1": 0.8666585326677869,
   "combined_s3": 0.8656762750815459,
   "combined_s10": 0.8609456854798854
  },
  {
   "pair": "Synechococcus elongatus -> Prochlorococcus marinus",
   "copies_only": 0.5774197206830628,
   "memorisation": 0.8342100241585029,
   "law_base": 0.7882854663743164,
   "law_context": 0.8025825475519264,
   "combined_s1": 0.8507150340775305,
   "combined_s3": 0.8458005249343832,
   "combined_s10": 0.8371065242359108
  },
  {
   "pair": "Cereibacter sphaeroides -> Candidatus Pelagibacter ubique",
   "copies_only": 0.6059059693903209,
   "memorisation": 0.8298449958930059,
   "law_base": 0.8205165313500556,
   "law_context": 0.833178366477987,
   "combined_s1": 0.8688656314433709,
   "combined_s3": 0.8737565865569978,
   "combined_s10": 0.8743622983521734
  },
  {
   "pair": "Nitratidesulfovibrio vulgaris -> Desulfotalea psychrophila",
   "copies_only": 0.6445834877033273,
   "memorisation": 0.8158790489044141,
   "law_base": 0.8408346123989979,
   "law_context": 0.8394000740975971,
   "combined_s1": 0.8319440033873188,
   "combined_s3": 0.840801533114569,
   "combined_s10": 0.8524818284464204
  },
  {
   "pair": "Myxococcus xanthus -> Geobacter sulfurreducens",
   "copies_only": 0.6153687586486739,
   "memorisation": 0.8973952968554375,
   "law_base": 0.8556625187713074,
   "law_context": 0.8522620075674814,
   "combined_s1": 0.8991009714259951,
   "combined_s3": 0.9005051345811701,
   "combined_s10": 0.8996593419551292
  },
  {
   "pair": "Methanosarcina acetivorans -> Methanococcoides burtonii",
   "copies_only": 0.5879022613611655,
   "memorisation": 0.8194949989128071,
   "law_base": 0.7494466188301805,
   "law_context": 0.7691639486844967,
   "combined_s1": 0.8224048706240487,
   "combined_s3": 0.8240106544901066,
   "combined_s10": 0.8229212872363557
  },
  {
   "pair": "Methanosarcina acetivorans -> Halobacterium salinarum",
   "copies_only": 0.5851809733772395,
   "memorisation": 0.9090999469777307,
   "law_base": 0.7864449614890886,
   "law_context": 0.7928024013506726,
   "c
… (잘림, 원본 파일 참조)
```

## parasites

```json
{
 "mean_auroc": {
  "copies_only": 0.6466693047031259,
  "memorisation": 0.7882956723635105,
  "law_base": 0.7597640843822151,
  "law_context": 0.7653708430517742,
  "combined_s1": 0.7930777139503002,
  "combined_s3": 0.7983505889489837,
  "combined_s10": 0.804083652911769
 },
 "context_gain": {
  "mean": 0.005606758669558888,
  "n_better": 77,
  "n": 90
 },
 "heldout": [
  {
   "pair": "Tetrahymena thermophila -> Ichthyophthirius multifiliis",
   "clade": "alveolata",
   "copies_only": 0.6843729713573167,
   "memorisation": 0.7367493146398532,
   "law_base": 0.7509266567345878,
   "law_context": 0.7548917045346635,
   "combined_s1": 0.741658532636531,
   "combined_s3": 0.7475827530539586,
   "combined_s10": 0.761999834984269
  },
  {
   "pair": "Tetrahymena thermophila -> Perkinsus marinus",
   "clade": "alveolata",
   "copies_only": 0.6243565597008711,
   "memorisation": 0.8149340401825542,
   "law_base": 0.7633468015337095,
   "law_context": 0.7680986046732937,
   "combined_s1": 0.8199739094921075,
   "combined_s3": 0.8257098561056944,
   "combined_s10": 0.8347769023667818
  },
  {
   "pair": "Chromera velia -> Plasmodium falciparum",
   "clade": "alveolata",
   "copies_only": 0.624691069050213,
   "memorisation": 0.8396175340593539,
   "law_base": 0.801607753254184,
   "law_context": 0.8044127675393324,
   "combined_s1": 0.848090676691801,
   "combined_s3": 0.8552812100787723,
   "combined_s10": 0.8620126717164559
  },
  {
   "pair": "Chromera velia -> Babesia bovis",
   "clade": "alveolata",
   "copies_only": 0.6090961112595233,
   "memorisation": 0.8509306418657702,
   "law_base": 0.8073843102506123,
   "law_context": 0.8090489599710378,
   "combined_s1": 0.8590684968568241,
   "combined_s3": 0.8656030134004059,
   "combined_s10": 0.8714049575516755
  },
  {
   "pair": "Chromera velia -> Toxoplasma gondii",
   "clade": "alveolata",
   "copies_only": 0.6233197287534065,
   "memorisation": 0.8352415235439509,
   "law_base": 0.8038575321630015,
   "law_context": 0.8085827999239495,
   "combined_s1": 0.8461910133722036,
   "combined_s3": 0.8549682489384625,
   "combined_s10": 0.8647108181760568
  },
  {
   "pair": "Chromera velia -> Eimeria tenella",
   "clade": "alveolata",
   "copies_only": 0.6630382613043462,
   "memorisation": 0.8245289378666494,
   "law_base": 0.8121326349899428,
   "law_context": 0.8129129278132526,
   "combined_s1": 0.8346793046591425,
   "combined_s3": 0.8426978809241186,
   "combined_s10": 0.8520303834718188
  },
  {
   "pair": "Chromera velia -> Cryptosporidium parvum",
   "clade": "alveolata",
   "copies_only": 0.6330129445537315,
   "memorisation": 0.8663920616213527,
   "law_base": 0.8228804759755879,
   "law_context": 0.8219725901228835,
   "combined_s1": 0.8771438154474952,
   "combined_s3": 0.8835330925610316,
   "combined_s10": 0.8878269301823609
  },
  {
   "pair": "Chromera velia -> Plasmodium vivax",
   "clade": "alveolata",
   "copies_only": 0.6212876672589477,
   "memorisation": 0.8349933583096516,
   "law_base": 0.7993641726610466,
   "law_context": 0.80284533449881,
   "combined_s1": 0.8435030240684934,
   "combined_s3": 0.8508458612535618,
   "combined_s10": 0.8579990381000185
  },
  {
   "pair": "Chromera velia -> Plasmodium berghei",
   "clade": "alveolata",
   "copies_only": 0.6191111999759492,
   "memorisation": 0.8398718580699162,
   "law_base": 0.8016054843390834,
   "law_context": 0.8046597889735809,
   "combined_s1": 0.8485116438653596,
   "combined_s3": 0.8557127975388046,
   "combined_s10": 0.8625262279850752
  },
  {
   "pair": "Chromera velia -> Plasmodium knowlesi",
   "clade": "alveolata",
   "copies_only": 0.6172615991923694,
   "memorisation": 0.8382551497895047,
   "law_base": 0.8000923660596715,
   "law_context": 0.803463536398716,
   "combined_s1": 0.8469209086988218,
   "combined_s3": 0.8544170632936515,
   "combined_s10": 0.8616458047870046
  },
  {
   "pair": "Chromera velia -> Theileria annulata",
   "clade": "alveolata",
   "copies_only": 0.6151684992058313,
   "memorisation": 0.8489118041789281,
   "law_base": 0.8079232180454831,
   "law_context": 0.8091865003632245,
   "combined_s1": 0.8573210042232537,
   "combined_s3": 0.8641062831673172,
   "combined_s10": 0.8704064420010589
  },
  {
   "pair": "Chromera velia -> Theileria parva",
   "clade": "alveolata",
   "copies_only": 0.6076658641801806,
   "memorisation": 0.8529880604675604,
   "law_base": 0.8109606618680419,
   "law_context": 0.8123506336384412,
   "combined_s1": 0.8614232118197706,
   "combined_s3": 0.8684043554241161,
   "combined_s10": 0.874762981339134
  },
  {
   "pair": "Chromera velia -> Babesia microti",
   "clade": "alveolata",
   "copies_only": 0.596199045904687,
   "memorisation": 0.8466451661331746,
   "law_base": 0.7995210513668266,
   "law_context": 0.8012343675133812,
   "combined_s1": 0.8548382536945969,
   "combined_s3": 0.8614699813850516,
   "combined_s10": 0.8670788374016671
  },
  {
   "pair": "Chromera velia -> Neospora caninum",
   "clade": "alveolata",
   "copies_only": 0.6402126539997026,
   "memorisation": 0.8320961217763325,
   "law_base": 0.8149989282003663,
   "law_context": 0.818706708371526,
   "combined_s1": 0.8431141474070157,
   "combined_s3": 0.8524281110911617,
   "combined_s10": 0.8633816049341577
  },
  {
   "pair": "Chromera velia -> Hammondia hammondi",
   "clade": "alveolata",
   "copies_only": 0.6259803786879641,
   "memorisation": 0.8342644831965611,
   "law_base": 0.8074873099029569,
   "law_context": 0.8120206867917155,
   "combined_s1": 0.8453645019213234,
   "combined_s3": 0.8542788625928097,
   "combined_s10": 0.8645128610622639
  },
  {
   "pair": "Chromera velia -> Cyclospora cayetanensis",
   "clade": "alveolata",
   "copies_only": 0.6551266858529429,
   "memorisation": 0.8274399615891899,
   "law_base": 0.8101921592594824,
   "law_context": 0.8128864633457001,
   "combined_s1": 0.8378295788105465,
   "combined_s3": 0.8460255906283745,
   "combined_s10": 0.8555369527105158
  },
  {
   "pair": "Chromera velia
… (잘림, 원본 파일 참조)
```

## 연결
- [[실험 목록]]
