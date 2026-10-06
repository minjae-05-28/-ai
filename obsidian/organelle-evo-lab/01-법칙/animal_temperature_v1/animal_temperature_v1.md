---
유형: 법칙 허브
법칙: animal_temperature_v1
클러스터: 동물
판정: 양성
기준선대비: 16.5799
tags:
  - 법칙/animal_temperature_v1
  - 클러스터/동물
  - 판정/양성
---

# animal_temperature_v1

> [!abstract] 적용 범위
> Whether the prokaryote temperature-composition law transfers to animal cells, tested on mitochondrion-encoded proteomes of endotherms (cells at 36-42 C) against ectotherms (cells near ambient, 12-27 C).

**모형** — Predicted IVYWREL difference from the fitted law (+0.00098 per C) against the observed difference; continuous slope over all animals; AT bias (FYMINK) as the control.

## 판정 — 양성

| 비교한 곳 | 법칙 | 기준선 | 차이 | 방향 |
| --- | --- | --- | --- | --- |
| endotherm_vs_ectotherm | `delta_temperature_c` 17 | `mean_ivywrel_ectotherm` 0.4201 | +16.5799 | 높을수록 좋음 |

## 이 클러스터의 노트
- [[animal_temperature_v1 · 계수]] — 학습된 가중치와 신뢰구간
- [[animal_temperature_v1 · 검증]] — 기준선과 나란히 본 성적
- [[animal_temperature_v1 · 한계]] — 이 법칙을 깨뜨리는 조건
- [[animal_temperature_v1 · 환경]] — 어떤 환경의 종들에서 나왔나
- [[animal_temperature_v1 · 데이터]] — 쓰인 종·쌍·유전자군

## 이 법칙을 만든 실험
- (연결된 실행 기록 없음)

## 클러스터
- [[클러스터 · 동물]]
- [[법칙 목록]]
