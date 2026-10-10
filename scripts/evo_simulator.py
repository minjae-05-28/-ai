"""Evolution simulator at the gene-family level (pre-registration 8:
docs/preregistration/2026-10-10_evolution_simulator.md).

    python scripts/evo_simulator.py bank      -> results/simulator/laws.npz   (base laws, G3c fit)
    python scripts/evo_simulator.py replay    -> results/simulator/replay.json (pre-registered test)
    python scripts/evo_simulator.py run --start leca --schedule "anaerobic:0.3,parasitic+anaerobic:0.2" --reps 200
        -> results/simulator/runs/<name>.json

Input: a genome as a set of Pfam families. Environment schedule: segments of (set of environments,
time in tree branch-length units). Output: the distribution of descendant genomes over repeated runs.

Laws:
  base         per family, the posterior over the (loss, gain/loss) grid from the G3c fit (empirical
               Bayes rate prior, prokaryote strata, reduced-lineage multiplier); a grid point is drawn
               per family and run
  environment  per environment and family, loss and gain multipliers from the independent origins in
               transition_catalog.py, shrunk toward the environment's genome-wide rate and scaled by the
               unicellular control pairs

Only gene-family presence is simulated. No sequence is produced, and no new family is invented: a
family can only be gained if it exists somewhere in the collected proteomes. This is "what our laws
imply", not a forecast of real organisms.
"""

import argparse
import json
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import transition_catalog as T  # noqa: E402
from run_transitions import gains, load_profiles, losses  # noqa: E402

from organelle_evo.predict import auroc  # noqa: E402

OUT = Path("results/simulator")
ALPHA = 2.0
ENVS = {
    "anaerobic": {k: (v["anaerobes"], v["relatives"]) for k, v in T.ANAEROBIC.items()},
    "parasitic": {k: (v["derived"], v["relatives"]) for k, v in T.AEROBIC_PARASITES.items()},
    "multicellular": {k: (v["derived"], v["relatives"]) for k, v in T.MULTICELLULAR.items()},
    # pre-registration 9
    "flagellum_loss": {k: (v["derived"], v["relatives"]) for k, v in T.FLAGELLUM_LOSS.items()},
    "photosynthesis_loss": {k: (v["derived"], v["relatives"]) for k, v in T.PHOTOSYNTHESIS_LOSS.items()},
    "acid_heat": {k: (v["derived"], v["relatives"]) for k, v in T.ACID_HEAT.items()},
}
FAILED_LAWS = {"multicellular": "the multicellular transition law was judged negative "
                                "(multicellular_transition_v1); its multipliers are shown but not validated"}


# ---------------------------------------------------------------- base laws
def build_bank():
    from leca_v3_model import GRID, ROOTS, g3_fit, setup, shares_for, strata_of
    d, fams, names, sg, plastid, _ = setup(ROOTS["amorphea"])
    strata = strata_of(fams, shares_for(fams))
    vis = np.zeros(len(d["parent"]), bool)
    vis[d["tips"]] = True
    R, info = g3_fit(d, vis, strata, use_strata=True, choose_mult=True, return_weights=True)
    OUT.mkdir(parents=True, exist_ok=True)
    np.savez_compressed(OUT / "laws.npz", families=fams, grid=np.array(GRID, np.float32),
                        weights=R.astype(np.float32), strata=strata, tree_depth=float(np.mean(d["depth"][d["tips"]])))
    print(f"base laws for {len(fams)} families, m = {info['m']}")


class Simulator:
    def __init__(self, prof=None):
        z = np.load(OUT / "laws.npz", allow_pickle=False)
        self.fams = [str(f) for f in z["families"]]
        self.col = {f: j for j, f in enumerate(self.fams)}
        self.grid = z["grid"].astype(float)            # (G, 2): loss, gain
        self.W = z["weights"].astype(float)            # (G, F)
        self.default = self.W.mean(1)                  # families outside the bank: the average family
        self.tree_depth = float(z["tree_depth"])
        self.prof = prof if prof is not None else load_profiles()
        self.universe = sorted({f for p in self.prof.values() for f in p} | set(self.fams))

    def weights(self, fams):
        return np.stack([self.W[:, self.col[f]] if f in self.col else self.default for f in fams], 1)

    # -------------------------------------------------------- environment laws
    def env_laws(self, env, exclude=None):
        origins = {k: v for k, v in ENVS[env].items() if k != exclude}
        lt = [losses(self.prof, d, r) for d, r in origins.values()]
        gt = [gains(self.prof, d, r) for d, r in origins.values()]
        ctrl_l, ctrl_g = [], []
        for a, b in T.UNICELLULAR_CONTROLS.values():
            for x, y in ((a, b), (b, a)):
                ctrl_l.append(losses(self.prof, x, y))
                ctrl_g.append(gains(self.prof, x, y))
        q0 = np.mean([np.mean(list(t.values())) for t in ctrl_l])
        g0 = np.mean([np.mean(list(t.values())) for t in ctrl_g])
        qE = np.mean([np.mean(list(t.values())) for t in lt])
        gE = np.mean([np.mean(list(t.values())) for t in gt])

        def mult(tables, prior, base):
            k, n = {}, {}
            for t in tables:
                for f, v in t.items():
                    k[f] = k.get(f, 0) + v
                    n[f] = n.get(f, 0) + 1
            out = {f: (k[f] + ALPHA * prior) / (n[f] + ALPHA) for f in n}
            conv = lambda q: float(np.clip(np.log(1 - np.clip(q, 1e-4, 0.999)) / np.log(1 - base), 0.1, 100))
            return {f: conv(q) for f, q in out.items()}, conv(prior)
        lm, l_default = mult(lt, qE, q0)
        gm, g_default = mult(gt, gE, g0)
        return {"loss": lm, "gain": gm, "loss_default": l_default, "gain_default": g_default,
                "q_env": qE, "q_control": q0, "g_env": gE, "g_control": g0, "n_origins": len(origins)}

    # -------------------------------------------------------- the run
    def probabilities(self, start, fams, schedule, laws):
        """Exact P(present at the end) per family, averaged over its grid posterior.
        schedule: [(set_of_envs, t)], laws: {env: env_laws(...)}"""
        Wf = self.weights(fams)                              # (G, F)
        lo0, g0 = self.grid[:, :1], self.grid[:, 1:2]        # (G, 1)
        p = np.repeat(np.array([f in start for f in fams], float)[None, :], len(self.grid), 0)
        for envs, t in schedule:
            lm = np.ones(len(fams))
            gm = np.ones(len(fams))
            for e in envs:
                L = laws[e]
                lm *= np.array([L["loss"].get(f, L["loss_default"]) for f in fams])
                gm *= np.array([L["gain"].get(f, L["gain_default"]) for f in fams])
            lo, g = lo0 * lm[None, :], g0 * gm[None, :]
            r = lo + g
            e = np.exp(-r * t)
            pi = g / r
            p = p * (pi + (1 - pi) * e) + (1 - p) * pi * (1 - e)
        return (Wf * p).sum(0)

    def sample(self, start, fams, schedule, laws, reps=200, seed=0):
        """Repeated runs: a grid point per family per run, then the states along the schedule."""
        rng = np.random.default_rng(seed)
        Wf = self.weights(fams)
        cum = np.cumsum(Wf / Wf.sum(0, keepdims=True), 0)
        out = np.zeros((reps, len(fams)), bool)
        for r_ in range(reps):
            k = (rng.random(len(fams))[None, :] > cum).sum(0).clip(0, len(self.grid) - 1)
            lo, g = self.grid[k, 0], self.grid[k, 1]
            state = np.array([f in start for f in fams])
            for envs, t in schedule:
                lm = np.ones(len(fams))
                gm = np.ones(len(fams))
                for e in envs:
                    L = laws[e]
                    lm *= np.array([L["loss"].get(f, L["loss_default"]) for f in fams])
                    gm *= np.array([L["gain"].get(f, L["gain_default"]) for f in fams])
                lo_e, g_e = lo * lm, g * gm
                rr = lo_e + g_e
                e = np.exp(-rr * t)
                pi = g_e / rr
                p1 = np.where(state, pi + (1 - pi) * e, pi * (1 - e))
                state = rng.random(len(fams)) < p1
            out[r_] = state
        return out

    def calibrate_time(self, start, q0):
        """Time at which base laws alone lose a share q0 of the start genome (from the control pairs)."""
        fams = sorted(start)
        lo_t, hi_t = 1e-4, 20.0
        for _ in range(60):
            mid = np.sqrt(lo_t * hi_t)
            lost = 1 - self.probabilities(start, fams, [(set(), mid)], {}).mean()
            lo_t, hi_t = (mid, hi_t) if lost < q0 else (lo_t, mid)
        return float(np.sqrt(lo_t * hi_t))


# ---------------------------------------------------------------- pre-registered replay test
def replay(reps=200, envs=None, out_name="replay.json"):
    sim = Simulator()
    prevalence = {}
    for p in sim.prof.values():
        for f in p:
            prevalence[f] = prevalence.get(f, 0) + 1
    n_sp = len(sim.prof)
    res = {"preregistration": "docs/preregistration/2026-10-10_evolution_simulator.md", "envs": {}}
    for env, origins in ENVS.items():
        if envs and env not in envs:
            continue
        kind = "gain" if env == "multicellular" else "loss"
        rows = {}
        for o, (derived, relatives) in origins.items():
            laws = {env: sim.env_laws(env, exclude=o)}
            start = {f for f in {f for n in relatives for f in sim.prof[n]}
                     if sum(f in sim.prof[n] for n in relatives) >= len(relatives) / 2}
            t = sim.calibrate_time(start, laws[env]["q_control"])
            if kind == "loss":
                table = losses(sim.prof, derived, relatives)
            else:
                table = gains(sim.prof, derived, relatives)
            fams = sorted(table)
            y = np.array([table[f] for f in fams], float)
            if y.min() == y.max():
                continue
            S_env = sim.sample(start, fams, [({env}, t)], laws, reps=reps, seed=0).mean(0)
            S_base = sim.sample(start, fams, [(set(), t)], {}, reps=reps, seed=0).mean(0)
            other = [losses(sim.prof, d, r) if kind == "loss" else gains(sim.prof, d, r)
                     for k, (d, r) in origins.items() if k != o]
            law = np.array([np.mean([tb[f] for tb in other if f in tb]) if any(f in tb for tb in other) else 0.0
                            for f in fams])
            rar = np.array([1 - prevalence.get(f, 0) / n_sp for f in fams])
            if kind == "loss":
                score = {"simulator_env": 1 - S_env, "simulator_base": 1 - S_base, "transition_law": law, "rarity": rar}
            else:
                score = {"simulator_env": S_env, "simulator_base": S_base, "transition_law": law, "rarity": 1 - rar}
            rows[o] = {k: round(float(auroc(v, y)), 4) for k, v in score.items()}
            rows[o].update({"n_candidates": len(fams), "n_changed": int(y.sum()), "time": round(t, 4)})
            print(f"  {env} {o}: " + ", ".join(f"{k} {rows[o][k]}" for k in score), flush=True)
        diffs = {}
        rng = np.random.default_rng(0)
        keys = list(rows)
        for a, b in (("simulator_env", "simulator_base"), ("simulator_env", "transition_law"),
                     ("simulator_env", "rarity")):
            d = np.array([rows[k][a] - rows[k][b] for k in keys])
            bs = [d[rng.integers(0, len(d), len(d))].mean() for _ in range(2000)]
            lo, hi = np.percentile(bs, [2.5, 97.5])
            diffs[f"{a}_minus_{b}"] = {"mean": round(float(d.mean()), 4), "ci95": [round(float(lo), 4), round(float(hi), 4)],
                                       "verdict": "양성" if lo > 0 else ("음성" if hi < 0 else "무승부")}
        res["envs"][env] = {"kind": kind, "origins": rows, **diffs}
        if env in FAILED_LAWS:
            res["envs"][env]["note"] = FAILED_LAWS[env]
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / out_name).write_text(json.dumps(res, ensure_ascii=False, indent=1))
    print(json.dumps({e: {k: v for k, v in r.items() if k != "origins"} for e, r in res["envs"].items()},
                     ensure_ascii=False, indent=1))


# ---------------------------------------------------------------- free runs
def run(start_name, schedule_text, reps, seed, name):
    sim = Simulator()
    if start_name == "leca":
        z = np.load("results/leca_v3/leca_posterior.npz", allow_pickle=False)
        start = {str(f) for f, p in zip(z["families"], z["posterior"]) if p >= 0.5}
        start_label = "LECA (G3, P >= 0.5 under every root)"
    else:
        start = set(sim.prof[start_name])
        start_label = start_name
    schedule = []
    for seg in schedule_text.split(","):
        envs, t = seg.rsplit(":", 1)
        schedule.append(({e for e in envs.split("+") if e and e != "none"}, float(t)))
    laws = {e: sim.env_laws(e) for e in {e for envs, _ in schedule for e in envs}}
    fams = sim.universe
    S = sim.sample(start, fams, schedule, laws, reps=reps, seed=seed)
    freq = S.mean(0)
    sizes = S.sum(1)
    start_v = np.array([f in start for f in fams])
    lost = [(fams[j], round(1 - float(freq[j]), 3)) for j in np.argsort(freq) if start_v[j] and freq[j] < 0.5][:40]
    gained = [(fams[j], round(float(freq[j]), 3)) for j in np.argsort(-freq) if not start_v[j] and freq[j] >= 0.5][:40]
    res = {"start": start_label, "start_size": len(start),
           "schedule": [{"environments": sorted(e) or ["none"], "time": t} for e, t in schedule],
           "time_unit": f"tree branch length; root-to-tip of the eukaryote tree is about {sim.tree_depth:.2f}",
           "reps": reps, "size_median": int(np.median(sizes)), "size_range_90": [int(np.percentile(sizes, 5)),
                                                                                 int(np.percentile(sizes, 95))],
           "lost_in_most_runs": lost, "gained_in_most_runs": gained,
           "warnings": [FAILED_LAWS[e] for e in laws if e in FAILED_LAWS]
           + ["what our laws imply at the gene-family level; not a forecast of a real organism; no sequences"]}
    (OUT / "runs").mkdir(parents=True, exist_ok=True)
    (OUT / "runs" / f"{name}.json").write_text(json.dumps(res, ensure_ascii=False, indent=1))
    print(json.dumps({k: v for k, v in res.items() if k not in ("lost_in_most_runs", "gained_in_most_runs")},
                     ensure_ascii=False, indent=1))
    return res


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("step", choices=["bank", "replay", "run"])
    ap.add_argument("--start", default="leca")
    ap.add_argument("--schedule", default="none:0.3")
    ap.add_argument("--reps", type=int, default=200)
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--name", default="run")
    ap.add_argument("--envs", default="", help="replay only these environments (comma-separated)")
    ap.add_argument("--out", default="replay.json")
    a = ap.parse_args()
    if a.step == "bank":
        build_bank()
    elif a.step == "replay":
        replay(a.reps, a.envs.split(",") if a.envs else None, a.out)
    else:
        run(a.start, a.schedule, a.reps, a.seed, a.name)


if __name__ == "__main__":
    main()
