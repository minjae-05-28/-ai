---
유형: 법칙 허브
법칙: environment_v1
클러스터: 기생·극한
판정: 무승부
기준선대비: -0.0077
tags:
  - 법칙/environment_v1
  - 클러스터/기생·극한
  - 판정/무승부
---

# environment_v1

> [!abstract] 적용 범위
> Gene-family loss, duplication and gain in bacteria and archaea when a lineage moves to a colder, saltier, anoxic, radiation-exposed or nutrient-poor environment.

**모형** — Linear birth-death per family; log rate = a_pair + x @ (environment change @ W).

## 판정 — 무승부

| 비교한 곳 | 법칙 | 기준선 | 차이 | 방향 |
| --- | --- | --- | --- | --- |
| leave_one_pair_out_auroc (auroc) | `environment_law` 0.808 | `no_environment` 0.8157 | -0.0077 | 높을수록 좋음 |

판정은 표의 첫 줄(교차검증 쪽, AUROC 우선)로 매깁니다. 차이가 ±0.01 안이면 무승부. 비교는 같은 지표끼리만 합니다.

## 이 클러스터의 노트
- [[environment_v1 · 계수]] — 학습된 가중치와 신뢰구간
- [[environment_v1 · 검증]] — 기준선과 나란히 본 성적
- [[environment_v1 · 한계]] — 이 법칙을 깨뜨리는 조건
- [[environment_v1 · 환경]] — 어떤 환경의 종들에서 나왔나
- [[environment_v1 · 데이터]] — 쓰인 종·쌍·유전자군

## 이 법칙을 만든 실험
- (연결된 실행 기록 없음)

## 클러스터
- [[클러스터 · 기생·극한]]
- [[법칙 목록]]
