---
유형: 법칙 허브
법칙: sequence_v1
클러스터: 서열·조성
판정: 양성
기준선대비: 10.62
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
| temperature | `ogt_per_0.01_ivywrel` 7.342 | `rmse_mean_only` 17.96 | +10.6200 | 낮을수록 좋음 |

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
