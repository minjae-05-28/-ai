---
유형: 검증
법칙: proteome_traits_v1
클러스터: 서열·조성
판정: 양성
tags:
  - 법칙/proteome_traits_v1
  - 클러스터/서열·조성
  - 판정/양성
  - 유형/검증
---

# proteome_traits_v1 · 검증

← [[proteome_traits_v1]]

> [!warning] 이 프로젝트의 규칙
> 새 수치는 언제나 기준선(암기·희귀도·평균값)과 나란히 둡니다. 기준선을 못 넘으면 음성 결과로 기록합니다.

| 항목 | 값 | 95% 구간 |
| --- | --- | --- |
| temperature · random_5fold · n | 7253 | — |
| temperature · random_5fold · n_orders | 180 | — |
| temperature · random_5fold · metric | MAE (deg C) | — |
| temperature · random_5fold · scores | 6.151 | [—, —] |
| temperature · leave_order_out · n | 7253 | — |
| temperature · leave_order_out · n_orders | 180 | — |
| temperature · leave_order_out · metric | MAE (deg C) | — |
| temperature · leave_order_out · scores | 6.199 | [—, —] |
| temperature · leave_order_out · composition - taxonomy | -0.5921 | [-2.181, 0.6987] |
| temperature · leave_order_out · pfam - taxonomy | -1.94 | [-3.757, -0.683] |
| temperature · leave_order_out · composition+pfam - taxonomy | -2.125 | [-4.051, -0.8447] |
| temperature · leave_order_out · composition+pfam - composition | -1.533 | [-2.24, -0.91] |
| temperature · composition_coefficients · ivywrel | 5.645 | — |
| temperature · composition_coefficients · cvp | 1.643 | — |
| temperature · composition_coefficients · acidic_excess | 0.5287 | — |
| temperature · composition_coefficients · n_side | -1.724 | — |
| temperature · composition_coefficients · gravy | 0.3352 | — |
| temperature · composition_coefficients · fymink | 0.4681 | — |
| temperature · composition_coefficients · median_pi | 3.229 | — |
| oxygen · random_5fold · n | 5363 | — |
| oxygen · random_5fold · n_orders | 177 | — |
| oxygen · random_5fold · metric | AUROC | — |
| oxygen · random_5fold · scores | 0.5 | [—, —] |
| oxygen · leave_order_out · n | 5363 | — |
| oxygen · leave_order_out · n_orders | 177 | — |
| oxygen · leave_order_out · metric | AUROC | — |
| oxygen · leave_order_out · scores | 0.5 | [—, —] |
| oxygen · leave_order_out · composition - taxonomy | 0.0936 | [0.0386, 0.1837] |
| oxygen · leave_order_out · pfam - taxonomy | 0.1479 | [0.0729, 0.2804] |
| oxygen · leave_order_out · composition+pfam - taxonomy | 0.1477 | [0.0715, 0.2792] |
| oxygen · leave_order_out · composition+pfam - composition | 0.0541 | [0.0239, 0.1101] |
| oxygen · composition_coefficients · ivywrel | -0.0498 | — |
| oxygen · composition_coefficients · cvp | -1.54 | — |
| oxygen · composition_coefficients · acidic_excess | 0.8501 | — |
| oxygen · composition_coefficients · n_side | 0.2958 | — |
| oxygen · composition_coefficients · gravy | -0.1422 | — |
| oxygen · composition_coefficients · fymink | -1.599 | — |
| oxygen · composition_coefficients · median_pi | 0.6366 | — |
| host · random_5fold · n | 5851 | — |
| host · random_5fold · n_orders | 180 | — |
| host · random_5fold · metric | AUROC | — |
| host · random_5fold · scores | 0.5 | [—, —] |
| host · leave_order_out · n | 5851 | — |
| host · leave_order_out · n_orders | 180 | — |
| host · leave_order_out · metric | AUROC | — |
| host · leave_order_out · scores | 0.5 | [—, —] |
| host · leave_order_out · composition - taxonomy | 0.1891 | [0.0986, 0.2571] |
| host · leave_order_out · pfam - taxonomy | 0.3556 | [0.2569, 0.4335] |
| host · leave_order_out · composition+pfam - taxonomy | 0.3582 | [0.2592, 0.4363] |
| host · leave_order_out · composition+pfam - composition | 0.1691 | [0.0958, 0.237] |
| host · composition_coefficients · ivywrel | -0.5374 | — |
| host · composition_coefficients · cvp | -0.0257 | — |
| host · composition_coefficients · acidic_excess | -0.6257 | — |
| host · composition_coefficients · n_side | 0.4517 | — |
| host · composition_coefficients · gravy | 0.2499 | — |
| host · composition_coefficients · fymink | 1.127 | — |
| host · composition_coefficients · median_pi | -0.7037 | — |

## 방법
- [[잎 숨기기 검증]]
- [[알려진 정답 모의]]
- [[부트스트랩 신뢰구간]]
