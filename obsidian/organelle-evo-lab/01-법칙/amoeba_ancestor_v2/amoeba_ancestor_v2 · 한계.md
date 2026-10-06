---
유형: 한계
법칙: amoeba_ancestor_v2
클러스터: 조상 복원
tags:
  - 법칙/amoeba_ancestor_v2
  - 클러스터/조상 복원
  - 판정/양성
  - 유형/한계
---

# amoeba_ancestor_v2 · 한계

← [[amoeba_ancestor_v2]]

### 한계 1
Twelve amoebozoan species, eight of them social amoebae. The subsampling experiment (results/sample_size/summary.json) showed that at this size the node reached is NOT the clade's root (Jaccard about 0.91 to it) and the ancestor's size is underestimated by 16-17%, so no family count is quoted and the node is named as the ancestor of the sampled species, not of Amoebozoa.

### 한계 2
Mitochondrion-encoded families (COX2, COX3, cytochrome b, complex I 49 kDa) come out low only because UniProt eukaryote proteomes hold nuclear proteins; the nuclear-encoded respiratory families are high, so the ancestor respired aerobically.

### 한계 3
Flagellar families are low (radial spoke, IFT) but only 1 of the 12 sampled species has them: nearly every sampled lineage is non-flagellate, so this sample cannot resolve whether the true Amoebozoa root was flagellate. The published view is that it was.

### 한계 4
Leave-tips-out AUROC 0.926 against 0.912 for the clade's present-day family frequency: the margin over the no-tree baseline is small, much smaller than in the 2,623-tip bacterial case. This test scores predicting a hidden tip's OBSERVED content, dropout included, which the completeness model deliberately stops reproducing, so it is not the test that speaks to the ancestor; the known-truth simulation (results/quality_correction/summary.json) is.

### 한계 5
Horizontal transfer is not modelled. It was measured for this clade at about 0.056 (results/hgt_rate/summary.json), below the 0.35 at which ancestor size starts to inflate; the estimator cannot separate transfer from an intrinsically high gain rate, so read it as an upper bound.

### 한계 6
Entamoeba proteomes are incomplete (BUSCO 37-53%, completeness score 0.43-0.51). That is modelled as dropout in the likelihood, not as loss. The reduced-lineage loss multiplier is ALSO applied on those branches, so the two corrections overlap; results/clade_ancestor/amoebozoa_v3_nomult holds the run without it.

### 한계 7
Superseded by amoeba_ancestor_v3. The completeness correction was applied to the in-clade tips only, leaving incomplete OUTGROUP proteomes read as real loss; scoring both groups raises leave-tips-out AUROC from 0.926 to 0.931 and the confident family count from 2,045 to 2,693. Switching off the reduced-lineage loss multiplier as well, which the dropout term had made redundant, reaches 0.936. Telomerase's drop to 0.77 recorded here was an artifact of the partial correction: it is 0.909 in v3.

