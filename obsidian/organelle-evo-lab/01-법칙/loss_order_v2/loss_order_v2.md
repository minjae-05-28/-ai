---
유형: 법칙 허브
법칙: loss_order_v2
클러스터: 소기관
판정: 음성
기준선대비: -0.0471
tags:
  - 법칙/loss_order_v2
  - 클러스터/소기관
  - 판정/음성
---

# loss_order_v2

> [!abstract] 적용 범위
> Order of gene loss in genome reduction: organelles, insect endosymbionts and eukaryotic parasites.

**모형** — Nestedness (containment) against row-fixed and row-and-column-fixed (curveball) nulls.

## 판정 — 음성

| 비교한 곳 | 법칙 | 기준선 | 차이 | 방향 |
| --- | --- | --- | --- | --- |
| results · mitochondrion | `containment` 0.962 | `fixed_null_mean` 0.9642 | -0.0022 | 높을수록 좋음 |
| results · plastid | `containment` 0.9347 | `fixed_null_mean` 0.9426 | -0.0078 | 높을수록 좋음 |
| results · insect_endosymbiont | `containment` 0.9464 | `fixed_null_mean` 0.9499 | -0.0035 | 높을수록 좋음 |
| results · eukaryote_parasites | `containment` 0.4682 | `fixed_null_mean` 0.5153 | -0.0471 | 높을수록 좋음 |

## 이 클러스터의 노트
- [[loss_order_v2 · 계수]] — 학습된 가중치와 신뢰구간
- [[loss_order_v2 · 검증]] — 기준선과 나란히 본 성적
- [[loss_order_v2 · 한계]] — 이 법칙을 깨뜨리는 조건
- [[loss_order_v2 · 환경]] — 어떤 환경의 종들에서 나왔나
- [[loss_order_v2 · 데이터]] — 쓰인 종·쌍·유전자군

## 이 법칙을 만든 실험
- (연결된 실행 기록 없음)

## 클러스터
- [[클러스터 · 소기관]]
- [[법칙 목록]]
