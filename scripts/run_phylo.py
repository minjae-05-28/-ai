"""Re-test species-level laws with phylogenetic correction (taxonomy rank GLS).

    python scripts/run_phylo.py

For each law: ordinary least squares (species independent) vs rank GLS (one variance
component per taxonomic rank, results/taxonomy/taxonomy.json). A law that survives keeps
its sign and stays significant; 'shared_history' is the share of residual variance that
the taxonomy explains.
"""

import json
from pathlib import Path

import numpy as np

from organelle_evo.eukaryotes import catalog as euk
from organelle_evo.eukaryotes.model import counts, family_features
from organelle_evo.laws import LAWS_DIR, save_law
from organelle_evo.phylo import pgls, rank_gls, taxonomy_cov, tree_cov
from organelle_evo.prokaryotes import catalog as pro

TAX = json.loads(Path("results/taxonomy/taxonomy.json").read_text())
C = Path("data/composition")
TREES = {f.stem: f.read_text() for f in Path("results/phylo_tree").glob("*.nwk") if not f.stem.endswith(".boot")}
BOOTS = {f.name.split(".")[0]: [t for t in f.read_text().splitlines() if t.strip()]
         for f in Path("results/phylo_tree").glob("*.boot.nwk")}


def load(sub):
    return {json.loads(f.read_text())["species"]: json.loads(f.read_text()) for f in (C / sub).glob("**/*.json")}


def test(name, names, X, y, col=1, tree=None):
    X = np.c_[np.ones(len(y)), X]
    keep = [i for i, n in enumerate(names) if n in TAX]
    names, X, y = [names[i] for i in keep], X[keep], y[keep]
    ols = pgls(X, y, taxonomy_cov(names, TAX), lam=0.0)
    lam = pgls(X, y, taxonomy_cov(names, TAX))
    rg = rank_gls(X, y, names, TAX)
    row = {"n": len(y), "ols": [float(ols.coef[col]), float(ols.p[col])],
           "pgls_lambda": [float(lam.coef[col]), float(lam.p[col]), lam.lam],
           "rank_gls": [float(rg.coef[col]), float(rg.p[col])], "shared_history": rg.shares["shared_history"]}
    row["survives"] = bool(np.sign(rg.coef[col]) == np.sign(ols.coef[col]) and rg.p[col] < 0.05)
    if tree in TREES:
        keep, V = tree_cov(names, TREES[tree])
        ix = [names.index(k) for k in keep]
        tp = pgls(X[ix], y[ix], V)
        row["tree_pgls"] = [float(tp.coef[col]), float(tp.p[col]), tp.lam, len(keep)]
        row["survives_tree"] = bool(np.sign(tp.coef[col]) == np.sign(ols.coef[col]) and tp.p[col] < 0.05)
        if tree in BOOTS:
            reps = []
            for t in BOOTS[tree]:
                k2, V2 = tree_cov(names, t)
                ix2 = [names.index(k) for k in k2]
                r2 = pgls(X[ix2], y[ix2], V2)
                reps.append((float(r2.p[col]), bool(np.sign(r2.coef[col]) == np.sign(ols.coef[col]) and r2.p[col] < 0.05)))
            row["bootstrap_trees"] = {"n": len(reps), "share_surviving": float(np.mean([r[1] for r in reps])),
                                      "median_p": float(np.median([r[0] for r in reps])),
                                      "max_p": float(max(r[0] for r in reps))}
            print(f"{'':42s} bootstrap trees: survives in {row['bootstrap_trees']['share_surviving']:.0%} "
                  f"of {len(reps)} (median p {row['bootstrap_trees']['median_p']:.1e})")
        print(f"{'':42s} tree PGLS {tp.coef[col]:+.4g} (p {tp.p[col]:.1e}, lambda {tp.lam:.2f}, n={len(keep)})  "
              f"{'survives' if row['survives_tree'] else 'DOES NOT SURVIVE'}")
    print(f"{name:42s} n={len(y):3d}  OLS {ols.coef[col]:+.4g} (p {ols.p[col]:.1e})  "
          f"rank GLS {rg.coef[col]:+.4g} (p {rg.p[col]:.1e}, history {rg.shares['shared_history']:.0%})  "
          f"{'survives' if row['survives'] else 'DOES NOT SURVIVE'}")
    return row


def main():
    res = {}
    P = {s: d for s, d in load("prokaryotes").items() if s in pro.SPECIES}
    sp = sorted(P)
    E = lambda k: np.array([P[s][k] for s in sp])  # noqa: E731
    env = lambda k: np.array([getattr(pro.SPECIES[s], k) for s in sp], dtype=float)  # noqa: E731
    res["ivywrel_vs_temperature"] = test("IVYWREL ~ optimal temperature", sp, env("temp"), E("ivywrel"), tree="prokaryotes")
    res["cvp_vs_temperature"] = test("charged-vs-polar ~ optimal temperature", sp, env("temp"), E("cvp"), tree="prokaryotes")
    res["acidic_vs_salt"] = test("acidic excess ~ optimal NaCl", sp, env("nacl"), E("acidic_excess"), tree="prokaryotes")
    res["nitrogen_vs_oligotrophy"] = test("side-chain N ~ oligotroph", sp, env("oligo"), E("n_side"), tree="prokaryotes")
    res["fymink_vs_anoxia"] = test("FYMINK ~ anaerobe", sp, 1 - env("aerobic"), E("fymink"), tree="prokaryotes")

    # van Nimwegen scaling: transcription regulators vs genome size
    ann = json.loads(Path("data/eukaryotes/family_annotations.json").read_text())
    slim = {v["name"]: k for k, v in ann["slims"].items()}
    tf_ids = {slim["regulation of DNA-templated transcription"], slim["transcription regulator activity"]}
    tf = {f for f, a in ann["families"].items() if tf_ids & set(a.get("go_slim", ()))}
    prof = {json.loads(f.read_text())["species"]: json.loads(f.read_text()) for f in Path("data/prokaryotes").glob("*.json")}
    ps = sorted(s for s in prof if s in pro.SPECIES)
    N = np.log([prof[s]["n_genes"] for s in ps])
    T = np.log([max(sum(v[0] for f, v in prof[s]["families"].items() if f in tf), 1) for s in ps])
    res["regulator_scaling"] = test("log regulators ~ log genes (exponent)", ps, N, T, tree="prokaryotes")

    # Endosymbiont AT bias
    S = load("endosymbiosis/insect_endosymbiont")
    ss = sorted(S)
    res["symbiont_fymink_vs_size"] = test("FYMINK ~ log proteome size (symbionts)", ss,
                                          np.log([S[s]["n_proteins"] for s in ss]), np.array([S[s]["fymink"] for s in ss]), tree="symbionts")

    # Eukaryote severity (pairs, named by descendant)
    profs = {}
    for f in Path("data/eukaryotes").glob("*.json"):
        if f.name not in ("pfam_meta.json", "family_annotations.json"):
            d = json.loads(f.read_text())
            profs[d["species"]] = d
    meta = json.loads(Path("data/eukaryotes/pfam_meta.json").read_text())
    fams, _ = family_features(list(profs.values()), meta)
    c = {s: counts(p, fams) for s, p in profs.items()}
    pairs = euk.resolve_pairs(profs)
    sev = np.array([np.mean(c[d][c[a] > 0] == 0) for a, d in pairs])
    y = np.log(sev / (1 - sev))
    Z = np.array([euk.design(d)[1:] for _, d in pairs])
    names = [d for _, d in pairs]
    for j, ax in enumerate(euk.AXES):
        res[f"severity_{ax}"] = test(f"share lost ~ axes [{ax}]", names, Z, y, col=1 + j, tree="eukaryotes")

    # Environment -> sequence change (pairs, named by descendant)
    pp = pro.resolve_pairs(P)
    Zp = np.array([pro.design(a, d)[1:] for a, d in pp])
    dn = [d for _, d in pp]
    for k, axis in (("ivywrel", 0), ("cvp", 0), ("acidic_excess", 1), ("fymink", 2)):
        dy = np.array([P[d][k] - P[a][k] for a, d in pp])
        res[f"pair_{k}_{pro.AXES[axis]}"] = test(f"change in {k} ~ env [{pro.AXES[axis]}]", dn, Zp, dy, col=1 + axis, tree="prokaryotes")

    out = Path("results/phylo")
    out.mkdir(parents=True, exist_ok=True)
    (out / "metrics.json").write_text(json.dumps(res, indent=2))
    save_law(LAWS_DIR / "phylo_check_v1.json", id="phylo_check_v1",
             scope="Which species-level laws survive phylogenetic correction (taxonomy rank GLS).",
             model="OLS vs PGLS (Pagel's lambda) vs rank GLS on NCBI taxonomy.", feature_names=[],
             data={"taxa": len(TAX)}, validation=res, contexts={},
             caveats=["Taxonomy is a coarse stand-in for a sequence-based phylogeny."])
    print(f"{sum(r['survives'] for r in res.values())}/{len(res)} survive rank GLS")
    if TREES:
        t = [r for r in res.values() if "survives_tree" in r]
        print(f"{sum(r['survives_tree'] for r in t)}/{len(t)} survive tree PGLS -> {out}/")


if __name__ == "__main__":
    main()
