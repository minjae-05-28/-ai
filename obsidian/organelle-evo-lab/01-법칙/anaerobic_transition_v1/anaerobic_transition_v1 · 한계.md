---
유형: 한계
법칙: anaerobic_transition_v1
클러스터: 전환 경로
tags:
  - 법칙/anaerobic_transition_v1
  - 클러스터/전환 경로
  - 판정/양성
  - 유형/한계
---

# anaerobic_transition_v1 · 한계

← [[anaerobic_transition_v1]]

### 한계 1
Leave-one-origin-out AUROC: law 0.7769 against parasite_baseline 0.6839, rarity_baseline 0.8007. Law minus the better baseline per origin: -0.0238 [-0.0574, 0.0101] — the law is not separated from the better baseline (interval holds zero).

### 한계 2
Added to rarity, the law gains 0.0213 [0.0078, 0.0347] AUROC; against the control signature added to rarity the same way: 0.0436 [0.0261, 0.0606]; with the law built from as many origins as there are control pairs: 0.0292 [0.0118, 0.0459].

### 한계 3
6 independent origins; the interval is a bootstrap over origins, so it is wide and would narrow only with more origins, not more species per origin.

### 한계 4
Pairs are curated from taxonomy (scripts/transition_catalog.py); the relative stands in for the ancestor, so changes on the relative's own branch are counted as the transition's.

### 한계 5
Presence comes from UniProt Pfam cross-references with no completeness model: an incomplete proteome reads as losses. Reduced genomes (Microsporidia, Giardia, Cryptosporidium) are both incomplete-looking and genuinely reduced, which this design cannot separate.

### 한계 6
Panel limits: ATP-synt_C and Fe_hyd_lg_C are Pfam families shared with the vacuolar ATPase and with the cytosolic Fe-S assembly protein NAR1, so aerobes carry them too; they are not markers of mitochondrial ATP synthase or of hydrogenase. The respiratory chain (COX15, COX17, Cytochrom_C1, Rieske, UCR_14kD) is lost in every anaerobic origin where it was a candidate and in no aerobic parasite pair.

### 한계 7
Parasitism-matched origins (both sides parasites): Microsporidia: law 0.7868 vs parasite 0.7067 vs rarity 0.8526; Cryptosporidium: law 0.7656 vs parasite 0.7106 vs rarity 0.8177. These are the only comparisons where oxygen is not confounded with parasitism.

### 한계 8
Metamonada's aerobic relatives are in another supergroup (Discoba), so its losses mix the anaerobic transition with a deep split.

