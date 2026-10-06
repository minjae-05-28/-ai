---
유형: 실험
실행: hgt_limit
산출: results/hgt_limit/summary.json
tags:
  - 유형/실험
  - 실험/hgt_limit
---

# 실험 · hgt_limit

**산출물** `results/hgt_limit/summary.json`

## 한눈에

| 항목 | 값 |
| --- | --- |
| reps | 2 |
| families | 500 |
| note | hgt is the per-unit-branch-length arrival rate used by mito_model_search.simulate; the GTDB alphaproteobacterial subtree has branch lengths with a median of 0.009 and a maximum of 0.70, so the arrival probability on a branch is about hgt x length x 10. |
| calibration_breaks_at_hgt | 0.5 |
| ranking_breaks_at_hgt | 0.8 |

## model

```json
{
 "ratio": null,
 "root": "stationary",
 "min_busco": 97,
 "drop_mag": false,
 "mult": 14.0,
 "tip_mult": 1.0
}
```

## levels

```json
[
 {
  "true_share": 0.492,
  "recon_auroc": 0.994831035340108,
  "freq_auroc": 0.9876632719878689,
  "recon_logloss": 0.12531724646454678,
  "freq_logloss": 0.29947625132171635,
  "prior_logloss": 0.6927310736542824,
  "recon_size_bias": -0.0814954121907552,
  "freq_size_bias": -0.27833800721632984,
  "hgt": 0.0,
  "recon_beats_freq_auroc": true,
  "recon_beats_freq_logloss": true,
  "recon_beats_prior_logloss": true
 },
 {
  "true_share": 0.495,
  "recon_auroc": 0.9863675616025229,
  "freq_auroc": 0.9500621681571539,
  "recon_logloss": 0.15524517223817383,
  "freq_logloss": 0.32617177304932077,
  "prior_logloss": 0.6927591078086941,
  "recon_size_bias": -0.07369798181743013,
  "freq_size_bias": -0.18089667442765212,
  "hgt": 0.02,
  "recon_beats_freq_auroc": true,
  "recon_beats_freq_logloss": true,
  "recon_beats_prior_logloss": true
 },
 {
  "true_share": 0.508,
  "recon_auroc": 0.9816001781721742,
  "freq_auroc": 0.9171744511007274,
  "recon_logloss": 0.1730351359208871,
  "freq_logloss": 0.3658342101811598,
  "prior_logloss": 0.6926270234041647,
  "recon_size_bias": -0.03660402083915784,
  "freq_size_bias": -0.06862134268682815,
  "hgt": 0.05,
  "recon_beats_freq_auroc": true,
  "recon_beats_freq_logloss": true,
  "recon_beats_prior_logloss": true
 },
 {
  "true_share": 0.525,
  "recon_auroc": 0.9688316389357675,
  "freq_auroc": 0.885539742467035,
  "recon_logloss": 0.22445253582785518,
  "freq_logloss": 0.42599267106617505,
  "prior_logloss": 0.691445462841439,
  "recon_size_bias": 0.04438260479430488,
  "freq_size_bias": 0.07695424437215567,
  "hgt": 0.1,
  "recon_beats_freq_auroc": true,
  "recon_beats_freq_logloss": true,
  "recon_beats_prior_logloss": true
 },
 {
  "true_share": 0.574,
  "recon_auroc": 0.915501745894034,
  "freq_auroc": 0.8037007693233129,
  "recon_logloss": 0.4013004969681497,
  "freq_logloss": 0.5816307471969161,
  "prior_logloss": 0.682122126970236,
  "recon_size_bias": 0.1675937142896354,
  "freq_size_bias": 0.21990968695100482,
  "hgt": 0.2,
  "recon_beats_freq_auroc": true,
  "recon_beats_freq_logloss": true,
  "recon_beats_prior_logloss": true
 },
 {
  "true_share": 0.626,
  "recon_auroc": 0.8371205553824332,
  "freq_auroc": 0.7298268528087399,
  "recon_logloss": 0.6203726438345329,
  "freq_logloss": 0.7003966535724,
  "prior_logloss": 0.6609733935996324,
  "recon_size_bias": 0.28765608856462854,
  "freq_size_bias": 0.27665991169444193,
  "hgt": 0.35,
  "recon_beats_freq_auroc": true,
  "recon_beats_freq_logloss": true,
  "recon_beats_prior_logloss": true
 },
 {
  "true_share": 0.695,
  "recon_auroc": 0.7420260402057036,
  "freq_auroc": 0.6484957323181727,
  "recon_logloss": 0.7013464822474926,
  "freq_logloss": 0.7339917660386996,
  "prior_logloss": 0.6149824832402402,
  "recon_size_bias": 0.2502764715664629,
  "freq_size_bias": 0.23067506969312251,
  "hgt": 0.5,
  "recon_beats_freq_auroc": true,
  "recon_beats_freq_logloss": true,
  "recon_beats_prior_logloss": false
 },
 {
  "true_share": 0.849,
  "recon_auroc": 0.6033944237753919,
  "freq_auroc": 0.5436849520349771,
  "recon_logloss": 0.5048695658489305,
  "freq_logloss": 0.5028984294524568,
  "prior_logloss": 0.423310577326395,
  "recon_size_bias": 0.08968062027243193,
  "freq_size_bias": 0.0739729622353079,
  "hgt": 0.8,
  "recon_beats_freq_auroc": true,
  "recon_beats_freq_logloss": false,
  "recon_beats_prior_logloss": false
 }
]
```

## 연결
- [[실험 목록]]
