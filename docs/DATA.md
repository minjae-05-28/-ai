# 데이터 카드

프로젝트가 쓰는 모든 유전체와 출처입니다. `scripts/build_data_card.py`로 생성합니다. 모든 데이터는 NCBI(Datasets, GenBank)와 EBI(Pfam, InterPro)에서 GitHub Actions로 받아 저장소에 커밋했습니다.

| 데이터 | 위치 | 출처 |
|---|---|---|
| 소기관·공생세균 유전체 (GenBank) | `data/raw/` | NCBI nuccore |
| 유전자군 계수 (Pfam, HMMER 수집 임계값) | `data/eukaryotes/`, `data/prokaryotes/` | NCBI Datasets 단백질 + Pfam-A |
| 유전자군 주석 (GO slim, 클랜) | `data/eukaryotes/family_annotations.json` | InterPro / pfam2go |
| 단백질 조성 | `data/composition/` | 위 단백질체 |
| 유전자군별 도메인 조성 | `data/family_composition/` | 위 단백질체 + Pfam |
| 유전자군 맥락 (발현·오페론·도메인) | `data/family_context/` | 단백질·CDS·GFF |
| 리보솜 단백질 마커 | `data/markers/` | 위 단백질체 + Pfam |
| 분류 체계 | `results/taxonomy/taxonomy.json` | NCBI Taxonomy |
| 유전체 GC | `results/gc/gc.json` | NCBI 어셈블리 통계, GenBank 서열 |

참고: NCBI 어셈블리 통계는 약 절반의 유전체에서 GC를 정수 %로 반올림해 줍니다(오차 ±0.5%p, 종 간 범위 25–70%에 비해 작음).

## 진핵생물 (125종)

| 종 | 어셈블리 | 유전자 | 역할 | 조성 | 맥락 | GC |
|---|---|---|---|---|---|---|
| *Acanthamoeba castellanii* | GCF_000313135.1 | 14,968 | 후손 | ✓ | ✓ | 58.5% |
| *Angomonas deanei* | GCA_903995115.1 | 10,365 | 후손 | ✓ |  | 50.0% |
| *Anncaliia algerae* | GCA_000385875.2 | 3,598 | 후손 | ✓ |  | 23.5% |
| *Anopheles gambiae* | GCF_943734735.2 | 12,519 | 후손 | ✓ | ✓ | 44.5% |
| *Aphanomyces astaci* | GCF_000520075.1 | 19,119 | 후손 | ✓ |  | 50.0% |
| *Aspergillus fumigatus* | GCF_000002655.1 | 9,823 | — (기후 대상) | ✓ |  | 50.0% |
| *Aspergillus nidulans* | GCF_000011425.1 | 10,453 | 후손 | ✓ | ✓ | 50.5% |
| *Auxenochlorella protothecoides* | GCF_000733215.1 | 7,010 | 조상 대리 | ✓ | ✓ | 63.5% |
| *Babesia bovis* | GCF_000165395.2 | 3,959 | 후손 | ✓ |  | 41.5% |
| *Babesia microti* | GCF_000691945.2 | 3,601 | 후손 | ✓ |  | 36.5% |
| *Batrachochytrium dendrobatidis* | GCF_000203795.2 | 8,386 | 후손 | ✓ |  | 39.5% |
| *Besnoitia besnoiti* | GCF_002563875.1 | 8,220 | 후손 | ✓ |  | 57.0% |
| *Blastocystis hominis* | GCF_000151665.1 | 6,020 | 후손 | ✓ |  | 45.0% |
| *Blumeria graminis* | GCA_905067625.1 | 7,993 | 후손 | ✓ |  | 43.5% |
| *Bodo saltans* | GCA_001460835.1 | 18,190 | 조상 대리 | ✓ | ✓ | 52.0% |
| *Brugia malayi* | GCF_000002995.4 | 10,904 | 후손 | ✓ |  | 28.5% |
| *Caenorhabditis briggsae* | GCF_000004555.2 | 21,922 | 후손 | ✓ | ✓ | 37.5% |
| *Caenorhabditis elegans* | GCF_000002985.6 | 19,983 | 조상 대리 | ✓ | ✓ | 35.5% |
| *Candida auris* | GCF_003013715.1 | 5,327 | — (기후 대상) | ✓ |  | 45.5% |
| *Capsaspora owczarzaki* | GCF_000151315.2 | 8,621 | 후손 | ✓ | ✓ | 54.0% |
| *Chlamydomonas reinhardtii* | GCF_000002595.2 | 17,742 | 조상 대리 | ✓ | ✓ | 64.0% |
| *Chlorella variabilis* | GCF_000147415.1 | 9,780 | 후손 | ✓ | ✓ | 67.0% |
| *Chromera velia* | GCA_900069035.1 | 29,094 | 조상 대리 | ✓ | ✓ | 49.0% |
| *Clonorchis sinensis* | GCA_003604175.2 | 13,489 | 후손 | ✓ |  | 44.0% |
| *Coccidioides immitis* | GCF_000149335.2 | 9,757 | — (기후 대상) | ✓ |  | 46.0% |
| *Coprinopsis cinerea* | GCF_000182895.1 | 13,355 | 조상 대리 | ✓ | ✓ | 51.5% |
| *Cryptococcus gattii* | GCF_000185945.1 | 6,565 | — (기후 대상) | ✓ |  | 48.0% |
| *Cryptococcus neoformans* | GCF_000149245.1 | 6,975 | — (기후 대상) | ✓ |  | 48.0% |
| *Cryptosporidium hominis* | GCF_000006425.1 | 3,885 | 후손 | ✓ |  | 31.0% |
| *Cryptosporidium parvum* | GCF_000165345.1 | 3,805 | 후손 | ✓ |  | 30.0% |
| *Cyanidioschyzon merolae* | GCF_000091205.1 | 4,803 | 조상 대리 | ✓ | ✓ | 55.0% |
| *Cyclospora cayetanensis* | GCF_002999335.1 | 5,793 | 후손 | ✓ |  | 52.0% |
| *Dictyostelium discoideum* | GCF_000004695.1 | 13,278 | 조상 대리 | ✓ | ✓ | 22.5% |
| *Dictyostelium purpureum* | GCF_000190715.1 | 12,395 | 후손 | ✓ | ✓ | 24.5% |
| *Drosophila melanogaster* | GCF_000001215.4 | 13,986 | 조상 대리 | ✓ | ✓ | 42.0% |
| *Echinococcus multilocularis* | GCA_000469725.3 | 10,656 | 후손 | ✓ |  | 42.0% |
| *Edhazardia aedis* | GCA_000230595.3 | 4,190 | 후손 | ✓ |  | 22.5% |
| *Eimeria tenella* | GCF_000499545.2 | 8,596 | 후손 | ✓ |  | 51.5% |
| *Encephalitozoon cuniculi* | GCF_000091225.2 | 2,122 | 후손 | ✓ |  | 47.5% |
| *Encephalitozoon intestinalis* | GCF_000146465.1 | 1,938 | 후손 | ✓ |  | 41.5% |
| *Entamoeba dispar* | GCF_000209125.1 | 8,811 | 후손 | ✓ |  | 24.0% |
| *Entamoeba histolytica* | GCF_000208925.1 | 8,151 | 후손 | ✓ |  | 24.5% |
| *Entamoeba invadens* | GCF_000330505.1 | 11,997 | 후손 | ✓ |  | 30.0% |
| *Enterocytozoon bieneusi* | GCF_000209485.1 | 3,632 | 후손 | ✓ |  |  |
| *Fasciola hepatica* | GCA_948099385.2 | 789 | 후손 | ✓ |  | 44.0% |
| *Galdieria sulphuraria* | GCF_000341285.1 | 6,594 | 후손 | ✓ | ✓ | 37.5% |
| *Giardia intestinalis* | GCF_000002435.2 | 4,965 | 후손 | ✓ |  | 49.5% |
| *Gregarina niphandrodes* | GCF_000223845.1 | 6,375 | 후손 | ✓ |  | 54.0% |
| *Haemonchus contortus* | GCA_041937105.1 | 19,234 | 후손 | ✓ |  | 43.0% |
| *Hammondia hammondi* | GCF_000258005.1 | 8,004 | 후손 | ✓ |  | 53.5% |
| *Helicosporidium sp. ATCC 50920* | GCA_000690575.1 | 6,033 | 후손 | ✓ |  | 61.5% |
| *Henneguya salminicola* | GCA_988225545.1 | 8,760 | 후손 | ✓ |  | 29.0% |
| *Hydra vulgaris* | GCF_037890685.1 | 21,916 | 후손 | ✓ | ✓ | 27.0% |
| *Ichthyophthirius multifiliis* | GCF_000220395.1 | 8,056 | 후손 | ✓ |  | 16.0% |
| *Kluyveromyces lactis* | GCF_000002515.2 | 5,084 | 후손 | ✓ | ✓ | 39.0% |
| *Laccaria bicolor* | GCF_000143565.1 | 18,213 | 후손 | ✓ | ✓ | 47.0% |
| *Leishmania braziliensis* | GCF_000002845.2 | 8,127 | 후손 | ✓ |  | 58.0% |
| *Leishmania donovani* | GCF_000227135.1 | 7,953 | 후손 | ✓ |  | 59.5% |
| *Leishmania infantum* | GCF_000002875.2 | 8,135 | 후손 | ✓ |  | 59.5% |
| *Leishmania major* | GCF_000002725.2 | 8,309 | 후손 | ✓ |  | 59.5% |
| *Leishmania mexicana* | GCF_000234665.1 | 8,147 | 후손 | ✓ |  | 60.0% |
| *Leptomonas pyrrhocoris* | GCF_001293395.1 | 9,872 | 후손 | ✓ |  | 56.5% |
| *Macrostomum lignano* | GCA_002269645.1 | 49,018 | 조상 대리 | ✓ | ✓ | 46.0% |
| *Malassezia globosa* | GCF_000181695.2 | 4,278 | 후손 | ✓ |  | 52.0% |
| *Mitosporidium daphniae* | GCF_000760515.2 | 3,291 | 후손 | ✓ |  | 43.0% |
| *Monosiga brevicollis* | GCF_000002865.3 | 9,202 | 조상 대리 | ✓ | ✓ | 55.0% |
| *Naegleria fowleri* | GCF_008403515.1 | 13,808 | 후손 | ✓ | ✓ | 37.0% |
| *Naegleria gruberi* | GCF_000004985.1 | 15,709 | 조상 대리 | ✓ | ✓ | 33.0% |
| *Nematocida parisii* | GCF_000250985.1 | 2,661 | 후손 | ✓ |  | 34.5% |
| *Nematostella vectensis* | GCF_932526225.1 | 19,231 | 조상 대리 | ✓ | ✓ | 40.5% |
| *Neospora caninum* | GCF_000208865.1 | 6,933 | 후손 | ✓ |  | 55.0% |
| *Neurospora crassa* | GCF_000182925.2 | 9,757 | 조상 대리 | ✓ | ✓ | 48.5% |
| *Nosema bombycis* | GCA_000383075.1 | 3,993 | 후손 | ✓ |  | 31.0% |
| *Nosema ceranae* | GCF_000988165.1 | 3,209 | 후손 | ✓ |  | 25.5% |
| *Ostreococcus lucimarinus* | GCF_000092065.1 | 7,603 | 조상 대리 | ✓ | ✓ | 60.5% |
| *Ostreococcus tauri* | GCF_000214015.3 | 7,760 | 후손 | ✓ | ✓ | 59.5% |
| *Paramecium tetraurelia* | GCF_000165425.1 | 39,642 | 후손 | ✓ | ✓ | 28.0% |
| *Pediculus humanus* | GCF_000006295.1 | 10,758 | 후손 | ✓ |  | 27.5% |
| *Perkinsus marinus* | GCF_000006405.1 | 23,474 | 후손 | ✓ |  | 47.5% |
| *Phaeodactylum tricornutum* | GCF_000150955.2 | 10,386 | 후손 | ✓ | ✓ | 49.0% |
| *Phytophthora infestans* | GCF_000142945.1 | 17,797 | 후손 | ✓ |  | 51.0% |
| *Phytophthora sojae* | GCF_000149755.1 | 26,489 | 후손 | ✓ |  | 54.5% |
| *Plasmodiophora brassicae* | GCA_036867785.1 | 10,490 | — | ✓ |  | 59.5% |
| *Plasmodium berghei* | GCF_900002375.2 | 4,932 | 후손 | ✓ |  | 22.0% |
| *Plasmodium falciparum* | GCF_000002765.6 | 5,285 | 후손 | ✓ |  | 19.5% |
| *Plasmodium knowlesi* | GCF_000006355.2 | 5,324 | 후손 | ✓ |  | 38.5% |
| *Plasmodium malariae* | GCF_900090045.1 | 5,909 | 후손 | ✓ |  | 24.5% |
| *Plasmodium vivax* | GCF_000002415.2 | 5,392 | 후손 | ✓ |  | 42.5% |
| *Plasmodium yoelii* | GCF_900002385.2 | 6,037 | 후손 | ✓ |  | 21.5% |
| *Pneumocystis jirovecii* | GCF_001477535.1 | 3,761 | 후손 | ✓ |  | 28.5% |
| *Pristionchus pacificus* | GCA_000180635.4 | 28,149 | 후손 | ✓ | ✓ | 43.0% |
| *Pseudoloma neurophilia* | GCA_001432165.1 | 3,644 | 후손 | ✓ |  | 29.5% |
| *Puccinia graminis* | GCF_000149925.1 | 15,799 | 후손 | ✓ |  | 43.5% |
| *Pyricularia oryzae* | GCF_000002495.2 | 12,825 | 후손 | ✓ |  | 51.5% |
| *Rozella allomycis* | GCA_000442015.1 | 6,350 | 후손 | ✓ |  | 35.0% |
| *Saccharomyces cerevisiae* | GCF_000146045.2 | 6,021 | 조상 대리 | ✓ | ✓ | 38.5% |
| *Salpingoeca rosetta* | GCF_000188695.1 | 11,618 | 조상 대리, 후손 | ✓ | ✓ | 56.0% |
| *Saprolegnia parasitica* | GCF_000151545.1 | 20,121 | 후손 | ✓ |  | 58.5% |
| *Schistosoma japonicum* | GCA_021461655.1 | 9,715 | 후손 | ✓ |  | 34.0% |
| *Schistosoma mansoni* | GCF_000237925.1 | 10,711 | 후손 | ✓ |  | 35.0% |
| *Schizophyllum commune* | GCF_000143185.2 | 16,186 | 후손 | ✓ | ✓ | 57.5% |
| *Schizosaccharomyces pombe* | GCF_000002945.2 | 5,123 | 조상 대리 | ✓ | ✓ | 36.0% |
| *Spironucleus salmonicida* | GCF_000497125.1 | 8,667 | 후손 | ✓ |  | 34.0% |
| *Spizellomyces punctatus* | GCF_000182565.1 | 8,950 | 조상 대리 | ✓ | ✓ | 47.5% |
| *Strigomonas culicis* | GCA_000442495.1 | 12,083 | 후손 | ✓ |  | 54.5% |
| *Strongyloides ratti* | GCF_001040885.1 | 12,445 | 후손 | ✓ |  | 21.5% |
| *Taphrina deformans* | GCA_000312925.2 | 4,653 | 후손 | ✓ |  | 49.5% |
| *Tetrahymena thermophila* | GCF_000189635.1 | 26,996 | 조상 대리 | ✓ | ✓ | 22.5% |
| *Thalassiosira pseudonana* | GCF_000149405.2 | 11,669 | 조상 대리 | ✓ | ✓ | 47.0% |
| *Theileria annulata* | GCF_000003225.4 | 3,795 | 후손 | ✓ |  | 32.5% |
| *Theileria parva* | GCF_000165365.1 | 3,964 | 후손 | ✓ |  | 34.0% |
| *Thelohanellus kitauei* | GCA_000827895.1 | 15,020 | 후손 | ✓ |  | 31.0% |
| *Toxoplasma gondii* | GCF_000006565.2 | 8,309 | 후손 | ✓ |  | 52.5% |
| *Trichinella spiralis* | GCF_000181795.1 | 16,380 | 후손 | ✓ |  | 34.0% |
| *Trichomonas vaginalis* | GCF_026262505.1 | 72,290 | 후손 | ✓ |  | 32.5% |
| *Tritrichomonas foetus* | GCF_001839685.1 | 24,454 | 후손 | ✓ |  | 31.0% |
| *Trypanosoma brucei* | GCF_000002445.2 | 8,758 | 후손 | ✓ |  | 46.5% |
| *Trypanosoma congolense* | GCA_000227395.2 | 5,984 | 후손 | ✓ |  | 47.5% |
| *Trypanosoma cruzi* | GCF_000209065.1 | 19,607 | 후손 | ✓ |  | 51.5% |
| *Trypanosoma grayi* | GCF_000691245.1 | 10,583 | 후손 | ✓ |  | 54.0% |
| *Trypanosoma vivax* | GCA_982375215.1 | 14,454 | 후손 | ✓ |  | 54.0% |
| *Ustilago maydis* | GCF_000328475.2 | 6,762 | 후손 | ✓ |  | 54.0% |
| *Vavraia culicis* | GCF_000192795.1 | 2,773 | 후손 | ✓ |  | 39.5% |
| *Vitrella brassicaformis* | GCA_001179505.1 | 23,034 | 후손 | ✓ | ✓ | 58.0% |
| *Volvox carteri* | GCF_000143455.1 | 14,331 | 후손 | ✓ | ✓ | 56.0% |

## 세균·고세균 (70종)

| 종 | 어셈블리 | 유전자 | 역할 | 조성 | 맥락 | GC |
|---|---|---|---|---|---|---|
| *Acinetobacter baylyi* | GCF_000046845.1 | 3,168 | 조상 대리 | ✓ | ✓ | 40.5% |
| *Alteromonas macleodii* | GCF_050500325.1 | 3,785 | 조상 대리 | ✓ | ✓ | 44.5% |
| *Bacillus licheniformis* | GCF_034478925.1 | 4,097 | 후손 | ✓ | ✓ | 46.0% |
| *Bacillus pumilus* | GCF_000017885.4 | 3,566 | 후손 | ✓ | ✓ | 41.5% |
| *Bacillus subtilis* | GCF_000009045.1 | 4,231 | 조상 대리 | ✓ | ✓ | 43.5% |
| *Burkholderia pseudomallei* | GCF_030297255.1 | 5,925 | — (기후 대상) | ✓ | ✓ | 68.0% |
| *Candidatus Pelagibacter ubique* | GCF_000012345.1 | 1,341 | 후손 | ✓ | ✓ | 29.5% |
| *Cereibacter sphaeroides* | GCF_003324715.1 | 4,250 | 조상 대리 | ✓ | ✓ | 69.0% |
| *Chromohalobacter salexigens* | GCF_000055785.1 | 3,278 | 후손 | ✓ | ✓ | 64.0% |
| *Chroococcidiopsis thermalis* | GCF_000317125.1 | 5,907 | 후손 | ✓ | ✓ | 44.5% |
| *Clostridium acetobutylicum* | GCF_000218855.1 | 3,789 | 후손 | ✓ | ✓ | 31.0% |
| *Colwellia psychrerythraea* | GCF_000012325.1 | 4,343 | 후손 | ✓ | ✓ | 38.0% |
| *Cupriavidus necator* | GCF_000219215.1 | 7,339 | 조상 대리 | ✓ | ✓ | 65.5% |
| *Deinococcus deserti* | GCF_000020685.1 | 3,458 | 후손 | ✓ | ✓ | 63.0% |
| *Deinococcus geothermalis* | GCF_000196275.1 | 2,988 | 후손 | ✓ | ✓ | 66.5% |
| *Deinococcus radiodurans* | GCF_020546685.1 | 3,088 | 후손 | ✓ | ✓ | 66.5% |
| *Desulfotalea psychrophila* | GCF_000025945.1 | 3,054 | 후손 | ✓ | ✓ | 46.5% |
| *Desulfuromonas acetoxidans* | GCF_000167355.1 | 3,213 | 후손 | ✓ | ✓ | 52.0% |
| *Flavobacterium johnsoniae* | GCF_000016645.1 | 5,074 | 조상 대리 | ✓ | ✓ | 34.0% |
| *Geobacillus kaustophilus* | GCF_000009785.1 | 3,324 | 후손 | ✓ | ✓ | 52.0% |
| *Geobacter metallireducens* | GCF_000012925.1 | 3,457 | 후손 | ✓ | ✓ | 59.5% |
| *Geobacter sulfurreducens* | GCF_000007985.2 | 3,330 | 후손 | ✓ | ✓ | 61.0% |
| *Haloarcula marismortui* | GCF_000011085.1 | 4,182 | 후손 | ✓ | ✓ | 61.0% |
| *Halobacillus halophilus* | GCF_000284515.1 | 3,925 | 후손 | ✓ | ✓ | 42.0% |
| *Halobacterium salinarum* | GCF_004799605.1 | 2,415 | 후손 | ✓ | ✓ | 66.5% |
| *Haloferax volcanii* | GCF_000025685.1 | 3,823 | 후손 | ✓ | ✓ | 65.5% |
| *Halomonas elongata* | GCF_000196875.2 | 3,664 | 후손 | ✓ | ✓ | 63.5% |
| *Hymenobacter swuensis* | GCF_000576555.1 | 4,411 | 후손 | ✓ | ✓ | 59.5% |
| *Kineococcus radiotolerans* | GCF_000017305.1 | 4,622 | 후손 | ✓ | ✓ | 74.0% |
| *Lactiplantibacillus plantarum* | GCF_009913655.1 | 2,874 | 후손 | ✓ | ✓ | 44.5% |
| *Legionella pneumophila* | GCF_001941585.1 | 2,942 | — (기후 대상) | ✓ | ✓ | 38.5% |
| *Methanocaldococcus jannaschii* | GCF_000091665.1 | 1,792 | 후손 | ✓ | ✓ | 31.5% |
| *Methanococcoides burtonii* | GCF_000013725.1 | 2,415 | 후손 | ✓ | ✓ | 41.0% |
| *Methanococcus maripaludis* | GCF_002945325.1 | 1,797 | 조상 대리 | ✓ | ✓ | 33.0% |
| *Methanosarcina acetivorans* | GCF_000007345.1 | 4,525 | 조상 대리 | ✓ | ✓ | 42.5% |
| *Methylobacterium radiotolerans* | GCF_000019725.1 | 6,315 | 후손 | ✓ | ✓ | 71.0% |
| *Methylorubrum extorquens* | GCF_000083545.1 | 5,427 | 조상 대리 | ✓ | ✓ | 68.0% |
| *Micrococcus luteus* | GCF_900475555.1 | 2,194 | 조상 대리 | ✓ | ✓ | 73.0% |
| *Myxococcus xanthus* | GCF_000012685.1 | 7,138 | 조상 대리 | ✓ | ✓ | 69.0% |
| *Natronomonas pharaonis* | GCF_000026045.1 | 2,738 | 후손 | ✓ | ✓ | 63.0% |
| *Nitratidesulfovibrio vulgaris* | GCF_000015485.1 | 3,037 | 조상 대리 | ✓ | ✓ | 63.0% |
| *Nitrosopumilus maritimus* | GCF_000018465.1 | 1,919 | 후손 | ✓ | ✓ | 34.0% |
| *Nitrososphaera viennensis* | GCF_000698785.1 | 2,900 | 조상 대리 | ✓ | ✓ | 52.5% |
| *Photobacterium profundum* | GCF_000153425.1 | 5,168 | 후손 | ✓ | ✓ | 41.5% |
| *Planococcus halocryophilus* | GCF_001687585.2 | 3,216 | 후손 | ✓ | ✓ | 40.0% |
| *Polynucleobacter asymbioticus* | GCF_000016345.1 | 2,096 | 후손 | ✓ | ✓ | 45.0% |
| *Prochlorococcus marinus* | GCF_000015665.1 | 1,855 | 후손 | ✓ | ✓ | 31.0% |
| *Pseudoalteromonas haloplanktis* | GCF_945859885.1 | 3,466 | 후손 | ✓ | ✓ | 40.0% |
| *Pseudomonas aeruginosa* | GCF_000006765.1 | 5,571 | 조상 대리 | ✓ | ✓ | 66.5% |
| *Pseudomonas putida* | GCF_000412675.1 | 5,263 | 후손 | ✓ | ✓ | 62.5% |
| *Psychrobacter arcticus* | GCF_000012305.1 | 2,121 | 후손 | ✓ | ✓ | 43.0% |
| *Psychroflexus torquis* | GCF_000153485.2 | 3,521 | 후손 | ✓ | ✓ | 34.5% |
| *Rhodothermus marinus* | GCF_000024845.1 | 2,888 | 조상 대리 | ✓ | ✓ | 64.5% |
| *Rubrobacter xylanophilus* | GCF_019448335.1 | 3,074 | 후손 | ✓ | ✓ | 68.5% |
| *Salinibacter ruber* | GCF_003491405.1 | 3,214 | 후손 | ✓ | ✓ | 65.5% |
| *Shewanella frigidimarina* | GCF_000014705.1 | 3,938 | 후손 | ✓ | ✓ | 41.5% |
| *Shewanella oneidensis* | GCF_000146165.2 | 4,171 | 조상 대리 | ✓ | ✓ | 46.0% |
| *Sphingobium japonicum* | GCF_000091125.1 | 4,057 | 조상 대리 | ✓ | ✓ | 65.0% |
| *Sphingopyxis alaskensis* | GCF_000013985.1 | 3,184 | 후손 | ✓ | ✓ | 65.5% |
| *Synechococcus elongatus* | GCF_022984195.1 | 2,691 | 조상 대리 | ✓ | ✓ | 55.5% |
| *Synechococcus sp. WH 8102* | GCF_000195975.1 | 2,610 | 후손 | ✓ | ✓ | 59.5% |
| *Synechocystis sp. PCC 6803* | GCF_000009725.1 | 3,521 | 조상 대리 | ✓ | ✓ | 47.5% |
| *Thermococcus gammatolerans* | GCF_000022365.1 | 2,142 | 후손 | ✓ | ✓ | 53.5% |
| *Thermococcus kodakarensis* | GCF_000009965.1 | 2,260 | 조상 대리 | ✓ | ✓ | 52.0% |
| *Thermus thermophilus* | GCF_000091545.1 | 2,132 | 조상 대리 | ✓ | ✓ | 69.5% |
| *Truepera radiovictrix* | GCF_000092425.1 | 2,921 | 후손 | ✓ | ✓ | 68.0% |
| *Vibrio cholerae* | GCF_008369605.1 | 3,563 | — (기후 대상) | ✓ | ✓ | 47.5% |
| *Vibrio natriegens* | GCF_001456255.1 | 4,411 | 조상 대리 | ✓ | ✓ | 45.0% |
| *Vibrio parahaemolyticus* | GCF_000196095.1 | 4,401 | — (기후 대상) | ✓ | ✓ | 45.5% |
| *Vibrio vulnificus* | GCF_002224265.1 | 4,118 | — (기후 대상) | ✓ | ✓ | 46.5% |

## 소기관·공생세균 (GenBank 레코드)

| 시스템 | 생물 | 레코드 |
|---|---|---|
| mitochondrion | *Acanthamoeba castellanii* | NC_001637.1 |
| mitochondrion | *Allomyces macrogynus* | NC_001715.1 |
| mitochondrion | *Andalucia godoyi* | NC_021124.1 |
| mitochondrion | *Arabidopsis thaliana* | NC_037304.1 |
| mitochondrion | *Caenorhabditis elegans* | NC_001328.1 |
| mitochondrion | *Chlamydomonas reinhardtii* | NC_001638.1 |
| mitochondrion | *Chondrus crispus* | NC_001677.2 |
| mitochondrion | *Cyanidioschyzon merolae* | NC_000887.3 |
| mitochondrion | *Danio rerio* | NC_002333.2 |
| mitochondrion | *Dictyostelium discoideum* | NC_000895.1 |
| mitochondrion | *Drosophila melanogaster* | NC_024511.2 |
| mitochondrion | *Gallus gallus* | NC_053523.1 |
| mitochondrion | *Homo sapiens* | NC_012920.1 |
| mitochondrion | *Jakoba libera* | NC_021127.1 |
| mitochondrion | *Marchantia polymorpha subsp. ruderalis* | NC_037508.1 |
| mitochondrion | *Metridium senile* | NC_000933.1 |
| mitochondrion | *Monosiga brevicollis* | NC_004309.1 |
| mitochondrion | *Mus musculus* | NC_005089.1 |
| mitochondrion | *Nephroselmis olivacea* | NC_008239.1 |
| mitochondrion | *Neurospora crassa OR74A* | NC_026614.1 |
| mitochondrion | *Physcomitrium patens* | NC_007945.1 |
| mitochondrion | *Phytophthora infestans* | NC_002387.1 |
| mitochondrion | *Plasmodium falciparum* | NC_037526.1 |
| mitochondrion | *Prototheca wickerhamii* | NC_001613.1 |
| mitochondrion | *Reclinomonas americana* | NC_001823.1 |
| mitochondrion | *Saccharomyces cerevisiae S288C* | NC_001224.1 |
| mitochondrion | *Schizosaccharomyces pombe* | NC_088682.1 |
| mitochondrion | *Tetrahymena thermophila* | NC_003029.1 |
| mitochondrion | *Thalassiosira pseudonana* | NC_007405.1 |
| mitochondrion | *Trichoplax adhaerens* | NC_008151.3 |
| plastid | *Amborella trichopoda* | NC_005086.1 |
| plastid | *Arabidopsis thaliana* | NC_000932.1 |
| plastid | *Chlamydomonas reinhardtii* | NC_005353.1 |
| plastid | *Cyanidioschyzon merolae strain 10D* | NC_004799.1 |
| plastid | *Cyanophora paradoxa* | NC_001675.1 |
| plastid | *Emiliania huxleyi* | NC_007288.1 |
| plastid | *Epifagus virginiana* | NC_001568.1 |
| plastid | *Euglena gracilis* | NC_001603.2 |
| plastid | *Guillardia theta* | NC_000926.1 |
| plastid | *Marchantia polymorpha* | NC_042505.1 |
| plastid | *Mesostigma viride* | NC_002186.1 |
| plastid | *Nephroselmis olivacea* | NC_000927.1 |
| plastid | *Nicotiana tabacum* | NC_001879.2 |
| plastid | *Oryza sativa Japonica Group* | NC_001320.1 |
| plastid | *Paulinella chromatophora* | NC_011087.1 |
| plastid | *Phaeodactylum tricornutum* | NC_008588.1 |
| plastid | *Physcomitrium patens* | NC_037465.1 |
| plastid | *Plasmodium falciparum 3D7* | NC_036769.1 |
| plastid | *Porphyra purpurea* | NC_000925.1 |
| plastid | *Thalassiosira pseudonana* | NC_008589.1 |
| plastid | *Toxoplasma gondii RH* | NC_001799.1 |
| insect_endosymbiont | *Candidatus Palibaumannia cicadellinicola* | NZ_CP008985.1 |
| insect_endosymbiont | *Candidatus Blochmanniella floridana* | BX248583.1 |
| insect_endosymbiont | *Candidatus Blochmanniella pennsylvanica* | NZ_CP095401.1 |
| insect_endosymbiont | *Buchnera aphidicola str. Bp (Baizongia pistaciae)* | AE016826.1 |
| insect_endosymbiont | *Buchnera aphidicola (Cinara tujafilina)* | CP001817.1 |
| insect_endosymbiont | *Buchnera aphidicola (Schizaphis graminum)* | NZ_CP029205.1 |
| insect_endosymbiont | *Buchnera aphidicola str. APS (Acyrthosiphon pisum)* | NZ_AP036055.1 |
| insect_endosymbiont | *Escherichia coli str. K-12 substr. MG1655* | NC_000913.3 |
| insect_endosymbiont | *Candidatus Hamiltonella defensa (Bemisia tabaci)* | NZ_CP016303.1 |
| insect_endosymbiont | *Candidatus Moranella endobia PCIT* | CP002243.1 |
| insect_endosymbiont | *Candidatus Riesia pediculicola* | NZ_CP062474.1 |
| insect_endosymbiont | *Serratia symbiotica* | NZ_CP050855.1 |
| insect_endosymbiont | *Sodalis glossinidius str. 'morsitans'* | AP008232.1 |
| insect_endosymbiont | *Wigglesworthia glossinidia endosymbiont of Glossina morsitans morsitans (Yale colony)* | CP003315.1 |

## Large-scale public layer (October 2026)

| 데이터 | 출처 | 규모 | 위치 |
|---|---|---|---|
| 세균·고세균 형질 | Madin 외 2020 (CC BY 4.0) | 14,893종 | `data/traits/` |
| GTDB 대표 유전체 형질(분류, GC, 크기, 코딩 밀도, CheckM2) | GTDB 2026년 4월판 | 199,923종 (세균 189,801, 고세균 10,122; 고품질 90,959) | `data/gtdb/species_reps.tsv.gz` |
| UniProt 참조 단백질체 Pfam + 아미노산 조성 | UniProt(InterPro가 미리 계산한 Pfam) | 세균·고세균·균류 참조 단백질체 전체 | `data/uniprot/shards/` |

**UniProt Pfam과 이 프로젝트의 HMMER 프로필 비교** (같은 종 4개):

| 종 | UniProt | HMMER | 공통 | Jaccard | 복제 수 상관 |
|---|---|---|---|---|---|
| Bacillus subtilis | 2,890 | 3,136 | 2,884 | 0.92 | 0.89 |
| Saccharomyces cerevisiae | 4,214 | 4,413 | 4,210 | 0.95 | 0.94 |
| Schizosaccharomyces pombe | 3,815 | 3,910 | 3,706 | 0.92 | 0.91 |
| Escherichia coli | 3,294 | 3,625 | 3,049 | 0.79 | 0.84 |

HMMER가 유전자군을 200–600개 더 찾고(UniProt은 약한 도메인을 덜 붙임), 복제 수 중앙 비율은 1.00입니다.
대장균은 균주가 달라 일치가 낮습니다(UniProt은 K-12). **두 데이터셋은 섞지 않고** 대규모 분석에만 UniProt을 씁니다.
