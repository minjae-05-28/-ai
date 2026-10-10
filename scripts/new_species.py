"""Out-of-sample test on eukaryote proteomes the project has never used (pre-registration 10:
docs/preregistration/2026-10-10_new_species_prediction.md).

    python scripts/new_species.py plan --n 1000 --n-shards 20   (Actions)
        -> data/new_species/pick.json  (UniProt eukaryote reference proteomes not yet collected, BUSCO C >= 60,
                                        round-robin over classes in a seeded random order, best BUSCO first)
    python scripts/new_species.py fetch --shard i --n-shards 20  (Actions) -> data/new_species/shards/part_<i>.json.gz
    python scripts/new_species.py predict                         -> results/new_species/summary.json

Prediction for a new species from its taxonomy only (its proteome is never used as input):
    anchor     the most specific taxon in its NCBI lineage that some tip of the leca2 tree also carries
    model      G3c (simulator base laws): posterior at the common ancestor of those tips, carried down a
               branch as long as the mean ancestor-to-tip distance of those tips
    relatives  share of collected proteomes (all ~1,800 eukaryotes and fungi) that carry the anchor taxon
               and have the family
    global     share of all collected eukaryote proteomes that have the family
Truth: the family is in the new species' UniProt Pfam annotation.
"""

import argparse
import gzip
import json
import random
import re
import sys
import time
import urllib.parse
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
from uniprot_proteomes import REST, get, profile  # noqa: E402

OUT = Path("data/new_species")
RES = Path("results/new_species")


def taxonomy(taxid):
    e = json.loads(get(f"{REST}/taxonomy/{taxid}?format=json", tries=4))
    names, ranks = [], {}
    for it in e.get("lineage", []):                     # order does not matter: the anchor is chosen by tip count
        name = it.get("scientificName") if isinstance(it, dict) else str(it).rpartition(" (")[0]
        rank = (it.get("rank") or "").lower() if isinstance(it, dict) else ""
        if name:
            names.append(name)
            if rank:
                ranks[rank] = name
    return {"lineage": names + [e.get("scientificName", "")], "ranks": ranks}


def plan(n, n_shards, min_busco=60.0, seed=0):
    collected = set()
    for f in Path("data/uniprot/shards").glob("*.json.gz"):
        collected |= set(json.loads(gzip.open(f, "rt").read()))
    collected |= set(json.loads(Path("data/markers/leca2_pick.json").read_text())["upids"])
    text = get(f"{REST}/proteomes/stream?query={urllib.parse.quote('reference:true AND taxonomy_id:2759')}"
               "&format=tsv&fields=upid,organism,organism_id,protein_count,busco")
    rows = {}
    for ln in text.strip().split("\n")[1:]:
        upid, org, tid, npr, busco = (ln.split("\t") + [""] * 5)[:5]
        m = re.search(r"C:([\d.]+)%", busco or "")
        c = float(m.group(1)) if m else None
        if upid in collected or c is None or c < min_busco:
            continue
        rows[upid] = {"organism": org, "taxid": tid, "busco_c": c}
    print(f"{len(rows)} uncollected eukaryote reference proteomes with BUSCO C >= {min_busco}", flush=True)
    tids = sorted({r["taxid"] for r in rows.values()})

    def safe(t):
        try:
            return t, taxonomy(t)
        except Exception as e:
            print(f"  taxonomy {t}: {e}", flush=True)
            return t, None
    with ThreadPoolExecutor(8) as ex:
        tax = dict(ex.map(safe, tids))
    by_class = {}
    for upid, r in rows.items():
        t = tax.get(r["taxid"])
        if not t:
            continue
        key = t["ranks"].get("class") or t["ranks"].get("phylum") or "?"
        by_class.setdefault(key, []).append((-r["busco_c"], r["organism"], upid))
    keys = sorted(by_class)
    random.Random(seed).shuffle(keys)
    for k in keys:
        by_class[k].sort()
    chosen, i = [], 0
    while len(chosen) < n and any(len(by_class[k]) > i for k in keys):
        for k in keys:
            if len(by_class[k]) > i and len(chosen) < n:
                chosen.append(by_class[k][i][2])
        i += 1
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "pick.json").write_text(json.dumps({
        "rule": f"uncollected UniProt eukaryote reference proteomes, BUSCO C >= {min_busco}; round-robin over NCBI "
                f"classes (phylum when no class) in a seeded random order (seed {seed}), best BUSCO first",
        "n_candidates": len(rows), "n_classes": len(keys), "upids": chosen,
        "species": {u: {**rows[u], **tax[rows[u]["taxid"]]} for u in chosen}}, indent=1))
    print(f"picked {len(chosen)} from {len(keys)} classes")
    print(json.dumps(list(range(n_shards))))


def fetch(shard, n_shards):
    meta = json.loads(Path("data/eukaryotes/pfam_meta.json").read_text())
    name_of = {v["accession"].split(".")[0]: k for k, v in meta.items()}
    pick = json.loads((OUT / "pick.json").read_text())
    mine = pick["upids"][shard::n_shards]
    out, t0 = {}, time.time()
    for i, upid in enumerate(mine):
        try:
            p = profile(upid, name_of)
        except Exception as e:
            print(f"  skip {upid}: {e}", flush=True)
            continue
        out[upid] = {"organism": pick["species"][upid]["organism"], "n_proteins": p["n_proteins"], "pfam": p["pfam"]}
        if i % 10 == 0:
            print(f"  {i + 1}/{len(mine)} {out[upid]['organism']}: {len(p['pfam'])} families ({time.time() - t0:.0f}s)",
                  flush=True)
    (OUT / "shards").mkdir(parents=True, exist_ok=True)
    with gzip.open(OUT / "shards" / f"part_{shard:03d}.json.gz", "wt") as f:
        json.dump(out, f)


def predict():
    from evo_simulator import Simulator
    from leca_v3_model import ROOTS, g3_fit, setup, shares_for, strata_of
    from run_clade_ancestor import mrca
    from organelle_evo.predict import auroc

    pick = json.loads((OUT / "pick.json").read_text())
    new = {}
    for f in sorted((OUT / "shards").glob("*.json.gz")):
        new.update(json.loads(gzip.open(f, "rt").read()))
    sim = Simulator()
    # node posteriors of G3c on the leca2 tree (amorphea root), and the tree tips' lineages
    d, fams, names, sg, plastid, lineage = setup(ROOTS["amorphea"])
    strata = strata_of(fams, shares_for(fams))
    vis = np.zeros(len(d["parent"]), bool)
    vis[d["tips"]] = True
    post, _ = g3_fit(d, vis, strata, use_strata=True, choose_mult=True)
    col = {f: j for j, f in enumerate(fams)}
    tip_lin = {v: set(lineage.get(names[v], [])) for v in d["tips"]}
    # all collected eukaryote proteomes with their lineage where known (for 'relatives')
    prof = sim.prof
    lin_all = {r["organism"].replace("'", ""): set(r["lineage"])
               for r in json.loads(Path("data/markers/leca2_pick.json").read_text())["lineage"].values()}
    F = len(fams)
    glob_freq = np.array([sum(f in p for p in prof.values()) for f in fams], float) / len(prof)
    W = sim.weights(fams)
    rows, skipped = [], {}
    for upid, rec in new.items():
        sp = pick["species"][upid]
        L = sp["lineage"]
        truth = np.array([f in rec["pfam"] for f in fams], float)
        if rec["n_proteins"] < 1000 or truth.sum() < 300:
            skipped[upid] = "proteome too small"
            continue
        # the most specific shared taxon = the one carried by the fewest tree tips (order-independent)
        cands = [(sum(taxon in tip_lin[v] for v in d["tips"]), taxon) for taxon in set(L[:-1]) if taxon]
        cands = [c for c in cands if c[0] > 0]
        if not cands:
            skipped[upid] = "no tree tip shares any taxon"
            continue
        anchor = min(cands)[1]
        A = [v for v in d["tips"] if anchor in tip_lin[v]]
        node = mrca(A, d["parent"], d["depth"]) if len(A) > 1 else A[0]
        t = float(np.mean([d["depth"][v] - d["depth"][node] for v in A])) if len(A) > 1 else 0.05
        p0 = post[node].astype(float)
        lo, g = sim.grid[:, :1], sim.grid[:, 1:2]
        r = lo + g
        e = np.exp(-r * t)
        pi = g / r
        model = (W * (p0[None, :] * (pi + (1 - pi) * e) + (1 - p0[None, :]) * pi * (1 - e))).sum(0)
        rel_orgs = [o for o, ls in lin_all.items() if anchor in ls and o in prof]
        rel_orgs += [names[v] for v in A if names[v] in prof and names[v] not in rel_orgs]
        relatives = np.array([np.mean([f in prof[o] for o in rel_orgs]) for f in fams]) if rel_orgs else glob_freq
        rows.append({"upid": upid, "organism": rec["organism"], "anchor": anchor,
                     "n_anchor_tips": len(A), "n_relatives": len(rel_orgs),
                     "phylum": sp["ranks"].get("phylum", "?"), "kingdom_or_group": next(
                         (x for x in ("Metazoa", "Fungi", "Viridiplantae", "Sar", "Discoba", "Amoebozoa", "Rhodophyta",
                                      "Metamonada", "Haptista", "Cryptophyceae") if x in L), "other"),
                     "auroc_model": float(auroc(model, truth)), "auroc_relatives": float(auroc(relatives, truth)),
                     "auroc_global": float(auroc(glob_freq, truth)),
                     "size_true": int(truth.sum()), "size_model": round(float(model.sum()), 1)})
    RES.mkdir(parents=True, exist_ok=True)
    rng = np.random.default_rng(0)
    A_ = np.array([[r["auroc_model"], r["auroc_relatives"], r["auroc_global"]] for r in rows])

    def ci(dv):
        bs = [dv[rng.integers(0, len(dv), len(dv))].mean() for _ in range(2000)]
        lo_, hi_ = np.percentile(bs, [2.5, 97.5])
        return {"mean": round(float(dv.mean()), 4), "ci95": [round(float(lo_), 4), round(float(hi_), 4)],
                "verdict": "양성" if lo_ > 0 else ("음성" if hi_ < 0 else "무승부"),
                "share_positive": round(float((dv > 0).mean()), 3)}
    groups = {}
    for r in rows:
        groups.setdefault(r["kingdom_or_group"], []).append(r)
    summary = {
        "preregistration": "docs/preregistration/2026-10-10_new_species_prediction.md",
        "n_new_species_fetched": len(new), "n_scored": len(rows), "skipped": skipped,
        "mean_auroc": {"model": round(float(A_[:, 0].mean()), 4), "relatives": round(float(A_[:, 1].mean()), 4),
                       "global": round(float(A_[:, 2].mean()), 4)},
        "model_minus_relatives": ci(A_[:, 0] - A_[:, 1]),
        "model_minus_global": ci(A_[:, 0] - A_[:, 2]),
        "relatives_minus_global": ci(A_[:, 1] - A_[:, 2]),
        "by_group": {g: {"n": len(v), "model": round(float(np.mean([x["auroc_model"] for x in v])), 4),
                         "relatives": round(float(np.mean([x["auroc_relatives"] for x in v])), 4),
                         "global": round(float(np.mean([x["auroc_global"] for x in v])), 4)} for g, v in groups.items()},
    }
    by_n = {}
    for r in rows:
        k = "relatives_1-2" if r["n_relatives"] <= 2 else ("relatives_3-10" if r["n_relatives"] <= 10 else "relatives_>10")
        by_n.setdefault(k, []).append(r)
    summary["by_number_of_relatives"] = {k: {"n": len(v), "model_minus_relatives": round(float(np.mean(
        [x["auroc_model"] - x["auroc_relatives"] for x in v])), 4)} for k, v in by_n.items()}
    (RES / "summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=1))
    (RES / "per_species.json").write_text(json.dumps(rows, ensure_ascii=False, indent=1))
    print(json.dumps({k: v for k, v in summary.items() if k != "skipped"}, ensure_ascii=False, indent=1))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("step", choices=["plan", "fetch", "predict"])
    ap.add_argument("--n", type=int, default=1000)
    ap.add_argument("--shard", type=int, default=0)
    ap.add_argument("--n-shards", type=int, default=20)
    a = ap.parse_args()
    if a.step == "plan":
        plan(a.n, a.n_shards)
    elif a.step == "fetch":
        fetch(a.shard, a.n_shards)
    else:
        predict()


if __name__ == "__main__":
    main()
