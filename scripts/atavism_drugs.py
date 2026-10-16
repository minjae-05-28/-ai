"""Reversal drugs and tilt-selective drugs / dependencies (pre-registration 23,
docs/preregistration/2026-10-16_atavism_drugs.md).

    python scripts/atavism_drugs.py   -> results/drug/summary.json, tilt_selective_compounds.tsv, tilt_dependencies.tsv
"""

import json
import re
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import cancer_atavism as ca  # noqa: E402

D = Path("data/drug")
OUT = Path("results/drug")
FDR = 0.10


def norm(name):
    return re.sub(r"[^a-z0-9]", "", (name or "").lower())


def table(path):
    lines = path.read_text().splitlines()
    head = lines[0].split("\t")
    return [dict(zip(head, x.split("\t"))) for x in lines[1:] if x]


def p_from_r(r, n):
    from scipy.stats import t as tdist
    tt = r * np.sqrt((n - 2) / max(1e-12, 1 - r * r))
    return float(2 * tdist.sf(abs(tt), n - 2))


def bh(p):
    p = np.asarray(p)
    o = np.argsort(p)
    q = np.empty(len(p))
    q[o] = np.minimum.accumulate((p[o] * len(p) / np.arange(1, len(p) + 1))[::-1])[::-1]
    return np.minimum(q, 1)


def l1000_names(tag):
    r = json.loads((D / f"l1000cds2_{tag}.json").read_text()).get("result") or {}
    top = r.get("topMeta") or []
    return [m.get("pert_desc") or m.get("pert_id") for m in top]


def diff_ci(a, b):
    rng = np.random.default_rng(ca.SEED)
    est = a.mean() - b.mean()
    bs = [rng.choice(a, len(a)).mean() - rng.choice(b, len(b)).mean() for _ in range(ca.N_BOOT)]
    lo, hi = np.percentile(bs, [2.5, 97.5])
    return {"difference": round(float(est), 4), "lo": round(float(lo), 4), "hi": round(float(hi), 4),
            "n_group": int(len(a)), "n_rest": int(len(b)),
            "verdict": "양성" if hi < 0 else ("음성" if lo > 0 else "무승부")}


def or_ci(sel, uc):
    rng = np.random.default_rng(ca.SEED)

    def orr(s, u):
        a = (s & u).sum() + .5
        b = (s & ~u).sum() + .5
        c = (~s & u).sum() + .5
        d = (~s & ~u).sum() + .5
        return (a / b) / (c / d)
    est = orr(sel, uc)
    bs = []
    for _ in range(ca.N_BOOT):
        i = rng.integers(0, len(sel), len(sel))
        bs.append(orr(sel[i], uc[i]))
    lo, hi = np.percentile(bs, [2.5, 97.5])
    return {"odds_ratio": round(float(est), 3), "lo": round(float(lo), 3), "hi": round(float(hi), 3),
            "n_selected": int(sel.sum()), "uc_share_selected": round(float(uc[sel].mean()), 4) if sel.any() else None,
            "uc_share_all": round(float(uc.mean()), 4), "verdict": "양성" if lo > 1 else ("음성" if hi < 1 else "무승부")}


def main():
    ages = ca.load_ages()
    src = json.loads((D / "source.json").read_text())
    lines = table(D / "lines.tsv")
    t = np.array([float(x["tilt"]) for x in lines])
    p = np.array([float(x["proliferation"]) for x in lines])
    out = {"source": src, "lines": len(lines), "tilt_vs_proliferation_r": round(float(np.corrcoef(t, p)[0, 1]), 3)}
    # (B) dependencies
    genes = table(D / "genes.tsv")
    r = np.array([float(g["rho_partial"]) for g in genes])
    n = np.array([int(g["n"]) for g in genes])
    q = bh([p_from_r(a, b) for a, b in zip(r, n)])
    sel = (r < 0) & (q < FDR)
    known = np.array([g["gene"] in ages for g in genes])
    uc = np.array([g["gene"] in ages and ages[g["gene"]][0] <= 3 for g in genes])
    out["B_dependencies"] = or_ci(sel[known], uc[known])
    order = np.argsort(r)
    dep_rows = ["gene\trho_partial\tq\tmean_effect\tage"]
    for i in order:
        if sel[i]:
            gname = genes[i]["gene"]
            dep_rows.append(f"{gname}\t{r[i]:.4f}\t{q[i]:.3g}\t{genes[i]['mean_effect']}\t"
                            f"{'PS' + str(ages[gname][0]) if gname in ages else ''}")
    (OUT / "tilt_dependencies.tsv").write_text("\n".join(dep_rows) + "\n")
    out["B_top_dependencies"] = dep_rows[1:21]
    # (A) compounds
    if (D / "compounds.tsv").exists():
        comps = table(D / "compounds.tsv")
        rc = np.array([float(c["rho_partial"]) for c in comps])
        rl = np.array([float(c["rho_lineage"]) for c in comps])
        nc = np.array([int(c["n"]) for c in comps])
        viab = np.array([float(c["mean_viability"]) for c in comps])
        qc = bh([p_from_r(a, b) for a, b in zip(rc, nc)])
        names = [norm(c["name"]) for c in comps]
        for tag in ("reverse", "mimic"):
            hits = {norm(x) for x in l1000_names(tag) if x}
            m = np.array([nm in hits and nm != "" for nm in names])
            out[f"A_{tag}"] = {"l1000_hits": len(hits), "matched_in_prism": int(m.sum()),
                               "matched_names": sorted({comps[i]["name"] for i in np.where(m)[0]}),
                               "partial_rho": diff_ci(rc[m], rc[~m]) if m.sum() >= 3 else None,
                               "mean_viability_group": round(float(viab[m].mean()), 4) if m.any() else None,
                               "mean_viability_rest": round(float(viab[~m].mean()), 4)}
        out["A_lineage_only_reverse"] = None
        hits = {norm(x) for x in l1000_names("reverse") if x}
        m = np.array([nm in hits and nm != "" for nm in names])
        if m.sum() >= 3:
            out["A_lineage_only_reverse"] = diff_ci(rl[m], rl[~m])
        o = np.argsort(rc)
        rows = ["compound\tname\tmoa\ttarget\trho_partial\tq\tmean_viability\tn"]
        for i in o:
            if rc[i] < 0 and qc[i] < FDR:
                c = comps[i]
                rows.append(f"{c['compound']}\t{c['name']}\t{c['moa']}\t{c['target']}\t{rc[i]:.4f}\t{qc[i]:.3g}\t"
                            f"{c['mean_viability']}\t{c['n']}")
        (OUT / "tilt_selective_compounds.tsv").write_text("\n".join(rows) + "\n")
        out["A_tilt_selective_compounds_fdr10"] = len(rows) - 1
        out["A_top_tilt_selective"] = rows[1:21]
        dep_set = {x.split("\t")[0] for x in dep_rows[1:]}
        targeted = [x for x in rows[1:] if any(tg.strip() in dep_set for tg in x.split("\t")[3].split(","))]
        out["dependencies_with_tilt_selective_drug"] = targeted[:20]
    (OUT / "summary.json").write_text(json.dumps(out, ensure_ascii=False, indent=1))
    print(json.dumps(out, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
