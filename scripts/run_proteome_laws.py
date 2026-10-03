"""Round 2 of the large-scale laws: proteome composition and Pfam content (UniProt reference
proteomes) against growth temperature, oxygen use and host association (trait table).

    python scripts/run_proteome_laws.py [--law-id proteome_traits_v1]

Each bacterial/archaeal reference proteome in data/uniprot/shards is matched to the trait table
(data/traits, Madin et al. 2020) by species name (first two words of the organism, without
"Candidatus"); one proteome per species. Taxonomy for grouping and memorisation comes from the
trait table (NCBI phylum ... genus).

Feature sets, compared side by side (same targets, folds and baselines as genome_traits_v1):
    composition     20 amino-acid frequencies + IVYWREL, charge-polarity, acidic excess, side-chain
                    N, GRAVY, FYMINK, median pI
    pfam            presence of every Pfam family carried by >= 1% of the proteomes
    composition+pfam
Baselines: mean (0.5 for AUROC), taxonomy memorisation (closest training taxon).
Schemes: random 5-fold and leave-order-out (whole orders unseen). Differences for the
leave-order-out scheme get a 95% interval from resampling orders.
Interpretation: the Pfam families with the largest coefficients per target (sign = direction).
Fungi have no trait record here and are not used.
"""

import argparse
import csv
import gzip
import json
import re
import sys
from collections import Counter
from pathlib import Path

import numpy as np
from scipy import sparse
from sklearn.linear_model import LogisticRegression, LogisticRegressionCV, Ridge, RidgeCV
from sklearn.metrics import mean_absolute_error, roc_auc_score
from sklearn.model_selection import GroupKFold, KFold
from sklearn.preprocessing import StandardScaler

sys.path.insert(0, str(Path(__file__).resolve().parent))
from run_genome_laws import ENVIRONMENTAL, boot_diff, taxonomy_predict  # noqa: E402

from organelle_evo.laws import LAWS_DIR, save_law  # noqa: E402

AA = "ACDEFGHIKLMNPQRSTVWY"
COMP = ("ivywrel", "cvp", "acidic_excess", "n_side", "gravy", "fymink", "median_pi")
RANKS = ("phylum", "class", "order", "family", "genus")


def species_key(name):
    words = re.sub(r"^Candidatus ", "", name.strip()).replace("[", "").replace("]", "").split()
    return " ".join(words[:2]).lower()


def load(min_share=0.01, shards="data/uniprot/shards"):
    traits = {}
    for r in csv.DictReader(gzip.open("data/traits/madin2020_condensed_species_NCBI.csv.gz", "rt")):
        traits.setdefault(species_key(r["species"]), r)
    proteomes = {}
    for f in sorted(Path(shards).glob("*.json.gz")):
        for upid, p in json.loads(gzip.open(f, "rt").read()).items():
            if p.get("kingdom") in ("bacteria", "archaea") and p.get("composition"):
                proteomes[upid] = p
    rows = {}
    for upid, p in proteomes.items():
        key = species_key(p["organism"])
        if key not in traits:
            continue
        busco = re.search(r"C:([\d.]+)%", p.get("busco") or "")
        comp = float(busco.group(1)) if busco else 100.0
        if key in rows and rows[key]["busco"] >= comp:
            continue  # keep the most complete proteome per species
        t = traits[key]
        temp = float(t["growth_tmp"]) if t["growth_tmp"] not in ("", "NA") else None
        met = t["metabolism"]
        oxy = 1 if met in ("aerobic", "obligate aerobic") else 0 if met in ("anaerobic", "obligate anaerobic") else None
        src = t["isolation_source"]
        host = 1 if src.startswith("host") else 0 if src.startswith(ENVIRONMENTAL) else None
        c = p["composition"]
        rows[key] = {"upid": upid, "species": key, "busco": comp, "temperature": temp, "oxygen": oxy, "host": host,
                     "comp": [c["composition"][a] for a in AA] + [c[k] for k in COMP],
                     "pfam": set(p["pfam"]), **{r: t.get(r, "") for r in RANKS}}
    rows = list(rows.values())
    counts = Counter(f for r in rows for f in r["pfam"])
    fams = sorted(f for f, n in counts.items() if n >= max(2, min_share * len(rows)))
    col = {f: i for i, f in enumerate(fams)}
    data, ii, jj = [], [], []
    for i, r in enumerate(rows):
        for f in r["pfam"]:
            if f in col:
                ii.append(i)
                jj.append(col[f])
                data.append(1.0)
    P = sparse.csr_matrix((data, (ii, jj)), shape=(len(rows), len(fams)))
    C = np.array([r["comp"] for r in rows])
    return rows, fams, C, P, len(proteomes)


def design(C, P, which, tr, te):
    blocks_tr, blocks_te = [], []
    if "composition" in which:
        sc = StandardScaler().fit(C[tr])
        blocks_tr.append(sparse.csr_matrix(sc.transform(C[tr])))
        blocks_te.append(sparse.csr_matrix(sc.transform(C[te])))
    if "pfam" in which:
        blocks_tr.append(P[tr])
        blocks_te.append(P[te])
    return sparse.hstack(blocks_tr).tocsr(), sparse.hstack(blocks_te).tocsr()


def fit_model(X, y, reg):
    if reg:
        return RidgeCV(alphas=np.logspace(-1, 5, 13)).fit(X, y)
    return LogisticRegressionCV(Cs=np.logspace(-4, 1, 6), cv=3, scoring="roc_auc", max_iter=3000).fit(X, y)


def evaluate(rows, C, P, target, scheme, seed=0):
    idx = np.array([i for i, r in enumerate(rows) if r[target] is not None])
    if target != "temperature":
        n_pos = sum(rows[i][target] for i in idx)
        if min(n_pos, len(idx) - n_pos) < 30:
            return {"skipped": f"too few examples in one class ({n_pos} vs {len(idx) - n_pos})"}
    elif len(idx) < 100:
        return {"skipped": f"too few species with a temperature ({len(idx)})"}
    sub = [rows[i] for i in idx]
    y = np.array([r[target] for r in sub], dtype=float)
    groups = np.array([r["order"] or "unknown" for r in sub])
    Cs, Ps = C[idx], P[idx]
    reg = target == "temperature"
    splitter = GroupKFold(n_splits=10) if scheme == "leave_order_out" else KFold(5, shuffle=True, random_state=seed)
    methods = ("mean", "taxonomy", "composition", "pfam", "composition+pfam")
    pred = {k: np.zeros(len(y)) for k in methods}
    for tr, te in splitter.split(Cs, y, groups if scheme == "leave_order_out" else None):
        base = float(y[tr].mean())
        pred["mean"][te] = base
        pred["taxonomy"][te] = taxonomy_predict([sub[i] for i in tr], [sub[i] for i in te], y[tr], base)
        for which in ("composition", "pfam", "composition+pfam"):
            Xtr, Xte = design(Cs, Ps, which, tr, te)
            # Penalty chosen by inner cross-validation on the training fold only: thousands of Pfam
            # columns overfit badly at a fixed penalty (random-feature check gave MAE above the mean).
            m = fit_model(Xtr, y[tr], reg)
            pred[which][te] = m.predict(Xte) if reg else m.predict_proba(Xte)[:, 1]
    score = (lambda p: mean_absolute_error(y, p)) if reg else (lambda p: roc_auc_score(y, p))
    out = {"n": int(len(y)), "n_orders": int(len(set(groups))), "metric": "MAE (deg C)" if reg else "AUROC",
           "scores": {k: round(float(score(p)), 4) for k, p in pred.items()}}
    if not reg:
        out["scores"]["mean"] = 0.5
    if scheme == "leave_order_out":
        for k in ("composition", "pfam", "composition+pfam"):
            out[f"{k} - taxonomy"] = boot_diff(y, pred[k], pred["taxonomy"], groups, reg)
        out["composition+pfam - composition"] = boot_diff(y, pred["composition+pfam"], pred["composition"], groups, reg)
    return out


def top_families(rows, P, fams, target, k=12):
    idx = np.array([i for i, r in enumerate(rows) if r[target] is not None])
    y = np.array([rows[i][target] for i in idx], dtype=float)
    m = fit_model(P[idx], y, target == "temperature")
    coef = m.coef_ if target == "temperature" else m.coef_[0]
    order = np.argsort(coef)
    meta = json.loads(Path("data/eukaryotes/pfam_meta.json").read_text())
    desc = lambda f: meta.get(f, {}).get("description", "")  # noqa: E731
    return {"positive": [(fams[j], desc(fams[j]), round(float(coef[j]), 3)) for j in order[::-1][:k]],
            "negative": [(fams[j], desc(fams[j]), round(float(coef[j]), 3)) for j in order[:k]]}


def composition_coefficients(rows, C, target):
    idx = np.array([i for i, r in enumerate(rows) if r[target] is not None])
    y = np.array([rows[i][target] for i in idx], dtype=float)
    X = StandardScaler().fit_transform(C[idx][:, len(AA):])  # summary statistics only, for reading
    m = Ridge(alpha=1.0).fit(X, y).coef_ if target == "temperature" else LogisticRegression(max_iter=3000).fit(X, y).coef_[0]
    return {k: round(float(v), 4) for k, v in zip(COMP, m)}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--law-id", default="proteome_traits_v1")
    ap.add_argument("--out", default="results/proteome_laws")
    ap.add_argument("--shards", default="data/uniprot/shards")
    args = ap.parse_args()
    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    rows, fams, C, P, n_prot = load(shards=args.shards)
    print(f"{n_prot} bacterial/archaeal reference proteomes; {len(rows)} matched to a trait record; "
          f"{len(fams)} Pfam families (>= 1% of proteomes)", flush=True)
    if len(rows) < 200:
        raise SystemExit("too few matched proteomes for a law (need >= 200); collection not finished?")
    results = {}
    for target in ("temperature", "oxygen", "host"):
        results[target] = {s: evaluate(rows, C, P, target, s) for s in ("random_5fold", "leave_order_out")}
        if "skipped" in results[target]["random_5fold"]:
            print(f"\n{target}: {results[target]['random_5fold']['skipped']}")
            continue
        results[target]["composition_coefficients"] = composition_coefficients(rows, C, target)
        results[target]["pfam_top"] = top_families(rows, P, fams, target)
        for s in ("random_5fold", "leave_order_out"):
            r = results[target][s]
            if "skipped" in r:
                print(f"\n{target} [{s}] skipped: {r['skipped']}")
                continue
            print(f"\n{target} [{s}] n={r['n']} orders={r['n_orders']} {r['metric']}: "
                  + ", ".join(f"{k} {v:.3f}" for k, v in r["scores"].items()), flush=True)
            for k, v in r.items():
                if " - " in k:
                    print(f"   {k}: {v['mean']:+.4f} {v['ci95']}")
        print("   composition:", results[target]["composition_coefficients"])
        print("   pfam +:", [f for f, _, _ in results[target]["pfam_top"]["positive"][:6]])
        print("   pfam -:", [f for f, _, _ in results[target]["pfam_top"]["negative"][:6]])
    (out / "metrics.json").write_text(json.dumps(results, indent=1))
    save_law(
        LAWS_DIR / f"{args.law_id}.json",
        id=args.law_id,
        scope=("Bacterial and archaeal growth temperature, oxygen use and host association predicted from "
               "proteome amino-acid composition and Pfam family content (UniProt reference proteomes), "
               "across species with a trait record."),
        model="Ridge / logistic regression on standardized composition and Pfam presence; taxonomy memorisation "
              "and the mean as baselines; random folds and leave-order-out.",
        feature_names=[*AA, *COMP],
        data={"proteomes_matched": len(rows), "proteomes_total": n_prot, "pfam_families": len(fams),
              "source": "UniProt reference proteomes (precomputed Pfam cross-references) x Madin et al. 2020"},
        validation=results,
        caveats=["UniProt Pfam counts every protein entry and uses InterPro's Pfam release; it is a separate "
                 "dataset from the HMMER profiles and is not mixed with them.",
                 "Species are matched by name; strain-level differences are ignored.",
                 "Traits are literature compilations, not measurements made here.",
                 "Pfam coefficients are associations within a regularised model; a family can stand in for "
                 "its lineage, which is why leave-order-out is reported next to random folds."],
        contexts={t: {k: {"weight": v, "ci95": [v, v]} for k, v in results[t]["composition_coefficients"].items()}
                  for t in results if "composition_coefficients" in results[t]},
    )
    print(f"Done -> {out}/metrics.json and laws/{args.law_id}.json")


if __name__ == "__main__":
    main()
