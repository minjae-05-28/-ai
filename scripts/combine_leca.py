"""LECA from several root positions: what holds whichever root is right.

    python scripts/combine_leca.py --roots discoba,opisthokonta,metamonada
        reads   results/clade_ancestor/leca_<root>/, results/node_power/leca_<root>/,
                results/hgt_rate/leca_<root>/
        writes  results/clade_ancestor/leca/{summary.json,posterior.npz}
                results/node_power/leca/summary.json   (each root's grade + the worst of them)
                results/hgt_rate/leca/summary.json     (the highest of the roots' transfer levels)

Why: eukaryotes have no usable outgroup at this distance (archaea are too far for gene-content
models), so the tree is rooted on a named split and the root position is the open question
(Discoba, Amorphea/unikont-bikont, Metamonada are the live proposals). A family is called
present in LECA only if it is present under every root, absent only if absent under every root;
the rest is reported as root-dependent, not averaged into a number that hides the disagreement.
The output files keep the single-clade format so the atlas and the vault read them unchanged;
their `posterior` is the MINIMUM over roots (a conservative "present"), `model_sd` the spread.
"""

import argparse
import json
from pathlib import Path

import numpy as np

KEY = "표본이 도달한 마디"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--roots", default="discoba,opisthokonta,metamonada")
    ap.add_argument("--prefix", default="leca", help="run-name prefix: leca, leca2")
    args = ap.parse_args()
    roots = args.roots.split(",")
    runs = {}
    for r in roots:
        d = Path(f"results/clade_ancestor/{args.prefix}_{r}")
        if not (d / "summary.json").exists():
            raise SystemExit(f"missing {d}")
        z = np.load(d / "posterior.npz", allow_pickle=False)
        runs[r] = (json.loads((d / "summary.json").read_text()), {k: z[k] for k in z.files})
    fams = sorted(set.intersection(*[set(map(str, z["families"])) for _, z in runs.values()]))
    P = []
    for r in roots:
        col = {str(f): i for i, f in enumerate(runs[r][1]["families"])}
        P.append(np.array([runs[r][1]["posterior"][col[f]] for f in fams]))
    P = np.stack(P)
    lo, hi = P.min(0), P.max(0)
    s0, z0 = runs[roots[0]]
    col0 = {str(f): i for i, f in enumerate(z0["families"])}
    freq = np.array([z0["clade_frequency"][col0[f]] for f in fams])
    robust_present = lo >= 0.9
    robust_absent = hi < 0.1
    dependent = ~robust_present & ~robust_absent & ((hi >= 0.9) | (lo < 0.1)) & (hi - lo >= 0.5)

    power, grades = {}, {}
    for r in roots:
        f = Path(f"results/node_power/{args.prefix}_{r}/summary.json")
        if f.exists():
            agg = json.loads(f.read_text())["aggregate"]
            grades[r] = next((v for k, v in agg.items() if KEY in k), None)
    if grades and all(grades.values()):
        worst = min(grades, key=lambda r: grades[r]["auroc_margin"])
        power = {f"{args.prefix} ({KEY}, 뿌리 {len(grades)}곳 중 가장 나쁜 값: {worst})": grades[worst],
                 **{f"뿌리 {r}": g for r, g in grades.items()}}
        out = Path(f"results/node_power/{args.prefix}")
        out.mkdir(parents=True, exist_ok=True)
        (out / "summary.json").write_text(json.dumps({"note": "세 뿌리 위치 각각의 알려진 정답 채점과 그중 "
                                                               "가장 나쁜 값", "aggregate": power},
                                                     ensure_ascii=False, indent=1))
    hg = {}
    for r in roots:
        f = Path(f"results/hgt_rate/{args.prefix}_{r}/summary.json")
        if f.exists():
            hg[r] = json.loads(f.read_text())["sets"][f"{args.prefix}_{r}"]
    if hg:
        top = max(hg, key=lambda r: hg[r]["estimated_hgt"])
        out = Path(f"results/hgt_rate/{args.prefix}")
        out.mkdir(parents=True, exist_ok=True)
        (out / "summary.json").write_text(json.dumps({"sets": {args.prefix: {**hg[top], "label": f"진핵생물 전체 "
                                                                         f"(뿌리별 가장 높은 값: {top})"}},
                                                      "per_root": {r: v["estimated_hgt"] for r, v in hg.items()}},
                                                     ensure_ascii=False, indent=1))

    from run_mito_ancestor import functions_of
    func, meta = functions_of(fams)

    def rows(mask, n=60):
        ix = [i for i in np.argsort(-(lo + hi)) if mask[i]][:n]
        return [{"family": fams[i], "description": meta.get(fams[i], {}).get("description", ""),
                 **{f"posterior_{r}": round(float(P[k, i]), 3) for k, r in enumerate(roots)},
                 "share_of_tips_today": round(float(freq[i]), 3)} for i in ix]

    from collections import Counter
    summary = {
        "clade": args.prefix, "roots": roots, "tips": s0["tips"], "clade_tips": s0["clade_tips"],
        "clade_species": s0["clade_species"], "families_considered": len(fams),
        "rooted_on": " / ".join(runs[r][0]["rooted_on"] for r in roots),
        "root_split_intruders": {r: runs[r][0].get("root_split_intruders") for r in roots},
        "misplaced_clade_tips_left_out": [], "non_clade_tips_inside_clade_node": [],
        "n_bootstrap_trees": min(runs[r][0].get("n_bootstrap_trees", 0) for r in roots),
        "leave_tips_out_auroc": s0["leave_tips_out_auroc"],
        "leave_tips_out_auroc_per_root": {r: runs[r][0]["leave_tips_out_auroc"] for r in roots},
        "sum_of_posteriors_per_root": {r: round(float(P[k].sum()), 1) for k, r in enumerate(roots)},
        "n_present_per_root": {r: int((P[k] >= 0.9).sum()) for k, r in enumerate(roots)},
        "n_confident_families": int(robust_present.sum()),
        "n_uncertain_families": int(dependent.sum()),
        "n_robust_absent": int(robust_absent.sum()),
        "functions_of_confident_families": Counter(t for i in np.flatnonzero(robust_present)
                                                   for t in func[i]).most_common(20),
        "functions_of_root_dependent_families": Counter(t for i in np.flatnonzero(dependent)
                                                        for t in func[i]).most_common(20),
        "top_families": rows(robust_present), "root_dependent_families": rows(dependent),
        "rule": "present = posterior >= 0.9 under every root; absent = < 0.1 under every root; root-dependent "
                "= >= 0.9 under one root and < 0.1 or far lower under another (spread >= 0.5)",
    }
    out = Path(f"results/clade_ancestor/{args.prefix}")
    out.mkdir(parents=True, exist_ok=True)
    np.savez_compressed(out / "posterior.npz", families=np.array(fams), posterior=lo, model_sd=P.std(0),
                        tree_sd=np.zeros(len(fams)), clade_frequency=freq, per_root=P, roots=np.array(roots),
                        posterior_max=hi)
    (out / "summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=1))
    print(f"robust present {robust_present.sum()}, robust absent {robust_absent.sum()}, root-dependent "
          f"{dependent.sum()} of {len(fams)}")
    print("present per root:", summary["n_present_per_root"])
    print(f"-> {out}")


if __name__ == "__main__":
    import sys
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    main()
