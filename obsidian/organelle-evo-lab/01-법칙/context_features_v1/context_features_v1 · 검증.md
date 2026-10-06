---
유형: 검증
법칙: context_features_v1
클러스터: 기생·극한
판정: 음성
tags:
  - 법칙/context_features_v1
  - 클러스터/기생·극한
  - 판정/음성
  - 유형/검증
---

# context_features_v1 · 검증

← [[context_features_v1]]

> [!warning] 이 프로젝트의 규칙
> 새 수치는 언제나 기준선(암기·희귀도·평균값)과 나란히 둡니다. 기준선을 못 넘으면 음성 결과로 기록합니다.

| 항목 | 값 | 95% 구간 |
| --- | --- | --- |
| extremophiles · mean_auroc · copies_only | 0.6173 | — |
| extremophiles · mean_auroc · memorisation | 0.8492 | — |
| extremophiles · mean_auroc · law_base | 0.8133 | — |
| extremophiles · mean_auroc · law_context | 0.8179 | — |
| extremophiles · mean_auroc · combined_s1 | 0.8597 | — |
| extremophiles · mean_auroc · combined_s3 | 0.8615 | — |
| extremophiles · mean_auroc · combined_s10 | 0.8607 | — |
| extremophiles · context_gain | 0.004605 | [—, —] |
| extremophiles · context_weights · ctx:expression | -0.3241 | — |
| extremophiles · context_weights · ctx:multi_domain | 0.0152 | — |
| extremophiles · context_weights · ctx:partners | 0.0052 | — |
| extremophiles · context_weights · ctx:operon | -0.0959 | — |
| extremophiles · context_weights · ctx:neighbourhood | -0.112 | — |
| extremophiles · context_weights · ctx:has_context | 0.0247 | — |
| parasites · mean_auroc · copies_only | 0.6467 | — |
| parasites · mean_auroc · memorisation | 0.7883 | — |
| parasites · mean_auroc · law_base | 0.7598 | — |
| parasites · mean_auroc · law_context | 0.7654 | — |
| parasites · mean_auroc · combined_s1 | 0.7931 | — |
| parasites · mean_auroc · combined_s3 | 0.7984 | — |
| parasites · mean_auroc · combined_s10 | 0.8041 | — |
| parasites · context_gain | 0.005607 | [—, —] |
| parasites · context_weights · ctx:expression | -0.0447 | — |
| parasites · context_weights · ctx:multi_domain | 0.0078 | — |
| parasites · context_weights · ctx:partners | -0.0078 | — |
| parasites · context_weights · ctx:exons | -0.127 | — |
| parasites · context_weights · ctx:has_context | 0.075 | — |

## 방법
- [[잎 숨기기 검증]]
- [[알려진 정답 모의]]
- [[부트스트랩 신뢰구간]]
