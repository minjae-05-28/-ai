---
유형: 환경
법칙: leca_ancestor_v1
클러스터: 조상 복원
tags:
  - 법칙/leca_ancestor_v1
  - 클러스터/조상 복원
  - 판정/음성
  - 유형/환경
---

# leca_ancestor_v1 · 환경

← [[leca_ancestor_v1]]

**카탈로그** ribosomal marker tree + UniProt · **종 수** —

## 환경 범위

```json
{
 "대상": "진핵생물 256종(큰 갈래마다 같은 몫으로 고름), 외군 없음; 계통수: FastTree",
 "환경": "모든 진핵생물 큰 갈래. 메타모나다·리자리아·합토파이트·크립토파이트·CRuMs는 매우 적거나 없음; 검증한 뿌리 위치: discoba, opisthokonta"
}
```

## 요약 수치

```json
{
 "잎 숨기기 (뿌리별)": {
  "discoba": {
   "reconstruction": 0.9818,
   "clade_frequency": 0.9329
  },
  "opisthokonta": {
   "reconstruction": 0.9828,
   "clade_frequency": 0.9141
  }
 },
 "알려진 정답 (뿌리별 복원/현생 AUROC, 크기 편향)": {
  "discoba": [
   0.6196,
   0.5554,
   0.3428
  ],
  "opisthokonta": [
   0.8227,
   0.6721,
   -0.3804
  ]
 },
 "mitochondrion, nuclear-encoded (expected present: LECA had a mitochondrion)": {
  "Complex1_51K": 1.0,
  "ATP-synt_ab": 1.0,
  "Mito_carr": 0.999,
  "Tim17": 0.999
 },
 "meiosis and sex (expected present)": {
  "TP6A_N": 0.961,
  "Rad51": 1.0,
  "HORMA": 1.0,
  "Mnd1": 0.973
 },
 "cilium (expected present)": {
  "Radial_spoke_3": 0.998,
  "IFT57": 0.998,
  "IFT52_GIFT": 0.998,
  "Dynein_heavy": 1.0,
  "Tubulin": 1.0
 },
 "endomembrane and nucleus (expected present)": {
  "Clathrin": 0.999,
  "Sec23_trunk": 1.0,
  "Snf7": 0.999,
  "Ran_BP1": 1.0,
  "Nup96": 1.0,
  "Nup54": 0.998,
  "Nucleoporin_N": 1.0
 },
 "peroxisome and autophagy (expected present)": {
  "Pex2_Pex12": 1.0,
  "ATG7_N": 1.0,
  "APG12": 0.981
 },
 "spliceosome (expected present)": {
  "PRP8_domainIV": 0.999,
  "SF3b1": 0.996,
  "U6-snRNA_bdg": 1.0,
  "LSM": 1.0
 },
 "photosynthesis (expected ABSENT: the plastid came after LECA)": {
  "Photo_RC": 0.064,
  "PSII": 0.057,
  "PsbP": 0.0,
  "Chloroa_b-bind": 0.0,
  "PsaA_PsaB": 0.071
 },
 "panel choice error, kept for transparency (Nup153 was in the first panel as a nuclear-pore marker; this Pfam family is in 7% of sampled species, not pan-eukaryotic; Nup96/Nup54/Nucleoporin_N replaced it AFTER the results were seen)": {
  "Nup153": 0.002
 }
}
```

> [!note]
> envelope 밖의 환경에 이 법칙을 쓰면 외삽이다. 값은 문헌 근사치(카탈로그 주석 참조).
