---
유형: 검증
법칙: composite_v1
클러스터: 기생·극한
판정: 무승부
tags:
  - 법칙/composite_v1
  - 클러스터/기생·극한
  - 판정/무승부
  - 유형/검증
---

# composite_v1 · 검증

← [[composite_v1]]

> [!warning] 이 프로젝트의 규칙
> 새 수치는 언제나 기준선(암기·희귀도·평균값)과 나란히 둡니다. 기준선을 못 넘으면 음성 결과로 기록합니다.

| 항목 | 값 | 95% 구간 |
| --- | --- | --- |
| mean_auroc_recover_lost · prior only (no law) | 0.774 | — |
| mean_auroc_recover_lost · axis law | 0.7762 | — |
| mean_auroc_recover_lost · axis + mitochondrion law | 0.7629 | — |
| mean_auroc_recover_lost · axis + plastid law | 0.7754 | — |
| mean_auroc_recover_lost · axis + insect-endosymbiont law | 0.7737 | — |
| mean_auroc_recover_lost · plastid law only | 0.7726 | — |
| mean_auroc_recover_lost · axis law, wrong lifestyle (free-living) | 0.7732 | — |
| best | axis law | — |

## 방법
- [[잎 숨기기 검증]]
- [[알려진 정답 모의]]
- [[부트스트랩 신뢰구간]]
