---
유형: 법칙 허브
법칙: context_features_v1
클러스터: 기생·극한
판정: 양성
기준선대비: 0.0158
tags:
  - 법칙/context_features_v1
  - 클러스터/기생·극한
  - 판정/양성
---

# context_features_v1

> [!abstract] 적용 범위
> Gene-family loss law with context features (codon-usage expression, domain partners, operons, exons) for parasitic eukaryotes and extremophile bacteria/archaea; memorisation kept as a separate score.

**모형** — Linear birth-death law on enriched + context family features; memorisation and a shrunk combination reported side by side, never mixed into the law.

## 판정 — 양성

| 비교한 곳 | 법칙 | 기준선 | 차이 | 방향 |
| --- | --- | --- | --- | --- |
| extremophiles · mean_auroc | `combined_s3` 0.8615 | `memorisation` 0.8492 | +0.0123 | 높을수록 좋음 |
| parasites · mean_auroc | `combined_s10` 0.8041 | `memorisation` 0.7883 | +0.0158 | 높을수록 좋음 |

## 이 클러스터의 노트
- [[context_features_v1 · 계수]] — 학습된 가중치와 신뢰구간
- [[context_features_v1 · 검증]] — 기준선과 나란히 본 성적
- [[context_features_v1 · 한계]] — 이 법칙을 깨뜨리는 조건
- [[context_features_v1 · 환경]] — 어떤 환경의 종들에서 나왔나
- [[context_features_v1 · 데이터]] — 쓰인 종·쌍·유전자군

## 이 법칙을 만든 실험
- (연결된 실행 기록 없음)

## 클러스터
- [[클러스터 · 기생·극한]]
- [[법칙 목록]]
