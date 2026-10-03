"""Genome-level laws at scale: GTDB species representatives x the bacterial/archaeal trait table.

    python scripts/run_genome_laws.py [--law-id genome_traits_v1]

Targets (from data/traits, Madin et al. 2020):
    temperature   growth temperature, deg C (regression)
    oxygen        aerobe (aerobic, obligate aerobic) vs anaerobe (anaerobic, obligate anaerobic)
    host          host-associated isolation source vs environmental (soil, water, sediment, rock,
                  compost, hot spring, hypersaline...); food, wastewater, built environment excluded
Features (from data/gtdb, one quality-filtered genome per NCBI species): GC, log genome size,
coding density, proteins per Mb. (Protein count itself is nearly collinear with genome size and
made the coefficients cancel; per-Mb density keeps the information without the collinearity.)

Compared side by side under two schemes:
    random 5-fold          relatives of every test species are in training
    leave-order-out        whole GTDB orders held out: a lineage never seen
Methods:
    mean                   training mean (or base rate)
    taxonomy               memorisation: mean of the closest training taxon (genus > family >
                           order > class > phylum)
    law_linear             ridge / logistic regression on the 4 genome features (the law)
    law_nonlinear          gradient boosting on the same 4 features (no taxonomy)
    law+taxonomy           tool, not a law: taxonomy prediction corrected by the law's residual
Intervals for the leave-order-out differences: bootstrap over orders.
"""

import argparse
import csv
import gzip
import json
from collections import defaultdict
from pathlib import Path

import numpy as np
from sklearn.ensemble import HistGradientBoostingClassifier, HistGradientBoostingRegressor
from sklearn.linear_model import LogisticRegression, Ridge
from sklearn.metrics import mean_absolute_error, roc_auc_score
from sklearn.model_selection import GroupKFold, KFold
from sklearn.preprocessing import StandardScaler

from organelle_evo.laws import LAWS_DIR, save_law

RANKS = ("phylum", "class", "order", "family", "genus")
FEATURES = ("gc", "log10_genome_size", "coding_density", "proteins_per_mb")
ENVIRONMENTAL = ("soil", "water", "sediment", "rock", "compost", "sludge", "petroleum", "bioreactor")


def load(min_completeness=90.0, max_contamination=5.0):
    csv.field_size_limit(10**8)
    traits = {r["species_tax_id"]: r for r in csv.DictReader(gzip.open("data/traits/madin2020_condensed_species_NCBI.csv.gz", "rt"))}
    best = {}
    for r in csv.DictReader(gzip.open("data/gtdb/species_reps.tsv.gz", "rt"), delimiter="\t"):
        sp = r["ncbi_species_taxid"]
        if sp not in traits:
            continue
        try:
            comp, cont = float(r["checkm2_completeness"]), float(r["checkm2_contamination"])
            feats = [float(r["gc_percentage"]) / 100, np.log10(float(r["genome_size"])),
                     float(r["coding_density"]) / 100, float(r["protein_count"]) / float(r["genome_size"]) * 1e6]
        except (ValueError, TypeError):
            continue
        if comp < min_completeness or cont > max_contamination:
            continue
        score = comp - 5 * cont + (5 if r["ncbi_genome_category"] in ("none", "") else 0)  # prefer isolates
        if sp not in best or score > best[sp][0]:
            tax = dict(zip(("domain", *RANKS, "species"), [t.split("__", 1)[-1] for t in r["gtdb_taxonomy"].split(";")]))
            best[sp] = (score, {"taxid": sp, "accession": r["accession"], "domain": r["domain"], "x": feats,
                                **{k: tax.get(k, "") for k in RANKS}})
    rows = []
    for sp, (_, row) in best.items():
        t = traits[sp]
        temp = float(t["growth_tmp"]) if t["growth_tmp"] not in ("", "NA") else None
        met = t["metabolism"]
        oxy = 1 if met in ("aerobic", "obligate aerobic") else 0 if met in ("anaerobic", "obligate anaerobic") else None
        src = t["isolation_source"]
        host = 1 if src.startswith("host") else 0 if src.startswith(ENVIRONMENTAL) else None
        rows.append({**row, "temperature": temp, "oxygen": oxy, "host": host})
    return rows


def taxonomy_predict(train, test, y_train, base):
    """Mean of the closest training taxon, genus first."""
    means = {}
    for rank in RANKS:
        acc = defaultdict(list)
        for r, y in zip(train, y_train):
            if r[rank]:
                acc[r[rank]].append(y)
        means[rank] = {k: float(np.mean(v)) for k, v in acc.items()}
    out = []
    for r in test:
        for rank in reversed(RANKS):
            if r[rank] in means[rank]:
                out.append(means[rank][r[rank]])
                break
        else:
            out.append(base)
    return np.array(out)


def evaluate(rows, target, scheme, seed=0):
    data = [r for r in rows if r[target] is not None]
    X = np.array([r["x"] for r in data])
    y = np.array([r[target] for r in data], dtype=float)
    groups = np.array([r["order"] for r in data])
    reg = target == "temperature"
    splitter = GroupKFold(n_splits=10) if scheme == "leave_order_out" else KFold(5, shuffle=True, random_state=seed)
    pred = {k: np.zeros(len(y)) for k in ("mean", "taxonomy", "law_linear", "law_nonlinear", "law+taxonomy")}
    for tr, te in splitter.split(X, y, groups if scheme == "leave_order_out" else None):
        sc = StandardScaler().fit(X[tr])
        Xtr, Xte = sc.transform(X[tr]), sc.transform(X[te])
        base = float(y[tr].mean())
        pred["mean"][te] = base
        tax = taxonomy_predict([data[i] for i in tr], [data[i] for i in te], y[tr], base)
        pred["taxonomy"][te] = tax
        if reg:
            lin = Ridge(alpha=1.0).fit(Xtr, y[tr])
            gbm = HistGradientBoostingRegressor(max_iter=300, random_state=seed).fit(Xtr, y[tr])
            pred["law_linear"][te] = lin.predict(Xte)
            pred["law_nonlinear"][te] = gbm.predict(Xte)
            tax_tr = taxonomy_predict([data[i] for i in tr], [data[i] for i in tr], y[tr], base)  # in-sample, for the residual
            res = Ridge(alpha=1.0).fit(Xtr, y[tr] - tax_tr)
            pred["law+taxonomy"][te] = tax + res.predict(Xte)
        else:
            lin = LogisticRegression(max_iter=1000).fit(Xtr, y[tr])
            gbm = HistGradientBoostingClassifier(max_iter=300, random_state=seed).fit(Xtr, y[tr])
            pred["law_linear"][te] = lin.predict_proba(Xte)[:, 1]
            pred["law_nonlinear"][te] = gbm.predict_proba(Xte)[:, 1]
            logit = lambda p: np.log(np.clip(p, 1e-3, 1 - 1e-3) / (1 - np.clip(p, 1e-3, 1 - 1e-3)))  # noqa: E731
            pred["law+taxonomy"][te] = 1 / (1 + np.exp(-(logit(tax) + lin.decision_function(Xte) - lin.intercept_[0])))
    score = (lambda p: mean_absolute_error(y, p)) if reg else (lambda p: roc_auc_score(y, p))
    out = {"n": int(len(y)), "n_orders": int(len(set(groups))), "metric": "MAE (deg C)" if reg else "AUROC",
           "scores": {k: round(float(score(p)), 4) for k, p in pred.items()}}
    if not reg:
        # A constant prediction has AUROC 0.5 by definition; pooling per-fold base rates across folds
        # gives a spurious value (below 0.5 when held-out groups differ in base rate).
        out["scores"]["mean"] = 0.5
        out["note"] = "mean = 0.5 by definition (pooled per-fold constants are not a meaningful AUROC)"
    if reg:
        out["r2"] = {k: round(float(1 - ((y - p) ** 2).sum() / ((y - y.mean()) ** 2).sum()), 4) for k, p in pred.items()}
    if scheme == "leave_order_out":
        out["law_linear - taxonomy"] = boot_diff(y, pred["law_linear"], pred["taxonomy"], groups, reg)
        out["law_nonlinear - law_linear"] = boot_diff(y, pred["law_nonlinear"], pred["law_linear"], groups, reg)
        if reg:
            out["law_linear - mean"] = boot_diff(y, pred["law_linear"], pred["mean"], groups, reg)
    return out


def boot_diff(y, a, b, groups, reg, n=300, seed=0):
    """Score(a) - score(b) with a 95% interval from resampling orders. For MAE, negative = a better."""
    rng = np.random.default_rng(seed)
    units = np.unique(groups)
    idx = {u: np.flatnonzero(groups == u) for u in units}
    f = (lambda yy, p: mean_absolute_error(yy, p)) if reg else (lambda yy, p: roc_auc_score(yy, p) if len(set(yy)) > 1 else np.nan)
    stats = []
    for _ in range(n):
        sel = np.concatenate([idx[u] for u in rng.choice(units, len(units))])
        stats.append(f(y[sel], a[sel]) - f(y[sel], b[sel]))
    stats = np.array(stats)
    return {"mean": round(float(f(y, a) - f(y, b)), 4),
            "ci95": [round(float(np.nanpercentile(stats, 2.5)), 4), round(float(np.nanpercentile(stats, 97.5)), 4)]}


def coefficients(rows, target):
    """Standardized law coefficients, overall and within phyla (phylum fixed effects)."""
    data = [r for r in rows if r[target] is not None]
    X = StandardScaler().fit_transform(np.array([r["x"] for r in data]))
    y = np.array([r[target] for r in data], dtype=float)
    phyla = sorted({r["phylum"] for r in data})
    D = np.array([[r["phylum"] == p for p in phyla[1:]] for r in data], dtype=float)
    if target == "temperature":
        overall = Ridge(alpha=1.0).fit(X, y).coef_
        within = Ridge(alpha=1.0).fit(np.hstack([X, D]), y).coef_[: X.shape[1]]
    else:
        overall = LogisticRegression(max_iter=2000).fit(X, y).coef_[0]
        within = LogisticRegression(max_iter=2000).fit(np.hstack([X, D]), y).coef_[0][: X.shape[1]]
    return {f: {"overall": round(float(o), 4), "within_phylum": round(float(w), 4),
                "same_sign": bool(np.sign(o) == np.sign(w))} for f, o, w in zip(FEATURES, overall, within)}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--law-id", default="genome_traits_v1")
    ap.add_argument("--out", default="results/genome_laws")
    args = ap.parse_args()
    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    rows = load()
    print(f"{len(rows)} species with a quality GTDB genome and a trait record")
    results = {}
    for target in ("temperature", "oxygen", "host"):
        results[target] = {s: evaluate(rows, target, s) for s in ("random_5fold", "leave_order_out")}
        results[target]["coefficients"] = coefficients(rows, target)
        for s in ("random_5fold", "leave_order_out"):
            r = results[target][s]
            print(f"\n{target} [{s}] n={r['n']} orders={r['n_orders']} {r['metric']}: "
                  + ", ".join(f"{k} {v:.3f}" for k, v in r["scores"].items()))
            for k in ("law_linear - taxonomy", "law_nonlinear - law_linear", "law_linear - mean"):
                if k in r:
                    print(f"   {k}: {r[k]['mean']:+.4f} {r[k]['ci95']}")
        print("   coefficients:", results[target]["coefficients"])
    (out / "metrics.json").write_text(json.dumps(results, indent=1))
    save_law(
        LAWS_DIR / f"{args.law_id}.json",
        id=args.law_id,
        scope=("Bacterial and archaeal growth temperature, oxygen use and host association predicted from "
               "genome-level traits (GC, genome size, coding density, proteins per Mb), across GTDB species "
               "with a trait record. Says nothing about gene content or protein sequence."),
        model="Ridge (temperature) / logistic (oxygen, host) on standardized genome features; gradient "
              "boosting on the same features reported next to it; taxonomy memorisation as the baseline.",
        feature_names=list(FEATURES),
        data={"species": len(rows), "genomes": "GTDB species representatives, CheckM2 >= 90% complete, <= 5% "
              "contamination, one per NCBI species", "traits": "Madin et al. 2020 condensed species table"},
        validation=results,
        caveats=["Traits are literature compilations (Madin et al. 2020), not measurements made here.",
                 "Leave-order-out is the honest test for an unseen lineage; random folds let taxonomy memorise.",
                 "Coefficients are associations; within-phylum signs are reported to show what survives the "
                 "coarsest phylogenetic control.",
                 "Isolation source is where a strain was isolated, not necessarily its lifestyle."],
        # Standard law format (feature -> weight); the within-phylum check stays in validation.
        contexts={t: {f: {"weight": c["overall"], "ci95": [c["overall"], c["overall"]]}
                      for f, c in results[t]["coefficients"].items()} for t in results},
    )
    print(f"Done -> {out}/metrics.json and laws/{args.law_id}.json")


if __name__ == "__main__":
    main()
