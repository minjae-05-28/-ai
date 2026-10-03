"""Does correcting for genome quality actually help? Known-truth simulation.

    PYTHONPATH=src python scripts/quality_correction.py [--families 800 --reps 3]

The simulator already drops a share of each tip's genes according to that tip's completeness, so
the truth about incompleteness is known. Four ways of handling it are scored against that truth
at the alphaproteobacterial root:

    none        observed absence taken at face value
    tip_mult    the current fix: loss accelerated on the terminal branch of flagged tips
    emission    the dropout written into the likelihood, with the TRUE completeness (the ceiling)
    estimated   the same, with completeness ESTIMATED from the data (what a real run can do)

The estimate is the one that matters: it is what scripts/genome_quality.py computes, and it uses
no outside information. If it lands near the ceiling, the correction is worth keeping.
"""

import argparse
import json
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
from mito_model_search import GENERATORS, fit, load_cache, posterior, simulate, visible_mask  # noqa: E402

from organelle_evo.predict import auroc  # noqa: E402

OUT = Path("results/quality_correction")
BASE = {"ratio": None, "root": "stationary", "min_busco": 0, "drop_mag": False, "mult": 14.0, "tip_mult": 1.0}


def logloss(p, y):
    p = np.clip(p, 1e-4, 1 - 1e-4)
    return float(-np.mean(y * np.log(p) + (1 - y) * np.log(1 - p)))


def estimate_completeness(obs, tips):
    """Completeness per tip from the data alone — the SAME function the reconstruction uses.

    It has to be the same one: an estimator validated here and a different one used in
    run_clade_ancestor would make this measurement say nothing about that run.
    """
    from genome_quality import completeness_for

    profiles = {v: {j for j in np.flatnonzero(obs[v])} for v in tips}
    scores, markers = completeness_for(profiles)
    if not markers:
        raise SystemExit("no marker families in the simulated set; the estimator would be undefined")
    return {v: max(float(c), 0.05) for v, c in scores.items()}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--families", type=int, default=800)
    ap.add_argument("--reps", type=int, default=3)
    ap.add_argument("--out", default=str(OUT))
    args = ap.parse_args()
    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    d = load_cache()
    ar, tips = d["alpha_root"], list(d["tips"])
    vis = visible_mask(d, BASE)
    rows = []
    for rep in range(args.reps):
        truth, obs = simulate(d, GENERATORS["reduced_x5"], args.families, seed=3000 + rep)
        t = truth[ar].astype(float)
        true_c = np.where(np.isfinite(d["busco"]), d["busco"] / 100, 0.9)
        est = estimate_completeness(obs, tips)
        est_vec = np.ones(len(d["parent"]))
        for v, c in est.items():
            est_vec[v] = c
        err = np.abs(est_vec[tips] - true_c[tips])
        ways = {
            "none": (dict(BASE), None),
            "tip_mult": ({**BASE, "tip_mult": 2.0}, None),
            "emission": (dict(BASE), np.where(np.isfinite(d["busco"]), d["busco"] / 100, 0.9)),
            "estimated": (dict(BASE), est_vec),
        }
        for name, (spec, comp) in ways.items():
            dd = dict(d)
            dd["completeness"] = comp
            g, lo, root, mult, _ = fit(dd, obs, vis, spec)
            post = posterior(dd, obs, vis, g, lo, mult, root)[ar]
            rows.append({"rep": rep, "way": name, "auroc": float(auroc(post, t)),
                         "logloss": logloss(post, t),
                         "size_bias": float((post.sum() - t.sum()) / max(t.sum(), 1))})
            r = rows[-1]
            print(f"rep{rep} {name:10s} AUROC {r['auroc']:.4f}  logloss {r['logloss']:.4f}  "
                  f"size {r['size_bias']:+.3f}", flush=True)
        print(f"  completeness estimate vs truth: median error {np.median(err):.3f}, "
              f"90th {np.percentile(err, 90):.3f}", flush=True)
        rows[-1]["completeness_median_error"] = float(np.median(err))

    agg = {}
    for name in ("none", "tip_mult", "emission", "estimated"):
        sel = [r for r in rows if r["way"] == name]
        agg[name] = {k: round(float(np.mean([r[k] for r in sel])), 4)
                     for k in ("auroc", "logloss", "size_bias")}
    best = min(agg, key=lambda k: agg[k]["logloss"])
    (out / "summary.json").write_text(json.dumps(
        {"generator": GENERATORS["reduced_x5"], "families": args.families, "reps": args.reps,
         "aggregate": agg, "best_by_logloss": best,
         "completeness_median_error": round(float(np.median(
             [r.get("completeness_median_error", np.nan) for r in rows
              if "completeness_median_error" in r])), 4),
         "runs": rows}, indent=1))
    print("\naggregate (mean over reps)")
    for k, v in agg.items():
        print(f"  {k:10s} AUROC {v['auroc']:.4f}  logloss {v['logloss']:.4f}  size {v['size_bias']:+.3f}")
    print(f"best by logloss: {best}\nDone -> {out}/summary.json")


if __name__ == "__main__":
    main()
