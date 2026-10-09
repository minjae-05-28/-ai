"""Pre-registration 5 (docs/preregistration/2026-10-09_prokaryote_and_loso.md).

    python scripts/prokaryote_and_loso.py   -> results/leca_models/prokaryote_and_loso.json

C. Does the prokaryotic distribution of a family (share of UniProt archaeal and bacterial proteomes
   carrying it) add to present-day eukaryotic frequency, against Vosseberg et al. 2021 gene-tree LECA?
D. Leave one supergroup out: hide every tip of a supergroup and predict which families it carries,
   from the tree (M7 posterior at the group's common ancestor) or by counting the other species.
"""

import gzip
import hashlib
import json
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
from leca_model_variants import OUT, PICK, ROOTS, TREE, labels, logistic, logit  # noqa: E402
from run_clade_ancestor import build, mrca  # noqa: E402
from tree_scramble_transfer import PLASTID, m7  # noqa: E402

from organelle_evo.predict import auroc  # noqa: E402

GROUPS = ["Alveolata", "Amoebozoa", "Discoba", "Fungi", "Metamonada", "Metazoa", "Rhodophyta", "Stramenopiles",
          "Viridiplantae"]


def prokaryote_shares(fams):
    seen = {"archaea": {}, "bacteria": {}}
    for f in sorted(Path("data/uniprot/shards").glob("*.json.gz")):
        for v in json.loads(gzip.open(f, "rt").read()).values():
            k = v.get("kingdom")
            if k in seen and v.get("pfam"):
                old = seen[k].get(v["organism"])
                if old is None or len(v["pfam"]) > len(old):
                    seen[k][v["organism"]] = set(v["pfam"])
    out = {}
    for k, orgs in seen.items():
        cnt = {}
        for s in orgs.values():
            for f in s:
                cnt[f] = cnt.get(f, 0) + 1
        out[k] = np.array([cnt.get(f, 0) / len(orgs) for f in fams])
        out[f"n_{k}"] = len(orgs)
    return out


def leca_m7h2(lineage):
    """M7 + H2 (pre-registration 4), minimum over the four roots, aligned to the first root's families."""
    fams_ref, freq, per = None, None, []
    for rname, split in ROOTS.items():
        d, fams, names, _, _, _ = build(TREE, set(), 100, "*", False, split, lineage)
        d["completeness"] = d["completeness_vec"]
        tips = d["tips"]
        node = mrca(tips, d["parent"], d["depth"])
        vis = np.zeros(len(d["parent"]), bool)
        vis[tips] = True
        if fams_ref is None:
            fams_ref, freq = fams, d["X"][tips].mean(0).astype(float)
        col = {f: j for j, f in enumerate(fams)}
        idx = np.array([col.get(f, -1) for f in fams_ref])
        p, _ = m7(d, vis)
        plastid = np.array([bool(PLASTID & set(lineage.get(names[v], []))) for v in tips])
        vis_h = vis.copy()
        vis_h[np.array(tips)[plastid]] = False
        p_h, _ = m7(d, vis_h)
        enriched = d["X"][np.array(tips)[plastid]].mean(0) > 2 * d["X"][np.array(tips)[~plastid]].mean(0)
        h2 = np.where(enriched, p_h[node], p[node])
        per.append(np.where(idx >= 0, h2[np.maximum(idx, 0)], 0.0))
        print(f"  M7H2 {rname} done", flush=True)
    return fams_ref, freq, np.min(np.stack(per), 0)


def boot_ci(vals):
    lo, hi = np.percentile(vals, [2.5, 97.5])
    return [round(float(lo), 4), round(float(hi), 4)]


def verdict(ci):
    return "양성" if ci[0] > 0 else ("음성" if ci[1] < 0 else "무승부")


def part_c(lineage):
    fams, freq, post = leca_m7h2(lineage)
    pro = prokaryote_shares(fams)
    leca, tested = labels()
    meta = json.loads(Path("data/eukaryotes/pfam_meta.json").read_text())
    acc = np.array([meta.get(f, {}).get("accession", "").split(".")[0] for f in fams])
    keep = np.isin(acc, list(tested))
    y = np.isin(acc[keep], list(leca)).astype(float)
    test = np.array([hashlib.md5(a.encode()).digest()[0] % 2 == 1 for a in acc[keep]])
    cal = ~test
    lf = np.log(freq[keep] + 1e-3)
    la, lb = np.log(pro["archaea"][keep] + 1e-3), np.log(pro["bacteria"][keep] + 1e-3)
    inputs = {"P0": [lf], "P1": [lf, la, lb], "P2": [lf, la, lb, logit(post[keep])]}
    scores, coefs, cal_auc = {}, {}, {}
    for k, cols in inputs.items():
        Xf = np.column_stack(cols)
        s = np.zeros(len(y))
        s[test], coefs[k] = logistic(Xf[cal], y[cal], Xf[test])
        ci = np.flatnonzero(cal)
        fold = np.random.default_rng(0).integers(0, 5, len(ci))
        for f in range(5):
            tr, te = ci[fold != f], ci[fold == f]
            s[te], _ = logistic(Xf[tr], y[tr], Xf[te])
        scores[k] = s
        cal_auc[k] = round(float(auroc(s[cal], y[cal])), 4)
    scores["frequency"] = freq[keep]
    scores["M7H2"] = post[keep]
    yt = y[test]
    T = {k: v[test] for k, v in scores.items()}
    rng = np.random.default_rng(0)
    pairs = {"P1_minus_frequency": ("P1", "frequency"), "P2_minus_P1": ("P2", "P1"), "P1_minus_P0": ("P1", "P0")}
    diffs = {k: [] for k in pairs}
    for _ in range(2000):
        ix = rng.integers(0, len(yt), len(yt))
        if yt[ix].min() == yt[ix].max():
            continue
        for k, (a, b) in pairs.items():
            diffs[k].append(auroc(T[a][ix], yt[ix]) - auroc(T[b][ix], yt[ix]))
    res = {"n_archaea": pro["n_archaea"], "n_bacteria": pro["n_bacteria"],
           "test_auroc": {k: round(float(auroc(v, yt)), 4) for k, v in T.items()},
           "calibration_auroc_cv": cal_auc, "coefficients_last_is_intercept": coefs}
    for k, (a, b) in pairs.items():
        ci = boot_ci(diffs[k])
        res[k] = {"mean": round(float(auroc(T[a], yt) - auroc(T[b], yt)), 4), "ci95": ci, "verdict": verdict(ci)}
    # descriptive: how LECA share depends on prokaryotic presence (test half)
    anyp = (pro["archaea"][keep] + pro["bacteria"][keep] > 0)[test]
    res["leca_share_by_prokaryote_presence"] = {"in_prokaryotes": round(float(yt[anyp].mean()), 3),
                                                "eukaryote_only": round(float(yt[~anyp].mean()), 3),
                                                "n_in_prokaryotes": int(anyp.sum()), "n_eukaryote_only": int((~anyp).sum())}
    return res


def part_d(lineage):
    sg = {r["organism"].replace("'", ""): r["supergroup"]
          for r in json.loads(Path(PICK).read_text())["lineage"].values()}
    d, fams, names, _, _, _ = build(TREE, set(), 100, "*", False, ROOTS["amorphea"], lineage)
    d["completeness"] = d["completeness_vec"]
    tips = np.array(d["tips"])
    grp = np.array([sg.get(names[v], "?") for v in tips])
    X = d["X"]
    per = {}
    for G in GROUPS:
        gt = tips[grp == G]
        vis = np.zeros(len(d["parent"]), bool)
        vis[tips[grp != G]] = True
        node = mrca(list(gt), d["parent"], d["depth"])
        under, stack = [], [node]
        while stack:
            v = stack.pop()
            if not d["children"][v]:
                under.append(v)
            stack.extend(d["children"][v])
        intruders = [v for v in under if v not in set(gt.tolist())]
        p, ch = m7(d, vis)
        others = tips[grp != G]
        freq = X[others].mean(0).astype(float)
        fam_ok = X[others].any(0)
        y_any = X[gt].any(0)[fam_ok].astype(float)
        y_half = (X[gt].mean(0) >= 0.5)[fam_ok].astype(float)
        per[G] = {"model": p[node][fam_ok].astype(float), "count": freq[fam_ok], "y_any": y_any, "y_half": y_half,
                  "n_tips": int(len(gt)), "non_group_tips_under_ancestor": len(intruders),
                  "mixed": len(intruders) > 0.1 * len(gt), "shared_ratio": str(ch.get("ratio"))}
        print(f"  {G}: {len(gt)} tips, {len(intruders)} other tips under its ancestor", flush=True)
    rng = np.random.default_rng(0)
    out = {"groups": {}}
    for target in ("y_any", "y_half"):
        rows = {}
        for G, r in per.items():
            rows[G] = (auroc(r["model"], r[target]), auroc(r["count"], r[target]))
        mean_diff = float(np.mean([a - b for a, b in rows.values()]))
        boots = []
        for _ in range(1000):
            ds = []
            for G, r in per.items():
                n = len(r[target])
                ix = rng.integers(0, n, n)
                if r[target][ix].min() == r[target][ix].max():
                    continue
                ds.append(auroc(r["model"][ix], r[target][ix]) - auroc(r["count"][ix], r[target][ix]))
            boots.append(np.mean(ds))
        ci = boot_ci(boots)
        out[target] = {"mean_model_minus_count": round(mean_diff, 4), "ci95": ci, "verdict": verdict(ci)}
        for G, (a, b) in rows.items():
            out["groups"].setdefault(G, {"n_tips": per[G]["n_tips"], "mixed": per[G]["mixed"],
                                         "non_group_tips_under_ancestor": per[G]["non_group_tips_under_ancestor"],
                                         "n_families": int(len(per[G]["y_any"]))})
            out["groups"][G][target] = {"model": round(float(a), 4), "count": round(float(b), 4),
                                        "diff": round(float(a - b), 4)}
    return out


def main():
    lineage = {r["organism"].replace("'", ""): r["lineage"]
               for r in json.loads(Path(PICK).read_text())["lineage"].values()}
    print("C: prokaryote distribution", flush=True)
    c = part_c(lineage)
    print(json.dumps(c, ensure_ascii=False, indent=1), flush=True)
    print("D: leave one supergroup out", flush=True)
    dd = part_d(lineage)
    print(json.dumps(dd, ensure_ascii=False, indent=1))
    res = {"preregistration": "docs/preregistration/2026-10-09_prokaryote_and_loso.md", "C": c, "D": dd}
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "prokaryote_and_loso.json").write_text(json.dumps(res, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
