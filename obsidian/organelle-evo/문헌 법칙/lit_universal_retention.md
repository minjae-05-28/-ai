---
id: lit_universal_retention
verdict: partly
tags:
  - 문헌법칙
---
# lit_universal_retention

> The same gene features (hydrophobicity, pKa, GC) predict retention in mitochondria and plastids; a model trained on one predicts the other.

**출처**: [Giannakis et al. 2022, Cell Systems](https://wrap.warwick.ac.uk/id/eprint/169973/)  
**우리 데이터 판정**: partly

## 우리 데이터로 다시 시험한 결과
Retention-rate model trained on mitochondria ranks plastid genes with Spearman 0.43 (plastid-trained, leave-one-gene-out: 0.50); plastid->mitochondria 0.36 (within 0.55). A shared component transfers, and system-specific laws fit better (endosymbiosis_v1, delta AIC 787).

## 관련 법칙
- [[endosymbiosis_v1]]