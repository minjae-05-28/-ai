---
유형: 법칙 허브
법칙: eukaryote_axes_v3
클러스터: 기생·극한
판정: 음성
기준선대비: -0.0818
tags:
  - 법칙/eukaryote_axes_v3
  - 클러스터/기생·극한
  - 판정/음성
---

# eukaryote_axes_v3

> [!abstract] 적용 범위
> Gene-family loss and duplication in eukaryotes (base law + parasite / intracellular / reduced-mitochondria effects), with families described by GO-slim functions, Pfam clans and cross-species statistics.

**모형** — Linear birth-death per family; log rate = a_pair + x @ (design @ W), enriched x.

## 판정 — 음성

| 비교한 곳 | 법칙 | 기준선 | 차이 | 방향 |
| --- | --- | --- | --- | --- |
| mean_heldout_auroc (auroc) | `enriched` 0.7699 | `memorisation` 0.8517 | -0.0818 | 높을수록 좋음 |

판정은 표의 첫 줄(교차검증 쪽, AUROC 우선)로 매깁니다. 차이가 ±0.01 안이면 무승부. 비교는 같은 지표끼리만 합니다.

## 이 클러스터의 노트
- [[eukaryote_axes_v3 · 계수]] — 학습된 가중치와 신뢰구간
- [[eukaryote_axes_v3 · 검증]] — 기준선과 나란히 본 성적
- [[eukaryote_axes_v3 · 한계]] — 이 법칙을 깨뜨리는 조건
- [[eukaryote_axes_v3 · 환경]] — 어떤 환경의 종들에서 나왔나
- [[eukaryote_axes_v3 · 데이터]] — 쓰인 종·쌍·유전자군

## 이 법칙을 만든 실험
- (연결된 실행 기록 없음)

## 클러스터
- [[클러스터 · 기생·극한]]
- [[법칙 목록]]
