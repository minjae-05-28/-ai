---
유형: 법칙 허브
법칙: genome_traits_v1
클러스터: 서열·조성
판정: 무승부
기준선대비: 0.0331
tags:
  - 법칙/genome_traits_v1
  - 클러스터/서열·조성
  - 판정/무승부
---

# genome_traits_v1

> [!abstract] 적용 범위
> Bacterial and archaeal growth temperature, oxygen use and host association predicted from genome-level traits (GC, genome size, coding density, proteins per Mb), across GTDB species with a trait record. Says nothing about gene content or protein sequence.

**모형** — Ridge (temperature) / logistic (oxygen, host) on standardized genome features; gradient boosting on the same features reported next to it; taxonomy memorisation as the baseline.

## 판정 — 무승부

| 비교한 곳 | 법칙 | 기준선 | 차이 | 방향 |
| --- | --- | --- | --- | --- |
| oxygen · leave_order_out · scores (auroc) | `law_linear` 0.7883 | `taxonomy` 0.7552 | +0.0331 [-0.1108, 0.179] | 높을수록 좋음 |
| host · leave_order_out · scores (auroc) | `law_nonlinear` 0.6797 | `taxonomy` 0.5021 | +0.1776 | 높을수록 좋음 |
| temperature · leave_order_out · scores (mae) | `law_nonlinear` 5.177 | `taxonomy` 4.703 | -0.4745 | 낮을수록 좋음 |
| temperature · leave_order_out · r2 (r2) | `law_nonlinear` 0.2123 | `taxonomy` 0.2738 | -0.0615 | 높을수록 좋음 |
| oxygen · random_5fold · scores (auroc) | `law_nonlinear` 0.8807 | `taxonomy` 0.9681 | -0.0874 | 높을수록 좋음 |
| host · random_5fold · scores (auroc) | `law_nonlinear` 0.7631 | `taxonomy` 0.8434 | -0.0803 | 높을수록 좋음 |
| temperature · random_5fold · scores (mae) | `law_nonlinear` 4.201 | `taxonomy` 2.591 | -1.6103 | 낮을수록 좋음 |
| temperature · random_5fold · r2 (r2) | `law_nonlinear` 0.4548 | `taxonomy` 0.7527 | -0.2979 | 높을수록 좋음 |

판정은 표의 첫 줄(교차검증 쪽, AUROC 우선)로 매깁니다. 차이가 ±0.01 안이면 무승부. 비교는 같은 지표끼리만 합니다.

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
