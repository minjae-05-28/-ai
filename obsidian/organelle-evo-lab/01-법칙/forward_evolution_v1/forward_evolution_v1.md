---
유형: 법칙 허브
법칙: forward_evolution_v1
클러스터: 예측
판정: 음성
기준선대비: -0.0201
tags:
  - 법칙/forward_evolution_v1
  - 클러스터/예측
  - 판정/음성
---

# forward_evolution_v1

> [!abstract] 적용 범위
> Evolving an ancestor proxy forward with the birth-death law alone (its lineage held out, the amount of loss predicted from the lifestyle/environment design) and comparing the result with the real descendant, for extremophile bacteria/archaea and eukaryote parasites, with the proxy as ancestor or a consensus ancestor (families shared with a close free-living relative).

**모형** — run_forward_evolution.py (200 stochastic replicates per pair) and run_function_level.py (GO-slim and keyword functions).

## 판정 — 음성

| 비교한 곳 | 법칙 | 기준선 | 차이 | 방향 |
| --- | --- | --- | --- | --- |
| extremophiles · family_level (auroc) | `law.loss_auroc` 0.793 | `memorisation.loss_auroc` 0.8131 | -0.0201 | 높을수록 좋음 |
| extremophiles_consensus · family_level (auroc) | `law.loss_auroc` 0.7642 | `memorisation.loss_auroc` 0.7878 | -0.0236 | 높을수록 좋음 |
| parasites · family_level (auroc) | `law.loss_auroc` 0.7739 | `memorisation.loss_auroc` 0.7883 | -0.0144 | 높을수록 좋음 |
| parasites_consensus · family_level (auroc) | `law.loss_auroc` 0.7482 | `memorisation.loss_auroc` 0.7607 | -0.0125 | 높을수록 좋음 |
| extremophiles · family_level (accuracy) | `law.fate_accuracy` 0.6799 | `memorisation.fate_accuracy` 0.7199 | -0.0400 | 높을수록 좋음 |
| extremophiles · function_level (spearman) | `law.spearman` 0.6623 | `memorisation.spearman` 0.7234 | -0.0611 | 높을수록 좋음 |
| extremophiles_consensus · family_level (accuracy) | `law.fate_accuracy` 0.7058 | `memorisation.fate_accuracy` 0.7419 | -0.0361 | 높을수록 좋음 |
| extremophiles_consensus · function_level (spearman) | `law.spearman` 0.6055 | `memorisation.spearman` 0.6811 | -0.0756 | 높을수록 좋음 |
| parasites · family_level (accuracy) | `law.fate_accuracy` 0.6464 | `memorisation.fate_accuracy` 0.6563 | -0.0099 | 높을수록 좋음 |
| parasites · function_level (spearman) | `law.spearman` 0.5399 | `memorisation.spearman` 0.5962 | -0.0563 | 높을수록 좋음 |
| parasites_consensus · family_level (accuracy) | `law.fate_accuracy` 0.6398 | `memorisation.fate_accuracy` 0.6531 | -0.0133 | 높을수록 좋음 |
| parasites_consensus · function_level (spearman) | `law.spearman` 0.4916 | `memorisation.spearman` 0.5576 | -0.0660 | 높을수록 좋음 |

판정은 표의 첫 줄(교차검증 쪽, AUROC 우선)로 매깁니다. 차이가 ±0.01 안이면 무승부. 비교는 같은 지표끼리만 합니다.

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
