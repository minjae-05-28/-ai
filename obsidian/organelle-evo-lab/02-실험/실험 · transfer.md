---
유형: 실험
실행: transfer
산출: results/transfer/metrics.json
tags:
  - 유형/실험
  - 실험/transfer
---

# 실험 · transfer

**산출물** `results/transfer/metrics.json`

## 한눈에

| 항목 | 값 |
| --- | --- |
| scheme | leave-one-clade-out |

## mean_auroc

```json
{
 "copies_only": 0.6466693047031259,
 "law": 0.7597347776910903,
 "memorisation": 0.7853556698489582
}
```

## by_clade

```json
{
 "alveolata": {
  "copies_only": 0.6312255739825979,
  "law": 0.8007985231064499,
  "memorisation": 0.833474005831232
 },
 "amoebozoa": {
  "copies_only": 0.6572025400251634,
  "law": 0.7975369752772457,
  "memorisation": 0.8046485213043763
 },
 "chelicerata": {
  "copies_only": 0.6457168422492694,
  "law": 0.7622225849296438,
  "memorisation": 0.7553246132922502
 },
 "chlorophyta": {
  "copies_only": 0.6748961370955746,
  "law": 0.7353019720979788,
  "memorisation": 0.6833514942075459
 },
 "cnidaria": {
  "copies_only": 0.6570664377828408,
  "law": 0.7935449094611517,
  "memorisation": 0.7469926466583562
 },
 "crustacea": {
  "copies_only": 0.6760715960303166,
  "law": 0.7722217944456234,
  "memorisation": 0.7578495962519258
 },
 "discoba": {
  "copies_only": 0.6348424115141006,
  "law": 0.7318188022088198,
  "memorisation": 0.7571935436461181
 },
 "fungi": {
  "copies_only": 0.6539375124486124,
  "law": 0.7618166396065966,
  "memorisation": 0.8040904886622249
 },
 "holozoa": {
  "copies_only": 0.6197295959408452,
  "law": 0.7311521564259638,
  "memorisation": 0.7408429243239899
 },
 "insecta": {
  "copies_only": 0.6426563251563252,
  "law": 0.7467235850569184,
  "memorisation": 0.7824406766073433
 },
 "metamonada": {
  "copies_only": 0.649854524849393,
  "law": 0.7546693659181849,
  "memorisation": 0.8055078777345438
 },
 "nematoda": {
  "copies_only": 0.6497704142813309,
  "law": 0.7420982448996992,
  "memorisation": 0.7377156174887093
 },
 "platyhelminthes": {
  "copies_only": 0.6771573922559918,
  "law": 0.6769873568659129,
  "memorisation": 0.722998660522558
 },
 "s
… (잘림 — 원본 파일 참조)
```

## within_clade_5fold

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
  "pair": "Tetrahymena thermophila -> Ichthyophthirius multifiliis",
  "clade": "alveolata",
  "copies_only": 0.6843729713573167,
  "memorisation": 0.734020717257999,
  "law": 0.7505082795864644
 },
 {
  "pair": "Tetrahymena thermophila -> Perkinsus marinus",
  "clade": "alveolata",
  "copies_only": 0.6243565597008711,
  "memorisation": 0.8121580577242574,
  "law": 0.7617290314394585
 },
 {
  "pair": "Chromera velia -> Plasmodium falciparum",
  "clade": "alveolata",
  "copies_only": 0.624691069050213,
  "memorisation": 0.8362012194510895,
  "law": 0.8011360355575408
 },
 {
  "pair": "Chromera velia -> Babesia bovis",
  "clade": "alveolata",
  "copies_only": 0.6090961112595233,
  "memorisation": 0.8488751327802667,
  "law": 0.8079526560189423
 },
 {
  "pair": "Chromera velia -> Toxoplasma gondii",
  "clade": "alveolata",
  "copies_only": 0.6233197287534065,
  "memorisation": 0.8333633310095697,
  "law": 0.8020181253564864
 },
 {
  "pair": "Chromera velia -> Eimeria tenella",
  "clade": "alveolata",
  "copies_only": 0.6630382613043462,
  "memorisation": 0.8205810760264274,
  "law": 0.8130503318689624
 },
 {
  "pair": "Chromera velia -> Cryptosporidium parvum",
  "clade": "alveolata",
  "copies_only": 0.6330129445537315,
  "memorisation": 0.8670440112879663,
  "law": 0.8228084292698504
 },
 {
  "pair": "Chromera velia -> Plasmodium vivax",
  "clade": "alveolata",
  "copies_only": 0.6212876672589477,
  "memorisation": 0.8316072652076578,
  "law": 0.7988717714800473
 },
 {
  "pair": "Chromera velia -> Plasmodium berghei",
  "clade": "alveolata",
  "copies_only": 0.619111199
… (잘림 — 원본 파일 참조)
```

## 연결
- [[실험 목록]]
