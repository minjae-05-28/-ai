"""Are tumour-up unicellular-era genes cancer-cell weak points? DepMap test and target candidates
(pre-registration 21, docs/preregistration/2026-10-16_cancer_depmap_targets.md).

    python scripts/cancer_depmap.py   -> results/cancer_depmap/summary.json, candidates.tsv
"""

import json
import sys
from collections import Counter
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import cancer_atavism as ca  # noqa: E402
import cancer_proliferation as cp  # noqa: E402

DEP = Path("data/depmap")
OUT = Path("results/cancer_depmap")
LINEAGE = {"BRCA": ["Breast"], "LUAD": ["Lung"], "LUSC": ["Lung"], "COAD": ["Bowel"], "LIHC": ["Liver"],
           "KIRC": ["Kidney"], "KIRP": ["Kidney"], "KICH": ["Kidney"], "PRAD": ["Prostate"],
           "STAD": ["Esophagus/Stomach"], "BLCA": ["Bladder/Urinary Tract"], "HNSC": ["Head and Neck"],
           "THCA": ["Thyroid"]}
UP, UP_COHORT, SEL, CAND = 0.5, 1.0, 0.10, 0.25


def tumour_lfc():
    """gene -> {cohort: mean paired LFC} over the QC cohorts."""
    out = {}
    for p in sorted(ca.DATA.glob("*.npz")):
        z = np.load(p, allow_pickle=False)
        m = np.nanmean(z["lfc"].astype(np.float32), 0)
        expressed = (z["normal_mean"] >= 1) | (z["tumour_mean"] >= 1)
        for g, v, e in zip(z["genes"], m, expressed):
            if e:
                out.setdefault(str(g), {})[p.stem] = float(v)
    return out


def load_dep():
    dep = {}
    for line in (DEP / "gene_dependency.tsv").read_text().splitlines()[1:]:
        g, n, me, fd, ce = line.split("\t")
        dep[g] = {"n": int(n), "frac": float(fd), "common": ce == "1", "mean": float(me)}
    lines = (DEP / "lineage_dependency.tsv").read_text().splitlines()
    head = lines[0].split("\t")[1:]
    names = [h.rsplit(" (", 1)[0] for h in head]
    counts = [int(h.rsplit(" (", 1)[1].rstrip(")")) for h in head]
    lin = {}
    for line in lines[1:]:
        x = line.split("\t")
        lin[x[0]] = [float(v) if v != "nan" else np.nan for v in x[1:]]
    return dep, lin, names, counts


def odds_ratio(uc_sel, mc_sel):
    a, b = uc_sel.sum() + 0.5, (~uc_sel).sum() + 0.5
    c, d = mc_sel.sum() + 0.5, (~mc_sel).sum() + 0.5
    return (a / b) / (c / d)


def or_ci(uc_sel, mc_sel):
    rng = np.random.default_rng(ca.SEED)
    est = odds_ratio(uc_sel, mc_sel)
    bs = [odds_ratio(uc_sel[rng.integers(0, len(uc_sel), len(uc_sel))],
                     mc_sel[rng.integers(0, len(mc_sel), len(mc_sel))]) for _ in range(ca.N_BOOT)]
    lo, hi = np.percentile(bs, [2.5, 97.5])
    return {"odds_ratio": round(float(est), 3), "lo": round(float(lo), 3), "hi": round(float(hi), 3),
            "uc_selective_share": round(float(uc_sel.mean()), 4), "mc_selective_share": round(float(mc_sel.mean()), 4),
            "n_uc": int(len(uc_sel)), "n_mc": int(len(mc_sel)),
            "verdict": "양성" if lo > 1 else ("음성" if hi < 1 else "무승부")}


def compare(genes, ages, dep, include_common=False):
    g = [x for x in genes if x in ages and x in dep and (include_common or not dep[x]["common"])]
    uc = np.array([dep[x]["frac"] >= SEL for x in g if ages[x][0] <= 3])
    mc = np.array([dep[x]["frac"] >= SEL for x in g if ages[x][0] > 3])
    return or_ci(uc, mc)


def main():
    ages = ca.load_ages()
    go, hall, _ = cp.load_p()
    P = go | hall
    lfc = tumour_lfc()
    dep, lin, lin_names, lin_counts = load_dep()
    approved = set((DEP / "approved_drug_genes.txt").read_text().split())
    med = {g: float(np.median(list(v.values()))) for g, v in lfc.items() if len(v) >= 7}
    up = [g for g, m in med.items() if m >= UP and g not in P]
    flat = [g for g, m in med.items() if m < UP and g not in P]
    by_stratum = {}
    for g in up:
        if g in ages and g in dep and not dep[g]["common"]:
            by_stratum.setdefault(f"PS{ages[g][0]}", []).append(dep[g]["frac"] >= SEL)
    out = {"source": json.loads((DEP / "source.json").read_text()),
           "primary_up_genes": compare(up, ages, dep),
           "with_common_essentials": compare(up, ages, dep, include_common=True),
           "control_not_up": compare(flat, ages, dep),
           "selective_share_by_stratum": {k: [len(v), round(float(np.mean(v)), 4)]
                                          for k, v in sorted(by_stratum.items(), key=lambda x: int(x[0][2:]))}}
    rows, per = [], {}
    idx = {n: i for i, n in enumerate(lin_names)}
    for cohort, lins in LINEAGE.items():
        li = [idx[n] for n in lins if n in idx]
        nlines = sum(lin_counts[i] for i in li)
        if nlines < 10:
            per[cohort] = {"lineage_lines": nlines, "skipped": True}
            continue
        cands = []
        for g, v in lfc.items():
            if cohort not in v or v[cohort] < UP_COHORT or g in P or g not in ages or ages[g][0] > 3:
                continue
            if g not in dep or dep[g]["common"] or g not in lin:
                continue
            fr = lin[g]
            own = np.nansum([fr[i] * lin_counts[i] for i in li]) / nlines
            others = [j for j in range(len(lin_names)) if j not in li]
            on = sum(lin_counts[j] for j in others)
            other = np.nansum([fr[j] * lin_counts[j] for j in others]) / on
            if own >= CAND and own > other:
                cands.append((g, v[cohort], own, other, ages[g][0], g in approved))
        cands.sort(key=lambda x: -(x[2] - x[3]))
        per[cohort] = {"lineage_lines": nlines, "n_candidates": len(cands),
                       "with_approved_drug": sum(c[5] for c in cands)}
        for c in cands:
            rows.append(f"{cohort}\t{c[0]}\t{c[1]:.3f}\t{c[2]:.3f}\t{c[3]:.3f}\tPS{c[4]}\t{int(c[5])}")
    out["candidates"] = per
    n_all = sum(v.get("n_candidates", 0) for v in per.values())
    n_drug = sum(v.get("with_approved_drug", 0) for v in per.values())
    out["candidates_total"] = {"rows": n_all, "unique_genes": len({r.split("\t")[1] for r in rows}),
                               "with_approved_drug_rows": n_drug,
                               "cohorts_with_candidate": sum(v.get("n_candidates", 0) > 0 for v in per.values())}
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "summary.json").write_text(json.dumps(out, ensure_ascii=False, indent=1))
    (OUT / "candidates.tsv").write_text("cohort\tgene\ttumour_lfc\tlineage_dep_frac\tother_dep_frac\tage\tapproved_drug\n"
                                        + "\n".join(rows) + "\n")
    print(json.dumps(out, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
