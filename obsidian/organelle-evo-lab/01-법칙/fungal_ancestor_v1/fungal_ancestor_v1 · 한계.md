---
유형: 한계
법칙: fungal_ancestor_v1
클러스터: 조상 복원
tags:
  - 법칙/fungal_ancestor_v1
  - 클러스터/조상 복원
  - 판정/양성
  - 유형/한계
---

# fungal_ancestor_v1 · 한계

← [[fungal_ancestor_v1]]

### 한계 1
289 Fungi proteomes, chosen round-robin over orders (data/markers/<set>_pick.json) so early-diverging lineages are not swamped. UniProt reference proteomes still over-represent Dikarya, and lineages without a reference proteome (for example Aphelida, most Nucleariida) are absent.

### 한계 2
The tree is a FastTree marker tree, unrooted as written; it was rooted on the outgroup tip farthest from the clade (Leishmania enriettii). With the tips listed next left out, the clade is monophyletic and the node reconstructed is the common ancestor of every remaining member. Left out because the tree placed them outside the clade (long-branch attraction): Astathelohania contejeani, Hamiltosporidium tvaerminnensis.

### 한계 3
No bootstrap trees were used (n_bootstrap_trees = 0), so the tree_sd column is zero and phylogenetic uncertainty is NOT in the reported spread.

### 한계 4
Leave-tips-out AUROC 0.972 against 0.950 for present-day frequency. That test scores a hidden tip's observed content, dropout included, which the completeness model deliberately does not reproduce; the known-truth grade below is the test that speaks to the ancestor.

### 한계 5
Mitochondrion-encoded families come out low only because UniProt eukaryote proteomes hold nuclear proteins.

### 한계 6
Completeness is estimated from families nearly every top-quartile proteome carries. Microsporidia and other reduced genomes really lack many of those, so they are scored as incomplete: their absences count as weak evidence. That keeps them from dragging the ancestor down, but it is a choice, not a measurement of their assembly quality.

### 한계 7
The clade node splits into 3 reduced lineages (Mitosporidium daphniae, Paramicrosporidium saccamoebae, Rozella allomycis (strain CSF55)) and everything else. Families those few lineages lack, and the outgroup mostly lacks too, sit near the prior (about 0.1) at the clade node: absent from the start and lost in the parasites look the same from this sample, so read ~0.1 there as undecided, not absent. The larger child node (validation.core_node) is reported beside it.

### 한계 8
Known-truth grade at this node (simulated families on the same tree, results/node_power/fungi): AUROC 0.8499 against 0.7453 for present-day frequency, log loss 0.452 against 0.724, ancestor-size bias -5.7% (frequency -55.1%). Verdict: 계통수가 도움이 됨.

### 한계 9
Horizontal transfer is not modelled; measured for this tree at about 0.014, which only says 'below 0.02': the calibration curve saturates at 0.02 on this tree. That is far below the 0.35 at which ancestor size starts to inflate. The estimator cannot separate transfer from an intrinsically high gain rate (gene duplication, domain shuffling), so it is an upper bound.

