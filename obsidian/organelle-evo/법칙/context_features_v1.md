---
id: context_features_v1
system: 공통
status: 현역
tags:
  - 법칙
  - 공통
---
# context_features_v1

> 유전자 맥락 특성(코돈으로 추정한 발현량, 오페론, 도메인 짝, 엑손)을 더함: 법칙 +0.005. 많이 발현되는 유전자가 남는다(가중치 −0.31). 법칙과 암기를 섞은 점수는 기생 0.814, 극한 0.860.

**시스템**: 공통  
**상태**: 현역  
**주제**: [[유전자 소실 성향]], [[녹아웃과 발현]]

## 적용 범위 (원문)
Gene-family loss law with context features (codon-usage expression, domain partners, operons, exons) for parasitic eukaryotes and extremophile bacteria/archaea; memorisation kept as a separate score.

## 모델
Linear birth-death law on enriched + context family features; memorisation and a shrunk combination reported side by side, never mixed into the law.

## 검증
- extremophiles:
  - mean_auroc: `{"copies_only": 0.6199392920234301, "memorisation": 0.8439985034182216, "law_base": 0.8191445774072861, "law_context": 0.8232006566776416, "combined_s1": 0.8580`
  - context_gain: `{"mean": 0.00405607927035582, "n_better": 29, "n": 40}`
  - context_weights: `{"ctx:expression": -0.3082, "ctx:multi_domain": -0.0083, "ctx:partners": 0.0229, "ctx:operon": -0.0918, "ctx:neighbourhood": -0.1104, "ctx:has_context": 0.0459}`
- parasites:
  - mean_auroc: `{"copies_only": 0.6438921622472106, "memorisation": 0.797798715194633, "law_base": 0.7606546179344121, "law_context": 0.766020699300282, "combined_s1": 0.802494`
  - context_gain: `{"mean": 0.0053660813658698535, "n_better": 71, "n": 79}`
  - context_weights: `{"ctx:expression": -0.0386, "ctx:multi_domain": 0.0034, "ctx:partners": -0.0063, "ctx:exons": -0.1457, "ctx:has_context": 0.1102}`

## 한계
- Context features are family averages over the species that carry the family.
- Codon adaptation is a proxy for expression, weaker in eukaryotes.
- combined_sN uses memorisation; it is a forecasting tool, not a law.

원본: `laws/context_features_v1.json`