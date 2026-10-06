---
유형: 법칙 허브
법칙: lab_evolution_v1
클러스터: 실험실 대조
판정: 양성
기준선대비: 3.59
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
| LTEE (50,000 generations, 12 populations, selection) | `essential_share_deleted` 0.04356 | `auroc_rarity_baseline` 0.5665 | +0.5229 | 낮을수록 좋음 |
| MAE (mutation accumulation, almost no selection) | `essential_share_deleted` 0.0339 | `auroc_rarity_baseline` 0.5598 | +0.5259 | 낮을수록 좋음 |
| LTEE (50,000 generations, 12 populations, selection), dispensable genes | `deleted_that_are_essential` 0 | `auroc_rarity_baseline` 0.5482 | +0.5482 | 낮을수록 좋음 |
| MAE (mutation accumulation, almost no selection), dispensable genes | `deleted_that_are_essential` 0 | `auroc_rarity_baseline` 0.5345 | +0.5345 | 낮을수록 좋음 |
| genes_lost_per_1000_generations | `max` 7.64 | `mean` 4.05 | +3.5900 | 높을수록 좋음 |

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
