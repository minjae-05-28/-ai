---
유형: 한계
법칙: plastid_ancestor_v1
클러스터: 조상 복원
tags:
  - 법칙/plastid_ancestor_v1
  - 클러스터/조상 복원
  - 판정/양성
  - 유형/한계
---

# plastid_ancestor_v1 · 한계

← [[plastid_ancestor_v1]]

### 한계 1
162 Cyanobacteriia proteomes: GTDB species representatives matched to UniProt by species name, ambiguous names ('Synechococcus sp.') skipped, so many marine picocyanobacteria and most uncultured lineages are missing. The non-photosynthetic sister classes (Vampirovibrionia, Sericytochromatia) did not match and are absent; the outgroup is 150 random other bacteria.

### 한계 2
The tree is the GTDB bac120 tree (rooted, pruned to the sampled species; scripts/make_gtdb_subtree.py); it was rooted again on the outgroup tip farthest from the clade (Prevotella jejuni). The clade is monophyletic, so the node reconstructed is the common ancestor of every sampled member.

### 한계 3
No bootstrap trees were used (n_bootstrap_trees = 0), so the tree_sd column is zero and phylogenetic uncertainty is NOT in the reported spread.

### 한계 4
Leave-tips-out AUROC 0.986 against 0.980 for present-day frequency. That test scores a hidden tip's observed content, dropout included, which the completeness model deliberately does not reproduce; the known-truth grade below is the test that speaks to the ancestor.

### 한계 5
Completeness is estimated from families nearly every top-quartile proteome carries. Reduced genomes (Microsporidia; Atelocyanobacterium among cyanobacteria) really lack many of those, so they are scored as incomplete: their absences count as weak evidence. That keeps them from dragging the ancestor down, but it is a choice, not a measurement of their assembly quality.

### 한계 6
The clade node splits into 3 tips (Gloeobacter kilaueensis (strain ATCC BAA-2537 / CCAP 1431/1 / ULC 316 / JS1), Gloeobacter morelensis MG652769, Gloeobacter violaceus (strain ATCC 29082 / PCC 7421)) and everything else. Families those few lack, and the outgroup mostly lacks too, come out low at the clade node: never there and lost on that one short side look alike from this sample, so read low values there as 'not shown to be present', not as proven absence. The larger child node (validation.core_node) is reported beside it.

### 한계 7
Extra node g__Gloeomargarita (that lineage): 1 sampled tips below, 1979 families at P>=0.9. A single sampled tip: this is its own proteome (with dropout), listed only for comparison.

### 한계 8
Extra node ^g__Gloeomargarita (the node where that lineage split off): 159 sampled tips below, 1910 families at P>=0.9. On this tree it is the same node as validation.core_node, so the known-truth grade there applies to it.

### 한계 9
Known-truth grade at this node (simulated families on the same tree, results/node_power/cyano): AUROC 0.9954 against 0.9756 for present-day frequency, log loss 0.073 against 0.179, ancestor-size bias -3.4% (frequency -6.3%). Verdict: 계통수가 도움이 됨.

### 한계 10
Horizontal transfer is not modelled; measured for this tree at about 0.004. That is far below the 0.35 at which ancestor size starts to inflate. The estimator cannot separate transfer from an intrinsically high gain rate (gene duplication, domain shuffling), so it is an upper bound.

