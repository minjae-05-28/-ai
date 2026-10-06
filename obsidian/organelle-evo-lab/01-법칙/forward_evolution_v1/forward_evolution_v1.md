---
유형: 법칙 허브
법칙: forward_evolution_v1
클러스터: 예측
판정: 양성
기준선대비: 0.0757
tags:
  - 법칙/forward_evolution_v1
  - 클러스터/예측
  - 판정/양성
---

# forward_evolution_v1

> [!abstract] 적용 범위
> Evolving an ancestor proxy forward with the birth-death law alone (its lineage held out, the amount of loss predicted from the lifestyle/environment design) and comparing the result with the real descendant, for extremophile bacteria/archaea and eukaryote parasites, with the proxy as ancestor or a consensus ancestor (families shared with a close free-living relative).

**모형** — run_forward_evolution.py (200 stochastic replicates per pair) and run_function_level.py (GO-slim and keyword functions).

## 판정 — 양성

| 비교한 곳 | 법칙 | 기준선 | 차이 | 방향 |
| --- | --- | --- | --- | --- |
| extremophiles · family_level | `fate_accuracy.law - no_change` -0.0403 | `fate_accuracy.law - no_axes_law` 0.0023 | +0.0426 | 낮을수록 좋음 |
| extremophiles · function_level | `mae.law - uniform` -0.0608 | `spearman.law - memorisation` -0.0611 | -0.0003 | 낮을수록 좋음 |
| extremophiles_consensus · family_level | `fate_accuracy.law - no_change` -0.0713 | `fate_accuracy.law - no_axes_law` 0.0044 | +0.0757 | 낮을수록 좋음 |
| extremophiles_consensus · function_level | `mae.law - uniform` -0.0453 | `spearman.law - memorisation` -0.0756 | -0.0303 | 낮을수록 좋음 |
| parasites · family_level | `fate_accuracy.law - no_change` 0.0303 | `fate_accuracy.law - no_axes_law` 0.0346 | +0.0043 | 낮을수록 좋음 |
| parasites · function_level | `mae.law - uniform` -0.0312 | `spearman.law - memorisation` -0.0563 | -0.0251 | 낮을수록 좋음 |
| parasites_consensus · family_level | `fate_accuracy.law - no_change` -0.0176 | `fate_accuracy.law - no_axes_law` 0.0217 | +0.0393 | 낮을수록 좋음 |
| parasites_consensus · function_level | `mae.law - uniform` -0.0282 | `spearman.law - memorisation` -0.0661 | -0.0379 | 낮을수록 좋음 |

## 이 클러스터의 노트
- [[forward_evolution_v1 · 계수]] — 학습된 가중치와 신뢰구간
- [[forward_evolution_v1 · 검증]] — 기준선과 나란히 본 성적
- [[forward_evolution_v1 · 한계]] — 이 법칙을 깨뜨리는 조건
- [[forward_evolution_v1 · 환경]] — 어떤 환경의 종들에서 나왔나
- [[forward_evolution_v1 · 데이터]] — 쓰인 종·쌍·유전자군

## 이 법칙을 만든 실험
- (연결된 실행 기록 없음)

## 클러스터
- [[클러스터 · 예측]]
- [[법칙 목록]]
