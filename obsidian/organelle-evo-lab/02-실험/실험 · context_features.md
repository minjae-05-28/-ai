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
 
… (잘림 — 원본 파일 참조)
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
 
… (잘림 — 원본 파일 참조)
```

## 연결
- [[실험 목록]]
