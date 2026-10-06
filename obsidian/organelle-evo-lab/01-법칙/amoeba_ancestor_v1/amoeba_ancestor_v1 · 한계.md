---
유형: 한계
법칙: amoeba_ancestor_v1
클러스터: 조상 복원
tags:
  - 법칙/amoeba_ancestor_v1
  - 클러스터/조상 복원
  - 판정/양성
  - 유형/한계
---

# amoeba_ancestor_v1 · 한계

← [[amoeba_ancestor_v1]]

### 한계 1
Twelve amoebozoan species, eight of them social amoebae. The subsampling experiment (results/sample_size/summary.json) showed that at this size the node reached is NOT the clade's root (Jaccard about 0.91 to it) and the ancestor's size is underestimated by 16-17%, so no family count is quoted and the node is named as the ancestor of the sampled species, not of Amoebozoa.

### 한계 2
Mitochondrion-encoded families (COX2, COX3, cytochrome b, complex I 49 kDa) come out low only because UniProt eukaryote proteomes hold nuclear proteins; the nuclear-encoded respiratory families are high, so the ancestor respired aerobically.

### 한계 3
Flagellar families are low (radial spoke, IFT) but only 1 of the 12 sampled species has them: nearly every sampled lineage is non-flagellate, so this sample cannot resolve whether the true Amoebozoa root was flagellate. The published view is that it was.

### 한계 4
Leave-tips-out AUROC 0.931 against 0.912 for the clade's present-day family frequency: the margin over the no-tree baseline is small, much smaller than in the 2,623-tip bacterial case.

### 한계 5
Horizontal transfer is not modelled. It was measured for this clade at about 0.056 (results/hgt_rate/summary.json), below the 0.35 at which ancestor size starts to inflate; the estimator cannot separate transfer from an intrinsically high gain rate, so read it as an upper bound.

### 한계 6
Entamoeba proteomes are incomplete (BUSCO 37-53%), which is why loss is accelerated on their branches; that is a modelling assumption, not a measurement. amoeba_ancestor_v2 replaces it with a dropout term fitted from the data.

### 한계 7
Superseded for the quality question by amoeba_ancestor_v2, which models incomplete proteomes as dropout in the likelihood (the Entamoeba tips score 0.43-0.51, every other tip 0.95-1.00). Known-truth simulation prefers that model (results/quality_correction/summary.json). The conclusions here hold - the marker panel moves by at most 0.11 - but 13.4% of families move by more than 0.1 and telomerase drops from 0.88 to 0.77, out of the confident set.

### 한계 8
amoeba_ancestor_v3 is the current reconstruction of this node: completeness modelled as dropout for every tip and no reduced-lineage loss multiplier, leave-tips-out AUROC 0.936 against 0.912. The readings here hold there - pseudopodia, phagocytosis, nuclear-encoded respiration and sex all stay high, the flagellum stays unresolved, the mitochondrion-encoded families stay low - but peroxisome import goes 0.957 to 0.999 and catalase 0.757 to 0.878, so the peroxisome is no longer the weak call it is called here.

