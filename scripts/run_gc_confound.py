"""GC confound check: do the sequence laws survive genome GC content as a covariate?

    python scripts/run_gc_confound.py

Amino-acid composition follows genome GC: GC-rich codons encode G, A, R, P (GARP) and
AT-rich codons F, Y, M, I, N, K (FYMINK). A composition law could therefore be mutation
bias rather than adaptation. Each law is refitted with GC (results/gc/gc.json) added:

  species laws   statistic ~ environment (+ GC), OLS and rank GLS on the NCBI taxonomy
  pair laws      change in statistic ~ environment change (+ change in GC); coefficient,
                 rank GLS p and leave-one-pair-out R^2
  symbionts      FYMINK / median pI ~ log proteome size (+ GC): is the AT bias the mechanism?

A law survives if its environment coefficient keeps its sign and stays significant
(rank GLS p < 0.05) with GC in the model.
"""

import json
from pathlib import Path

import numpy as np

from organelle_evo.laws import LAWS_DIR, save_law
from organelle_evo.phylo import pgls, rank_gls, taxonomy_cov, tree_cov
from organelle_evo.prokaryotes import catalog as pro

TAX = json.loads(Path("results/taxonomy/taxonomy.json").read_text())
GC = json.loads(Path("results/gc/gc.json").read_text())
C = Path("data/composition")
TREES = {f.stem: f.read_text() for f in Path("results/phylo_tree").glob("*.nwk")}


def load(sub):
    return {json.loads(f.read_text())["species"]: json.loads(f.read_text()) for f in (C / sub).glob("*.json")}


def fit(names, X, y):
    X = np.c_[np.ones(len(y)), X]
    keep = [i for i, n in enumerate(names) if n in TAX]
    names, X, y = [names[i] for i in keep], X[keep], y[keep]
    ols = pgls(X, y, taxonomy_cov(names, TAX), lam=0.0)
    rg = rank_gls(X, y, names, TAX)
    return ols, rg, len(y)


def loo_r2(X, y):
    X = np.c_[np.ones(len(y)), X]
    pred = np.empty(len(y))
    for i in range(len(y)):
        m = np.arange(len(y)) != i
        pred[i] = X[i] @ np.linalg.lstsq(X[m], y[m], rcond=None)[0]
    return float(1 - ((y - pred) ** 2).sum() / ((y - y.mean()) ** 2).sum())


def compare(name, names, env, gc, y, extra=None, tree=None):
    """Environment effect (column 1) without and with GC."""
    extra = np.zeros((len(y), 0)) if extra is None else extra
    o0, r0, n = fit(names, np.c_[env, extra], y)
    o1, r1, _ = fit(names, np.c_[env, extra, gc], y)
    gcol = 1 + 1 + extra.shape[1]
    row = {"n": n, "without_gc": {"coef": float(r0.coef[1]), "p_ols": float(o0.p[1]), "p_rank_gls": float(r0.p[1])},
           "with_gc": {"coef": float(r1.coef[1]), "p_ols": float(o1.p[1]), "p_rank_gls": float(r1.p[1]),
                       "gc_coef": float(r1.coef[gcol]), "gc_p_rank_gls": float(r1.p[gcol])},
           "corr_env_gc": float(np.corrcoef(env, gc)[0, 1])}
    row["retained_share_of_effect"] = row["with_gc"]["coef"] / row["without_gc"]["coef"]
    row["survives"] = bool(np.sign(r1.coef[1]) == np.sign(r0.coef[1]) and r1.p[1] < 0.05)
    if tree in TREES:
        keep, V = tree_cov(names, TREES[tree])
        ix = [names.index(k) for k in keep]
        X1 = np.c_[np.ones(len(y)), env, extra, gc][ix]
        tp = pgls(X1, y[ix], V)
        row["with_gc"]["tree_pgls"] = [float(tp.coef[1]), float(tp.p[1]), tp.lam, len(keep)]
        row["survives_tree"] = bool(np.sign(tp.coef[1]) == np.sign(r0.coef[1]) and tp.p[1] < 0.05)
    print(f"{name:40s} n={n:3d} r(env,GC) {row['corr_env_gc']:+.2f} | env {r0.coef[1]:+.4g} (p {r0.p[1]:.1e}) -> "
          f"{r1.coef[1]:+.4g} (p {r1.p[1]:.1e}), {row['retained_share_of_effect']:.0%} kept | GC p {r1.p[gcol]:.1e}  "
          f"{'survives' if row['survives'] else 'DOES NOT SURVIVE'}")
    return row


def main():
    res = {"species": {}, "pairs": {}, "symbionts": {}}
    gpro = {s: v["gc"] for s, v in GC["prokaryotes"].items() if v["gc"] is not None}
    P = {s: d for s, d in load("prokaryotes").items() if s in pro.SPECIES and s in gpro}
    sp = sorted(P)
    E = lambda k: np.array([P[s][k] for s in sp])  # noqa: E731
    env = lambda k: np.array([getattr(pro.SPECIES[s], k) for s in sp], dtype=float)  # noqa: E731
    g = np.array([gpro[s] for s in sp])
    print(f"species laws ({len(sp)} bacteria and archaea with GC)")
    S = res["species"]
    S["ivywrel_vs_temperature"] = compare("IVYWREL ~ optimal temperature", sp, env("temp"), g, E("ivywrel"), tree="prokaryotes")
    S["cvp_vs_temperature"] = compare("charged-vs-polar ~ optimal temperature", sp, env("temp"), g, E("cvp"), tree="prokaryotes")
    S["acidic_vs_salt"] = compare("acidic excess ~ optimal NaCl", sp, env("nacl"), g, E("acidic_excess"), tree="prokaryotes")
    S["nitrogen_vs_oligotrophy"] = compare("side-chain N ~ oligotroph", sp, env("oligo"), g, E("n_side"), tree="prokaryotes")
    S["fymink_vs_anoxia"] = compare("FYMINK ~ anaerobe", sp, 1 - env("aerobic"), g, E("fymink"), tree="prokaryotes")
    S["gc_explains"] = {k: float(np.corrcoef(g, E(k))[0, 1]) for k in ("fymink", "garp", "ivywrel", "cvp", "acidic_excess", "n_side")}
    print("   r(GC, statistic): " + ", ".join(f"{k} {v:+.2f}" for k, v in S["gc_explains"].items()))

    print("\npair laws (change in statistic ~ environment change + change in GC)")
    pp = [(a, d) for a, d in pro.resolve_pairs(P)]
    Z = np.array([pro.design(a, d)[1:] for a, d in pp])
    dn = [d for _, d in pp]
    dg = np.array([gpro[d] - gpro[a] for a, d in pp])
    for k, axis in (("ivywrel", 0), ("cvp", 0), ("acidic_excess", 1), ("n_side", 4), ("fymink", 2)):
        dy = np.array([P[d][k] - P[a][k] for a, d in pp])
        others = np.delete(Z, axis, axis=1)
        row = compare(f"change in {k} ~ {pro.AXES[axis]}", dn, Z[:, axis], dg, dy, extra=others, tree="prokaryotes")
        row["loo_r2_env"] = loo_r2(Z, dy)
        row["loo_r2_env_gc"] = loo_r2(np.c_[Z, dg], dy)
        row["loo_r2_gc_only"] = loo_r2(dg[:, None], dy)
        print(f"   LOO R^2: environment {row['loo_r2_env']:.2f}, environment + dGC {row['loo_r2_env_gc']:.2f}, dGC alone {row['loo_r2_gc_only']:.2f}")
        res["pairs"][f"{k}_{pro.AXES[axis]}"] = row

    print("\nsymbiont AT bias")
    gs = {s: v["gc"] for s, v in GC["endosymbiosis/insect_endosymbiont"].items() if v["gc"] is not None}
    Sy = {s: d for s, d in load("endosymbiosis/insect_endosymbiont").items() if s in gs}
    ss = sorted(Sy)
    size = np.log([Sy[s]["n_proteins"] for s in ss])
    gg = np.array([gs[s] for s in ss])
    for k in ("fymink", "median_pi"):
        y = np.array([Sy[s][k] for s in ss])
        row = compare(f"{k} ~ log proteome size", ss, size, gg, y, tree="symbionts")
        row["r_gc"] = float(np.corrcoef(gg, y)[0, 1])
        row["r_size_gc"] = float(np.corrcoef(size, gg)[0, 1])
        res["symbionts"][k] = row
    print(f"   r(GC, FYMINK) {res['symbionts']['fymink']['r_gc']:+.2f}; r(size, GC) {res['symbionts']['fymink']['r_size_gc']:+.2f}")

    adaptive = {**{f"species:{k}": v for k, v in S.items() if k != "gc_explains"}, **{f"pair:{k}": v for k, v in res["pairs"].items()}}
    res["summary"] = {"adaptive_laws_tested": len(adaptive), "survive": sorted(k for k, v in adaptive.items() if v["survives"]),
                      "do_not_survive": sorted(k for k, v in adaptive.items() if not v["survives"])}
    print(f"\n{len(res['summary']['survive'])}/{len(adaptive)} environment laws survive GC; "
          f"not: {res['summary']['do_not_survive']}")
    out = Path("results/gc_confound")
    out.mkdir(parents=True, exist_ok=True)
    (out / "metrics.json").write_text(json.dumps(res, indent=2))
    save_law(LAWS_DIR / "gc_confound_v1.json", id="gc_confound_v1",
             scope="Whether the proteome-composition laws (temperature, salt, oxygen, nutrients, symbiont AT bias) survive genome GC content as a covariate.",
             model="Environment effect with and without GC (or change in GC) as a covariate; OLS and taxonomy rank GLS; leave-one-pair-out R^2.",
             feature_names=[], data={"prokaryotes": len(sp), "pairs": len(pp), "insect_endosymbionts": len(ss)},
             validation=res, contexts={},
             caveats=["Genome GC from NCBI assembly stats (organelles and symbionts counted from GenBank records).",
                      "GC is itself shaped by environment and lifestyle, so adding it can remove real effects (over-adjustment).",
                      "Taxonomy is a coarse stand-in for a sequence-based phylogeny."])
    print(f"Done -> {out}/ and laws/gc_confound_v1.json")


if __name__ == "__main__":
    main()
