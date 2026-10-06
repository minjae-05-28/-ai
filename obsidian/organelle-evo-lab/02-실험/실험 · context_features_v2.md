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
  
… (잘림 — 원본 파일 참조)
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

… (잘림 — 원본 파일 참조)
```

## 연결
- [[실험 목록]]
