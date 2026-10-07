---
유형: 조상
마디: leca2
표본: 250
신뢰도: 중간
tags:
  - 유형/조상
  - 조상/leca2
  - 클러스터/조상 복원
---

# 모든 진핵생물의 조상 (LECA, 2판)

> [!abstract] 희귀 갈래를 보강하고 제약 계통수로 다시 복원
> 1판보다 메타모나다(4→18종)·리자리아·합토파이트를 늘리고, 큰 갈래의 단계통성을 제약으로 준 IQ-TREE 계통수로 다시 복원했습니다. 그 덕분에 뿌리 위치 네 곳(디스코바·후편모생물·아모르페아·메타모나다)을 모두 시험했고, 네 경우 모두에서 있는 것만 '있었다'로 셉니다. 아래 확률은 네 뿌리 중 가장 작은 값입니다.

## 두 가지 시험

| 시험 | 복원 | 기준선 | 차이 |
| --- | --- | --- | --- |
| 잎 숨기기 (현생 종 맞히기) | 0.9851 | 0.9149 | 0.0702 |
| 알려진 정답 (조상 맞히기) | 0.8057 | 0.7056 | 0.1001 |

로그손실 0.5057 vs 0.9568 · 판정 **계통수가 도움이 됨** · 이 마디의 크기 오차 **8.1%**

## 크기
**4221개 (추정)** · 오늘날 후손 중앙값 4063

> [!warning]
> 뿌리 위치별 크기 discoba 3,951, opisthokonta 4,601, amorphea 4,413, metamonada 3,919; 막대는 그 평균입니다. 알려진 정답 모의의 크기 편향은 가장 나쁜 뿌리에서도 +8.1%로 10% 안쪽입니다.

> [!danger]
> 알려진 정답 채점: 네 뿌리 모두 기준선보다 낫고 AUROC 0.81~0.86, 크기 오차 +4~+8%(조금 크게 나옴)라 크기는 뿌리별 범위로만 말합니다(3,900~4,600개). 음성 대조 일부 실패: 엽록체 유전체의 광계 유전자군이 0.24~0.73으로 나왔습니다. 엽록체는 2차 내공생으로 여러 갈래에 옆으로 퍼졌는데, 보유/소실 모형은 이를 '조상에 있었고 여러 번 잃음'으로 읽습니다. 이 유전자군들은 '모든 뿌리에서 있음' 목록에는 들지 않지만, '지금은 드문데 조상에 있었다'는 목록은 같은 이유로 부풀 수 있습니다. 계통수는 빠른 탐색(-fast)이고 부트스트랩이 없어 계통수 불확실성은 빠져 있습니다.

## 수평 전달
측정값 **0.014** — 크기가 부풀기 시작하는 0.35 아래. [[수평 전달 추정량]]

## 조상에 있었으나 지금은 드문 유전자군

| 유전자군 | 설명 | 조상 | 오늘날 |
| --- | --- | --- | --- |
| `Acetyltransf_4` | Acetyltransferase (GNAT) domain | 0.91 | 7% |
| `GKRP_SIS_2` | Glucokinase regulatory protein, second SIS domain | 1 | 19% |
| `GKRP-like_C` | C-terminal lid domain of glucokinase regulatory protein | 0.99 | 19% |
| `Saposin` | Saposin-like domain | 0.98 | 18% |
| `DUF2418` | Protein of unknown function (DUF2418) | 0.97 | 16% |
| `SAC9_GBDL_1st` | SAC9 first GBDL domain | 0.93 | 14% |
| `VID27_PH` | VID27 PH-like domain | 1 | 22% |
| `GKRP_SIS_N` | Glucokinase regulatory protein N-terminal SIS domain | 1 | 24% |
| `Peptidase_M64` | IgA Peptidase M64 | 0.87 | 11% |
| `DUF1746` | Fungal domain of unknown function (DUF1746) | 0.85 | 10% |
| `DUF2196` | Uncharacterized conserved protein (DUF2196) | 0.89 | 14% |
| `FH3_FHOD1-3` | FHOD1/3 FH3 domain | 0.99 | 25% |

## 방법
- [[2상태 마르코프 모형]]
- [[완전도 관측 모형]]
- [[표본 크기의 한계]]

## 클러스터
- [[클러스터 · 조상 복원]]
- [[조상 목록]]
