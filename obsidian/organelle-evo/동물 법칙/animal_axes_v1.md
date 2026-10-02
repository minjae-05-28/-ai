---
id: animal_axes_v1
system: 동물 세포
status: 현역
tags:
  - 법칙
  - 동물세포
---
# animal_axes_v1

> 동물 세포 조성을 직접 학습: 세포 온도(−1~42°C), 세포 내 삼투압(해양 1000 vs 조절 300 mOsm), 저산소, 항온성, 기생, 요소 삼투. 결과는 대체로 음성 — 조성 지표 9개 전부 분류군 하나를 빼면 평균 기준선보다 못하다. 가장 끈질긴 축은 삼투압으로, 분류군 수준에서 측쇄 질소에 남고 GC 보정 후에도 지표 4개에 남는다(바닷물에 맞춰 사는 세포는 산성 과잉 +0.0029). 온도는 GC 보정에서 탈락한다. 동물 조성은 환경보다 계통이 정한다.

**저장소**: `laws/animals/` (미생물 법칙과 분리)  
**상태**: 현역  
**주제**: [[동물 세포 법칙]]

## 적용 범위 (원문)
Composition laws fitted to animal cells on the variables an animal cell experiences: operating temperature, intracellular osmolarity, hypoxia, endothermy, parasitism and urea-based osmoconformity.

## 모델
Additive least squares per composition statistic, checked by leave-one-clade-out, a clade-level refit, and genome GC as a covariate.

## 검증
- n_species: 69
- n_clades: 18
- axes: `["tcell", "osmol_high", "hypoxia", "endo", "parasite", "urea"]`
- traits:
  - ivywrel: `{"r2": 0.2763395313426954, "coef": {"tcell": 0.00020303478990723627, "osmol_high": -0.00389131084817045, "hypoxia": 0.0018766144394684956, "endo": -0.0011838379`
  - cvp: `{"r2": 0.2670560650410666, "coef": {"tcell": 0.00010241862515687861, "osmol_high": -0.0011779334211649967, "hypoxia": -0.0029846998774793374, "endo": 0.01096920`
  - acidic_excess: `{"r2": 0.2363413576989959, "coef": {"tcell": -9.745694152220518e-05, "osmol_high": 0.0029155959019122398, "hypoxia": -0.00033565265621699256, "endo": -8.8926197`
  - median_pi: `{"r2": 0.2619919096772557, "coef": {"tcell": 0.008474960493172062, "osmol_high": -0.16581261305907086, "hypoxia": -0.04565072624187672, "endo": 0.05800751161635`
  - n_side: `{"r2": 0.24977411187849086, "coef": {"tcell": 5.895844941186293e-06, "osmol_high": -0.005741999347173928, "hypoxia": -0.0004762047738967732, "endo": 0.000572758`
  - gravy: `{"r2": 0.23660612126989855, "coef": {"tcell": 0.000572124358215134, "osmol_high": -0.0024257074802232184, "hypoxia": 0.00239264287965076, "endo": 0.004332659957`
  - fymink: `{"r2": 0.2213895013054037, "coef": {"tcell": 0.00039142216297785587, "osmol_high": 0.008055991557309102, "hypoxia": 0.006120729719166459, "endo": -0.03093661986`
  - aromatic: `{"r2": 0.19084708342195567, "coef": {"tcell": 9.974577407616032e-05, "osmol_high": 0.0018560405174722098, "hypoxia": 0.0013061653574493273, "endo": -0.004720608`
  - cysteine: `{"r2": 0.09252661294508513, "coef": {"tcell": -1.6907945405457197e-05, "osmol_high": 0.0006275202809897086, "hypoxia": 0.0004716589563427029, "endo": 0.00088746`

## 한계
- Axis values are literature approximations of typical conditions, not measurements of each animal's cells.
- Cell temperature and endothermy are correlated by biology (r about 0.56), so their separate coefficients are less certain than the pair of them together.
- Whole-proteome averages: a law here says nothing about any individual protein.
- Clades are unevenly sampled, which is why leave-one-clade-out and the clade-level refit are reported next to the fit.
