---
유형: 법칙 허브
법칙: plastid_ancestor_v1
클러스터: 조상 복원
판정: 무승부
기준선대비: 0.0066
tags:
  - 법칙/plastid_ancestor_v1
  - 클러스터/조상 복원
  - 판정/무승부
---

# plastid_ancestor_v1

> [!abstract] 적용 범위
> Gene-family (Pfam) content of the common ancestor of the sampled Cyanobacteriia, reconstructed on the GTDB bac120 tree (rooted, pruned to the sampled species; scripts/make_gtdb_subtree.py) from UniProt proteomes. Family presence only; no sequences, no cell shape.

**모형** — Two-state gain/loss Markov chain per family, ensemble of the five leading models of the mitochondrial model search, incomplete proteomes handled as dropout in the likelihood (completeness from in-group marker families, clade and outgroup scored separately), no reduced-lineage loss multiplier, tree rooted on the outgroup; bootstrap trees for phylogenetic spread.

## 판정 — 무승부

| 비교한 곳 | 법칙 | 기준선 | 차이 | 방향 |
| --- | --- | --- | --- | --- |
| leave_tips_out_auroc (auroc) | `reconstruction` 0.9863 | `clade_frequency` 0.9797 | +0.0066 | 높을수록 좋음 |
| known_truth (logloss) | `recon_logloss` 0.0733 | `prior_logloss` 0.6611 | +0.5878 | 낮을수록 좋음 |
| known_truth_subclades · cyano 뿌리 아래 큰 쪽 (159종) (logloss) | `recon_logloss` 0.0335 | `prior_logloss` 0.6573 | +0.6238 | 낮을수록 좋음 |
| core_node · known_truth (logloss) | `recon_logloss` 0.0335 | `prior_logloss` 0.6573 | +0.6238 | 낮을수록 좋음 |

판정은 표의 첫 줄(교차검증 쪽, AUROC 우선)로 매깁니다. 차이가 ±0.01 안이면 무승부. 비교는 같은 지표끼리만 합니다.

## 이 클러스터의 노트
- [[plastid_ancestor_v1 · 계수]] — 학습된 가중치와 신뢰구간
- [[plastid_ancestor_v1 · 검증]] — 기준선과 나란히 본 성적
- [[plastid_ancestor_v1 · 한계]] — 이 법칙을 깨뜨리는 조건
- [[plastid_ancestor_v1 · 환경]] — 어떤 환경의 종들에서 나왔나
- [[plastid_ancestor_v1 · 데이터]] — 쓰인 종·쌍·유전자군

## 이 법칙을 만든 실험
- (연결된 실행 기록 없음)

## 클러스터
- [[클러스터 · 조상 복원]]
- [[법칙 목록]]
