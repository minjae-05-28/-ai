---
유형: 실험
실행: real
산출: results/real/metrics.json
tags:
  - 유형/실험
  - 실험/real
---

# 실험 · real

**산출물** `results/real/metrics.json`

## mitochondrion

```json
{
 "n_genomes": 30,
 "genes_added_by_homology": {
  "Acanthamoeba castellanii": 1,
  "Allomyces macrogynus": 2,
  "Andalucia godoyi": 0,
  "Arabidopsis thaliana": 1,
  "Caenorhabditis elegans": 0,
  "Chlamydomonas reinhardtii": 0,
  "Chondrus crispus": 0,
  "Cyanidioschyzon merolae": 4,
  "Danio rerio": 0,
  "Dictyostelium discoideum": 3,
  "Drosophila melanogaster": 0,
  "Gallus gallus": 0,
  "Homo sapiens": 0,
  "Jakoba libera": 0,
  "Marchantia polymorpha subsp. ruderalis": 1,
  "Metridium senile": 0,
  "Monosiga brevicollis": 0,
  "Mus musculus": 0,
  "Nephroselmis olivacea": 2,
  "Neurospora crassa OR74A": 1,
  "Physcomitrium patens": 1,
  "Phytophthora infestans": 0,
  "Plasmodium falciparum": 0,
  "Prototheca wickerhamii": 1,
  "Reclinomonas americana": 0,
  "Saccharomyces cerevisiae S288C": 1,
  "Schizosaccharomyces pombe": 1,
  "Tetrahymena thermophila": 1,
  "Thalassiosira pseudonana": 1,
  "Trichoplax adhaerens": 1
 },
 "n_genes": 71,
 "law": {
  "hydrophobicity_gravy": {
   "weight": -0.3241418241760178,
   "se": 0.07812490827748861
  },
  "tm_helices": {
   "weight": -0.3671598749796798,
   "se": 0.11905868574019886
  },
  "protein_length": {
   "weight": -0.1877466109932678,
   "se": 0.04548552858076347
  },
  "redox_core": {
   "weight": -1.5404350977773398,
   "se": 0.25985244014032344
  },
  "atp_synthase": {
   "weight": -1.29932218522161,
   "se": 0.23807102474607147
  },
  "translation": {
   "weight": -1.122903065311948,
   "se": 0.27198708302460084
  },
  "transcription": {
   "weight": 1.0168733663072134,
   "se": 0.2681975563217674
  },
  "protein_ta
… (잘림 — 원본 파일 참조)
```

## plastid

```json
{
 "n_genomes": 21,
 "genes_added_by_homology": {
  "Amborella trichopoda": 3,
  "Arabidopsis thaliana": 0,
  "Chlamydomonas reinhardtii": 1,
  "Cyanidioschyzon merolae strain 10D": 7,
  "Cyanophora paradoxa": 4,
  "Emiliania huxleyi": 3,
  "Epifagus virginiana": 1,
  "Euglena gracilis": 0,
  "Guillardia theta": 2,
  "Marchantia polymorpha": 3,
  "Mesostigma viride": 0,
  "Nephroselmis olivacea": 0,
  "Nicotiana tabacum": 0,
  "Oryza sativa Japonica Group": 1,
  "Paulinella chromatophora": 32,
  "Phaeodactylum tricornutum": 0,
  "Physcomitrium patens": 2,
  "Plasmodium falciparum 3D7": 2,
  "Porphyra purpurea": 18,
  "Thalassiosira pseudonana": 0,
  "Toxoplasma gondii RH": 0
 },
 "n_genes": 252,
 "law": {
  "hydrophobicity_gravy": {
   "weight": 0.013405401849953383,
   "se": 0.04655984972687289
  },
  "tm_helices": {
   "weight": -0.04664167495332825,
   "se": 0.059313435989215485
  },
  "protein_length": {
   "weight": -0.04012684807099351,
   "se": 0.0373882530071814
  },
  "redox_core": {
   "weight": -1.364761403819263,
   "se": 0.15892393019594317
  },
  "atp_synthase": {
   "weight": -1.848839314336799,
   "se": 0.2194269317094987
  },
  "translation": {
   "weight": -1.3034161951242544,
   "se": 0.0908535455095053
  },
  "transcription": {
   "weight": -2.5516116783998766,
   "se": 0.3562524824727305
  },
  "protein_targeting": {
   "weight": -0.6680114134096448,
   "se": 0.22656746263645053
  }
 },
 "lolo_auroc": {
  "law_features_only": 0.7363440881318014,
  "gene_prevalence": 0.8666595274366087,
  "law_plus_prevalence": 0.8454312691012017
 }
}
```

## insect_endosymbiont

```json
{
 "n_genomes": 13,
 "genes_added_by_homology": {
  "Candidatus Palibaumannia cicadellinicola": 111,
  "Candidatus Blochmanniella floridana": 91,
  "Candidatus Blochmanniella pennsylvanica": 112,
  "Buchnera aphidicola str. Bp (Baizongia pistaciae)": 80,
  "Buchnera aphidicola (Cinara tujafilina)": 48,
  "Buchnera aphidicola (Schizaphis graminum)": 130,
  "Buchnera aphidicola str. APS (Acyrthosiphon pisum)": 125,
  "Candidatus Hamiltonella defensa (Bemisia tabaci)": 237,
  "Candidatus Moranella endobia PCIT": 101,
  "Candidatus Riesia pediculicola": 133,
  "Serratia symbiotica": 472,
  "Sodalis glossinidius str. 'morsitans'": 1439,
  "Wigglesworthia glossinidia endosymbiont of Glossina morsitans morsitans (Yale colony)": 71
 },
 "n_genes": 4277,
 "law": {
  "hydrophobicity_gravy": {
   "weight": -0.012701211750331594,
   "se": 0.009137284346539033
  },
  "tm_helices": {
   "weight": 0.16227785939474115,
   "se": 0.010179706246226286
  },
  "protein_length": {
   "weight": -0.13458257554168274,
   "se": 0.007699312044840191
  },
  "redox_core": {
   "weight": -2.0486728551204476,
   "se": 0.24330917668783283
  },
  "atp_synthase": {
   "weight": -1.747347733149512,
   "se": 0.37878029047937006
  },
  "translation": {
   "weight": -3.073558285494741,
   "se": 0.11022108597299336
  },
  "transcription": {
   "weight": -1.3994394449666816,
   "se": 0.09429999392687857
  },
  "protein_targeting": {
   "weight": -0.7963226288444202,
   "se": 0.03247843144612104
  }
 },
 "lolo_auroc": {
  "law_features_only": 0.6447232455484303,
  "gene_prevalence": 0.9533839192735963,
  "law_plus
… (잘림 — 원본 파일 참조)
```

## universality

```json
{
 "systems": [
  "mitochondrion",
  "plastid",
  "insect_endosymbiont"
 ],
 "delta_aic_shared_minus_separate": 786.6381325855909,
 "shared_weights": {
  "hydrophobicity_gravy": -0.012185535834246265,
  "tm_helices": 0.14364596722106382,
  "protein_length": -0.13865754264813954,
  "redox_core": -2.099747593227983,
  "atp_synthase": -2.0106604695359174,
  "translation": -1.494367311011397,
  "transcription": -1.0963252210737076,
  "protein_targeting": -0.7878280236921446
 }
}
```

## 연결
- [[실험 목록]]
