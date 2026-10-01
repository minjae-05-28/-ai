"""Mars with random laws: one minimal cell, environment variables only, no learned laws.

    python scripts/run_mars_random.py [--laws 200] [--workers 3]

Scenarios (the same random laws are reused across scenarios, so they are paired):
  gradual   early Mars lake -> present subsurface brine over 70% of the run
  abrupt    the same change over 10% of the run
  earth     Earth soil throughout (control: what random laws do with no Mars pressure)
  isolated_gradual / isolated_abrupt
            as above, but gene gain at 2%: no other organisms to take genes from
For each module: how often it grew or shrank among surviving lineages, and how much
more than in the Earth control. A module that changes the same way under most random
laws is a law-independent prediction; one that goes either way depends on the law.
"""

import argparse
import json
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

from organelle_evo.mars import (EARLY_MARS, EARTH_SOIL, ENV_VARS, MODERN_MARS, NAMES, START, STRESS_NAMES,
                                RandomLaw, evolve)

# name: (environment path, ramp share, gain scale)
SCENARIOS = {
    "gradual": ([EARLY_MARS, MODERN_MARS], 0.7, 1.0),
    "abrupt": ([EARLY_MARS, MODERN_MARS], 0.1, 1.0),
    "earth": ([EARTH_SOIL, EARTH_SOIL], 0.7, 1.0),
    # Mars has no other organisms to take genes from: new functions arise de novo only.
    "isolated_gradual": ([EARLY_MARS, MODERN_MARS], 0.7, 0.02),
    "isolated_abrupt": ([EARLY_MARS, MODERN_MARS], 0.1, 0.02),
}


def one(args):
    seed, scenario, generations = args
    law = RandomLaw.sample(np.random.default_rng(seed))
    path, ramp, gain_scale = SCENARIOS[scenario]
    r = evolve(law, path, generations=generations, ramp=ramp, gain_scale=gain_scale,
               rng=np.random.default_rng(10_000 + seed))
    r.update(seed=seed, scenario=scenario)
    return r


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--laws", type=int, default=200)
    ap.add_argument("--control-laws", type=int, default=100)
    ap.add_argument("--generations", type=int, default=6000)
    ap.add_argument("--workers", type=int, default=3)
    ap.add_argument("--out", default="results/mars_random")
    args = ap.parse_args()
    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)

    mars_scenarios = [sc for sc in SCENARIOS if sc != "earth"]
    jobs = [(s, sc, args.generations) for sc in mars_scenarios for s in range(args.laws)]
    jobs += [(s, "earth", args.generations) for s in range(args.control_laws)]
    with ProcessPoolExecutor(args.workers) as ex:
        runs = list(ex.map(one, jobs, chunksize=4))

    start = START.astype(float)
    summary = {}
    for sc in SCENARIOS:
        rs = [r for r in runs if r["scenario"] == sc]
        alive = [r for r in rs if r["survived"]]
        F = np.array([r["final"] for r in alive]) if alive else np.zeros((0, len(NAMES)))
        summary[sc] = {
            "n_laws": len(rs), "survived": len(alive), "survival_rate": len(alive) / len(rs),
            "median_genes": float(np.median(F.sum(1))) if len(F) else None,
            "modules": {m: {"median": float(np.median(F[:, i])) if len(F) else None,
                            "share_grew": float((F[:, i] >= start[i] + 2).mean()) if len(F) else None,
                            "share_shrank": float((F[:, i] <= start[i] - 2).mean()) if len(F) else None}
                        for i, m in enumerate(NAMES)},
        }
        print(f"{sc:8s} survived {len(alive)}/{len(rs)}; median genome {summary[sc]['median_genes']}")

    # Law-independent changes: share of surviving Mars lineages that moved a module in the
    # same direction, compared with the Earth control under the same laws.
    conv = []
    for i, m in enumerate(NAMES):
        g, e = summary["gradual"]["modules"][m], summary["earth"]["modules"][m]
        conv.append({"module": m, "start": int(start[i]), "mars_median": g["median"], "earth_median": e["median"],
                     "mars_grew": g["share_grew"], "mars_shrank": g["share_shrank"],
                     "earth_grew": e["share_grew"], "earth_shrank": e["share_shrank"]})
    conv.sort(key=lambda r: -abs((r["mars_grew"] - r["mars_shrank"]) - (r["earth_grew"] - r["earth_shrank"])))
    print("\nmodule                 start  Mars median  grew/shrank   Earth median  grew/shrank")
    for r in conv:
        print(f"  {r['module']:22s} {r['start']:4d}  {r['mars_median']:8.1f}   {r['mars_grew']:.2f}/{r['mars_shrank']:.2f}"
              f"     {r['earth_median']:8.1f}   {r['earth_grew']:.2f}/{r['earth_shrank']:.2f}")

    # Which random-law coefficients separate survivors from extinctions (abrupt scenario)?
    cand = [sc for sc in ("isolated_abrupt", "isolated_gradual", "abrupt")
            if 0 < np.mean([r["survived"] for r in runs if r["scenario"] == sc]) < 1]
    driver_scenario = cand[0] if cand else "abrupt"
    ab = [r for r in runs if r["scenario"] == driver_scenario]
    y = np.array([r["survived"] for r in ab], dtype=float)
    drivers = []
    if 0 < y.mean() < 1:
        for kind in ("loss", "dup", "gain"):
            W = np.array([getattr(RandomLaw.sample(np.random.default_rng(r["seed"])), kind) for r in ab])
            for i, m in enumerate(NAMES):
                for k, s in enumerate(STRESS_NAMES):
                    v = W[:, i, k]
                    corr = float(np.corrcoef(v, y)[0, 1])
                    drivers.append({"kind": kind, "module": m, "stress": s, "corr_with_survival": corr})
        drivers.sort(key=lambda d: -abs(d["corr_with_survival"]))
        print(f"\nrandom-law terms that most decide survival ({driver_scenario}):")
        for d in drivers[:10]:
            print(f"  {d['kind']:4s} rate of {d['module']:22s} under {d['stress']:11s} r = {d['corr_with_survival']:+.2f}")

    (out / "metrics.json").write_text(json.dumps({
        "environments": {e.name: dict(zip(ENV_VARS, e.vector().tolist())) for e in (EARTH_SOIL, EARLY_MARS, MODERN_MARS)},
        "start_genome": dict(zip(NAMES, map(int, START))), "summary": summary, "modules": conv,
        "survival_drivers": drivers[:30], "driver_scenario": driver_scenario,
        "extinctions": [{"scenario": r["scenario"], "seed": r["seed"], "at": r["extinct_at"]} for r in runs if not r["survived"]],
    }, indent=2))

    fig, ax = plt.subplots(figsize=(10, 5.5))
    order = [r["module"] for r in conv][::-1]
    yy = np.arange(len(order))
    net = lambda sc, m: summary[sc]["modules"][m]["share_grew"] - summary[sc]["modules"][m]["share_shrank"]  # noqa: E731
    ax.barh(yy + 0.2, [net("gradual", m) for m in order], 0.4, color="#e76f51", label="Mars (gradual)")
    ax.barh(yy - 0.2, [net("earth", m) for m in order], 0.4, color="#8d99ae", label="Earth control")
    ax.set_yticks(yy, [m.replace("_", " ") for m in order], fontsize=8)
    ax.axvline(0, color="k", lw=0.8)
    ax.set(xlabel="share of random laws where the module grew minus share where it shrank", xlim=(-1, 1),
           title=f"One minimal cell, {summary['gradual']['n_laws']} random laws: what does Mars do to it?")
    ax.legend(fontsize=8)
    fig.tight_layout()
    fig.savefig(out / "fig_mars_random.png", dpi=130)
    print(f"Done -> {out}/")


if __name__ == "__main__":
    main()
