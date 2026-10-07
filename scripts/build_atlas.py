"""One data file for the ancestor atlas: every node this project has reconstructed, plus the
candidates it cannot reach yet and why.

    PYTHONPATH=src python scripts/build_atlas.py

Reads the saved reconstructions (results/mito_ancestor/, results/clade_ancestor/) and rebuilds
only the cheap part of the pipeline — which species sit under each node and which families they
carry today — so each ancestor can be put beside its living descendants. No reconstruction is
re-run and no posterior is recomputed here.

Size is quoted only where the sample reaches the clade's root. results/sample_size/summary.json
measured that: with every species rep in hand the node reached IS the root (size -8.6%); every
subsample lands on a younger node (size -10 to -17%). So the alphaproteobacterial ancestor
carries a size, the orders carry it with a warning, and the amoeba node carries none.
"""

import gzip
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
from run_mito_ancestor import functions_of, load_tips, parse_newick, postorder, prune  # noqa: E402

OUT = Path("results/atlas")
MITO = Path("results/mito_ancestor/completeness")  # the quality-corrected run
AMOEBA = Path("results/clade_ancestor/amoebozoa_v4")  # the current best model
# The function classes worth a comparison bar: broad enough to hold families, specific enough to read.
FUNCS = ["catalytic activity", "transferase activity", "oxidoreductase activity", "hydrolase activity",
         "protease", "DNA binding", "ribosome", "transporter_channel", "organelle", "kinase",
         "structural molecule activity", "uncharacterised"]
FUNC_KO = {"catalytic activity": "효소 전반", "transferase activity": "전이효소",
           "oxidoreductase activity": "산화환원효소", "hydrolase activity": "가수분해효소",
           "protease": "단백질분해효소", "DNA binding": "DNA 결합", "ribosome": "리보솜",
           "transporter_channel": "운반체·통로", "organelle": "소기관", "kinase": "인산화효소",
           "structural molecule activity": "구조 단백질", "uncharacterised": "기능 미상"}

BLOCKED = [
    {"id": "giant_virus", "name": "거대바이러스의 조상", "group": "바이러스",
     "why": "유전자군 수준 통계가 통하는 유일한 바이러스 무리(수백~수천 유전자). 프로테옴 수집은 돌고 있지만, "
            "조상 크기를 말하려면 핵심 유전자 계통수를 세우고 수평 전달 비율이 0.35 아래임을 먼저 재야 합니다.",
     "blocker": "계통수 미구축 · 수평 전달률 미측정"},
    {"id": "cpr", "name": "CPR(패테스세균)의 조상", "group": "세균",
     "why": "UniProt이 중복 프로테옴의 서열을 버려서, 목록에 있는 2,202종 가운데 실제로 쓸 수 있는 것이 15종뿐입니다.",
     "blocker": "서열 없음 — NCBI에서 받아 HMMER를 직접 돌려야 함(수십 시간)"},
    {"id": "common_cold", "name": "감기 바이러스의 조상", "group": "바이러스",
     "why": "RNA 바이러스는 유전자가 10개 안팎이고 서열이 너무 빨리 바뀌어, 유전자군 보유/소실 모형이 성립하지 않습니다.",
     "blocker": "방법이 성립하지 않음 — 하지 않기로 함"},
]


# Each clade: results dir, display text. Only drawn when its run exists.
CLADES = [
    {"id": "fungi", "dir": "results/clade_ancestor/fungi", "name": "균류의 조상", "group": "진핵생물",
     "sub": "표본 균류 전체의 공통 조상",
     "blurb": "효모·곰팡이·버섯·키트리드·미포자충이 갈라지기 전의 유전자 구성입니다. 목(order)마다 고르게 "
              "뽑은 균류와 외군(깃편모충·어류포자충·폰티쿨라 등)의 리보솜 마커 계통수 위에서 복원했습니다. "
              "뿌리의 한쪽은 로젤라·미포자충 계열 3종뿐이라, 그 3종에 없는 유전자군은 여기서 '판단 불가'(약 0.1)로 "
              "나옵니다 — 옆의 '핵심 균류의 조상'과 같이 보세요."},
    {"id": "fungi_core", "dir": "results/clade_ancestor/fungi", "child": True, "power_key": "뿌리 아래 큰 쪽",
     "hgt_id": "fungi", "shared_with": "균류 뿌리 복원(같은 실행)", "name": "핵심 균류의 조상", "group": "진핵생물", "sub": "로젤라 계열이 갈라진 뒤의 마디",
     "blurb": "균류 뿌리에서 로젤라·미포자충 계열(세포 안 기생체, 유전체가 크게 줄어듦)을 뺀 나머지 286종의 공통 "
              "조상입니다. 키틴 합성효소 1군·균류 전사인자 같은 '균류다운' 유전자군이 여기서 확실해집니다."},
    {"id": "leca", "dir": "results/clade_ancestor/leca", "name": "모든 진핵생물의 조상 (LECA)", "group": "진핵생물",
     "sub": "동물·식물·균류·원생생물의 마지막 공통 조상", "confidence": "낮음",
     "blurb": "핵·미토콘드리아·섬모를 가진 첫 진핵세포입니다. 진핵생물의 뿌리가 어디인지는 아직 결론이 없어서, "
              "이 계통수에서 나눌 수 있는 두 뿌리(디스코바 / 후편모생물)로 각각 복원하고 두 경우 모두에서 있는 것만 "
              "'있었다'로 셉니다. 아래 확률은 두 뿌리 중 작은 값입니다.",
     "caveat": "외군 없이 뿌리를 '이름 붙은 갈래 | 나머지'로 잡았습니다. 아모르페아 뿌리는 이 계통수에서 갈래가 "
               "깔끔하게 나뉘지 않고(아메보조아 등 15종이 밖에 있음), 메타모나다 뿌리는 표본이 2종뿐이라 시험하지 "
               "못했습니다. 알려진 정답 채점에서 두 뿌리 모두 기준선보다는 낫지만 AUROC가 0.62(디스코바)·0.82"
               "(후편모생물)로 다른 조상보다 크게 낮고, 크기 오차가 +34%와 −38%로 반대 방향이라 개수는 말하지 "
               "않습니다. 유전자군 목록은 순위로만 읽어 주세요."},
    {"id": "leca2", "dir": "results/clade_ancestor/leca2", "hgt_id": "leca2",
     "name": "모든 진핵생물의 조상 (LECA, 2판)", "group": "진핵생물",
     "sub": "희귀 갈래를 보강하고 제약 계통수로 다시 복원", "confidence": "중간",
     "blurb": "1판보다 메타모나다(4→18종)·리자리아·합토파이트를 늘리고, 큰 갈래의 단계통성을 제약으로 준 IQ-TREE "
              "계통수로 다시 복원했습니다. 그 덕분에 뿌리 위치 네 곳(디스코바·후편모생물·아모르페아·메타모나다)을 "
              "모두 시험했고, 네 경우 모두에서 있는 것만 '있었다'로 셉니다. 아래 확률은 네 뿌리 중 가장 작은 값입니다.",
     "caveat": "알려진 정답 채점: 네 뿌리 모두 기준선보다 낫고 AUROC 0.81~0.86, 크기 오차 +4~+8%(조금 크게 나옴)라 "
               "크기는 뿌리별 범위로만 말합니다(3,900~4,600개). 음성 대조 일부 실패: 엽록체 유전체의 광계 유전자군이 "
               "0.24~0.73으로 나왔습니다. 엽록체는 2차 내공생으로 여러 갈래에 옆으로 퍼졌는데, 보유/소실 모형은 이를 "
               "'조상에 있었고 여러 번 잃음'으로 읽습니다. 이 유전자군들은 '모든 뿌리에서 있음' 목록에는 들지 않지만, "
               "'지금은 드문데 조상에 있었다'는 목록은 같은 이유로 부풀 수 있습니다. 계통수는 빠른 탐색(-fast)이고 "
               "부트스트랩이 없어 계통수 불확실성은 빠져 있습니다."},
    {"id": "cyano", "dir": "results/clade_ancestor/cyano", "name": "남세균의 조상", "group": "소기관",
     "ko_clade": "남세균", "sub": "산소 광합성 남세균(Cyanobacteriia) 공통 조상",
     "blurb": "엽록체를 낳은 남세균 무리 전체의 공통 조상입니다. GTDB 세균 계통수 위에서 복원했고, 뿌리의 한쪽은 "
              "가장 먼저 갈라진 글로에오박터 3종입니다."},
    {"id": "plastid", "dir": "results/clade_ancestor/cyano", "child": True, "power_key": "뿌리 아래 큰 쪽",
     "hgt_id": "cyano", "shared_with": "남세균 뿌리 복원(같은 실행)", "ko_clade": "남세균",
     "name": "엽록체 분기점의 조상", "group": "소기관", "sub": "글로에오마르가리타 계통이 갈라진 마디",
     "blurb": "엽록체에 가장 가까운 현생 남세균인 글로에오마르가리타가 갈라져 나간 마디입니다. 이 계통수에서는 "
              "글로에오박터 다음 마디와 같아서 알려진 정답 채점도 그 마디에서 받았습니다. 엽록체가 된 세균이 "
              "삼켜지기 직전 가졌던 유전자 구성에 가장 가까운 추정입니다."},
]


_COUNTS = {}


def family_counts(species):
    """Pfam family count per collected UniProt proteome (richest copy), for the today-vs-ancestor bars."""
    if not _COUNTS:
        for f in sorted(Path("data/uniprot/shards").glob("*.json.gz")):
            for v in json.loads(gzip.open(f, "rt").read()).values():
                o = v["organism"].replace("'", "")
                _COUNTS[o] = max(_COUNTS.get(o, 0), len(v.get("pfam") or {}))
    return [_COUNTS[s] for s in species if s in _COUNTS]


def clade_entry(c):
    R = Path(c["dir"])
    if not (R / "summary.json").exists():
        return None
    a = json.loads((R / "summary.json").read_text())
    z0 = np.load(R / "posterior.npz", allow_pickle=False)
    z = {k: z0[k] for k in z0.files}
    n_tips = a["clade_tips"]
    if c.get("child"):
        if "child_posteriors" not in z or not len(z["child_n_tips"]):
            return None
        j = int(np.argmax(z["child_n_tips"]))
        z["posterior"] = z["child_posteriors"][j]
        n_tips = int(z["child_n_tips"][j])
    fams = [str(x) for x in z["families"]]
    func, meta = functions_of(fams)
    comp = []
    for fn in FUNCS:
        ix = np.array([i for i, tags in enumerate(func) if fn in tags])
        if len(ix) < 15:
            continue
        comp.append({"func": fn, "ko": FUNC_KO[fn], "n_families": int(len(ix)),
                     "ancestor": round(float(z["posterior"][ix].mean()), 3),
                     "today": round(float(z["clade_frequency"][ix].mean()), 3)})
    gap = z["posterior"] - z["clade_frequency"]
    top = np.argsort(-gap)[:14]
    pw_file = Path("results/node_power") / c.get("hgt_id", c["id"]) / "summary.json"
    agg = json.loads(pw_file.read_text())["aggregate"] if pw_file.exists() else {}
    power = next((v for k, v in agg.items() if c.get("power_key", "표본이 도달한 마디") in k), None)
    hid = c.get("hgt_id", c["id"])
    hg_file = Path("results/hgt_rate") / hid / "summary.json"
    hg = json.loads(hg_file.read_text())["sets"].get(hid) if hg_file.exists() else None
    # A size is quoted only when the known-truth test says the reconstruction gets it within 10%.
    bias = power["recon_size_bias"] if power else None
    quote = bias is not None and abs(bias) <= 0.10
    expected = int(round(float(z["posterior"].sum()))) if quote else None
    per_root = a.get("sum_of_posteriors_per_root")
    if per_root and quote:
        # Several root positions: the minimum-over-roots posterior is a "present everywhere" call, not a size.
        # The size is each root's own sum; the bar shows their mean, the note their range.
        expected = int(round(float(np.mean(list(per_root.values())))))
    v = a["leave_tips_out_auroc"]
    kc = c.get("ko_clade", "균류")
    counts = family_counts(a["clade_species"])
    intruders = a.get("non_clade_tips_inside_clade_node") or []
    return {
        "id": c["id"], "name": c["name"], "sub": c["sub"], "group": c["group"], "blurb": c["blurb"],
        "confidence": c.get("confidence") or ("중간" if power and power["verdict"] == "계통수가 도움이 됨" else "낮음"),
        "quote_size": quote, "power": power, "_hgt": hg,
        "phylum_power": {k: val for k, val in agg.items() if "표본이 도달한 마디" not in k
                         and "뿌리 아래 큰 쪽" not in k},
        "extra_caveat": c.get("caveat") or (f"뿌리는 {kc}에서 가장 먼 외군 잎({a.get('rooted_on')})에 잡았습니다. "
                         + (f"{kc} 마디 안으로 외군 {len(intruders)}종이 들어왔습니다: {', '.join(intruders[:5])}."
                            if intruders else f"{kc}는 계통수에서 한 덩어리(단계통)로 나왔습니다")
                         + (f" — 단, 계통수가 {kc} 밖에 붙인 {len(a['misplaced_clade_tips_left_out'])}종"
                            f"({', '.join(a['misplaced_clade_tips_left_out'])}, 진화가 빨라 엉뚱한 곳에 붙는 "
                            "'긴 가지 끌림')을 뺀 뒤입니다." if a.get("misplaced_clade_tips_left_out") else ".")
                         + (" 부트스트랩 계통수 없이 돌려서 계통수 불확실성은 아직 반영되지 않았습니다."
                            if not a.get("n_bootstrap_trees") else "")
                         + " 불완전한 프로테옴은 손실이 아니라 누락으로 다룹니다(완전도 모형, 축소 계통 가속 끔)."),
        "size_note": (f"뿌리 위치별 크기 {', '.join(f'{k} {v:,.0f}' for k, v in per_root.items())}; 막대는 그 평균입니다. "
                      f"알려진 정답 모의의 크기 편향은 가장 나쁜 뿌리에서도 {bias:+.1%}로 10% 안쪽입니다."
                      if per_root and quote else
                      f"알려진 정답 모의에서 조상 크기 편향 {bias:+.1%}. 10% 안쪽이라 개수를 함께 보입니다 "
                      "(모든 유전자군의 사후확률 합)." if quote else
                      (f"알려진 정답 모의에서 조상 크기 편향 {bias:+.1%}로 10%를 넘어 개수를 말하지 않습니다."
                       if bias is not None else "알려진 정답 채점 전이라 개수를 말하지 않습니다.")),
        "tips": n_tips, "families_considered": a["families_considered"],
        "validation": {"reconstruction": v["reconstruction"], "baseline": v["clade_frequency"],
                       "baseline_label": "현생 빈도(계통수 없음)", "shared": bool(c.get("child")),
                       "shared_with": c.get("shared_with", ""),
                       "margin": round(v["reconstruction"] - v["clade_frequency"], 4), "extra": {}},
        "expected_families": expected,
        "today_median_families": int(np.median(counts)) if counts else None,
        "today_min_families": min(counts) if counts else None,
        "today_max_families": max(counts) if counts else None,
        "confident": (int((z["posterior"] >= 0.9).sum()) if c.get("child") else a["n_confident_families"]),
        "uncertain": (int(((z["posterior"] >= 0.5) & (z["posterior"] < 0.9)).sum()) if c.get("child")
                      else a["n_uncertain_families"]),
        "functions": [[k, n] for k, n in a["functions_of_confident_families"][:12]] if not c.get("child") else
                     Counter(t for j in np.flatnonzero(z["posterior"] >= 0.9) for t in func[j]).most_common(12),
        "comparison": comp,
        "lost": [{"family": fams[i], "desc": meta.get(fams[i], {}).get("description", ""),
                  "p": round(float(z["posterior"][i]), 2), "today": round(float(z["clade_frequency"][i]), 2)}
                 for i in top],
        "positive_control": None,
        "species_examples": [s.split(" (")[0] for s in a["clade_species"][:8]],
        "report_url": "",
    }


def tip_matrix():
    """Rebuild which species sit on the tree and which families each carries (the saved run's inputs)."""
    tips = load_tips(300, min_busco=0.0)
    parent, length, label = parse_newick(gzip.open("results/phylo_tree/gtdb_bac120.tree.gz", "rt").read())
    acc_node = {lab: i for i, lab in enumerate(label) if lab in tips}
    parent, length, label, _ = prune(parent, length, label, list(acc_node.values()))
    order, children = postorder(parent)
    tip_of = {i: label[i] for i in range(len(parent)) if not children[i]}
    counts = Counter(f for a in tip_of.values() for f in tips[a][2])
    fams = sorted(f for f, c in counts.items() if c >= 3)
    return tips, tip_of, fams


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    saved = json.loads((MITO / "families.json").read_text())
    tips, tip_of, fams = tip_matrix()
    if fams != saved:
        raise SystemExit(f"family list does not match the saved run ({len(fams)} vs {len(saved)})")
    col = {f: j for j, f in enumerate(fams)}
    func_of, meta = functions_of(fams)
    func_idx = {fn: np.array([i for i, tags in enumerate(func_of) if fn in tags]) for fn in FUNCS}

    by_order = defaultdict(list)
    alpha = []
    for v, a in tip_of.items():
        tax = tips[a][1]
        if "c__Alphaproteobacteria" in tax:
            alpha.append(v)
            by_order[tax.split(";")[3]].append(v)
    members = {"Alphaproteobacteria": alpha, "Rickettsiales": by_order["o__Rickettsiales"],
               "Rhodospirillales": by_order["o__Rhodospirillales"],
               "Caulobacterales": by_order["o__Caulobacterales"]}

    # One of the 2,526 proteomes (Magnetospirillum gryphiswaldense) is empty: UniProt keeps the
    # record but not the sequences. It is one tip in 2,526, so the reconstruction is unaffected, but
    # it would drag the present-day counts, so it is left out of the comparison statistics.
    EMPTY = [v for v in tip_of if len(tips[tip_of[v]][2]) < 100]

    def present(vs):
        """families x tips presence among the tips with a usable proteome."""
        vs = [v for v in vs if v not in set(EMPTY)]
        M = np.zeros((len(vs), len(fams)), dtype=bool)
        for i, v in enumerate(vs):
            M[i, [col[f] for f in tips[tip_of[v]][2] if f in col]] = True
        return M

    power = json.loads(Path("results/node_power/summary.json").read_text())["aggregate"]
    summ = json.loads((MITO / "summary.json").read_text())
    targets = []
    META = {
        "Alphaproteobacteria": dict(
            id="alpha", name="미토콘드리아의 조상", sub="알파프로테오박테리아 공통 조상", group="소기관",
            blurb="미토콘드리아는 이 무리 안에서 삼켜진 세균에서 왔습니다. 그 세균이 아직 자유생활하던 시절의 "
                  "유전자 구성을 되돌린 것입니다.",
            confidence="높음", quote_size=True,
            size_note="표본이 이 분류군의 종 대표를 사실상 전부 덮어 마디가 뿌리에 도달합니다. "
                      "모의실험에서 이 조건의 크기 오차는 −8.6%입니다 — 즉 적힌 수는 하한입니다. "
                      "이 복원은 유전체 품질 보정 이전 판이고, 보정을 넣으면 그 오차가 −6.6%까지 "
                      "줄어드는 것으로 측정됐으므로(results/quality_correction), 실제 조상은 적힌 수보다 "
                      "7~9% 더 컸을 것으로 봅니다."),
        "Rickettsiales": dict(
            id="rickettsiales", name="리케차목의 조상", sub="세포 안에 사는 기생 세균 무리", group="세균",
            blurb="발진티푸스균과 볼바키아가 속한 무리로, 미토콘드리아의 가장 가까운 친척 후보입니다. "
                  "오늘날은 숙주 세포 안에서만 살며 유전체가 크게 줄었습니다.",
            confidence="중간", quote_size=True,
            extra_caveat="알려진 정답으로 채점하면 이 마디는 계통수 효과가 가장 큰 곳입니다"
                         "(AUROC 0.975 vs 기준선 0.908). 대신 크기가 가장 많이 어긋납니다 — 모든 "
                         "후손이 다 잃어버린 유전자군은 보이지 않고, 이 마디에서 그 몫이 −37%로 "
                         "다른 마디(−1% 안팎)와 비교가 안 됩니다. 즉 적힌 조상 크기는 크게 낮은 값이고, "
                         "실제 소실 폭은 적힌 것보다 큽니다.",
            size_note="40종으로 세운 마디입니다. 모의실험에서 이 규모의 크기 오차는 −10~12%이고, "
                      "도달 마디가 목의 뿌리보다 젊을 수 있습니다. 품질 보정 이전 판이므로 적힌 수는 "
                      "하한으로 읽어야 합니다."),
        "Rhodospirillales": dict(
            id="rhodospirillales", name="홍색비황세균목의 조상", sub="자유생활 광합성·대사 다재다능 무리", group="세균",
            blurb="리케차목과 정반대 방향으로 간 무리입니다. 같은 조상에서 갈라졌는데 유전자군을 줄이지 않았습니다.",
            confidence="중간", quote_size=True,
            size_note="45종. 크기 오차 −10~12% 구간이고, 품질 보정 이전 판이라 적힌 수는 하한입니다."),
        "Caulobacterales": dict(
            id="caulobacterales", name="카울로박터목의 조상", sub="물에 붙어 사는 자루 달린 세균", group="세균",
            blurb="세포 분열 연구의 모델 생물(Caulobacter)이 속한 무리입니다.",
            confidence="중간", quote_size=True,
            size_note="122종. 크기 오차 −10% 안팎이고, 품질 보정 이전 판이라 적힌 수는 하한입니다."),
    }
    for keyname, vs in members.items():
        node = {"Alphaproteobacteria": "Alphaproteobacteria (common ancestor)"}.get(
            keyname, f"{keyname} (common ancestor)")
        p = np.load(MITO / f"posterior_{node.replace(' ', '_').replace('(', '').replace(')', '')}.npy")
        M = present(vs)
        today = M.mean(0)
        n = summ["nodes"][node]
        m = META[keyname]
        pnv = summ["per_node_validation"][node]
        # Hiding tips cannot grade a tight clade (its baseline already scores 0.99), so each node
        # also carries the known-truth simulation that grades the ANCESTOR directly.
        pw = power.get(keyname)
        comp = []
        for fn in FUNCS:
            ix = func_idx[fn]
            if len(ix) < 15:
                continue
            comp.append({"func": fn, "ko": FUNC_KO[fn], "n_families": int(len(ix)),
                         "ancestor": round(float(p[ix].mean()), 3),
                         "today": round(float(today[ix].mean()), 3)})
        gap = p - today
        top = np.argsort(-gap)[:14]
        targets.append({**m, "tips": len(vs), "families_considered": len(fams),
            "reduced_lineage": keyname in ("Rickettsiales",),
            # Each node is now scored on its own tips (summary["per_node_validation"]).
            "validation": {"reconstruction": pnv["reconstruction"], "baseline": pnv["clade_frequency"],
                           "baseline_label": "현생 빈도(계통수 없음)", "shared": False,
                           "margin": round(pnv["reconstruction"] - pnv["clade_frequency"], 4),
                           "n_hidden": pnv["n_hidden"],
                           "extra": {"분류군 전체 기준 복원": summ["leave_tips_out_auroc"]["reconstruction"],
                                     "가장 가까운 친척": summ["leave_tips_out_auroc"]["nearest_tip"]}},
            "power": pw,
            "expected_families": round(n["expected_families"]),
            "tips_with_profile": int(M.shape[0]), "today_median_families": int(np.median(M.sum(1))),
            "today_min_families": int(M.sum(1).min()), "today_max_families": int(M.sum(1).max()),
            "confident": n["families_p_ge_0.9"], "uncertain": n["families_p_0.5_0.9"],
            "functions": [[k, v] for k, v in n["functions_top"][:12]],
            "comparison": comp,
            "lost": [{"family": str(fams[i]), "desc": meta.get(str(fams[i]), {}).get("description", ""),
                      "p": round(float(p[i]), 2), "today": round(float(today[i]), 2)} for i in top],
            "positive_control": n.get("positive_control"),
            "species_examples": [g for g, _ in Counter(
                tips[tip_of[v]][1].split(";")[5].replace("g__", "") for v in vs).most_common(8)],
        })

    # The amoeba node, from the other pipeline. Its sample cannot carry a size.
    ap_file = Path("results/node_power/amoebozoa/summary.json")
    amoeba_power = (list(json.loads(ap_file.read_text())["aggregate"].values())[0]
                    if ap_file.exists() else None)
    a = json.loads((AMOEBA / "summary.json").read_text())
    az = np.load(AMOEBA / "posterior.npz", allow_pickle=False)
    afams = [str(x) for x in az["families"]]
    afunc, ameta = functions_of(afams)
    acomp = []
    for fn in FUNCS:
        ix = np.array([i for i, tags in enumerate(afunc) if fn in tags])
        if len(ix) < 15:
            continue
        acomp.append({"func": fn, "ko": FUNC_KO[fn], "n_families": int(len(ix)),
                      "ancestor": round(float(az["posterior"][ix].mean()), 3),
                      "today": round(float(az["clade_frequency"][ix].mean()), 3)})
    agap = az["posterior"] - az["clade_frequency"]
    atop = np.argsort(-agap)[:14]
    targets.append({
        "id": "amoebozoa", "name": "아메바의 조상", "sub": "표본 12종의 공통 조상", "group": "진핵생물",
        "blurb": "세포성 점균·엔타모에바·아칸타모에바가 갈라지기 전의 유전자 구성입니다. 아메보조아 전체의 "
                 "뿌리는 아닙니다.",
        "confidence": "낮음", "quote_size": False,
        "power": amoeba_power,
        "extra_caveat": "불완전한 유전체는 손실이 아니라 누락으로 다룹니다 — 완전도를 자료에서 추정해 "
                        "가능도에 넣었고(엔타모에바 0.43~0.51), 축소 계통 손실 가속은 껐습니다. 첫 판"
                        "(laws/amoeba_ancestor_v1.json)은 그 반대였고 검증이 0.931이었습니다.",
        "size_note": "12종, 그중 8종이 한 덩어리입니다. 이 조건에서 크기는 16~17% 낮게 나오고 도달 마디가 "
                     "분류군 뿌리와 어긋나므로(자카드 0.91) 유전자군 개수를 말하지 않습니다.",
        "tips": a["clade_tips"], "families_considered": a["families_considered"],
        "validation": {"reconstruction": a["leave_tips_out_auroc"]["reconstruction"],
                       "baseline": a["leave_tips_out_auroc"]["clade_frequency"],
                       "baseline_label": "현생 빈도(계통수 없음)", "shared": False,
                       "margin": round(a["leave_tips_out_auroc"]["reconstruction"]
                                       - a["leave_tips_out_auroc"]["clade_frequency"], 4), "extra": {}},
        "expected_families": None,
        "today_median_families": None, "today_min_families": None, "today_max_families": None,
        "confident": a["n_confident_families"], "uncertain": a["n_uncertain_families"],
        "functions": [[k, v] for k, v in a["functions_of_confident_families"][:12]],
        "comparison": acomp,
        "lost": [{"family": afams[i], "desc": ameta.get(afams[i], {}).get("description", ""),
                  "p": round(float(az["posterior"][i]), 2),
                  "today": round(float(az["clade_frequency"][i]), 2)} for i in atop],
        "positive_control": None,
        "species_examples": [s.split(" (")[0] for s in a["clade_species"][:8]],
        "report_url": "",
    })

    # Clades reconstructed with run_clade_ancestor.py --clade-kingdom (fungi, then the rest in turn).
    for c in CLADES:
        e = clade_entry(c)
        if e:
            targets.append(e)

    # Measured, not assumed: the transfer level of each clade (hgt_rate.py) and, where the
    # reconstruction used it, the per-tip completeness (genome_quality.py).
    power = json.loads(Path("results/node_power/summary.json").read_text())["aggregate"]
    hgt_rate = json.loads(Path("results/hgt_rate/summary.json").read_text())
    qc = json.loads(Path("results/quality_correction/summary.json").read_text())["aggregate"]
    for t in targets:
        key = "amoebozoa" if t["id"] == "amoebozoa" else "alphaproteobacteria"
        m = t.pop("_hgt", None) or hgt_rate["sets"].get(key)
        if m:
            t["hgt"] = {"estimated": m["estimated_hgt"], "by_median_q": m["estimated_hgt_by_median_q"],
                        "gates_broken": m["gates_broken"], "set": m["label"]}
    out = {"targets": targets, "blocked": BLOCKED,
           "hgt_rate": {k: {"estimated": v["estimated_hgt"], "by_median_q": v["estimated_hgt_by_median_q"],
                            "label": v["label"], "gates_broken": v["gates_broken"]}
                        for k, v in hgt_rate["sets"].items()},
           "quality_correction": qc,
           "limits": {k: json.loads(Path("results/sample_size/summary.json").read_text())["aggregate"][k]
                      for k in ("spread_12", "spread_50", "spread_300", "spread_2323")},
           "hgt": json.loads(Path("results/hgt_limit/summary.json").read_text()).get("summary",
                 json.loads(Path("results/hgt_limit/summary.json").read_text()))}
    (OUT / "atlas.json").write_text(json.dumps(out, ensure_ascii=False, separators=(",", ":")))
    print(f"{len(targets)} targets, {len(BLOCKED)} blocked -> {OUT}/atlas.json "
          f"({(OUT / 'atlas.json').stat().st_size // 1024} KB)")
    for t in targets:
        print(f"  {t['name']:18s} tips {t['tips']:5d}  AUROC {t['validation']['reconstruction']:.3f} "
              f"vs {t['validation']['baseline']:.3f}  size {t['expected_families']} "
              f"today median {t['today_median_families']}")


if __name__ == "__main__":
    main()
