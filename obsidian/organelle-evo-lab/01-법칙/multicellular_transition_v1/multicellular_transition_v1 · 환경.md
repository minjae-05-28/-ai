---
유형: 환경
법칙: multicellular_transition_v1
클러스터: 전환 경로
tags:
  - 법칙/multicellular_transition_v1
  - 클러스터/전환 경로
  - 판정/음성
  - 유형/환경
---

# multicellular_transition_v1 · 환경

← [[multicellular_transition_v1]]

**카탈로그** scripts/transition_catalog.py + UniProt · **종 수** —

## 환경 범위

```json
{
 "대상": "독립 기원 5개: Volvocales, Metazoa, Dictyostelia, Phaeophyceae, Rhodophyta (Bangiophyceae + Florideophyceae)",
 "환경": "단세포 친척과 비교한 다세포 계통(클론형 4, 집합형 1)"
}
```

## 요약 수치

```json
{
 "한 기원 빼고 (법칙 / 기준선들)": {
  "law": 0.6191,
  "control_baseline": 0.7298,
  "rarity_baseline": 0.8137
 },
 "법칙+희귀도 − 대조+희귀도": {
  "mean": -0.0456,
  "ci95": [
   -0.0603,
   -0.0271
  ],
  "what": "law+rarity minus control+rarity, per origin: is the added information specific to this transition"
 }
}
```

> [!note]
> envelope 밖의 환경에 이 법칙을 쓰면 외삽이다. 값은 문헌 근사치(카탈로그 주석 참조).
