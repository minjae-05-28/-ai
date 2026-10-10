"""Learning loop: predict each new batch of species BEFORE learning from it, then graft it into the tree
and retrain (pre-registration 12: docs/preregistration/2026-10-11_learning_loop.md).

    python scripts/learning_loop.py plan --n 300 --n-shards 15     (Actions) -> data/learning_loop/batch/pick.json
    python scripts/learning_loop.py fetch --shard i --n-shards 15  (Actions) -> data/learning_loop/batch/shards/
    python scripts/learning_loop.py round                           (Actions) -> results/learning_loop/round_<k>.json,
                                                                     tree.nwk, state.json; batch moved to rounds/<k>/

Sources, in order, until each is used up: UniProt eukaryote reference proteomes with BUSCO C >= 60, then
the remaining eukaryote reference proteomes, then other (non-reference, non-redundant) eukaryote proteomes.
Already used: everything in data/uniprot/shards, the leca2 pick, data/new_species (round 1) and earlier rounds.

A round:
  1. score the batch with the CURRENT model (base 250-species tree plus every grafted species so far), with
     the BASE model (250 species only) and by counting relatives among all proteomes held so far
  2. graft the batch into the tree: each species hangs from the common ancestor of the tree tips that share
     its most specific taxon (polytomies split into a balanced binary scaffold with 1e-6 internal branches;
     a 250-way node underflows, see pre-registration 4), branch length = mean ancestor-to-tip distance there
  3. refit G3c on the grown tree (next round's CURRENT model)
Gene-family level only; sequences are never kept.
"""

import argparse
import gzip
import json
import re
import shutil
import sys
import time
import urllib.parse
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))

DATA = Path("data/learning_loop")
RES = Path("results/learning_loop")
BATCH = DATA / "batch"
BASE_TREE = "results/phylo_tree/leca2_fast.nwk"
AMORPHEA = "Opisthokonta+Amoebozoa+Apusozoa+Breviatea"
SOURCES = [("reference, BUSCO C >= 60", "reference:true AND taxonomy_id:2759", 60.0),
           ("reference, any BUSCO", "reference:true AND taxonomy_id:2759", None),
           ]
# Round 4 tried the non-reference proteomes ("reference:false"): all 848 came back with 0 proteins, because
# UniProtKB now holds only reference-proteome proteins (the rest are in UniParc). From then on the loop
# continues on NCBI annotated genomes, counted with HMMER (pre-registration 13).
NCBI_API = "https://api.ncbi.nlm.nih.gov/datasets/v2"
NCBI_SHARDS = 100                                  # each species is a full Pfam search (tens of minutes)


# ---------------------------------------------------------------- bookkeeping
def mem(tag):
    """Current and peak resident memory, for the Actions log (the runner has 16 GB)."""
    try:
        st_ = dict(ln.split(":", 1) for ln in open("/proc/self/status") if ln.startswith(("VmRSS", "VmHWM")))
        print(f"  [mem] {tag}: now {int(st_['VmRSS'].split()[0]) / 1e6:.2f} GB, "
              f"peak {int(st_['VmHWM'].split()[0]) / 1e6:.2f} GB", flush=True)
    except OSError:
        pass


def state():
    p = RES / "state.json"
    return json.loads(p.read_text()) if p.exists() else {"rounds": [], "used_upids": []}


def all_new_species():
    """label -> {"upid", "organism", "lineage", "pfam", "n_proteins", "busco"} for round 1 and every loop round."""
    out = {}
    sources = [(Path("data/new_species/pick.json"), Path("data/new_species/shards"))]
    for rd in sorted((DATA / "rounds").glob("*")):
        sources.append((rd / "pick.json", rd / "shards"))
    for pick_p, shard_dir in sources:
        if not pick_p.exists():
            continue
        pick = json.loads(pick_p.read_text())
        for f in sorted(shard_dir.glob("*.json.gz")):
            for u, r in json.loads(gzip.open(f, "rt").read()).items():
                sp = pick["species"][u]
                out[f"NS_{u}"] = {"upid": u, "organism": r["organism"], "lineage": sp["lineage"], "pfam": r["pfam"],
                                  "n_proteins": r["n_proteins"], "busco": f"C:{sp.get('busco_c', '')}%"}
    return out


def binomial(org):
    return " ".join(org.replace("[", "").replace("]", "").split()[:2])


def used_species():
    """Binomials of every organism already used (base collection, round 1, loop rounds)."""
    names = set()
    for f in Path("data/uniprot/shards").glob("*.json.gz"):
        names |= {binomial(v["organism"]) for v in json.loads(gzip.open(f, "rt").read()).values()}
    names |= {binomial(o) for o in json.loads(Path("data/markers/leca2_pick.json").read_text())["lineage"]}
    for p in [Path("data/new_species/pick.json")] + sorted((DATA / "rounds").glob("*/pick.json")):
        if p.exists():
            names |= {binomial(sp["organism"]) for sp in json.loads(p.read_text())["species"].values()}
    return names


def used_upids():
    used = set()
    for f in Path("data/uniprot/shards").glob("*.json.gz"):
        used |= set(json.loads(gzip.open(f, "rt").read()))
    used |= set(json.loads(Path("data/markers/leca2_pick.json").read_text())["upids"])
    for p in [Path("data/new_species/pick.json")] + sorted((DATA / "rounds").glob("*/pick.json")):
        if p.exists():
            used |= set(json.loads(p.read_text())["upids"])
    return used


def compact(profiles):
    """Share one string object per family name across all profiles (memory grows with every round)."""
    for v in profiles.values():
        v["pfam"] = [sys.intern(x) for x in v["pfam"]]
    return profiles


SHARES_CACHE = RES / "prokaryote_shares.json"


def build_shares_cache():
    """Share of bacterial / archaeal proteomes carrying each family, for every family seen in any prokaryote.
    The prokaryote collection (data/uniprot/shards) is fixed, so a family missing here has share 0."""
    from prokaryote_and_loso import prokaryote_shares
    fams = set()
    for f in sorted(Path("data/uniprot/shards").glob("*.json.gz")):
        for v in json.loads(gzip.open(f, "rt").read()).values():
            if v.get("kingdom") in ("bacteria", "archaea"):
                fams.update(v.get("pfam") or [])
    fams = sorted(fams)
    pro = prokaryote_shares(fams)
    SHARES_CACHE.parent.mkdir(parents=True, exist_ok=True)
    SHARES_CACHE.write_text(json.dumps({k: {f: round(float(x), 6) for f, x in zip(fams, pro[k]) if x > 0}
                                        for k in ("bacteria", "archaea")}))
    print(f"prokaryote shares cached for {len(fams)} families")


def load_shares_cache():
    import leca_v3_model as lv
    if not SHARES_CACHE.exists():
        build_shares_cache()
    c = json.loads(SHARES_CACHE.read_text())
    for k in ("bacteria", "archaea"):
        lv._SHARES.setdefault(k, {}).update(c[k])
    lv._SHARES["complete"] = True


def fill_missing_shares(fams):
    import leca_v3_model as lv
    if lv._SHARES.get("complete"):
        for k in ("bacteria", "archaea"):
            for f in fams:
                lv._SHARES[k].setdefault(f, 0.0)


# ---------------------------------------------------------------- 1. next batch (Actions)
def plan(n, n_shards, seed=0):
    import random
    from new_species import taxonomy
    from uniprot_proteomes import REST, get
    used = used_upids()
    rows, source_used = {}, None
    for label, q, min_busco in SOURCES:
        try:
            text = get(f"{REST}/proteomes/stream?query={urllib.parse.quote(q)}&format=tsv"
                       "&fields=upid,organism,organism_id,protein_count,busco")
        except Exception as e:
            print(f"source {label!r} failed: {e}", flush=True)
            continue
        for ln in text.strip().split("\n")[1:]:
            upid, org, tid, npr, busco = (ln.split("\t") + [""] * 5)[:5]
            if upid in used or upid in rows:
                continue
            m = re.search(r"C:([\d.]+)%", busco or "")
            c = float(m.group(1)) if m else None
            if min_busco is not None and (c is None or c < min_busco):
                continue
            rows[upid] = {"organism": org, "taxid": tid, "busco_c": c if c is not None else -1.0, "source": label}
        print(f"source {label!r}: {len(rows)} candidates so far", flush=True)
        if rows:
            source_used = label
            break
    if not rows:
        rows = ncbi_candidates(used_species())
        if rows:
            source_used = "ncbi"
            keep = sorted(rows)
            random.Random(seed + len(state()["rounds"])).shuffle(keep)
            rows = {u: rows[u] for u in keep[:3 * n]}        # taxonomy is looked up one taxid at a time
            print(f"source 'ncbi': {len(keep)} unused species, {len(rows)} looked up", flush=True)
    if not rows:
        print("no uncollected eukaryote proteomes left in UniProt or NCBI")
        BATCH.mkdir(parents=True, exist_ok=True)
        (BATCH / "pick.json").write_text(json.dumps({"upids": [], "species": {}, "exhausted": True}))
        print("[]")
        return
    tax = {}
    for t in sorted({r["taxid"] for r in rows.values()}):
        try:
            tax[t] = taxonomy(t)
        except Exception as e:
            print(f"  taxonomy {t}: {e}", flush=True)
    by_class = {}
    for u, r in rows.items():
        t = tax.get(r["taxid"])
        if t:
            by_class.setdefault(t["ranks"].get("class") or t["ranks"].get("phylum") or "?", []).append(
                (-r["busco_c"], r["organism"], u))
    keys = sorted(by_class)
    random.Random(seed + len(state()["rounds"])).shuffle(keys)
    for k in keys:
        by_class[k].sort()
    chosen, i = [], 0
    while len(chosen) < n and any(len(by_class[k]) > i for k in keys):
        for k in keys:
            if len(by_class[k]) > i and len(chosen) < n:
                chosen.append(by_class[k][i][2])
        i += 1
    if source_used == "ncbi":
        n_shards = NCBI_SHARDS
    BATCH.mkdir(parents=True, exist_ok=True)
    (BATCH / "pick.json").write_text(json.dumps({
        "source": source_used, "n_candidates": len(rows), "upids": chosen, "n_shards": n_shards,
        "species": {u: {**rows[u], **tax[rows[u]["taxid"]]} for u in chosen}}, indent=1))
    print(f"picked {len(chosen)} of {len(rows)} ({source_used})")
    print(json.dumps(list(range(min(n_shards, max(1, len(chosen)))))))


def ncbi_candidates(used):
    """accession -> row, one annotated assembly per unused species (RefSeq first, then assembly level,
    then protein-coding gene count), from NCBI Datasets."""
    from organelle_evo.eukaryotes.proteomes import _LEVEL, _get
    best, token, pages = {}, None, 0
    while True:
        url = f"{NCBI_API}/genome/taxon/2759/dataset_report?filters.has_annotation=true&page_size=1000"
        if token:
            url += f"&page_token={urllib.parse.quote(token)}"
        try:
            page = json.loads(_get(url))
        except Exception as e:
            print(f"  ncbi listing failed on page {pages + 1}: {e}", flush=True)
            break
        pages += 1
        for r in page.get("reports", []):
            org = r.get("organism", {})
            name, tid = org.get("organism_name", ""), org.get("tax_id")
            bn = binomial(name)
            if not tid or len(bn.split()) < 2 or bn in used or " sp." in f" {bn}":
                continue
            ann = r.get("annotation_info", {})
            genes = int(ann.get("stats", {}).get("gene_counts", {}).get("protein_coding", 0) or 0)
            busco = ann.get("busco", {}).get("complete")
            score = (r.get("source_database") == "SOURCE_DATABASE_REFSEQ",
                     _LEVEL.get(r.get("assembly_info", {}).get("assembly_level", ""), 0), genes)
            if genes < 1000:
                continue
            if bn not in best or score > best[bn][0]:
                best[bn] = (score, {"organism": name, "taxid": str(tid), "accession": r["accession"],
                                    "busco_c": round(100 * float(busco), 1) if busco is not None else -1.0,
                                    "source": "ncbi", "protein_coding_genes": genes})
        token = page.get("next_page_token")
        if not token:
            break
    print(f"  ncbi: {pages} pages, {len(best)} unused species with an annotated assembly", flush=True)
    return {row["accession"]: row for _, row in best.values()}


def ncbi_proteome(acc):
    """gene -> longest protein for one NCBI assembly (sequences are only held in memory)."""
    import io
    import zipfile
    from organelle_evo.eukaryotes.proteomes import _get, longest_per_gene, protein_to_gene, read_fasta
    url = f"{NCBI_API}/genome/accession/{acc}/download?include_annotation_type=PROT_FASTA" \
          "&include_annotation_type=GENOME_GFF"
    zf = zipfile.ZipFile(io.BytesIO(_get(url)))
    names = zf.namelist()
    faa = next(n for n in names if n.endswith("protein.faa"))
    gff = next((n for n in names if re.search(r"genomic\.gff$", n)), None)
    proteins = read_fasta(zf.read(faa).decode())
    gene_of = protein_to_gene(zf.read(gff).decode()) if gff else {}
    return longest_per_gene(proteins, gene_of)


def fetch(shard, n_shards, pfam="pfam/Pfam-A.hmm", budget_s=300 * 60):
    pick = json.loads((BATCH / "pick.json").read_text())
    n_shards = pick.get("n_shards", n_shards)
    if pick.get("source") == "ncbi":
        return fetch_ncbi(pick, shard, n_shards, pfam, budget_s)
    from uniprot_proteomes import profile
    meta = json.loads(Path("data/eukaryotes/pfam_meta.json").read_text())
    name_of = {v["accession"].split(".")[0]: k for k, v in meta.items()}
    out = {}
    for upid in pick["upids"][shard::n_shards]:
        try:
            p = profile(upid, name_of)
        except Exception as e:
            print(f"  skip {upid}: {e}", flush=True)
            continue
        out[upid] = {"organism": pick["species"][upid]["organism"], "n_proteins": p["n_proteins"], "pfam": p["pfam"]}
    (BATCH / "shards").mkdir(parents=True, exist_ok=True)
    with gzip.open(BATCH / "shards" / f"part_{shard:03d}.json.gz", "wt") as f:
        json.dump(out, f)


def fetch_ncbi(pick, shard, n_shards, pfam, budget_s):
    """HMMER (Pfam GA cut-offs) on each assembly's proteins; stops starting new species near the time budget."""
    from organelle_evo.eukaryotes.pfam import family_profile, load_hmms
    t_start = time.time()
    hmms = load_hmms(pfam)
    print(f"loaded {len(hmms)} Pfam HMMs", flush=True)
    out, took = {}, []
    for acc in pick["upids"][shard::n_shards]:
        if took and time.time() - t_start + 1.5 * max(took) > budget_s:
            print(f"  time budget reached; {acc} left for a later round", flush=True)
            break
        t0 = time.time()
        try:
            proteins = ncbi_proteome(acc)
            fam = family_profile(proteins, hmms)
        except Exception as e:
            print(f"  skip {acc}: {e}", flush=True)
            continue
        took.append(time.time() - t0)
        out[acc] = {"organism": pick["species"][acc]["organism"], "n_proteins": len(proteins),
                    "pfam": sorted(f for f, v in fam.items() if v[0] > 0)}
        print(f"  {acc} {out[acc]['organism']}: {len(proteins)} genes, {len(out[acc]['pfam'])} families, "
              f"{took[-1]:.0f}s", flush=True)
        del proteins
    (BATCH / "shards").mkdir(parents=True, exist_ok=True)
    with gzip.open(BATCH / "shards" / f"part_{shard:03d}.json.gz", "wt") as f:
        json.dump(out, f)


# ---------------------------------------------------------------- 2. tree handling
def to_newick(parent, length, label):
    children = [[] for _ in parent]
    for v, p in enumerate(parent):
        if p >= 0:
            children[p].append(v)

    def rec(v):
        if not children[v]:
            return "'" + label[v].replace("'", "") + f"':{length[v]:.6f}"
        kids = [rec(c) for c in children[v]]
        while len(kids) > 2:                          # balanced binary scaffold
            kids = [f"({kids[i]},{kids[i + 1]}):0.000001" if i + 1 < len(kids) else kids[i]
                    for i in range(0, len(kids), 2)]
        return f"({','.join(kids)}):{length[v]:.6f}"
    return rec(0).rsplit(":", 1)[0] + ";"


def current_tree():
    p = RES / "tree.nwk"
    return str(p) if p.exists() else None


def load_tree_rooted(lineage_all, profiles):
    """parent, length, labels of the current rooted tree (the base tree rooted on Amorphea | rest)."""
    import run_clade_ancestor as rca
    plain = {k.replace("'", ""): v for k, v in profiles.items()}   # tree labels carry no apostrophes
    rca.load_profiles = lambda: {**profiles, **plain}
    path = current_tree()
    if path is None:
        d, fams, names, *_ = rca.build(BASE_TREE, set(), 100, "*", False, AMORPHEA, lineage_all)
    else:
        d, fams, names, *_ = rca.build(path, set(), 100, "*", False, None, lineage_all)
    return d, fams, names


def graft(d, names, tip_lin, new):
    """Hang each new species from the common ancestor of the tips sharing its most specific taxon."""
    from run_clade_ancestor import mrca
    parent = list(d["parent"])
    length = list(d["length"])
    label = [names.get(v, "") for v in range(len(parent))]
    tips = list(d["tips"])
    depth = d["depth"]
    placed = {}
    for lab, sp in new.items():
        L = set(sp["lineage"][:-1])
        cands = [(sum(t in tip_lin[v] for v in tips), t) for t in L if t]
        cands = [c for c in cands if c[0] > 0]
        if not cands:
            continue
        anchor = min(cands)[1]
        A = [v for v in tips if anchor in tip_lin[v]]
        if len(A) > 1:
            node = mrca(A, d["parent"], depth)
            bl = float(np.mean([depth[v] - depth[node] for v in A]))
            parent.append(node)
            length.append(max(bl, 1e-3))
            label.append(lab)
        else:                                          # split the single relative's branch in half
            t = A[0]
            half = length[t] / 2
            mid = len(parent)
            parent.append(parent[t])
            length.append(half)
            label.append("")
            parent[t] = mid
            length[t] = half
            parent.append(mid)
            length.append(half)
            label.append(lab)
        placed[lab] = anchor
    return np.array(parent), np.array(length), label, placed


# ---------------------------------------------------------------- 3. prediction
class NodePost(dict):
    """Posterior rows for the nodes that were asked for (node -> (F,) vector); indexed like the full array."""


def fit_model(d, fams, nodes, chunk=2000):
    """G3c fit; the posterior is the same as g3_fit's, but only kept at `nodes` and computed in family chunks,
    so memory does not grow with tips x families as the tree grows."""
    from leca_v3_model import GRID, g3_fit, shares_for, strata_of
    from mito_model_search import posterior
    fill_missing_shares(fams)
    strata = strata_of(fams, shares_for(fams))
    vis = np.zeros(len(d["parent"]), bool)
    vis[d["tips"]] = True
    R, info = g3_fit(d, vis, strata, use_strata=True, choose_mult=True, return_weights=True)
    mult = np.where(d["reduced_branch"], info["m"], 1.0).astype(np.float32)
    nodes = sorted(set(int(v) for v in nodes))
    F = len(fams)
    out = np.zeros((len(nodes), F), np.float32)
    for a in range(0, F, chunk):
        b = min(a + chunk, F)
        X = d["X"][:, a:b]
        for k, (lv, gv) in enumerate(GRID):
            w = R[k, a:b]
            if w.max() < 1e-6:
                continue
            gk = np.full(b - a, gv, np.float32)
            lk = np.full(b - a, lv, np.float32)
            out[:, a:b] += w[None, :].astype(np.float32) * posterior(d, X, vis, gk, lk, mult, gk / (gk + lk))[nodes]
    post = NodePost({v: out[i] for i, v in enumerate(nodes)})
    return post, R, info


def anchor_node(d, tip_lin, lineage):
    """(node, anchor taxon, tips under it) for a species with this lineage, or None."""
    from run_clade_ancestor import mrca
    L = set(lineage[:-1])
    cands = [(sum(t in tip_lin[v] for v in d["tips"]), t) for t in L if t]
    cands = [c for c in cands if c[0] > 0]
    if not cands:
        return None
    anchor = min(cands)[1]
    A = [v for v in d["tips"] if anchor in tip_lin[v]]
    node = mrca(A, d["parent"], d["depth"]) if len(A) > 1 else A[0]
    return node, anchor, A


def predict_batch(d, fams, names, tip_lin, post, R, batch, fam_universe):
    """Per batch species: probability per family in fam_universe (families outside the model get 0)."""
    from leca_v3_model import GRID
    col = {f: j for j, f in enumerate(fams)}
    idx = np.array([col.get(f, -1) for f in fam_universe])
    lo = np.array([a for a, _ in GRID])[:, None]
    g = np.array([b for _, b in GRID])[:, None]
    out = {}
    for lab, sp in batch.items():
        hit = anchor_node(d, tip_lin, sp["lineage"])
        if hit is None:
            continue
        node, anchor, A = hit
        t = float(np.mean([d["depth"][v] - d["depth"][node] for v in A])) if len(A) > 1 else 0.05
        p0 = post[node].astype(float)
        r = lo + g
        e = np.exp(-r * t)
        pi = g / r
        p = (R * (p0[None, :] * (pi + (1 - pi) * e) + (1 - p0[None, :]) * pi * (1 - e))).sum(0)
        out[lab] = (np.where(idx >= 0, p[np.maximum(idx, 0)], 0.0), anchor)
    return out


WEIGHTS = (0.0, 0.25, 0.5, 0.75, 1.0)           # w * current model + (1 - w) * relatives


def group_of(lineage):
    from prokaryote_and_loso import GROUPS
    return next((g for g in GROUPS if g in lineage), "기타")


def lesson_from(st):
    """Blend weights learned from every species scored in earlier rounds (pre-registration 12)."""
    rows = [r for k in st["rounds"] for r in json.loads((RES / f"round_{k['round']:03d}.json").read_text())["species"]]
    if not rows:
        return {"w_global": 1.0, "w_by_group": {}, "n_from": 0}

    def best(rs):
        return WEIGHTS[int(np.argmax([np.mean([r["blend"][i] for r in rs]) for i in range(len(WEIGHTS))]))]
    by = {}
    for r in rows:
        by.setdefault(r["group"], []).append(r)
    return {"w_global": best(rows), "w_by_group": {g: best(rs) for g, rs in sorted(by.items()) if len(rs) >= 30},
            "n_from": len(rows)}


def round_():
    from run_clade_ancestor import load_profiles as base_loader
    from organelle_evo.predict import auroc
    st = state()
    lesson = lesson_from(st)
    k = len(st["rounds"]) + 2                        # round 1 = pre-registration 10
    pick = json.loads((BATCH / "pick.json").read_text()) if (BATCH / "pick.json").exists() else {"upids": []}
    if not pick["upids"]:
        print("nothing to do: the batch is empty (sources used up)")
        return
    base_prof = compact(base_loader())
    load_shares_cache()
    mem("profiles")
    held = compact(all_new_species())                # everything learned so far (round 1 + earlier rounds)
    batch = {}
    for f in sorted((BATCH / "shards").glob("*.json.gz")):
        for u, r in json.loads(gzip.open(f, "rt").read()).items():
            sp = pick["species"][u]
            if r["n_proteins"] >= 1000 and len(r["pfam"]) >= 300:
                batch[f"NS_{u}"] = {"upid": u, "organism": r["organism"], "lineage": sp["lineage"], "pfam": r["pfam"],
                                    "n_proteins": r["n_proteins"], "busco": f"C:{sp.get('busco_c', '')}%"}
    base_lin = {r["organism"].replace("'", ""): r["lineage"]
                for r in json.loads(Path("data/markers/leca2_pick.json").read_text())["lineage"].values()}
    compact(batch)
    lin_all = {**base_lin, **{k_: v["lineage"] for k_, v in held.items()}}
    prof_all = {**base_prof, **{k_: {**v, "kingdom": "eukaryotes"} for k_, v in held.items()}}
    # CURRENT model: tree with everything grafted so far
    d, fams, names = load_tree_rooted(lin_all, prof_all)
    names = {v: names[v] for v in d["tips"]}
    tip_lin = {v: set(lin_all.get(names[v], [])) for v in d["tips"]}
    def needed(dd, tl):
        hits = [anchor_node(dd, tl, sp["lineage"]) for sp in batch.values()]
        return [int(np.where(dd["parent"] < 0)[0][0])] + [h[0] for h in hits if h]
    mem("current tree built")
    post, R, info = fit_model(d, fams, needed(d, tip_lin))
    mem("current model fitted")
    # BASE model: the 250-species tree only
    import run_clade_ancestor as rca
    rca.load_profiles = lambda: base_prof
    db, fb, nb, *_ = rca.build(BASE_TREE, set(), 100, "*", False, AMORPHEA, base_lin)
    nb = {v: nb[v] for v in db["tips"]}
    tlb = {v: set(base_lin.get(nb[v], [])) for v in db["tips"]}
    post_b, R_b, _ = fit_model(db, fb, needed(db, tlb))
    mem("base model fitted")
    universe = sorted(set(fams) | set(fb))
    pc = predict_batch(d, fams, names, tip_lin, post, R, batch, universe)
    pb = predict_batch(db, fb, nb, tlb, post_b, R_b, batch, universe)
    # relatives among every proteome held so far (base collection + learned species)
    # (counted without building a set per proteome: memory grows with every round)
    from collections import Counter
    held_lin = {**{o: set(L) for o, L in base_lin.items()}, **{k_: set(v["lineage"]) for k_, v in held.items()}}
    held_prof = {**{o: p["pfam"] for o, p in base_prof.items()}, **{k_: v["pfam"] for k_, v in held.items()}}

    def share(orgs):
        c = Counter(f for o in orgs for f in set(held_prof[o]))
        return np.array([c.get(f, 0) for f in universe], float) / len(orgs)
    gfreq = share(list(held_prof))
    rel_cache = {}
    rows = []
    miss = np.zeros(len(universe))                    # sum over species of (predicted - present)
    lose_by_anchor = {}
    for lab, sp in batch.items():
        if lab not in pc or lab not in pb:
            continue
        truth = np.array([f in sp["pfam"] for f in universe], float)
        anchor = pc[lab][1]
        if anchor not in rel_cache:
            rel_ = [o for o, L in held_lin.items() if anchor in L and o in held_prof]
            rel_cache[anchor] = (rel_, share(rel_) if rel_ else gfreq)
        rel, relp = rel_cache[anchor]
        grp = group_of(sp["lineage"])
        w = lesson["w_by_group"].get(grp, lesson["w_global"])
        applied = w * pc[lab][0] + (1 - w) * relp
        miss += pc[lab][0] - truth
        r = {"label": lab, "organism": sp["organism"], "group": grp, "anchor": anchor, "n_relatives": len(rel),
             "busco": sp["busco"], "w": w,
             "current": float(auroc(pc[lab][0], truth)), "base": float(auroc(pb[lab][0], truth)),
             "relatives": float(auroc(relp, truth)), "global": float(auroc(gfreq, truth)),
             "applied": float(auroc(applied, truth)),
             "blend": [round(float(auroc(x * pc[lab][0] + (1 - x) * relp, truth)), 5) for x in WEIGHTS]}
        rows.append(r)
        lose_by_anchor.setdefault(anchor, []).append(r["current"] - r["relatives"])
    mem("batch scored")
    rng = np.random.default_rng(0)

    def ci(dv):
        bs = [dv[rng.integers(0, len(dv), len(dv))].mean() for _ in range(2000)]
        lo_, hi_ = np.percentile(bs, [2.5, 97.5])
        return {"mean": round(float(dv.mean()), 4), "ci95": [round(float(lo_), 4), round(float(hi_), 4)],
                "verdict": "양성" if lo_ > 0 else ("음성" if hi_ < 0 else "무승부"),
                "share_positive": round(float((dv > 0).mean()), 3)}
    A = {k_: np.array([r[k_] for r in rows]) for k_ in ("applied", "current", "base", "relatives", "global")}
    busco = np.array([float(r["busco"][2:-1]) for r in rows if r["busco"][2:-1] not in ("", "-1.0")])
    order = np.argsort(miss)
    summary = {"round": k, "source": pick.get("source"), "n_batch": len(batch), "n_scored": len(rows),
               "tree_tips_before": len(d["tips"]), "learned_species_before": len(held),
               "busco_c_quartiles": [round(float(q), 1) for q in np.percentile(busco, [25, 50, 75])] if len(busco) else None,
               "lesson_applied": lesson,
               "mean_auroc": {k_: round(float(v.mean()), 4) for k_, v in A.items()},
               "applied_minus_relatives": ci(A["applied"] - A["relatives"]),
               "current_minus_relatives": ci(A["current"] - A["relatives"]),
               "current_minus_base": ci(A["current"] - A["base"]),
               "applied_minus_current": ci(A["applied"] - A["current"]),
               "fit_before": {"m": info["m"]},
               "report_only": {
                   "anchors_where_model_loses": sorted(
                       [[a, len(v), round(float(np.mean(v)), 4)] for a, v in lose_by_anchor.items()
                        if len(v) >= 5 and np.mean(v) < 0], key=lambda x: x[2])[:20],
                   "lost_more_than_predicted": [[universe[i], round(float(miss[i] / len(rows)), 3)] for i in order[::-1][:20]],
                   "present_more_than_predicted": [[universe[i], round(float(miss[i] / len(rows)), 3)] for i in order[:20]]}}
    print(json.dumps({k_: v for k_, v in summary.items() if k_ != "report_only"}, ensure_ascii=False, indent=1), flush=True)
    # learn: graft the batch, save the grown tree, and rerun evolution (refit G3c) on it
    parent, length, label, placed = graft(d, names, tip_lin, batch)
    RES.mkdir(parents=True, exist_ok=True)
    (RES / "tree.nwk").write_text(to_newick(parent, length, label))
    root_before = int(np.where(d["parent"] < 0)[0][0])
    leca_before = {fams[j] for j in np.where(post[root_before] >= 0.5)[0]}
    del post, R, post_b, R_b, db, pc, pb, held_prof, held_lin, rel_cache
    import gc
    gc.collect()
    mem("freed before refit")
    lin_all.update({lab: sp["lineage"] for lab, sp in batch.items()})
    prof_all.update({lab: {**sp, "kingdom": "eukaryotes"} for lab, sp in batch.items()})
    d2, fams2, _ = load_tree_rooted(lin_all, prof_all)
    post2, _, info2 = fit_model(d2, fams2, [int(np.where(d2["parent"] < 0)[0][0])])
    mem("refit done")
    root2 = int(np.where(d2["parent"] < 0)[0][0])
    leca_after = {fams2[j] for j in np.where(post2[root2] >= 0.5)[0]}
    summary["evolution_after"] = {"tips": len(d2["tips"]), "m": info2["m"],
                                  "prior_mean_gain_loss_ratio": info2.get("prior_mean_ratio"),
                                  "leca_families_before": len(leca_before), "leca_families_after": len(leca_after),
                                  "leca_gained": sorted(leca_after - leca_before)[:200],
                                  "leca_lost": sorted(leca_before - leca_after)[:200]}
    summary["lesson_next"] = None                     # filled after this round is saved
    (RES / "leca_calls.json").write_text(json.dumps(sorted(leca_after)))
    dest = DATA / "rounds" / f"{k:03d}"
    dest.mkdir(parents=True, exist_ok=True)
    shutil.copy(BATCH / "pick.json", dest / "pick.json")
    shutil.copytree(BATCH / "shards", dest / "shards", dirs_exist_ok=True)
    shutil.rmtree(BATCH)
    summary["grafted"] = len(placed)
    summary["tree_tips_after"] = int(sum(1 for lab in label if lab))
    (RES / f"round_{k:03d}.json").write_text(json.dumps({**summary, "species": rows}, ensure_ascii=False, indent=1))
    st["rounds"].append({k_: summary[k_] for k_ in ("round", "source", "n_scored", "tree_tips_before", "tree_tips_after",
                                                     "mean_auroc", "applied_minus_relatives", "current_minus_relatives",
                                                     "current_minus_base", "applied_minus_current")})
    st["rounds"][-1]["leca_families"] = summary["evolution_after"]["leca_families_after"]
    st["lesson_next"] = lesson_from(st)
    summary["lesson_next"] = st["lesson_next"]
    (RES / f"round_{k:03d}.json").write_text(json.dumps({**summary, "species": rows}, ensure_ascii=False, indent=1))
    (RES / "state.json").write_text(json.dumps(st, ensure_ascii=False, indent=1))
    print(json.dumps({"evolution_after": {k_: v for k_, v in summary["evolution_after"].items()
                                          if k_ not in ("leca_gained", "leca_lost")},
                      "lesson_next": st["lesson_next"]}, ensure_ascii=False, indent=1))


def bootstrap_round1():
    """Before the first loop round: graft round 1 (pre-registration 10) into the base tree, so round 2 is
    predicted by a model that has learned from it. Round 1's own scores are in results/new_species."""
    from run_clade_ancestor import load_profiles as base_loader
    if current_tree():
        print("tree already exists")
        return
    base_prof = base_loader()
    base_lin = {r["organism"].replace("'", ""): r["lineage"]
                for r in json.loads(Path("data/markers/leca2_pick.json").read_text())["lineage"].values()}
    held = all_new_species()
    d, fams, names = load_tree_rooted(base_lin, base_prof)
    names = {v: names[v] for v in d["tips"]}
    tip_lin = {v: set(base_lin.get(names[v], [])) for v in d["tips"]}
    keep = {k_: v for k_, v in held.items() if v["n_proteins"] >= 1000 and len(v["pfam"]) >= 300}
    parent, length, label, placed = graft(d, names, tip_lin, keep)
    RES.mkdir(parents=True, exist_ok=True)
    (RES / "tree.nwk").write_text(to_newick(parent, length, label))
    st = state()
    st["round1"] = {"grafted": len(placed), "tree_tips_after": int(sum(1 for lab in label if lab))}
    (RES / "state.json").write_text(json.dumps(st, ensure_ascii=False, indent=1))
    print(f"grafted {len(placed)} round-1 species; tree now has {st['round1']['tree_tips_after']} tips")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("step", choices=["plan", "fetch", "round", "bootstrap"])
    ap.add_argument("--n", type=int, default=1000)
    ap.add_argument("--shard", type=int, default=0)
    ap.add_argument("--n-shards", type=int, default=20)
    a = ap.parse_args()
    if a.step == "plan":
        plan(a.n, a.n_shards)
    elif a.step == "fetch":
        fetch(a.shard, a.n_shards)
    elif a.step == "bootstrap":
        bootstrap_round1()
    else:
        round_()


if __name__ == "__main__":
    main()
