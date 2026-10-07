---
유형: 실험
실행: clade_ancestor/leca2
산출: results/clade_ancestor/leca2/summary.json
tags:
  - 유형/실험
  - 실험/clade_ancestor-leca2
---

# 실험 · clade_ancestor-leca2

**산출물** `results/clade_ancestor/leca2/summary.json`

## 한눈에

| 항목 | 값 |
| --- | --- |
| clade | leca2 |
| tips | 250 |
| clade_tips | 250 |
| families_considered | 14335 |
| rooted_on | split: Discoba | rest / split: Opisthokonta | rest / split: Opisthokonta+Amoebozoa+Apusozoa+Breviatea | rest / split: Metamonada | rest |
| n_bootstrap_trees | 0 |
| n_confident_families | 2849 |
| n_uncertain_families | 683 |
| n_robust_absent | 8844 |
| rule | present = posterior >= 0.9 under every root; absent = < 0.1 under every root; root-dependent = >= 0.9 under one root and < 0.1 or far lower under another (spread >= 0.5) |

## roots

```json
[
 "discoba",
 "opisthokonta",
 "amorphea",
 "metamonada"
]
```

## clade_species

```json
[
 "Blattamonas nauphoetae",
 "Paratrimastix pyriformis",
 "Anaeramoeba ignava (Anaerobic marine amoeba)",
 "Tritrichomonas foetus",
 "Tritrichomonas musculus",
 "Carpediemonas membranifera",
 "Aduncisulcus paluster",
 "Kipferlia bialata",
 "Giardia muris",
 "Hexamita inflata",
 "Spironucleus salmonicida",
 "Reticulomyxa filosa",
 "Bonamia ostreae",
 "Plasmodiophora brassicae (Clubroot disease agent)",
 "Ichthyophthirius multifiliis (White spot disease agent) (Ich)",
 "Pseudocohnilembus persalinus (Ciliate)",
 "Paramecium tetraurelia",
 "Paramecium pentaurelia",
 "Paramecium sonneborni",
 "Euplotes crassus",
 "Stylonychia lemnae (Ciliate)",
 "Blepharisma stoltei",
 "Stentor coeruleus",
 "Perkinsus chesapeaki (Clam parasite) (Perkinsus andrewsi)",
 "Perkinsus marinus (strain ATCC 50983 / TXsc)",
 "Polarella glacialis (Dinoflagellate)",
 "Prorocentrum cordatum",
 "Symbiodinium microadriaticum (Dinoflagellate) (Zooxanthella microadriatica)",
 "Symbiodinium natans",
 "Cladocopium goreaui",
 "Durusdinium trenchii",
 "Gregarina niphandrodes (Septate eugregarine)",
 "Vitrella brassicaformis",
 "Cryptosporidium muris (strain RN66)",
 "Cyclospora cayetanensis",
 "Eimeria tenella (Coccidian parasite)",
 "Besnoitia besnoiti (Apicomplexan protozoan)",
 "Cystoisospora suis",
 "Plasmodium falciparum (isolate 3D7)",
 "Plasmodium reichenowi",
 "Plasmodium chabaudi chabaudi",
 "Plasmodium gonderi",
 "Babesia bovis",
 "Theileria parva (East coast fever infection agent)",
 "Blastocystis hominis",
 "Blastocystis sp. subtype 1 (strain ATCC 50177 / NandII)",
 "Hondaea fermentalgiana",
 "Nannochl
… (잘림 — 원본 파일 참조)
```

## root_split_intruders

```json
{
 "discoba": [],
 "opisthokonta": [],
 "amorphea": [],
 "metamonada": []
}
```

## misplaced_clade_tips_left_out

```json
[]
```

## non_clade_tips_inside_clade_node

```json
[]
```

## leave_tips_out_auroc

```json
{
 "reconstruction": 0.9851,
 "clade_frequency": 0.9149
}
```

## leave_tips_out_auroc_per_root

```json
{
 "discoba": {
  "reconstruction": 0.9851,
  "clade_frequency": 0.9149
 },
 "opisthokonta": {
  "reconstruction": 0.9794,
  "clade_frequency": 0.9184
 },
 "amorphea": {
  "reconstruction": 0.9846,
  "clade_frequency": 0.9099
 },
 "metamonada": {
  "reconstruction": 0.9835,
  "clade_frequency": 0.93
 }
}
```

## sum_of_posteriors_per_root

```json
{
 "discoba": 3951.3,
 "opisthokonta": 4601.3,
 "amorphea": 4413.1,
 "metamonada": 3918.8
}
```

## n_present_per_root

```json
{
 "discoba": 3153,
 "opisthokonta": 4085,
 "amorphea": 3969,
 "metamonada": 3058
}
```

## functions_of_confident_families

```json
[
 [
  "catalytic activity",
  405
 ],
 [
  "organelle",
  218
 ],
 [
  "transferase activity",
  143
 ],
 [
  "helicase_nucleic",
  118
 ],
 [
  "repeat_domain",
  115
 ],
 [
  "hydrolase activity",
  109
 ],
 [
  "nucleus",
  85
 ],
 [
  "protease",
  78
 ],
 [
  "zinc_finger",
  72
 ],
 [
  "methyl_glyco_transferase",
  71
 ],
 [
  "kinase",
  70
 ],
 [
  "uncharacterised",
  68
 ],
 [
  "DNA binding",
  64
 ],
 [
  "structural molecule activity",
  63
 ],
 [
  "catalytic activity, acting on RNA",
  60
 ],
 [
  "cytoskeleton_motor",
  59
 ],
 [
  "catalytic activity, acting on a protein",
  57
 ],
 [
  "transporter_channel",
  56
 ],
 [
  "RNA binding",
  56
 ],
 [
  "oxidoreductase activity",
  52
 ]
]
```

## functions_of_root_dependent_families

```json
[
 [
  "catalytic activity",
  90
 ],
 [
  "organelle",
  45
 ],
 [
  "uncharacterised",
  34
 ],
 [
  "transferase activity",
  27
 ],
 [
  "repeat_domain",
  21
 ],
 [
  "hydrolase activity",
  20
 ],
 [
  "methyl_glyco_transferase",
  17
 ],
 [
  "helicase_nucleic",
  16
 ],
 [
  "oxidoreductase activity",
  16
 ],
 [
  "cell_adhesion_surface",
  14
 ],
 [
  "amino acid metabolic process",
  14
 ],
 [
  "transporter_channel",
  13
 ],
 [
  "lyase activity",
  13
 ],
 [
  "transporter activity",
  13
 ],
 [
  "DNA binding",
  13
 ],
 [
  "mitochondrion",
  13
 ],
 [
  "regulation of DNA-templated transcription",
  13
 ],
 [
  "nucleobase-containing small molecule metabolic process",
  12
 ],
 [
  "carbohydrate derivative metabolic process",
  12
 ],
 [
  "kinase",
  12
 ]
]
```

## top_families

```json
[
 {
  "family": "PRK",
  "description": "Phosphoribulokinase / Uridine kinase family",
  "posterior_discoba": 1.0,
  "posterior_opisthokonta": 1.0,
  "posterior_amorphea": 1.0,
  "posterior_metamonada": 1.0,
  "share_of_tips_today": 0.92
 },
 {
  "family": "ClpB_D2-small",
  "description": "C-terminal, D2-small domain, of ClpB protein",
  "posterior_discoba": 1.0,
  "posterior_opisthokonta": 1.0,
  "posterior_amorphea": 1.0,
  "posterior_metamonada": 1.0,
  "share_of_tips_today": 0.948
 },
 {
  "family": "HBB",
  "description": "Helical and beta-bridge domain",
  "posterior_discoba": 1.0,
  "posterior_opisthokonta": 1.0,
  "posterior_amorphea": 1.0,
  "posterior_metamonada": 1.0,
  "share_of_tips_today": 0.932
 },
 {
  "family": "IMS_C",
  "description": "impB/mucB/samB family C-terminal domain",
  "posterior_discoba": 1.0,
  "posterior_opisthokonta": 1.0,
  "posterior_amorphea": 1.0,
  "posterior_metamonada": 1.0,
  "share_of_tips_today": 0.892
 },
 {
  "family": "Peptidase_S8",
  "description": "Subtilase family",
  "posterior_discoba": 1.0,
  "posterior_opisthokonta": 1.0,
  "posterior_amorphea": 1.0,
  "posterior_metamonada": 1.0,
  "share_of_tips_today": 0.944
 },
 {
  "family": "G6PD_C",
  "description": "Glucose-6-phosphate dehydrogenase, C-terminal domain",
  "posterior_discoba": 1.0,
  "posterior_opisthokonta": 1.0,
  "posterior_amorphea": 1.0,
  "posterior_metamonada": 1.0,
  "share_of_tips_today": 0.908
 },
 {
  "family": "PI3Ka",
  "description": "Phosphoinositide 3-kinase family, accessory domain (PIK domain)",
  "posterior_discoba": 1.0,
  "posterior_opisthok
… (잘림 — 원본 파일 참조)
```

## root_dependent_families

```json
[
 {
  "family": "Tra1_central",
  "description": "Tra1 HEAT repeat central region",
  "posterior_discoba": 0.5,
  "posterior_opisthokonta": 1.0,
  "posterior_amorphea": 1.0,
  "posterior_metamonada": 0.505,
  "share_of_tips_today": 0.736
 },
 {
  "family": "BRR2_plug",
  "description": "Pre-mRNA-splicing helicase BRR2 plug domain",
  "posterior_discoba": 0.52,
  "posterior_opisthokonta": 1.0,
  "posterior_amorphea": 1.0,
  "posterior_metamonada": 0.497,
  "share_of_tips_today": 0.704
 },
 {
  "family": "HCNGP",
  "description": "HCNGP-like protein",
  "posterior_discoba": 0.496,
  "posterior_opisthokonta": 0.999,
  "posterior_amorphea": 1.0,
  "posterior_metamonada": 0.501,
  "share_of_tips_today": 0.676
 },
 {
  "family": "Helicase_PWI",
  "description": "N-terminal helicase PWI domain",
  "posterior_discoba": 0.494,
  "posterior_opisthokonta": 0.999,
  "posterior_amorphea": 0.994,
  "posterior_metamonada": 0.513,
  "share_of_tips_today": 0.876
 },
 {
  "family": "MoaC",
  "description": "MoaC family",
  "posterior_discoba": 0.547,
  "posterior_opisthokonta": 1.0,
  "posterior_amorphea": 1.0,
  "posterior_metamonada": 0.492,
  "share_of_tips_today": 0.764
 },
 {
  "family": "PAN_1",
  "description": "PAN domain",
  "posterior_discoba": 0.489,
  "posterior_opisthokonta": 0.995,
  "posterior_amorphea": 0.997,
  "posterior_metamonada": 0.5,
  "share_of_tips_today": 0.48
 },
 {
  "family": "Phytochelatin",
  "description": "Phytochelatin synthase",
  "posterior_discoba": 0.658,
  "posterior_opisthokonta": 0.999,
  "posterior_amorphea": 1.0,
  "posterior_metamonada": 0.484,
  
… (잘림 — 원본 파일 참조)
```

## 연결
- [[실험 목록]]
