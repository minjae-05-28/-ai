---
유형: 법칙 허브
법칙: anaerobic_transition_v1
클러스터: 전환 경로
판정: 양성
기준선대비: 0.0292
tags:
  - 법칙/anaerobic_transition_v1
  - 클러스터/전환 경로
  - 판정/양성
---

# anaerobic_transition_v1

> [!abstract] 적용 범위
> Whether independent origins of the anaerobic transition change the same gene families (Pfam presence) — eukaryotes, UniProt reference and collected proteomes.

**모형** — Leave-one-origin-out: the share of the other origins that changed each family, scored as a predictor of the held-out origin's changes (AUROC), against baselines.

## 판정 — 양성

| 비교한 곳 | 법칙 | 기준선 | 차이 | 방향 |
| --- | --- | --- | --- | --- |
| leave_one_origin_out (auroc) | `law` 0.7769 | `rarity_baseline` 0.8007 | -0.0238 | 높을수록 좋음 |
| law_plus_rarity_minus_control_plus_rarity (difference) | `법칙 - 대조` 0.0292 | `0` 0 | +0.0292 [0.0118, 0.0459] | 높을수록 좋음 |

판정은 표의 첫 줄(교차검증 쪽, AUROC 우선)로 매깁니다. 차이가 ±0.01 안이면 무승부. 비교는 같은 지표끼리만 합니다.

## 이 클러스터의 노트
- [[anaerobic_transition_v1 · 계수]] — 학습된 가중치와 신뢰구간
- [[anaerobic_transition_v1 · 검증]] — 기준선과 나란히 본 성적
- [[anaerobic_transition_v1 · 한계]] — 이 법칙을 깨뜨리는 조건
- [[anaerobic_transition_v1 · 환경]] — 어떤 환경의 종들에서 나왔나
- [[anaerobic_transition_v1 · 데이터]] — 쓰인 종·쌍·유전자군

## 이 법칙을 만든 실험
- (연결된 실행 기록 없음)

## 클러스터
- [[클러스터 · 전환 경로]]
- [[법칙 목록]]
