---
유형: 법칙 허브
법칙: animal_content_v1
클러스터: 동물
판정: 양성
기준선대비: 8.1639
tags:
  - 법칙/animal_content_v1
  - 클러스터/동물
  - 판정/양성
---

# animal_content_v1

> [!abstract] 적용 범위
> Gene-family (Pfam) loss, duplication and gain in animals when a lineage changes cell temperature, moves from sea to fresh water, into hypoxia, becomes endothermic or parasitic. Learned from designed within-clade pairs; animal registry only.

**모형** — Linear birth-death per family; log rate = a_pair + x @ (axis change @ W), design = (base, colder, freshwater, hypoxia, endothermy, parasite).

## 판정 — 양성

| 비교한 곳 | 법칙 | 기준선 | 차이 | 방향 |
| --- | --- | --- | --- | --- |
| leave_one_origin_out_auroc · all | `axes_better_in` 9 | `rarity` 0.8361 | +8.1639 | 높을수록 좋음 |
| leave_one_origin_out_auroc · close_proxies_only | `axes_better_in` 7 | `rarity` 0.8324 | +6.1676 | 높을수록 좋음 |

## 이 클러스터의 노트
- [[animal_content_v1 · 계수]] — 학습된 가중치와 신뢰구간
- [[animal_content_v1 · 검증]] — 기준선과 나란히 본 성적
- [[animal_content_v1 · 한계]] — 이 법칙을 깨뜨리는 조건
- [[animal_content_v1 · 환경]] — 어떤 환경의 종들에서 나왔나
- [[animal_content_v1 · 데이터]] — 쓰인 종·쌍·유전자군

## 이 법칙을 만든 실험
- (연결된 실행 기록 없음)

## 클러스터
- [[클러스터 · 동물]]
- [[법칙 목록]]
