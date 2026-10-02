"""Robustness of the headline numbers: bootstrap intervals and multiple-testing correction.

    python scripts/run_robustness.py

1. Bootstrap 95% intervals for the held-out AUROCs and for the differences that carry the
   conclusions (law vs memorisation, environment vs none). Resampling unit: the clade for
   leave-one-clade-out results (pairs of one clade are not independent), the pair otherwise.
2. Benjamini-Hochberg false discovery rate over every p-value the phylogenetic and GC
   re-tests report (rank GLS), so "survives" is judged across all laws tested together.
"""

import json
from pathlib import Path

import numpy as np

RNG = np.random.default_rng(0)
B = 4000


def boot(rows, keys, unit=None, diffs=()):
    groups = {}
    for r in rows:
        groups.setdefault(r[unit] if unit else r["pair"], []).append(r)
    g = list(groups.values())
    stats = {}
    for name, f in [*[(k, lambda rs, k=k: np.mean([r[k] for r in rs])) for k in keys],
                    *[(f"{a} - {b}", lambda rs, a=a, b=b: np.mean([r[a] - r[b] for r in rs])) for a, b in diffs]]:
        est = f(rows)
        samples = [f([r for i in RNG.integers(0, len(g), len(g)) for r in g[i]]) for _ in range(B)]
        lo, hi = np.percentile(samples, [2.5, 97.5])
        stats[name] = {"estimate": round(float(est), 4), "ci95": [round(float(lo), 4), round(float(hi), 4)]}
    return {"n_rows": len(rows), "n_units": len(g), "unit": unit or "pair", "stats": stats}


def bh(pvals):
    names = list(pvals)
    p = np.array([pvals[n] for n in names])
    order = np.argsort(p)
    q = np.empty(len(p))
    prev = 1.0
    for rank, i in reversed(list(enumerate(order, 1))):
        prev = min(prev, p[i] * len(p) / rank)
        q[i] = prev
    return {n: float(q[i]) for i, n in enumerate(names)}


def main():
    res = {"bootstrap": {}}
    load = lambda p: json.loads(Path(p).read_text()) if Path(p).exists() else None  # noqa: E731
    t = load("results/transfer/metrics.json")
    if t:
        res["bootstrap"]["parasites_leave_one_clade_out"] = boot(
            t["heldout"], ("law", "memorisation", "copies_only"), unit="clade", diffs=[("memorisation", "law")])
    f = load("results/features/metrics.json")
    if f:
        res["bootstrap"]["parasites_5fold"] = boot(
            f["heldout"], ("enriched", "base", "memorisation"), diffs=[("enriched", "base"), ("memorisation", "enriched")])
    e = load("results/environment_v2/metrics.json") or load("results/environment/metrics.json")
    if e:
        res["bootstrap"]["extremophiles_leave_one_pair_out"] = boot(
            e["heldout"], ("no_environment", "environment_law", "memorisation"),
            diffs=[("environment_law", "no_environment"), ("memorisation", "no_environment")])
    c = load("results/context_features/metrics.json")
    if c:
        for k, unit in (("parasites", "clade"), ("extremophiles", None)):
            res["bootstrap"][f"context_{k}"] = boot(
                c[k]["heldout"], ("law_base", "law_context", "memorisation", "combined_s3"), unit=unit,
                diffs=[("law_context", "law_base"), ("combined_s3", "memorisation")])
    for name, b in res["bootstrap"].items():
        print(f"\n{name} ({b['n_units']} {b['unit']}s)")
        for k, v in b["stats"].items():
            print(f"   {k:34s} {v['estimate']:+.3f}  [{v['ci95'][0]:+.3f}, {v['ci95'][1]:+.3f}]")

    pv = {}
    ph = load("results/phylo/metrics.json") or {}
    for k, r in ph.items():
        pv[f"phylo:{k}"] = r["rank_gls"][1]
    gc = load("results/gc_confound/metrics.json") or {}
    for part in ("species", "pairs", "symbionts"):
        for k, r in gc.get(part, {}).items():
            if isinstance(r, dict) and "with_gc" in r:
                pv[f"gc:{part}:{k}"] = r["with_gc"]["p_rank_gls"]
    q = bh(pv)
    res["fdr"] = {k: {"p": pv[k], "q": q[k], "significant_q05": q[k] < 0.05} for k in sorted(pv, key=pv.get)}
    print(f"\nBenjamini-Hochberg over {len(pv)} tests: {sum(v < 0.05 for v in q.values())} with q < 0.05 "
          f"({sum(v < 0.05 for v in pv.values())} with p < 0.05)")
    for k, v in res["fdr"].items():
        if (v["p"] < 0.05) != v["significant_q05"]:
            print(f"   changes verdict: {k} p {v['p']:.3f} -> q {v['q']:.3f}")
    out = Path("results/robustness")
    out.mkdir(parents=True, exist_ok=True)
    (out / "metrics.json").write_text(json.dumps(res, indent=2))
    print(f"Done -> {out}/")


if __name__ == "__main__":
    main()
