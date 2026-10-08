---
유형: 한계
법칙: leca_ancestor_v2
클러스터: 조상 복원
tags:
  - 법칙/leca_ancestor_v2
  - 클러스터/조상 복원
  - 판정/음성
  - 유형/한계
---

# leca_ancestor_v2 · 한계

← [[leca_ancestor_v2]]

### 한계 1
250 eukaryote proteomes reached the tree out of 300 picked with an equal share per supergroup (data/markers/leca2_pick.json; pick_eukaryotes.py). UniProt has very few proteomes for Metamonada, Rhizaria, Haptista, Cryptista, CRuMs and Hemimastigophora, so those lineages are thin or absent, and the deepest-branching candidates are exactly the ones least sampled.

### 한계 2
No prokaryote outgroup: at this distance gene-content models cannot place the root, so the tree is rooted on a named split and the root position is treated as unknown. Root positions tested: discoba, opisthokonta, amorphea, metamonada. A family is called present in LECA only if P >= 0.9 under every tested root; the 'posterior' column of results/clade_ancestor/leca2 is the minimum over roots.

### 한계 3
Root positions NOT tested, with the reason: none.

### 한계 4
Tips left out because the tree placed them outside their group (long-branch attraction): discoba: none; opisthokonta: none; amorphea: none; metamonada: none.

### 한계 5
No bootstrap trees: phylogenetic uncertainty is NOT in the reported spread (tree_sd is zero).

### 한계 6
Mitochondrion-encoded families (COX2, COX3, cytochrome b) come out low only because UniProt eukaryote proteomes hold nuclear proteins.

### 한계 7
Completeness is scored once across all sampled eukaryotes (no outgroup): near-universal families among the top-quartile proteomes. Reduced parasites (Microsporidia, Cryptosporidium, Giardia-like lineages) score low and their absences count as weak evidence.

### 한계 8
Present under every root: 2849 families; root-dependent: 683; absent under every root: 8844. Families present per root: {'discoba': 3153, 'opisthokonta': 4085, 'amorphea': 3969, 'metamonada': 3058}.

### 한계 9
Known-truth grade with the discoba root: AUROC 0.8057 against 0.7056 for present-day frequency, log loss 0.506 against 0.957, ancestor-size bias +8.1%. Verdict: 계통수가 도움이 됨.

### 한계 10
Known-truth grade with the opisthokonta root: AUROC 0.8630 against 0.7404 for present-day frequency, log loss 0.455 against 0.904, ancestor-size bias +4.3%. Verdict: 계통수가 도움이 됨.

### 한계 11
Known-truth grade with the amorphea root: AUROC 0.8509 against 0.7335 for present-day frequency, log loss 0.502 against 0.905, ancestor-size bias +4.0%. Verdict: 계통수가 도움이 됨.

### 한계 12
Known-truth grade with the metamonada root: AUROC 0.8247 against 0.7205 for present-day frequency, log loss 0.501 against 0.935, ancestor-size bias +6.4%. Verdict: 계통수가 도움이 됨.

### 한계 13
Negative control partly FAILED: Photo_RC 0.24-0.53, PSII 0.23-0.53, PsaA_PsaB 0.50-0.73 across roots, though the plastid came after LECA. These are plastid-encoded photosystem families; plastids spread between eukaryote groups by secondary and tertiary endosymbiosis (red algae into Sar, haptophytes, cryptophytes), i.e. sideways, and the gain/loss model reads a family scattered over many groups as present at the root and lost many times. None of them is in the present-under-every-root list (P >= 0.9 under all roots), but the same effect can lift any family spread by endosymbiosis or transfer, so families that are rare today and high at the root need that caution. The transfer estimator below does not catch it.

### 한계 14
Known-truth quality: lowest AUROC over roots 0.806 (fungi 0.850, plastid 0.995 in this project), size bias within 10% under every root and of the same sign. The tree beats the no-tree baseline under every root. Tree: IQ-TREE LG+F+G4 with -fast on the ribosomal concatenate after dropping columns with more than 50% gaps (131,149 columns before trimming), constrained to the uncontested supergroups (Amorphea with Opisthokonta and Amoebozoa inside, Sar with Stramenopiles, Alveolata and Rhizaria inside, Viridiplantae, Rhodophyta, Glaucophyta, Discoba, Metamonada, Haptista, Cryptophyta); no bootstrap (IQ-TREE refuses ultrafast bootstrap with -fast; the full searches did not finish inside the CI time limit).

### 한계 15
Horizontal transfer is not modelled; measured per root at {'discoba': 0.014, 'opisthokonta': 0.013, 'amorphea': 0.013, 'metamonada': 0.014}. The estimator cannot separate transfer from duplication or domain shuffling, so read it as an upper bound.

### 한계 16
Ancestor size (sum of posteriors) per root: {'discoba': 3951.3, 'opisthokonta': 4601.3, 'amorphea': 4413.1, 'metamonada': 3918.8}; the known-truth bias is within 10% under every root (an overestimate of a few percent), so the range across roots is quoted, not one number.

### 한계 17
Correction (2026-10-08, pre-registered external benchmark 2, docs/preregistration/2026-10-08_external_benchmark_phylogenetic_RESULT.md): against Vosseberg et al. 2021 gene-tree LECA families (5,489 shared Pfams, 3,858 LECA) this reconstruction does WORSE than present-day frequency (AUROC 0.866 vs 0.954, difference -0.088 [-0.096, -0.080]; negative under every root). Families present in 20-50% of species today are 78% LECA by their trees but average P 0.29 here: the model underestimates massive loss and overestimates late gains. Within the shared Pfams our LECA size is 15-26% smaller than theirs (2,866-3,278 vs 3,858), so the size range quoted above (3,919-4,601) is likely an UNDERestimate; the known-truth bias (+4-8%) was measured on data simulated from the same model and cannot see this.

