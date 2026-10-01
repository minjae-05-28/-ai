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
                       "보통 → 극한 환경", ["환경과 서열"], "results/environment/fig_environment.png", "현역 (65종 재학습 중)"),
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
}

TOPICS = {
    "유전자 소실 성향": "유전체가 줄어들 때 **무엇부터** 잃는지는 환경보다 유전자 자체의 성향(얼마나 여러 상황에서 필요한가)이 정한다. 네 시스템(미토콘드리아, 엽록체, 곤충 공생세균, 진핵 기생생물)에서 잃는 순서는 유전자별 소실률만으로 설명된다. Krylov 외 2003의 '유전자 소실 성향'과 같은 결론을 독립적으로 재현.",
    "생활 방식 축": "기생을 기생·세포 안·미토콘드리아 퇴화로 나누면 **얼마나** 잃는지가 축의 덧셈으로 예측된다. 에너지 유전자 소실은 기생 자체가 아니라 미토콘드리아 퇴화 때문. 기생생물은 아미노산 수송체와 퓨린 재활용 효소를 늘린다.",
    "소기관 묶음과 독립성": "기생생물과 극한 세균에서는 유전자군이 거의 독립적으로 사라지지만, 소기관에서는 복합체 단위로 함께 사라진다(NDH 복합체, 광수확 안테나 등). 통합 법칙: 성향 × 강도는 공통, 소기관에서는 복합체 묶음이 추가.",
    "환경과 서열": "환경 정보는 어떤 유전자를 잃을지 예측하지 못했지만, 단백질 아미노산 조성 변화는 잘 설명한다(R² 0.53–0.63). 적응은 유전자 구성이 아니라 서열에서 일어난다. 고온 → IVYWREL·전하 아미노산 증가, 고염 → 산성 단백질, 빈영양 → 질소 절약, 무산소·빈영양 → AT 편향.",
    "계통 보정": "가까운 종을 독립으로 취급한 문제를 NCBI 분류 체계로 보정(분류 단계별 분산 성분을 추정하는 일반화 최소제곱). 14개 중 13개 유지. 세포 안 효과는 탈락, 빈영양 질소 절약은 보정 후 드러남.",
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
        body = [frontmatter({"tags": ["주제"]}), f"# {t}", "", text, ""]
        if laws:
            body += ["## 법칙"] + [f"- [[{i}]] — {LAWS[i][0][:60]}…" for i in laws]
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
            ["", f"## 문헌 법칙 ({n_lit}개, 일치 {consistent})"] + [f"- [[{L['id']}]] — {L['verdict']}" for L in lit] + \
            ["", "## 페이지"] + [f"- [{k}]({v})" for k, v in ARTIFACTS.items()] + \
            ["", "## 데이터", "- 진핵생물 120종 (비교 쌍 99개)", "- 세균·고세균 65종 (비교 쌍 43개) + 기후 관련 병원체 5종",
             "- 소기관·공생세균 유전체 64개", "- 단백질 조성 209종, NCBI 분류 242개"]
    (root / "00 시작.md").write_text("\n".join(index))
    print(f"vault -> {root} ({len(list(root.rglob('*.md')))} notes)")


if __name__ == "__main__":
    main()
