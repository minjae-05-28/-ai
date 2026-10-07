---
유형: 환경
법칙: leca_ancestor_v2
클러스터: 조상 복원
tags:
  - 법칙/leca_ancestor_v2
  - 클러스터/조상 복원
  - 판정/양성
  - 유형/환경
---

# leca_ancestor_v2 · 환경

← [[leca_ancestor_v2]]

**카탈로그** ribosomal marker tree + UniProt · **종 수** —

## 환경 범위

```json
{
 "대상": "진핵생물 250종(큰 갈래마다 같은 몫으로 고름), 외군 없음; 계통수: IQ-TREE LG+F+G4 with -fast on the ribosomal concatenate afte",
 "환경": "모든 진핵생물 큰 갈래. 메타모나다·리자리아·합토파이트·크립토파이트·CRuMs는 매우 적거나 없음; 검증한 뿌리 위치: discoba, opisthokonta, amorphea, metamonada"
}
```

## 요약 수치

```json
{
 "잎 숨기기 (뿌리별)": {
  "discoba": {
   "reconstruction": 0.9851,
   "clade_frequency": 0.9149
  },
  "opisthokonta": {
   "reconstruction": 0.9794,
   "clade_frequency": 0.9184
  },
  "amorphea": {
   "reconstruction": 0.9846,
   "clade_frequency": 0.9099
  },
  "metamonada": {
   "reconstruction": 0.9835,
   "clade_frequency": 0.93
  }
 },
 "알려진 정답 (뿌리별 복원/현생 AUROC, 크기 편향)": {
  "discoba": [
   0.8057,
   0.7056,
   0.0805
  ],
  "opisthokonta": [
   0.863,
   0.7404,
   0.0431
  ],
  "amorphea": [
   0.8509,
   0.7335,
   0.0405
  ],
  "metamonada": [
   0.8247,
   0.7205,
   0.0636
  ]
 },
 "mitochondrion, nuclear-encoded (expected present: LECA had a mitochondrion)": {
  "Complex1_51K": 1.0,
  "ATP-synt_ab": 1.0,
  "Mito_carr": 1.0,
  "Tim17": 1.0
 },
 "meiosis and sex (expected present)": {
  "TP6A_N": 0.996,
  "Rad51": 1.0,
  "HORMA": 1.0,
  "Mnd1": 0.98
 },
 "cilium (expected present)": {
  "Radial_spoke_3": 1.0,
  "IFT57": 1.0,
  "IFT52_GIFT": 1.0,
  "Dynein_heavy": 1.0,
  "Tubulin": 1.0
 },
 "endomembrane and nucleus (expected present)": {
  "Clathrin": 1.0,
  "Sec23_trunk": 1.0,
  "Snf7": 1.0,
  "Ran_BP1": 1.0,
  "Nup96": 0.998,
  "Nup54": 0.996,
  "Nucleoporin_N": 1.0
 },
 "peroxisome and autophagy (expected present)": {
  "Pex2_Pex12": 0.697,
  "ATG7_N": 1.0,
  "APG12": 0.99
 },
 "spliceosome (expected present)": {
  "PRP8_domainIV": 1.0,
  "SF3b1": 0.999,
  "U6-snRNA_bdg": 1.0,
  "LSM": 1.0
 },
 "photosynthesis (expected ABSENT: the plastid came after LECA)": {
  "Photo_RC": 0.236,
  "PSII": 0.235,
  "PsbP": 0.0,
  "Chloroa_b-bind": 0.0,
  "PsaA_PsaB": 0.501
 },
 "panel choice error, kept for transparency (Nup153 was in the first panel as a nuclear-pore marker; this Pfam family is in 7% of sampled species, not pan-eukaryotic; Nup96/Nup54/Nucleoporin_N replaced it AFTER the results were seen)": {
  "Nup153": 0.002
 }
}
```

> [!note]
> envelope 밖의 환경에 이 법칙을 쓰면 외삽이다. 값은 문헌 근사치(카탈로그 주석 참조).
