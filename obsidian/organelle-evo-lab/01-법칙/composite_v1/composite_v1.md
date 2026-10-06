---
유형: 법칙 허브
법칙: composite_v1
클러스터: 기생·극한
판정: 무승부
기준선대비: 0.0023
tags:
  - 법칙/composite_v1
  - 클러스터/기생·극한
  - 판정/무승부
---

# composite_v1

> [!abstract] 적용 범위
> Composite loss law for reconstructing ancestors of eukaryotic parasites from their genomes (reverse inference). Chosen by leave-one-out validation among law mixes.

**모형** — loss weights = 1.0 x eukaryote_axes law(design); used inside a Bayesian reverse birth-death reconstruction.

## 판정 — 무승부

| 비교한 곳 | 법칙 | 기준선 | 차이 | 방향 |
| --- | --- | --- | --- | --- |
| mean_auroc_recover_lost (auroc) | `axis law` 0.7762 | `prior only (no law)` 0.774 | +0.0023 | 높을수록 좋음 |

판정은 표의 첫 줄(교차검증 쪽, AUROC 우선)로 매깁니다. 차이가 ±0.01 안이면 무승부. 비교는 같은 지표끼리만 합니다.

## 이 클러스터의 노트
- [[composite_v1 · 계수]] — 학습된 가중치와 신뢰구간
- [[composite_v1 · 검증]] — 기준선과 나란히 본 성적
- [[composite_v1 · 한계]] — 이 법칙을 깨뜨리는 조건
- [[composite_v1 · 환경]] — 어떤 환경의 종들에서 나왔나
- [[composite_v1 · 데이터]] — 쓰인 종·쌍·유전자군

## 이 법칙을 만든 실험
- (연결된 실행 기록 없음)

## 클러스터
- [[클러스터 · 기생·극한]]
- [[법칙 목록]]
