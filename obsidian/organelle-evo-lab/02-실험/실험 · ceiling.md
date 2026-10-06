---
유형: 실험
실행: ceiling
산출: results/ceiling/metrics.json
tags:
  - 유형/실험
  - 실험/ceiling
---

# 실험 · ceiling

**산출물** `results/ceiling/metrics.json`

## parasites

```json
{
 "mean_auroc": {
  "sibling_oracle": 0.8951473134570804,
  "best_single_sibling": 0.8682222185673799,
  "memorisation_other_clades": 0.7884345964125631,
  "law_other_clades": 0.7813487552205394,
  "n_with_law": 42
 },
 "targets": [
  {
   "pair": "Dictyostelium discoideum -> Entamoeba histolytica",
   "n_siblings": 2,
   "sibling_oracle": 0.9854853989293085,
   "best_single_sibling": 0.9736511545407637,
   "memorisation_other_clades": 0.8064114502708978
  },
  {
   "pair": "Chromera velia -> Plasmodium falciparum",
   "n_siblings": 15,
   "sibling_oracle": 0.9808424634687213,
   "best_single_sibling": 0.9702896590032226,
   "memorisation_other_clades": 0.8362012194510895
  },
  {
   "pair": "Chromera velia -> Babesia bovis",
   "n_siblings": 15,
   "sibling_oracle": 0.968071059765353,
   "best_single_sibling": 0.9473606226889665,
   "memorisation_other_clades": 0.8488751327802667
  },
  {
   "pair": "Chromera velia -> Toxoplasma gondii",
   "n_siblings": 15,
   "sibling_oracle": 0.9733040116610685,
   "best_single_sibling": 0.9783554090880284,
   "memorisation_other_clades": 0.8333633310095697
  },
  {
   "pair": "Chromera velia -> Eimeria tenella",
   "n_siblings": 15,
   "sibling_oracle": 0.9203699365651277,
   "best_single_sibling": 0.8888527620123587,
   "memorisation_other_clades": 0.8205810760264274
  },
  {
   "pair": "Chromera velia -> Cryptosporidium parvum",
   "n_siblings": 1,
   "sibling_oracle": 0.9349294112664497,
   "best_single_sibling": 0.9349294112664497,
   "memorisation_other_clades": 0.8670440112879663
  },
  {
   "pair": "Bodo saltans -> Leishmania major",
   "n_siblings": 5,
   "sibling_oracle": 0.9952816779552084,
   "best_single_sibling": 0.979206461210713,
   "memorisation_other_clades": 0.7692092477651384
  },
  {
   "pair": "Bodo saltans -> Trypanosoma cruzi",
   "n_siblings": 5,
   "sibling_oracle": 0.8825699742320334,
   "best_single_sibling": 0.8645894625248549,
   "memorisation_other_clades": 0.771274740798604
  },
  {
   "pair": "Bodo saltans -> Trypanosoma brucei",
   "n_siblings": 6,
   "sibling_oracle": 0.9577333164117161,
   "best_single_sibling": 0.9347059072376723,
   "memorisation_other_clades": 0.7768324380808909
  },
  {
   "pair": "Spizellomyces punctatus -> Rozella allomycis",
   "n_siblings": 2,
   "sibling_oracle": 0.805261075490998,
   "best_single_sibling": 0.7457203664291663,
   "memorisation_other_clades": 0.7864725037898909
  },
  {
   "pair": "Spizellomyces punctatus -> Encephalitozoon cuniculi",
   "n_siblings": 9,
   "sibling_oracle": 0.9902591692134303,
   "best_single_sibling": 0.9785946531791907,
   "memorisation_other_clades": 0.8665775299388777
  },
  {
   "pair": "Spizellomyces punctatus -> Nosema ceranae",
   "n_siblings": 9,
   "sibling_oracle": 0.9873925548292974,
   "best_single_sibling": 0.9433939142481795,
   "memorisation_other_clades": 0.8634764158298369
  },
  {
   "pair": "Schizosaccharomyces pombe -> Pneumocystis jirovecii",
   "n_siblings": 1,
   "sibling_oracle": 0.5891328958171651,
   "best_single_sibling": 0.5891328958171651,
   "memorisation_other_clades": 0.7725535487637664
  },
  {
   "pair": "Schizosaccharomyces pombe -> Taphrina deformans",
   "n_siblings": 1,
   "sibling_oracle": 0.5834630779601162,
   "best_single_sibling": 0.5834630779601162,
   "memorisation_other_clades": 0.6611984438364548
  },
  {
   "pair": "Coprinopsis cinerea -> Ustilago maydis",
   "n_siblings": 1,
   "sibling_oracle": 0.7730478305231075,
   "best_single_sibling": 0.7730478305231075,
   "memorisation_other_clades": 0.7088982672090904
  },
  {
   "pair": "Spizellomyces punctatus -> Batrachochytrium dendrobatidis",
   "n_siblings": 2,
   "sibling_oracle": 0.7804170043954162,
   "best_single_sibling": 0.7355524242504807,
   "memorisation_other_clades": 0.7668762686841543
  },
  {
   "pair": "Spizellomyces punctatus -> Enterocytozoon bieneusi",
   "n_siblings": 9,
   "sibling_oracle": 0.9462291346933204,
   "best_single_sibling": 0.905864940747833,
   "memorisation_other_clades": 0.8554664040363783
  },
  {
   "pair": "Spizellomyces punctatus -> Nematocida parisii",
   "n_siblings": 9,
   "sibling_oracle": 0.9538265780633961,
   "best_single_sibling": 0.8985850131847211,
   "memorisation_other_clades": 0.8630152162257778
  },
  {
   "pair": "Spizellomyces punctatus -> Vavraia culicis",
   "n_siblings": 9,
   "sibling_oracle": 0.9831182313904011,
   "best_single_sibling": 0.9161272317383456,
   "memorisation_other_clades": 0.8649066620515683
  },
  {
   "pair": "Spizellomyces punctatus -> Encephalitozoon intestinalis",
   "n_siblings": 9,
   "sibling_oracle": 0.9892527349470238,
   "best_single_sibling": 0.9769967266775778,
   "memorisation_other_clades": 0.8658677534671375
  },
  {
   "pair": "Chromera velia -> Plasmodium vivax",
   "n_siblings": 15,
   "sibling_oracle": 0.9816046171199111,
   "best_single_sibling": 0.9798380324564903,
   "memorisation_other_clades": 0.8316072652076578
  },
  {
   "pair": "Chromera velia -> Plasmodium berghei",
   "n_siblings": 15,
   "sibling_oracle": 0.9828450963390815,
   "best_single_sibling": 0.9893162566503481,
   "memorisation_other_clades": 0.8365352909260357
  },
  {
   "pair": "Chromera velia -> Plasmodium knowlesi",
   "n_siblings": 15,
   "sibling_oracle": 0.9842116537723139,
   "best_single_sibling": 0.979802319456796,
   "memorisation_other_clades": 0.83519170728356
  },
  {
   "pair": "Chromera velia -> Theileria annulata",
   "n_siblings": 15,
   "sibling_oracle": 0.9644185330657374,
   "best_single_sibling": 0.9689830946722977,
   "memorisation_other_clades": 0.8468925225014468
  },
  {
   "pair": "Chromera velia -> Theileria parva",
   "n_siblings": 15,
   "sibling_oracle": 0.9713486661208129,
   "best_single_sibling": 0.9654755648975302,
   "memorisation_other_clades": 0.8508318566767283
  },
  {
   "pair": "Chromera velia -> Babesia microti",
   "n_siblings": 15,
   "sibling_oracle": 0.9651126913588912,
   "best_single_sibling": 0.9355656648519651,
   "memorisation_other_clades": 
… (잘림, 원본 파일 참조)
```

## extremophiles

```json
{
 "mean_auroc": {
  "sibling_oracle": 0.8526768195049236,
  "best_single_sibling": 0.8114754748155437,
  "memorisation_other_clades": 0.8092719159037682
 },
 "targets": [
  {
   "pair": "Shewanella oneidensis -> Shewanella frigidimarina",
   "n_siblings": 2,
   "sibling_oracle": 0.8612946647087616,
   "best_single_sibling": 0.8029891577655744,
   "memorisation_other_clades": 0.8324436431785113
  },
  {
   "pair": "Shewanella oneidensis -> Colwellia psychrerythraea",
   "n_siblings": 2,
   "sibling_oracle": 0.8260064884456783,
   "best_single_sibling": 0.7843383307748714,
   "memorisation_other_clades": 0.7964251684733593
  },
  {
   "pair": "Bacillus subtilis -> Planococcus halocryophilus",
   "n_siblings": 6,
   "sibling_oracle": 0.8852310185819294,
   "best_single_sibling": 0.7837711728986897,
   "memorisation_other_clades": 0.8120999406473999
  },
  {
   "pair": "Bacillus subtilis -> Geobacillus kaustophilus",
   "n_siblings": 6,
   "sibling_oracle": 0.8814349855739618,
   "best_single_sibling": 0.7835283820144584,
   "memorisation_other_clades": 0.8369596820598437
  },
  {
   "pair": "Bacillus subtilis -> Lactiplantibacillus plantarum",
   "n_siblings": 6,
   "sibling_oracle": 0.8380660001301617,
   "best_single_sibling": 0.7555863785753799,
   "memorisation_other_clades": 0.7991012739578927
  },
  {
   "pair": "Flavobacterium johnsoniae -> Psychroflexus torquis",
   "n_siblings": 2,
   "sibling_oracle": 0.8082138775781917,
   "best_single_sibling": 0.7346750840443355,
   "memorisation_other_clades": 0.8243689740488844
  },
  {
   "pair": "Thermus thermophilus -> Deinococcus radiodurans",
   "n_siblings": 4,
   "sibling_oracle": 0.9641159430406254,
   "best_single_sibling": 0.8828493647912886,
   "memorisation_other_clades": 0.8089295686165014
  },
  {
   "pair": "Micrococcus luteus -> Kineococcus radiotolerans",
   "n_siblings": 1,
   "sibling_oracle": 0.7330855594270228,
   "best_single_sibling": 0.7330855594270228,
   "memorisation_other_clades": 0.8183417215124532
  },
  {
   "pair": "Synechocystis sp. PCC 6803 -> Chroococcidiopsis thermalis",
   "n_siblings": 1,
   "sibling_oracle": 0.781149612039142,
   "best_single_sibling": 0.781149612039142,
   "memorisation_other_clades": 0.8526845285163586
  },
  {
   "pair": "Synechococcus elongatus -> Prochlorococcus marinus",
   "n_siblings": 2,
   "sibling_oracle": 0.8299174794508711,
   "best_single_sibling": 0.8040623008543685,
   "memorisation_other_clades": 0.7852089476469762
  },
  {
   "pair": "Myxococcus xanthus -> Geobacter sulfurreducens",
   "n_siblings": 2,
   "sibling_oracle": 0.9443892432171853,
   "best_single_sibling": 0.9177112270625896,
   "memorisation_other_clades": 0.8348079430808875
  },
  {
   "pair": "Methanosarcina acetivorans -> Methanococcoides burtonii",
   "n_siblings": 5,
   "sibling_oracle": 0.834115025005436,
   "best_single_sibling": 0.8325755599043271,
   "memorisation_other_clades": 0.7874151989562949
  },
  {
   "pair": "Methanosarcina acetivorans -> Halobacterium salinarum",
   "n_siblings": 5,
   "sibling_oracle": 0.9380123451191605,
   "best_single_sibling": 0.8919326791594575,
   "memorisation_other_clades": 0.7973812405815706
  },
  {
   "pair": "Methanosarcina acetivorans -> Haloferax volcanii",
   "n_siblings": 5,
   "sibling_oracle": 0.9597300496148801,
   "best_single_sibling": 0.9178528372822479,
   "memorisation_other_clades": 0.7872358942037802
  },
  {
   "pair": "Methanococcus maripaludis -> Methanocaldococcus jannaschii",
   "n_siblings": 1,
   "sibling_oracle": 0.7905020489376318,
   "best_single_sibling": 0.7905020489376318,
   "memorisation_other_clades": 0.6881410332330578
  },
  {
   "pair": "Bacillus subtilis -> Bacillus licheniformis",
   "n_siblings": 6,
   "sibling_oracle": 0.9052832761374571,
   "best_single_sibling": 0.8235081666185992,
   "memorisation_other_clades": 0.7749304785667605
  },
  {
   "pair": "Pseudomonas aeruginosa -> Pseudomonas putida",
   "n_siblings": 2,
   "sibling_oracle": 0.8423929031071888,
   "best_single_sibling": 0.8189648832505976,
   "memorisation_other_clades": 0.8157234785806214
  },
  {
   "pair": "Pseudomonas aeruginosa -> Halomonas elongata",
   "n_siblings": 2,
   "sibling_oracle": 0.9102881176341633,
   "best_single_sibling": 0.8826195686151922,
   "memorisation_other_clades": 0.8455130052816829
  },
  {
   "pair": "Pseudomonas aeruginosa -> Chromohalobacter salexigens",
   "n_siblings": 2,
   "sibling_oracle": 0.8843224593561068,
   "best_single_sibling": 0.8728627685559045,
   "memorisation_other_clades": 0.8409956774694325
  },
  {
   "pair": "Bacillus subtilis -> Halobacillus halophilus",
   "n_siblings": 6,
   "sibling_oracle": 0.9079062653713723,
   "best_single_sibling": 0.8184661419904903,
   "memorisation_other_clades": 0.8317298430070503
  },
  {
   "pair": "Methanosarcina acetivorans -> Haloarcula marismortui",
   "n_siblings": 5,
   "sibling_oracle": 0.9551062469103586,
   "best_single_sibling": 0.9175839877094294,
   "memorisation_other_clades": 0.7971435633466077
  },
  {
   "pair": "Methanosarcina acetivorans -> Natronomonas pharaonis",
   "n_siblings": 5,
   "sibling_oracle": 0.9589809427109774,
   "best_single_sibling": 0.9048355918303589,
   "memorisation_other_clades": 0.7987366735658219
  },
  {
   "pair": "Bacillus subtilis -> Clostridium acetobutylicum",
   "n_siblings": 6,
   "sibling_oracle": 0.8318207786195018,
   "best_single_sibling": 0.7668968842052504,
   "memorisation_other_clades": 0.8054370841377143
  },
  {
   "pair": "Myxococcus xanthus -> Geobacter metallireducens",
   "n_siblings": 2,
   "sibling_oracle": 0.9370936341631938,
   "best_single_sibling": 0.9187135786267105,
   "memorisation_other_clades": 0.8421770909833608
  },
  {
   "pair": "Myxococcus xanthus -> Desulfuromonas acetoxidans",
   "n_siblings": 2,
   "sibling_oracle": 0.8602111573847243,
   "best_single_sibling": 0.8358303221460068,
   "memorisation_other_clades": 0.8434110287712995
  },
  {
   "pair": "Thermus thermophilus -> Deinococcus geo
… (잘림, 원본 파일 참조)
```

## 연결
- [[실험 목록]]
