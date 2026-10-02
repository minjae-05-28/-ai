"""Build an Obsidian vault of the project: one note per law, topic notes, an index.

    python scripts/build_obsidian.py [--out obsidian/organelle-evo]

Law notes are generated from laws/*.json and laws/literature/laws.json, so rerun this
after the laws change. Copy the output folder into an Obsidian vault (or open it as one).
"""

import argparse
import json
import shutil
from pathlib import Path

ARTIFACTS = {
    "포트폴리오": "https://claude.ai/artifact/KmEtXRmrMdLmDY7rw2QkaA",
    "진화 법칙 지도": "https://claude.ai/artifact/6P3rWZp3Y1sjwuh2JycjVj",
    "조상 역추적기": "https://claude.ai/artifact/6en5NX62SRcLPZhnut7YJg",
    "화성 소금물 세포": "https://claude.ai/artifact/BqL7Xh35uPsdYF3t8utzrs",
    "두 행성의 45억 년": "https://claude.ai/artifact/N3rhy44F7hP3aqxMfFxFPK",
    "사람 몸 세포 3D": "https://claude.ai/artifact/XW5r3bLqC8MY1t5rzEWLmA",
    "GitHub 저장소": "https://github.com/minjae-05-28/-ai",
}

# id: (Korean summary, system, topics, figure or None, status)
LAWS = {
    "endosymbiosis_v1": ("공생 소기관·공생세균에서 어떤 유전자가 남는가. 에너지·번역 유전자는 어디서나 남고, RNA 중합효소는 미토콘드리아는 버리고 엽록체는 지킨다.",
                         "공생 → 소기관", ["유전자 소실 성향", "시스템별 법칙"], "results/real/fig_real_laws.png", "현역"),
    "eukaryote_lifestyle_v1": ("진핵생물 유전자군의 복제·소실을 자유생활과 기생으로 나눠 학습. 기생이 법칙을 바꾼다(ΔAIC 213).",
                               "자유생활 → 기생", ["생활 방식 축"], "results/eukaryotes/fig_eukaryotes.png", "이전 버전"),
    "eukaryote_axes_v1": ("기생을 기생·세포 안·미토콘드리아 퇴화 세 축으로 나눔. 전자전달 유전자 소실은 미토콘드리아 퇴화에서 온다(+1.54).",
                          "자유생활 → 기생", ["생활 방식 축"], "results/eukaryote_axes/fig_eukaryote_axes.png", "이전 버전"),
    "eukaryote_axes_v3": ("축별 법칙을 유전자군 특성 56개로 다시 학습. 처음 보는 기생생물 0.78, 처음 보는 계통 0.777로 계통을 넘어 통한다(수렴).",
                          "자유생활 → 기생", ["생활 방식 축", "유전자 소실 성향"], "results/transfer/fig_transfer.png", "현역"),
    "composite_v1": ("조상 역추적용 복합 법칙. 여러 법칙 조합 중 검증 성능으로 선택했고 결과는 축 법칙.",
                     "자유생활 → 기생", ["조상 역추적"], "results/reverse/fig_reverse.png", "현역"),
    "severity_v1": ("얼마나 잃나: 자유생활 10%, 세포 밖 기생 26%, 세포 안 36%, 세포 안 + 미토콘드리아 퇴화 72%. 세포 안 효과는 계통 보정 후 유지되지 않음.",
                    "자유생활 → 기생", ["생활 방식 축", "계통 보정"], "results/severity/fig_severity.png", "현역"),
    "loss_order_v1": ("잃는 순서가 계통을 넘어 같다. 더 줄어든 기생생물이 덜 줄어든 쪽의 소실을 무작위의 1.62배로 함께 잃음.",
                      "자유생활 → 기생", ["유전자 소실 성향"], "results/loss_order/fig_loss_order.png", "해석 수정됨 → loss_order_v2"),
    "loss_order_v2": ("네 시스템 공통: 순서는 유전자별 소실 성향만으로 설명된다(유전자별 소실률을 고정한 귀무모형보다 엄격하지 않음).",
                      "공통", ["유전자 소실 성향"], "results/nestedness/fig_nestedness.png", "현역"),
    "coloss_modules_v1": ("기생생물에서 유전자군은 거의 독립적으로 사라진다(묶음 효과 +0.001). 예외: 편모 축사, B12 대사.",
                          "자유생활 → 기생", ["소기관 묶음과 독립성"], "results/modules/fig_modules.png", "현역"),
    "convergent_expansion_v1": ("기생생물은 유전자군을 덜 늘리지만, 아미노산 수송체와 퓨린 재활용 효소는 여러 계통에서 독립적으로 늘린다(숙주에게서 영양을 빼온다).",
                                "자유생활 → 기생", ["생활 방식 축"], "results/expansion/fig_expansion.png", "현역"),
    "environment_v1": ("세균·고세균 환경 법칙(36종). 환경 축을 넣어도 무엇을 잃는지 예측이 나아지지 않음(0.808 vs 0.816). 일관된 효과는 편모 소실.",
                       "보통 → 극한 환경", ["환경과 서열"], "results/environment/fig_environment.png", "이전 버전 → environment_v3"),
    "severity_environment_v1": ("극한 환경에서 얼마나 잃나: 환경 변수로 예측되지 않음. 영양 부족(+0.80)만 확실히 더 많이 잃게 함.",
                                "보통 → 극한 환경", ["환경과 서열"], None, "현역"),
    "loss_order_environment_v1": ("극한 환경 적응의 소실 순서는 무작위보다 약간만 겹친다(z +2.2). 기생보다 훨씬 약함.",
                                  "보통 → 극한 환경", ["유전자 소실 성향"], None, "현역"),
    "coloss_environment_endosymbiosis_v1": ("함께 잃는 묶음: 극한 세균에는 없고, 소기관에는 있다(미토콘드리아 0.923→0.964, 엽록체 0.832→0.915).",
                                            "공통", ["소기관 묶음과 독립성"], None, "현역"),
    "severity_endosymbiosis_v1": ("공생에서 얼마나 잃나: 광합성 안 하는 색소체 92%, 동물 미토콘드리아 82%, 곤충 공생세균 85%.",
                                  "공생 → 소기관", ["시스템별 법칙"], None, "현역"),
    "organelle_modules_v1": ("소기관이 함께 잃는 묶음의 정체: NDH 복합체(홍조류 계열 색소체), 광수확 안테나(녹색 계열), 리보솜 단백질 + 호흡 복합체 부단위(식물·동물 미토콘드리아), 보조인자 합성(부크네라).",
                             "공생 → 소기관", ["소기관 묶음과 독립성"], None, "현역"),
    "sequence_v1": ("단백질 서열 수준: 환경은 유전자 소실이 아니라 아미노산 조성 변화를 설명한다(R² 0.53–0.63). 고온 IVYWREL, 고염 산성, 빈영양 질소 절약, 공생 AT 편향.",
                    "공통", ["환경과 서열"], None, "현역"),
    "family_sequence_v1": ("유전자군 단위 서열 적응: 온도·염분 적응 때 유전자군의 90%가 같은 방향으로 바뀐다(단백질 전체 적응). 막·수송 단백질은 덜 바뀌고, 흔한 핵심 세포질 단백질(번역 등)은 염분에 더 많이 산성화된다.",
                           "보통 → 극한 환경", ["환경과 서열"], None, "현역"),
    "phylo_check_v1": ("계통 보정(분류 체계 기반 분산 성분 모델) 뒤에도 14개 법칙 중 13개 유지. 세포 안 효과는 탈락, 빈영양 질소 절약은 보정 후에야 드러남.",
                       "공통", ["계통 보정"], None, "현역"),
    "gc_confound_v1": ("GC 함량 교란 검증: 온도(IVYWREL, 전하−극성)와 염분(산성 과잉) 법칙은 GC를 넣어도 효과의 88–102%가 남는다. 빈영양 질소 절약과 무산소 FYMINK는 GC로 설명되고(쌍 단위 FYMINK는 ΔGC 하나로 R² 0.94), 공생세균 AT 편향도 크기가 아니라 GC가 원인(r −0.98).",
                       "공통", ["환경과 서열", "GC 교란"], None, "현역"),
    "environment_v3": ("세균·고세균 54쌍으로 다시 학습: 환경 축을 넣어도 무엇을 잃는지 예측이 그대로(0.813 vs 0.814, 암기 0.849). 환경은 유전자 구성이 아니라 서열에 남는다.",
                       "보통 → 극한 환경", ["환경과 서열"], None, "현역"),
    "context_features_v1": ("유전자 맥락 특성(코돈으로 추정한 발현량, 오페론, 도메인 짝, 엑손)을 더함: 법칙 +0.005. 많이 발현되는 유전자가 남는다(가중치 −0.31). 법칙과 암기를 섞은 점수는 기생 0.814, 극한 0.860.",
                            "공통", ["유전자 소실 성향", "녹아웃과 발현"], None, "현역"),
    "gc3_confound_v1": ("코돈 세 번째 자리 GC(GC3)로 더 엄격하게 교란 검증: 온도·염분 법칙은 모든 검증에서 살아남고, 빈영양 질소 절약은 사라지며, 무산소 FYMINK는 32%만 남는다.",
                        "공통", ["환경과 서열", "GC 교란"], None, "현역"),
    "knockout_v1": ("실험실 녹아웃·실측 발현과 진화 소실 비교. 극한 세균: 필수 아닌 유전자군 60% vs 대부분 필수 14% 소실(Spearman −0.46, 흔한 정도 빼면 −0.17), 녹아웃만으로 AUROC 0.72. 기생생물 −0.31, 효모 필수 유전자군도 32% 잃음. 조상이 약하게 발현하는 유전자군이 사라짐(실측 RNA 49종, AUROC 0.59–0.64).",
                    "공통", ["유전자 소실 성향", "녹아웃과 발현"], None, "현역"),
    "lab_evolution_v1": ("짧은 세대 검증: 비교진화(수억 년)로 만든 소실 법칙이 대장균 5만 세대 실험(LTEE)의 결실을 맞히는지. AUROC 0.59로 거의 못 맞히고, 선택압 없는 돌연변이 축적 대조군(0.60)과 차이가 없다(−0.005 [−0.067, +0.056]). 우리 법칙은 짧은 세대에 쓸 수 없다는 뜻. 속도도 1,000세대당 4개로, 축소 유전체와 규모가 다르다.",
                         "공통", ["유전자 소실 성향", "시간 규모"], None, "현역"),
    "human_cell_v1": ("사람 몸(장·피부·혈액)에 맞춘 세포를 법칙으로 예측하고 실제 공생균 10종과 맞춰 봄(역예측 검증). 조성 오차 작음(장 IVYWREL 0.011), 유전자 수 2,324 vs 자유생활 3,215. 유전자 구성은 법칙 0.86이 희귀도 기준선 0.93에 짐.",
                      "보통 → 극한 환경", ["사람 몸 세포"], None, "현역"),
}

# 동물 법칙은 미생물 법칙과 섞어 쓰면 안 되므로 폴더부터 분리한다 (laws/animals/)
ANIMAL_LAWS = {
    "animal_temperature_v1": ("미생물 온도 법칙이 동물 세포에 전이되는지. 전이되지 않는다. 미토콘드리아 단백질체에서 항온동물(세포 37~42°C)은 변온동물(12~27°C)보다 IVYWREL이 +0.017 높아야 하는데 실제로는 0.021 낮다(부호 반대, p 0.006). 다만 핵 단백질체로 다시 보면 부호는 같고 5배 약하다 — 부호 역전은 미토콘드리아 AT 편향의 성질이었다.",
                              ["동물 세포 법칙", "시간 규모"], "현역 (일부는 animal_axes_v1로 갱신)"),
    "animal_axes_v1": ("동물 세포 조성을 직접 학습: 세포 온도(−1~42°C), 세포 내 삼투압(해양 1000 vs 조절 300 mOsm), 저산소, 항온성, 기생, 요소 삼투. 결과는 대체로 음성 — 조성 지표 9개 전부 분류군 하나를 빼면 평균 기준선보다 못하고, 분류군 수준 재학습에서는 삼투압 → 측쇄 질소만 남는다. 동물 조성은 환경보다 계통이 정한다.",
                       ["동물 세포 법칙"], "현역"),
}

TOPICS = {
    "유전자 소실 성향": "유전체가 줄어들 때 **무엇부터** 잃는지는 환경보다 유전자 자체의 성향(얼마나 여러 상황에서 필요한가)이 정한다. 네 시스템(미토콘드리아, 엽록체, 곤충 공생세균, 진핵 기생생물)에서 잃는 순서는 유전자별 소실률만으로 설명된다. Krylov 외 2003의 '유전자 소실 성향'과 같은 결론을 독립적으로 재현.",
    "생활 방식 축": "기생을 기생·세포 안·미토콘드리아 퇴화로 나누면 **얼마나** 잃는지가 축의 덧셈으로 예측된다. 에너지 유전자 소실은 기생 자체가 아니라 미토콘드리아 퇴화 때문. 기생생물은 아미노산 수송체와 퓨린 재활용 효소를 늘린다.",
    "소기관 묶음과 독립성": "기생생물과 극한 세균에서는 유전자군이 거의 독립적으로 사라지지만, 소기관에서는 복합체 단위로 함께 사라진다(NDH 복합체, 광수확 안테나 등). 통합 법칙: 성향 × 강도는 공통, 소기관에서는 복합체 묶음이 추가.",
    "환경과 서열": "환경 정보는 어떤 유전자를 잃을지 예측하지 못했지만, 단백질 아미노산 조성 변화는 잘 설명한다(R² 0.53–0.63). 적응은 유전자 구성이 아니라 서열에서 일어난다. 고온 → IVYWREL·전하 아미노산 증가, 고염 → 산성 단백질, 빈영양 → 질소 절약, 무산소·빈영양 → AT 편향. 이 중 질소 절약과 AT 편향은 GC 함량으로 설명된다([[GC 교란]]).",
    "계통 보정": "가까운 종을 독립으로 취급한 문제를 NCBI 분류 체계로 보정(분류 단계별 분산 성분을 추정하는 일반화 최소제곱). 14개 중 13개 유지. 세포 안 효과는 탈락, 빈영양 질소 절약은 보정 후 드러남.",
    "GC 교란": "아미노산 조성은 유전체 GC 함량에 크게 좌우된다(FYMINK와 r −0.96, GARP와 +0.98). GC를 공변량으로 넣자 온도·염분 법칙은 그대로 남았고, 빈영양 질소 절약, 무산소 FYMINK, 공생세균 AT 편향은 GC로 설명됐다. 다만 GC 자체가 환경 적응일 수 있어(AT 염기쌍은 질소가 적다) '적응이 아니다'라고 단정할 수는 없다.",
    "녹아웃과 발현": "실험실에서 유전자를 지워 본 결과(DEG 필수 유전자, Fitness Browser 세균 69종, 효모 결실)와 실측 발현량(PaxDb 단백질 양, 공개 RNA-seq 49종)을 진화 소실과 비교. 지워도 괜찮은 유전자, 약하게 발현되는 유전자가 진화에서도 먼저 사라진다. 다만 상당 부분은 '흔한 유전자가 남는다'는 경향과 겹친다. 기생생물은 효모에서 필수인 유전자까지 버린다(숙주가 대신 해 줌).",
    "사람 몸 세포": "장·피부·혈액을 환경 값으로 넣어 법칙이 예측하는 세포를 만들고, 실제 사람 공생균 10종을 정답지로 맞춰 본 역예측 검증. 서열 조성과 유전체 크기는 잘 맞지만, 어떤 유전자를 가질지는 단순 기준선보다 못하다. 장은 산화환원효소, 피부는 편모, 혈액은 반복 도메인을 버린다. 실험용 설계가 아니라 유전자군 수준의 계산 결과다.",
    "동물 세포 법칙": "미생물 법칙을 동물에 그대로 쓸 수 없다는 게 측정으로 확인됐기 때문에(온도 법칙 전이 실패), 동물은 별도 저장소(`laws/animals/`)에 따로 학습해 둔다. 축도 동물 생리에 맞게 다시 정의했다 — 세포가 실제로 작동하는 온도, 세포 내 삼투압(해양 무척추동물은 바닷물에 맞춰 약 1000 mOsm, 척추동물·담수·육상은 약 300으로 조절), 저산소, 항온성, 기생, 요소 삼투. 핵 단백질체 69종 18개 분류군으로 학습한 결과는 대체로 음성이다: 동물 조성은 이 환경 축보다 계통이 정한다. 유일하게 분류군 검증을 통과한 것은 삼투압 → 측쇄 질소.",
    "시간 규모": "우리 법칙은 조상이 수천만~수억 년 전에 갈라진 현재 유전체들을 비교해서 얻은 것이다. 대장균 장기 진화 실험(5만 세대, 약 25년)으로 짧은 세대에서도 통하는지 시험했더니, 결실 예측 AUROC 0.59에 선택압 없는 대조군과 차이가 없었다. 규모도 다르다 — 실험은 1,000세대당 4개를 잃는데, 우리가 다루는 축소 유전체는 수백~수천 개를 잃었다. 따라서 이 법칙으로 몇 세대~몇십 년 뒤를 예측해서는 안 된다.",
    "시스템별 법칙": "미토콘드리아와 엽록체는 보존 규칙 일부를 공유하지만(교차 예측 0.36–0.43), 시스템별 규칙이 더 잘 맞는다(ΔAIC 787). 소수성 단백질이 남는 효과는 미토콘드리아에서만.",
    "조상 역추적": "현대 기생생물 유전체 하나로 자유생활 조상의 유전자군을 복원(AUROC 0.78). 대부분은 흔한 유전자는 원래 있었다는 사전 지식에서 나오고, 법칙이 더하는 몫은 작다.",
    "화성 실험": "학습한 법칙과 별개로, 최소 세포에 무작위 진화 법칙 수백 개를 적용해 화성 환경 변화를 따라 진화시킴. 법칙과 무관하게 과염소산염 호흡, 저온·삼투 보호, DNA 수선 2배, 편모 소실이 나타남. 유전자 풀이 없는 고립 조건에서 급변하면 64.5%만 생존. 미래 예측 작업은 중단함.",
}


TAG = {"공생 → 소기관": "공생소기관", "자유생활 → 기생": "기생", "보통 → 극한 환경": "극한환경", "공통": "공통"}


def rnd(x):
    return round(x, 3) if isinstance(x, float) else x


def frontmatter(d):
    lines = ["---"]
    for k, v in d.items():
        if isinstance(v, list):
            lines.append(f"{k}:")
            lines += [f"  - {x}" for x in v]
        else:
            lines.append(f"{k}: {json.dumps(v, ensure_ascii=False) if isinstance(v, str) and ':' in v else v}")
    lines.append("---")
    return "\n".join(lines)


def fmt_validation(v, depth=0):
    if not isinstance(v, dict):
        return f"`{json.dumps(v, ensure_ascii=False)[:300]}`"
    out = []
    for k, x in list(v.items())[:12]:
        if isinstance(x, (int, float, str, bool)) or x is None:
            out.append(f"{'  ' * depth}- {k}: {rnd(x)}")
        elif isinstance(x, dict) and depth < 1:
            out.append(f"{'  ' * depth}- {k}:")
            out.append(fmt_validation(x, depth + 1))
        else:
            out.append(f"{'  ' * depth}- {k}: `{json.dumps(x, ensure_ascii=False)[:160]}`")
    return "\n".join(out)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default="obsidian/organelle-evo")
    args = ap.parse_args()
    root = Path(args.out)
    if root.exists():
        shutil.rmtree(root)
    for sub in ("법칙", "문헌 법칙", "주제", "첨부"):
        (root / sub).mkdir(parents=True, exist_ok=True)

    lit = json.loads(Path("laws/literature/laws.json").read_text())["laws"]
    related_lit = {}
    for L in lit:
        for r in L.get("related", []):
            related_lit.setdefault(r, []).append(L["id"])

    for law_id, (ko, topics, status) in ANIMAL_LAWS.items():
        p = Path("laws/animals") / f"{law_id}.json"
        if not p.exists():
            continue
        d = json.loads(p.read_text())
        body = [frontmatter({"id": law_id, "system": "동물 세포", "status": status,
                             "tags": ["법칙", "동물세포"]}),
                f"# {law_id}", "", f"> {ko}", "", "**저장소**: `laws/animals/` (미생물 법칙과 분리)  ",
                f"**상태**: {status}  ", f"**주제**: {', '.join(f'[[{t}]]' for t in topics)}", "",
                "## 적용 범위 (원문)", d["scope"], "", "## 모델", d["model"], "", "## 검증",
                fmt_validation(d["validation"]), "", "## 한계",
                "\n".join(f"- {c}" for c in d.get("caveats", []))]
        out = root / "동물 법칙" / f"{law_id}.md"
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text("\n".join(body) + "\n")

    for law_id, (ko, system, topics, fig, status) in LAWS.items():
        p = Path("laws") / f"{law_id}.json"
        if not p.exists():
            continue
        d = json.loads(p.read_text())
        body = [frontmatter({"id": law_id, "system": system, "status": status, "tags": ["법칙", TAG[system]]}),
                f"# {law_id}", "", f"> {ko}", "", f"**시스템**: {system}  ", f"**상태**: {status}  ",
                "**주제**: " + ", ".join(f"[[{t}]]" for t in topics), ""]
        if fig and Path(fig).exists():
            name = f"{law_id}.png"
            shutil.copy(fig, root / "첨부" / name)
            body += [f"![[{name}]]", ""]
        body += ["## 적용 범위 (원문)", d.get("scope", ""), "", "## 모델", d.get("model", ""), ""]
        if d.get("validation"):
            body += ["## 검증", fmt_validation(d["validation"]), ""]
        if d.get("caveats"):
            body += ["## 한계"] + [f"- {c}" for c in d["caveats"]] + [""]
        if law_id in related_lit:
            body += ["## 관련 문헌 법칙"] + [f"- [[{x}]]" for x in related_lit[law_id]] + [""]
        body += [f"원본: `laws/{law_id}.json`"]
        (root / "법칙" / f"{law_id}.md").write_text("\n".join(body))

    for L in lit:
        body = [frontmatter({"id": L["id"], "verdict": L["verdict"], "tags": ["문헌법칙"]}), f"# {L['id']}", "",
                f"> {L['statement']}", "", f"**출처**: [{L['source']}]({L['url']})  ", f"**우리 데이터 판정**: {L['verdict']}", "",
                "## 우리 데이터로 다시 시험한 결과", L["our_test"], ""]
        if L.get("related"):
            body += ["## 관련 법칙"] + [f"- [[{r}]]" for r in L["related"]]
        (root / "문헌 법칙" / f"{L['id']}.md").write_text("\n".join(body))

    for t, text in TOPICS.items():
        laws = [i for i, v in LAWS.items() if t in v[2] and (Path('laws') / f'{i}.json').exists()]
        laws += [i for i, v in ANIMAL_LAWS.items() if t in v[1] and (Path('laws/animals') / f'{i}.json').exists()]
        body = [frontmatter({"tags": ["주제"]}), f"# {t}", "", text, ""]
        if laws:
            body += ["## 법칙"] + [f"- [[{i}]] — {(LAWS[i][0] if i in LAWS else ANIMAL_LAWS[i][0])[:60]}…" for i in laws]
        if t == "화성 실험":
            body += ["", f"- 페이지: [화성 소금물 세포]({ARTIFACTS['화성 소금물 세포']})",
                     f"- 페이지: [두 행성의 45억 년]({ARTIFACTS['두 행성의 45억 년']})"]
            if Path("results/mars_random/fig_mars_random.png").exists():
                shutil.copy("results/mars_random/fig_mars_random.png", root / "첨부" / "mars_random.png")
                body += ["", "![[mars_random.png]]"]
        (root / "주제" / f"{t}.md").write_text("\n".join(body))

    n_lit = len(lit)
    consistent = sum(1 for L in lit if L["verdict"].startswith("consistent"))
    index = [frontmatter({"tags": ["시작"]}), "# organelle-evo", "",
             "> 공생 세균이 소기관이 되고, 자유생활 생물이 기생생물이 되고, 평범한 세균이 극한 환경으로 갈 때 유전체는 무엇을 남기고 무엇을 바꾸는가. 실제 유전체 약 270개에서 규칙을 학습하고 검증한 개인 연구.",
             "", "## 핵심 결론", "1. **무엇을 잃나**는 유전자 성향이 정한다 → [[유전자 소실 성향]]",
             "2. **얼마나 잃나**는 생활 방식이 정한다 → [[생활 방식 축]]",
             "3. 기생생물·극한 세균은 독립적으로, 소기관은 **묶음으로** 잃는다 → [[소기관 묶음과 독립성]]",
             "4. **환경 적응은 서열에서** 일어난다 → [[환경과 서열]]",
             "5. 계통 보정 후에도 대부분 유지 → [[계통 보정]]", "",
             "## 주제"] + [f"- [[{t}]]" for t in TOPICS] + ["", "## 법칙 (데이터로 학습)"] + \
            [f"- [[{i}]] — {v[1]} · {v[4]}" for i, v in LAWS.items() if (Path('laws') / f'{i}.json').exists()] + \
            ["", "## 동물 세포 법칙 (`laws/animals/`, 미생물 법칙과 섞어 쓰지 않음)"] + \
            [f"- [[{i}]] — 동물 세포 · {v[2]}" for i, v in ANIMAL_LAWS.items() if (Path('laws/animals') / f'{i}.json').exists()] + \
            ["", f"## 문헌 법칙 ({n_lit}개, 일치 {consistent})"] + [f"- [[{L['id']}]] — {L['verdict']}" for L in lit] + \
            ["", "## 페이지"] + [f"- [{k}]({v})" for k, v in ARTIFACTS.items()] + \
            ["", "## 데이터", "- 진핵생물 120종 (비교 쌍 99개)", "- 세균·고세균 65종 (비교 쌍 43개) + 기후 관련 병원체 5종",
             "- 소기관·공생세균 유전체 64개", "- 단백질 조성 209종, NCBI 분류 242개"]
    (root / "00 시작.md").write_text("\n".join(index))
    print(f"vault -> {root} ({len(list(root.rglob('*.md')))} notes)")


if __name__ == "__main__":
    main()
