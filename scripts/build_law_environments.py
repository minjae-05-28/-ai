"""Environment card for every law: under which conditions its data were collected, and
which environment produced which result.

    python scripts/build_law_environments.py

Writes laws/environments/<law_id>.json and laws/environments/README.md. Law files are not
touched (a law is never rewritten); the card sits next to it.

Each card has
  envelope      the environment values of the species the law was fitted on (range, median,
                counts) from the catalogues, plus measured genome GC (results/gc/gc.json).
                Outside the envelope the law is an extrapolation.
  contrasts     for pair laws: how many pairs change each axis, and by how much.
  findings      results the law reports per environment / lifestyle / system, keeping only
                effects whose 95% interval excludes 0 (or the law's own pass/fail verdicts).
  species_from  "law" when the law lists its species, "catalogue" when they were rebuilt
                from the catalogue and the data present now (the law only stored counts).
"""

import json
from pathlib import Path
from statistics import median

from organelle_evo.animals import catalog as animal_cat
from organelle_evo.eukaryotes import catalog as euk_cat
from organelle_evo.laws import ANIMAL_LAWS_DIR, LAWS_DIR
from organelle_evo.prokaryotes import catalog as pro_cat
from organelle_evo.realdata.catalog import CATALOG as REAL

OUT = LAWS_DIR / "environments"
GC = json.loads(Path("results/gc/gc.json").read_text())
PRO_AXES = ("colder", "saltier", "anaerobic", "radiation_resistant", "oligotrophic")
EUK_AXES = ("parasite", "intracellular", "reduced_mitochondria")

PRO_LABEL = {"temp": "최적 온도 °C", "nacl": "최적 NaCl %", "aerobic": "산소 호흡(1)", "radiation": "방사선 내성(1)",
             "oligo": "빈영양(1)"}
ANIMAL_LABEL = {"tcell": "세포 온도 °C", "osmol": "세포 내 삼투압 mOsm", "hypoxia": "저산소(1)", "endo": "항온(1)",
                "parasite": "기생(1)", "urea": "요소 삼투(1)"}


def present(folder):
    out = set()
    for f in Path(folder).glob("*.json"):
        try:
            d = json.loads(f.read_text())
        except Exception:
            continue
        if isinstance(d, dict) and d.get("species"):
            out.add(d["species"])
    return out


def numeric(values):
    v = [x for x in values if x is not None]
    if not v:
        return None
    return {"min": min(v), "median": round(median(v), 3), "max": max(v), "n": len(v)}


def counts(values):
    out = {}
    for v in values:
        out[str(v)] = out.get(str(v), 0) + 1
    return dict(sorted(out.items(), key=lambda t: -t[1]))


def gc_range(catalog, species):
    table = GC.get(catalog, {})
    return numeric([table[s]["gc"] for s in species if s in table and table[s].get("gc") is not None])


def split_pairs(items):
    pairs = []
    for p in items:
        if isinstance(p, str) and "->" in p:
            a, d = (s.strip() for s in p.split("->", 1))
            pairs.append((a, d))
    return pairs


# ---- envelopes per catalogue ----------------------------------------------------------------

def prokaryote_envelope(species, pairs=()):
    env = [pro_cat.SPECIES[s] for s in species if s in pro_cat.SPECIES]
    card = {"catalogue": "prokaryotes", "n_species": len(env),
            "envelope": {PRO_LABEL[k]: (numeric([getattr(e, k) for e in env]) if k in ("temp", "nacl")
                                        else counts([getattr(e, k) for e in env])) for k in PRO_LABEL},
            "groups": counts([e.group for e in env]),
            "gc": gc_range("prokaryotes", species)}
    if pairs:
        rows = [pro_cat.design(a, d) for a, d in pairs if a in pro_cat.SPECIES and d in pro_cat.SPECIES]
        card["contrasts"] = {
            ax: {"pairs_changed": sum(abs(r[i + 1]) >= 0.25 for r in rows),
                 "change_range": [round(min(r[i + 1] for r in rows), 2), round(max(r[i + 1] for r in rows), 2)]}
            for i, ax in enumerate(PRO_AXES)}
        for ax in PRO_AXES:
            if card["contrasts"][ax]["pairs_changed"] < 5:
                card["contrasts"][ax]["warning"] = "표본 적음 (5쌍 미만)"
        card["contrasts"]["scale"] = (f"colder: (relative - descendant temperature)/{pro_cat.TEMP_SCALE} C; "
                                      f"saltier: change in NaCl/{pro_cat.NACL_SCALE}%; others -1/0/1")
        card["contrasts"]["control_pairs"] = sum(max(abs(v) for v in r[1:]) < 0.25 for r in rows)
    return card


def eukaryote_envelope(species, pairs=()):
    sp = [s for s in species if s in euk_cat.SPECIES]
    e = [euk_cat.SPECIES[s] for s in sp]
    card = {"catalogue": "eukaryotes", "n_species": len(sp),
            "envelope": {"생활 방식": counts([x.lifestyle for x in e]), "위치": counts([x.location for x in e]),
                         "에너지(미토콘드리아)": counts([x.energy for x in e]),
                         "세포 온도 °C (동물 카탈로그에 있는 종만)":
                             numeric([animal_cat.SPECIES[s].tcell for s in sp if s in animal_cat.SPECIES])},
            "groups": counts([x.group.split("_")[0] for x in e]),
            "gc": gc_range("eukaryotes", sp)}
    if pairs:
        rows = [euk_cat.design(d) for _, d in pairs if d in euk_cat.SPECIES]
        card["contrasts"] = {ax: {"pairs_with_axis": sum(r[i + 1] > 0 for r in rows)} for i, ax in enumerate(EUK_AXES)}
        card["contrasts"]["control_pairs"] = sum(not any(r[1:]) for r in rows)
        card["contrasts"]["independent_parasite_clades"] = len({euk_cat.SPECIES[d].group.split("_")[0]
                                                                for _, d in pairs if d in euk_cat.SPECIES
                                                                and euk_cat.design(d)[1]})
    return card


def animal_envelope(species):
    e = [animal_cat.SPECIES[s] for s in species if s in animal_cat.SPECIES]
    return {"catalogue": "animals", "n_species": len(e),
            "envelope": {ANIMAL_LABEL[k]: (numeric([getattr(x, k) for x in e]) if k in ("tcell", "osmol")
                                           else counts([getattr(x, k) for x in e])) for k in ANIMAL_LABEL},
            "groups": counts([x.group for x in e]),
            "gc": gc_range("animals", species)}


def endosymbiont_envelope(systems=("mitochondrion", "plastid", "insect_endosymbiont"), law_data=None):
    card = {"catalogue": "realdata", "envelope": {}}
    for s in systems:
        measured = list(GC.get(f"endosymbiosis/{s}", {}))
        card["envelope"][s] = {"lineages_in_catalogue": len(measured),
                               "gc": gc_range(f"endosymbiosis/{s}", measured)}
        own = (law_data or {}).get(s)
        if isinstance(own, dict):
            n = own.get("n_genomes") or own.get("lineages")
            if n:
                card["envelope"][s]["lineages_in_law"] = n
        elif isinstance(own, (int, float)):
            card["envelope"][s]["value_in_law"] = own
    card["envelope"]["환경"] = "의무적 세포 내 공생(숙주 세포질). 자유생활 생물과 유전자 획득에는 적용 범위 밖."
    return card


def genome_traits_envelope():
    import sys

    sys.path.insert(0, str(Path(__file__).resolve().parent))
    from run_genome_laws import load

    rows = load()
    temps = [r["temperature"] for r in rows if r["temperature"] is not None]
    return {"catalogue": "GTDB + Madin 2020", "n_species": len(rows),
            "envelope": {"서식 온도 °C": numeric(temps),
                         "산소": counts(["호기" if r["oxygen"] == 1 else "혐기" for r in rows if r["oxygen"] is not None]),
                         "숙주": counts(["숙주 관련" if r["host"] == 1 else "환경" for r in rows if r["host"] is not None]),
                         "GC": numeric([round(r["x"][0], 3) for r in rows]),
                         "유전체 크기 Mb": numeric([round(10 ** r["x"][1] / 1e6, 2) for r in rows])},
            "groups": dict(list(counts([r["phylum"] for r in rows]).items())[:12])}


# ---- findings --------------------------------------------------------------------------------

def significant(ctx, top=6):
    """Features whose 95% interval excludes 0, strongest first."""
    out = []
    for f, v in ctx.items():
        if isinstance(v, dict) and "ci95" in v and v["ci95"][0] != v["ci95"][1]:
            lo, hi = v["ci95"]
            if lo > 0 or hi < 0:
                out.append((f, v["weight"]))
    out.sort(key=lambda t: -abs(t[1]))
    return [{"feature": f, "weight": w, "direction": "더 잘 사라짐" if w > 0 else "덜 사라짐"} for f, w in out[:top]]


def axis_findings(law, axes, kinds=("loss", "duplication")):
    ctx = law.get("contexts") or {}
    out = {}
    for kind in kinds:
        for ax in axes:
            key = f"{kind}_{ax}"
            if key in ctx:
                sig = significant(ctx[key])
                out[key] = sig if sig else "신뢰구간이 0을 벗어나는 효과 없음 (또는 구간 미계산)"
    return out


def coefficient_findings(table):
    out = {}
    for k, v in table.items():
        if isinstance(v, dict) and "ci95" in v:
            lo, hi = v["ci95"]
            out[k] = {"weight": v["weight"], "ci95": v["ci95"],
                      "verdict": "효과 있음" if (lo > 0 or hi < 0) else "0과 구분 안 됨"}
    return out


def findings_for(law):
    lid, val = law["id"], law.get("validation") or {}
    if lid.startswith("environment_v"):
        f = axis_findings(law, PRO_AXES)
        f["summary"] = {"leave_one_pair_out_auroc": val.get("leave_one_pair_out_auroc"),
                        "환경 축 효과": val.get("env_vs_none"),
                        "주의": "축별 계수가 0과 구분돼도 환경 축은 처음 보는 쌍의 소실 예측을 개선하지 못함. "
                                "계수는 '이 데이터에서 이 환경일 때 이런 경향'이지 예측 규칙이 아님"}
        return f
    if lid in ("eukaryote_axes_v1", "eukaryote_axes_v3"):
        return axis_findings(law, EUK_AXES)
    if lid == "eukaryote_lifestyle_v1":
        return axis_findings(law, ("free_living", "parasite"))
    if lid == "composite_v1":
        return {"mean_auroc_recover_lost": val.get("mean_auroc_recover_lost")}
    if lid == "endosymbiosis_v1":
        return {s: significant(law["contexts"][s]) for s in ("mitochondrion", "plastid", "insect_endosymbiont")}
    if lid in ("severity_v1", "severity_environment_v1", "severity_endosymbiosis_v1"):
        f = {"loss_share_coefficients": coefficient_findings(law["contexts"]["loss"])}
        if "typical_share_lost" in law["contexts"]:
            f["typical_share_lost"] = law["contexts"]["typical_share_lost"]
        if "typical_share_lost" in val:
            f["typical_share_lost"] = val["typical_share_lost"]
        return f
    if lid == "sequence_v1":
        ep = val.get("environment_pairs", {}).get("by_statistic", {})
        return {"temperature": {k: val["temperature"].get(k) for k in ("pearson_ivywrel", "spearman_ivywrel",
                                                                         "rmse_ivywrel_loo_group", "rmse_mean_only")},
                "salt": {k: val["salt"].get(k) for k in ("spearman_acidic_excess", "spearman_median_pi")},
                "pairs_coef_per_axis": {stat: {"coef": v.get("coef"), "loo_r2": v.get("loo_r2_environment")}
                                        for stat, v in ep.items()},
                "note": "계수에 신뢰구간이 저장돼 있지 않음. GC로 설명되는 항목은 gc_confound_v1 / gc3_confound_v1 참조"}
    if lid in ("gc_confound_v1", "gc3_confound_v1", "phylo_check_v1"):
        out = {}
        for level, block in val.items():
            if not isinstance(block, dict):
                continue
            items = block.items() if level in ("species", "pairs", "symbionts") else [(level, block)]
            for k, v in items:
                if isinstance(v, dict) and "survives" in v:
                    out[k if level not in ("species", "pairs", "symbionts") else f"{level}:{k}"] = {
                        "survives": v.get("survives"), "survives_tree": v.get("survives_tree"),
                        "retained_share_of_effect": v.get("retained_share_of_effect")}
        return out
    if lid == "family_sequence_v1":
        return {ax: {k: v.get(k) for k in ("axis", "share_positive", "median_sensitivity", "families_tested")}
                for ax, v in val.items() if isinstance(v, dict) and "share_positive" in v}
    if lid in ("loss_order_v2",):
        return {s: {"fixed_null_p": r["fixed_null_p"], "row_null_z": round(r["row_null_z"], 1),
                    "판정": "유전자별 성향 이상의 순서 없음" if r["fixed_null_p"] > 0.05 else "성향 이상의 순서"}
                for s, r in val["results"].items()}
    if lid == "loss_order_environment_v1":
        return {"fixed_null_p": val.get("fixed_null_p"), "containment": val.get("containment"),
                "row_null_mean": val.get("row_null_mean")}
    if lid in ("organelle_modules_v1", "coloss_environment_endosymbiosis_v1"):
        key = "hidden_half_auroc" if "hidden_half_auroc" in val else None
        return val[key] if key else val
    if lid == "context_features_v1":
        return {sys: {"mean_auroc": v["mean_auroc"], "context_weights": v["context_weights"]} for sys, v in val.items()}
    if lid == "human_cell_v1":
        return {"body_sites": {site: {"errors": v["errors"], "n_commensals": v["n_commensals"]}
                               for site, v in val["composition"].items()}}
    if lid == "lab_evolution_v1":
        return {k: {kk: v.get(kk) for kk in ("auroc_comparative_loss_rate", "auroc_rarity_baseline",
                                              "auroc_minus_no_selection_control")}
                for k, v in val.items() if isinstance(v, dict) and "auroc_comparative_loss_rate" in v}
    if lid == "animal_axes_v1":
        out = {}
        for trait, v in val["traits"].items():
            out[trait] = {"p<0.05 (종 수준)": [a for a, p in v["p"].items() if p < 0.05],
                          "분류군 수준 통과": v["survives_clade_level"], "GC 보정 통과": v["survives_gc"],
                          "분류군 빼고 평균 기준선을 이김": v["leave_one_clade_out"]["beats_baseline"]}
        return out
    if lid == "animal_temperature_v1":
        return {"law_per_degree_c": val.get("law_per_degree_c"), "판정": "미생물 온도 법칙은 동물 세포에 전이되지 않음"}
    if lid == "convergent_expansion_v1":
        return {"convergent": [{"family": c["family"], "n_clades": c["n_clades"]} for c in law["contexts"]["convergent"]]}
    if lid == "loss_order_v1":
        return {k: val.get(k) for k in ("containment_over_random_median", "share_above_random")}
    if lid == "coloss_modules_v1":
        return {"gain_vs_additive": val.get("gain_vs_additive")}
    if lid.startswith("loss_prediction"):
        out = {}
        for tag, sm in val.items():
            out[tag] = {k: sm[k]["mean"] for k in ("law.auroc", "memorisation.auroc", "propensity20k.auroc",
                                                   "relatives.auroc", "relatives_other_genera.auroc",
                                                   "no_change.fate", "relatives_other_genera.fate") if k in sm}
        return out
    if lid.startswith("proteome_traits"):
        out = {}
        for t in ("temperature", "oxygen", "host"):
            lo = val.get(t, {}).get("leave_order_out", {})
            if "scores" in lo:
                out[t] = {"처음 보는 목": lo["scores"], "metric": lo["metric"]}
        return out
    if lid.startswith("genome_traits"):
        out = {}
        for t in ("temperature", "oxygen", "host"):
            lo = val[t]["leave_order_out"]
            out[t] = {"처음 보는 목": lo["scores"], "metric": lo["metric"],
                      "법칙 - 분류 암기": lo.get("law_linear - taxonomy"),
                      "계수(표준화, 전체/문 안)": val[t]["coefficients"]}
        return out
    if lid == "knockout_v1":
        return {"note": "실험실 배지(풍부·최소)의 필수성. 숙주 안 조건 아님"}
    return {}


# ---- species per law ---------------------------------------------------------------------------

def card_for(law):
    lid, data = law["id"], law.get("data") or {}
    listed = split_pairs(data.get("pairs", [])) if isinstance(data.get("pairs"), list) else []
    pro_present, euk_present = present("data/prokaryotes"), present("data/eukaryotes")
    pro_pairs_now = pro_cat.resolve_pairs(pro_present)
    euk_pairs_now = euk_cat.resolve_pairs(euk_present)
    sp = lambda pairs: sorted({s for p in pairs for s in p})  # noqa: E731

    if lid.startswith(("environment_v", "severity_environment")):
        card = prokaryote_envelope(sp(listed), listed)
        card["species_from"] = "law"
    elif lid in ("loss_order_environment_v1", "family_sequence_v1"):
        card = prokaryote_envelope(sp(pro_pairs_now), pro_pairs_now)
        card["species_from"] = "catalogue"
    elif listed and lid.startswith(("eukaryote_", "severity_v1", "loss_order_v1", "coloss_modules", "convergent")):
        card = eukaryote_envelope(sp(listed), listed)
        card["species_from"] = "law"
    elif lid == "composite_v1":
        pairs = split_pairs(json.loads((LAWS_DIR / "eukaryote_lifestyle_v1.json").read_text())["data"]["pairs"])
        card = eukaryote_envelope(sp(pairs), pairs)
        card["species_from"] = "eukaryote_lifestyle_v1 (same 14 pairs)"
    elif lid == "context_features_v1":
        card = {"parasites": eukaryote_envelope(sp(euk_pairs_now), euk_pairs_now),
                "extremophiles": prokaryote_envelope(sp(pro_pairs_now), pro_pairs_now), "species_from": "catalogue"}
    elif lid in ("sequence_v1", "gc_confound_v1", "gc3_confound_v1", "phylo_check_v1"):
        card = {"prokaryotes": prokaryote_envelope(sorted(present("data/composition/prokaryotes")), pro_pairs_now),
                "eukaryotes": eukaryote_envelope(sorted(present("data/composition/eukaryotes"))),
                "insect_endosymbionts": endosymbiont_envelope(("insect_endosymbiont",)),
                "species_from": "catalogue"}
    elif lid in ("endosymbiosis_v1", "severity_endosymbiosis_v1", "organelle_modules_v1"):
        card = endosymbiont_envelope(law_data=data)
        card["species_from"] = "catalogue"
    elif lid == "loss_order_v2":
        card = {"endosymbiosis": endosymbiont_envelope(), "parasites": eukaryote_envelope(sp(euk_pairs_now), euk_pairs_now),
                "species_from": "catalogue"}
    elif lid == "coloss_environment_endosymbiosis_v1":
        card = {"extremophiles": prokaryote_envelope(sp(pro_pairs_now), pro_pairs_now),
                "endosymbiosis": endosymbiont_envelope(), "species_from": "catalogue"}
    elif lid == "animal_axes_v1":
        card = animal_envelope(sorted(present("data/composition/animals")))
        card["species_from"] = "catalogue"
    elif lid == "animal_temperature_v1":
        names = [r["species"] for r in law["validation"]["species"]]
        card = animal_envelope([n for n in names if n in animal_cat.SPECIES])
        card["envelope"]["세포 온도 °C (법칙에 기록된 값)"] = numeric([r["temperature_c"] for r in law["validation"]["species"]])
        card["species_from"] = "law"
    elif lid == "human_cell_v1":
        card = {"catalogue": "human body sites", "envelope": {
            "부위": list(law["validation"]["composition"]),
            "공생균": data.get("commensals")}, "species_from": "law"}
    elif lid == "lab_evolution_v1":
        card = {"catalogue": "laboratory", "envelope": {
            "LTEE": "대장균 REL606, Davis 최소배지 + 포도당(DM25), 37°C, 매일 1:100 희석, 12개 집단, 5만 세대",
            "MA": "돌연변이 축적: 단일 콜로니 병목, 선택압 거의 없음"}, "species_from": "law"}
    elif lid == "knockout_v1":
        card = {"catalogue": "laboratory", "envelope": {
            "조건": "실험실 배지(풍부 배지, 최소 배지)에서의 결실 생존·적합도. DEG + Fitness Browser + 분열효모 결실 목록"},
            "species_from": "law"}
    elif lid.startswith("loss_prediction"):
        card = prokaryote_envelope(sp(pro_pairs_now), pro_pairs_now)
        card["species_from"] = "catalogue (extremophile pairs) + UniProt reference proteomes as relatives"
    elif lid.startswith("proteome_traits"):
        card = genome_traits_envelope()
        card["catalogue"] = "UniProt reference proteomes + Madin 2020 (envelope shown for the GTDB-matched set)"
        card["species_from"] = "UniProt x trait table"
    elif lid.startswith("genome_traits"):
        card = genome_traits_envelope()
        card["species_from"] = "GTDB x trait table (rebuilt with scripts/run_genome_laws.py load())"
    else:
        card = {"species_from": "unknown"}
    card = {"law_id": lid, **card, "findings": findings_for(law),
            "note": "envelope 밖의 환경에 이 법칙을 쓰면 외삽이다. 값은 문헌 근사치(카탈로그 주석 참조)."}
    return card


def short_env(card):
    """One line: the numeric ranges and the biggest categorical counts of a card."""
    parts = []
    blocks = [card] if "envelope" in card else [v for v in card.values() if isinstance(v, dict) and "envelope" in v]
    for b in blocks:
        for k, v in (b.get("envelope") or {}).items():
            if isinstance(v, dict) and "min" in v:
                parts.append(f"{k} {v['min']}–{v['max']}")
            elif isinstance(v, dict) and v and all(isinstance(x, int) for x in v.values()) and len(v) <= 4:
                parts.append(f"{k} " + "/".join(f"{a}:{n}" for a, n in v.items()))
            elif isinstance(v, dict) and "lineages_in_catalogue" in v:
                own = f" (법칙 학습 {v['lineages_in_law']})" if "lineages_in_law" in v else ""
                parts.append(f"{k} {v['lineages_in_catalogue']}계통{own}")
            elif isinstance(v, str) and k == "환경":
                parts.append(v.split(".")[0])
            elif isinstance(v, str):
                parts.append(f"{k}: {v}")
            elif isinstance(v, list) and v and isinstance(v[0], str) and k == "부위":
                parts.append("부위: " + ", ".join(x.split(" (")[0] for x in v))
        if b.get("gc"):
            parts.append(f"GC {b['gc']['min']}–{b['gc']['max']}")
    return "; ".join(parts[:6]) or "-"


def short_findings(card):
    f = card.get("findings") or {}
    out = []
    for k, v in f.items():
        if isinstance(v, list) and v and isinstance(v[0], dict) and "feature" in v[0]:
            out.append(f"{k}: " + ", ".join(f"{x['feature']} {x['weight']:+.2f}" for x in v[:2]))
        elif isinstance(v, dict) and v and all(isinstance(x, dict) and "verdict" in x for x in v.values()):
            out.append(", ".join(f"{a} {x['verdict']}" for a, x in v.items() if a != "base"))
        elif isinstance(v, dict) and "survives" in v:
            out.append(f"{k} {'유지' if v['survives'] and v.get('survives_tree') else '탈락'}")
        elif k == "summary" and isinstance(v, dict):
            out.append(f"환경 축 효과 {v.get('환경 축 효과'):+.4f}")
        elif isinstance(v, dict) and "판정" in v:
            out.append(f"{k}: {v['판정']}")
        elif isinstance(v, dict) and "k0" in v and "k2" in v:
            out.append(f"{k} 묶음 없이 {v['k0']:.3f} → 묶음 {v['k2']:.3f}")
        elif isinstance(v, (int, float)) and not isinstance(v, bool):
            out.append(f"{k} {v:+.4f}")
        elif isinstance(v, dict) and "mean_auroc" in v:
            m = v["mean_auroc"]
            out.append(f"{k}: 법칙 {m['law_context']:.3f} / 기본 {m['law_base']:.3f} / 암기 {m['memorisation']:.3f}")
        elif isinstance(v, dict) and "share_positive" in v:
            out.append(f"{k}: 적응 방향 유전자군 {v['share_positive']:.0%} (축 {v['axis']})")
        elif k == "convergent" and isinstance(v, list):
            out.append("수렴 확장: " + ", ".join(f"{x['family']}({x['n_clades']}계통)" for x in v[:4]))
        elif isinstance(v, dict) and v and all(isinstance(x, (int, float)) for x in v.values()):
            out.append(f"{k}: " + ", ".join(f"{a} {x:.3f}" for a, x in list(v.items())[:4]))
        elif isinstance(v, dict) and "p<0.05 (종 수준)" in v:
            out.append(f"{k}: 분류군 {v['분류군 수준 통과'] or '없음'}, GC {v['GC 보정 통과'] or '없음'}")
        elif isinstance(v, dict) and "errors" in v:
            out.append(f"{k.split(' (')[0]} 오차 " + ", ".join(f"{a} {x:+.3f}" for a, x in v["errors"].items()))
        elif isinstance(v, dict) and "auroc_comparative_loss_rate" in v:
            out.append(f"{k.split(' (')[0]}: 법칙 {v['auroc_comparative_loss_rate']:.3f} / 희귀도 {v['auroc_rarity_baseline']:.3f}")
        elif k == "body_sites" and isinstance(v, dict):
            out += [f"{a.split(' (')[0]} 조성 오차 " + ", ".join(f"{m} {x:+.3f}" for m, x in b["errors"].items())
                    for a, b in v.items()]
        elif isinstance(v, dict) and "처음 보는 목" in v:
            sc = v["처음 보는 목"]
            best = "law_linear" if "law_linear" in sc else "composition+pfam"
            out.append(f"{k}: 법칙 {sc[best]:.3f} / 암기 {sc['taxonomy']:.3f} / 평균 {sc['mean']:.3f} ({v['metric']})")
        elif isinstance(v, dict) and "relatives.auroc" in v:
            out.append(f"{k}: 법칙 {v['law.auroc']:.3f} / 2만 종 성향 {v['propensity20k.auroc']:.3f} / "
                       f"친척 {v['relatives.auroc']:.3f} (다른 속만 {v['relatives_other_genera.auroc']:.3f}) / "
                       f"암기 {v['memorisation.auroc']:.3f} AUROC")
        elif k == "note" and isinstance(v, str):
            out.append(v)
    return "<br>".join(out[:7]) or "-"


def readme(cards):
    lines = ["# 법칙별 환경 카드", "",
             "각 법칙이 **어떤 환경의 데이터에서** 나왔는지(적용 범위)와 **환경마다 어떤 결과**가 나왔는지입니다.",
             "`scripts/build_law_environments.py`가 법칙 파일과 카탈로그, 측정 GC에서 자동으로 만듭니다. "
             "법칙 파일은 건드리지 않습니다.", "",
             "- 범위 밖 환경에 법칙을 쓰면 **외삽**입니다.",
             "- 환경별 결과에는 95% 신뢰구간이 0을 벗어난 효과(또는 법칙 자체의 통과/탈락 판정)만 넣었습니다.",
             "- 환경 축 계수는 유의해도 예측을 개선하지 못한 경우가 많습니다(`environment_v3`: 0.813 vs 0.814). "
             "계수는 '이 데이터에서의 경향'입니다.",
             "- 종 목록이 법칙에 없으면 카탈로그와 지금 있는 데이터에서 복원했습니다(`species_from: catalogue`).", "",
             "| 법칙 | 데이터 환경 범위 | 환경별 결과 (요약) |", "|---|---|---|"]
    for c in cards:
        lines.append(f"| `{c['law_id']}` | {short_env(c)} | {short_findings(c)} |")
    return "\n".join(lines) + "\n"


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    rows = []
    for path in sorted(LAWS_DIR.glob("*.json")) + sorted(ANIMAL_LAWS_DIR.glob("*.json")):
        law = json.loads(path.read_text())
        card = card_for(law)
        (OUT / f"{law['id']}.json").write_text(json.dumps(card, ensure_ascii=False, indent=1, default=str))
        rows.append(card)
        print(f"  {law['id']:40s} {card.get('catalogue', '+'.join(k for k in card if isinstance(card[k], dict) and 'envelope' in card[k]))}")
    (OUT / "README.md").write_text(readme(rows))
    print(f"{len(rows)} cards -> {OUT}/")


if __name__ == "__main__":
    main()
