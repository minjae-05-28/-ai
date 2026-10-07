---
유형: 법칙 허브
법칙: leca_ancestor_v2
클러스터: 조상 복원
판정: 양성
기준선대비: 0.1001
tags:
  - 법칙/leca_ancestor_v2
  - 클러스터/조상 복원
  - 판정/양성
---

# leca_ancestor_v2

> [!abstract] 적용 범위
> Gene-family (Pfam) content of the last eukaryotic common ancestor (LECA), reconstructed on a ribosomal-marker tree of supergroup-balanced UniProt proteomes under several root positions; reported as what holds under every root. Family presence only; no sequences.

**모형** — Two-state gain/loss Markov chain per family, ensemble of the five leading models of the mitochondrial model search, incomplete proteomes as dropout in the likelihood, no reduced-lineage multiplier; one run per root position (rooted on the named split), combined by minimum.

## 판정 — 양성

| 비교한 곳 | 법칙 | 기준선 | 차이 | 방향 |
| --- | --- | --- | --- | --- |
| leave_tips_out_auroc_per_root · discoba (auroc) | `reconstruction` 0.9851 | `clade_frequency` 0.9149 | +0.0702 | 높을수록 좋음 |
| leave_tips_out_auroc_per_root · opisthokonta (auroc) | `reconstruction` 0.9794 | `clade_frequency` 0.9184 | +0.0610 | 높을수록 좋음 |
| leave_tips_out_auroc_per_root · amorphea (auroc) | `reconstruction` 0.9846 | `clade_frequency` 0.9099 | +0.0747 | 높을수록 좋음 |
| leave_tips_out_auroc_per_root · metamonada (auroc) | `reconstruction` 0.9835 | `clade_frequency` 0.93 | +0.0535 | 높을수록 좋음 |
| known_truth_per_root · discoba (auroc) | `recon_auroc` 0.8057 | `freq_auroc` 0.7056 | +0.1001 | 높을수록 좋음 |
| known_truth_per_root · opisthokonta (auroc) | `recon_auroc` 0.863 | `freq_auroc` 0.7404 | +0.1226 | 높을수록 좋음 |
| known_truth_per_root · amorphea (auroc) | `recon_auroc` 0.8509 | `freq_auroc` 0.7335 | +0.1174 | 높을수록 좋음 |
| known_truth_per_root · metamonada (auroc) | `recon_auroc` 0.8247 | `freq_auroc` 0.7205 | +0.1042 | 높을수록 좋음 |
| known_truth_per_root · discoba (logloss) | `recon_logloss` 0.5057 | `prior_logloss` 0.6929 | +0.1872 | 낮을수록 좋음 |
| known_truth_per_root · opisthokonta (logloss) | `recon_logloss` 0.4554 | `prior_logloss` 0.6929 | +0.2375 | 낮을수록 좋음 |
| known_truth_per_root · amorphea (logloss) | `recon_logloss` 0.5017 | `prior_logloss` 0.6929 | +0.1912 | 낮을수록 좋음 |
| known_truth_per_root · metamonada (logloss) | `recon_logloss` 0.5007 | `prior_logloss` 0.6929 | +0.1922 | 낮을수록 좋음 |

판정은 표의 첫 줄(교차검증 쪽, AUROC 우선)로 매깁니다. 차이가 ±0.01 안이면 무승부. 비교는 같은 지표끼리만 합니다.

## 이 클러스터의 노트
- [[leca_ancestor_v2 · 계수]] — 학습된 가중치와 신뢰구간
- [[leca_ancestor_v2 · 검증]] — 기준선과 나란히 본 성적
- [[leca_ancestor_v2 · 한계]] — 이 법칙을 깨뜨리는 조건
- [[leca_ancestor_v2 · 환경]] — 어떤 환경의 종들에서 나왔나
- [[leca_ancestor_v2 · 데이터]] — 쓰인 종·쌍·유전자군

## 이 법칙을 만든 실험
- (연결된 실행 기록 없음)

## 클러스터
- [[클러스터 · 조상 복원]]
- [[법칙 목록]]
