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
  - mean_auroc: `{"copies_only": 0.6172579176865324, "memorisation": 0.849235234515775, "law_base": 0.8132686604717007, "law_context": 0.8178732595435612, "combined_s1": 0.85969`
  - context_gain: `{"mean": 0.004604599071860593, "n_better": 40, "n": 54}`
  - context_weights: `{"ctx:expression": -0.3241, "ctx:multi_domain": 0.0152, "ctx:partners": 0.0052, "ctx:operon": -0.0959, "ctx:neighbourhood": -0.112, "ctx:has_context": 0.0247}`
- parasites:
  - mean_auroc: `{"copies_only": 0.6466693047031259, "memorisation": 0.7882956723635105, "law_base": 0.7597640843822151, "law_context": 0.7653708430517742, "combined_s1": 0.7930`
  - context_gain: `{"mean": 0.005606758669558888, "n_better": 77, "n": 90}`
  - context_weights: `{"ctx:expression": -0.0447, "ctx:multi_domain": 0.0078, "ctx:partners": -0.0078, "ctx:exons": -0.127, "ctx:has_context": 0.075}`

## 한계
- Context features are family averages over the species that carry the family.
- Codon adaptation is a proxy for expression, weaker in eukaryotes.
- combined_sN uses memorisation; it is a forecasting tool, not a law.

원본: `laws/context_features_v1.json`