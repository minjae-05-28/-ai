# 법칙 저장소

학습된 진화 법칙을 버전별로 고정해 둔 곳입니다. 각 파일에는 계수와 95% 신뢰구간, 모델 식, 데이터 출처, 그리고 **적용 범위(scope)**가 함께 기록되어 있습니다.

| id | 적용 범위 | 데이터 |
|---|---|---|
| `endosymbiosis_v1` | 의무적 내공생에서의 유전체 축소(소기관, 곤충 내공생세균). 자유생활 생물과 유전자 획득에는 적용 불가 | 실제 유전체 64개 |
| `eukaryote_axes_v1` | 진핵생물 유전자군 소실·복제를 기본 법칙 + 기생 / 세포 안 / 미토콘드리아 퇴화 효과의 합으로 표현 | 진핵생물 32종, 22쌍 |
| `eukaryote_lifestyle_v1` | 진핵생물 유전자군(Pfam)의 복제와 소실. 자유생활 계통과 기생으로 전환한 계통 각각 | 진핵생물 23종, 14쌍 |

이후 분석은 이 법칙들을 **학습에 섞지 않고**, 비교 대상이나 기준 예측기로만 사용합니다. 불러오기:

```python
from organelle_evo.laws import load_law
law = load_law("endosymbiosis_v1")
law.weights["mitochondrion"], law.ci95["mitochondrion"], law.scope
```
