---
유형: 법칙 허브
법칙: amoeba_ancestor_v3
클러스터: 조상 복원
판정: 양성
기준선대비: 0.024
tags:
  - 법칙/amoeba_ancestor_v3
  - 클러스터/조상 복원
  - 판정/양성
---

# amoeba_ancestor_v3

> [!abstract] 적용 범위
> Gene-family (Pfam) content of the common ancestor of the sampled Amoebozoa (social amoebae, Entamoeba, Acanthamoeba, Planoprotostelium), reconstructed on a ribosomal-marker tree from UniProt proteomes. Family presence only; no sequences, no cell size or shape.

**모형** — Two-state gain/loss Markov chain per family, ensemble of the five leading models of the mitochondrial model search (their differences were inside the interval), with loss accelerated on the reduced Entamoeba branches; 20 bootstrap trees for phylogenetic spread. Incomplete proteomes are handled as dropout in the likelihood (completeness estimated from in-clade marker families) rather than as accelerated loss on their branch.

## 판정 — 양성

| 비교한 곳 | 법칙 | 기준선 | 차이 | 방향 |
| --- | --- | --- | --- | --- |
| leave_tips_out_auroc | `reconstruction` 0.936 | `clade_frequency` 0.912 | +0.0240 | 높을수록 좋음 |

## 이 클러스터의 노트
- [[amoeba_ancestor_v3 · 계수]] — 학습된 가중치와 신뢰구간
- [[amoeba_ancestor_v3 · 검증]] — 기준선과 나란히 본 성적
- [[amoeba_ancestor_v3 · 한계]] — 이 법칙을 깨뜨리는 조건
- [[amoeba_ancestor_v3 · 환경]] — 어떤 환경의 종들에서 나왔나
- [[amoeba_ancestor_v3 · 데이터]] — 쓰인 종·쌍·유전자군

## 이 법칙을 만든 실험
- (연결된 실행 기록 없음)

## 클러스터
- [[클러스터 · 조상 복원]]
- [[법칙 목록]]
