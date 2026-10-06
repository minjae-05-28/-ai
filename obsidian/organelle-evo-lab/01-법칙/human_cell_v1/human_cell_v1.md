---
유형: 법칙 허브
법칙: human_cell_v1
클러스터: 실험실 대조
판정: 음성
기준선대비: -0.0657
tags:
  - 법칙/human_cell_v1
  - 클러스터/실험실 대조
  - 판정/음성
---

# human_cell_v1

> [!abstract] 적용 범위
> What the laws predict for a cell living in the human body, tested against real human commensals.

**모형** — Sequence law for composition, severity law for genome size, environment birth-death law for gene content; commensals are never in a training pair.

## 판정 — 음성

| 비교한 곳 | 법칙 | 기준선 | 차이 | 방향 |
| --- | --- | --- | --- | --- |
| gene_content · validation_auroc · Bacteroides thetaiotaomicron | `Bacillus subtilis` 0.8932 | `Bacillus subtilis (rarity baseline)` 0.9371 | -0.0440 | 높을수록 좋음 |
| gene_content · validation_auroc · Bifidobacterium longum | `Bacillus subtilis` 0.8645 | `Pseudomonas putida (rarity baseline)` 0.9144 | -0.0500 | 높을수록 좋음 |
| gene_content · validation_auroc · Akkermansia muciniphila | `Bacillus subtilis` 0.8901 | `Bacillus subtilis (rarity baseline)` 0.9378 | -0.0478 | 높을수록 좋음 |
| gene_content · validation_auroc · Faecalibacterium prausnitzii | `Pseudomonas putida` 0.8595 | `Pseudomonas putida (rarity baseline)` 0.9199 | -0.0604 | 높을수록 좋음 |
| gene_content · validation_auroc · Streptococcus salivarius | `Pseudomonas putida` 0.8644 | `Pseudomonas putida (rarity baseline)` 0.9282 | -0.0638 | 높을수록 좋음 |
| gene_content · validation_auroc · Lactobacillus crispatus | `Bacillus subtilis` 0.8316 | `Pseudomonas putida (rarity baseline)` 0.8974 | -0.0657 | 높을수록 좋음 |

## 이 클러스터의 노트
- [[human_cell_v1 · 계수]] — 학습된 가중치와 신뢰구간
- [[human_cell_v1 · 검증]] — 기준선과 나란히 본 성적
- [[human_cell_v1 · 한계]] — 이 법칙을 깨뜨리는 조건
- [[human_cell_v1 · 환경]] — 어떤 환경의 종들에서 나왔나
- [[human_cell_v1 · 데이터]] — 쓰인 종·쌍·유전자군

## 이 법칙을 만든 실험
- (연결된 실행 기록 없음)

## 클러스터
- [[클러스터 · 실험실 대조]]
- [[법칙 목록]]
