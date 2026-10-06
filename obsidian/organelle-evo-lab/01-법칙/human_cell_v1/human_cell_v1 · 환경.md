---
유형: 환경
법칙: human_cell_v1
클러스터: 실험실 대조
tags:
  - 법칙/human_cell_v1
  - 클러스터/실험실 대조
  - 판정/음성
  - 유형/환경
---

# human_cell_v1 · 환경

← [[human_cell_v1]]

**카탈로그** human body sites · **종 수** —

## 환경 범위

```json
{
 "부위": [
  "gut lumen (anaerobic, nutrient-rich)",
  "skin surface (aerobic, dry, nutrient-poor)",
  "blood and tissue (aerobic, nutrient-rich)"
 ],
 "공생균": [
  "Akkermansia muciniphila",
  "Bacteroides thetaiotaomicron",
  "Bifidobacterium longum",
  "Corynebacterium glutamicum",
  "Cutibacterium acnes",
  "Escherichia coli",
  "Faecalibacterium prausnitzii",
  "Lactobacillus crispatus",
  "Staphylococcus epidermidis",
  "Streptococcus salivarius"
 ]
}
```

## 요약 수치

```json
{
 "body_sites": {
  "gut lumen (anaerobic, nutrient-rich)": {
   "errors": {
    "ivywrel": 0.0105,
    "cvp": -0.0055,
    "acidic_excess": -0.0099,
    "n_side": -0.0194
   },
   "n_commensals": 6
  },
  "skin surface (aerobic, dry, nutrient-poor)": {
   "errors": {
    "ivywrel": -0.0032,
    "cvp": 0.0279,
    "acidic_excess": -0.0189,
    "n_side": -0.0228
   },
   "n_commensals": 2
  },
  "blood and tissue (aerobic, nutrient-rich)": {
   "errors": {
    "ivywrel": 0.0029,
    "cvp": 0.0269,
    "acidic_excess": 0.0025,
    "n_side": -0.023
   },
   "n_commensals": 2
  }
 }
}
```

> [!note]
> envelope 밖의 환경에 이 법칙을 쓰면 외삽이다. 값은 문헌 근사치(카탈로그 주석 참조).
