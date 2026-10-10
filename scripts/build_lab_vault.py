"""A lab-notebook Obsidian vault: every law split into its parts, every run an experiment note.

    PYTHONPATH=src python scripts/build_lab_vault.py [--out obsidian/organelle-evo-lab]

obsidian/organelle-evo (build_obsidian.py) is a reading vault: one note per law. This one is for
working: a law is not one note but a cluster of six, so a coefficient, a validation number, a
caveat and an environment envelope can each be linked, tagged and argued with on its own. Runs get
their own notes with inputs, outputs and a verdict, the way a protocol would.

Clusters are made with tags, and .obsidian/graph.json ships colour groups for them, so the graph
view separates laws from methods from experiments without any setup.
"""

import argparse
import json
import re
import shutil
from collections import defaultdict
from pathlib import Path

LAWS = Path("laws")
RESULTS = Path("results")
# A law's validation names its baselines differently per experiment; these are the ones used.
LAW_KEYS = ("composition", "law", "axis_law", "environment_law", "reconstruction", "relatives", "combined", "recon")
BASE_KEYS = ("taxonomy", "memorisation", "rarity", "copies_only", "no_environment", "no_axes", "clade_frequency",
             "alpha_frequency", "frequency", "freq", "mean", "baseline", "prior", "nearest_tip")
CLUSTERS = {
    "소기관": ("mito", "organelle", "endosymbiosis", "coloss", "severity", "loss_order"),
    "기생·극한": ("environment", "eukaryote", "context", "composite", "convergent", "expansion"),
    "서열·조성": ("sequence", "gc", "gc3", "family_sequence", "proteome_traits", "genome_traits"),
    "조상 복원": ("ancestor",),
    "실험실 대조": ("knockout", "lab_evolution", "human_cell", "literature", "phylo_check"),
    "동물": ("animal",),
    "예측": ("loss_prediction", "forward_evolution"),
    "전환 경로": ("transition",),
}


def slug(s):
    return re.sub(r"[\\/:*?\"<>|#\[\]^]", "-", str(s)).strip() or "이름없음"


def cluster_of(law_id):
    for name, keys in CLUSTERS.items():
        if any(k in law_id for k in keys):
            return name
    return "기타"


def fm(**kv):
    """YAML frontmatter. Lists are written as YAML lists so Obsidian reads the tags."""
    out = ["---"]
    for k, v in kv.items():
        if isinstance(v, (list, tuple)):
            out.append(f"{k}:")
            out += [f"  - {x}" for x in v]
        else:
            out.append(f"{k}: {v}")
    out.append("---")
    return "\n".join(out) + "\n\n"


def num(x):
    if isinstance(x, float):
        return f"{x:.4g}"
    return str(x)


def flat(d, prefix=""):
    """validation dicts nest one or two deep; flatten to name -> value for the tables."""
    out = {}
    for k, v in (d or {}).items():
        key = f"{prefix}{k}"
        if isinstance(v, dict):
            if set(v) >= {"mean"} or set(v) >= {"weight"}:
                out[key] = v
            else:
                out.update(flat(v, key + " · "))
        elif isinstance(v, (int, float, str, bool)) or v is None:
            out[key] = v
    return out


# A comparison is only meaningful between two numbers of the same metric. The first version of
# this matched a law to a baseline by name alone and compared a count of pairs (9) with an AUROC
# (0.836), a regression slope with an RMSE, and read "loss_biased" in a path as "lower is
# better" - so a negative law came out positive. Now both sides must carry the same metric.
METRICS = {"auroc": False, "auc": False, "r2": False, "spearman": False, "pearson": False,
           "accuracy": False, "rmse": True, "logloss": True, "mae": True, "brier": True}
NOT_A_METHOD = ("better_in", "delta", "per_", "max", "min", "share", "coef", "deleted",
                "essential", "count", "folds", "scheme", "best_k", "lineages", "genes", "pairs",
                "clades", "species", "threshold", "seed", "families", " - ", "difference", "gain_vs")
PRIMARY = ("leave", "heldout", "held_out", "hidden", "loo", "out_of", "loco", "lopo")


def metric_in(text):
    t = text.lower().replace("loss_biased", "")
    for m in METRICS:
        if re.search(rf"(^|[^a-z]){m}($|[^a-z])", t):
            return m
    return None


def _is(name, words):
    n = name.lower()
    return any(w in n for w in words)


def is_count(name):
    """n, n_pairs, pairs_n - but not mean_only, whose 'n_' is inside a word."""
    n = name.lower()
    return n == "n" or n.startswith("n_") or n.endswith("_n")


def comparison_groups(validation):
    """Places where methods were scored side by side ON THE SAME METRIC.

    A group is a parent whose numeric children compete. The metric comes from the child's own
    name (auroc_rarity_baseline) or else from the parent path (leave_one_out_auroc); a law and a
    baseline are only compared when they share it, and counts, deltas, slopes and differences are
    never treated as a method.
    """
    groups = []
    parents = []

    def walk(d, path, inherited=None):
        parent = parents[-1] if parents else None
        if not isinstance(d, dict):
            return
        if isinstance(d.get("metric"), str):
            inherited = metric_in(d["metric"]) or inherited
        nums = {}
        for k, v in d.items():
            if isinstance(v, bool):
                continue
            if isinstance(v, (int, float)):
                nums[k] = v
            elif isinstance(v, dict) and isinstance(v.get("mean"), (int, float)):
                nums[k] = v["mean"]
        path_metric = metric_in(path) or inherited
        by_metric = {}
        for k, v in nums.items():
            if _is(k, NOT_A_METHOD) or is_count(k):
                continue
            m = metric_in(k) or path_metric
            if m:
                by_metric.setdefault(m, []).append((v, k))
        for m, items in by_metric.items():
            base = [x for x in items if _is(x[1], BASE_KEYS) and "+" not in x[1]]
            law = [x for x in items if not _is(x[1], BASE_KEYS)]
            if not law or not base:
                continue
            lower = METRICS[m]
            pick = min if lower else max
            # The law's own score first: a key that IS the law (law, law.auroc, law_linear), never
            # the law with something added and never another predictor that merely sits beside it.
            own = [x for x in law if x[1].lower().startswith("law") and "+" not in x[1]]
            explicit = [x for x in law if _is(x[1], LAW_KEYS) and "+" not in x[1]]
            bl, bb = pick(own or explicit or law), pick(base)
            if m in ("auroc", "auc", "accuracy") and not (0 <= bl[0] <= 1 and 0 <= bb[0] <= 1):
                continue
            margin = (bb[0] - bl[0]) if lower else (bl[0] - bb[0])
            # bounded scores (AUROC, r2) are judged on the raw difference; errors with units
            # (RMSE in degrees, MAE) on the difference relative to the baseline's error
            bounded = m in ("auroc", "auc", "accuracy", "r2", "spearman", "pearson")
            rel = margin if bounded else margin / max(abs(bb[0]), 1e-9)
            ci = None
            for scope in (d, parent):
                diff = (scope or {}).get(f"{bl[1]} - {bb[1]}")
                if isinstance(diff, dict) and isinstance(diff.get("ci95"), list):
                    ci = diff["ci95"]
                    break
            groups.append({"where": path or "(최상위)", "metric": m, "law": bl[1], "law_value": bl[0],
                           "ci95": ci, "ci_holds_zero": bool(ci and ci[0] <= 0 <= ci[1]),
                           "baseline": bb[1], "baseline_value": bb[0], "lower_is_better": lower,
                           "primary": _is(path, PRIMARY) or _is(bl[1], PRIMARY),
                           "margin": round(margin, 4), "relative": round(rel, 4),
                           "bounded": bounded})
        for k, v in d.items():
            if isinstance(v, dict):
                parents.append(d)
                walk(v, f"{path} · {k}" if path else k, inherited)
                parents.pop()

    walk(validation or {}, "")
    return groups


# Not every law is a method race. Some ask whether an effect survives a confounder, others whether
# a law transfers, others describe structure; calling those "unclassified" hides what they are.
KINDS = {"교란 검정": ("confound", "phylo_check"),
         "전이 검정": ("animal_temperature",),
         "구조 분석": ("modules", "loss_order", "convergent", "family_sequence", "nestedness"),
         "규모 보고": ("severity_endosymbiosis", "coloss_environment", "endosymbiosis", "knockout")}


def kind_of(law_id):
    for k, pats in KINDS.items():
        if any(p in law_id for p in pats):
            return k
    return None


def decisive_tests(validation):
    """Differences a law reports itself with an interval, e.g. auroc_minus_no_selection_control:
    {"mean", "ci95"}. When a law states its own head-to-head test, that test decides the verdict,
    not whichever baseline happens to sit next to it (lab_evolution_v1 beat rarity but not the
    no-selection control, which is its actual claim)."""
    out = []

    def walk(d, path):
        if not isinstance(d, dict):
            return
        for k, v in d.items():
            if isinstance(v, dict):
                if "_minus_" in k and isinstance(v.get("mean"), (int, float)) and isinstance(v.get("ci95"), list):
                    out.append({"where": f"{path} · {k}" if path else k, "mean": v["mean"], "ci95": v["ci95"]})
                else:
                    walk(v, f"{path} · {k}" if path else k)

    walk(validation or {}, "")
    return out


# Pre-registered comparisons against an external reference that can adjudicate (built by a different
# method on different data). They outrank the law's own known-truth grade, which is measured on data
# simulated from the same model and cannot see that model's own bias. Laws are not rewritten; the
# correction is also in each law's caveats.
EXTERNAL_VERDICTS = {
    "leca_ancestor_v2": {"where": "외부 기준 · Vosseberg 2021 계통수 LECA (사전 등록 2)",
                         "law_value": 0.866, "baseline_value": 0.954, "mean": -0.088, "ci95": [-0.096, -0.080]},
    "leca_ancestor_v1": {"where": "외부 기준 · Vosseberg 2021 계통수 LECA (사전 등록 2, 보조)",
                         "law_value": 0.872, "baseline_value": 0.955, "mean": -0.083, "ci95": [-0.091, -0.076]},
}


def verdict_of(validation, law_id=""):
    """Did the law beat the baselines it was measured against? Read off the comparison groups."""
    groups = comparison_groups(validation)
    ext = EXTERNAL_VERDICTS.get(law_id)
    if ext:
        lo, hi = ext["ci95"]
        label = "양성" if lo > 0 else ("음성" if hi < 0 else "무승부")
        return label, ext["mean"], (groups or []) + [{
            "where": ext["where"], "metric": "auroc", "law": "법칙", "law_value": ext["law_value"],
            "baseline": "현생 빈도", "baseline_value": ext["baseline_value"], "ci95": ext["ci95"],
            "ci_holds_zero": lo <= 0 <= hi, "lower_is_better": False, "primary": True,
            "margin": ext["mean"], "relative": ext["mean"], "bounded": True, "decisive": True}]
    tests = decisive_tests(validation)
    if tests:
        t = tests[0]
        lo, hi = t["ci95"]
        label = "양성" if lo > 0 else ("음성" if hi < 0 else "무승부")
        return label, round(t["mean"], 4), groups + [{
            "where": t["where"], "metric": "difference", "law": "법칙 - 대조", "law_value": t["mean"],
            "ci95": t["ci95"], "ci_holds_zero": lo <= 0 <= hi, "baseline": "0", "baseline_value": 0.0,
            "lower_is_better": False, "primary": True, "margin": round(t["mean"], 4),
            "relative": round(t["mean"], 4), "bounded": True, "decisive": True}]
    # Ancestor reconstructions: the known-truth test (simulated families on the same tree) speaks
    # to the ancestor; leave-tips-out saturates in tight clades. Judge on the WORST known-truth
    # node (several root positions or nodes), against present-day frequency.
    kt = [x for x in groups if "known_truth" in x["where"] and x["metric"] == "auroc"
          and "subclades" not in x["where"] and "core_node" not in x["where"]]   # other nodes, not this law's
    if kt:
        g = min(kt, key=lambda x: x["relative"])
        r = g["relative"]
        return ("양성" if r > 0.01 else ("음성" if r < -0.01 else "무승부")), g["margin"], groups
    if not groups:
        if not validation:
            return "검증 없음", None, None
        return kind_of(law_id) or "미분류", None, None
    rank = {"auroc": 0, "auc": 0, "logloss": 1, "r2": 2, "rmse": 2, "mae": 2, "brier": 1,
            "spearman": 3, "pearson": 3, "accuracy": 1}
    g = sorted(groups, key=lambda x: (not x["primary"], rank.get(x["metric"], 9)))[0]
    r = g["relative"]
    label = "양성" if r > 0.01 else ("음성" if r < -0.01 else "무승부")
    if g.get("ci_holds_zero") and label != "무승부":
        label = "무승부"   # the interval of the difference holds zero: not separated
    return label, g["margin"], groups


def table(rows, head):
    out = ["| " + " | ".join(head) + " |", "|" + "|".join([" --- "] * len(head)) + "|"]
    for r in rows:
        out.append("| " + " | ".join(str(c) for c in r) + " |")
    return "\n".join(out)


def write(path, text):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


# ---------------------------------------------------------------- law cluster
def law_notes(out, law, env, experiments):
    lid = law["id"]
    cl = cluster_of(lid)
    label, margin, pair = verdict_of(law.get("validation"), lid)
    base = out / "01-법칙" / slug(lid)
    tags = [f"법칙/{lid}", f"클러스터/{cl}", f"판정/{label}"]
    link = lambda n: f"[[{lid} · {n}]]"  # noqa: E731

    hub = fm(유형="법칙 허브", 법칙=lid, 클러스터=cl, 판정=label,
             기준선대비=(margin if margin is not None else "—"), tags=tags)
    hub += f"# {lid}\n\n> [!abstract] 적용 범위\n> {law.get('scope', '—')}\n\n"
    hub += f"**모형** — {law.get('model', '—')}\n\n"
    if pair:
        hub += f"## 판정 — {label}\n\n"
        pair = sorted(pair, key=lambda x: (not x["primary"], x["metric"] != "auroc"))
        hub += table([[f'{g["where"]} ({g["metric"]})', f'`{g["law"]}` {num(g["law_value"])}',
                       f'`{g["baseline"]}` {num(g["baseline_value"])}',
                       f'{g["margin"]:+.4f}' + (f' [{num(g["ci95"][0])}, {num(g["ci95"][1])}]'
                                                 if g.get("ci95") else ""),
                       "낮을수록 좋음" if g["lower_is_better"] else "높을수록 좋음"]
                      for g in pair],
                     ["비교한 곳", "법칙", "기준선", "차이", "방향"]) + "\n\n"
        hub += ("판정은 표의 첫 줄(교차검증 쪽, AUROC 우선)로 매깁니다. 차이가 ±0.01 안이면 무승부. "
                "비교는 같은 지표끼리만 합니다.\n\n")
    else:
        why = {"교란 검정": "교란 변수를 넣었을 때 효과가 살아남는지를 묻는 검정입니다. "
                            "법칙 대 기준선의 경주가 아니라 '살아남음/탈락'이 결과입니다.",
               "구조 분석": "소실 순서·모듈·수렴 같은 구조를 기술하는 분석입니다. 기준선은 "
                            "경쟁 방법이 아니라 무작위 귀무분포입니다.",
               "규모 보고": "얼마나 잃는지를 보고하는 분석입니다.",
               "전이 검정": "한 계통에서 얻은 법칙이 다른 계통에도 통하는지 부호와 크기로 보는 검정입니다.",
               "검증 없음": "이 법칙 파일에는 검증 블록이 없습니다. 그 자체가 점검 대상입니다.",
               "미분류": "검증 블록에 법칙과 기준선을 나란히 둔 비교 묶음이 없습니다."}
        hub += f"## 판정 — {label}\n\n{why.get(label, '')} 수치는 [[{lid} · 검증]]에 그대로 있습니다.\n\n"
    hub += ("## 이 클러스터의 노트\n"
            f"- {link('계수')} — 학습된 가중치와 신뢰구간\n"
            f"- {link('검증')} — 기준선과 나란히 본 성적\n"
            f"- {link('한계')} — 이 법칙을 깨뜨리는 조건\n"
            f"- {link('환경')} — 어떤 환경의 종들에서 나왔나\n"
            f"- {link('데이터')} — 쓰인 종·쌍·유전자군\n\n")
    rel = [f"- [[{e}]]" for e in experiments.get(lid, [])]
    hub += "## 이 법칙을 만든 실험\n" + ("\n".join(rel) if rel else "- (연결된 실행 기록 없음)") + "\n\n"
    hub += f"## 클러스터\n- [[클러스터 · {cl}]]\n- [[법칙 목록]]\n"
    write(base / f"{lid}.md", hub)

    # --- coefficients
    ctx = law.get("contexts") or {}
    body = fm(유형="계수", 법칙=lid, 클러스터=cl, tags=tags + ["유형/계수"])
    body += f"# {lid} · 계수\n\n← [[{lid}]]\n\n"
    if not ctx:
        body += "이 법칙은 가중치 표 대신 사후확률·분포를 산출합니다. [[%s · 검증]]을 보세요.\n" % lid
    for cname, feats in ctx.items():
        if not isinstance(feats, dict):
            continue
        rows = []
        for f, v in feats.items():
            if isinstance(v, dict) and "weight" in v:
                ci = v.get("ci95") or ["—", "—"]
                crosses = (isinstance(ci[0], (int, float)) and isinstance(ci[1], (int, float))
                           and ci[0] <= 0 <= ci[1])
                rows.append([f"`{f}`", num(v["weight"]),
                             f"[{num(ci[0])}, {num(ci[1])}]",
                             "0 포함 — 효과 불확실" if crosses else ""])
            elif isinstance(v, (int, float)):
                rows.append([f"`{f}`", num(v), "—", ""])
        if rows:
            body += (f"## {cname}\n\n"
                     + table(rows, ["특성", "가중치", "95% 구간", "읽기"]) + "\n\n")
    write(base / f"{lid} · 계수.md", body)

    # --- validation
    body = fm(유형="검증", 법칙=lid, 클러스터=cl, 판정=label, tags=tags + ["유형/검증"])
    body += f"# {lid} · 검증\n\n← [[{lid}]]\n\n"
    body += ("> [!warning] 이 프로젝트의 규칙\n> 새 수치는 언제나 기준선(암기·희귀도·평균값)과 "
             "나란히 둡니다. 기준선을 못 넘으면 음성 결과로 기록합니다.\n\n")
    rows = []
    for k, v in flat(law.get("validation")).items():
        if isinstance(v, dict):
            ci = v.get("ci95") or ["—", "—"]
            rows.append([k, num(v.get("mean", "—")), f"[{num(ci[0])}, {num(ci[1])}]"])
        else:
            rows.append([k, num(v), "—"])
    body += (table(rows, ["항목", "값", "95% 구간"]) if rows else "(검증 항목 없음)") + "\n\n"
    body += "## 방법\n- [[잎 숨기기 검증]]\n- [[알려진 정답 모의]]\n- [[부트스트랩 신뢰구간]]\n"
    write(base / f"{lid} · 검증.md", body)

    # --- caveats, one bullet each so they can be cited separately
    body = fm(유형="한계", 법칙=lid, 클러스터=cl, tags=tags + ["유형/한계"])
    body += f"# {lid} · 한계\n\n← [[{lid}]]\n\n"
    cav = law.get("caveats") or []
    for i, c in enumerate(cav, 1):
        body += f"### 한계 {i}\n{c}\n\n"
    if not cav:
        body += "(기록된 한계 없음 — 그 자체가 점검 대상입니다.)\n"
    write(base / f"{lid} · 한계.md", body)

    # --- environment card
    body = fm(유형="환경", 법칙=lid, 클러스터=cl, tags=tags + ["유형/환경"])
    body += f"# {lid} · 환경\n\n← [[{lid}]]\n\n"
    if env:
        body += f"**카탈로그** {env.get('catalogue', '—')} · **종 수** {env.get('n_species', '—')}\n\n"
        for key, title in (("envelope", "환경 범위"), ("groups", "분류군 구성"),
                           ("gc", "GC 함량"), ("contrasts", "축별 대비"), ("findings", "요약 수치")):
            v = env.get(key)
            if not v:
                continue
            body += f"## {title}\n\n```json\n{json.dumps(v, ensure_ascii=False, indent=1)}\n```\n\n"
        if env.get("note"):
            body += f"> [!note]\n> {env['note']}\n"
    else:
        body += "환경 카드가 없습니다 (`scripts/build_law_environments.py`가 이 법칙을 다루지 않음).\n"
    write(base / f"{lid} · 환경.md", body)

    # --- data
    body = fm(유형="데이터", 법칙=lid, 클러스터=cl, tags=tags + ["유형/데이터"])
    body += f"# {lid} · 데이터\n\n← [[{lid}]]\n\n"
    d = law.get("data") or {}
    for k, v in d.items():
        if isinstance(v, list):
            body += f"## {k} ({len(v)}개)\n\n" + "\n".join(f"- {x}" for x in v[:60])
            if len(v) > 60:
                body += f"\n- … 외 {len(v) - 60}개"
            body += "\n\n"
        else:
            body += f"**{k}** — {v}\n\n"
    if law.get("feature_names"):
        body += ("## 특성 목록\n"
                 + "\n".join(f"- `{f}`" for f in law["feature_names"]) + "\n\n")
    body += "## 데이터셋 노트\n- [[데이터셋 · UniProt 프로테옴]]\n- [[데이터셋 · GTDB 종 대표]]\n"
    write(base / f"{lid} · 데이터.md", body)
    return lid, cl, label, margin


# ---------------------------------------------------------------- experiments
def experiment_notes(out):
    """One note per run that left a summary behind: what went in, what came out, what it settled."""
    made = defaultdict(list)
    names = []
    for f in sorted(list(RESULTS.glob("*/summary.json")) + list(RESULTS.glob("*/metrics.json"))
                    + list(RESULTS.glob("*/*/summary.json"))):
        rel = f.parent.relative_to(RESULTS).as_posix()
        name = f"실험 · {slug(rel)}"
        names.append((name, rel))
        try:
            data = json.loads(f.read_text())
        except Exception:
            continue
        tags = ["유형/실험", f"실험/{slug(rel)}"]
        body = fm(유형="실험", 실행=rel, 산출=f.as_posix(), tags=tags)
        body += f"# {name}\n\n**산출물** `{f.as_posix()}`\n\n"
        scalars = {k: v for k, v in data.items()
                   if isinstance(v, (int, float, str, bool)) or v is None}
        if scalars:
            body += ("## 한눈에\n\n"
                     + table([[k, num(v)] for k, v in scalars.items()], ["항목", "값"]) + "\n\n")
        for k, v in data.items():
            if k in scalars:
                continue
            txt = json.dumps(v, ensure_ascii=False, indent=1)
            if len(txt) > 1600:
                txt = txt[:1600] + "\n… (잘림 — 원본 파일 참조)"
            body += f"## {k}\n\n```json\n{txt}\n```\n\n"
        body += "## 연결\n- [[실험 목록]]\n"
        write(out / "02-실험" / f"{name}.md", body)
        for lid in re.findall(r"[a-z_]+_v\d", json.dumps(data)[:4000]):
            if lid not in made or name not in made[lid]:
                made[lid].append(name)
    return made, names


# ---------------------------------------------------------------- static notes
METHODS = {
    "진화 시뮬레이터 (사전 등록 8)": (
        "유전체(Pfam 유전자군)와 환경 일정·시간을 넣으면 법칙대로 가상 후손을 만듭니다. 기본 법칙 = G3c의 유전자군별 속도 분포, "
        "환경 법칙 = 독립 기원들에서 추정한 유전자군별 손실·획득 배수(축소 추정, 단세포 대조로 눈금). 서열은 만들지 않고, 새 유전자군을 발명하지 않습니다.\n\n"
        "**재연 시험(기원 하나 빼고)** — 무산소 손실: 환경 법칙이 기본 법칙보다 **+0.025 [+0.017, +0.031] (양성, 6/6 기원)**, 이전 전환 법칙보다 +0.11. "
        "기생 손실 +0.010 (무승부), 다세포 획득 +0.016 (무승부)이며 다세포 획득은 '흔한 유전자'에 −0.12로 짐.\n\n"
        "**예시** — LECA + 무산소: COX17 0.69→0.02, UCR_hinge 0.72→0.05, PFOR_II 0.11→0.71 획득, Fe-S 조립 유지(교과서적 그림과 일치).\n\n"
        "**새 환경(사전 등록 9)** — 편모 상실 +0.019 [+0.005, +0.029] 양성(4/5 기원; LECA에서 편모 유전자 16개 중 15개가 더 빨리 사라짐, IFT20 0.68→0.12), "
        "광합성 상실 무승부(2기원), 산성·고온 근거 부족(2기원).\n\n"
        "구현: `scripts/evo_simulator.py`. 결과: `results/simulator/`, `docs/preregistration/2026-10-10_evolution_simulator_RESULT.md`, "
        "`docs/preregistration/2026-10-10_simulator_new_environments_RESULT.md`. 실험대 페이지: https://claude.ai/artifact/Arrb4W78W9nftbhDEf9jB6"),
    "통합 모형 G3 (사전 등록 7)": (
        "격자 위 속도분포를 EM으로 배우는 경험적 베이즈 + 원핵 분포 3층별 사전분포 + 축소 갈래 손실 배수(가능도로 선택) + 엽록체 전달 처리. "
        "모든 매개변수를 유전체 자료만으로 정합니다.\n\n"
        "| 시험 | G3 | M7 | 종수 세기 |\n|---|---|---|---|\n"
        "| 초군 가리고 예측(주) | 9개 평균 M7보다 **+0.0036 [+0.0028, +0.0044]** | — | G3가 +0.057 |\n"
        "| 다른 방식 가짜 진화 | **0.951** | 0.937 | 0.915 |\n"
        "| Vosseberg 시험 절반(참고) | 0.900 | **0.926** | 0.957 |\n\n"
        "**읽기** — 얕은 마디(초군 조상)와 가짜 진화에서는 G3가 이기고, 가장 깊은 LECA를 외부 판정과 비교하면 M7이 이깁니다. 속도분포 학습만으로 "
        "Vosseberg 점수가 0.926 → 0.894(탐색적). 원핵층은 원핵에 흔한 유전자군의 획득/손실 비를 2.93으로 배웠습니다(원핵에 없음 0.62). "
        "LECA 3판 법칙으로 고정하지 않음: 초군 예측엔 G3c, LECA 판정엔 M7+H2가 각각 최선.\n\n"
        "구현: `scripts/leca_v3_model.py`. 결과: `results/leca_v3/`, `docs/preregistration/2026-10-10_leca_v3_model_RESULT.md`."),
    "원핵생물 분포로 LECA 판정 보정 (사전 등록 5C)": (
        "유전자군마다 UniProt 고세균(628종)·세균(17,441종) 중 가진 비율을 진핵 빈도와 함께 로지스틱 회귀에 넣고(보정 절반으로 학습), "
        "Vosseberg 2021 계통수 LECA의 시험 절반으로 채점했습니다.\n\n"
        "| 모형 | 시험 AUROC |\n|---|---|\n| 현생 빈도 | 0.957 |\n| **빈도 + 원핵 분포** | **0.974** |\n| + 트리 모형 | 0.973 |\n\n"
        "**처음으로 종수 세기를 이김**: +0.017 [+0.013, +0.021] (양성). 트리 모형은 더 보태지 못함(−0.001, 무승부).\n\n"
        "**방향** — 세균 계수가 음수(−0.39): 같은 진핵 빈도라면 세균에 흔할수록 LECA가 아닐 가능성이 높습니다(원핵에도 있으면 LECA 0.62, "
        "진핵에만 있으면 0.87). 세균 → 진핵 수평이동의 신호이거나, 원핵 서열을 함께 넣어 나무를 그린 기준의 성질입니다(구별 불가).\n\n"
        "구현: `scripts/prokaryote_and_loso.py` (part_c). 결과: `results/leca_models/prokaryote_and_loso.json`."),
    "초군 가리고 예측하기 (사전 등록 5D)": (
        "초군 하나(잎 10개 이상인 9개)의 잎을 모두 숨기고, 나머지로 그 초군이 가진 유전자군을 예측합니다. 외부 라벨이 아니라 실제 관측으로 "
        "채점하므로 누구의 LECA 정의에도 기대지 않습니다.\n\n"
        "나무(M7의 그 초군 공통조상 사후확률) vs 종수 세기: 평균 **+0.053 [+0.052, +0.055] (양성), 9개 초군 모두 나무가 이김** "
        "(Metazoa 0.865 vs 0.769, Viridiplantae 0.925 vs 0.840). '초군 절반 이상에 있음' 기준으로도 +0.015 (8/9). "
        "탐색적으로 '가까운 친척에서만 세기'와 비교해도 9개 모두 나무가 이김.\n\n"
        "**읽기** — 나무는 세기 이상의 정보를 줍니다. Vosseberg 기준에서 나무가 진 것은 그 기준이 종수 세기에 유리하기 때문일 가능성이 큽니다.\n\n"
        "구현: `scripts/prokaryote_and_loso.py` (part_d)."),
    "내공생 유전자 전달 처리 (색소체 편중 유전자군)": (
        "엽록체는 LECA 뒤에 생겼지만, 2·3차 내공생으로 엽록체 유래 유전자가 여러 초군에 옆으로 퍼집니다. 획득/손실 모형은 이것을 "
        "'LECA에 있었고 여러 번 잃음'으로 읽습니다. 처리: 색소체 계통(녹색식물, 홍조류, 회색조류, 황색조류, 착편모조류, 은편모조류, 와편모조류, "
        "유글레나조류, 클로라라크니온, 크로메라, 정단복합체, 볼리도조류)의 빈도가 나머지의 2배를 넘는 유전자군에 한해, 그 잎들을 관측 안 됨으로 두고 다시 계산합니다.\n\n"
        "**사전 등록 4B 결과** — Vosseberg 2021 시험 절반에서 0.926 → 0.930, +0.0034 [+0.0008, +0.0060] (양성). 광합성 음성 대조 5개가 모든 뿌리에서 "
        "0.000으로 통과(처리 전 PsaA_PsaB 0.15–0.27로 실패). 예측 네 가지 모두 맞음. 현생 빈도는 여전히 못 이김(−0.027). "
        "세균 → 진핵 수평이동은 다루지 못합니다(서열 계통 필요).\n\n"
        "구현: `scripts/tree_scramble_transfer.py` (H2). 관련: [[2상태 마르코프 모형]] · [[수평 전달 추정량]]"),
    "2상태 마르코프 모형": (
        "유전자군마다 '있음/없음' 두 상태를 두고, 가지 길이에 따라 획득률 g와 손실률 lo로 상태가 "
        "바뀐다고 봅니다. 잎의 관측에서 Felsenstein 가지치기로 가능도를 구하고, (g, lo)를 격자 "
        "최대우도로 유전자군마다 따로 맞춥니다. 조상 상태는 위-아래 전달로 얻은 주변 사후확률입니다.\n\n"
        "구현: `scripts/mito_model_search.py`의 `loglik`/`posterior`, `scripts/run_mito_ancestor.py`의 "
        "`loglik_grid`/`marginals`.\n\n관련: [[완전도 관측 모형]] · [[수평 전달 추정량]]"),
    "완전도 관측 모형": (
        "불완전한 프로테옴은 실제로 가진 유전자를 놓칩니다. 완전도 c인 잎에서 "
        "P(관측 없음 | 실제 있음) = 1 − c 로 두고 가능도에 직접 넣습니다. c = 1이면 예전 지시함수와 "
        "같아져 기존 결과가 바뀌지 않습니다.\n\n"
        "**왜 가지 손실 가속이 아닌가** — 예전에는 불완전한 잎의 가지 손실률을 올려 땜질했습니다. "
        "알려진 정답 모의에서 관측 모형이 더 정확했고(크기 편향 −7.9% → −6.6%), 두 보정을 함께 걸면 "
        "같은 것을 두 번 보정하게 됩니다.\n\n"
        "완전도는 자료에서 직접 추정합니다: 그 분류군의 상위 4분위 프로테옴이 거의 다 가진 마커 "
        "유전자군을 뽑고, 각 종이 그중 몇 %를 가졌나로 점수를 냅니다.\n\n"
        "구현: `scripts/genome_quality.py` · 검증: [[실험 · quality_correction]]"),
    "수평 전달 추정량": (
        "유전자군마다 상한 없는 격자로 획득/손실 비 q를 맞추고, q ≥ 0.3인 유전자군의 비율을 봅니다. "
        "전달이 많으면 친척이 아닌 종에 같은 유전자군이 나타나고, 모형은 그것을 획득률을 올려서만 "
        "설명할 수 있습니다.\n\n"
        "그 통계량 자체는 뜻이 없으므로 **같은 나무 위에서 전달 수준을 알고 돌린 모의**로 보정 곡선을 "
        "만들어 읽습니다.\n\n"
        "> [!warning] 상한으로 읽을 것\n"
        "> 이 추정량은 전달과 '원래 획득이 잦은 것'(중복·신규 생성·수렴 획득)을 구분하지 못합니다. "
        "> 또 곡선이 전달 0.1 위에서 포화해 '0.35 아래인가'에만 답합니다.\n\n"
        "구현: `scripts/hgt_rate.py` · 한계 측정: `scripts/hgt_limit.py`"),
    "잎 숨기기 검증": (
        "잎 몇 개를 가리고 나머지로 그 종의 유전자 구성을 맞히게 합니다. 기준선은 계통수를 전혀 쓰지 "
        "않는 현생 빈도입니다.\n\n"
        "> [!danger] 이 시험이 재는 것은 조상이 아닙니다\n"
        "> 현생 종을 맞히는 시험입니다. 한 분류군의 종들이 서로 비슷하면 기준선만으로 0.99가 나와 "
        "> 변별력이 사라집니다. 리케차목에서 실제로 그랬고(+0.0005), 그것을 '복원이 쓸모없다'로 읽은 "
        "> 것은 오판이었습니다. [[정정 · 리케차목 판정 철회]]\n\n"
        "짝이 되는 시험: [[알려진 정답 모의]]"),
    "알려진 정답 모의": (
        "실제 계통수 위에서 유전자군을 진화시켜 **모든 마디의 참값을 기록**한 뒤, 잎만 보고 복원해 "
        "그 마디의 참값과 대조합니다. 조상을 직접 채점하므로 꽉 짜인 분류군에서도 변별력이 있습니다.\n\n"
        "재는 것: AUROC(순위), 로그손실(확률 보정), 크기 편향(조상 유전자군 수 오차).\n\n"
        "> [!tip] 기준선이 0.99를 넘으면\n"
        "> 순위에는 이길 여유가 남아 있지 않으므로 로그손실로 판정합니다.\n\n"
        "구현: `scripts/node_power.py` · 표본 크기 판: `scripts/sample_size_limit.py`"),
    "부트스트랩 신뢰구간": (
        "구간은 종이 아니라 **계통 단위로 재표집**합니다. 같은 계통의 종들은 독립 관측이 아니므로 "
        "종 단위 재표집은 구간을 가짜로 좁힙니다. 계통수 자체의 불확실성은 부트스트랩 나무 20그루에 "
        "같은 복원을 돌려 퍼짐으로 넣습니다."),
    "표본 크기의 한계": (
        "알려진 정답 모의에서 표본을 깎아가며 잰 값입니다.\n\n"
        + table([["12종", "0.965", "−15.8%", "0%"], ["50종", "0.974", "−10.3%", "0%"],
                 ["300종", "0.977", "−9.9%", "0%"], ["2,323종(전부)", "0.986", "−8.6%", "100%"]],
                ["표본", "순위 정확도", "크기 오차", "분류군 뿌리 도달"])
        + "\n\n**읽는 법** — 순위는 적은 표본으로도 거의 다 맞힙니다. 크기는 12→50에서 좋아지고 멈추며 "
          "전부 넣어도 −8.6%에서 바닥입니다(모든 후손이 함께 잃은 유전자군은 보이지 않음). "
          "종을 늘려야만 풀리는 것은 **어느 마디에 도달하느냐**입니다.\n\n"
        "개수보다 퍼짐이 중요합니다: 쏠린 50종(0.962) < 퍼진 50종(0.974).\n\n"
        "구현: `scripts/sample_size_limit.py`"),
}

DATASETS = {
    "데이터셋 · UniProt 프로테옴": (
        "UniProt이 미리 계산한 Pfam 교차참조로 프로테옴마다 유전자군 보유 여부를 셉니다. HMMER를 "
        "직접 돌리지 않으므로 수만 종이 가능합니다.\n\n"
        "**알려진 흠** — 중복 프로테옴은 서열이 빠져 있어 기록만 남습니다(세균 11.2%, 진핵 31.7%가 "
        "빈 Pfam). 같은 종이 여러 샤드에 들어가 유전자군 수가 다를 수 있습니다(545종). 바이러스는 "
        "BUSCO가 없습니다.\n\n수집: `scripts/uniprot_proteomes.py`"),
    "데이터셋 · GTDB 종 대표": (
        "세균·고세균 종 대표 계통수(bac120/ar53)와 분류 체계. 조상 복원의 나무가 여기서 옵니다.\n\n"
        "수집: `scripts/fetch_gtdb.py`"),
    "데이터셋 · 리보솜 마커 계통수": (
        "카탈로그에 없는 분류군(아메보조아 등)은 같은 UniProt 프로테옴에서 리보솜 단백질 마커를 뽑아 "
        "정렬(mafft)하고 나무를 세웁니다(FastTree).\n\n"
        "**알려진 흠** — 마커가 거의 없는 종을 커버리지 필터 앞에서 떨어뜨리지 않으면 정렬이 비어 "
        "별 모양 나무가 나옵니다(첫 아메바 나무가 그랬음).\n\n"
        "수집: `scripts/uniprot_markers.py` · 구축: `scripts/ribosomal_tree.py`"),
}


CORRECTIONS = {
    "정정 · 볼트 판정기가 단위가 다른 수치를 비교했음": (
        "**무엇이 틀렸나** — 볼트를 처음 넘겼을 때 판정기가 이름만 보고 법칙과 기준선을 짝지어서 "
        "단위가 다른 수치를 비교했습니다. `animal_content_v1`은 '축이 더 나았던 쌍의 수 9'를 "
        "AUROC 0.836과 비교해 **음성 법칙을 양성 +8.16으로** 찍었고, `sequence_v1`은 회귀 기울기를 "
        "RMSE와, `mito_ancestor_v1`은 경로 이름의 'loss_biased'를 보고 AUROC를 '낮을수록 좋음'으로 "
        "뒤집었습니다. `loss_prediction_v1`은 법칙 단독(0.793)이 아니라 근친 정보를 더한 값(0.925)을 "
        "법칙 성적으로 집었습니다.\n\n"
        "**고친 것** — 같은 지표(AUROC끼리, RMSE끼리)만 비교합니다. 개수·차이·기울기는 방법으로 "
        "취급하지 않습니다. 법칙 단독 성적을 우선합니다. 단위가 있는 오차는 기준선 대비 비율로 "
        "판정합니다. 차이의 신뢰구간이 기록돼 있으면 그것이 0을 포함할 때 무승부로 내립니다.\n\n"
        "**결과** — 양성 16 → **9**, 음성 7 → **9**. 양성으로 잘못 찍혔던 것: animal_content_v1, "
        "loss_prediction_v1, context_features_v1(법칙 단독은 암기에 짐), genome_traits_v1(구간이 0 포함 "
        "→ 무승부). 이 경우들은 테스트로 고정했습니다(`tests/test_lab_vault.py`).\n\n"
        "**교훈** — 자동 판정은 '그동안 손으로 확인한 결론'과 대조하기 전까지 믿으면 안 됩니다."),
    "정정 · 판정기가 법칙 자신의 질문을 보지 않았음": (
        "**무엇이 틀렸나** — 두 가지였습니다. (1) `lab_evolution_v1`이 **양성**으로 찍혔습니다. 판정기가 "
        "옆에 있던 희귀도 기준선(0.590 대 0.566)만 봤기 때문입니다. 이 법칙이 묻는 것은 '선택압 없는 대조군보다 "
        "나은가'이고, 그 차이는 −0.005 [−0.067, +0.056]로 0을 포함합니다. (2) 조상 복원 법칙들은 포화된 잎 "
        "숨기기 검증으로 판정됐고, 알려진 정답 채점에서는 현생 빈도 기준선(`freq_auroc`)을 기준선으로 알아보지 "
        "못해 사전확률과 비교했습니다. 그래서 알려진 정답이 분명히 좋은 `plastid_ancestor_v1`이 무승부로 "
        "찍혔습니다.\n\n"
        "**고친 것** — 법칙이 스스로 '법칙 − 대조' 차이와 신뢰구간을 기록해 두었으면 그 검정이 판정을 정합니다. "
        "조상 법칙은 그 법칙 자신의 마디(하위 분류군·핵심 마디 제외)의 알려진 정답 AUROC를 현생 빈도와 비교하고, "
        "뿌리 위치가 여러 개면 가장 나쁜 뿌리로 판정합니다.\n\n"
        "**결과** — lab_evolution_v1 양성 → **무승부**(선택의 몫이 대조군과 구별되지 않음), plastid_ancestor_v1 "
        "무승부 → **양성**. 다른 법칙의 판정은 바뀌지 않았습니다(이전 판정기와 전수 비교). 테스트로 고정했습니다.\n\n"
        "**남은 것** — `mito_ancestor_v1`과 아메바 법칙들은 알려진 정답 채점이 법칙 파일이 아니라 "
        "`results/node_power/`에만 있어서 여전히 잎 숨기기로 판정됩니다(미토콘드리아 무승부). 법칙 파일은 "
        "덮어쓰지 않으므로, 새 판(_v2/_v5)을 만들 때 채점을 함께 넣어야 바뀝니다."),
    "정정 · 리케차목 판정 철회": (
        "**무엇을 말했나** — 잎 숨기기에서 리케차목이 0.988 vs 기준선 0.988(+0.0005)이므로 "
        "'계통수가 아무것도 벌어주지 못한다'고 보고했습니다.\n\n"
        "**무엇이 틀렸나** — 그 시험은 조상이 아니라 현생 종을 맞히는 시험입니다. 53종이 유전자군을 "
        "거의 다 공유하므로 기준선만으로 0.988이 나오고, 남은 여유가 0.012뿐이라 좋은 복원과 "
        "쓸모없는 복원을 구별할 수 없습니다. 문제는 복원이 아니라 측정 도구였습니다.\n\n"
        "**다시 재니** — 알려진 정답으로 조상을 직접 채점하면 리케차목은 **계통수 효과가 가장 큰 "
        "마디**입니다(0.975 vs 0.908, +0.067).\n\n"
        "**대신 진짜 문제** — 크기 오차가 −37%로 다른 마디(−1% 안팎)와 비교가 안 됩니다. 축소 계통이라 "
        "모든 후손이 함께 잃은 유전자군이 많기 때문이고, 따라서 보고된 소실 폭은 **과장이 아니라 "
        "축소된** 값입니다.\n\n관련: [[잎 숨기기 검증]] · [[알려진 정답 모의]]"),
    "정정 · 마커 선택이 실행마다 달랐음": (
        "동점인 유전자군을 파이썬 `set` 순회 순서로 끊었는데 문자열 해시가 프로세스마다 무작위입니다. "
        "같은 코드·같은 데이터로 두 번 돌리면 완전도가 ±0.02 흔들리고 유전자군의 0.54%가 0.1 이상 "
        "움직였습니다. 이름순으로 고정하고 해시 시드 3개로 동일함을 확인했습니다.\n\n"
        "**교훈** — 재현되지 않는 수치는 결과가 아닙니다."),
    "정정 · 검증한 추정량이 쓰는 추정량과 달랐음": (
        "완전도 보정을 검증하는 스크립트가 추정 함수를 자체 구현해서 쓰고 있었고, 그 구현은 "
        "거의 보편적인 유전자군이 하나도 없으면 조용히 적중률 상위 150개로 대체했습니다. "
        "실제로 쓰는 쪽은 그럴 때 보정을 아예 하지 않습니다.\n\n"
        "같은 함수를 쓰도록 통일하고 재검증 → 결과 동일(−6.6%). 버그는 실재했으나 결론까지 닿지는 "
        "않았습니다."),
    "정정 · 품질 보정을 반쪽만 걸었음": (
        "완전도를 분류군 안쪽에만 매기고 외군의 불완전한 프로테옴은 그대로 '잃었다'로 읽히게 두었습니다. "
        "외군도 전체 속도 적합에 들어가므로 결과를 끌어당깁니다. 양쪽을 따로 채점하니 검증 0.926 → "
        "0.931, 확신 유전자군 2,045 → 2,693.\n\n"
        "그리고 축소 계통 손실 가속은 원래 불완전성 땜질을 겸하던 것이라 **이중 보정**이었습니다. "
        "끄니 0.936으로 최선."),
    "정정 · 바이러스가 아메바로 분류될 수 있었음": (
        "종을 이름 첫 단어로만 분류해서 `Acanthamoeba polyphaga mimivirus`(바이러스)가 아메보조아로 "
        "잡힙니다. 당시 나무에는 없어 피해는 없었지만, 이제 계(kingdom)까지 확인합니다."),
    "정정 · 온도 법칙의 부호 역전 주장 철회": (
        "미토콘드리아 단백질체에서 본 부호 역전은 미토콘드리아 AT 편향의 성질이었습니다. 핵 "
        "단백질체에서 온도 계수는 미생물과 **부호가 같고** 5배 약합니다. "
        "'전이하면 안 된다'는 결론은 두 자료 모두에서 유지되지만 '법칙이 뒤집힌다'는 주장은 "
        "철회합니다."),
}

NEGATIVES = {
    "판정 보류 · 유전자 계통수의 '수평이동 지지'는 나무 크기로 설명된다 (사전 등록 6)": (
        "유전자군 268개(빈도 맞춘 Vosseberg LECA 134 / 비LECA 134), 진핵 300종 + 원핵 130종(GTDB 63개 문)으로 나무 248개를 그렸습니다.\n\n"
        "등록한 판정: 상관(세균 비율, '확실히 갈라진 진핵 기원 ≥ 2' | 진핵 빈도) = 0.367 [0.250, 0.474] → 규칙상 '해석 1(수평이동) 지지'. "
        "그러나 그 지표가 91%의 유전자군에서 참이고(파랄로그·여러 LECA 유전자군 때문), 세균 비율은 나무 속 원핵 서열 수와 거의 같습니다(0.887). "
        "원핵·진핵 잎 수를 통제하면 0.095 [−0.053, +0.237]로 사라집니다(탐색적). Q1 예측(비LECA에서 더 흔함)도 틀림.\n\n"
        "**남는 결론** — 수평이동인지 착시인지는 아직 가리지 못했습니다. 등록 단계에서 나무 크기를 통제하지 않은 설계 실수이며, 원핵 서열 수를 "
        "맞춘 나무로 새 사전 등록이 필요합니다.\n\n"
        "- 결과: `results/gene_trees/summary.json` · `docs/preregistration/2026-10-09_gene_trees_RESULT.md`"),
    "음성 · 실제 계통수가 종 이름을 섞은 나무보다 외부 LECA 판정과 덜 맞는다 (사전 등록 4A)": (
        "사전 등록(`docs/preregistration/2026-10-09_tree_scramble_and_transfer.md`) 그대로, 최선 모형 M7을 실제 나무, 종 이름을 섞은 "
        "나무 5개, 별 모양 나무에서 돌려 Vosseberg 2021 시험 절반과 비교했습니다.\n\n"
        "| 나무 | 시험 AUROC |\n|---|---|\n| 실제 | 0.926 |\n| 이름 섞음(5회 평균) | 0.955 |\n| 별 모양 | 0.936 |\n| 현생 빈도 | 0.957 |\n\n"
        "실제 − 섞음 = −0.029 [−0.035, −0.022] → 음성. 예측('0 근처')은 틀렸습니다. 유전체 자료의 가능도는 실제 나무가 훨씬 높습니다.\n\n"
        "**탐색적 진단** — 초군마다 고르게 센 빈도(0.943), 초군 수(0.933)도 그냥 센 빈도(0.954)보다 낮습니다. 계통적 중복을 바로잡을수록 "
        "외부 기준과 멀어집니다. 그들의 LECA 판정에 '종 범위 15% 이상 덮음' 조건이 있어 종 수 세기가 구조적으로 유리할 수 있습니다(사후 해석).\n\n"
        "**남는 결론** — 이 외부 기준에서는 계통수가 빈도 이상의 정보를 주지 못하고 오히려 손해입니다. 그것이 모형의 결함인지 기준의 성질인지는 "
        "덮음 조건이 없는 다른 외부 기준으로만 가릴 수 있습니다. 구현 중 별 모양 나무의 수치 버그(250갈래 곱이 0으로 떨어짐)를 고쳤고 이전 결과와는 무관합니다.\n\n"
        "- 결과: `results/leca_models/scramble_transfer.json` · `docs/preregistration/2026-10-09_tree_scramble_and_transfer_RESULT.md`"),
    "음성 · 10가지 LECA 모형 모두 현생 빈도를 못 이긴다 (사전 등록 3)": (
        "사전 등록(`docs/preregistration/2026-10-08_leca_model_variants.md`, 모형을 돌리기 전 커밋)대로 Vosseberg 2021 계통수 LECA를 "
        "보정 절반·시험 절반(Pfam md5)으로 나눠 시험했습니다.\n\n"
        "| 모형 | 시험 AUROC | − 현생 빈도 [95%] |\n|---|---|---|\n"
        "| M0 현재(유전자군별 자유 획득률) | 0.865 | −0.092 [−0.104, −0.080] |\n"
        "| **M7 공통 획득/손실 비(0.2)** | **0.926** | **−0.031 [−0.037, −0.024]** |\n"
        "| M9 공통 비 + 공통 뿌리 π | 0.912 | −0.045 |\n"
        "| 뿌리 사전확률만 바꾼 M1·M2·M8 | 0.79–0.85 | −0.11 ~ −0.17 |\n"
        "| 선택된 S2(빈도 + M0, 학습) | 0.957 | +0.0005 [−0.0006, +0.0015] → 무승부 |\n\n"
        "**읽기** — 원인은 유전자군마다 자유로운 획득률(과적합): 공통 비로 묶으면 외부 일치가 0.865 → 0.926으로 오르지만, 우리 유전체의 "
        "가능도는 오히려 낮아집니다(가능도가 높은 모형이 조상에서는 더 틀림). 그래도 트리 모형 10개 모두 빈도에 지고, 학습형에서 M0의 계수는 "
        "0.067로 빈도에 거의 보태지 못합니다. 예측 3개 중 2개 틀림(뿌리 사전확률이 원인이라는 예측, 학습형이 빈도를 이긴다는 예측).\n\n"
        "**남는 결론** — Pfam 유무 행렬 + 리보솜 계통수로는 LECA 판정에서 '몇 종이 가졌나' 이상의 정보를 못 뽑습니다. 넘으려면 유전자군 안의 서열 계통이 필요합니다.\n\n"
        "- 결과: `results/leca_models/summary.json` · `docs/preregistration/2026-10-08_leca_model_variants_RESULT.md` · [[leca_ancestor_v2]]"),
    "음성 · 계통수로 확인한 LECA 목록과도 현생 빈도를 못 이긴다 (사전 등록 2)": (
        "사전 등록(`docs/preregistration/2026-10-08_external_benchmark_phylogenetic.md`, 자료를 받기 전 커밋) 그대로 비교했습니다. "
        "대상은 Vosseberg 등 2021(Nat Ecol Evol)이 Pfam마다 계통수를 그려 판정한 LECA 유전자군. 분포 넓이가 아니라 나무 모양으로 정한 "
        "기준이라 1차(Dollo)와 달리 판정력이 있습니다. 공통 Pfam 5,489개, 그중 그들 LECA 3,858개.\n\n"
        "| 비교 | 우리 AUROC | 현생 빈도 | 차이 [95%] | 판정 |\n|---|---|---|---|---|\n"
        "| LECA 2판(뿌리 4곳 최솟값) | 0.866 | 0.954 | −0.088 [−0.096, −0.080] | 음성 |\n"
        "| LECA 1판(보조) | 0.872 | 0.955 | −0.083 [−0.091, −0.076] | 음성 |\n\n"
        "뿌리 하나씩 써도 모두 음성(−0.056 ~ −0.101). **두 예측 모두 틀렸습니다** — 차이 > 0, 빈도 층화 AUROC > 0.55(실제 0.543 [0.501, 0.588]).\n\n"
        "**탐색적 진단** — 오늘날 20–50%의 종에 있는 유전자군 1,397개를 계통수는 78% LECA로 보는데 우리 평균 사후확률은 0.29. "
        "우리 모형은 대량 손실을 과소평가하고 뒤늦은 획득을 과대평가합니다. 같은 Pfam 안에서 LECA 크기를 15–26% 작게 잡습니다"
        "(그들 3,858 vs 우리 2,866–3,278). 알려진 정답 채점은 같은 모형으로 만든 모의 자료라 이 구조적 편향을 볼 수 없었습니다.\n\n"
        "**남는 결론** — 진핵생물에서 '흔함'은 LECA 기원의 매우 강한 신호(계통수 판정과 AUROC 0.954)이고, 우리 모형은 그것을 깎아 먹습니다. "
        "LECA 크기 인용(3,919–4,601)은 과소 추정일 가능성이 높습니다. 고치려면 획득률 사전분포나 손실 편향 모형을 새 사전 등록으로 시험해야 합니다.\n\n"
        "- 결과: `results/external_benchmark/phylogenetic.json` · `docs/preregistration/2026-10-08_external_benchmark_phylogenetic_RESULT.md` · [[leca_ancestor_v2]] · [[leca_ancestor_v1]]"),
    "음성 · 외부 복원과의 일치에서 현생 빈도를 못 이긴다 (사전 등록)": (
        "사전 등록(`docs/preregistration/2026-10-08_external_benchmark.md`, 자료를 열기 전 커밋) 그대로 비교했습니다. "
        "대상은 Zmasek & Godzik 2011(114개 유전체, Dollo 절약법, Pfam 24.0)의 조상 Pfam 집합.\n\n"
        "| 비교 | 우리 AUROC | 현생 빈도 | 차이 [95%] | 판정 |\n|---|---|---|---|---|\n"
        "| LECA 2판 | 0.900 | 0.912 | −0.012 [−0.021, −0.003] | 음성 |\n"
        "| LECA 1판 | 0.904 | 0.911 | −0.007 [−0.015, +0.002] | 무승부 |\n"
        "| 균류 | 0.866 | 0.930 | −0.064 [−0.077, −0.050] | 음성 |\n\n"
        "**예측은 틀렸습니다** — '우리 복원이 빈도보다 0.02 이상 높다'고 등록했습니다. 보조 예측(정밀도 > 재현율)은 맞았습니다: "
        "정밀도 0.996, 재현율 0.46.\n\n"
        "**탐색적 진단(판정을 바꾸지 않음)** — 그들의 LECA 집합은 '뿌리 양쪽에 한 종이라도 있으면 있음'과 100% 같습니다(Dollo의 정의). "
        "우리가 없다고 본(P<0.1) 1,253개 중 세균 유전자로 보이는 것(DnaA, 편모 FliH, DNA 중합효소 III 등)이 있지만 소수이고, "
        "대부분은 오늘날 21% 안팎의 종에 흩어진 유전자군입니다. 두 방법이 갈리는 곳이 정확히 '다시 얻을 수 있는가'라는 가정이라, "
        "이 비교는 어느 쪽이 맞는지 가려 주지 못합니다. 그리고 빈도가 그들과 더 잘 맞는 이유도 Dollo 집합이 분포의 넓이로 정해지기 때문일 수 있습니다.\n\n"
        "**남는 결론** — 외부 검증 첫 시도는 우리 방법의 우위를 보여 주지 못했습니다. 판정할 수 있는 외부 기준은 방법 가정이 다른 "
        "절약법 집합이 아니라, 계통수로 하나하나 확인한 목록(예: 유전자별 계통 분석으로 만든 LECA 목록)이어야 합니다.\n\n"
        "- 결과: `results/external_benchmark/summary.json` · [[leca_ancestor_v2]] · [[fungal_ancestor_v1]]"),
    "음성 · 환경 축은 무엇을 잃을지 예측하지 못한다": (
        "86종 54쌍에서 환경 축을 넣은 법칙 0.8142 vs 축 없는 법칙 0.8133 — 차이 −0.000 "
        "[−0.004, +0.003]. 데이터를 43 → 54쌍으로 늘려도 같습니다.\n\n"
        "**읽기** — 무엇을 잃을지는 환경이 아니라 유전자군 자체의 성향이 정합니다.\n\n"
        "- [[environment_v3]] · [[environment_v2]] · [[environment_v1]]"),
    "음성 · 동물 유전자 구성도 같은 결론": (
        "23쌍 17기원: 희귀도 기준선 0.836 > 축 없는 법칙 0.801 > 축 법칙 0.794. 축을 넣는 효과 "
        "−0.007 [−0.018, +0.001], 기준선 대비 −0.042 [−0.084, −0.008].\n\n"
        "잡음 바닥이 0.01이므로 축 효과는 잡음 수준입니다. 미생물에서 얻은 결론이 동물에서도 "
        "같습니다.\n\n- [[animal_content_v1]]"),
    "음성 · 법칙은 대체로 암기를 이기지 못한다": (
        "처음 보는 계통 전이에서 법칙 0.760 vs 암기 0.785 vs 복제수만 0.647(15개 계통). "
        "형제 계통 천장은 기생 0.895 / 극한 0.853이고, 법칙 0.78·암기 0.80이 현실적 상한 "
        "근처입니다."),
    "음성 · 수억 년 법칙은 5만 세대 실험에 통하지 않는다": (
        "LTEE 대장균 303클론 + 돌연변이 축적 15클론: 비교진화로 만든 소실 법칙이 실험 결실을 거의 "
        "못 맞힙니다(AUROC 0.59). 선택압이 거의 없는 대조군도 0.60으로 같아서 차이 −0.005 "
        "[−0.067, +0.056] — **선택이 하는 몫이 검출되지 않습니다**.\n\n"
        "속도 1,000세대당 4.0개, 5만 세대에 약 200개 — 우리가 다루는 축소 유전체(수백~수천 소실)와 "
        "규모가 다릅니다.\n\n- [[lab_evolution_v1]]"),
    "음성 · 미생물 법칙은 동물 세포에 전이되지 않는다": (
        "동물 69종 핵 단백질체 직접 학습: 조성 지표 9개 전부 분류군 하나를 빼면 평균 기준선보다 "
        "못합니다. 분류군 수준 재학습에서는 삼투압 → 측쇄 질소(−0.0057, p 0.010)만 남습니다.\n\n"
        "**읽기** — 동물 조성은 환경보다 계통이 정합니다.\n\n"
        "- [[animal_axes_v1]] · [[정정 · 온도 법칙의 부호 역전 주장 철회]]"),
    "음성 · 정방향 진화는 유전자군 수준에서 '변화 없음'에 진다": (
        "무작위 조상을 법칙대로 진화시켜 현대 후손과 대조하면, 유전자군 하나하나 수준에서는 "
        "'아무것도 안 바뀐다'는 예측을 이기지 못합니다. 기능 수준으로 올리면 작동합니다.\n\n"
        "**읽기** — 이 법칙들의 값어치는 유전체 재현이 아니라 **순위**입니다.\n\n"
        "- [[forward_evolution_v1]]"),
}


def ancestor_notes(out):
    """One note per reconstructed node, carrying both tests and the measured size error."""
    made = []
    atlas_f = RESULTS / "atlas" / "atlas.json"
    if not atlas_f.exists():
        return made
    atlas = json.loads(atlas_f.read_text())
    for t in atlas.get("targets", []):
        name = f"조상 · {slug(t['name'])}"
        made.append((name, t))
        v, pw = t.get("validation") or {}, t.get("power") or {}
        tags = ["유형/조상", f"조상/{t['id']}", f"클러스터/조상 복원"]
        body = fm(유형="조상", 마디=t["id"], 표본=t["tips"], 신뢰도=t.get("confidence", "—"), tags=tags)
        body += f"# {t['name']}\n\n> [!abstract] {t.get('sub', '')}\n> {t.get('blurb', '')}\n\n"
        rows = [["잎 숨기기 (현생 종 맞히기)", num(v.get("reconstruction")), num(v.get("baseline")),
                 num(v.get("margin"))]]
        if pw:
            rows.append(["알려진 정답 (조상 맞히기)", num(pw.get("recon_auroc")),
                         num(pw.get("freq_auroc")), num(pw.get("auroc_margin"))])
        body += "## 두 가지 시험\n\n" + table(rows, ["시험", "복원", "기준선", "차이"]) + "\n\n"
        if pw:
            body += (f"로그손실 {num(pw.get('recon_logloss'))} vs {num(pw.get('freq_logloss'))} · "
                     f"판정 **{pw.get('verdict')}** · 이 마디의 크기 오차 "
                     f"**{pw.get('recon_size_bias', 0) * 100:.1f}%**\n\n")
        body += (f"## 크기\n{'**' + str(t['expected_families']) + '개 (추정)**' if t.get('quote_size') else '**보고하지 않음**'}"
                 f" · 오늘날 후손 중앙값 {t.get('today_median_families') or '—'}\n\n"
                 f"> [!warning]\n> {t.get('size_note', '')}\n\n")
        if t.get("extra_caveat"):
            body += f"> [!danger]\n> {t['extra_caveat']}\n\n"
        if t.get("hgt"):
            body += (f"## 수평 전달\n측정값 **{t['hgt']['estimated']}** — 크기가 부풀기 시작하는 0.35 "
                     f"{'아래' if t['hgt']['estimated'] < 0.35 else '위'}. [[수평 전달 추정량]]\n\n")
        if t.get("lost"):
            body += ("## 조상에 있었으나 지금은 드문 유전자군\n\n"
                     + table([[f"`{x['family']}`", x.get("desc", "")[:60], num(x["p"]),
                               f"{x['today'] * 100:.0f}%"] for x in t["lost"][:12]],
                             ["유전자군", "설명", "조상", "오늘날"]) + "\n\n")
        if t.get("positive_control"):
            ok = [k for k, p in t["positive_control"].items() if p is not None and p >= 0.9]
            have = [k for k, p in t["positive_control"].items() if p is not None]
            body += (f"## 양성 대조\n아는 답 {len(have)}개 중 **{len(ok)}개**를 사후확률 0.9 이상으로 "
                     f"되찾았습니다 (모형에 알려주지 않음).\n\n")
        body += "## 방법\n- [[2상태 마르코프 모형]]\n- [[완전도 관측 모형]]\n- [[표본 크기의 한계]]\n"
        body += "\n## 클러스터\n- [[클러스터 · 조상 복원]]\n- [[조상 목록]]\n"
        write(out / "05-조상" / f"{name}.md", body)
    for b in atlas.get("blocked", []):
        body = fm(유형="막힌 후보", tags=["유형/막힘", "클러스터/조상 복원"])
        body += (f"# 막힘 · {b['name']}\n\n{b['why']}\n\n> [!failure] 막힌 곳\n> {b['blocker']}\n\n"
                 "- [[조상 목록]]\n")
        write(out / "05-조상" / f"막힘 · {slug(b['name'])}.md", body)
    return made


GRAPH = {
    "collapse-filter": False, "search": "", "showTags": True, "showAttachments": False,
    "hideUnresolved": True, "showOrphans": True,
    "collapse-color-groups": False,
    "colorGroups": [
        {"query": "tag:#유형/법칙 OR path:01-법칙", "color": {"a": 1, "rgb": 2777814}},
        {"query": "tag:#유형/검증", "color": {"a": 1, "rgb": 15427124}},
        {"query": "tag:#유형/한계", "color": {"a": 1, "rgb": 14701102}},
        {"query": "tag:#유형/계수", "color": {"a": 1, "rgb": 1814138}},
        {"query": "tag:#유형/실험", "color": {"a": 1, "rgb": 9474192}},
        {"query": "tag:#유형/조상", "color": {"a": 1, "rgb": 5025616}},
        {"query": "tag:#판정/음성", "color": {"a": 1, "rgb": 14893620}},
        {"query": "path:03-방법", "color": {"a": 1, "rgb": 11119017}},
        {"query": "path:07-정정", "color": {"a": 1, "rgb": 16098851}},
    ],
    "collapse-display": False, "showArrow": True, "textFadeMultiplier": -0.8,
    "nodeSizeMultiplier": 1.2, "lineSizeMultiplier": 1,
    "collapse-forces": False, "centerStrength": 0.42, "repelStrength": 12,
    "linkStrength": 1, "linkDistance": 180, "scale": 0.7, "close": False,
}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default="obsidian/organelle-evo-lab")
    args = ap.parse_args()
    out = Path(args.out)
    if out.exists():
        shutil.rmtree(out)
    out.mkdir(parents=True)

    experiments, exp_names = experiment_notes(out)
    laws = []
    for f in sorted(list(LAWS.glob("*.json")) + list(LAWS.glob("animals/*.json"))):
        law = json.loads(f.read_text())
        if "id" not in law:
            continue
        envf = LAWS / "environments" / f"{law['id']}.json"
        env = json.loads(envf.read_text()) if envf.exists() else None
        laws.append(law_notes(out, law, env, experiments))

    for name, text in METHODS.items():
        write(out / "03-방법" / f"{name}.md",
              fm(유형="방법", tags=["유형/방법"]) + f"# {name}\n\n{text}\n")
    for name, text in DATASETS.items():
        write(out / "04-데이터셋" / f"{name}.md",
              fm(유형="데이터셋", tags=["유형/데이터셋"]) + f"# {name}\n\n{text}\n")
    for name, text in NEGATIVES.items():
        write(out / "06-음성 결과" / f"{name}.md",
              fm(유형="음성 결과", tags=["유형/음성", "판정/음성"]) + f"# {name}\n\n{text}\n")
    for name, text in CORRECTIONS.items():
        write(out / "07-정정" / f"{name}.md",
              fm(유형="정정", tags=["유형/정정"]) + f"# {name}\n\n{text}\n")
    ancestors = ancestor_notes(out)

    by_cluster = defaultdict(list)
    for lid, cl, label, margin in laws:
        by_cluster[cl].append((lid, label, margin))
    for cl, items in by_cluster.items():
        body = fm(유형="클러스터", tags=["유형/클러스터", f"클러스터/{cl}"])
        body += f"# 클러스터 · {cl}\n\n이 묶음의 법칙 {len(items)}개.\n\n"
        body += table([[f"[[{i}]]", lab, (f"{m:+.4f}" if m is not None else "—")]
                       for i, lab, m in sorted(items)], ["법칙", "판정", "기준선 대비"]) + "\n\n"
        body += "- [[법칙 목록]]\n"
        write(out / "00-색인" / f"클러스터 · {cl}.md", body)

    counts = defaultdict(int)
    for _, _, label, _ in laws:
        counts[label] += 1
    body = fm(유형="색인", tags=["유형/색인"])
    body += ("# 법칙 목록\n\n"
             + table([[c, counts[c]] for c in ("양성", "음성", "무승부", "미분류") if counts[c]],
                     ["판정", "개수"]) + "\n\n")
    for cl, items in sorted(by_cluster.items()):
        body += (f"## [[클러스터 · {cl}]]\n\n"
                 + table([[f"[[{i}]]", lab, (f"{m:+.4f}" if m is not None else "—"),
                           f"[[{i} · 검증]]", f"[[{i} · 한계]]"] for i, lab, m in sorted(items)],
                         ["법칙", "판정", "기준선 대비", "검증", "한계"]) + "\n\n")
    write(out / "00-색인" / "법칙 목록.md", body)

    write(out / "00-색인" / "실험 목록.md",
          fm(유형="색인", tags=["유형/색인"]) + "# 실험 목록\n\n"
          + "\n".join(f"- [[{n}]] — `results/{r}/`" for n, r in sorted(exp_names)) + "\n")
    write(out / "00-색인" / "조상 목록.md",
          fm(유형="색인", tags=["유형/색인"]) + "# 조상 목록\n\n"
          + table([[f"[[{n}]]", t["tips"], t.get("confidence", "—"),
                    (num((t.get("power") or {}).get("auroc_margin")) if t.get("power") else "—")]
                   for n, t in ancestors], ["마디", "표본 종 수", "신뢰도", "조상 채점 차이"])
          + "\n\n## 막힌 후보\n" + "\n".join(
              f"- [[막힘 · {slug(b['name'])}]]" for b in
              json.loads((RESULTS / 'atlas' / 'atlas.json').read_text()).get("blocked", []))
          + "\n")
    write(out / "00-색인" / "음성 결과 목록.md",
          fm(유형="색인", tags=["유형/색인"]) + "# 음성 결과 목록\n\n"
          "> [!important] 이 프로젝트의 중심\n> 법칙이 안 통한다는 측정 결과를 숨기거나 좋게 "
          "포장하면 이 프로젝트의 의미가 없습니다.\n\n"
          + "\n".join(f"- [[{n}]]" for n in NEGATIVES) + "\n")
    write(out / "00-색인" / "정정 목록.md",
          fm(유형="색인", tags=["유형/색인"]) + "# 정정 목록\n\n"
          "틀렸던 것과 왜 틀렸는지. 결론보다 **측정 도구**가 틀린 경우가 많았습니다.\n\n"
          + "\n".join(f"- [[{n}]]" for n in CORRECTIONS) + "\n")

    write(out / "홈.md", fm(유형="홈", tags=["유형/색인"]) + f"""# organelle-evo 실험 노트

실제 유전체를 비교해 **유전체 진화의 법칙을 학습하고 검증**합니다.

## 들어가는 문
- [[법칙 목록]] — 법칙 {len(laws)}개, 판정별
- [[실험 목록]] — 실행 기록 {len(exp_names)}개
- [[조상 목록]] — 복원한 마디 {len(ancestors)}개
- [[음성 결과 목록]] — 법칙이 통하지 않은 곳
- [[정정 목록]] — 틀렸던 것과 왜 틀렸는지

## 클러스터
{chr(10).join(f'- [[클러스터 · {c}]] ({len(v)})' for c, v in sorted(by_cluster.items()))}

## 방법
{chr(10).join(f'- [[{m}]]' for m in METHODS)}

## 데이터셋
{chr(10).join(f'- [[{d}]]' for d in DATASETS)}

## 읽는 규칙
> [!important]
> 1. 새 수치는 **항상 기준선과 나란히**. 기준선을 못 넘으면 음성으로 기록합니다.
> 2. 조상의 유전자군 **개수**는 표본이 분류군 뿌리에 닿을 때만 말합니다.
> 3. 수치가 이상하면 **측정 대상보다 측정 도구를 먼저** 봅니다. ([[정정 목록]])

- [[그래프 읽는 법]] · [[명명 규칙]]
""")
    write(out / "99-메타" / "그래프 읽는 법.md", fm(유형="메타", tags=["유형/메타"]) + """# 그래프 읽는 법

그래프 뷰의 색 묶음은 `.obsidian/graph.json`에 미리 넣어두었습니다.

| 색 | 무엇 |
| --- | --- |
| 파랑 | 법칙 허브 (`01-법칙/`) |
| 주황 | 검증 노트 |
| 빨강 | 한계 노트 |
| 남색 | 계수 노트 |
| 회색 | 실험 기록 |
| 초록 | 조상 마디 |
| 진홍 | 음성 판정 |
| 보라 | 방법 |
| 노랑 | 정정 |

**덩어리가 생기는 이유** — 법칙 하나는 허브 1 + 부품 5로 작은 성단을 이루고, 그 성단들이
클러스터 색인과 방법 노트를 거쳐 서로 이어집니다. 방법 노트(예: [[잎 숨기기 검증]])는 여러
성단에 걸쳐 있어 다리 역할을 합니다.

**유용한 검색**
- `tag:#판정/음성` — 기준선을 못 넘은 것만
- `tag:#유형/한계` — 모든 한계를 한 번에
- `path:07-정정` — 틀렸던 기록
""")
    write(out / "99-메타" / "명명 규칙.md", fm(유형="메타", tags=["유형/메타"]) + """# 명명 규칙

- 법칙 허브는 법칙 id 그대로: `environment_v3`
- 부품은 `법칙id · 종류`: `environment_v3 · 검증`
- 실험은 `실험 · 산출 폴더`: `실험 · hgt_rate`
- 조상은 `조상 · 이름`, 막힌 후보는 `막힘 · 이름`
- 버전은 지우지 않습니다. `_v2`가 생겨도 `_v1`은 남고, 무엇으로 왜 대체됐는지 그 법칙의
  한계 노트에 적습니다.
""")
    (out / ".obsidian").mkdir(exist_ok=True)
    (out / ".obsidian" / "graph.json").write_text(json.dumps(GRAPH, ensure_ascii=False, indent=2))
    (out / ".obsidian" / "app.json").write_text(json.dumps(
        {"attachmentFolderPath": "99-메타", "newLinkFormat": "shortest",
         "useMarkdownLinks": False, "showLineNumber": True}, indent=2))

    n = sum(1 for _ in out.rglob("*.md"))
    print(f"{n} notes -> {out}")
    print(f"  법칙 {len(laws)} (판정: {dict(counts)}), 실험 {len(exp_names)}, 조상 {len(ancestors)}, "
          f"방법 {len(METHODS)}, 음성 {len(NEGATIVES)}, 정정 {len(CORRECTIONS)}")


if __name__ == "__main__":
    main()
