"""Which families a lineage loses: large-scale per-family propensity (2) and close relatives (1),
from ~18,000 UniProt bacterial/archaeal reference proteomes, scored on the held-out extremophile
pairs of run_forward_evolution.py.

    python scripts/run_relatives.py [--scores results/forward_evolution/extremophiles_scores.npz]

For every held-out pair (proxy -> descendant) the ancestral families are ranked by how likely
they are to be lost, by:
    copies            fewer ancestral copies first
    memorisation      (reference) loss frequency in the other training pairs
    law / no_axes_law the birth-death law (lineage held out, amount predicted), as saved
    rarity20k         families carried by fewer of the ~18,000 proteomes first
    turnover20k       within-genus absence rate: in genera (>= 3 proteomes) where the family
                      occurs, the share of members lacking it. Genera of the evaluated pair are
                      removed before scoring, so the pair never informs its own propensity.
    propensity20k     rank average of rarity20k and turnover20k
    relatives         share of the descendant's genus (else its taxonomic family) lacking the
                      family, without the descendant's and the proxy's own species. This is not a
                      law: it uses the lineage's close relatives, the information the sibling ceiling
                      (run_ceiling.py) showed the laws cannot reach.
    combinations      rank averages: law+propensity20k, law+relatives, law+propensity20k+relatives
Metrics per pair: AUROC of the loss ranking, and fate accuracy when the top-k families are
removed with k = the law's own predicted amount (so only the choice of families differs), next to
"no change" (keep everything). Intervals: bootstrap over held-out lineages.
Families UniProt never annotates (HMMER-only weak domains) get no relative/propensity signal and
take the median score instead of reading as "absent everywhere".
"""

import argparse
import csv
import gzip
import json
import re
from collections import defaultdict
from pathlib import Path

import numpy as np
from scipy.stats import rankdata

from organelle_evo.predict import auroc


def key(name):
    w = re.sub(r"^Candidatus ", "", name.strip()).replace("[", "").replace("]", "").split()
    return (w[0] if w else ""), " ".join(w[:2]).lower()


def genus_to_family():
    out = {}
    csv.field_size_limit(10**8)
    for r in csv.DictReader(gzip.open("data/gtdb/species_reps.tsv.gz", "rt"), delimiter="\t"):
        ranks = dict(t.split("__", 1) for t in r["ncbi_taxonomy"].split(";") if "__" in t)
        g, f = ranks.get("g", ""), ranks.get("f", "")
        if g and f:
            out[g.replace("Candidatus ", "")] = f
    return out


def scan(fams, relevant_genera, relevant_families, g2f):
    """One pass over the shards: per-genus presence counts, and member vectors for relevant taxa."""
    col = {f: i for i, f in enumerate(fams)}
    F = len(fams)
    total = np.zeros(F)
    n_total = 0
    genus_n = defaultdict(int)
    genus_cnt = {}
    members = defaultdict(list)  # taxon -> [(species, presence)]
    for path in sorted(Path("data/uniprot/shards").glob("*.json.gz")):
        for p in json.loads(gzip.open(path, "rt").read()).values():
            if p.get("kingdom") not in ("bacteria", "archaea"):
                continue
            g, sp = key(p["organism"])
            v = np.zeros(F, dtype=bool)
            idx = [col[f] for f in p["pfam"] if f in col]
            v[idx] = True
            total += v
            n_total += 1
            genus_n[g] += 1
            genus_cnt.setdefault(g, np.zeros(F, dtype=np.int32))
            genus_cnt[g] += v
            if g in relevant_genera:
                members[("genus", g)].append((sp, v))
            fam = g2f.get(g)
            if fam in relevant_families:
                members[("family", fam)].append((sp, v))
                members[("family_genus", fam)].append((g, v))
    return total, n_total, genus_n, genus_cnt, members


def boot(vals, units, n=2000, seed=0):
    rng = np.random.default_rng(seed)
    by = defaultdict(list)
    for v, u in zip(vals, units):
        if np.isfinite(v):
            by[u].append(v)
    ks = list(by)
    flat = [v for vs in by.values() for v in vs]
    st = [np.mean([v for i in rng.choice(len(ks), len(ks)) for v in by[ks[i]]]) for _ in range(n)]
    return {"mean": round(float(np.mean(flat)), 4),
            "ci95": [round(float(np.percentile(st, 2.5)), 4), round(float(np.percentile(st, 97.5)), 4)]}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--scores", default="results/forward_evolution/extremophiles_scores.npz")
    ap.add_argument("--out", default="results/relatives")
    ap.add_argument("--save-law", action="store_true", help="only write laws/loss_prediction_v1.json from results")
    args = ap.parse_args()
    if args.save_law:
        save()
        return
    z = np.load(args.scores)
    fams, pairs, units = list(z["fams"]), [str(p) for p in z["pairs"]], [str(u) for u in z["units"]]
    g2f = genus_to_family()
    split = [tuple(s.strip() for s in p.split("->")) for p in pairs]
    genera = {key(x)[0] for a, d in split for x in (a, d)}
    families = {g2f.get(key(d)[0]) for _, d in split} - {None}
    total, n_total, genus_n, genus_cnt, members = scan(fams, genera, families, g2f)
    print(f"{n_total} bacterial/archaeal proteomes, {len(genus_n)} genera; {len(pairs)} held-out pairs")

    big = [g for g, n in genus_n.items() if n >= 3]
    occ = np.zeros(len(fams))  # genera where the family occurs
    absent = np.zeros(len(fams))  # sum over those genera of the share lacking it
    for g in big:
        c, n = genus_cnt[g], genus_n[g]
        occ += c > 0
        absent += np.where(c > 0, 1 - c / n, 0)
    seen = total > 0

    rows = []
    for i, ((a, d), u) in enumerate(zip(split, units)):
        idx = z[f"{i}|fam_idx"]
        lost = z[f"{i}|real_lost"].astype(bool)
        # Remove the evaluated pair's genera from the propensity statistics.
        o, s, t, nt = occ.copy(), absent.copy(), total.copy(), n_total
        for g in {key(a)[0], key(d)[0]}:
            if g in genus_cnt:
                c, n = genus_cnt[g], genus_n[g]
                t -= c
                nt -= n
                if n >= 3:
                    o -= c > 0
                    s -= np.where(c > 0, 1 - c / n, 0)
        rarity = 1 - t / max(nt, 1)
        turnover = np.where(o > 0, s / np.maximum(o, 1), np.nan)
        # Close relatives: the descendant's genus, else its taxonomic family, without own species.
        dg, dsp = key(d)
        _, asp = key(a)
        rel, rel_level = None, None
        for level, taxon in (("genus", dg), ("family", g2f.get(dg))):
            mem = [v for sp, v in members.get((level, taxon), []) if sp not in (dsp, asp)]
            if len(mem) >= 2:
                rel, rel_level = 1 - np.mean(mem, axis=0), f"{level} ({len(mem)})"
                break
        # Stricter: other genera of the descendant's family only (the descendant's and the proxy's
        # genera removed), so very close sister species, sometimes split from the same species, cannot
        # stand in for the descendant.
        ag = key(a)[0]
        far = [v for g_, v in members.get(("family_genus", g2f.get(dg)), []) if g_ not in (dg, ag)]
        rel_far = 1 - np.mean(far, axis=0) if len(far) >= 2 else None
        sc = {"copies": -z[f"{i}|copies"], "memorisation": z[f"{i}|memorisation"], "law": z[f"{i}|law"],
              "no_axes_law": z[f"{i}|no_axes_law"]}
        known = seen[idx]
        fill = lambda x: np.where(known & np.isfinite(x), x, np.nanmedian(x[known]) if known.any() else 0.5)  # noqa: E731
        sc["rarity20k"] = fill(rarity[idx])
        sc["turnover20k"] = fill(np.nan_to_num(turnover[idx], nan=np.nan))
        sc["propensity20k"] = (rankdata(sc["rarity20k"]) + rankdata(sc["turnover20k"])) / 2
        if rel is not None:
            sc["relatives"] = fill(rel[idx])
        if rel_far is not None:
            sc["relatives_other_genera"] = fill(rel_far[idx])
        ra = lambda *ks: sum(rankdata(sc[k]) for k in ks) / len(ks)  # noqa: E731
        sc["law+propensity20k"] = ra("law", "propensity20k")
        if rel is not None:
            sc["law+relatives"] = ra("law", "relatives")
            sc["law+propensity20k+relatives"] = ra("law", "propensity20k", "relatives")
        if rel_far is not None:
            sc["law+relatives_other_genera"] = ra("law", "relatives_other_genera")
        k = int(round(z[f"{i}|law"].sum()))
        row = {"pair": f"{a} -> {d}", "unit": u, "relatives_from": rel_level,
               "other_genera": len(far), "n_ancestral": int(len(idx)),
               "n_lost": int(lost.sum()), "k_removed": k, "no_change.fate": round(float(1 - lost.mean()), 4)}
        for name, s_ in sc.items():
            row[f"{name}.auroc"] = round(float(auroc(s_, lost)), 4)
            top = np.argsort(-s_)[:k]
            pred = np.zeros(len(idx), dtype=bool)
            pred[top] = True
            row[f"{name}.fate"] = round(float((pred == lost).mean()), 4)
        rows.append(row)
        print(f"  {d:34s} rel={rel_level or '-':14s} law {row['law.auroc']:.3f} prop20k {row['propensity20k.auroc']:.3f} "
              f"rel {row.get('relatives.auroc', float('nan')):.3f} far {row.get('relatives_other_genera.auroc', float('nan')):.3f} law+rel {row.get('law+relatives.auroc', float('nan')):.3f} "
              f"memo {row['memorisation.auroc']:.3f}", flush=True)

    methods = [m for m in ("copies", "memorisation", "law", "no_axes_law", "rarity20k", "turnover20k", "propensity20k",
                           "relatives", "relatives_other_genera", "law+propensity20k", "law+relatives",
                           "law+relatives_other_genera", "law+propensity20k+relatives")
               if f"{m}.auroc" in rows[0] or any(f"{m}.auroc" in r for r in rows)]
    summary = {"n_pairs": len(rows), "n_lineages": len(set(units)),
               "pairs_with_relatives": sum(r["relatives_from"] is not None for r in rows)}
    sub = [r for r in rows if r["relatives_from"] is not None]
    far_rows = [r for r in rows if "relatives_other_genera.auroc" in r]
    summary["pairs_with_other_genera"] = len(far_rows)
    for m in methods:
        rr = far_rows if "other_genera" in m else sub if "relatives" in m else rows
        summary[f"{m}.auroc"] = boot([r[f"{m}.auroc"] for r in rr], [r["unit"] for r in rr])
        summary[f"{m}.fate"] = boot([r[f"{m}.fate"] for r in rr], [r["unit"] for r in rr])
    summary["no_change.fate"] = boot([r["no_change.fate"] for r in rows], [r["unit"] for r in rows])
    summary["no_change.fate (pairs with relatives)"] = boot([r["no_change.fate"] for r in sub], [r["unit"] for r in sub])
    for m, ref, rr in (("propensity20k", "law", rows), ("law+propensity20k", "law", rows),
                       ("law+propensity20k", "memorisation", rows), ("relatives", "law", sub),
                       ("law+relatives", "law", sub), ("law+relatives", "memorisation", sub),
                       ("relatives_other_genera", "law", far_rows), ("law+relatives_other_genera", "law", far_rows),
                       ("law+relatives_other_genera", "memorisation", far_rows),
                       ("law+propensity20k+relatives", "memorisation", sub)):
        summary[f"{m} - {ref} (auroc)"] = boot([r[f"{m}.auroc"] - r[f"{ref}.auroc"] for r in rr], [r["unit"] for r in rr])
    summary["no_change.fate (pairs with other genera)"] = boot([r["no_change.fate"] for r in far_rows],
                                                               [r["unit"] for r in far_rows])
    for m, rr in (("law", rows), ("law+propensity20k", rows), ("relatives", sub), ("law+relatives", sub),
                  ("relatives_other_genera", far_rows), ("law+relatives_other_genera", far_rows),
                  ("law+propensity20k+relatives", sub)):
        summary[f"{m} - no_change (fate)"] = boot([r[f"{m}.fate"] - r["no_change.fate"] for r in rr], [r["unit"] for r in rr])
    print("\nsummary (mean [95% CI over lineages])")
    for k_, v in summary.items():
        if isinstance(v, dict):
            print(f"  {k_:45s} {v['mean']:+.4f} {v['ci95']}")
        else:
            print(f"  {k_:45s} {v}")
    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    tag = Path(args.scores).stem.replace("_scores", "")
    (out / f"{tag}.json").write_text(json.dumps({"summary": summary, "pairs": rows}, indent=1))
    print(f"Done -> {out}/{tag}.json")


def save(law_id="loss_prediction_v1"):
    """Write the law card from the proxy and consensus-ancestor results (both must exist)."""
    from organelle_evo.laws import LAWS_DIR, save_law

    res = {t: json.loads(Path(f"results/relatives/{t}.json").read_text())["summary"]
           for t in ("extremophiles", "extremophiles_consensus")}
    save_law(
        LAWS_DIR / f"{law_id}.json",
        id=law_id,
        scope=("Which ancestral gene families a bacterial/archaeal lineage loses when it moves to an extreme "
               "environment, scored on held-out lineages: the birth-death law against a per-family propensity "
               "estimated from ~18,000 UniProt reference proteomes, and against close relatives of the descendant."),
        model=("propensity20k = rank average of rarity across ~18,000 proteomes and within-genus absence rate, "
               "with the evaluated pair's genera removed (a law: properties of the family). relatives = share of "
               "the descendant's genus (or family) lacking the family, without its own and the proxy's species "
               "(a predictor, not a law: it reads the lineage's relatives). Combinations are rank averages."),
        feature_names=["rarity20k", "turnover20k", "relatives", "relatives_other_genera"],
        data={"held_out_pairs": res["extremophiles"]["n_pairs"], "lineages": res["extremophiles"]["n_lineages"],
              "proteomes": "UniProt reference proteomes, bacteria + archaea"},
        validation=res,
        caveats=[
            "relatives is not a law: it uses the descendant lineage's close relatives, the information the "
            "sibling ceiling showed cross-lineage laws cannot reach. Reported apart from the laws.",
            "Some genus relatives are near-identical sister species split from the same species (e.g. "
            "Lactiplantibacillus argentoratensis, Bacteroides hominis agree with the truth almost as well as the "
            "descendant's own UniProt proteome, 0.94 vs 0.93 median). relatives_other_genera removes the "
            "descendant's and the proxy's genera and is the stricter number.",
            "UniProt Pfam misses weak domains HMMER finds; families UniProt never annotates take the median score.",
            "Fate accuracy removes the top-k families with k = the law's own predicted amount; this deterministic "
            "rule beats the stochastic forward simulation of run_forward_evolution.py.",
            "With a consensus ancestor (proxy's own gains removed) the law falls from 0.793 to 0.764 AUROC while "
            "relatives stay at 0.919: part of the law's score came from families only the proxy carried.",
            "Extremophiles only: the eukaryote parasites are mostly protists, which the UniProt layer (bacteria, "
            "archaea, fungi) does not cover.",
        ],
        contexts={},
    )
    print(f"law -> laws/{law_id}.json")


if __name__ == "__main__":
    main()
