---
유형: 환경
법칙: environment_v3
클러스터: 기생·극한
tags:
  - 법칙/environment_v3
  - 클러스터/기생·극한
  - 판정/음성
  - 유형/환경
---

# environment_v3 · 환경

← [[environment_v3]]

**카탈로그** prokaryotes · **종 수** 81

## 환경 범위

```json
{
 "최적 온도 °C": {
  "min": 5,
  "median": 30,
  "max": 100,
  "n": 81
 },
 "최적 NaCl %": {
  "min": 0,
  "median": 1,
  "max": 25,
  "n": 81
 },
 "산소 호흡(1)": {
  "1": 59,
  "0": 22
 },
 "방사선 내성(1)": {
  "0": 69,
  "1": 12
 },
 "빈영양(1)": {
  "0": 74,
  "1": 7
 }
}
```

## 분류군 구성

```json
{
 "archaea": 16,
 "gamma": 14,
 "firmicutes": 11,
 "cyano": 7,
 "bacteroidetes": 6,
 "alpha": 6,
 "deinococcus": 6,
 "delta": 6,
 "beta": 4,
 "actino": 3,
 "thermotogae": 2
}
```

## GC 함량

```json
{
 "min": 0.295,
 "median": 0.475,
 "max": 0.74,
 "n": 81
}
```

## 축별 대비

```json
{
 "colder": {
  "pairs_changed": 31,
  "change_range": [
   -1.6,
   1.33
  ]
 },
 "saltier": {
  "pairs_changed": 20,
  "change_range": [
   -0.05,
   2.3
  ]
 },
 "anaerobic": {
  "pairs_changed": 10,
  "change_range": [
   -1.0,
   1.0
  ]
 },
 "radiation_resistant": {
  "pairs_changed": 12,
  "change_range": [
   0.0,
   1.0
  ]
 },
 "oligotrophic": {
  "pairs_changed": 7,
  "change_range": [
   0.0,
   1.0
  ]
 },
 "scale": "colder: (relative - descendant temperature)/30.0 C; saltier: change in NaCl/10.0%; others -1/0/1",
 "control_pairs": 3
}
```

## 요약 수치

```json
{
 "loss_colder": [
  {
   "feature": "go:organelle",
   "weight": 1.3534,
   "direction": "더 잘 사라짐"
  },
  {
   "feature": "kw:cilium_flagellum",
   "weight": 0.5141,
   "direction": "더 잘 사라짐"
  },
  {
   "feature": "go:structural molecule activity",
   "weight": -0.4484,
   "direction": "덜 사라짐"
  },
  {
   "feature": "kw:ubiquitin_system",
   "weight": -0.4131,
   "direction": "덜 사라짐"
  },
  {
   "feature": "go:isomerase activity",
   "weight": -0.3967,
   "direction": "덜 사라짐"
  },
  {
   "feature": "go:lyase activity",
   "weight": -0.3463,
   "direction": "덜 사라짐"
  }
 ],
 "loss_saltier": [
  {
   "feature": "protein_targeting",
   "weight": -0.5543,
   "direction": "덜 사라짐"
  },
  {
   "feature": "kw:ubiquitin_system",
   "weight": 0.4569,
   "direction": "더 잘 사라짐"
  },
  {
   "feature": "transcription",
   "weight": 0.4059,
   "direction": "더 잘 사라짐"
  },
  {
   "feature": "go:ribosome",
   "weight": 0.3098,
   "direction": "더 잘 사라짐"
  },
  {
   "feature": "kw:zinc_finger",
   "weight": 0.2595,
   "direction": "더 잘 사라짐"
  },
  {
   "feature": "kw:cytoskeleton_motor",
   "weight": 0.2183,
   "direction": "더 잘 사라짐"
  }
 ],
 "loss_anaerobic": [
  {
   "feature": "transcription",
   "weight": 0.9126,
   "direction": "더 잘 사라짐"
  },
  {
   "feature": "go:ribosome",
   "weight": 0.7286,
   "direction": "더 잘 사라짐"
  },
  {
   "feature": "atp_synthase",
   "weight": -0.7199,
   "direction": "덜 사라짐"
  },
  {
   "feature": "kw:cilium_flagellum",
   "weight": 0.6877,
   "direction": "더 잘 사라짐"
  },
  {
   "feature": "kw:gtpase_signalling",
   "weight": -0.5638,
   "direction": "덜 사라짐"
  },
  {
   "feature": "go:carbohydrate metabolic process",
   "weight": -0.5136,
   "direction": "덜 사라짐"
  }
 ],
 "loss_radiation_resistant": [
  {
   "feature": "kw:ubiquitin_system",
   "weight": 1.3243,
   "direction": "더 잘 사라짐"
  },
  {
   "feature": "go:structural molecule activity",
   "weight": -0.7268,
   "direction": "덜 사라짐"
  },
  {
   "feature": "atp_synthase",
   "weight": -0.6732,
   "direction": "덜 사라짐"
  },
  {
   "feature": "go:RNA binding",
   "weight": 0.5187,
   "direction": "더 잘 사라짐"
  },
  {
   "feature": "kw:cytoskeleton_motor",
   "weight": -0.5141,
   "direction": "덜 사라짐"
  },
  {
   "feature": "kw:gtpase_signalling",
   "weight": -0.4201,
   "direction": "덜 사라짐"
  }
 ],
 "loss_oligotrophic": [
  {
   "feature": "kw:cilium_flagellum",
   "weight": 2.2341,
   "direction": "더 잘 사라짐"
  },
  {
   "feature": "transcription",
   "weight": -1.6588,
   "direction": "덜 사라짐"
  },
  {
   "feature": "protein_targeting",
   "weight": -1.0026,
   "direction": "덜 사라짐"
  },
  {
   "feature": "go:ribosome",
   "weight": -0.7139,
   "direction": "덜 사라짐"
  },
  {
   "feature": "kw:cell_adhesion_surface",
   "weight": -0.4717,
   "direction": "덜 사라짐"
  },
  {
   "feature": "kw:amino_acid_metabolism",
   "weight": -0.3604,
   "direction": "덜 사라짐"
  }
 ],
 "duplication_colder": [
  {
   "feature": "go:ribosome",
   "weight": -0.8592,
   "direction": "덜 사라짐"
  },
  {
   "feature": "go:organelle",
   "weight": 0.8474,
   "direction": "더 잘 사라짐"
  },
  {
   "feature": "kw:ubiquitin_system",
   "weight": -0.7088,
   "direction": "덜 사라짐"
  },
  {
   "feature": "transcription",
   "weight": 0.573,
   "direction": "더 잘 사라짐"
  },
  {
   "feature": "protein_targeting",
   "weight": -0.4906,
   "direction": "덜 사라짐"
  },
  {
   "feature": "translation",
   "weight": 0.4482,
   "direction": "더 잘 사라짐"
  }
 ],
 "duplication_saltier": [
  {
   "feature": "kw:ubiquitin_system",
   "weight": -1.4251,
   "direction": "덜 사라짐"
  },
  {
   "feature": "atp_synthase",
   "weight": 0.7057,
   "direction": "더 잘 사라짐"
  },
  {
   "feature": "go:organelle",
   "weight": -0.6634,
   "direction": "덜 사라짐"
  },
  {
   "feature": "protein_targeting",
   "weight": 0.6609,
   "direction": "더 잘 사라짐"
  },
  {
   "feature": "go:catalytic activity, acting on DNA",
   "weight": -0.2771,
   "direction": "덜 사라짐"
  },
  {
   "feature": "go:RNA binding",
   "weight": -0.2446,
   "direction": "덜 사라짐"
  }
 ],
 "duplication_anaerobic": [
  {
   "feature": "go:ribosome",
   "weight": -1.599,
   "direction": "덜 사라짐"
  },
  {
   "feature": "go:structural molecule activity",
   "weight": 1.2458,
   "direction": "더 잘 사라짐"
  },
  {
   "feature": "transcription",
   "weight": -1.0695,
   "direction": "덜 사라짐"
  },
  {
   "feature": "atp_synthase",
   "weight": 0.7723,
   "direction": "더 잘 사라짐"
  },
  {
   "feature": "kw:ubiquitin_system",
   "weight": -0.5528,
   "direction": "덜 사라짐"
  },
  {
   "feature": "go:catalytic activity, acting on DNA",
   "weight": -0.5449,
   "direction": "덜 사라짐"
  }
 ],
 "duplication_radiation_resistant": [
  {
   "feature": "atp_synthase",
   "weight": -1.9728,
   "direction": "덜 사라짐"
  },
  {
   "feature": "kw:ubiquitin_system",
   "weight": 1.9314,
   "direction": "더 잘 사라짐"
  },
  {
   "feature": "protein_targeting",
   "weight": -1.0446,
   "direction": "덜 사라짐"
  },
  {
   "feature": "go:ribosome",
   "weight": -0.9475,
   "direction": "덜 사라짐"
  },
  {
   "feature": "kw:cell_adhesion_surface",
   "weight": 0.88,
   "direction": "더 잘 사라짐"
  },
  {
   "feature": "go:structural molecule activity",
   "weight": 0.865,
   "direction": "더 잘 사라짐"
  }
 ],
 "duplication_oligotrophic": [
  {
   "feature": "kw:cilium_flagellum",
   "weight": 2.6999,
   "direction": "더 잘 사라짐"
  },
  {
   "feature": "atp_synthase",
   "weight": -1.8938,
   "direction": "덜 사라짐"
  },
  {
   "feature": "kw:cell_adhesion_surface",
   "weight": -1.4538,
   "direction": "덜 사라짐"
  },
  {
   "feature": "protein_targeting",
   "weight": -1.3823,
   "direction": "덜 사라짐"
  },
  {
   "feature": "transcription",
   "weight": -0.9441,
   "direction": "덜 사라짐"
  },
  {
   "feature": "go:lyase activity",
   "weight": -0.8505,
   "direction": "덜 사라짐"
  }
 ],
 "summary": {
  "leave_one_pair_out_auroc": {
   "copies_only": 0.6172579176865324,
   "no_environment": 0.8132686604717007,
   "environment_law": 0.8141681436768096,
   "memorisation": 0.849235234515775
  },
  "환경 축 효과": 0.0008994832051090464,
  "주의": "축별 계수가 0과 구분돼도 환경 축은 처음 보는 쌍의 소실 예측을 개선하지 못함. 계수는 '이 데이터에서 이 환경일 때 이런 경향'이지 예측 규칙이 아님"
 }
}
```

> [!note]
> envelope 밖의 환경에 이 법칙을 쓰면 외삽이다. 값은 문헌 근사치(카탈로그 주석 참조).
