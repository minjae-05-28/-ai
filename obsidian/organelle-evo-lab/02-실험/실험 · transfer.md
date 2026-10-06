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
 "stramenopiles": {
  "copies_only": 0.6157971020683191,
  "law": 0.7551533751309838,
  "memorisation": 0.8006636545849093
 },
 "streptophyta": {
  "copies_only": 0.7297131265800413,
  "law": 0.785835235879695,
  "memorisation": 0.7013534111780316
 }
}
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
  "copies_only": 0.6191111999759492,
  "memorisation": 0.8365352909260357,
  "law": 0.800768479366205
 },
 {
  "pair": "Chromera velia -> Plasmodium knowlesi",
  "clade": "alveolata",
  "copies_only": 0.6172615991923694,
  "memorisation": 0.83519170728356,
  "law": 0.7993934183457315
 },
 {
  "pair": "Chromera velia -> Theileria annulata",
  "clade": "alveolata",
  "copies_only": 0.6151684992058313,
  "memorisation": 0.8468925225014468,
  "law": 0.8087358557937377
 },
 {
  "pair": "Chromera velia -> Theileria parva",
  "clade": "alveolata",
  "copies_only": 0.6076658641801806,
  "memorisation": 0.8508318566767283,
  "law": 0.811509611506923
 },
 {
  "pair": "Chromera velia -> Babesia microti",
  "clade": "alveolata",
  "copies_only": 0.596199045904687,
  "memorisation": 0.8447378528809789,
  "law": 0.7999777731959365
 },
 {
  "pair": "Chromera velia -> Neospora caninum",
  "clade": "alveolata",
  "copies_only": 0.6402126539997026,
  "memorisation": 0.8294245803693059,
  "law": 0.8134598637148327
 },
 {
  "pair": "Chromera velia -> Hammondia hammondi",
  "clade": "alveolata",
  "copies_only": 0.6259803786879641,
  "memorisation": 0.8322757404422301,
  "law": 0.805545633466849
 },
 {
  "pair": "Chromera velia -> Cyclospora cayetanensis",
  "clade": "alveolata",
  "copies_only": 0.6551266858529429,
  "memorisation": 0.8236486156900891,
  "law": 0.8101115788124594
 },
 {
  "pair": "Chromera velia -> Cryptosporidium hominis",
  "clade": "alveolata",
  "copies_only": 0.6432884108352236,
  "memorisation": 0.8544267234314644,
  "law": 0.8142919002919853
 },
 {
  "pair": "Chromera velia -> Gregarina niphandrodes",
  "clade": "alveolata",
  "copies_only": 0.6840790247222995,
  "memorisation": 0.855346282618166,
  "law": 0.7847992998368938
 },
 {
  "pair": "Chromera velia -> Besnoitia besnoiti",
  "clade": "alveolata",
  "copies_only": 0.6249869426794984,
  "memorisation": 0.8357563178507574,
  "law": 0.8073604935692381
 },
 {
  "pair": "Chromera velia -> Plasmodium yoelii",
  "clade": "alveolata",
  "copies_only": 0.6201622156752824,
  "memorisation": 0.8371025417765002,
  "law": 0.8006739107098129
 },
 {
  "pair": "Chromera velia -> Plasmodium malariae",
  "clade": "alveolata",
  "copies_only": 0.623319219484268,
  "memorisation": 0.8369332792633764,
  "law": 0.8020665060470886
 },
 {
  "pair": "Dictyostelium discoideum -> Entamoeba histolytica",
  "clade": "amoebozoa",
  "copies_only": 0.6538274396929824,
  "memorisation": 0.8064114502708978,
  "law": 0.7979868098555212
 },
 {
  "pair": "Dictyostelium discoideum -> Entamoeba dispar",
  "clade": "amoebozoa",
  "copies_only": 0.6573835709065989,
  "memorisation": 0.8015171132599338,
  "law": 0.7968184083147105
 },
 {
  "pair": "Dictyostelium discoideum -> Entamoeba invadens",
  "clade": "amoebozoa",
  "copies_only": 0.660396609475909,
  "memorisation": 0.8060170003822971,
  "law": 0.7978057076615054
 },
 {
  "pair": "Galendromus occidentalis -> Varroa destructor",
  "clade": "chelicerata",
  "copies_only": 0.6222894997033814,
  "memorisation": 0.7592469843780898,
  "law": 0.7348799683606881
 },
 {
  "pair": "Galendromus occidentalis -> Ixodes scapularis",
  "clade": "chelicerata",
  "copies_only": 0.6613540313307349,
  "memorisation": 0.7643935208000439,
  "law": 0.7973893543200474
 },
 {
  "pair": "Galendromus occidentalis -> Sarcoptes scabiei",
  "clade": "chelicerata",
  "copies_only": 0.6535069957136919,
  "memorisation": 0.7423333346986171,
  "law": 0.754398432108196
 },
 {
  "pair": "Auxenochlorella protothecoides -> Helicosporidium sp. ATCC 50920",
  "clade": "chlorophyta",
  "copies_only": 0.6748961370955746,
  "memorisation": 0.6833514942075459,
  "law": 0.7353019720979788
 },
 {
  "pair": "Nematostella vectensis -> Thelohanellus kitauei",
  "clade": "cnidaria",
  "copies_only": 0.6671940548775719,
  "memorisation": 0.7371511755829947,
  "law": 0.7744537634610431
 },
 {
  "pair": "Nematostella vectensis -> Henneguya salminicola",
  "clade": "cnidaria",
  "copies_only": 0.6469388206881096,
  "memorisation": 0.7568341177337177,
  "law": 0.8126360554612604
 },
 {
  "pair": "Tigriopus californicus -> Lepeophtheirus salmonis",
  "clade": "crustacea",
  "copies_only": 0.6760715960303166,
  "memorisation": 0.7578495962519258,
  "law": 0.7722217944456234
 },
 {
  "pair": "Bodo saltans -> Leishmania major",
  "clade": "discoba",
  "copies_only": 0.6183900794168011,
  "memorisation": 0.7692092477651384,
  "
… (잘림, 원본 파일 참조)
```

## 연결
- [[실험 목록]]
