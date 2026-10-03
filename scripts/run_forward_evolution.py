"""Forward evolution: evolve an ancestor with the law alone and compare it to the real modern descendant.

    python scripts/run_forward_evolution.py --system parasites     [--epochs 300] [--reps 200]
    python scripts/run_forward_evolution.py --system extremophiles

The usual validation hands the law the true number of lost families and only scores the
ranking. Here the law gets nothing from the held-out lineage:
  - no memorisation: every pair of the held-out lineage (eukaryote clade, or prokaryote
    proxy group) is removed from training, so the law knows which *kinds* of families tend to
    go, never which families went in this lineage;
  - no amount: the pair intercepts (how much is lost, duplicated, gained) are predicted from
    the lineage's lifestyle/environment design by least squares on the training pairs, as in
    the Mars forecast of run_environment.py.
The ancestor (extant proxy) is then evolved forward by sampling each family's loss, and gains
from the pool of families seen in training species, `reps` times.

Compared with the real descendant, side by side:
    no_change            the ancestor unchanged
    random_same_amount   the law's number of losses/gains, families picked at random
                         (law - this = what the law knows about WHICH families)
    random_true_amount   the true number of losses, picked at random
    no_axes_law          same law without lifestyle/environment axes
    mean_share           (amount only) the mean share lost in the training pairs
    memorisation         reference only, not part of the law: each family's loss frequency in
                         the training pairs, scaled to the law's amount
Intervals: bootstrap over lineages. Random examples are drawn with a fixed seed.
"""

import argparse
import json
from pathlib import Path

import numpy as np
import torch

from organelle_evo.eukaryotes.features import enriched_features
from organelle_evo.eukaryotes.model import counts, family_features, fit_bd, loss_probability
from organelle_evo.predict import auroc

ANN = Path("data/eukaryotes")
METHODS = ("law", "law_losses_only", "no_axes_law", "random_same_amount", "random_true_amount", "no_change", "memorisation")


def load_system(system, ancestor="proxy"):
    meta = json.loads((ANN / "pfam_meta.json").read_text())
    ann = json.loads((ANN / "family_annotations.json").read_text())
    if system == "parasites":
        from organelle_evo.eukaryotes.catalog import AXES, CO_PROXIES, SPECIES, design, resolve_pairs
        data_dir = ANN
        labels = ("base", *AXES)
        unit = lambda a, d: SPECIES[d].group.split("_")[0]  # noqa: E731  (clade, as run_transfer.py)
        dsg = lambda a, d: design(d)  # noqa: E731
        evaluate = lambda z: z[1] > 0  # noqa: E731  parasites only
    else:
        from organelle_evo.prokaryotes.catalog import AXES, CO_PROXIES, design, resolve_pairs
        data_dir = Path("data/prokaryotes")
        labels = ("base", *AXES)
        unit = lambda a, d: a  # noqa: E731  pairs sharing a proxy are held out together
        dsg = design
        evaluate = lambda z: max(abs(v) for v in z[1:]) >= 0.25  # noqa: E731  controls carry no change
    profiles = {}
    for f in data_dir.glob("*.json"):
        d = json.loads(f.read_text())
        if "families" in d and d.get("species"):
            profiles[d["species"]] = d
    pairs = resolve_pairs(profiles)
    fams, _ = family_features(list(profiles.values()), meta)
    c = {s: counts(p, fams) for s, p in profiles.items()}
    # Ubiquity from ancestor proxies only, so a descendant never informs its own features.
    proxies = sorted({a for a, _ in pairs})
    fams, names, x = enriched_features(profiles, meta, ann, c, free=proxies)
    # Ancestor counts. "consensus": a family counts as ancestral only if the proxy shares it
    # with at least one close free-living relative (CO_PROXIES), so the proxy's own gains are
    # not scored as the descendant's losses. Proxies without a profiled relative keep their counts.
    anc, removed = {}, {}
    for a in proxies:
        co = [s for s in CO_PROXIES.get(a, ()) if s in c] if ancestor == "consensus" else []
        if co:
            shared = np.any([c[s] > 0 for s in co], axis=0)
            anc[a] = np.where(shared, c[a], 0)
            removed[a] = int(((c[a] > 0) & ~shared).sum())
        else:
            anc[a] = c[a]
    if ancestor == "consensus":
        print(f"consensus ancestor: {len(removed)}/{len(proxies)} proxies have a relative; families dropped "
              + ", ".join(f"{k} {v}" for k, v in removed.items()))
    return dict(fams=fams, names=names, x=x, c=c, anc=anc, pairs=pairs, labels=labels, unit=unit, design=dsg,
                evaluate=evaluate, meta=meta)


def intercepts_from_design(law, train_designs, z):
    Z = np.asarray(train_designs, dtype=float)
    keep = np.abs(Z).sum(0) > 0
    out = {}
    for k in ("lam", "mu", "nu"):
        coef = np.linalg.lstsq(Z[:, keep], getattr(law, f"a_{k}"), rcond=None)[0]
        out[k] = float(np.asarray(z, dtype=float)[keep] @ coef)
    return out


def jaccard(a, b):
    u = np.logical_or(a, b).sum()
    return float(np.logical_and(a, b).sum() / u) if u else 1.0


def simulate(p_loss, p_gain, had, pool, rng, reps):
    """Presence vectors sampled from per-family loss and gain probabilities."""
    out = np.zeros((reps, len(had)), dtype=bool)
    for r in range(reps):
        keep = had & (rng.random(len(had)) >= p_loss)
        gain = pool & (rng.random(len(had)) < p_gain)
        out[r] = keep | gain
    return out


def random_with_amount(n_lost, n_gain, had, pool, rng):
    pres = had.copy()
    idx = np.flatnonzero(had)
    pres[rng.choice(idx, min(int(n_lost), len(idx)), replace=False)] = False
    cand = np.flatnonzero(pool)
    if len(cand) and n_gain:
        pres[rng.choice(cand, min(int(n_gain), len(cand)), replace=False)] = True
    return pres


def score(sim, real, had):
    """Mean over replicates: Jaccard with the real genome, share lost, precision of losses."""
    real_lost = had & ~real
    jac, jac_anc, share, prec, acc = [], [], [], [], []
    for s in np.atleast_2d(sim):
        lost = had & ~s
        jac.append(jaccard(s, real))
        jac_anc.append(jaccard(s[had], real[had]))
        acc.append(float((s[had] == real[had]).mean()))
        share.append(lost.sum() / had.sum())
        prec.append((lost & real_lost).sum() / lost.sum() if lost.sum() else np.nan)
    return {"jaccard": float(np.mean(jac)), "jaccard_ancestral": float(np.mean(jac_anc)),
            "fate_accuracy": float(np.mean(acc)), "share_lost": float(np.mean(share)),
            "loss_precision": float(np.nanmean(prec)) if not np.all(np.isnan(prec)) else float("nan")}


def boot(rows, f, n=2000, seed=0):
    rng = np.random.default_rng(seed)
    by = {}
    for r in rows:
        by.setdefault(r["unit"], []).append(f(r))
    units = list(by)
    vals = [v for vs in by.values() for v in vs]
    stats = [np.mean([v for i in rng.choice(len(units), len(units)) for v in by[units[i]]]) for _ in range(n)]
    return {"mean": round(float(np.mean(vals)), 4),
            "ci95": [round(float(np.percentile(stats, 2.5)), 4), round(float(np.percentile(stats, 97.5)), 4)]}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--system", choices=("parasites", "extremophiles"), required=True)
    ap.add_argument("--epochs", type=int, default=300)
    ap.add_argument("--reps", type=int, default=200)
    ap.add_argument("--examples", type=int, default=6)
    ap.add_argument("--threads", type=int, default=4)
    ap.add_argument("--max-units", type=int, default=0, help="only the first N held-out lineages (testing)")
    ap.add_argument("--out", default="results/forward_evolution")
    ap.add_argument("--ancestor", choices=("proxy", "consensus"), default="proxy")
    args = ap.parse_args()
    torch.set_num_threads(args.threads)
    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    S = load_system(args.system, args.ancestor)
    anc = S["anc"]
    tag = args.system + ("_consensus" if args.ancestor == "consensus" else "")
    fams, names, x, c, pairs, labels = S["fams"], S["names"], S["x"], S["c"], S["pairs"], S["labels"]
    designs = [S["design"](a, d) for a, d in pairs]
    units = [S["unit"](a, d) for a, d in pairs]
    test_units = list(dict.fromkeys(u for u, z in zip(units, designs) if S["evaluate"](z)))
    if args.max_units:
        test_units = test_units[: args.max_units]
    print(f"{args.system}: {len(pairs)} pairs, {len(fams)} families, {len(test_units)} held-out lineages")
    rng = np.random.default_rng(0)
    rows = []
    saved = {}  # per pair: ancestral family indices and each method's per-family loss score
    for u in test_units:
        tr = [i for i in range(len(pairs)) if units[i] != u]
        train = [(anc[pairs[i][0]], c[pairs[i][1]], designs[i]) for i in tr]
        law = fit_bd(x, train, labels, epochs=args.epochs)
        base = fit_bd(x, [(n, m, (1.0,)) for n, m, _ in train], ("base",), epochs=args.epochs)
        train_species = {s for i in tr for s in pairs[i]}
        pool = np.array([sum(c[s][j] > 0 for s in train_species) >= 2 for j in range(len(fams))])
        mean_share = float(np.mean([(m[n > 0] == 0).mean() for n, m, _ in train]))
        for i in range(len(pairs)):
            if units[i] != u or not S["evaluate"](designs[i]):
                continue
            (a, d), z = pairs[i], designs[i]
            n, m = anc[a], c[d]
            had, real = n > 0, m > 0
            pool_i = pool & ~had
            res = {}
            for name, fit, zz, icpt in (
                ("law", law, z, intercepts_from_design(law, [t[2] for t in train], z)),
                ("no_axes_law", base, (1.0,), {k: float(np.mean(getattr(base, f"a_{k}"))) for k in ("lam", "mu", "nu")}),
            ):
                wl, wm, wn = fit.weights(zz)
                p_loss = np.zeros(len(fams))
                p_loss[had] = loss_probability(n[had], x[had], wl, wm, icpt["lam"], icpt["mu"])
                p_gain = 1 - np.exp(-np.exp(icpt["nu"] + x @ wn))
                sim = simulate(p_loss, p_gain, had, pool_i, rng, args.reps)
                res[name] = {**score(sim, real, had), "loss_auroc": auroc(p_loss[had], ~real[had]),
                             "n_gained_sim": float(np.mean([(s & ~had).sum() for s in sim])),
                             "gain_precision": float(np.nanmean([((s & ~had) & real).sum() / max((s & ~had).sum(), 1)
                                                                 for s in sim]))}
                if name == "no_axes_law":
                    noaxes_ploss = p_loss
                if name == "law":
                    law_sim, law_ploss = sim, p_loss
                    res["law_losses_only"] = score(simulate(p_loss, p_gain, had, pool_i & False, rng, args.reps),
                                                   real, had)
            n_lost_law = [int((had & ~s).sum()) for s in law_sim]
            n_gain_law = [int((s & ~had).sum()) for s in law_sim]
            true_lost, true_gain = int((had & ~real).sum()), int((real & pool_i).sum())
            res["random_same_amount"] = score(np.array([random_with_amount(nl, ng, had, pool_i, rng)
                                                        for nl, ng in zip(n_lost_law, n_gain_law)]), real, had)
            res["random_true_amount"] = score(np.array([random_with_amount(true_lost, true_gain, had, pool_i, rng)
                                                        for _ in range(args.reps)]), real, had)
            res["no_change"] = score(had[None, :], real, had)
            # Reference only: memorisation, scaled to the law's own amount.
            idx = np.flatnonzero(had)
            freq = np.array([np.mean([tm[j] == 0 for tn, tm, _ in train if tn[j] > 0])
                             if any(tn[j] > 0 for tn, _, _ in train) else 0.5 for j in idx])
            target = float(np.mean(n_lost_law))
            scale = target / max(freq.sum(), 1e-9)
            p_mem = np.zeros(len(fams))
            p_mem[idx] = np.clip(freq * scale, 0, 1)
            res["memorisation"] = {**score(simulate(p_mem, np.zeros(len(fams)), had, pool_i & False, rng, args.reps),
                                            real, had), "loss_auroc": auroc(freq, ~real[had])}
            real_share = true_lost / had.sum()
            row = {"unit": u, "pair": f"{a} -> {d}", "design": list(map(float, z)),
                   "real_share_lost": round(float(real_share), 4), "mean_share_baseline": round(mean_share, 4),
                   "n_ancestral": int(had.sum()), "real_gained_from_pool": true_gain,
                   **{f"{k}.{mk}": round(v, 4) for k, r in res.items() for mk, v in r.items()}}
            saved[f"{a} -> {d}"] = {
                "fam_idx": np.flatnonzero(had), "real_lost": ~real[had],
                "law": law_ploss[had], "no_axes_law": noaxes_ploss[had], "memorisation": freq,
                "copies": n[had].astype(float),
            }
            row["law_lost_examples"] = {
                "predicted_and_lost": [fams[j] for j in np.argsort(-law_ploss) if had[j] and not real[j]][:8],
                "predicted_but_kept": [fams[j] for j in np.argsort(-law_ploss) if had[j] and real[j]][:8],
            }
            rows.append(row)
            print(f"  [{u}] {d:32s} share lost real {real_share:.2f} law {res['law']['share_lost']:.2f} "
                  f"(mean {mean_share:.2f}) | Jaccard law {res['law']['jaccard']:.3f} "
                  f"random {res['random_same_amount']['jaccard']:.3f} no-axes {res['no_axes_law']['jaccard']:.3f} "
                  f"losses-only {res['law_losses_only']['jaccard']:.3f} unchanged {res['no_change']['jaccard']:.3f} memo(ref) {res['memorisation']['jaccard']:.3f}",
                  flush=True)

    summary = {"n_pairs": len(rows), "n_lineages": len({r["unit"] for r in rows})}
    for k in METHODS:
        for mk in ("fate_accuracy", "jaccard", "jaccard_ancestral", "loss_precision", "share_lost", "loss_auroc"):
            key = f"{k}.{mk}"
            if key in rows[0]:
                summary[key] = boot(rows, lambda r, key=key: r[key])
    summary["amount_error.law"] = boot(rows, lambda r: abs(r["law.share_lost"] - r["real_share_lost"]))
    summary["amount_error.no_axes_law"] = boot(rows, lambda r: abs(r["no_axes_law.share_lost"] - r["real_share_lost"]))
    summary["amount_error.mean_share"] = boot(rows, lambda r: abs(r["mean_share_baseline"] - r["real_share_lost"]))
    for other in ("random_same_amount", "no_axes_law", "no_change", "memorisation"):
        summary[f"jaccard.law - {other}"] = boot(rows, lambda r, o=other: r["law.jaccard"] - r[f"{o}.jaccard"])
        summary[f"jaccard_ancestral.law - {other}"] = boot(
            rows, lambda r, o=other: r["law.jaccard_ancestral"] - r[f"{o}.jaccard_ancestral"])
    for other in ("random_same_amount", "random_true_amount", "no_axes_law", "no_change", "memorisation"):
        summary[f"fate_accuracy.law - {other}"] = boot(
            rows, lambda r, o=other: r["law.fate_accuracy"] - r[f"{o}.fate_accuracy"])
    summary["jaccard.law_losses_only - no_change"] = boot(
        rows, lambda r: r["law_losses_only.jaccard"] - r["no_change.jaccard"])
    summary["loss_precision.law - random_same_amount"] = boot(
        rows, lambda r: r["law.loss_precision"] - r["random_same_amount.loss_precision"])
    summary["gain_precision.law"] = boot(rows, lambda r: r["law.gain_precision"])
    ex = np.random.default_rng(2026).choice(len(rows), min(args.examples, len(rows)), replace=False)
    summary["random_examples"] = [rows[i]["pair"] for i in ex]

    print("\nsummary (mean [95% CI over lineages])")
    for k, v in summary.items():
        if isinstance(v, dict):
            print(f"  {k:45s} {v['mean']:+.4f} {v['ci95']}")
    (out / f"{tag}.json").write_text(json.dumps({"summary": summary, "pairs": rows}, indent=1))
    np.savez_compressed(out / f"{tag}_scores.npz", fams=np.array(fams), pairs=np.array(list(saved)),
                        units=np.array([r["unit"] for r in rows]),
                        **{f"{i}|{k}": v for i, rec in enumerate(saved.values()) for k, v in rec.items()})
    print(f"Done -> {out}/{tag}.json")


if __name__ == "__main__":
    main()
