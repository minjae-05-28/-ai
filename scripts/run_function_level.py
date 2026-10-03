"""Function-level prediction: does the law know which FUNCTIONS a lineage loses?

    python scripts/run_function_level.py --system parasites      (after run_forward_evolution.py)
    python scripts/run_function_level.py --system extremophiles

run_forward_evolution.py saves, for every held-out pair, each ancestral family's loss score
from the law (lineage held out, amount predicted from the design), the axis-free law and
memorisation (reference). Here families are pooled into functions (GO-slim categories and
the keyword classes used as law features), and for each pair and function with at least
MIN_FAMILIES ancestral families the share lost is compared with the prediction.

Compared, each rescaled to the law's own total amount so only the split across functions
differs:
    law               mean law loss probability of the function's families
    no_axes_law       same, axis-free law
    uniform           every function loses the same share (knows the amount, not the kind)
    memorisation      reference only: mean training loss frequency
Metrics per pair, then mean with a 95% interval over lineages:
    spearman          rank agreement between predicted and real per-function share lost
    mae               mean absolute error of the per-function share lost
    top_hit           of the 5 functions predicted to lose most, share that are in the real top 10
"""

import argparse
import json
import re
from pathlib import Path

import numpy as np
from scipy.stats import spearmanr

from organelle_evo.eukaryotes.features import KEYWORD_CLASSES

ANN = Path("data/eukaryotes")
MIN_FAMILIES = 8
METHODS = ("law", "no_axes_law", "uniform", "memorisation")


def functions(fams):
    meta = json.loads((ANN / "pfam_meta.json").read_text())
    ann = json.loads((ANN / "family_annotations.json").read_text())
    slims = ann["slims"]
    out = {}
    for i, f in enumerate(fams):
        for t in ann["families"].get(f, {}).get("go_slim", ()):
            if t in slims:
                out.setdefault(f"go:{slims[t]['name']}", []).append(i)
        text = f"{f} {meta.get(f, {}).get('description', '')}"
        for name, pat in KEYWORD_CLASSES:
            if re.search(pat, text):
                out.setdefault(f"kw:{name}", []).append(i)
    return {k: np.array(v) for k, v in out.items()}


def boot(vals, units, n=2000, seed=0):
    rng = np.random.default_rng(seed)
    by = {}
    for v, u in zip(vals, units):
        if np.isfinite(v):
            by.setdefault(u, []).append(v)
    keys = list(by)
    flat = [v for vs in by.values() for v in vs]
    stats = [np.mean([v for i in rng.choice(len(keys), len(keys)) for v in by[keys[i]]]) for _ in range(n)]
    return {"mean": round(float(np.mean(flat)), 4),
            "ci95": [round(float(np.percentile(stats, 2.5)), 4), round(float(np.percentile(stats, 97.5)), 4)]}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--system", choices=("parasites", "extremophiles", "parasites_consensus", "extremophiles_consensus"), required=True)
    ap.add_argument("--dir", default="results/forward_evolution")
    args = ap.parse_args()
    z = np.load(Path(args.dir) / f"{args.system}_scores.npz")
    fams, pairs, units = list(z["fams"]), list(z["pairs"]), list(z["units"])
    func = functions(fams)
    print(f"{args.system}: {len(pairs)} pairs, {len(func)} functions")

    rows = []
    for i, pair in enumerate(pairs):
        idx, lost = z[f"{i}|fam_idx"], z[f"{i}|real_lost"].astype(bool)
        pos = {f: k for k, f in enumerate(idx)}
        target = z[f"{i}|law"].sum()  # the law's own amount
        score = {}
        for m in ("law", "no_axes_law", "memorisation"):
            s = z[f"{i}|{m}"].astype(float)
            score[m] = np.clip(s * target / max(s.sum(), 1e-9), 0, 1)
        score["uniform"] = np.full(len(idx), target / len(idx))
        real, pred = [], {m: [] for m in METHODS}
        for name, members in func.items():
            k = [pos[j] for j in members if j in pos]
            if len(k) < MIN_FAMILIES:
                continue
            real.append(lost[k].mean())
            for m in METHODS:
                pred[m].append(score[m][k].mean())
        real = np.array(real)
        row = {"pair": pair, "unit": units[i], "n_functions": len(real)}
        top_real = set(np.argsort(-real)[:10])
        for m in METHODS:
            p = np.array(pred[m])
            row[f"{m}.spearman"] = float(spearmanr(p, real)[0]) if np.ptp(p) > 1e-9 else 0.0
            row[f"{m}.mae"] = float(np.abs(p - real).mean())
            row[f"{m}.top_hit"] = float(len(set(np.argsort(-p)[:5]) & top_real) / 5) if np.ptp(p) > 1e-9 else 5 / len(real) * 2
        rows.append(row)

    u = [r["unit"] for r in rows]
    summary = {"n_pairs": len(rows), "n_lineages": len(set(u)), "min_families_per_function": MIN_FAMILIES}
    for m in METHODS:
        for k in ("spearman", "mae", "top_hit"):
            summary[f"{m}.{k}"] = boot([r[f"{m}.{k}"] for r in rows], u)
    for other in ("uniform", "no_axes_law", "memorisation"):
        summary[f"spearman.law - {other}"] = boot([r["law.spearman"] - r[f"{other}.spearman"] for r in rows], u)
        summary[f"mae.law - {other}"] = boot([r["law.mae"] - r[f"{other}.mae"] for r in rows], u)
    print("summary (mean [95% CI over lineages]); uniform spearman is 0 by construction")
    for k, v in summary.items():
        if isinstance(v, dict):
            print(f"  {k:32s} {v['mean']:+.4f} {v['ci95']}")
    (Path(args.dir) / f"{args.system}_functions.json").write_text(json.dumps({"summary": summary, "pairs": rows}, indent=1))


if __name__ == "__main__":
    main()
