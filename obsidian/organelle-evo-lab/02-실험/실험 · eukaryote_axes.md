---
유형: 실험
실행: eukaryote_axes
산출: results/eukaryote_axes/metrics.json
tags:
  - 유형/실험
  - 실험/eukaryote_axes
---

# 실험 · eukaryote_axes

**산출물** `results/eukaryote_axes/metrics.json`

## 한눈에

| 항목 | 값 |
| --- | --- |
| n_families | 11162 |

## pairs

```json
[
 "Dictyostelium discoideum -> Entamoeba histolytica",
 "Tetrahymena thermophila -> Ichthyophthirius multifiliis",
 "Tetrahymena thermophila -> Perkinsus marinus",
 "Chromera velia -> Plasmodium falciparum",
 "Chromera velia -> Babesia bovis",
 "Chromera velia -> Toxoplasma gondii",
 "Chromera velia -> Eimeria tenella",
 "Chromera velia -> Cryptosporidium parvum",
 "Bodo saltans -> Leishmania major",
 "Bodo saltans -> Trypanosoma cruzi",
 "Bodo saltans -> Trypanosoma brucei",
 "Spizellomyces punctatus -> Rozella allomycis",
 "Spizellomyces punctatus -> Encephalitozoon cuniculi",
 "Spizellomyces punctatus -> Nosema ceranae",
 "Dictyostelium discoideum -> Dictyostelium purpureum",
 "Dictyostelium discoideum -> Acanthamoeba castellanii",
 "Chromera velia -> Vitrella brassicaformis",
 "Naegleria gruberi -> Naegleria fowleri",
 "Saccharomyces cerevisiae -> Kluyveromyces lactis",
 "Chlamydomonas reinhardtii -> Volvox carteri",
 "Monosiga brevicollis -> Salpingoeca rosetta",
 "Drosophila melanogaster -> Anopheles gambiae"
]
```

## aic_relative

```json
{
 "shared": 749.6226839382434,
 "parasite_only": 368.0226495548268,
 "axes": 0.0
}
```

## loss_effects

```json
{
 "base": {
  "hydrophobicity_gravy": {
   "weight": 0.07400568604707419,
   "se": 0.035579567399862455
  },
  "tm_helices": {
   "weight": -0.007178240756253854,
   "se": 0.031658834973363276
  },
  "protein_length": {
   "weight": -0.14983329196211212,
   "se": 0.023287639071219203
  },
  "redox_core": {
   "weight": -0.006157287223893006,
   "se": 0.24165958818072714
  },
  "atp_synthase": {
   "weight": -0.386518839367805,
   "se": 0.24291086316262248
  },
  "translation": {
   "weight": -0.7528296707208599,
   "se": 0.19659650542441917
  },
  "transcription": {
   "weight": -1.2513515437562013,
   "se": 0.3254539220011023
  },
  "protein_targeting": {
   "weight": -0.30608869331801314,
   "se": 0.21811430113896635
  }
 },
 "parasite": {
  "hydrophobicity_gravy": {
   "weight": 0.039265375287118806,
   "se": 0.04268355202917735
  },
  "tm_helices": {
   "weight": 0.09805965624534053,
   "se": 0.037822369742166156
  },
  "protein_length": {
   "weight": 0.04355326462837418,
   "se": 0.026799659804920297
  },
  "redox_core": {
   "weight": -0.7040321049097266,
   "se": 0.31852081478097727
  },
  "atp_synthase": {
   "weight": -1.3322531762502574,
   "se": 0.2621959995927317
  },
  "translation": {
   "weight": -0.35789925653051274,
   "se": 0.24855812778468184
  },
  "transcription": {
   "weight": -0.034486666984996035,
   "se": 0.48061920516356404
  },
  "protein_targeting": {
   "weight": -0.21680752309664908,
   "se": 0.6608138459529989
  }
 },
 "intracellular": {
  "hydrophobicity_gravy": {
   "weight": 0.03863818982340858,
   "se": 0.04028870913458348
  },
  "tm_he
… (잘림 — 원본 파일 참조)
```

## duplication_effects

```json
{
 "base": {
  "hydrophobicity_gravy": {
   "weight": 0.12619607060016244,
   "se": 0.032292438417414526
  },
  "tm_helices": {
   "weight": -0.06383900101769618,
   "se": 0.023421468871201265
  },
  "protein_length": {
   "weight": -0.1708935310465521,
   "se": 0.023793893973286035
  },
  "redox_core": {
   "weight": -0.4322930289481622,
   "se": 0.48816674766163204
  },
  "atp_synthase": {
   "weight": -1.2530991519623107,
   "se": 0.30729945136422143
  },
  "translation": {
   "weight": -0.9631575792880203,
   "se": 0.35918168172790016
  },
  "transcription": {
   "weight": -1.3354972340039069,
   "se": 0.36512335223020764
  },
  "protein_targeting": {
   "weight": -1.1537977939498663,
   "se": 0.20219314602113328
  }
 },
 "parasite": {
  "hydrophobicity_gravy": {
   "weight": -0.021038868246628855,
   "se": 0.050045137378755336
  },
  "tm_helices": {
   "weight": 0.226956639744676,
   "se": 0.030170655073925384
  },
  "protein_length": {
   "weight": 0.021423402819271384,
   "se": 0.024306675511138742
  },
  "redox_core": {
   "weight": -0.6244051206245186,
   "se": 0.3045987243602256
  },
  "atp_synthase": {
   "weight": 0.38735097133390706,
   "se": 0.31154272549160056
  },
  "translation": {
   "weight": 0.7519536280480769,
   "se": 0.3478000078601831
  },
  "transcription": {
   "weight": 0.3625335342569805,
   "se": 0.4284604994191974
  },
  "protein_targeting": {
   "weight": 0.7209751678721525,
   "se": 0.1972171372316547
  }
 },
 "intracellular": {
  "hydrophobicity_gravy": {
   "weight": 0.14587962923091682,
   "se": 0.046873777075505926
  },
  "tm_helices": {

… (잘림 — 원본 파일 참조)
```

## heldout_parasites

```json
[
 {
  "pair": "Dictyostelium discoideum -> Entamoeba histolytica",
  "design": {
   "parasite": 1,
   "intracellular": 0,
   "reduced_mitochondria": 1
  },
  "copies_only": 0.6538274396929824,
  "lumped_parasite_law": 0.6699863744840041,
  "split_law": 0.6751703189499484
 },
 {
  "pair": "Tetrahymena thermophila -> Ichthyophthirius multifiliis",
  "design": {
   "parasite": 1,
   "intracellular": 0,
   "reduced_mitochondria": 0
  },
  "copies_only": 0.6843729713573167,
  "lumped_parasite_law": 0.6974327599815058,
  "split_law": 0.6977557860586615
 },
 {
  "pair": "Tetrahymena thermophila -> Perkinsus marinus",
  "design": {
   "parasite": 1,
   "intracellular": 1,
   "reduced_mitochondria": 0
  },
  "copies_only": 0.6243565597008711,
  "lumped_parasite_law": 0.6459617207046816,
  "split_law": 0.6443657587857208
 },
 {
  "pair": "Chromera velia -> Plasmodium falciparum",
  "design": {
   "parasite": 1,
   "intracellular": 1,
   "reduced_mitochondria": 0
  },
  "copies_only": 0.624691069050213,
  "lumped_parasite_law": 0.6656413905197389,
  "split_law": 0.668024793692106
 },
 {
  "pair": "Chromera velia -> Babesia bovis",
  "design": {
   "parasite": 1,
   "intracellular": 1,
   "reduced_mitochondria": 0
  },
  "copies_only": 0.6090961112595233,
  "lumped_parasite_law": 0.6643696836192337,
  "split_law": 0.6666537718354503
 },
 {
  "pair": "Chromera velia -> Toxoplasma gondii",
  "design": {
   "parasite": 1,
   "intracellular": 1,
   "reduced_mitochondria": 0
  },
  "copies_only": 0.6233197287534065,
  "lumped_parasite_law": 0.6637140503200456,
  "split_law": 0.663678813613
… (잘림 — 원본 파일 참조)
```

## plasmodium_ancestor

```json
{
 "ancestor_families": 2587,
 "lost": 685,
 "laws": {
  "free-living, aerobic": {
   "auroc": 0.6203105451810235,
   "fraction_lost_by_class": {
    "redox_core": 0.415338988724424,
    "atp_synthase": 0.25578970748711033,
    "translation": 0.17138644684510354,
    "transcription": 0.07674154920240228,
    "protein_targeting": 0.23072826823990766
   },
   "projected_families_kept": 2177.26,
   "matches_plasmodium_biology": false
  },
  "free-living, reduced mito": {
   "auroc": 0.6162786770744587,
   "fraction_lost_by_class": {
    "redox_core": 0.9236626794013352,
    "atp_synthase": 0.4345950660356715,
    "translation": 0.20325982930043374,
    "transcription": 0.049525457238734145,
    "protein_targeting": 0.1802022004578891
   },
   "projected_families_kept": 2167.5,
   "matches_plasmodium_biology": false
  },
  "parasite, aerobic": {
   "auroc": 0.6359406540944224,
   "fraction_lost_by_class": {
    "redox_core": 0.26242655492846656,
    "atp_synthase": 0.08305532274135727,
    "translation": 0.11410870902807653,
    "transcription": 0.07836710968726014,
    "protein_targeting": 0.20325929447710106
   },
   "projected_families_kept": 1307.42,
   "matches_plasmodium_biology": false
  },
  "parasite, reduced mito": {
   "auroc": 0.6204932188169195,
   "fraction_lost_by_class": {
    "redox_core": 0.7668558798414847,
    "atp_synthase": 0.16119728038815026,
    "translation": 0.14717122782454667,
    "transcription": 0.05414535174755229,
    "protein_targeting": 0.17338798345411982
   },
   "projected_families_kept": 1302.02,
   "matches_plasmodium_biology": false
  },
… (잘림 — 원본 파일 참조)
```

## 연결
- [[실험 목록]]
