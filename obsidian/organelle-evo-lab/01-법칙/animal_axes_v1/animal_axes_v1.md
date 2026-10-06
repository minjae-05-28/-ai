---
유형: 법칙 허브
법칙: animal_axes_v1
클러스터: 동물
판정: 양성
기준선대비: 0.0117
tags:
  - 법칙/animal_axes_v1
  - 클러스터/동물
  - 판정/양성
---

# animal_axes_v1

> [!abstract] 적용 범위
> Composition laws fitted to animal cells on the variables an animal cell experiences: operating temperature, intracellular osmolarity, hypoxia, endothermy, parasitism and urea-based osmoconformity.

**모형** — Additive least squares per composition statistic, checked by leave-one-clade-out, a clade-level refit, and genome GC as a covariate.

## 판정 — 양성

| 비교한 곳 | 법칙 | 기준선 | 차이 | 방향 |
| --- | --- | --- | --- | --- |
| traits · ivywrel · leave_one_clade_out | `mae_law` 0.005266 | `mae_mean_baseline` 0.005078 | +0.0002 | 높을수록 좋음 |
| traits · cvp · leave_one_clade_out | `mae_law` 0.01004 | `mae_mean_baseline` 0.009494 | +0.0005 | 높을수록 좋음 |
| traits · acidic_excess · leave_one_clade_out | `mae_law` 0.004277 | `mae_mean_baseline` 0.003712 | +0.0006 | 높을수록 좋음 |
| traits · median_pi · leave_one_clade_out | `mae_law` 0.318 | `mae_mean_baseline` 0.3063 | +0.0117 | 높을수록 좋음 |
| traits · n_side · leave_one_clade_out | `mae_law` 0.005806 | `mae_mean_baseline` 0.005731 | +0.0001 | 높을수록 좋음 |
| traits · gravy · leave_one_clade_out | `mae_law` 0.0309 | `mae_mean_baseline` 0.02951 | +0.0014 | 높을수록 좋음 |
| traits · fymink · leave_one_clade_out | `mae_law` 0.02424 | `mae_mean_baseline` 0.0225 | +0.0017 | 높을수록 좋음 |
| traits · aromatic · leave_one_clade_out | `mae_law` 0.004976 | `mae_mean_baseline` 0.00427 | +0.0007 | 높을수록 좋음 |
| traits · cysteine · leave_one_clade_out | `mae_law` 0.001479 | `mae_mean_baseline` 0.001196 | +0.0003 | 높을수록 좋음 |

## 이 클러스터의 노트
- [[animal_axes_v1 · 계수]] — 학습된 가중치와 신뢰구간
- [[animal_axes_v1 · 검증]] — 기준선과 나란히 본 성적
- [[animal_axes_v1 · 한계]] — 이 법칙을 깨뜨리는 조건
- [[animal_axes_v1 · 환경]] — 어떤 환경의 종들에서 나왔나
- [[animal_axes_v1 · 데이터]] — 쓰인 종·쌍·유전자군

## 이 법칙을 만든 실험
- (연결된 실행 기록 없음)

## 클러스터
- [[클러스터 · 동물]]
- [[법칙 목록]]
