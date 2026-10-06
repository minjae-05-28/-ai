---
유형: 한계
법칙: amoeba_ancestor_v3
클러스터: 조상 복원
tags:
  - 법칙/amoeba_ancestor_v3
  - 클러스터/조상 복원
  - 판정/양성
  - 유형/한계
---

# amoeba_ancestor_v3 · 한계

← [[amoeba_ancestor_v3]]

### 한계 1
Twelve amoebozoan species, eight of them social amoebae. The subsampling experiment (results/sample_size/summary.json) showed that at this size the node reached is NOT the clade's root (Jaccard about 0.91 to it) and the ancestor's size is underestimated by 16-17%, so no family count is quoted and the node is named as the ancestor of the sampled species, not of Amoebozoa.

### 한계 2
Mitochondrion-encoded families (COX2, COX3, cytochrome b, complex I 49 kDa) come out low only because UniProt eukaryote proteomes hold nuclear proteins; the nuclear-encoded respiratory families are high, so the ancestor respired aerobically.

### 한계 3
Flagellar families are low (radial spoke, IFT) but only 1 of the 12 sampled species has them: nearly every sampled lineage is non-flagellate, so this sample cannot resolve whether the true Amoebozoa root was flagellate. The published view is that it was.

### 한계 4
Leave-tips-out AUROC 0.936 against 0.912 for the clade's present-day family frequency: the margin over the no-tree baseline is small, much smaller than in the 2,623-tip bacterial case. This test scores predicting a hidden tip's OBSERVED content, dropout included, which the completeness model deliberately stops reproducing, so it is not the test that speaks to the ancestor; the known-truth simulation (results/quality_correction/summary.json) is.

### 한계 5
Horizontal transfer is not modelled. It was measured for this clade at about 0.056 (results/hgt_rate/summary.json), below the 0.35 at which ancestor size starts to inflate; the estimator cannot separate transfer from an intrinsically high gain rate, so read it as an upper bound.

### 한계 6
Entamoeba proteomes are incomplete (BUSCO 37-53%, completeness score 0.43-0.51). That is modelled as dropout in the likelihood, not as loss. The reduced-lineage loss multiplier is switched off here, so incompleteness is corrected once.

### 한계 7
Superseded by amoeba_ancestor_v4, which fixes a reproducibility fault rather than a modelling one: the marker families were ordered by iterating sets of strings, so Python's per-process hash seed moved the completeness scores by about 0.02 between identical runs. v4 breaks ties by name. It also requires a clade member's kingdom to match (a virus named after an amoeba genus would otherwise have counted), keeps the richest profile when an organism appears in several shards, and stops dropping tips with few families now that incompleteness is modelled. AUROC 0.936 to 0.934, confident families 2,706 to 2,697.

