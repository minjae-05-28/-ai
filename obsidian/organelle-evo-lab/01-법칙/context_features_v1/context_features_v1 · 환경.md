---
유형: 환경
법칙: context_features_v1
클러스터: 기생·극한
tags:
  - 법칙/context_features_v1
  - 클러스터/기생·극한
  - 판정/음성
  - 유형/환경
---

# context_features_v1 · 환경

← [[context_features_v1]]

**카탈로그** — · **종 수** —

## 요약 수치

```json
{
 "extremophiles": {
  "mean_auroc": {
   "copies_only": 0.6172579176865324,
   "memorisation": 0.849235234515775,
   "law_base": 0.8132686604717007,
   "law_context": 0.8178732595435612,
   "combined_s1": 0.8596954810622316,
   "combined_s3": 0.8615463752219165,
   "combined_s10": 0.8606810305907693
  },
  "context_weights": {
   "ctx:expression": -0.3241,
   "ctx:multi_domain": 0.0152,
   "ctx:partners": 0.0052,
   "ctx:operon": -0.0959,
   "ctx:neighbourhood": -0.112,
   "ctx:has_context": 0.0247
  }
 },
 "parasites": {
  "mean_auroc": {
   "copies_only": 0.6466693047031259,
   "memorisation": 0.7882956723635105,
   "law_base": 0.7597640843822151,
   "law_context": 0.7653708430517742,
   "combined_s1": 0.7930777139503002,
   "combined_s3": 0.7983505889489837,
   "combined_s10": 0.804083652911769
  },
  "context_weights": {
   "ctx:expression": -0.0447,
   "ctx:multi_domain": 0.0078,
   "ctx:partners": -0.0078,
   "ctx:exons": -0.127,
   "ctx:has_context": 0.075
  }
 }
}
```

> [!note]
> envelope 밖의 환경에 이 법칙을 쓰면 외삽이다. 값은 문헌 근사치(카탈로그 주석 참조).
