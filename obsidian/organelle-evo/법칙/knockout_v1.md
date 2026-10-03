---
id: knockout_v1
system: 공통
status: 현역
tags:
  - 법칙
  - 공통
---
# knockout_v1

> 실험실 녹아웃·실측 발현과 진화 소실 비교. 극한 세균: 필수 아닌 유전자군 60% vs 대부분 필수 14% 소실(Spearman −0.46, 흔한 정도 빼면 −0.17), 녹아웃만으로 AUROC 0.72. 기생생물 −0.31, 효모 필수 유전자군도 32% 잃음. 조상이 약하게 발현하는 유전자군이 사라짐(실측 RNA 49종, AUROC 0.59–0.64).

**시스템**: 공통  
**상태**: 현역  
**주제**: [[유전자 소실 성향]], [[녹아웃과 발현]]

## 적용 범위 (원문)
Whether genes that laboratory knockouts show to be dispensable are the ones lost in evolution (insect symbionts vs E. coli knockouts; parasites and extremophiles vs family essentiality).

## 모델
Knockout phenotype classes and family essential shares compared with observed retention; Spearman with and without ubiquity; held-out pair AUROC.

## 검증
- symbionts_vs_ecoli_knockouts:
  - essential: `{"n_genes": 352, "share_kept_mean": 0.5920454545454545, "by_symbiont": {"Arsenophonus nasoniae": 0.8778409090909091, "Candidatus Palibaumannia cicadellinicola":`
  - costly in rich medium: `{"n_genes": 50, "share_kept_mean": 0.3512, "by_symbiont": {"Arsenophonus nasoniae": 0.82, "Candidatus Palibaumannia cicadellinicola": 0.5, "Candidatus Blochmann`
  - needed only in minimal medium: `{"n_genes": 676, "share_kept_mean": 0.20142011834319526, "by_symbiont": {"Arsenophonus nasoniae": 0.5340236686390533, "Candidatus Palibaumannia cicadellinicola"`
  - dispensable: `{"n_genes": 2249, "share_kept_mean": 0.076016007114273, "by_symbiont": {"Arsenophonus nasoniae": 0.2810137839039573, "Candidatus Palibaumannia cicadellinicola":`
  - auroc_essential_predicts_retention: 0.874
  - n_matched_genes: 3327
- families_with_knockout_data:
  - eukaryote_screens: 8186
  - bacterial_screens: 10573
- parasites (eukaryote screens):
  - n_families: 7189
  - spearman_essential_vs_loss: -0.295
  - partial_controlling_ubiquity: -0.133
  - groups: `{"never essential": {"n_families": 4522, "mean_loss_rate": 0.4634944677018225}, "sometimes essential (≤50%)": {"n_families": 1678, "mean_loss_rate": 0.286613767`
  - heldout_auroc_knockout_only: 0.641
  - heldout_auroc_memorisation_same_families: 0.837
  - n_pairs: 90
- extremophiles (bacterial screens):
  - n_families: 7715
  - spearman_essential_vs_loss: -0.464
  - partial_controlling_ubiquity: -0.174
  - groups: `{"never essential": {"n_families": 3439, "mean_loss_rate": 0.6020218682092239}, "sometimes essential (≤50%)": {"n_families": 3437, "mean_loss_rate": 0.366554029`
  - heldout_auroc_knockout_only: 0.72
  - heldout_auroc_memorisation_same_families: 0.85
  - n_pairs: 57
- abundance_proxy_check:
  - Saccharomyces cerevisiae: `{"n_families": 4530, "spearman_codon_proxy_vs_measured": 0.6864519944066301}`
  - Caenorhabditis elegans: `{"n_families": 5054, "spearman_codon_proxy_vs_measured": 0.7293645130181093}`
  - Dictyostelium discoideum: `{"n_families": 4284, "spearman_codon_proxy_vs_measured": 0.15639119738115423}`
  - Synechocystis sp. PCC 6803: `{"n_families": 1474, "spearman_codon_proxy_vs_measured": 0.3719643977802302}`
  - Drosophila melanogaster: `{"n_families": 6290, "spearman_codon_proxy_vs_measured": 0.40082179289036446}`
  - Macrostomum lignano: `{"n_families": 2048, "spearman_codon_proxy_vs_measured": 0.27713572178081364}`
  - Chlamydomonas reinhardtii: `{"n_families": 4150, "spearman_codon_proxy_vs_measured": 0.49417425063921355}`
- measured_rna:
  - n_relatives_with_rna: 51
  - codon_proxy_vs_rna_spearman: `[0.2581962597265621, 0.07231285054085326, 0.37467379603096107, 0.43423390220133434, 0.33228976188649695, 0.5508534578590172, 0.1912835344120802, 0.5324837390666`
  - parasites: `{"n_pairs": 78, "auroc_low_rna_predicts_loss": 0.5842293369314946, "auroc_low_codon_proxy_predicts_loss": 0.5736129513262872, "partial_spearman_rna_vs_loss_cont`
  - extremophiles: `{"n_pairs": 36, "auroc_low_rna_predicts_loss": 0.636585209599741, "auroc_low_codon_proxy_predicts_loss": 0.623053513913076, "partial_spearman_rna_vs_loss_contro`

## 한계
- Essentiality is measured in lab media, not in the host.
- Fitness Browser 'likely essential' = no transposon mutants recovered.
- Families are matched by Pfam domains, not orthology.

원본: `laws/knockout_v1.json`