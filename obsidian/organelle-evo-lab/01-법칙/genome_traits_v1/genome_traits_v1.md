---
유형: 법칙 허브
법칙: genome_traits_v1
클러스터: 서열·조성
판정: 양성
기준선대비: 6.4358
tags:
  - 법칙/genome_traits_v1
  - 클러스터/서열·조성
  - 판정/양성
---

# genome_traits_v1

> [!abstract] 적용 범위
> Bacterial and archaeal growth temperature, oxygen use and host association predicted from genome-level traits (GC, genome size, coding density, proteins per Mb), across GTDB species with a trait record. Says nothing about gene content or protein sequence.

**모형** — Ridge (temperature) / logistic (oxygen, host) on standardized genome features; gradient boosting on the same features reported next to it; taxonomy memorisation as the baseline.

## 판정 — 양성

| 비교한 곳 | 법칙 | 기준선 | 차이 | 방향 |
| --- | --- | --- | --- | --- |
| temperature · random_5fold · scores | `law_linear` 5.337 | `mean` 5.971 | -0.6344 | 높을수록 좋음 |
| temperature · random_5fold · r2 | `law+taxonomy` 0.7537 | `mean` -0.0002 | +0.7539 | 높을수록 좋음 |
| temperature · leave_order_out | `scores` 5.994 | `law_linear - mean` -0.4419 | +6.4358 | 높을수록 좋음 |
| temperature · leave_order_out · scores | `law_linear` 5.552 | `mean` 5.994 | -0.4419 | 높을수록 좋음 |
| temperature · leave_order_out · r2 | `law+taxonomy` 0.2811 | `mean` -0.0061 | +0.2872 | 높을수록 좋음 |
| oxygen · random_5fold · scores | `law+taxonomy` 0.9782 | `mean` 0.5 | +0.4782 | 높을수록 좋음 |
| oxygen · leave_order_out · scores | `law+taxonomy` 0.8505 | `mean` 0.5 | +0.3505 | 높을수록 좋음 |
| host · random_5fold · scores | `law+taxonomy` 0.8439 | `mean` 0.5 | +0.3439 | 높을수록 좋음 |
| host · leave_order_out · scores | `law_linear` 0.6518 | `mean` 0.5 | +0.1518 | 높을수록 좋음 |

## 이 클러스터의 노트
- [[genome_traits_v1 · 계수]] — 학습된 가중치와 신뢰구간
- [[genome_traits_v1 · 검증]] — 기준선과 나란히 본 성적
- [[genome_traits_v1 · 한계]] — 이 법칙을 깨뜨리는 조건
- [[genome_traits_v1 · 환경]] — 어떤 환경의 종들에서 나왔나
- [[genome_traits_v1 · 데이터]] — 쓰인 종·쌍·유전자군

## 이 법칙을 만든 실험
- (연결된 실행 기록 없음)

## 클러스터
- [[클러스터 · 서열·조성]]
- [[법칙 목록]]
