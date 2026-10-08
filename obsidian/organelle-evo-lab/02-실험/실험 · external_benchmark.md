---
유형: 실험
실행: external_benchmark
산출: results/external_benchmark/summary.json
tags:
  - 유형/실험
  - 실험/external_benchmark
---

# 실험 · external_benchmark

**산출물** `results/external_benchmark/summary.json`

## 한눈에

| 항목 | 값 |
| --- | --- |
| source | Zmasek & Godzik 2011, Genome Biol 12:R4, Additional file 4 (Dollo parsimony, Pfam 24.0, 114 genomes); their tree is rooted between Unikonta and Bikonta |
| preregistration | docs/preregistration/2026-10-08_external_benchmark.md |

## preregistered

```json
{
 "LECA v2 (minimum over 4 roots) vs their Eukaryota": {
  "n_families_compared": 5321,
  "n_in_their_node": 3543,
  "auroc_ours": 0.8998,
  "auroc_present_day_frequency": 0.9121,
  "ours_minus_frequency": {
   "mean": -0.0123,
   "ci95": [
    -0.0213,
    -0.0033
   ]
  },
  "verdict": "음성",
  "ours_p_ge_0.9": 1640,
  "theirs": 3543,
  "jaccard": 0.4604,
  "precision": 0.9963,
  "recall": 0.4612,
  "ours_only_examples": [
   "RNA_pol_Rpb1_6",
   "IRS",
   "DUF2921",
   "DUF2418",
   "GAS2",
   "Hexapep"
  ],
  "theirs_only_examples": [
   "Acyl-ACP_TE",
   "FGF",
   "ANATO",
   "ATS3",
   "Caldesmon",
   "Cornifin",
   "DUF641",
   "Dehydrin",
   "FYTT",
   "GASA",
   "Glycophorin_A",
   "IFP_35_N",
   "INCENP_N",
   "MARCKS",
   "MFMR",
   "Matrilin_ccoil",
   "NESP55",
   "NGF",
   "PduV-EutP",
   "Pedibin",
   "Prog_receptor",
   "SAB",
   "TCP",
   "Terpene_synth_C",
   "zf-RNPHF"
  ]
 },
 "LECA v1 (minimum over 2 roots) vs their Eukaryota": {
  "n_families_compared": 5408,
  "n_in_their_node": 3554,
  "auroc_ours": 0.9043,
  "auroc_present_day_frequency": 0.9109,
  "ours_minus_frequency": {
   "mean": -0.0066,
   "ci95": [
    -0.0153,
    0.0021
   ]
  },
  "verdict": "무승부",
  "ours_p_ge_0.9": 1779,
  "theirs": 3554,
  "jaccard": 0.4985,
  "precision": 0.9972,
  "recall": 0.4992,
  "ours_only_examples": [
   "RNA_pol_Rpb1_6",
   "DUF2921",
   "IRS",
   "Metallophos_C",
   "DUF1746"
  ],
  "theirs_only_examples": [
   "DUF1191",
   "DUF641",
   "Dehydrin",
   "FGF",
   "GASA",
   "Lipase3_N",
   "MFMR",
   "Na_trans_assoc",
   "PTB",
   "TCP",
   "Terpene_synth_C",

… (잘림 — 원본 파일 참조)
```

## exploratory

```json
{
 "LECA v2, Amorphea root only (their root) vs their Eukaryota": {
  "n_families_compared": 5321,
  "n_in_their_node": 3543,
  "auroc_ours": 0.9038,
  "auroc_present_day_frequency": 0.9121,
  "ours_minus_frequency": {
   "mean": -0.0084,
   "ci95": [
    -0.0163,
    -0.0005
   ]
  },
  "verdict": "음성",
  "ours_p_ge_0.9": 2209,
  "theirs": 3543,
  "jaccard": 0.6157,
  "precision": 0.9923,
  "recall": 0.6187,
  "ours_only_examples": [
   "RNA_pol_Rpb1_6",
   "DUF2921",
   "IRS",
   "Metallophos_C",
   "EST1_DNA_bind",
   "Hexapep",
   "RNA_pol_Rpb1_R",
   "GAS2",
   "Mrr_cat",
   "UPF0556",
   "DUF488",
   "PTA_PTB",
   "DBI_PRT",
   "DUF2418",
   "DUF1746",
   "UcrQ",
   "Glycos_transf_N"
  ],
  "theirs_only_examples": [
   "Acyl-ACP_TE",
   "FGF",
   "ANATO",
   "Caldesmon",
   "Cornifin",
   "FYTT",
   "Glycophorin_A",
   "IFP_35_N",
   "INCENP_N",
   "MARCKS",
   "Matrilin_ccoil",
   "NESP55",
   "NGF",
   "Pedibin",
   "Prog_receptor",
   "SAB",
   "zf-RNPHF",
   "ATS3",
   "DUF641",
   "Dehydrin",
   "GASA",
   "MFMR",
   "TCP",
   "Terpene_synth_C",
   "zf-XS"
  ]
 },
 "Core fungi (Rozella lineage excluded) vs their Fungi": {
  "n_families_compared": 3916,
  "n_in_their_node": 2973,
  "auroc_ours": 0.8783,
  "auroc_present_day_frequency": 0.9302,
  "ours_minus_frequency": {
   "mean": -0.0519,
   "ci95": [
    -0.0632,
    -0.0397
   ]
  },
  "verdict": "음성",
  "ours_p_ge_0.9": 2160,
  "theirs": 2973,
  "jaccard": 0.6709,
  "precision": 0.9542,
  "recall": 0.6932,
  "ours_only_examples": [
   "Rod_C",
   "FIBP",
   "DUF2045",
   "Copine",
   "CytochromB561_N",
   "PE
… (잘림 — 원본 파일 참조)
```

## 연결
- [[실험 목록]]
