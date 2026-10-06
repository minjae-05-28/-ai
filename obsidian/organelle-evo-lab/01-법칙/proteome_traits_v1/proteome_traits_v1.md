---
유형: 법칙 허브
법칙: proteome_traits_v1
클러스터: 서열·조성
판정: 음성
기준선대비: -1.7639
tags:
  - 법칙/proteome_traits_v1
  - 클러스터/서열·조성
  - 판정/음성
---

# proteome_traits_v1

> [!abstract] 적용 범위
> Bacterial and archaeal growth temperature, oxygen use and host association predicted from proteome amino-acid composition and Pfam family content (UniProt reference proteomes), across species with a trait record.

**모형** — Ridge / logistic regression on standardized composition and Pfam presence; taxonomy memorisation and the mean as baselines; random folds and leave-order-out.

## 판정 — 음성

| 비교한 곳 | 법칙 | 기준선 | 차이 | 방향 |
| --- | --- | --- | --- | --- |
| temperature · random_5fold · scores | `composition` 4.387 | `mean` 6.151 | -1.7639 | 높을수록 좋음 |
| temperature · leave_order_out · scores | `taxonomy` 5.592 | `mean` 6.199 | -0.6071 | 높을수록 좋음 |
| oxygen · random_5fold · scores | `composition+pfam` 0.9845 | `mean` 0.5 | +0.4845 | 높을수록 좋음 |
| oxygen · leave_order_out · scores | `pfam` 0.9776 | `mean` 0.5 | +0.4776 | 높을수록 좋음 |
| host · random_5fold · scores | `composition+pfam` 0.8925 | `mean` 0.5 | +0.3925 | 높을수록 좋음 |
| host · leave_order_out · scores | `composition+pfam` 0.8431 | `mean` 0.5 | +0.3431 | 높을수록 좋음 |

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
