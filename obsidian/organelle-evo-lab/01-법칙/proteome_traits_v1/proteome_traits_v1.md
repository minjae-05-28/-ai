---
유형: 법칙 허브
법칙: proteome_traits_v1
클러스터: 서열·조성
판정: 양성
기준선대비: 0.0935
tags:
  - 법칙/proteome_traits_v1
  - 클러스터/서열·조성
  - 판정/양성
---

# proteome_traits_v1

> [!abstract] 적용 범위
> Bacterial and archaeal growth temperature, oxygen use and host association predicted from proteome amino-acid composition and Pfam family content (UniProt reference proteomes), across species with a trait record.

**모형** — Ridge / logistic regression on standardized composition and Pfam presence; taxonomy memorisation and the mean as baselines; random folds and leave-order-out.

## 판정 — 양성

| 비교한 곳 | 법칙 | 기준선 | 차이 | 방향 |
| --- | --- | --- | --- | --- |
| oxygen · leave_order_out · scores (auroc) | `composition` 0.9232 | `taxonomy` 0.8297 | +0.0935 [0.0386, 0.1837] | 높을수록 좋음 |
| host · leave_order_out · scores (auroc) | `composition` 0.6739 | `mean` 0.5 | +0.1739 | 높을수록 좋음 |
| temperature · leave_order_out · scores (mae) | `composition` 5 | `taxonomy` 5.592 | +0.5921 [-2.181, 0.6987] | 낮을수록 좋음 |
| oxygen · random_5fold · scores (auroc) | `composition` 0.949 | `taxonomy` 0.9698 | -0.0208 | 높을수록 좋음 |
| host · random_5fold · scores (auroc) | `composition` 0.755 | `taxonomy` 0.8476 | -0.0926 | 높을수록 좋음 |
| temperature · random_5fold · scores (mae) | `composition` 4.387 | `taxonomy` 2.576 | -1.8110 | 낮을수록 좋음 |

판정은 표의 첫 줄(교차검증 쪽, AUROC 우선)로 매깁니다. 차이가 ±0.01 안이면 무승부. 비교는 같은 지표끼리만 합니다.

## 이 클러스터의 노트
- [[proteome_traits_v1 · 계수]] — 학습된 가중치와 신뢰구간
- [[proteome_traits_v1 · 검증]] — 기준선과 나란히 본 성적
- [[proteome_traits_v1 · 한계]] — 이 법칙을 깨뜨리는 조건
- [[proteome_traits_v1 · 환경]] — 어떤 환경의 종들에서 나왔나
- [[proteome_traits_v1 · 데이터]] — 쓰인 종·쌍·유전자군

## 이 법칙을 만든 실험
- (연결된 실행 기록 없음)

## 클러스터
- [[클러스터 · 서열·조성]]
- [[법칙 목록]]
