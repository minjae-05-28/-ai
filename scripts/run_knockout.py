"""Knockout experiments vs evolution: do genes a living cell can lose in the lab get lost in nature?

    python scripts/run_knockout.py

Uses measured phenotypes from data/phenotypes (scripts/collect_phenotypes.py):
  Fitness Browser   transposon knockouts in ~50 bacteria, fitness in rich and minimal media
  DEG               essential genes from published screens (bacteria, archaea, eukaryotes)
  SGD, PomBase      deletion viability for every gene of budding and fission yeast
  PaxDb             measured protein abundance

Experiments
  1. E. coli -> insect symbionts. Every E. coli gene is classed by its knockout phenotype
     (essential; needed only in minimal medium = biosynthesis; dispensable). How often does
     each class survive in the 24 symbiont genomes?
  2. Family knockout cost vs loss rate. Per Pfam family: share of member genes that are
     essential (eukaryote screens for parasites, bacterial screens for extremophiles). Does it
     predict how often the family is lost, beyond how common the family is (ubiquity)?
  3. Held-out prediction. For every parasite / extremophile pair: AUROC of "non-essential
     families are lost", next to memorisation and the learned law.
  4. Measured abundance. Does PaxDb abundance agree with the codon-based expression proxy,
     and are abundant families lost less?
"""

import json
import re
from collections import defaultdict
from pathlib import Path

import numpy as np
from scipy.stats import spearmanr

from organelle_evo.eukaryotes import catalog as euk
from organelle_evo.eukaryotes.model import counts, family_features
from organelle_evo.laws import LAWS_DIR, save_law
from organelle_evo.predict import auroc
from organelle_evo.prokaryotes import catalog as pro

PH = Path("data/phenotypes")
OUT = Path("results/knockout")


def load(p):
    return json.loads(Path(p).read_text()) if Path(p).exists() else None


def profiles(d, skip=("pfam_meta.json", "family_annotations.json")):
    return {json.loads(f.read_text())["species"]: json.loads(f.read_text()) for f in Path(d).glob("*.json") if f.name not in skip}


def partial_spearman(x, y, z):
    """Spearman of x and y after removing the rank-linear effect of z."""
    from scipy.stats import rankdata

    rx, ry, rz = (rankdata(v) for v in (x, y, z))
    A = np.c_[np.ones_like(rz), rz]
    ex = rx - A @ np.linalg.lstsq(A, rx, rcond=None)[0]
    ey = ry - A @ np.linalg.lstsq(A, ry, rcond=None)[0]
    return float(np.corrcoef(ex, ey)[0, 1])


# ---------------------------------------------------------------------------------------

def symbionts_vs_ecoli(res):
    keio = load(PH / "fitness" / "Keio.json")
    if keio is None:
        print("no Keio data")
        return
    import sys

    sys.path.insert(0, "scripts")
    from run_realdata import load_system

    cache_path = Path("data/processed/homology.json")
    cache = json.loads(cache_path.read_text()) if cache_path.exists() else {}
    ds, _ = load_system("insect_endosymbiont", Path("data/raw"), cache)
    cache_path.write_text(json.dumps(cache))
    cols = keio["columns"]
    if "gene" not in cols:
        print("  Keio data has no gene names yet (re-collect with --orgs Keio)")
        return
    i_ess, i_rich, i_min, i_gene = cols.index("likely_essential"), cols.index("rich_mean_fit"), cols.index("minimal_min_fit"), cols.index("gene")
    cls = {}
    for g, row in keio["genes"].items():
        name = (row[i_gene] or "").lower()
        if not name:
            continue
        if row[i_ess]:
            c = "essential"
        elif row[i_min] is not None and row[i_min] < -1 and (row[i_rich] is None or row[i_rich] > -0.5):
            c = "needed only in minimal medium"
        elif row[i_rich] is not None and row[i_rich] < -1:
            c = "costly in rich medium"
        else:
            c = "dispensable"
        cls[name] = c
    genes = [g.lower() for g in ds.genes]
    present = ds.present  # (lineages, genes)
    out = {}
    for c in ("essential", "costly in rich medium", "needed only in minimal medium", "dispensable"):
        idx = [j for j, g in enumerate(genes) if cls.get(g) == c]
        if not idx:
            continue
        kept = present[:, idx].mean()
        per = {ds.lineages[i]: float(present[i, idx].mean()) for i in range(len(ds.lineages))}
        out[c] = {"n_genes": len(idx), "share_kept_mean": float(kept), "by_symbiont": per}
        print(f"  {c:32s} {len(idx):4d} E. coli genes, kept on average in {kept:.0%} of symbiont genomes")
    matched = sum(1 for g in genes if g in cls)
    y = np.array([cls.get(g) == "essential" for g in genes if g in cls])
    keep_rate = np.array([present[:, j].mean() for j, g in enumerate(genes) if g in cls])
    out["auroc_essential_predicts_retention"] = auroc(keep_rate, y) if y.any() and (~y).any() else None
    out["n_matched_genes"] = matched
    res["symbionts_vs_ecoli_knockouts"] = out


def family_knockout_cost():
    """Per family: share of member genes essential, from eukaryote and bacterial screens."""
    euk_frac, pro_frac = defaultdict(list), defaultdict(list)
    for src in ("yeast/Saccharomyces_cerevisiae.json", "pombe/Schizosaccharomyces_pombe.json"):
        d = load(PH / src)
        if not d:
            continue
        tot, ess = defaultdict(int), defaultdict(int)
        for fams, inviable, viable in d["genes"].values():
            for f in fams:
                tot[f] += 1
                ess[f] += inviable
        for f in tot:
            euk_frac[f].append(ess[f] / tot[f])
    for f in (PH / "fitness").glob("*.json"):
        d = json.loads(f.read_text())
        i = d["columns"].index("likely_essential")
        tot, ess = defaultdict(int), defaultdict(int)
        for row in d["genes"].values():
            for fam in row[0]:
                tot[fam] += 1
                ess[fam] += row[i]
        for fam in tot:
            pro_frac[fam].append(ess[fam] / tot[fam])
    # DEG: essential genes per organism; denominators from the project's own Pfam profiles of
    # the same species. Descendants (parasites, extremophiles) are excluded so the knockout
    # data never come from the lineages being predicted.
    euk_desc = {d for _, d in euk.resolve_pairs(euk.SPECIES)}
    pro_desc = {d for _, d in pro.resolve_pairs(pro.SPECIES)}
    for domain, prof_dir, frac, desc in (("eukaryotes", "data/eukaryotes", euk_frac, euk_desc),
                                         ("bacteria", "data/prokaryotes", pro_frac, pro_desc),
                                         ("archaea", "data/prokaryotes", pro_frac, pro_desc)):
        d = load(PH / "deg" / f"{domain}.json")
        if not d:
            continue
        prof = profiles(prof_dir)
        by_binomial = {" ".join(k.split()[:2]): v for k, v in prof.items()}
        for org, e in d.items():
            key = " ".join(org.split()[:2])
            if key in desc or key not in by_binomial or e["n_essential"] < 100:
                continue
            fams = by_binomial[key]["families"]
            # every family the organism has: essential share (0 when no member is essential)
            for fam, v in fams.items():
                if v[0] > 0:
                    frac[fam].append(min(1.0, e["families"].get(fam, 0) / v[0]))
            print(f"  DEG {domain}: {org} ({e['n_essential']} essential) matched to profile {key}")
    return ({f: float(np.mean(v)) for f, v in euk_frac.items()}, {f: float(np.mean(v)) for f, v in pro_frac.items()},
            {f: len(v) for f, v in euk_frac.items()}, {f: len(v) for f, v in pro_frac.items()})


def pairs_test(name, prof, pairs, ess, res, ubiquity_species):
    meta = json.loads(Path("data/eukaryotes/pfam_meta.json").read_text())
    fams, _ = family_features(list(prof.values()), meta)
    c = {s: counts(p, fams) for s, p in prof.items()}
    fidx = {f: i for i, f in enumerate(fams)}
    tested = [f for f in fams if f in ess]
    if len(tested) < 50:
        print(f"{name}: too few families with knockout data ({len(tested)})")
        return
    ubi = np.mean([c[s] > 0 for s in ubiquity_species if s in c], axis=0)
    # loss rate across descendant lineages, for families the relative had
    lost = np.zeros(len(fams))
    seen = np.zeros(len(fams))
    for a, d in pairs:
        had = c[a] > 0
        seen += had
        lost += had & (c[d] == 0)
    ix = np.array([fidx[f] for f in tested])
    ok = seen[ix] >= 3
    ix = ix[ok]
    e = np.array([ess[fams[i]] for i in ix])
    rate = lost[ix] / seen[ix]
    rho = float(spearmanr(e, rate).correlation)
    prho = partial_spearman(e, rate, ubi[ix])
    print(f"{name}: {len(ix)} families with knockout data; Spearman(essential share, loss rate) {rho:+.2f}, "
          f"controlling for ubiquity {prho:+.2f}")
    # quartiles
    q = np.quantile(e, [0.25, 0.5, 0.75])
    groups = {"never essential": e == 0, "sometimes essential (≤50%)": (e > 0) & (e <= 0.5), "mostly essential (>50%)": e > 0.5}
    gq = {k: {"n_families": int(m.sum()), "mean_loss_rate": float(rate[m].mean()) if m.any() else None} for k, m in groups.items()}
    for k, v in gq.items():
        print(f"   {k:28s} {v['n_families']:5d} families, loss rate {v['mean_loss_rate']}")
    # held-out pairs: AUROC of (1 - essential share) for families with data
    aucs, memo = [], []
    for a, d in pairs:
        had = c[a] > 0
        j = np.array([fidx[f] for f in tested])
        j = j[had[j]]
        y = (c[d][j] == 0)
        if y.all() or not y.any():
            continue
        aucs.append(auroc(-np.array([ess[fams[i]] for i in j]), y))
        others = [(c[x], c[z]) for x, z in pairs if z != d]
        fr = np.array([np.mean([om[i] == 0 for on, om in others if on[i] > 0]) if any(on[i] > 0 for on, _ in others) else 0.5 for i in j])
        memo.append(auroc(fr, y))
    res[name] = {"n_families": int(len(ix)), "spearman_essential_vs_loss": rho, "partial_controlling_ubiquity": prho,
                 "groups": gq, "heldout_auroc_knockout_only": float(np.mean(aucs)) if aucs else None,
                 "heldout_auroc_memorisation_same_families": float(np.mean(memo)) if memo else None, "n_pairs": len(aucs)}
    if aucs:
        print(f"   held-out pairs ({len(aucs)}): knockout alone AUROC {np.mean(aucs):.3f}, memorisation {np.mean(memo):.3f}")


def abundance(res):
    ctx = {}
    for cat in ("eukaryotes", "prokaryotes"):
        for f in Path(f"data/family_context/{cat}").glob("*.json"):
            d = json.loads(f.read_text())
            ctx[d["species"]] = d["families"]
    out = {}
    for f in (PH / "paxdb").glob("*.json"):
        d = json.loads(f.read_text())
        sp = d["species"]
        fam_ab = {k: float(np.median(v)) for k, v in d["families"].items() if v}
        if sp in ctx:
            common = [k for k in fam_ab if k in ctx[sp] and ctx[sp][k][2]]
            if len(common) > 30:
                cz = [ctx[sp][k][1] / ctx[sp][k][2] for k in common]
                r = float(spearmanr(cz, [np.log10(fam_ab[k] + 1e-3) for k in common]).correlation)
                out[sp] = {"n_families": len(common), "spearman_codon_proxy_vs_measured": r}
                print(f"  {sp:40s} codon proxy vs measured abundance: Spearman {r:+.2f} ({len(common)} families)")
    res["abundance_proxy_check"] = out


def main():
    res = {}
    print("1. E. coli knockouts vs insect symbiont genomes")
    symbionts_vs_ecoli(res)
    euk_ess, pro_ess, n_euk, n_pro = family_knockout_cost()
    res["families_with_knockout_data"] = {"eukaryote_screens": len(euk_ess), "bacterial_screens": len(pro_ess)}
    print(f"\nfamilies with knockout data: eukaryote screens {len(euk_ess)}, bacterial screens {len(pro_ess)}")
    print("\n2-3. Family knockout cost vs loss")
    E = profiles("data/eukaryotes")
    epairs = [(a, d) for a, d in euk.resolve_pairs(E) if euk.design(d)[1]]
    pairs_test("parasites (eukaryote screens)", E, epairs, euk_ess, res,
               [s for s in E if euk.SPECIES.get(s) and euk.SPECIES[s].lifestyle == euk.FREE])
    P = profiles("data/prokaryotes")
    ppairs = pro.resolve_pairs(P)
    pairs_test("extremophiles (bacterial screens)", P, ppairs, pro_ess, res, list(P))
    print("\n4. Measured protein abundance")
    abundance(res)
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "metrics.json").write_text(json.dumps(res, indent=2))
    save_law(LAWS_DIR / "knockout_v1.json", id="knockout_v1",
             scope="Whether genes that laboratory knockouts show to be dispensable are the ones lost in evolution "
                   "(insect symbionts vs E. coli knockouts; parasites and extremophiles vs family essentiality).",
             model="Knockout phenotype classes and family essential shares compared with observed retention; "
                   "Spearman with and without ubiquity; held-out pair AUROC.",
             feature_names=[], data=res.get("families_with_knockout_data", {}), validation=res, contexts={},
             caveats=["Essentiality is measured in lab media, not in the host.",
                      "Fitness Browser 'likely essential' = no transposon mutants recovered.",
                      "Families are matched by Pfam domains, not orthology."])
    print(f"Done -> {OUT}/")


if __name__ == "__main__":
    main()
