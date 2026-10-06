---
유형: 검증
법칙: loss_order_v2
클러스터: 소기관
판정: 음성
tags:
  - 법칙/loss_order_v2
  - 클러스터/소기관
  - 판정/음성
  - 유형/검증
---

# loss_order_v2 · 검증

← [[loss_order_v2]]

> [!warning] 이 프로젝트의 규칙
> 새 수치는 언제나 기준선(암기·희귀도·평균값)과 나란히 둡니다. 기준선을 못 넘으면 음성 결과로 기록합니다.

| 항목 | 값 | 95% 구간 |
| --- | --- | --- |
| n_null | 200 | — |
| results · mitochondrion · lineages | 75 | — |
| results · mitochondrion · genes | 80 | — |
| results · mitochondrion · containment | 0.962 | — |
| results · mitochondrion · row_null_mean | 0.7871 | — |
| results · mitochondrion · row_null_z | 185.1 | — |
| results · mitochondrion · fixed_null_mean | 0.9642 | — |
| results · mitochondrion · fixed_null_z | -4.128 | — |
| results · mitochondrion · fixed_null_p | 1 | — |
| results · plastid · lineages | 54 | — |
| results · plastid · genes | 271 | — |
| results · plastid · containment | 0.9347 | — |
| results · plastid · row_null_mean | 0.8129 | — |
| results · plastid · row_null_z | 211.1 | — |
| results · plastid · fixed_null_mean | 0.9426 | — |
| results · plastid · fixed_null_z | -22.51 | — |
| results · plastid · fixed_null_p | 1 | — |
| results · insect_endosymbiont · lineages | 25 | — |
| results · insect_endosymbiont · genes | 2206 | — |
| results · insect_endosymbiont · containment | 0.9464 | — |
| results · insect_endosymbiont · row_null_mean | 0.828 | — |
| results · insect_endosymbiont · row_null_z | 264 | — |
| results · insect_endosymbiont · fixed_null_mean | 0.9499 | — |
| results · insect_endosymbiont · fixed_null_z | -18.3 | — |
| results · insect_endosymbiont · fixed_null_p | 1 | — |
| results · eukaryote_parasites · lineages | 79 | — |
| results · eukaryote_parasites · genes | 1238 | — |
| results · eukaryote_parasites · containment | 0.4682 | — |
| results · eukaryote_parasites · row_null_mean | 0.2485 | — |
| results · eukaryote_parasites · row_null_z | 164.8 | — |
| results · eukaryote_parasites · fixed_null_mean | 0.5153 | — |
| results · eukaryote_parasites · fixed_null_z | -10.92 | — |
| results · eukaryote_parasites · fixed_null_p | 1 | — |

## 방법
- [[잎 숨기기 검증]]
- [[알려진 정답 모의]]
- [[부트스트랩 신뢰구간]]
