"""Push-then-kill: do atavism-promoting drugs synergise with lipid synthesis inhibitors?
(pre-registration 27, docs/preregistration/2026-10-16_push_then_kill.md)

    python scripts/push_then_kill.py   -> results/drug/push_then_kill.json
"""

import gzip
import json
import re
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import cancer_atavism as ca  # noqa: E402
from combo_probe import LIPID_NAMES  # noqa: E402
from drug_fetch import partial  # noqa: E402

D = Path("data/combo")
OUT = Path("results/drug/push_then_kill.json")
LIPID = ["SCD", "SREBF", "MBTPS", "SCAP", "FASN", "ACACA", "ACC1", "ACC2", "HMGCR", "SQLE"]
LIPID_WORDS = ["STEAROYL", "FATTY ACID SYNTHASE", "SREBP", "ACETYL-COA CARBOXYLASE", "HMGCR INHIBITOR",
               "SQUALENE", "LIPOGEN", "DESATURASE"]
MIN_PAIRS = 5
SCORES = ["loewe", "zip", "bliss", "hsa"]


def norm(x):
    return re.sub(r"[^a-z0-9]", "", (x or "").lower())


def prism_lipid():
    """PRISM compound names whose MOA or target names a lipid synthesis enzyme."""
    out = set()
    p = Path("data/drug/compounds.tsv")
    if not p.exists():
        return out
    for line in p.read_text().splitlines()[1:]:
        x = line.split("\t")
        if len(x) < 4:
            continue
        txt = (x[2] + " " + x[3]).upper()
        if any(k in txt for k in LIPID) or any(w in txt for w in LIPID_WORDS):
            if x[1]:
                out.add(norm(x[1]))
    return out


def classes():
    s = json.loads(Path("results/drug/summary.json").read_text())
    push = {norm(x) for x in s["A_mimic"]["matched_names"]}
    rev = {norm(x) for x in s["A_reverse"]["matched_names"]}
    # PRISM annotation, plus known inhibitors of the same targets by name: the combination data carries no
    # mechanism column (deviation of 2026-10-17).
    lip = prism_lipid() | {norm(x) for x in LIPID_NAMES}
    overlap = {"push_and_lipid": sorted(push & lip), "reverse_and_lipid": sorted(rev & lip),
               "push_and_reverse": sorted(push & rev)}
    push, rev, lip = push - lip - rev, rev - lip - push, lip - push - rev
    return push, rev, lip, overlap


def combos():
    gz, plain = D / "combos.tsv.gz", D / "combos.tsv"
    if gz.exists():
        text = gzip.decompress(gz.read_bytes()).decode()
    elif plain.exists():
        text = plain.read_text()
    else:
        return []
    rows = []
    for line in text.splitlines()[1:]:
        x = line.split("\t")
        if len(x) < 7:
            continue
        vals = {}
        for k, v in zip(SCORES, x[3:7]):
            try:
                vals[k] = float(v)
            except ValueError:
                pass
        if vals:
            rows.append((norm(x[0]), norm(x[1]), x[2], vals))
    return rows


def aliases():
    """DrugCombDB name -> official name, so "compactin" also matches "mevastatin"."""
    out, p = {}, D / "drug_names.tsv"
    if p.exists():
        for line in p.read_text().splitlines()[1:]:
            x = line.split("\t")
            if len(x) == 2 and x[1] and norm(x[0]) != norm(x[1]):
                out[norm(x[0])] = norm(x[1])
    return out


def lines_scores():
    """Tilt and proliferation per cell line, reachable by DepMap id and by cell line name."""
    rows = [x.split("\t") for x in Path("data/drug/lines.tsv").read_text().splitlines()[1:]]
    out = {}
    for r in rows:
        out[norm(r[0])] = (r[1], float(r[2]), float(r[3]))
    p = D / "line_names.tsv"
    if p.exists():
        for line in p.read_text().splitlines()[1:]:
            x = line.split("\t")
            if len(x) >= 2 and norm(x[0]) in out:
                for name in x[1:]:
                    if name:
                        out.setdefault(norm(name), out[norm(x[0])])
    return out


def single_agent():
    """PRISM mean viability per compound (auxiliary 2)."""
    out, p = {}, Path("data/drug/compounds.tsv")
    if p.exists():
        for line in p.read_text().splitlines()[1:]:
            x = line.split("\t")
            if len(x) >= 6 and x[1]:
                try:
                    out[norm(x[1])] = float(x[5])
                except ValueError:
                    pass
    return out


def diff_ci(a, b):
    rng = np.random.default_rng(ca.SEED)
    est = a.mean() - b.mean()
    bs = [rng.choice(a, len(a)).mean() - rng.choice(b, len(b)).mean() for _ in range(ca.N_BOOT)]
    lo, hi = np.percentile(bs, [2.5, 97.5])
    return {"difference": round(float(est), 4), "lo": round(float(lo), 4), "hi": round(float(hi), 4),
            "n_group": int(len(a)), "n_rest": int(len(b)),
            "verdict": "양성" if lo > 0 else ("음성" if hi < 0 else "무승부")}


def main():
    push, rev, lip, overlap = classes()
    rows = combos()
    src = json.loads((D / "source.json").read_text()) if (D / "source.json").exists() else {}
    out = {"source": src, "class_sizes": {"push": len(push), "reverse": len(rev), "lipid": len(lip)},
           "class_overlap_removed": overlap, "combo_rows": len(rows)}
    if not rows:
        out["note"] = "no combination data"
        OUT.write_text(json.dumps(out, ensure_ascii=False, indent=1))
        print(json.dumps(out, ensure_ascii=False, indent=1))
        return
    score_key = next((k for k in SCORES if sum(k in r[3] for r in rows) > 0.5 * len(rows)), SCORES[0])
    out["score_used"] = score_key
    # per pair: mean synergy over cell lines, and which classes the pair spans
    by_pair = {}
    for d1, d2, line, vals in rows:
        if score_key not in vals:
            continue
        key = tuple(sorted((d1, d2)))
        by_pair.setdefault(key, []).append((line, vals[score_key]))
    alias = aliases()
    members = lambda d: {d, alias.get(d, d)}
    tag = lambda d: ("P" if members(d) & push else "") + ("R" if members(d) & rev else "") + \
                    ("L" if members(d) & lip else "")
    groups = {"P+L": [], "R+L": [], "rest": []}
    for (a, b), v in by_pair.items():
        ta, tb = tag(a), tag(b)
        m = float(np.mean([x[1] for x in v]))
        if ("P" in ta and "L" in tb) or ("P" in tb and "L" in ta):
            groups["P+L"].append(m)
        elif ("R" in ta and "L" in tb) or ("R" in tb and "L" in ta):
            groups["R+L"].append(m)
        else:
            groups["rest"].append(m)
    out["pairs"] = {k: len(v) for k, v in groups.items()}
    rest = np.array(groups["rest"])
    for k, name in (("P+L", "primary_push_plus_lipid"), ("R+L", "secondary_reverse_plus_lipid")):
        g = np.array(groups[k])
        out[name] = diff_ci(g, rest) if len(g) >= MIN_PAIRS and len(rest) >= MIN_PAIRS else {
            "n_group": len(g), "skipped": f"fewer than {MIN_PAIRS} pairs"}
    p1 = out["primary_push_plus_lipid"].get("verdict")
    p2 = out["secondary_reverse_plus_lipid"].get("verdict")
    out["overall"] = ("강한 지지" if p1 == "양성" and p2 == "양성" else
                      "밀고 때리기 지지" if p1 == "양성" else
                      "지지하지 않음" if p1 in ("무승부", "음성") else "판정 불가(짝 부족)")
    # auxiliary 1: within P+L pairs, does synergy track the tilt score?
    S = lines_scores()
    pl_rows = []
    for (a, b), v in by_pair.items():
        ta, tb = tag(a), tag(b)
        if ("P" in ta and "L" in tb) or ("P" in tb and "L" in ta):
            for line, s in v:
                if norm(line) in S:
                    pl_rows.append((S[norm(line)], s))
    if len(pl_rows) >= 100:
        g = np.array([r[0][0] for r in pl_rows])
        t = np.array([r[0][1] for r in pl_rows])
        p = np.array([r[0][2] for r in pl_rows])
        y = np.array([r[1] for r in pl_rows])
        r = partial(y, t, p, g)
        out["aux_synergy_vs_tilt"] = {"rho_lineage": round(r[0], 4), "rho_partial": round(r[1], 4), "n": r[2]} if r \
            else {"n": len(pl_rows), "skipped": "partial correlation needs more lines"}
    else:
        out["aux_synergy_vs_tilt"] = {"n": len(pl_rows), "skipped": "fewer than 100 matched rows"}
    # auxiliary 2: single-agent toxicity of each class (PRISM mean viability)
    via = single_agent()
    out["aux_single_agent_viability"] = {
        name: ({"n": len(v), "mean": round(float(np.mean(v)), 4)} if v else {"n": 0})
        for name, cls in (("push", push), ("reverse", rev), ("lipid", lip))
        for v in [[via[d] for d in cls if d in via]]}
    # auxiliary 3: HDAC inhibitors alone as the push class
    hdac = {d for d in push if any(k in d for k in ("vorinostat", "zolinza", "belinostat", "trichostatin",
                                                    "panobinostat", "entinostat", "mocetinostat", "saha"))}
    hd_pairs = [np.mean([x[1] for x in v]) for (a, b), v in by_pair.items()
                if ("L" in tag(a) and b in hdac) or ("L" in tag(b) and a in hdac)]
    out["aux_hdac_only_push"] = diff_ci(np.array(hd_pairs), rest) if len(hd_pairs) >= MIN_PAIRS else {
        "n_group": len(hd_pairs), "skipped": f"fewer than {MIN_PAIRS} pairs", "hdac_drugs": sorted(hdac)}
    # auxiliary 4: the primary metric under each synergy score
    out["aux_by_score"] = {}
    for k in SCORES:
        pairs_k, rest_k, bp = [], [], {}
        for d1, d2, line, vals in rows:
            if k in vals:
                bp.setdefault(tuple(sorted((d1, d2))), []).append(vals[k])
        for (a, b), v in bp.items():
            ta, tb = tag(a), tag(b)
            m = float(np.mean(v))
            (pairs_k if (("P" in ta and "L" in tb) or ("P" in tb and "L" in ta)) else rest_k).append(m)
        out["aux_by_score"][k] = diff_ci(np.array(pairs_k), np.array(rest_k)) \
            if len(pairs_k) >= MIN_PAIRS and len(rest_k) >= MIN_PAIRS else {"n_group": len(pairs_k),
                                                                           "skipped": "too few pairs"}
    seen = {d for pair in by_pair for d in pair}
    out["drugs_in_combination_data"] = len(seen)
    out["lipid_drugs_in_combination_data"] = sorted(d for d in seen if "L" in tag(d))
    out["push_drugs_in_combination_data"] = sorted(d for d in seen if "P" in tag(d))
    out["reverse_drugs_in_combination_data"] = sorted(d for d in seen if "R" in tag(d))
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(out, ensure_ascii=False, indent=1))
    print(json.dumps(out, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
