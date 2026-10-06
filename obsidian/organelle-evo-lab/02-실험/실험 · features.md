---
유형: 실험
실행: features
산출: results/features/metrics.json
tags:
  - 유형/실험
  - 실험/features
---

# 실험 · features

**산출물** `results/features/metrics.json`

## n_features

```json
{
 "base": 8,
 "enriched": 56
}
```

## feature_names

```json
[
 "hydrophobicity_gravy",
 "tm_helices",
 "protein_length",
 "redox_core",
 "atp_synthase",
 "translation",
 "transcription",
 "protein_targeting",
 "ubiquity_free_living",
 "copies_free_living",
 "hmm_length",
 "clan_size",
 "in_clan",
 "has_go_annotation",
 "go:DNA binding",
 "go:RNA binding",
 "go:catalytic activity",
 "go:structural molecule activity",
 "go:transporter activity",
 "go:nucleus",
 "go:mitochondrion",
 "go:ribosome",
 "go:carbohydrate metabolic process",
 "go:DNA-templated transcription",
 "go:regulation of DNA-templated transcription",
 "go:lipid metabolic process",
 "go:oxidoreductase activity",
 "go:transferase activity",
 "go:hydrolase activity",
 "go:lyase activity",
 "go:isomerase activity",
 "go:ligase activity",
 "go:signaling",
 "go:organelle",
 "go:transmembrane transport",
 "go:nucleobase-containing small molecule metabolic process",
 "go:molecular function regulator activity",
 "go:catalytic activity, acting on a protein",
 "go:catalytic activity, acting on RNA",
 "go:carbohydrate derivative metabolic process",
 "kw:kinase",
 "kw:phosphatase",
 "kw:transporter_channel",
 "kw:zinc_finger",
 "kw:repeat_domain",
 "kw:ubiquitin_system",
 "kw:protease",
 "kw:helicase_nucleic",
 "kw:gtpase_signalling",
 "kw:methyl_glyco_transferase",
 "kw:cytoskeleton_motor",
 "kw:cilium_flagellum",
 "kw:cell_adhesion_surface",
 "kw:lipid_metabolism",
 "kw:amino_acid_metabolism",
 "kw:uncharacterised"
]
```

## mean_heldout_auroc

```json
{
 "copies_only": 0.6466693047031259,
 "base": 0.67057666758796,
 "enriched": 0.769860430012379,
 "memorisation": 0.8516556973408791
}
```

## heldout

```json
[
 {
  "pair": "Chromera velia -> Plasmodium falciparum",
  "copies_only": 0.624691069050213,
  "memorisation": 0.9448367074152495,
  "base": 0.6674359220303379,
  "enriched": 0.8092974436575324
 },
 {
  "pair": "Coprinopsis cinerea -> Ustilago maydis",
  "copies_only": 0.5771335042578518,
  "memorisation": 0.7754909719587862,
  "base": 0.5896290894345102,
  "enriched": 0.7076912763090769
 },
 {
  "pair": "Spizellomyces punctatus -> Encephalitozoon intestinalis",
  "copies_only": 0.6854698940477216,
  "memorisation": 0.9458492333534326,
  "base": 0.7084613231113791,
  "enriched": 0.8408082091480747
 },
 {
  "pair": "Chromera velia -> Theileria parva",
  "copies_only": 0.6076658641801806,
  "memorisation": 0.9424179691796307,
  "base": 0.6675332706008872,
  "enriched": 0.8219450317124736
 },
 {
  "pair": "Chromera velia -> Neospora caninum",
  "copies_only": 0.6402126539997026,
  "memorisation": 0.9294701132029303,
  "base": 0.6819284137315687,
  "enriched": 0.8199451218693379
 },
 {
  "pair": "Chromera velia -> Hammondia hammondi",
  "copies_only": 0.6259803786879641,
  "memorisation": 0.9351870084749903,
  "base": 0.6676207136576788,
  "enriched": 0.8123608363455777
 },
 {
  "pair": "Thalassiosira pseudonana -> Phytophthora infestans",
  "copies_only": 0.611587689524816,
  "memorisation": 0.8667917462704768,
  "base": 0.6386849111824723,
  "enriched": 0.7548178935815617
 },
 {
  "pair": "Caenorhabditis elegans -> Brugia malayi",
  "copies_only": 0.6088821757907794,
  "memorisation": 0.8268944598757242,
  "base": 0.6427589948634479,
  "enriched": 0.7088171580104068
 },
 {
 
… (잘림 — 원본 파일 참조)
```

## significant_loss_effects

```json
{
 "base": [
  [
   "go:ligase activity",
   -0.4181332896428694,
   0.06937946946370828
  ],
  [
   "ubiquity_free_living",
   -0.3898159552835325,
   0.020769427870173628
  ],
  [
   "copies_free_living",
   0.3554355079959326,
   0.017987160938131002
  ],
  [
   "transcription",
   -0.35023590762999884,
   0.07567327698887324
  ],
  [
   "kw:gtpase_signalling",
   -0.31912036062649324,
   0.016835187142015814
  ],
  [
   "go:DNA-templated transcription",
   -0.2964930781486783,
   0.040377639552412685
  ],
  [
   "translation",
   -0.2822083146743135,
   0.05044623230768332
  ],
  [
   "go:carbohydrate metabolic process",
   0.24722290945122383,
   0.049912569996669875
  ],
  [
   "go:nucleus",
   -0.24483378185990834,
   0.08879717945674553
  ],
  [
   "kw:helicase_nucleic",
   0.2248011862067602,
   0.06878979361537937
  ],
  [
   "in_clan",
   0.2051584512951919,
   0.011964983760817376
  ],
  [
   "go:oxidoreductase activity",
   0.20365843323512753,
   0.06803401748186431
  ]
 ],
 "parasite": [
  [
   "go:mitochondrion",
   -0.30605091761797837,
   0.09275820386087337
  ],
  [
   "kw:cell_adhesion_surface",
   -0.3037860861615432,
   0.05840752523530052
  ],
  [
   "go:ribosome",
   0.2579275683874966,
   0.0887804675763376
  ],
  [
   "go:DNA-templated transcription",
   0.2560919349049485,
   0.03809321178299638
  ],
  [
   "go:organelle",
   0.21582762235482036,
   0.014325073143185438
  ],
  [
   "go:ligase activity",
   0.1759084693935091,
   0.06266231081807752
  ],
  [
   "kw:helicase_nucleic",
   -0.17343760629532698,
   0.08580872224877907
  ],
  [
   "in_c
… (잘림 — 원본 파일 참조)
```

## 연결
- [[실험 목록]]
