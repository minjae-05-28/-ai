---
유형: 법칙 허브
법칙: lab_evolution_v1
클러스터: 실험실 대조
판정: 양성
기준선대비: 0.0232
tags:
  - 법칙/lab_evolution_v1
  - 클러스터/실험실 대조
  - 판정/양성
---

# lab_evolution_v1

> [!abstract] 적용 범위
> Whether the comparative loss law, fitted to genomes that diverged over millions of years, predicts which genes are deleted in 50,000 generations of experimental evolution in E. coli (LTEE), with mutation accumulation as the no-selection control.

**모형** — Per gene: mean comparative loss rate of its Pfam families across the project's prokaryote pairs, scored against whether the gene falls inside a deletion in a sequenced clone. Rarity, expression proxy and lab essentiality as baselines.

## 판정 — 양성

| 비교한 곳 | 법칙 | 기준선 | 차이 | 방향 |
| --- | --- | --- | --- | --- |
| LTEE (50,000 generations, 12 populations, selection) (auroc) | `auroc_comparative_loss_rate` 0.5897 | `auroc_rarity_baseline` 0.5665 | +0.0232 | 높을수록 좋음 |
| MAE (mutation accumulation, almost no selection) (auroc) | `auroc_low_expression` 0.6012 | `auroc_rarity_baseline` 0.5598 | +0.0415 | 높을수록 좋음 |
| LTEE (50,000 generations, 12 populations, selection), dispensable genes (auroc) | `auroc_comparative_loss_rate` 0.5646 | `auroc_rarity_baseline` 0.5482 | +0.0163 | 높을수록 좋음 |
| MAE (mutation accumulation, almost no selection), dispensable genes (auroc) | `auroc_low_expression` 0.5798 | `auroc_rarity_baseline` 0.5345 | +0.0452 | 높을수록 좋음 |

판정은 표의 첫 줄(교차검증 쪽, AUROC 우선)로 매깁니다. 차이가 ±0.01 안이면 무승부. 비교는 같은 지표끼리만 합니다.

## 이 클러스터의 노트
- [[lab_evolution_v1 · 계수]] — 학습된 가중치와 신뢰구간
- [[lab_evolution_v1 · 검증]] — 기준선과 나란히 본 성적
- [[lab_evolution_v1 · 한계]] — 이 법칙을 깨뜨리는 조건
- [[lab_evolution_v1 · 환경]] — 어떤 환경의 종들에서 나왔나
- [[lab_evolution_v1 · 데이터]] — 쓰인 종·쌍·유전자군

## 이 법칙을 만든 실험
- (연결된 실행 기록 없음)

## 클러스터
- [[클러스터 · 실험실 대조]]
- [[법칙 목록]]
