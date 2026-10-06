---
유형: 실험
실행: severity
산출: results/severity/metrics.json
tags:
  - 유형/실험
  - 실험/severity
---

# 실험 · severity

**산출물** `results/severity/metrics.json`

## coefficients

```json
{
 "base": {
  "weight": -2.3182512805824067,
  "ci95": [
   -2.656063704887176,
   -2.0306440719220453
  ]
 },
 "parasite": {
  "weight": 0.9286313453495845,
  "ci95": [
   0.3758650072855674,
   1.3761585663538252
  ]
 },
 "intracellular": {
  "weight": 0.7595963641727695,
  "ci95": [
   -0.06470094033038123,
   1.424912780946958
  ]
 },
 "reduced_mitochondria": {
  "weight": 1.7190805569498995,
  "ci95": [
   0.9817859748393861,
   2.4844345930535296
  ]
 }
}
```

## loco_rmse_logit

```json
{
 "mean_only": 1.4373159872386505,
 "parasite_only": 1.2642714162437565,
 "all_axes": 1.040697811067861
}
```

## typical_share_lost

```json
{
 "free_living": 0.0896226357292453,
 "extracellular_parasite": 0.19946843895552296,
 "intracellular_parasite": 0.34750519316016293,
 "intracellular_reduced_mito": 0.7482041043116332
}
```

## severity

```json
{
 "Entamoeba histolytica": 0.5737122557726465,
 "Ichthyophthirius multifiliis": 0.3233148526407937,
 "Perkinsus marinus": 0.312226437117012,
 "Plasmodium falciparum": 0.5084249084249084,
 "Babesia bovis": 0.5699633699633699,
 "Toxoplasma gondii": 0.3785103785103785,
 "Eimeria tenella": 0.5037851037851038,
 "Cryptosporidium parvum": 0.5706959706959707,
 "Leishmania major": 0.22361024359775142,
 "Trypanosoma cruzi": 0.18988132417239226,
 "Trypanosoma brucei": 0.23079325421611493,
 "Rozella allomycis": 0.38211867781760256,
 "Encephalitozoon cuniculi": 0.7578653922739944,
 "Nosema ceranae": 0.7702110712863401,
 "Dictyostelium purpureum": 0.06816163410301954,
 "Acanthamoeba castellanii": 0.22135879218472468,
 "Vitrella brassicaformis": 0.13382173382173382,
 "Naegleria fowleri": 0.07715207144629124,
 "Kluyveromyces lactis": 0.08112395196011783,
 "Volvox carteri": 0.12294390552509489,
 "Salpingoeca rosetta": 0.09924190213645762,
 "Anopheles gambiae": 0.0658261011953496,
 "Pneumocystis jirovecii": 0.22531969309462915,
 "Taphrina deformans": 0.24782608695652175,
 "Ustilago maydis": 0.11530299457675076,
 "Malassezia globosa": 0.2758783305824098,
 "Batrachochytrium dendrobatidis": 0.22520908004778972,
 "Enterocytozoon bieneusi": 0.8245718837116687,
 "Nematocida parisii": 0.7757865392273995,
 "Vavraia culicis": 0.7737953006770211,
 "Encephalitozoon intestinalis": 0.7566706491437675,
 "Plasmodium vivax": 0.5057387057387057,
 "Plasmodium berghei": 0.5081807081807082,
 "Plasmodium knowlesi": 0.49621489621489623,
 "Theileria annulata": 0.5885225885225885,
 "Theileria parva": 0.57753357753
… (잘림 — 원본 파일 참조)
```

## more_lost_than_predicted

```json
[
 [
  "Fasciola hepatica",
  0.9679087181315743
 ],
 [
  "Trypanosoma congolense",
  0.7117426608369769
 ],
 [
  "Thelohanellus kitauei",
  0.6641756901021809
 ],
 [
  "Gregarina niphandrodes",
  0.5846153846153846
 ],
 [
  "Mitosporidium daphniae",
  0.6270410195141378
 ]
]
```

## less_lost_than_predicted

```json
[
 [
  "Varroa destructor",
  0.04710759374411155
 ],
 [
  "Cimex lectularius",
  0.03605408112168253
 ],
 [
  "Ixodes scapularis",
  0.029395138496325607
 ],
 [
  "Ipomoea triloba",
  0.009623259623259623
 ],
 [
  "Pyricularia oryzae",
  0.04054350208196362
 ]
]
```

## 연결
- [[실험 목록]]
