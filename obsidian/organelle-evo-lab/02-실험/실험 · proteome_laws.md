---
유형: 실험
실행: proteome_laws
산출: results/proteome_laws/metrics.json
tags:
  - 유형/실험
  - 실험/proteome_laws
---

# 실험 · proteome_laws

**산출물** `results/proteome_laws/metrics.json`

## temperature

```json
{
 "random_5fold": {
  "n": 7253,
  "n_orders": 180,
  "metric": "MAE (deg C)",
  "scores": {
   "mean": 6.1513,
   "taxonomy": 2.5764,
   "composition": 4.3874,
   "pfam": 2.6846,
   "composition+pfam": 2.6047
  }
 },
 "leave_order_out": {
  "n": 7253,
  "n_orders": 180,
  "metric": "MAE (deg C)",
  "scores": {
   "mean": 6.1993,
   "taxonomy": 5.5922,
   "composition": 5.0001,
   "pfam": 3.6522,
   "composition+pfam": 3.4673
  },
  "composition - taxonomy": {
   "mean": -0.5921,
   "ci95": [
    -2.181,
    0.6987
   ]
  },
  "pfam - taxonomy": {
   "mean": -1.94,
   "ci95": [
    -3.7571,
    -0.683
   ]
  },
  "composition+pfam - taxonomy": {
   "mean": -2.1249,
   "ci95": [
    -4.0506,
    -0.8447
   ]
  },
  "composition+pfam - composition": {
   "mean": -1.5329,
   "ci95": [
    -2.2396,
    -0.91
   ]
  }
 },
 "composition_coefficients": {
  "ivywrel": 5.645,
  "cvp": 1.6434,
  "acidic_excess": 0.5287,
  "n_side": -1.7241,
  "gravy": 0.3352,
  "fymink": 0.4681,
  "median_pi": 3.2292
 },
 "pfam_top": {
  "positive": [
   [
    "zf_Rg",
    "Reverse gyrase zinc finger",
    0.604
   ],
   [
    "SDH_protease",
    "ClpP-like SDH-type serine proteinase",
    0.573
   ],
   [
    "Endonuclease_5",
    "Endonuclease V",
    0.5
   ],
   [
    "Methyltr_RsmF_N",
    "N-terminal domain of 16S rRNA methyltransferase RsmF",
    0.472
   ],
   [
    "HSP20",
    "Hsp20/alpha crystallin family",
    0.47
   ],
   [
    "YjbQ",
    "UPF0047 protein YjbQ-like",
    0.44
   ],
   [
    "Methyltranf_PUA",
    "Methyltransferase RsmF PUA domain",
    0.421
   ],
   [
    "Carb_kin
… (잘림 — 원본 파일 참조)
```

## oxygen

```json
{
 "random_5fold": {
  "n": 5363,
  "n_orders": 177,
  "metric": "AUROC",
  "scores": {
   "mean": 0.5,
   "taxonomy": 0.9698,
   "composition": 0.949,
   "pfam": 0.9831,
   "composition+pfam": 0.9845
  }
 },
 "leave_order_out": {
  "n": 5363,
  "n_orders": 177,
  "metric": "AUROC",
  "scores": {
   "mean": 0.5,
   "taxonomy": 0.8297,
   "composition": 0.9232,
   "pfam": 0.9776,
   "composition+pfam": 0.9773
  },
  "composition - taxonomy": {
   "mean": 0.0936,
   "ci95": [
    0.0386,
    0.1837
   ]
  },
  "pfam - taxonomy": {
   "mean": 0.1479,
   "ci95": [
    0.0729,
    0.2804
   ]
  },
  "composition+pfam - taxonomy": {
   "mean": 0.1477,
   "ci95": [
    0.0715,
    0.2792
   ]
  },
  "composition+pfam - composition": {
   "mean": 0.0541,
   "ci95": [
    0.0239,
    0.1101
   ]
  }
 },
 "composition_coefficients": {
  "ivywrel": -0.0498,
  "cvp": -1.5399,
  "acidic_excess": 0.8501,
  "n_side": 0.2958,
  "gravy": -0.1422,
  "fymink": -1.5993,
  "median_pi": 0.6366
 },
 "pfam_top": {
  "positive": [
   [
    "Ribonuc_red_sm",
    "Ribonucleotide reductase, small chain",
    0.225
   ],
   [
    "Cu-oxidase_3",
    "Multicopper oxidase",
    0.206
   ],
   [
    "Cu-oxidase_2",
    "Multicopper oxidase",
    0.181
   ],
   [
    "GSHPx",
    "Glutathione peroxidase",
    0.177
   ],
   [
    "GmrSD_N",
    "GmrSD restriction endonuclease, N-terminal domain",
    0.172
   ],
   [
    "Thioredox_DsbH",
    "Protein of unknown function, DUF255",
    0.166
   ],
   [
    "ParD_antitoxin",
    "Bacterial antitoxin of ParD toxin-antitoxin type II system and RHH",
    0.166

… (잘림 — 원본 파일 참조)
```

## host

```json
{
 "random_5fold": {
  "n": 5851,
  "n_orders": 180,
  "metric": "AUROC",
  "scores": {
   "mean": 0.5,
   "taxonomy": 0.8476,
   "composition": 0.755,
   "pfam": 0.8922,
   "composition+pfam": 0.8925
  }
 },
 "leave_order_out": {
  "n": 5851,
  "n_orders": 180,
  "metric": "AUROC",
  "scores": {
   "mean": 0.5,
   "taxonomy": 0.4849,
   "composition": 0.6739,
   "pfam": 0.8405,
   "composition+pfam": 0.8431
  },
  "composition - taxonomy": {
   "mean": 0.1891,
   "ci95": [
    0.0986,
    0.2571
   ]
  },
  "pfam - taxonomy": {
   "mean": 0.3556,
   "ci95": [
    0.2569,
    0.4335
   ]
  },
  "composition+pfam - taxonomy": {
   "mean": 0.3582,
   "ci95": [
    0.2592,
    0.4363
   ]
  },
  "composition+pfam - composition": {
   "mean": 0.1691,
   "ci95": [
    0.0958,
    0.237
   ]
  }
 },
 "composition_coefficients": {
  "ivywrel": -0.5374,
  "cvp": -0.0257,
  "acidic_excess": -0.6257,
  "n_side": 0.4517,
  "gravy": 0.2499,
  "fymink": 1.1267,
  "median_pi": -0.7037
 },
 "pfam_top": {
  "positive": [
   [
    "PDZ",
    "PDZ domain",
    0.161
   ],
   [
    "Acetyltransf_4",
    "Acetyltransferase (GNAT) domain",
    0.147
   ],
   [
    "YadA_head",
    "YadA head domain repeat (2 copies)",
    0.142
   ],
   [
    "NUDIX-like",
    "NADH pyrophosphatase-like rudimentary NUDIX domain",
    0.117
   ],
   [
    "TetR_C_13_2",
    "Transcriptional regulator LmrA/YxaF-like, C-terminal domain",
    0.113
   ],
   [
    "NMN_transporter",
    "Nicotinamide mononucleotide transporter",
    0.112
   ],
   [
    "3-dmu-9_3-mt",
    "3-demethylubiquinone-9 3-methyltransferase
… (잘림 — 원본 파일 참조)
```

## 연결
- [[실험 목록]]
