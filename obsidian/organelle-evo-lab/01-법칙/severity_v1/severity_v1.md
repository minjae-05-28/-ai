---
유형: 법칙 허브
법칙: severity_v1
클러스터: 소기관
판정: 양성
기준선대비: 0.3966
tags:
  - 법칙/severity_v1
  - 클러스터/소기관
  - 판정/양성
---

# severity_v1

> [!abstract] 적용 범위
> Share of ancestral gene families lost by a eukaryotic lineage, from its lifestyle axes.

**모형** — logit(share lost) = b0 + b_parasite + b_intracellular + b_reduced_mitochondria (additive).

## 판정 — 양성

| 비교한 곳 | 법칙 | 기준선 | 차이 | 방향 |
| --- | --- | --- | --- | --- |
| loco_rmse_logit (rmse) | `all_axes` 1.041 | `mean_only` 1.437 | +0.3966 | 낮을수록 좋음 |

판정은 표의 첫 줄(교차검증 쪽, AUROC 우선)로 매깁니다. 차이가 ±0.01 안이면 무승부. 비교는 같은 지표끼리만 합니다.

## 이 클러스터의 노트
- [[severity_v1 · 계수]] — 학습된 가중치와 신뢰구간
- [[severity_v1 · 검증]] — 기준선과 나란히 본 성적
- [[severity_v1 · 한계]] — 이 법칙을 깨뜨리는 조건
- [[severity_v1 · 환경]] — 어떤 환경의 종들에서 나왔나
- [[severity_v1 · 데이터]] — 쓰인 종·쌍·유전자군

## 이 법칙을 만든 실험
- (연결된 실행 기록 없음)

## 클러스터
- [[클러스터 · 소기관]]
- [[법칙 목록]]
