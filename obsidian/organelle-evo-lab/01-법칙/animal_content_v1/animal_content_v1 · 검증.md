---
유형: 검증
법칙: animal_content_v1
클러스터: 동물
판정: 양성
tags:
  - 법칙/animal_content_v1
  - 클러스터/동물
  - 판정/양성
  - 유형/검증
---

# animal_content_v1 · 검증

← [[animal_content_v1]]

> [!warning] 이 프로젝트의 규칙
> 새 수치는 언제나 기준선(암기·희귀도·평균값)과 나란히 둡니다. 기준선을 못 넘으면 음성 결과로 기록합니다.

| 항목 | 값 | 95% 구간 |
| --- | --- | --- |
| leave_one_origin_out_auroc · all · copies_only | 0.6755 | [0.6488, 0.6962] |
| leave_one_origin_out_auroc · all · rarity | 0.8361 | [0.8077, 0.8588] |
| leave_one_origin_out_auroc · all · memorisation | 0.7763 | [0.7484, 0.8074] |
| leave_one_origin_out_auroc · all · no_axes | 0.8009 | [0.7717, 0.8237] |
| leave_one_origin_out_auroc · all · axis_law | 0.7943 | [0.7558, 0.8219] |
| leave_one_origin_out_auroc · all · axis_law - no_axes | -0.0066 | [-0.0175, 0.0008] |
| leave_one_origin_out_auroc · all · axis_law - memorisation | 0.0181 | [-0.032, 0.0589] |
| leave_one_origin_out_auroc · all · axis_law - rarity | -0.0418 | [-0.0842, -0.0077] |
| leave_one_origin_out_auroc · all · axes_better_in | 9 | — |
| leave_one_origin_out_auroc · close_proxies_only · copies_only | 0.6776 | [0.6473, 0.6987] |
| leave_one_origin_out_auroc · close_proxies_only · rarity | 0.8324 | [0.8037, 0.857] |
| leave_one_origin_out_auroc · close_proxies_only · memorisation | 0.7681 | [0.7439, 0.7968] |
| leave_one_origin_out_auroc · close_proxies_only · no_axes | 0.8007 | [0.7671, 0.8272] |
| leave_one_origin_out_auroc · close_proxies_only · axis_law | 0.7924 | [0.7477, 0.8241] |
| leave_one_origin_out_auroc · close_proxies_only · axis_law - no_axes | -0.0083 | [-0.0198, -0.0013] |
| leave_one_origin_out_auroc · close_proxies_only · axis_law - memorisation | 0.0242 | [-0.0299, 0.0643] |
| leave_one_origin_out_auroc · close_proxies_only · axis_law - rarity | -0.0401 | [-0.088, -0.0048] |
| leave_one_origin_out_auroc · close_proxies_only · axes_better_in | 7 | — |

## 방법
- [[잎 숨기기 검증]]
- [[알려진 정답 모의]]
- [[부트스트랩 신뢰구간]]
