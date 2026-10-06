---
유형: 검증
법칙: environment_v1
클러스터: 기생·극한
판정: 무승부
tags:
  - 법칙/environment_v1
  - 클러스터/기생·극한
  - 판정/무승부
  - 유형/검증
---

# environment_v1 · 검증

← [[environment_v1]]

> [!warning] 이 프로젝트의 규칙
> 새 수치는 언제나 기준선(암기·희귀도·평균값)과 나란히 둡니다. 기준선을 못 넘으면 음성 결과로 기록합니다.

| 항목 | 값 | 95% 구간 |
| --- | --- | --- |
| leave_one_pair_out_auroc · copies_only | 0.6143 | — |
| leave_one_pair_out_auroc · no_environment | 0.8157 | — |
| leave_one_pair_out_auroc · environment_law | 0.808 | — |
| leave_one_pair_out_auroc · memorisation | 0.8042 | — |
| env_vs_none | -0.00766 | — |

## 방법
- [[잎 숨기기 검증]]
- [[알려진 정답 모의]]
- [[부트스트랩 신뢰구간]]
