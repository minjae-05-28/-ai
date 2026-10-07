---
유형: 법칙 허브
법칙: fungal_ancestor_v1
클러스터: 조상 복원
판정: 양성
기준선대비: 0.1046
tags:
  - 법칙/fungal_ancestor_v1
  - 클러스터/조상 복원
  - 판정/양성
---

# fungal_ancestor_v1

> [!abstract] 적용 범위
> Gene-family (Pfam) content of the common ancestor of the sampled Fungi, reconstructed on a ribosomal-marker tree from UniProt proteomes. Family presence only; no sequences, no cell shape.

**모형** — Two-state gain/loss Markov chain per family, ensemble of the five leading models of the mitochondrial model search, incomplete proteomes handled as dropout in the likelihood (completeness from in-group marker families, clade and outgroup scored separately), no reduced-lineage loss multiplier, tree rooted on the outgroup; bootstrap trees for phylogenetic spread.

## 판정 — 양성

| 비교한 곳 | 법칙 | 기준선 | 차이 | 방향 |
| --- | --- | --- | --- | --- |
| leave_tips_out_auroc (auroc) | `reconstruction` 0.9721 | `clade_frequency` 0.95 | +0.0221 | 높을수록 좋음 |
| known_truth (auroc) | `recon_auroc` 0.8499 | `freq_auroc` 0.7453 | +0.1046 | 높을수록 좋음 |
| known_truth_subclades · fungi 뿌리 아래 큰 쪽 (286종) (auroc) | `recon_auroc` 0.8904 | `freq_auroc` 0.8098 | +0.0806 | 높을수록 좋음 |
| known_truth_subclades · Ascomycota (auroc) | `recon_auroc` 0.8317 | `freq_auroc` 0.7678 | +0.0639 | 높을수록 좋음 |
| known_truth_subclades · Basidiomycota (auroc) | `recon_auroc` 0.8475 | `freq_auroc` 0.8143 | +0.0332 | 높을수록 좋음 |
| known_truth_subclades · Chytridiomycota (auroc) | `recon_auroc` 0.8862 | `freq_auroc` 0.7933 | +0.0929 | 높을수록 좋음 |
| known_truth_subclades · Glomeromycota (auroc) | `recon_auroc` 0.8737 | `freq_auroc` 0.8448 | +0.0289 | 높을수록 좋음 |
| known_truth_subclades · Kickxellomycota (auroc) | `recon_auroc` 0.8893 | `freq_auroc` 0.8441 | +0.0452 | 높을수록 좋음 |
| known_truth_subclades · Mucoromycota (auroc) | `recon_auroc` 0.8904 | `freq_auroc` 0.7936 | +0.0968 | 높을수록 좋음 |
| core_node · known_truth (auroc) | `recon_auroc` 0.8904 | `freq_auroc` 0.8098 | +0.0806 | 높을수록 좋음 |
| known_truth (logloss) | `recon_logloss` 0.4524 | `prior_logloss` 0.6668 | +0.2144 | 낮을수록 좋음 |
| known_truth_subclades · fungi 뿌리 아래 큰 쪽 (286종) (logloss) | `recon_logloss` 0.3382 | `freq_logloss` 0.5427 | +0.2045 | 낮을수록 좋음 |
| known_truth_subclades · Ascomycota (logloss) | `recon_logloss` 0.3282 | `freq_logloss` 0.4425 | +0.1143 | 낮을수록 좋음 |
| known_truth_subclades · Basidiomycota (logloss) | `recon_logloss` 0.3105 | `freq_logloss` 0.3956 | +0.0851 | 낮을수록 좋음 |
| known_truth_subclades · Chytridiomycota (logloss) | `recon_logloss` 0.31 | `freq_logloss` 0.5653 | +0.2553 | 낮을수록 좋음 |
| known_truth_subclades · Glomeromycota (logloss) | `recon_logloss` 0.2948 | `freq_logloss` 0.5214 | +0.2266 | 낮을수록 좋음 |
| known_truth_subclades · Kickxellomycota (logloss) | `recon_logloss` 0.2659 | `freq_logloss` 0.4496 | +0.1837 | 낮을수록 좋음 |
| known_truth_subclades · Mucoromycota (logloss) | `recon_logloss` 0.2753 | `prior_logloss` 0.5088 | +0.2335 | 낮을수록 좋음 |
| core_node · known_truth (logloss) | `recon_logloss` 0.3382 | `freq_logloss` 0.5427 | +0.2045 | 낮을수록 좋음 |

판정은 표의 첫 줄(교차검증 쪽, AUROC 우선)로 매깁니다. 차이가 ±0.01 안이면 무승부. 비교는 같은 지표끼리만 합니다.

## 이 클러스터의 노트
- [[fungal_ancestor_v1 · 계수]] — 학습된 가중치와 신뢰구간
- [[fungal_ancestor_v1 · 검증]] — 기준선과 나란히 본 성적
- [[fungal_ancestor_v1 · 한계]] — 이 법칙을 깨뜨리는 조건
- [[fungal_ancestor_v1 · 환경]] — 어떤 환경의 종들에서 나왔나
- [[fungal_ancestor_v1 · 데이터]] — 쓰인 종·쌍·유전자군

## 이 법칙을 만든 실험
- (연결된 실행 기록 없음)

## 클러스터
- [[클러스터 · 조상 복원]]
- [[법칙 목록]]
