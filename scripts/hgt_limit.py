"""How much horizontal transfer can ancestral reconstruction survive?

    python scripts/hgt_limit.py [--levels 0,0.02,0.05,0.1,0.2,0.35,0.5,0.8]

Simulation with known truth on the real pruned GTDB tree (the cache of mito_model_search.py).
Gene families evolve by gain/loss along the branches, plus horizontal arrivals at a rate that is
swept from none to very high. At each level the ancestral posterior at the alphaproteobacterial
root is scored against the truth, next to two baselines:

    frequency   the family's share among present-day tips (no tree at all)
    root_prior  the model's own prior, i.e. the reconstruction with the data ignored

The useful question is not "does accuracy fall" (it must) but "at what transfer rate does the
reconstruction stop beating present-day frequency". Beyond that point a reconstruction for a clade
with that much transfer carries no information the modern genomes do not already give.
Written for the virus question (recombination and host gene uptake are high there), but the answer
is about the method, not about any one clade.
"""

import argparse
import json
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
from mito_model_search import GENERATORS, fit, load_cache, posterior, simulate, visible_mask  # noqa: E402

from organelle_evo.predict import auroc  # noqa: E402

OUT = Path("results/hgt_limit")
# The round-3 leader of the model search, used as the reconstruction model throughout.
SPEC = {"ratio": None, "root": "stationary", "min_busco": 97, "drop_mag": False, "mult": 14.0, "tip_mult": 1.0}


def logloss(p, y):
    p = np.clip(p, 1e-4, 1 - 1e-4)
    return float(-np.mean(y * np.log(p) + (1 - y) * np.log(1 - p)))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--levels", default="0,0.02,0.05,0.1,0.2,0.35,0.5,0.8")
    ap.add_argument("--families", type=int, default=800)
    ap.add_argument("--reps", type=int, default=3)
    ap.add_argument("--out", default=str(OUT))
    args = ap.parse_args()
    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    d = load_cache()
    ar = d["alpha_root"]
    vis = visible_mask(d, SPEC)
    rows = []
    for level in [float(x) for x in args.levels.split(",")]:
        gen = dict(GENERATORS["reduced_x5"])
        gen["hgt"] = level
        per_rep = []
        for rep in range(args.reps):
            truth, obs = simulate(d, gen, args.families, seed=1000 + rep)
            g, lo, root, mult, _ = fit(d, obs, vis, SPEC)
            post = posterior(d, obs, vis, g, lo, mult, root)[ar]
            t = truth[ar].astype(float)
            vis_tips = [v for v in d["tips"] if vis[v]]
            freq = obs[vis_tips].mean(0).astype(float)
            per_rep.append({
                "true_share": float(t.mean()),
                "recon_auroc": float(auroc(post, t)), "freq_auroc": float(auroc(freq, t)),
                "recon_logloss": logloss(post, t), "freq_logloss": logloss(freq, t),
                "prior_logloss": logloss(np.full_like(t, t.mean()), t),
                "recon_size_bias": float((post.sum() - t.sum()) / max(t.sum(), 1)),
                "freq_size_bias": float((freq.sum() - t.sum()) / max(t.sum(), 1)),
            })
        agg = {k: float(np.mean([r[k] for r in per_rep])) for k in per_rep[0]}
        agg["hgt"] = level
        agg["recon_beats_freq_auroc"] = agg["recon_auroc"] > agg["freq_auroc"]
        agg["recon_beats_freq_logloss"] = agg["recon_logloss"] < agg["freq_logloss"]
        rows.append(agg)
        print(f"hgt {level:4.2f}: ancestor share {agg['true_share']:.2f} | AUROC recon {agg['recon_auroc']:.3f} "
              f"freq {agg['freq_auroc']:.3f} | logloss recon {agg['recon_logloss']:.3f} freq {agg['freq_logloss']:.3f} "
              f"prior {agg['prior_logloss']:.3f} | size bias recon {agg['recon_size_bias']:+.3f} "
              f"freq {agg['freq_size_bias']:+.3f}", flush=True)
    # Two crossing points. Ranking (AUROC vs frequency) survives much longer than calibration:
    # once the reconstruction's log-loss is worse than the base rate, its probabilities are
    # overconfident and the ancestor size is inflated, so the numbers must not be quoted.
    for r in rows:
        r["recon_beats_prior_logloss"] = r["recon_logloss"] < r["prior_logloss"]
    worse_than_prior = [r["hgt"] for r in rows if not r["recon_beats_prior_logloss"]]
    worse_than_freq = [r["hgt"] for r in rows if not r["recon_beats_freq_logloss"]]
    summary = {"model": SPEC, "levels": rows, "reps": args.reps, "families": args.families,
               "calibration_breaks_at_hgt": (min(worse_than_prior) if worse_than_prior else None),
               "ranking_breaks_at_hgt": (min(worse_than_freq) if worse_than_freq else None),
               "note": "hgt is the per-unit-branch-length arrival rate used by mito_model_search.simulate; "
                       "the GTDB alphaproteobacterial subtree has branch lengths with a median of 0.009 and a "
                       "maximum of 0.70, so the arrival probability on a branch is about hgt x length x 10."}
    (out / "summary.json").write_text(json.dumps(summary, indent=1))
    print(f"\nprobabilities become worse than the base rate at hgt >= {summary['calibration_breaks_at_hgt']}; "
          f"ranking stops beating present-day frequency at hgt >= {summary['ranking_breaks_at_hgt']}")
    print(f"Done -> {out}/summary.json")


if __name__ == "__main__":
    main()
