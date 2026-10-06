---
유형: 실험
실행: animal_content
산출: results/animal_content/metrics.json
tags:
  - 유형/실험
  - 실험/animal_content
---

# 실험 · animal_content

**산출물** `results/animal_content/metrics.json`

## pairs

```json
[
 {
  "origin": "nematode parasitism, filarial",
  "proxy": "Caenorhabditis elegans",
  "descendant": "Brugia malayi",
  "distant": false,
  "design": [
   1.0,
   -0.85,
   0.0,
   0.0,
   0.0,
   1.0
  ],
  "share_lost": 0.1333
 },
 {
  "origin": "nematode parasitism, Trichinella",
  "proxy": "Caenorhabditis elegans",
  "descendant": "Trichinella spiralis",
  "distant": false,
  "design": [
   1.0,
   -0.85,
   0.0,
   0.0,
   0.0,
   1.0
  ],
  "share_lost": 0.2856
 },
 {
  "origin": "flatworm parasitism",
  "proxy": "Macrostomum lignano",
  "descendant": "Schistosoma mansoni",
  "distant": false,
  "design": [
   1.0,
   -0.85,
   1.0,
   1.0,
   0.0,
   1.0
  ],
  "share_lost": 0.2603
 },
 {
  "origin": "flatworm parasitism",
  "proxy": "Macrostomum lignano",
  "descendant": "Echinococcus granulosus",
  "distant": false,
  "design": [
   1.0,
   -0.85,
   1.0,
   1.0,
   0.0,
   1.0
  ],
  "share_lost": 0.3039
 },
 {
  "origin": "bird endothermy",
  "proxy": "Crocodylus porosus",
  "descendant": "Gallus gallus",
  "distant": false,
  "design": [
   1.0,
   -0.575,
   0.0,
   0.0,
   1.0,
   0.0
  ],
  "share_lost": 0.033
 },
 {
  "origin": "bird endothermy",
  "proxy": "Crocodylus porosus",
  "descendant": "Anas platyrhynchos",
  "distant": false,
  "design": [
   1.0,
   -0.575,
   0.0,
   0.0,
   1.0,
   0.0
  ],
  "share_lost": 0.0283
 },
 {
  "origin": "bird endothermy",
  "proxy": "Crocodylus porosus",
  "descendant": "Taeniopygia guttata",
  "distant": false,
  "design": [
   1.0,
   -0.55,
   0.0,
   0.0,
   1.0,
   0.0
  ],
  "share_lost": 0.0388
 },
 {
  "ori
… (잘림 — 원본 파일 참조)
```

## heldout

```json
[
 {
  "origin": "nematode parasitism, filarial",
  "pair": "Caenorhabditis elegans -> Brugia malayi",
  "distant": false,
  "design": [
   1.0,
   -0.85,
   0.0,
   0.0,
   0.0,
   1.0
  ],
  "n_ancestral": 5452,
  "n_lost": 727,
  "copies_only": 0.552889674897928,
  "rarity": 0.8675363711127122,
  "memorisation": 0.8735344934244521,
  "no_axes": 0.7560335654971143,
  "axis_law": 0.7276207943058012
 },
 {
  "origin": "nematode parasitism, Trichinella",
  "pair": "Caenorhabditis elegans -> Trichinella spiralis",
  "distant": false,
  "design": [
   1.0,
   -0.85,
   0.0,
   0.0,
   0.0,
   1.0
  ],
  "n_ancestral": 5452,
  "n_lost": 1557,
  "copies_only": 0.6057875196944851,
  "rarity": 0.8292338299105534,
  "memorisation": 0.7709938882169473,
  "no_axes": 0.7611096682916936,
  "axis_law": 0.7514393154275322
 },
 {
  "origin": "flatworm parasitism",
  "pair": "Macrostomum lignano -> Schistosoma mansoni",
  "distant": false,
  "design": [
   1.0,
   -0.85,
   1.0,
   1.0,
   0.0,
   1.0
  ],
  "n_ancestral": 5821,
  "n_lost": 1515,
  "copies_only": 0.6608851874504682,
  "rarity": 0.8119416609566205,
  "memorisation": 0.7609233566180584,
  "no_axes": 0.6856903943994028,
  "axis_law": 0.6358845359686921
 },
 {
  "origin": "flatworm parasitism",
  "pair": "Macrostomum lignano -> Echinococcus granulosus",
  "distant": false,
  "design": [
   1.0,
   -0.85,
   1.0,
   1.0,
   0.0,
   1.0
  ],
  "n_ancestral": 5821,
  "n_lost": 1769,
  "copies_only": 0.6691935031141235,
  "rarity": 0.8213766540903807,
  "memorisation": 0.7689029334312502,
  "no_axes": 0.679008949233732,
  "axis_la
… (잘림 — 원본 파일 참조)
```

## summary

```json
{
 "all": {
  "copies_only": {
   "mean": 0.6755,
   "ci95": [
    0.6488,
    0.6962
   ],
   "n_pairs": 23,
   "n_origins": 17
  },
  "rarity": {
   "mean": 0.8361,
   "ci95": [
    0.8077,
    0.8588
   ],
   "n_pairs": 23,
   "n_origins": 17
  },
  "memorisation": {
   "mean": 0.7763,
   "ci95": [
    0.7484,
    0.8074
   ],
   "n_pairs": 23,
   "n_origins": 17
  },
  "no_axes": {
   "mean": 0.8009,
   "ci95": [
    0.7717,
    0.8237
   ],
   "n_pairs": 23,
   "n_origins": 17
  },
  "axis_law": {
   "mean": 0.7943,
   "ci95": [
    0.7558,
    0.8219
   ],
   "n_pairs": 23,
   "n_origins": 17
  },
  "axis_law - no_axes": {
   "mean": -0.0066,
   "ci95": [
    -0.0175,
    0.0008
   ],
   "n_pairs": 23,
   "n_origins": 17
  },
  "axis_law - memorisation": {
   "mean": 0.0181,
   "ci95": [
    -0.032,
    0.0589
   ],
   "n_pairs": 23,
   "n_origins": 17
  },
  "axis_law - rarity": {
   "mean": -0.0418,
   "ci95": [
    -0.0842,
    -0.0077
   ],
   "n_pairs": 23,
   "n_origins": 17
  },
  "axes_better_in": 9
 },
 "close_proxies_only": {
  "copies_only": {
   "mean": 0.6776,
   "ci95": [
    0.6473,
    0.6987
   ],
   "n_pairs": 21,
   "n_origins": 16
  },
  "rarity": {
   "mean": 0.8324,
   "ci95": [
    0.8037,
    0.857
   ],
   "n_pairs": 21,
   "n_origins": 16
  },
  "memorisation": {
   "mean": 0.7681,
   "ci95": [
    0.7439,
    0.7968
   ],
   "n_pairs": 21,
   "n_origins": 16
  },
  "no_axes": {
   "mean": 0.8007,
   "ci95": [
    0.7671,
    0.8272
   ],
   "n_pairs": 21,
   "n_origins": 16
  },
  "axis_law": {
   "mean": 0.7924,
   "ci95": [
    0.7477,
   
… (잘림 — 원본 파일 참조)
```

## significant_effects

```json
{
 "loss_colder": [
  [
   "go:receptor ligand activity",
   -0.539,
   0.265
  ],
  [
   "go:oxidoreductase activity",
   -0.29,
   0.145
  ],
  [
   "kw:phosphatase",
   -0.238,
   0.113
  ],
  [
   "clan_size",
   0.065,
   0.032
  ]
 ],
 "loss_freshwater": [
  [
   "kw:cell_adhesion_surface",
   0.411,
   0.114
  ],
  [
   "kw:transporter_channel",
   0.294,
   0.123
  ],
  [
   "go:signaling",
   0.273,
   0.096
  ],
  [
   "kw:methyl_glyco_transferase",
   -0.253,
   0.106
  ],
  [
   "has_go_annotation",
   -0.111,
   0.037
  ]
 ],
 "loss_hypoxia": [
  [
   "go:molecular function regulator activity",
   0.364,
   0.138
  ],
  [
   "go:catalytic activity, acting on RNA",
   0.341,
   0.171
  ]
 ],
 "loss_endothermy": [
  [
   "translation",
   0.726,
   0.342
  ],
  [
   "kw:cilium_flagellum",
   0.632,
   0.258
  ],
  [
   "go:ATP-dependent activity",
   -0.385,
   0.174
  ],
  [
   "kw:uncharacterised",
   0.347,
   0.153
  ],
  [
   "kw:ubiquitin_system",
   -0.299,
   0.151
  ],
  [
   "protein_length",
   -0.272,
   0.092
  ],
  [
   "hmm_length",
   0.216,
   0.077
  ],
  [
   "has_go_annotation",
   -0.108,
   0.04
  ],
  [
   "clan_size",
   0.106,
   0.039
  ]
 ],
 "loss_parasite": [
  [
   "transcription",
   1.148,
   0.501
  ],
  [
   "go:oxidoreductase activity",
   -0.476,
   0.168
  ],
  [
   "kw:kinase",
   0.465,
   0.213
  ],
  [
   "go:ATP-dependent activity",
   0.389,
   0.142
  ],
  [
   "ubiquity_free_living",
   0.286,
   0.121
  ]
 ],
 "duplication_colder": [
  [
   "kw:phosphatase",
   -0.379,
   0.141
  ],
  [
   "go:oxidoreductase activity"
… (잘림 — 원본 파일 참조)
```

## 연결
- [[실험 목록]]
