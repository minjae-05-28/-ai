---
유형: 법칙 허브
법칙: sequence_v1
클러스터: 서열·조성
판정: 양성
기준선대비: 7.6411
tags:
  - 법칙/sequence_v1
  - 클러스터/서열·조성
  - 판정/양성
---

# sequence_v1

> [!abstract] 적용 범위
> Proteome amino-acid composition: temperature, salt, nutrient and genome-reduction signals.

**모형** — Correlations and least-squares axis laws on proteome statistics (scripts/run_sequence_laws.py).

## 판정 — 양성

| 비교한 곳 | 법칙 | 기준선 | 차이 | 방향 |
| --- | --- | --- | --- | --- |
| temperature (rmse) | `rmse_ivywrel_loo_group` 10.32 | `rmse_mean_only` 17.96 | +7.6411 | 낮을수록 좋음 |

판정은 표의 첫 줄(교차검증 쪽, AUROC 우선)로 매깁니다. 차이가 ±0.01 안이면 무승부. 비교는 같은 지표끼리만 합니다.

## 이 클러스터의 노트
- [[sequence_v1 · 계수]] — 학습된 가중치와 신뢰구간
- [[sequence_v1 · 검증]] — 기준선과 나란히 본 성적
- [[sequence_v1 · 한계]] — 이 법칙을 깨뜨리는 조건
- [[sequence_v1 · 환경]] — 어떤 환경의 종들에서 나왔나
- [[sequence_v1 · 데이터]] — 쓰인 종·쌍·유전자군

## 이 법칙을 만든 실험
- (연결된 실행 기록 없음)

## 클러스터
- [[클러스터 · 서열·조성]]
- [[법칙 목록]]
