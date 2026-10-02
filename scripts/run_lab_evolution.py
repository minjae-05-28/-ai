"""Does a law learned over hundreds of millions of years hold over 50,000 generations?

    python scripts/run_lab_evolution.py [--ltee data/raw/ltee]

The laws in this project are fitted to comparisons between present-day genomes whose
ancestors split tens to hundreds of millions of years ago. The long-term evolution
experiment with E. coli (Lenski 1988-, Barrick lab's curated genome-diff files) is the
opposite regime: one known ancestor, 12 replicate populations, a constant glucose-limited
medium, and sequenced clones from 0 to >50,000 generations (~25 years). Genes really are
deleted there, mostly by IS150-mediated deletions.

So we can ask whether the same genes are involved:
  1. Which REL606 genes fall inside a deletion in a sequenced clone, at which generation.
  2. Does the comparative loss rate (how often a Pfam family is lost across our 57
     prokaryote pairs) predict which E. coli genes the experiment deletes?
  3. Controls: knockout essentiality (Fitness Browser / DEG) and the expression proxy.
  4. The mutation-accumulation experiment (MAE), where single cells are passaged with
     almost no selection, is the negative control: if the law tracks LTEE deletions but
     not MAE deletions, selection rather than mutation bias is doing the work.
  5. Scale: genes lost per 1,000 generations, next to what the reduced genomes lost.

Gene -> Pfam families comes from the Keio profile in data/phenotypes/fitness (gene names),
so no HMM search is needed here. Output: results/lab_evolution/.
"""

import argparse
import json
import re
import subprocess
from collections import defaultdict
from pathlib import Path

import numpy as np
from scipy.stats import spearmanr

from organelle_evo.eukaryotes.model import counts, family_features
from organelle_evo.laws import LAWS_DIR, save_law
from organelle_evo.predict import auroc
from organelle_evo.prokaryotes import catalog as pro

REPO = "https://github.com/barricklab/LTEE-Ecoli.git"
OUT = Path("results/lab_evolution")
PH = Path("data/phenotypes")


def ensure_repo(path):
    path = Path(path)
    if not (path / "reference" / "REL606.gff3").exists():
        path.parent.mkdir(parents=True, exist_ok=True)
        print(f"cloning {REPO} -> {path}")
        subprocess.run(["git", "clone", "-q", "--depth", "1", REPO, str(path)], check=True)
    return path


def genes_of(gff):
    """Gene name and interval for every annotated gene of the ancestor."""
    out = []
    for line in Path(gff).read_text().splitlines():
        c = line.split("\t")
        if len(c) > 8 and c[2] == "gene":
            m = re.search(r"Name=([^;]+)", c[8])
            if m:
                out.append((m.group(1).lower(), int(c[3]), int(c[4])))
    return out


def deletions(gd):
    """(start, length) of every DEL entry, plus the clone's generation and population."""
    gen = pop = None
    dels = []
    for line in Path(gd).read_text().splitlines():
        if line.startswith("#=TIME"):
            gen = int(float(line.split("\t")[1]))
        elif line.startswith("#=POPULATION"):
            pop = line.split("\t")[1]
        elif line.startswith("DEL\t"):
            c = line.split("\t")
            dels.append((int(c[4]), int(c[5])))
    return pop, gen, dels


def deleted_genes(dels, genes, min_frac=0.8):
    """Genes with at least min_frac of their length inside a deletion."""
    hit = set()
    for name, s, e in genes:
        covered = sum(max(0, min(e, ds + dl - 1) - max(s, ds) + 1) for ds, dl in dels)
        if covered >= min_frac * (e - s + 1):
            hit.add(name)
    return hit


def scan(folder, genes):
    """Per clone: population, generation, and the set of genes deleted in it."""
    rows = []
    for gd in sorted(Path(folder).glob("*.gd")):
        pop, gen, dels = deletions(gd)
        if not gen:  # generation 0 = the ancestor itself, relative to the reference
            continue
        rows.append({"clone": gd.stem, "population": pop, "generation": gen,
                     "n_deletions": len(dels), "genes": sorted(deleted_genes(dels, genes))})
    return rows


def keio_families():
    k = json.loads((PH / "fitness" / "Keio.json").read_text())
    ci = {c: i for i, c in enumerate(k["columns"])}
    fams, ess = {}, {}
    for row in k["genes"].values():
        name = (row[ci["gene"]] or "").lower()
        if name:
            fams[name] = row[ci["families"]]
            ess[name] = row[ci["likely_essential"]]
    return fams, ess


def comparative_loss():
    """How often each Pfam family is lost across the project's prokaryote pairs."""
    prof = {}
    for f in Path("data/prokaryotes").glob("*.json"):
        if f.name in ("pfam_meta.json", "family_annotations.json"):
            continue
        d = json.loads(f.read_text())
        prof[d["species"]] = d
    meta = json.loads(Path("data/eukaryotes/pfam_meta.json").read_text())
    fams, _ = family_features(list(prof.values()), meta)
    c = {s: counts(p, fams) for s, p in prof.items()}
    pairs = pro.resolve_pairs(prof)
    lost = np.zeros(len(fams))
    seen = np.zeros(len(fams))
    for a, d in pairs:
        had = c[a] > 0
        seen += had
        lost += had & (c[d] == 0)
    ubi = np.mean([c[s] > 0 for s in prof], axis=0)
    rate = {f: (lost[i] / seen[i] if seen[i] >= 3 else None) for i, f in enumerate(fams)}
    return rate, {f: float(ubi[i]) for i, f in enumerate(fams)}, len(pairs)


def expression_proxy():
    p = Path("data/family_context/prokaryotes")
    for f in p.glob("*.json"):
        d = json.loads(f.read_text())
        if d["species"].startswith("Escherichia coli"):
            return {k: v[1] / v[2] for k, v in d["families"].items() if v[2]}
    return {}


def gene_score(name, fams, per_family):
    """A gene's score is the mean over its families of whatever per-family value is given."""
    vs = [per_family[f] for f in fams.get(name, []) if per_family.get(f) is not None]
    return float(np.mean(vs)) if vs else None


def boot_auroc(x, y, n=2000, seed=0):
    rng = np.random.default_rng(seed)
    vs = []
    for _ in range(n):
        i = rng.integers(0, len(y), len(y))
        if y[i].any() and not y[i].all():
            vs.append(auroc(x[i], y[i]))
    return [float(np.percentile(vs, 2.5)), float(np.percentile(vs, 97.5))] if vs else None


def paired_diff(xa, ya, xb, yb, n=2000, seed=0):
    """Bootstrap CI for AUROC(a) - AUROC(b); the two gene sets are resampled independently."""
    rng = np.random.default_rng(seed)
    vs = []
    for _ in range(n):
        i, j = rng.integers(0, len(ya), len(ya)), rng.integers(0, len(yb), len(yb))
        if ya[i].any() and not ya[i].all() and yb[j].any() and not yb[j].all():
            vs.append(auroc(xa[i], ya[i]) - auroc(xb[j], yb[j]))
    return (float(np.mean(vs)), [float(np.percentile(vs, 2.5)), float(np.percentile(vs, 97.5))]) if vs else (None, None)


def test(label, rows, genes, fams, ess, rate, ubi, expr, res, keep=None):
    deleted = defaultdict(set)
    for r in rows:
        for g in r["genes"]:
            deleted[g].add(r["population"] or r["clone"])
    names = [n for n, _, _ in genes] if keep is None else [n for n, _, _ in genes if n in keep]
    scored = [n for n in names if gene_score(n, fams, rate) is not None]
    y = np.array([n in deleted for n in scored])
    print(f"\n{label}: {len(rows)} clones, {len(deleted)} genes deleted in at least one "
          f"({y.sum()} of {len(scored)} with a comparative loss rate)")
    out = {"n_clones": len(rows), "n_genes_deleted": len(deleted), "n_scored": len(scored),
           "n_deleted_scored": int(y.sum())}
    if y.sum() < 10 or y.all():
        print("  too few deleted genes to test")
        res[label] = out
        return
    x = np.array([gene_score(n, fams, rate) for n in scored])
    out["auroc_comparative_loss_rate"] = auroc(x, y)
    out["auroc_ci"] = boot_auroc(x, y)
    out["_x"], out["_y"] = x, y
    ci = out["auroc_ci"]
    print(f"  comparative loss rate predicts deletion: AUROC {out['auroc_comparative_loss_rate']:.3f} "
          f"[{ci[0]:.3f}, {ci[1]:.3f}]")
    u = np.array([gene_score(n, fams, ubi) for n in scored], dtype=float)
    out["auroc_rarity_baseline"] = auroc(-u, y)
    print(f"  rarity baseline (uncommon families deleted): AUROC {out['auroc_rarity_baseline']:.3f}")
    if expr:
        se = [n for n in scored if gene_score(n, fams, expr) is not None]
        ye = np.array([n in deleted for n in se])
        if ye.any() and not ye.all():
            out["auroc_low_expression"] = auroc(-np.array([gene_score(n, fams, expr) for n in se]), ye)
            print(f"  low expression predicts deletion: AUROC {out['auroc_low_expression']:.3f} ({len(se)} genes)")
    known = [n for n in names if n in ess]
    de = sum(1 for n in known if n in deleted)
    ee = sum(1 for n in known if ess[n] and n in deleted)
    out["deleted_genes_with_knockout_data"] = de
    out["deleted_that_are_essential"] = ee
    out["essential_share_overall"] = float(np.mean([ess[n] for n in known]))
    out["essential_share_deleted"] = (ee / de) if de else None
    print(f"  essential in the lab: {out['essential_share_overall']:.1%} of all genes, "
          f"{(out['essential_share_deleted'] or 0):.1%} of deleted genes")
    res[label] = out
    return deleted


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--ltee", default="data/raw/ltee")
    args = ap.parse_args()
    repo = ensure_repo(args.ltee)
    genes = genes_of(repo / "reference" / "REL606.gff3")
    fams, ess = keio_families()
    rate, ubi, n_pairs = comparative_loss()
    expr = expression_proxy()
    print(f"{len(genes)} ancestor genes, {sum(1 for n, _, _ in genes if n in fams)} mapped to Pfam families; "
          f"comparative loss rates from {n_pairs} pairs")

    res = {"n_ancestor_genes": len(genes), "n_comparative_pairs": n_pairs}
    ltee = scan(repo / "LTEE-clone-curated", genes)
    mae = scan(repo / "MAE-clone-curated", genes)
    L = "LTEE (50,000 generations, 12 populations, selection)"
    M = "MAE (mutation accumulation, almost no selection)"
    deleted = test(L, ltee, genes, fams, ess, rate, ubi, expr, res)
    test(M, mae, genes, fams, ess, rate, ubi, expr, res)
    # a deletion covering an essential gene kills the cell, so it can never be sequenced in
    # either experiment. Re-test on genes the lab says are dispensable.
    disp = {n for n, v in ess.items() if not v}
    print("\nSame tests on genes that are dispensable in the lab (the deletion is survivable):")
    test(L + ", dispensable genes", ltee, genes, fams, ess, rate, ubi, expr, res, keep=disp)
    test(M + ", dispensable genes", mae, genes, fams, ess, rate, ubi, expr, res, keep=disp)
    for a, b in ((L, M), (L + ", dispensable genes", M + ", dispensable genes")):
        if "_x" in res.get(a, {}) and "_x" in res.get(b, {}):
            d, dci = paired_diff(res[a]["_x"], res[a]["_y"], res[b]["_x"], res[b]["_y"])
            res[a]["auroc_minus_no_selection_control"] = {"mean": d, "ci95": dci}
            print(f"\n{a.split(' (')[0]} minus the no-selection control: {d:+.3f} [{dci[0]:+.3f}, {dci[1]:+.3f}]"
                  f"{'  -> selection adds nothing detectable' if dci[0] < 0 < dci[1] else ''}")
    for v in res.values():
        if isinstance(v, dict):
            v.pop("_x", None)
            v.pop("_y", None)

    # how fast, and how parallel
    per_pop = defaultdict(set)
    last = {}
    for r in ltee:
        if r["population"]:
            per_pop[r["population"]] |= set(r["genes"])
            last[r["population"]] = max(last.get(r["population"], 0), r["generation"])
    rates = [len(v) / max(last[p], 1) * 1000 for p, v in per_pop.items()]
    res["genes_lost_per_1000_generations"] = {"mean": float(np.mean(rates)), "min": float(np.min(rates)),
                                              "max": float(np.max(rates)), "n_populations": len(per_pop)}
    print(f"\nscale: {np.mean(rates):.1f} genes lost per 1,000 generations "
          f"({np.min(rates):.1f}-{np.max(rates):.1f} across {len(per_pop)} populations); "
          f"at this rate {np.mean(rates) * 50:.0f} genes in 50,000 generations")
    if deleted:
        n_par = defaultdict(int)
        for g, pops in deleted.items():
            n_par[len(pops)] += 1
        res["parallelism"] = {str(k): v for k, v in sorted(n_par.items())}
        rep = sum(v for k, v in n_par.items() if k >= 3)
        print(f"parallel loss: {rep} genes deleted in 3 or more of the 12 populations")
        # time course: generation of first deletion
        first = {}
        for r in sorted(ltee, key=lambda r: r["generation"]):
            for g in r["genes"]:
                first.setdefault(g, r["generation"])
        early = [g for g, t in first.items() if t <= 5000]
        late = [g for g, t in first.items() if t > 20000]
        for name, gs in (("deleted by 5,000 generations", early), ("first deleted after 20,000", late)):
            vs = [gene_score(g, fams, rate) for g in gs]
            vs = [v for v in vs if v is not None]
            if vs:
                print(f"  {name}: {len(gs)} genes, mean comparative loss rate {np.mean(vs):.3f}")
                res.setdefault("by_first_generation", {})[name] = {"n_genes": len(gs), "mean_comparative_loss_rate": float(np.mean(vs))}
        if len(first) > 20:
            fg = [g for g in first if gene_score(g, fams, rate) is not None]
            rho = spearmanr([first[g] for g in fg], [gene_score(g, fams, rate) for g in fg]).correlation
            res["spearman_first_generation_vs_comparative_loss_rate"] = float(rho)
            print(f"  Spearman(generation first deleted, comparative loss rate) {rho:+.2f} ({len(fg)} genes)")

    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "metrics.json").write_text(json.dumps(res, indent=2))
    (OUT / "ltee_deleted_genes.json").write_text(json.dumps(
        {"clones": ltee, "mae_clones": mae}, separators=(",", ":")))
    save_law(LAWS_DIR / "lab_evolution_v1.json", id="lab_evolution_v1",
             scope="Whether the comparative loss law, fitted to genomes that diverged over millions of years, "
                   "predicts which genes are deleted in 50,000 generations of experimental evolution in E. coli "
                   "(LTEE), with mutation accumulation as the no-selection control.",
             model="Per gene: mean comparative loss rate of its Pfam families across the project's prokaryote "
                   "pairs, scored against whether the gene falls inside a deletion in a sequenced clone. "
                   "Rarity, expression proxy and lab essentiality as baselines.",
             feature_names=[], data={"ancestor_genes": len(genes), "ltee_clones": len(ltee), "mae_clones": len(mae)},
             validation=res, contexts={},
             caveats=["One species in one constant medium: a lab regime, not a model of any natural environment.",
                      "LTEE deletions are largely IS150-mediated, so mutation bias shapes which genes are reachable.",
                      "Gene-to-family mapping uses Keio gene names, so unnamed and unmatched genes are left out.",
                      "50,000 generations removes tens of genes; the reduced genomes in this project lost "
                      "hundreds to thousands, so the regimes differ in scale by orders of magnitude."])
    print(f"\nDone -> {OUT}/")


if __name__ == "__main__":
    main()
