---
유형: 법칙 허브
법칙: mito_ancestor_v1
클러스터: 소기관
판정: 무승부
기준선대비: 0.0069
tags:
  - 법칙/mito_ancestor_v1
  - 클러스터/소기관
  - 판정/무승부
---

# mito_ancestor_v1

> [!abstract] 적용 범위
> Gene-family (Pfam) content of the alphaproteobacterial ancestors from which mitochondria are thought to descend, reconstructed on the GTDB tree from UniProt reference proteomes. Candidate ancestors: the alphaproteobacterial common ancestor and deep orders (Rickettsiales, Holosporales, Pelagibacterales). Family presence only; no sequences.

**모형** — Two-state gain/loss Markov chain per Pfam family on the pruned GTDB bac120 tree, rates by grid maximum likelihood, marginal posteriors by the up-down algorithm. Variants: symmetric vs loss-biased (gain <= 0.1 x loss, flat root prior) x all proteomes vs BUSCO >= 90%.

## 판정 — 무승부

| 비교한 곳 | 법칙 | 기준선 | 차이 | 방향 |
| --- | --- | --- | --- | --- |
| loss_biased_busco0 · leave_tips_out_auroc (auroc) | `reconstruction` 0.9846 | `nearest_tip` 0.9777 | +0.0069 | 높을수록 좋음 |
| loss_biased_busco90 · leave_tips_out_auroc (auroc) | `reconstruction` 0.9849 | `nearest_tip` 0.9792 | +0.0057 | 높을수록 좋음 |
| symmetric_busco0 · leave_tips_out_auroc (auroc) | `reconstruction` 0.9847 | `nearest_tip` 0.9777 | +0.0070 | 높을수록 좋음 |
| symmetric_busco90 · leave_tips_out_auroc (auroc) | `reconstruction` 0.9852 | `nearest_tip` 0.9792 | +0.0060 | 높을수록 좋음 |

판정은 표의 첫 줄(교차검증 쪽, AUROC 우선)로 매깁니다. 차이가 ±0.01 안이면 무승부. 비교는 같은 지표끼리만 합니다.

## 이 클러스터의 노트
- [[mito_ancestor_v1 · 계수]] — 학습된 가중치와 신뢰구간
- [[mito_ancestor_v1 · 검증]] — 기준선과 나란히 본 성적
- [[mito_ancestor_v1 · 한계]] — 이 법칙을 깨뜨리는 조건
- [[mito_ancestor_v1 · 환경]] — 어떤 환경의 종들에서 나왔나
- [[mito_ancestor_v1 · 데이터]] — 쓰인 종·쌍·유전자군

## 이 법칙을 만든 실험
- (연결된 실행 기록 없음)

## 클러스터
- [[클러스터 · 소기관]]
- [[법칙 목록]]
