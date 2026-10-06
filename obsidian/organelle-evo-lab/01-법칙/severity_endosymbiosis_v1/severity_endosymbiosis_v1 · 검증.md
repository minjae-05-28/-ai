---
유형: 검증
법칙: severity_endosymbiosis_v1
클러스터: 소기관
판정: 규모 보고
tags:
  - 법칙/severity_endosymbiosis_v1
  - 클러스터/소기관
  - 판정/규모 보고
  - 유형/검증
---

# severity_endosymbiosis_v1 · 검증

← [[severity_endosymbiosis_v1]]

> [!warning] 이 프로젝트의 규칙
> 새 수치는 언제나 기준선(암기·희귀도·평균값)과 나란히 둡니다. 기준선을 못 넘으면 음성 결과로 기록합니다.

| 항목 | 값 | 95% 구간 |
| --- | --- | --- |
| leave_one_lineage_out_rmse_logit · system_only | 1.011 | — |
| leave_one_lineage_out_rmse_logit · with_covariates | 0.9947 | — |
| typical_share_lost · mitochondrion | 0.6949 | — |
| typical_share_lost · plastid | 0.7214 | — |
| typical_share_lost · insect_endosymbiont | 0.8771 | — |
| typical_share_lost · plastid, non-photosynthetic | 0.9239 | — |
| typical_share_lost · mitochondrion, animal | 0.8407 | — |

## 방법
- [[잎 숨기기 검증]]
- [[알려진 정답 모의]]
- [[부트스트랩 신뢰구간]]
