"""Reliability grades for ancestral calls, calibrated against gene trees (pre-registration 11:
docs/preregistration/2026-10-11_reliability_system.md).

    python scripts/reliability.py select     -> data/reliability/families.json   (families to build gene trees for)
    (Actions: gene-trees.yml with families_file=data/reliability/families.json, out_dir=results/reliability/gene_trees)
    python scripts/reliability.py verify     -> results/reliability/checks.npz   (gene-tree verdict per node x family)
    python scripts/reliability.py calibrate  -> results/reliability/calibration.json
    python scripts/reliability.py apply      -> results/reliability/ancestors.json (grades for every call at named nodes)

The gene-tree check for an ancestor X of the species tree (children A and B) and a family carried by
both sides: the model says present or absent at X. Under one shared origin before X, some eukaryote-only
clade of the gene tree holds sequences from both A and B.
    shared     a eukaryote-only clade with support >= 0.9 holds sequences from A and from B
    separate   even after collapsing every node with support < 0.9, no eukaryote-only group holds both
               (A and B copies sit apart, with prokaryote sequences between them on supported branches)
    unclear    otherwise
The gene tree is rooted on the prokaryote leaf farthest from the eukaryote leaves. Families without
prokaryote sequences in their tree are not checked (nothing could separate the copies).
"""

import argparse
import gzip
import hashlib
import json
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))

DATA = Path("data/reliability")
RES = Path("results/reliability")
TREES = [RES / "gene_trees" / "trees", Path("results/gene_trees/trees")]   # this run + pre-registration 6
SUPPORT = 0.9
GRADES = [("A", 0.9), ("B", 0.75), ("C", 0.5), ("D", 0.0)]


def acc_of(fams):
    meta = json.loads(Path("data/eukaryotes/pfam_meta.json").read_text())
    return {f: meta.get(f, {}).get("accession", "").split(".")[0] for f in fams}


# ---------------------------------------------------------------- 1. families
def select(per_decile=60, seed=0):
    from prokaryote_and_loso import prokaryote_shares
    z = np.load("results/leca_models/posteriors.npz", allow_pickle=False)
    fams = [str(f) for f in z["families"]]
    freq = z["clade_frequency"].astype(float)
    pro = prokaryote_shares(fams)
    acc = acc_of(fams)
    done = {f["family"] for f in json.loads(Path("data/gene_trees/families.json").read_text())["families"]}
    ok = np.array([(pro["bacteria"][i] >= 0.01 or pro["archaea"][i] >= 0.01) and acc[f] and f not in done
                   for i, f in enumerate(fams)])
    idx = np.flatnonzero(ok)
    edges = np.quantile(freq[idx], np.linspace(0, 1, 11))
    dec = np.clip(np.searchsorted(edges, freq, side="right") - 1, 0, 9)
    rng = np.random.default_rng(seed)
    picked = []
    for b in range(10):
        pool = [i for i in idx if dec[i] == b]
        picked += list(rng.choice(pool, min(per_decile, len(pool)), replace=False))
    out = [{"family": fams[i], "accession": acc[fams[i]], "eukaryote_frequency": round(float(freq[i]), 4)}
           for i in picked]
    DATA.mkdir(parents=True, exist_ok=True)
    (DATA / "families.json").write_text(json.dumps({
        "rule": f"families in >= 1% of UniProt bacterial or archaeal proteomes, not already in pre-registration 6; "
                f"{per_decile} per eukaryote-frequency decile, seed {seed}",
        "n_candidates": int(len(idx)), "families": out}, indent=1))
    print(f"{len(idx)} candidates, picked {len(out)}")


# ---------------------------------------------------------------- 2. gene-tree verdicts
def species_tree():
    from leca_v3_model import ROOTS, g3_fit, setup, shares_for, strata_of
    from tree_scramble_transfer import m7
    d, fams, names, sg, plastid, lineage = setup(ROOTS["amorphea"])
    strata = strata_of(fams, shares_for(fams))
    vis = np.zeros(len(d["parent"]), bool)
    vis[d["tips"]] = True
    p_g3, _ = g3_fit(d, vis, strata, use_strata=True, choose_mult=True)
    p_m7, _ = m7(d, vis)
    return d, fams, names, sg, p_g3, p_m7


def gene_tree_masks(nwk, panel, tip_index):
    """Rooted gene tree -> per node: species bitmask, eukaryote-only flag, support; plus collapsed groups."""
    from run_clade_ancestor import farthest_outgroup_tip, reroot
    from run_mito_ancestor import parse_newick, postorder
    parent, length, label = parse_newick(nwk.strip())
    _, children = postorder(parent)
    tips = [v for v in range(len(parent)) if not children[v]]
    is_e = {v: panel[label[v].split("|")[0]]["domain"] == "E" for v in tips}
    if all(is_e.values()):
        return None
    t = farthest_outgroup_tip(parent, np.maximum(length, 1e-6), set(tips), is_e)
    sup_label = {v: label[v] for v in range(len(parent)) if children[v]}
    tagged = [label[v] if not children[v] else f"__n{v}" for v in range(len(parent))]
    parent, length, lab = reroot(parent, np.maximum(length, 1e-6), tagged, t)
    order, children = postorder(parent)
    n = len(parent)
    sup = np.ones(n)
    for v in range(n):
        if children[v] and lab[v].startswith("__n"):
            try:
                sup[v] = float(sup_label[int(lab[v][3:])] or 1.0)
            except ValueError:
                sup[v] = 1.0
    mask = [0] * n
    pure = [True] * n
    for v in order:
        if not children[v]:
            up = lab[v].split("|")[0]
            if panel[up]["domain"] == "E":
                org = panel[up]["organism"].replace("'", "")
                mask[v] = 1 << tip_index[org] if org in tip_index else 0
            else:
                pure[v] = False
        else:
            for c in children[v]:
                mask[v] |= mask[c]
                pure[v] = pure[v] and pure[c]
    strong = [mask[v] for v in range(n) if children[v] and pure[v] and sup[v] >= SUPPORT]

    def lifted(v):
        out = []
        for c in children[v]:
            if children[c] and sup[c] < SUPPORT:
                out += lifted(c)
            else:
                out.append(c)
        return out
    groups = []
    for v in range(n):
        if children[v] and (v == 0 or sup[v] >= SUPPORT):
            if pure[v]:
                groups.append(mask[v])
            else:
                m = 0
                for c in lifted(v):
                    if pure[c]:
                        m |= mask[c]
                if m:
                    groups.append(m)
    present = mask[0] if pure[0] else 0
    for v in range(n):
        if not children[v]:
            present |= mask[v]
    return strong, groups, present


def verify():
    d, fams, names, sg, p_g3, p_m7 = species_tree()
    tips = d["tips"]
    tip_index = {names[v].replace("'", ""): i for i, v in enumerate(tips)}
    panel = json.loads(Path("data/gene_trees/panel.json").read_text())
    col = {f: j for j, f in enumerate(fams)}
    # species bitmask under each child of every internal node
    tipbit = {v: 1 << i for i, v in enumerate(tips)}
    msk = np.zeros(len(d["parent"]), dtype=object)
    for v in d["order"]:
        msk[v] = tipbit.get(v, 0)
        for c in d["children"][v]:
            msk[v] |= msk[c]
    internal = [v for v in range(len(d["parent"])) if len(d["children"][v]) >= 2]
    X = d["X"]
    rows = []
    seen = set()
    for folder in TREES:
        if not folder.exists():
            continue
        for f in sorted(folder.glob("*.nwk")):
            fam = f.stem
            if fam in seen or fam not in col:
                continue
            seen.add(fam)
            g = gene_tree_masks(f.read_text(), panel, tip_index)
            if g is None:
                continue
            strong, groups, present = g
            j = col[fam]
            for v in internal:
                kids = d["children"][v]
                A, B = msk[kids[0]], msk[kids[1]] if len(kids) == 2 else 0
                if len(kids) > 2:
                    B = 0
                    for c in kids[1:]:
                        B |= msk[c]
                if not (present & A) or not (present & B):
                    continue
                if any((m & A) and (m & B) for m in strong):
                    verdict = 1
                elif not any((m & A) and (m & B) for m in groups):
                    verdict = 0
                else:
                    verdict = -1
                under_tips = [t for t in tips if tipbit[t] & msk[v]]
                rows.append((j, v, verdict, float(p_g3[v, j]), float(p_m7[v, j]), float(d["depth"][v]),
                             len(under_tips), float(X[under_tips, j].mean())))
    arr = np.array(rows, dtype=float)
    RES.mkdir(parents=True, exist_ok=True)
    np.savez_compressed(RES / "checks.npz", rows=arr, families=fams,
                        columns=np.array(["family", "node", "verdict", "p_g3", "p_m7", "depth", "n_tips", "freq_under"]))
    v = arr[:, 2]
    print(f"{len(seen)} gene trees, {len(arr)} node x family checks: shared {int((v == 1).sum())}, "
          f"separate {int((v == 0).sum())}, unclear {int((v == -1).sum())}")


# ---------------------------------------------------------------- 3. calibration
def features(p_g3, p_m7, depth, n_tips, freq):
    conf = np.abs(p_g3 - 0.5) * 2
    return np.column_stack([np.log(np.clip(p_g3, 1e-4, 1)) - np.log(np.clip(1 - p_g3, 1e-4, 1)),
                            conf, np.abs(p_g3 - p_m7), depth, np.log(n_tips), freq])


def split(fams, js):
    return np.array([hashlib.md5(fams[int(j)].encode()).digest()[0] % 2 == 1 for j in js])


def fit_reliability(arr, fams):
    from sklearn.linear_model import LogisticRegression
    ok = arr[:, 2] >= 0
    a = arr[ok]
    y = a[:, 2]
    call = (a[:, 3] >= 0.5).astype(float)
    agree = (call == y).astype(float)
    Xf = features(a[:, 3], a[:, 4], a[:, 5], a[:, 6], a[:, 7])
    test = split(fams, a[:, 0])
    m = LogisticRegression(C=1.0, max_iter=2000).fit(Xf[~test], agree[~test])
    return m, a, agree, Xf, test


def calibrate():
    from organelle_evo.predict import auroc
    z = np.load(RES / "checks.npz", allow_pickle=False)
    arr, fams = z["rows"], [str(f) for f in z["families"]]
    m, a, agree, Xf, test = fit_reliability(arr, fams)
    rel = m.predict_proba(Xf)[:, 1]
    conf = np.abs(a[:, 3] - 0.5) * 2
    rng = np.random.default_rng(0)
    # bootstrap over families (rows of one family move together)
    fam_t = a[test, 0]
    uf = np.unique(fam_t)
    idx_by = {f: np.flatnonzero(fam_t == f) for f in uf}
    yt, rt, ct = agree[test], rel[test], conf[test]
    diffs = []
    for _ in range(1000):
        pick = rng.choice(uf, len(uf))
        ix = np.concatenate([idx_by[f] for f in pick])
        if yt[ix].min() != yt[ix].max():
            diffs.append(auroc(rt[ix], yt[ix]) - auroc(ct[ix], yt[ix]))
    lo, hi = np.percentile(diffs, [2.5, 97.5])
    grade = np.select([rt >= 0.9, rt >= 0.75, rt >= 0.5], ["A", "B", "C"], "D")
    by_grade = {g: {"n": int((grade == g).sum()), "observed_agreement": round(float(yt[grade == g].mean()), 3)
                    if (grade == g).any() else None} for g in "ABCD"}
    depth = a[test, 5]
    q = np.quantile(a[:, 5], [1 / 3, 2 / 3])
    by_depth = {}
    for name, sel in (("shallow", depth < q[0]), ("middle", (depth >= q[0]) & (depth < q[1])), ("deep", depth >= q[1])):
        by_depth[name] = {"n": int(sel.sum()), "agreement": round(float(yt[sel].mean()), 3),
                          "mean_reliability": round(float(rt[sel].mean()), 3)}
    res = {"preregistration": "docs/preregistration/2026-10-11_reliability_system.md",
           "n_checks": int(len(arr)), "n_decided": int(len(a)), "n_test": int(test.sum()),
           "agreement_overall_test": round(float(yt.mean()), 4),
           "auroc_reliability": round(float(auroc(rt, yt)), 4), "auroc_posterior_confidence": round(float(auroc(ct, yt)), 4),
           "reliability_minus_confidence": {"mean": round(float(auroc(rt, yt) - auroc(ct, yt)), 4),
                                            "ci95": [round(float(lo), 4), round(float(hi), 4)],
                                            "verdict": "양성" if lo > 0 else ("음성" if hi < 0 else "무승부")},
           "brier_reliability": round(float(np.mean((rt - yt) ** 2)), 4),
           "grades_on_test": by_grade, "by_depth_test": by_depth,
           "coefficients": dict(zip(["log_odds_p", "confidence", "model_gap", "depth", "log_n_tips", "freq_under"],
                                    [round(float(c), 4) for c in m.coef_[0]]))}
    (RES / "calibration.json").write_text(json.dumps(res, ensure_ascii=False, indent=1))
    print(json.dumps(res, ensure_ascii=False, indent=1))


# ---------------------------------------------------------------- 4. grades for every call at named ancestors
NAMED = {"LECA (진핵생물 공통조상)": None, "후편모생물 (동물+균류)": ["Metazoa", "Fungi"], "동물": ["Metazoa"],
         "균류": ["Fungi"], "녹색식물": ["Viridiplantae"], "Sar": ["Stramenopiles", "Alveolata", "Rhizaria"],
         "부등편모류": ["Stramenopiles"], "알베올라타": ["Alveolata"], "아메바류": ["Amoebozoa"], "Discoba": ["Discoba"],
         "메타모나다": ["Metamonada"], "홍조류": ["Rhodophyta"]}


def apply():
    from run_clade_ancestor import mrca
    from organelle_evo.predict import auroc
    z = np.load(RES / "checks.npz", allow_pickle=False)
    arr, fams_c = z["rows"], [str(f) for f in z["families"]]
    m, a, agree, Xf, test = fit_reliability(arr, fams_c)
    d, fams, names, sg, p_g3, p_m7 = species_tree()
    meta = json.loads(Path("data/eukaryotes/pfam_meta.json").read_text())
    tips = d["tips"]
    grp = {v: sg.get(names[v], "?") for v in tips}
    # new species (pre-registration 10) under each node, for the descendant check
    new_rows = json.loads(Path("results/new_species/per_species.json").read_text()) if Path(
        "results/new_species/per_species.json").exists() else []
    new_prof = {}
    for f in sorted(Path("data/new_species/shards").glob("*.json.gz")):
        for u, r in json.loads(gzip.open(f, "rt").read()).items():
            new_prof[r["organism"]] = set(r["pfam"])
    lin_pick = json.loads(Path("data/new_species/pick.json").read_text())["species"] if Path(
        "data/new_species/pick.json").exists() else {}
    new_lin = {v["organism"]: set(v["lineage"]) for v in lin_pick.values()}
    out = {}
    for label, groups in NAMED.items():
        sel = tips if groups is None else [v for v in tips if grp[v] in groups]
        if len(sel) < 2:
            continue
        node = group_node(d, set(sel)) if groups else 0
        under = [t for t in tips if node in _ancestors(d, t)]
        pg, pm = p_g3[node].astype(float), p_m7[node].astype(float)
        freq = d["X"][under].mean(0).astype(float)
        Xf_n = features(pg, pm, np.full(len(fams), d["depth"][node]), np.full(len(fams), len(under)), freq)
        rel = m.predict_proba(Xf_n)[:, 1]
        grade = np.select([rel >= 0.9, rel >= 0.75, rel >= 0.5], ["A", "B", "C"], "D")
        present = pg >= 0.5
        # descendant check: new species whose lineage contains one of the groups (or all, for LECA)
        desc = [o for o, L in new_lin.items() if (groups is None or L & set(groups) or
                any(x in L for x in groups)) and o in new_prof]
        desc_auc = None
        if desc:
            aucs = []
            for o in desc[:200]:
                y = np.array([f in new_prof[o] for f in fams], float)
                if 0 < y.sum() < len(y):
                    aucs.append(auroc(pg, y))
            desc_auc = round(float(np.mean(aucs)), 4) if aucs else None
        # gene-tree record at this node
        here = a[a[:, 1] == node]
        gt = {"n_checked": int(len(here)), "agreement": round(float(((here[:, 3] >= 0.5) == here[:, 2]).mean()), 3)
              if len(here) else None}
        out[label] = {
            "node_depth": round(float(d["depth"][node]), 3), "n_tips_under": len(under),
            "expected_size": round(float(pg.sum())), "n_present_calls": int(present.sum()),
            "grade_counts_present": {g: int(((grade == g) & present).sum()) for g in "ABCD"},
            "grade_counts_absent": {g: int(((grade == g) & ~present).sum()) for g in "ABCD"},
            "mean_reliability": round(float(rel.mean()), 3),
            "gene_tree_record": gt, "descendant_check": {"n_new_species": len(desc), "mean_auroc": desc_auc},
            "model_agreement": round(float(((pg >= 0.5) == (pm >= 0.5)).mean()), 4),
            "families": [{"f": fams[j], "d": meta.get(fams[j], {}).get("description", "")[:60],
                          "p": round(float(pg[j]), 3), "m7": round(float(pm[j]), 3), "r": round(float(rel[j]), 3),
                          "g": str(grade[j]), "fu": round(float(freq[j]), 3)}
                         for j in np.argsort(-pg) if pg[j] >= 0.2 or freq[j] >= 0.2]}
        print(f"{label}: size {out[label]['expected_size']}, present {present.sum()}, grades {out[label]['grade_counts_present']}, "
              f"gene trees {gt}, descendants {out[label]['descendant_check']}", flush=True)
    (RES / "ancestors.json").write_text(json.dumps(out, ensure_ascii=False))


def group_node(d, members):
    """The node with the most group tips among nodes whose tips are at least 90% group members (a few
    long-branch strays elsewhere in the tree do not drag the ancestor up to a mixed node)."""
    best, best_n = None, -1
    count, total = {}, {}
    for v in d["order"]:
        if not d["children"][v]:
            count[v], total[v] = int(v in members), 1
        else:
            count[v] = sum(count[c] for c in d["children"][v])
            total[v] = sum(total[c] for c in d["children"][v])
        if d["children"][v] and count[v] >= 0.9 * total[v] and count[v] > best_n:
            best, best_n = v, count[v]
    return best


def _ancestors(d, t):
    s, w = set(), t
    while w != -1:
        s.add(w)
        w = d["parent"][w]
    return s


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("step", choices=["select", "verify", "calibrate", "apply"])
    a = ap.parse_args()
    {"select": select, "verify": verify, "calibrate": calibrate, "apply": apply}[a.step]()


if __name__ == "__main__":
    main()
