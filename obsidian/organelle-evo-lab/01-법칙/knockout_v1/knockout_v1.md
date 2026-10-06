---
유형: 법칙 허브
법칙: knockout_v1
클러스터: 실험실 대조
판정: 양성
기준선대비: 1.0246
tags:
  - 법칙/knockout_v1
  - 클러스터/실험실 대조
  - 판정/양성
---

# knockout_v1

> [!abstract] 적용 범위
> Whether genes that laboratory knockouts show to be dispensable are the ones lost in evolution (insect symbionts vs E. coli knockouts; parasites and extremophiles vs family essentiality).

**모형** — Knockout phenotype classes and family essential shares compared with observed retention; Spearman with and without ubiquity; held-out pair AUROC.

## 판정 — 양성

| 비교한 곳 | 법칙 | 기준선 | 차이 | 방향 |
| --- | --- | --- | --- | --- |
| parasites (eukaryote screens) | `partial_controlling_ubiquity` -0.1328 | `heldout_auroc_memorisation_same_families` 0.8372 | +0.9699 | 낮을수록 좋음 |
| extremophiles (bacterial screens) | `partial_controlling_ubiquity` -0.1745 | `heldout_auroc_memorisation_same_families` 0.8502 | +1.0246 | 낮을수록 좋음 |

## 이 클러스터의 노트
- [[knockout_v1 · 계수]] — 학습된 가중치와 신뢰구간
- [[knockout_v1 · 검증]] — 기준선과 나란히 본 성적
- [[knockout_v1 · 한계]] — 이 법칙을 깨뜨리는 조건
- [[knockout_v1 · 환경]] — 어떤 환경의 종들에서 나왔나
- [[knockout_v1 · 데이터]] — 쓰인 종·쌍·유전자군

## 이 법칙을 만든 실험
- (연결된 실행 기록 없음)

## 클러스터
- [[클러스터 · 실험실 대조]]
- [[법칙 목록]]
