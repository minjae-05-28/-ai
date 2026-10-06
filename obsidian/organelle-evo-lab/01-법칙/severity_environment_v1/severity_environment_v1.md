---
유형: 법칙 허브
법칙: severity_environment_v1
클러스터: 소기관
판정: 양성
기준선대비: 0.0323
tags:
  - 법칙/severity_environment_v1
  - 클러스터/소기관
  - 판정/양성
---

# severity_environment_v1

> [!abstract] 적용 범위
> Share of a relative's gene families lost when a bacterium or archaeon moves to an extreme environment.

**모형** — logit(share lost) = environment change @ b (base, colder, saltier, anaerobic, radiation, oligotrophic).

## 판정 — 양성

| 비교한 곳 | 법칙 | 기준선 | 차이 | 방향 |
| --- | --- | --- | --- | --- |
| leave_one_pair_out_rmse_logit | `environment` 0.5372 | `mean_only` 0.5695 | +0.0323 | 낮을수록 좋음 |

## 이 클러스터의 노트
- [[severity_environment_v1 · 계수]] — 학습된 가중치와 신뢰구간
- [[severity_environment_v1 · 검증]] — 기준선과 나란히 본 성적
- [[severity_environment_v1 · 한계]] — 이 법칙을 깨뜨리는 조건
- [[severity_environment_v1 · 환경]] — 어떤 환경의 종들에서 나왔나
- [[severity_environment_v1 · 데이터]] — 쓰인 종·쌍·유전자군

## 이 법칙을 만든 실험
- (연결된 실행 기록 없음)

## 클러스터
- [[클러스터 · 소기관]]
- [[법칙 목록]]
