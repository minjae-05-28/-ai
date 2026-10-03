---
id: proteome_traits_v1
system: 공통
status: 현역
tags:
  - 법칙
  - 공통
---
# proteome_traits_v1

> 대규모 2라운드: 단백질 조성 + Pfam 유전자군으로 처음 보는 목의 온도(오차 3.5°C, 암기 5.6), 산소(0.977, 암기 0.830), 숙주 관련(0.843, 암기 0.485)을 맞힘. 1라운드 유전체 특징으로는 암기에 지던 온도까지 이김.

**시스템**: 공통  
**상태**: 현역  
**주제**: [[대규모 유전체 형질]], [[환경과 서열]]

## 적용 범위 (원문)
Bacterial and archaeal growth temperature, oxygen use and host association predicted from proteome amino-acid composition and Pfam family content (UniProt reference proteomes), across species with a trait record.

## 모델
Ridge / logistic regression on standardized composition and Pfam presence; taxonomy memorisation and the mean as baselines; random folds and leave-order-out.

## 검증
- temperature:
  - random_5fold: `{"n": 7253, "n_orders": 180, "metric": "MAE (deg C)", "scores": {"mean": 6.1513, "taxonomy": 2.5764, "composition": 4.3874, "pfam": 2.6846, "composition+pfam": `
  - leave_order_out: `{"n": 7253, "n_orders": 180, "metric": "MAE (deg C)", "scores": {"mean": 6.1993, "taxonomy": 5.5922, "composition": 5.0001, "pfam": 3.6522, "composition+pfam": `
  - composition_coefficients: `{"ivywrel": 5.645, "cvp": 1.6434, "acidic_excess": 0.5287, "n_side": -1.7241, "gravy": 0.3352, "fymink": 0.4681, "median_pi": 3.2292}`
  - pfam_top: `{"positive": [["zf_Rg", "Reverse gyrase zinc finger", 0.604], ["SDH_protease", "ClpP-like SDH-type serine proteinase", 0.573], ["Endonuclease_5", "Endonuclease `
- oxygen:
  - random_5fold: `{"n": 5363, "n_orders": 177, "metric": "AUROC", "scores": {"mean": 0.5, "taxonomy": 0.9698, "composition": 0.949, "pfam": 0.9831, "composition+pfam": 0.9845}}`
  - leave_order_out: `{"n": 5363, "n_orders": 177, "metric": "AUROC", "scores": {"mean": 0.5, "taxonomy": 0.8297, "composition": 0.9232, "pfam": 0.9776, "composition+pfam": 0.9773}, `
  - composition_coefficients: `{"ivywrel": -0.0498, "cvp": -1.5399, "acidic_excess": 0.8501, "n_side": 0.2958, "gravy": -0.1422, "fymink": -1.5993, "median_pi": 0.6366}`
  - pfam_top: `{"positive": [["Ribonuc_red_sm", "Ribonucleotide reductase, small chain", 0.225], ["Cu-oxidase_3", "Multicopper oxidase", 0.206], ["Cu-oxidase_2", "Multicopper `
- host:
  - random_5fold: `{"n": 5851, "n_orders": 180, "metric": "AUROC", "scores": {"mean": 0.5, "taxonomy": 0.8476, "composition": 0.755, "pfam": 0.8922, "composition+pfam": 0.8925}}`
  - leave_order_out: `{"n": 5851, "n_orders": 180, "metric": "AUROC", "scores": {"mean": 0.5, "taxonomy": 0.4849, "composition": 0.6739, "pfam": 0.8405, "composition+pfam": 0.8431}, `
  - composition_coefficients: `{"ivywrel": -0.5374, "cvp": -0.0257, "acidic_excess": -0.6257, "n_side": 0.4517, "gravy": 0.2499, "fymink": 1.1267, "median_pi": -0.7037}`
  - pfam_top: `{"positive": [["PDZ", "PDZ domain", 0.161], ["Acetyltransf_4", "Acetyltransferase (GNAT) domain", 0.147], ["YadA_head", "YadA head domain repeat (2 copies)", 0.`

## 한계
- UniProt Pfam counts every protein entry and uses InterPro's Pfam release; it is a separate dataset from the HMMER profiles and is not mixed with them.
- Species are matched by name; strain-level differences are ignored.
- Traits are literature compilations, not measurements made here.
- Pfam coefficients are associations within a regularised model; a family can stand in for its lineage, which is why leave-order-out is reported next to random folds.

원본: `laws/proteome_traits_v1.json`