---
유형: 법칙 허브
법칙: loss_prediction_v1
클러스터: 예측
판정: 음성
기준선대비: -0.0201
tags:
  - 법칙/loss_prediction_v1
  - 클러스터/예측
  - 판정/음성
---

# loss_prediction_v1

> [!abstract] 적용 범위
> Which ancestral gene families a bacterial/archaeal lineage loses when it moves to an extreme environment, scored on held-out lineages: the birth-death law against a per-family propensity estimated from ~18,000 UniProt reference proteomes, and against close relatives of the descendant.

**모형** — propensity20k = rank average of rarity across ~18,000 proteomes and within-genus absence rate, with the evaluated pair's genera removed (a law: properties of the family). relatives = share of the descendant's genus (or family) lacking the family, without its own and the proxy's species (a predictor, not a law: it reads the lineage's relatives). Combinations are rank averages.

## 판정 — 음성

| 비교한 곳 | 법칙 | 기준선 | 차이 | 방향 |
| --- | --- | --- | --- | --- |
| extremophiles (auroc) | `law.auroc` 0.793 | `memorisation.auroc` 0.8131 | -0.0201 | 높을수록 좋음 |
| extremophiles_consensus (auroc) | `law.auroc` 0.7642 | `memorisation.auroc` 0.7878 | -0.0236 | 높을수록 좋음 |

판정은 표의 첫 줄(교차검증 쪽, AUROC 우선)로 매깁니다. 차이가 ±0.01 안이면 무승부. 비교는 같은 지표끼리만 합니다.

## 이 클러스터의 노트
- [[loss_prediction_v1 · 계수]] — 학습된 가중치와 신뢰구간
- [[loss_prediction_v1 · 검증]] — 기준선과 나란히 본 성적
- [[loss_prediction_v1 · 한계]] — 이 법칙을 깨뜨리는 조건
- [[loss_prediction_v1 · 환경]] — 어떤 환경의 종들에서 나왔나
- [[loss_prediction_v1 · 데이터]] — 쓰인 종·쌍·유전자군

## 이 법칙을 만든 실험
- (연결된 실행 기록 없음)

## 클러스터
- [[클러스터 · 예측]]
- [[법칙 목록]]
