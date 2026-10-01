---
id: lit_ivywrel_temperature
verdict: consistent (correlation weaker than the published 0.93)
tags:
  - 문헌법칙
---
# lit_ivywrel_temperature

> The proteome share of I, V, Y, W, R, E, L rises linearly with optimal growth temperature.

**출처**: [Zeldovich, Berezovsky & Shakhnovich 2007, PLoS Computational Biology](https://journals.plos.org/ploscompbiol/article?id=10.1371/journal.pcbi.0030005)  
**우리 데이터 판정**: consistent (correlation weaker than the published 0.93)

## 우리 데이터로 다시 시험한 결과
70 bacteria and archaea: Pearson 0.82 (Spearman 0.57); +0.01 IVYWREL = +6.4 C. Predicting a held-out group's temperature from IVYWREL alone: RMSE 9.8 C vs 15.5 C for the mean; a 20-amino-acid ridge model does worse (11.3 C).

## 관련 법칙
- [[sequence_v1]]