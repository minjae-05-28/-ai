---
유형: 법칙 허브
법칙: gc3_confound_v1
클러스터: 서열·조성
판정: 교란 검정
기준선대비: —
tags:
  - 법칙/gc3_confound_v1
  - 클러스터/서열·조성
  - 판정/교란 검정
---

# gc3_confound_v1

> [!abstract] 적용 범위
> Whether the proteome-composition laws (temperature, salt, oxygen, nutrients, symbiont AT bias) survive genome GC content as a covariate.

**모형** — Environment effect with and without GC (or change in GC) as a covariate; OLS and taxonomy rank GLS; leave-one-pair-out R^2.

## 판정 — 교란 검정

교란 변수를 넣었을 때 효과가 살아남는지를 묻는 검정입니다. 법칙 대 기준선의 경주가 아니라 '살아남음/탈락'이 결과입니다. 수치는 [[gc3_confound_v1 · 검증]]에 그대로 있습니다.

## 이 클러스터의 노트
- [[gc3_confound_v1 · 계수]] — 학습된 가중치와 신뢰구간
- [[gc3_confound_v1 · 검증]] — 기준선과 나란히 본 성적
- [[gc3_confound_v1 · 한계]] — 이 법칙을 깨뜨리는 조건
- [[gc3_confound_v1 · 환경]] — 어떤 환경의 종들에서 나왔나
- [[gc3_confound_v1 · 데이터]] — 쓰인 종·쌍·유전자군

## 이 법칙을 만든 실험
- (연결된 실행 기록 없음)

## 클러스터
- [[클러스터 · 서열·조성]]
- [[법칙 목록]]
