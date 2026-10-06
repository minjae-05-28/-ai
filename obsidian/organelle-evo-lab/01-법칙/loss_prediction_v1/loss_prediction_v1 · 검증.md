---
유형: 검증
법칙: loss_prediction_v1
클러스터: 예측
판정: 양성
tags:
  - 법칙/loss_prediction_v1
  - 클러스터/예측
  - 판정/양성
  - 유형/검증
---

# loss_prediction_v1 · 검증

← [[loss_prediction_v1]]

> [!warning] 이 프로젝트의 규칙
> 새 수치는 언제나 기준선(암기·희귀도·평균값)과 나란히 둡니다. 기준선을 못 넘으면 음성 결과로 기록합니다.

| 항목 | 값 | 95% 구간 |
| --- | --- | --- |
| extremophiles · n_pairs | 54 | — |
| extremophiles · n_lineages | 26 | — |
| extremophiles · pairs_with_relatives | 48 | — |
| extremophiles · pairs_with_other_genera | 39 | — |
| extremophiles · copies.auroc | 0.6173 | [0.6078, 0.6271] |
| extremophiles · copies.fate | 0.6361 | [0.6115, 0.6606] |
| extremophiles · memorisation.auroc | 0.8131 | [0.799, 0.8248] |
| extremophiles · memorisation.fate | 0.764 | [0.745, 0.7825] |
| extremophiles · law.auroc | 0.793 | [0.7708, 0.8134] |
| extremophiles · law.fate | 0.7453 | [0.7204, 0.7692] |
| extremophiles · no_axes_law.auroc | 0.7979 | [0.7801, 0.8141] |
| extremophiles · no_axes_law.fate | 0.7469 | [0.7249, 0.7689] |
| extremophiles · rarity20k.auroc | 0.7878 | [0.7495, 0.8223] |
| extremophiles · rarity20k.fate | 0.7289 | [0.6983, 0.7583] |
| extremophiles · turnover20k.auroc | 0.8192 | [0.8033, 0.8337] |
| extremophiles · turnover20k.fate | 0.7548 | [0.7381, 0.7718] |
| extremophiles · propensity20k.auroc | 0.825 | [0.7996, 0.8458] |
| extremophiles · propensity20k.fate | 0.7598 | [0.7399, 0.7788] |
| extremophiles · relatives.auroc | 0.9238 | [0.9081, 0.9356] |
| extremophiles · relatives.fate | 0.8351 | [0.8096, 0.8583] |
| extremophiles · relatives_other_genera.auroc | 0.8955 | [0.873, 0.9106] |
| extremophiles · relatives_other_genera.fate | 0.8112 | [0.7869, 0.8319] |
| extremophiles · law+propensity20k.auroc | 0.8366 | [0.8131, 0.8564] |
| extremophiles · law+propensity20k.fate | 0.7668 | [0.7448, 0.788] |
| extremophiles · law+relatives.auroc | 0.9246 | [0.9131, 0.9345] |
| extremophiles · law+relatives.fate | 0.8358 | [0.8149, 0.8555] |
| extremophiles · law+relatives_other_genera.auroc | 0.905 | [0.8944, 0.9137] |
| extremophiles · law+relatives_other_genera.fate | 0.8174 | [0.7967, 0.8351] |
| extremophiles · law+propensity20k+relatives.auroc | 0.9093 | [0.8936, 0.9218] |
| extremophiles · law+propensity20k+relatives.fate | 0.8204 | [0.7982, 0.8415] |
| extremophiles · no_change.fate | 0.7202 | [0.6822, 0.7635] |
| extremophiles · no_change.fate (pairs with relatives) | 0.7184 | [0.68, 0.7621] |
| extremophiles · propensity20k - law (auroc) | 0.032 | [0.0175, 0.0444] |
| extremophiles · law+propensity20k - law (auroc) | 0.0436 | [0.0343, 0.0515] |
| extremophiles · law+propensity20k - memorisation (auroc) | 0.0234 | [0.0108, 0.0361] |
| extremophiles · relatives - law (auroc) | 0.1317 | [0.1115, 0.1547] |
| extremophiles · law+relatives - law (auroc) | 0.1325 | [0.1157, 0.1513] |
| extremophiles · law+relatives - memorisation (auroc) | 0.1138 | [0.1046, 0.1229] |
| extremophiles · relatives_other_genera - law (auroc) | 0.104 | [0.0704, 0.1366] |
| extremophiles · law+relatives_other_genera - law (auroc) | 0.1136 | [0.0925, 0.1362] |
| extremophiles · law+relatives_other_genera - memorisation (auroc) | 0.0938 | [0.0826, 0.1026] |
| extremophiles · law+propensity20k+relatives - memorisation (auroc) | 0.0985 | [0.0912, 0.1047] |
| extremophiles · no_change.fate (pairs with other genera) | 0.7067 | [0.6742, 0.7509] |
| extremophiles · law - no_change (fate) | 0.0251 | [-0.0176, 0.0621] |
| extremophiles · law+propensity20k - no_change (fate) | 0.0466 | [0.0032, 0.0833] |
| extremophiles · relatives - no_change (fate) | 0.1166 | [0.0774, 0.1517] |
| extremophiles · law+relatives - no_change (fate) | 0.1174 | [0.0747, 0.1552] |
| extremophiles · relatives_other_genera - no_change (fate) | 0.1044 | [0.0608, 0.1365] |
| extremophiles · law+relatives_other_genera - no_change (fate) | 0.1107 | [0.0677, 0.1419] |
| extremophiles · law+propensity20k+relatives - no_change (fate) | 0.102 | [0.0581, 0.14] |
| extremophiles_consensus · n_pairs | 54 | — |
| extremophiles_consensus · n_lineages | 26 | — |
| extremophiles_consensus · pairs_with_relatives | 48 | — |
| extremophiles_consensus · pairs_with_other_genera | 39 | — |
| extremophiles_consensus · copies.auroc | 0.6054 | [0.5916, 0.6175] |
| extremophiles_consensus · copies.fate | 0.676 | [0.65, 0.7009] |
| extremophiles_consensus · memorisation.auroc | 0.7878 | [0.772, 0.8003] |
| extremophiles_consensus · memorisation.fate | 0.7756 | [0.7564, 0.7937] |
| extremophiles_consensus · law.auroc | 0.7642 | [0.7376, 0.7872] |
| extremophiles_consensus · law.fate | 0.7555 | [0.732, 0.7776] |
| extremophiles_consensus · no_axes_law.auroc | 0.7701 | [0.7498, 0.7882] |
| extremophiles_consensus · no_axes_law.fate | 0.7559 | [0.7345, 0.7764] |
| extremophiles_consensus · rarity20k.auroc | 0.7723 | [0.7325, 0.8071] |
| extremophiles_consensus · rarity20k.fate | 0.7471 | [0.7226, 0.7716] |
| extremophiles_consensus · turnover20k.auroc | 0.7995 | [0.7802, 0.8158] |
| extremophiles_consensus · turnover20k.fate | 0.7651 | [0.7471, 0.7821] |
| extremophiles_consensus · propensity20k.auroc | 0.8076 | [0.7782, 0.83] |
| extremophiles_consensus · propensity20k.fate | 0.7708 | [0.7509, 0.7886] |
| extremophiles_consensus · relatives.auroc | 0.919 | [0.9007, 0.9325] |
| extremophiles_consensus · relatives.fate | 0.8427 | [0.8211, 0.8637] |
| extremophiles_consensus · relatives_other_genera.auroc | 0.8835 | [0.8552, 0.9032] |
| extremophiles_consensus · relatives_other_genera.fate | 0.8203 | [0.7997, 0.8391] |
| extremophiles_consensus · law+propensity20k.auroc | 0.818 | [0.7922, 0.8401] |
| extremophiles_consensus · law+propensity20k.fate | 0.7769 | [0.7551, 0.7971] |
| extremophiles_consensus · law+relatives.auroc | 0.9134 | [0.9006, 0.9253] |
| extremophiles_consensus · law+relatives.fate | 0.8428 | [0.8242, 0.8611] |
| extremophiles_consensus · law+relatives_other_genera.auroc | 0.8897 | [0.8752, 0.9013] |
| extremophiles_consensus · law+relatives_other_genera.fate | 0.8251 | [0.8067, 0.8418] |
| extremophiles_consensus · law+propensity20k+relatives.auroc | 0.8998 | [0.8819, 0.9138] |
| extremophiles_consensus · law+propensity20k+relatives.fate | 0.8295 | [0.8101, 0.8491] |
| extremophiles_consensus · no_change.fate | 0.7772 | [0.7416, 0.8152] |
| extremophiles_consensus · no_change.fate (pairs with relatives) | 0.7772 | [0.741, 0.8182] |
| extremophiles_consensus · propensity20k - law (auroc) | 0.0434 | [0.0223, 0.0622] |
| extremophiles_consensus · law+propensity20k - law (auroc) | 0.0538 | [0.0407, 0.065] |
| extremophiles_consensus · law+propensity20k - memorisation (auroc) | 0.0302 | [0.0174, 0.0436] |
| extremophiles_consensus · relatives - law (auroc) | 0.1561 | [0.131, 0.1863] |
| extremophiles_consensus · law+relatives - law (auroc) | 0.1504 | [0.1322, 0.173] |
| extremophiles_consensus · law+relatives - memorisation (auroc) | 0.1279 | [0.1187, 0.1383] |
| extremophiles_consensus · relatives_other_genera - law (auroc) | 0.1223 | [0.0813, 0.1641] |
| extremophiles_consensus · law+relatives_other_genera - law (auroc) | 0.1285 | [0.1042, 0.1556] |
| extremophiles_consensus · law+relatives_other_genera - memorisation (auroc) | 0.1049 | [0.0932, 0.115] |
| extremophiles_consensus · law+propensity20k+relatives - memorisation (auroc) | 0.1143 | [0.106, 0.1217] |
| extremophiles_consensus · no_change.fate (pairs with other genera) | 0.7718 | [0.7388, 0.8161] |
| extremophiles_consensus · law - no_change (fate) | -0.0217 | [-0.0581, 0.0103] |
| extremophiles_consensus · law+propensity20k - no_change (fate) | -0.0003 | [-0.0381, 0.0314] |
| extremophiles_consensus · relatives - no_change (fate) | 0.0655 | [0.0285, 0.0966] |
| extremophiles_consensus · law+relatives - no_change (fate) | 0.0656 | [0.027, 0.0979] |
| extremophiles_consensus · relatives_other_genera - no_change (fate) | 0.0485 | [0.0065, 0.0786] |
| extremophiles_consensus · law+relatives_other_genera - no_change (fate) | 0.0533 | [0.0122, 0.0841] |
| extremophiles_consensus · law+propensity20k+relatives - no_change (fate) | 0.0523 | [0.0133, 0.0841] |

## 방법
- [[잎 숨기기 검증]]
- [[알려진 정답 모의]]
- [[부트스트랩 신뢰구간]]
