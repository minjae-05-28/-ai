---
유형: 환경
법칙: lab_evolution_v1
클러스터: 실험실 대조
tags:
  - 법칙/lab_evolution_v1
  - 클러스터/실험실 대조
  - 판정/양성
  - 유형/환경
---

# lab_evolution_v1 · 환경

← [[lab_evolution_v1]]

**카탈로그** laboratory · **종 수** —

## 환경 범위

```json
{
 "LTEE": "대장균 REL606, Davis 최소배지 + 포도당(DM25), 37°C, 매일 1:100 희석, 12개 집단, 5만 세대",
 "MA": "돌연변이 축적: 단일 콜로니 병목, 선택압 거의 없음"
}
```

## 요약 수치

```json
{
 "LTEE (50,000 generations, 12 populations, selection)": {
  "auroc_comparative_loss_rate": 0.5897250688456503,
  "auroc_rarity_baseline": 0.5664957914253113,
  "auroc_minus_no_selection_control": {
   "mean": -0.005493386466515391,
   "ci95": [
    -0.06658759003265548,
    0.05623955525958089
   ]
  }
 },
 "MAE (mutation accumulation, almost no selection)": {
  "auroc_comparative_loss_rate": 0.5953360431705095,
  "auroc_rarity_baseline": 0.5597589179339828,
  "auroc_minus_no_selection_control": null
 },
 "LTEE (50,000 generations, 12 populations, selection), dispensable genes": {
  "auroc_comparative_loss_rate": 0.5645617245339034,
  "auroc_rarity_baseline": 0.5482238383762942,
  "auroc_minus_no_selection_control": {
   "mean": 0.002826493189253262,
   "ci95": [
    -0.05677099845617566,
    0.06641507273463902
   ]
  }
 },
 "MAE (mutation accumulation, almost no selection), dispensable genes": {
  "auroc_comparative_loss_rate": 0.5622187494886355,
  "auroc_rarity_baseline": 0.5345498355451556,
  "auroc_minus_no_selection_control": null
 }
}
```

> [!note]
> envelope 밖의 환경에 이 법칙을 쓰면 외삽이다. 값은 문헌 근사치(카탈로그 주석 참조).
