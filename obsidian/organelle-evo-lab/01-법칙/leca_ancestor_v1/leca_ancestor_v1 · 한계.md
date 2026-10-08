---
유형: 한계
법칙: leca_ancestor_v1
클러스터: 조상 복원
tags:
  - 법칙/leca_ancestor_v1
  - 클러스터/조상 복원
  - 판정/음성
  - 유형/한계
---

# leca_ancestor_v1 · 한계

← [[leca_ancestor_v1]]

### 한계 1
256 eukaryote proteomes reached the tree out of 300 picked with an equal share per supergroup (data/markers/leca_pick.json; pick_eukaryotes.py). UniProt has very few proteomes for Metamonada, Rhizaria, Haptista, Cryptista, CRuMs and Hemimastigophora, so those lineages are thin or absent, and the deepest-branching candidates are exactly the ones least sampled.

### 한계 2
No prokaryote outgroup: at this distance gene-content models cannot place the root, so the tree is rooted on a named split and the root position is treated as unknown. Root positions tested: discoba, opisthokonta. A family is called present in LECA only if P >= 0.9 under every tested root; the 'posterior' column of results/clade_ancestor/leca is the minimum over roots.

### 한계 3
Root positions NOT tested, with the reason: Amorphea (Opisthokonta + Amoebozoa + Apusozoa | rest; the unikont-bikont root): not a split of this marker tree: 15 of 103 amorphean tips (all 9 Amoebozoa, Thecamonas, the Microsporidia) sit outside the largest amorphean-only subtree; Metamonada | rest: only 2 metamonads reached the tree (most metamonad proteomes had too few ribosomal markers) and they do not group together.

### 한계 4
Tips left out because the tree placed them outside their group (long-branch attraction): discoba: none; opisthokonta: Encephalitozoon cuniculi (strain GB-M1) (Microsporidian parasite), Encephalitozoon hellem (Microsporidian parasite), Encephalitozoon intestinalis (strain ATCC 50506) (Microsporidian parasite) (Septata intestinalis), Nematocida ausubeli (Nematode killer fungus), Nematocida displodere.

### 한계 5
Bootstrap trees used per root: discoba 6, opisthokonta 5 of the 9 the time-capped build produced (a bootstrap tree on which the root split does not hold is skipped); the tree_sd of each root run includes them.

### 한계 6
Mitochondrion-encoded families (COX2, COX3, cytochrome b) come out low only because UniProt eukaryote proteomes hold nuclear proteins.

### 한계 7
Completeness is scored once across all sampled eukaryotes (no outgroup): near-universal families among the top-quartile proteomes. Reduced parasites (Microsporidia, Cryptosporidium, Giardia-like lineages) score low and their absences count as weak evidence.

### 한계 8
Present under every root: 3048 families; root-dependent: 452; absent under every root: 9512. Families present per root: {'discoba': 3193, 'opisthokonta': 3767}.

### 한계 9
Known-truth grade with the discoba root: AUROC 0.6196 against 0.5554 for present-day frequency, log loss 0.770 against 1.034, ancestor-size bias +34.3%. Verdict: 계통수가 도움이 됨.

### 한계 10
Known-truth grade with the opisthokonta root: AUROC 0.8227 against 0.6721 for present-day frequency, log loss 0.703 against 0.810, ancestor-size bias -38.0%. Verdict: 계통수가 도움이 됨.

### 한계 11
Read the known-truth grades above as the main limit of this card. The tree beats the no-tree baseline under every root, but the absolute quality is far below the other ancestors in this project (lowest AUROC 0.620; fungi 0.850, plastid 0.995), and the size bias runs in opposite directions under the two roots. So no family count is quoted, and the families are a ranking: the robust-present list (high under every root) and the expected-marker panel are what the data support. Deep eukaryote splits on a FastTree ribosomal tree of ~250 species are the weak link.

### 한계 12
Horizontal transfer is not modelled; measured per root at {'discoba': 0.012, 'opisthokonta': 0.008}. The estimator cannot separate transfer from duplication or domain shuffling, so read it as an upper bound.

### 한계 13
Correction (2026-10-08, pre-registered external benchmark 2): against Vosseberg et al. 2021 gene-tree LECA families this reconstruction does worse than present-day frequency (AUROC 0.872 vs 0.955, -0.083 [-0.091, -0.076]); intermediate-frequency families are under-called. See docs/preregistration/2026-10-08_external_benchmark_phylogenetic_RESULT.md.

