---
유형: 환경
법칙: fungal_ancestor_v1
클러스터: 조상 복원
tags:
  - 법칙/fungal_ancestor_v1
  - 클러스터/조상 복원
  - 판정/양성
  - 유형/환경
---

# fungal_ancestor_v1 · 환경

← [[fungal_ancestor_v1]]

**카탈로그** ribosomal marker tree + UniProt · **종 수** —

## 환경 범위

```json
{
 "대상": "균류 289종(16개 문, 목마다 고르게) + 외군 45종",
 "환경": "자유생활·공생·기생 균류 모두. 레퍼런스 프로테옴이 없는 계통(아펠리다 등)과 누클레아리아는 미포함"
}
```

## 요약 수치

```json
{
 "잎 숨기기 (복원 / 현생 빈도)": {
  "reconstruction": 0.9721,
  "clade_frequency": 0.95
 },
 "알려진 정답 (복원 / 현생 빈도 AUROC, 크기 편향)": [
  0.8499,
  0.7453,
  -0.0567
 ],
 "chitin cell wall (expected present)": {
  "Chitin_synth_1": 0.116,
  "Chitin_synth_2": 0.998,
  "Chitin_synth_1N": 0.101
 },
 "fungal-specific Zn2Cys6 transcription factors (expected present)": {
  "Zn_clus": 1.0,
  "Fungal_trans": 0.113
 },
 "flagellum (expected present: chytrids, Rozella and Blastocladiomycota swim; Dikarya lost it)": {
  "Radial_spoke_3": 1.0,
  "IFT57": 1.0,
  "IFT52_GIFT": 1.0,
  "BBS2_Mid": 0.0,
  "Dynein_heavy": 1.0
 },
 "sterol synthesis": {
  "ERG4_ERG24": 0.999,
  "SQS_PSY": 1.0,
  "p450": 1.0
 },
 "actin cytoskeleton": {
  "Actin": 1.0,
  "Cofilin_ADF": 1.0,
  "FH2": 1.0,
  "Myosin_head": 1.0
 },
 "peroxisome": {
  "Pex2_Pex12": 0.999,
  "Pex14_N": 0.972
 },
 "mitochondrion-encoded (absent from most UniProt proteomes: an artifact, not loss)": {
  "COX2": 0.233,
  "COX3": 0.167,
  "Cytochrome_B": 0.167
 }
}
```

> [!note]
> envelope 밖의 환경에 이 법칙을 쓰면 외삽이다. 값은 문헌 근사치(카탈로그 주석 참조).
