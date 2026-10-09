"""Gene trees for the families of pre-registration 6 (docs/preregistration/2026-10-09_gene_trees.md).

Run on Actions (.github/workflows/gene-trees.yml); UniProt and the Pfam HMMs are not reachable here.

    python scripts/gene_trees.py panel   -> data/gene_trees/panel.json  (run locally, committed in advance)
        eukaryotes: the leca2 pick (supergroup, Amorphea side); prokaryotes: 100 bacteria and 30 archaea from
        the collected UniProt proteomes, round-robin over GTDB phyla (then class, order), richest first
    python scripts/gene_trees.py fetch --shard i --n-shards N   -> work/seqs_<i>.json.gz
        per proteome, the proteins carrying any selected Pfam (UniProt query, batches of 40 families)
    python scripts/gene_trees.py build --shard j --n-shards M --pfam pfam/Pfam-A.hmm
        -> results/gene_trees/part_<j>.json (+ trees/<family>.nwk)
        per family: best-scoring domain envelope per protein (hmmsearch, i-Evalue < 1e-5), at most two
        per proteome; hmmalign to the family HMM, match columns only; columns with > 50% gaps dropped,
        then sequences with < 30% residues left; FastTree -lg -gamma (SH-like local supports)
    python scripts/gene_trees.py analyze  -> results/gene_trees/summary.json

Nothing here writes or designs a sequence; sequences are read from UniProt, aligned and discarded.
Only trees and per-family counts are kept.
"""

import argparse
import gzip
import json
import shutil
import subprocess
import sys
import tempfile
import urllib.parse
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))

FAMS = Path("data/gene_trees/families.json")
PANEL = Path("data/gene_trees/panel.json")
OUT = Path("results/gene_trees")
WORK = Path("work")
AMORPHEA = {"Opisthokonta", "Amoebozoa", "Apusozoa", "Breviatea"}
SUPPORT = 0.9


# ---------------------------------------------------------------- panel and download
def gtdb_lineages():
    """NCBI taxid and genus name -> (phylum, class, order) from the GTDB species representatives."""
    by_taxid, by_genus = {}, {}
    with gzip.open("data/gtdb/species_reps.tsv.gz", "rt") as f:
        head = f.readline().rstrip("\n").split("\t")
        i_tax, i_t1, i_t2, i_name = (head.index(k) for k in ("gtdb_taxonomy", "ncbi_taxid", "ncbi_species_taxid",
                                                              "ncbi_organism_name"))
        for ln in f:
            r = ln.rstrip("\n").split("\t")
            ranks = dict(x.split("__", 1) for x in r[i_tax].split(";") if "__" in x)
            lin = (ranks.get("p", "?"), ranks.get("c", "?"), ranks.get("o", "?"))
            by_taxid.setdefault(r[i_t1], lin)
            by_taxid.setdefault(r[i_t2], lin)
            by_genus.setdefault(r[i_name].split()[0], lin)
    return by_taxid, by_genus


def pick_prokaryotes(kingdom, n, floor):
    """Round-robin over GTDB phyla (then class, order), richest proteome first; deterministic."""
    by_taxid, by_genus = gtdb_lineages()
    rows = {}
    for f in sorted(Path("data/uniprot/shards").glob("*.json.gz")):
        for upid, p in json.loads(gzip.open(f, "rt").read()).items():
            if p.get("kingdom") != kingdom or not p.get("pfam") or len(p["pfam"]) < floor:
                continue
            lin = by_taxid.get(str(p.get("taxid"))) or by_genus.get(p["organism"].split()[0])
            if lin and (upid not in rows or len(p["pfam"]) > rows[upid][0]):
                rows[upid] = (len(p["pfam"]), p["organism"], lin)
    by_phylum = {}
    for upid, (nf, org, lin) in rows.items():
        by_phylum.setdefault(lin[0], []).append((lin[1], lin[2], -nf, org, upid))
    queues = {}
    for ph, lst in by_phylum.items():
        # within a phylum: one per order (class-ordered), richest first, then second round
        by_order = {}
        for c, o, nf, org, upid in sorted(lst):
            by_order.setdefault((c, o), []).append((nf, org, upid))
        rounds, k = [], 0
        while any(len(v) > k for v in by_order.values()):
            rounds += [sorted(v)[k][2] for key, v in sorted(by_order.items()) if len(v) > k]
            k += 1
        queues[ph] = rounds
    chosen, k = [], 0
    phyla = sorted(queues, key=lambda p: -len(queues[p]))      # big phyla first within each round
    while len(chosen) < n and any(len(q) > k for q in queues.values()):
        for ph in phyla:
            if len(queues[ph]) > k and len(chosen) < n:
                chosen.append(queues[ph][k])
        k += 1
    return {u: {"domain": "P", "kingdom": kingdom, "organism": rows[u][1], "gtdb": list(rows[u][2])} for u in chosen}


def make_panel(n_bact=100, n_arch=30):
    euk = json.loads(Path("data/markers/leca2_pick.json").read_text())
    panel = {}
    for upid, r in euk["lineage"].items():
        panel[upid] = {"domain": "E", "organism": r["organism"], "supergroup": r["supergroup"],
                       "amorphea": bool(AMORPHEA & set(r["lineage"]))}
    panel.update(pick_prokaryotes("bacteria", n_bact, 1000))
    panel.update(pick_prokaryotes("archaea", n_arch, 500))
    PANEL.parent.mkdir(parents=True, exist_ok=True)
    PANEL.write_text(json.dumps(panel, indent=1))
    ph = {}
    for v in panel.values():
        if v["domain"] == "P":
            ph[v["gtdb"][0]] = ph.get(v["gtdb"][0], 0) + 1
    n_e = sum(v["domain"] == "E" for v in panel.values())
    print(f"panel: {n_e} eukaryote, {len(panel) - n_e} prokaryote proteomes from {len(ph)} phyla: {ph}")


def fetch(shard, n_shards):
    from uniprot_proteomes import REST, get
    accs = [f["accession"] for f in json.loads(FAMS.read_text())["families"]]
    upids = sorted(json.loads(PANEL.read_text()))[shard::n_shards]
    batches = [accs[i:i + 40] for i in range(0, len(accs), 40)]

    def one(upid):
        rows = []
        for b in batches:
            q = urllib.parse.quote(f"proteome:{upid} AND (" + " OR ".join(f"xref:pfam-{a}" for a in b) + ")")
            text = get(f"{REST}/uniprotkb/stream?query={q}&format=tsv&fields=accession,xref_pfam,sequence"
                       f"&compressed=true")
            for ln in text.split("\n")[1:]:
                parts = ln.split("\t")
                if len(parts) == 3 and parts[2]:
                    rows.append([parts[0], [a for a in parts[1].split(";") if a], parts[2]])
        seen, out = set(), []
        for r in rows:                        # a protein with two selected families comes back twice
            if r[0] not in seen:
                seen.add(r[0])
                out.append(r)
        return upid, out

    res = {}
    with ThreadPoolExecutor(6) as ex:
        for k, (upid, rows) in enumerate(ex.map(one, upids)):
            res[upid] = rows
            print(f"  {k + 1}/{len(upids)} {upid}: {len(rows)} proteins", flush=True)
    WORK.mkdir(exist_ok=True)
    with gzip.open(WORK / f"seqs_{shard}.json.gz", "wt") as f:
        json.dump(res, f)


# ---------------------------------------------------------------- one family's tree
def build(shard, n_shards, pfam_path):
    import pyhmmer
    fams = json.loads(FAMS.read_text())["families"][shard::n_shards]
    want = {f["accession"] for f in fams}
    hmms = {}
    with pyhmmer.plan7.HMMFile(pfam_path) as hf:
        for h in hf:
            if h.accession is None:
                continue
            a = (h.accession.decode() if isinstance(h.accession, bytes) else h.accession).split(".")[0]
            if a in want:
                hmms[a] = h
    seqs = {}
    for p in sorted(WORK.glob("seqs_*.json.gz")):
        seqs.update(json.loads(gzip.open(p, "rt").read()))
    panel = json.loads(PANEL.read_text())
    alphabet = pyhmmer.easel.Alphabet.amino()
    (OUT / "trees").mkdir(parents=True, exist_ok=True)
    results = {}
    for f in fams:
        a = f["accession"]
        if a not in hmms:
            results[f["family"]] = {"skipped": "HMM not in this Pfam release"}
            continue
        names, texts = [], []
        for upid, rows in seqs.items():
            for acc, pf, s in rows:
                if a in pf:
                    names.append(f"{upid}|{acc}")
                    texts.append(s)
        if not texts:
            results[f["family"]] = {"skipped": "no sequences"}
            continue
        dig = [pyhmmer.easel.TextSequence(name=n.encode(), sequence=s).digitize(alphabet)
               for n, s in zip(names, texts)]
        best = {}
        for hits in pyhmmer.hmmer.hmmsearch([hmms[a]], pyhmmer.easel.DigitalSequenceBlock(alphabet, dig), cpus=4):
            for hit in hits:
                doms = [d for d in hit.domains if d.i_evalue < 1e-5]
                if not doms:
                    continue
                d = max(doms, key=lambda x: x.score)
                n = hit.name.decode() if isinstance(hit.name, bytes) else hit.name
                best[n] = (d.score, d.env_from, d.env_to)
        by_prot = {}
        for n, (sc, s0, s1) in best.items():
            by_prot.setdefault(n.split("|")[0], []).append((sc, n, s0, s1))
        keep = []
        for upid, lst in by_prot.items():
            keep += sorted(lst, reverse=True)[:2]
        text_of = dict(zip(names, texts))
        dom = [pyhmmer.easel.TextSequence(name=n.encode(), sequence=text_of[n][s0 - 1:s1]).digitize(alphabet)
               for _, n, s0, s1 in keep]
        n_e = sum(panel[k[1].split("|")[0]]["domain"] == "E" for k in keep)
        if n_e < 4 or len(keep) - n_e < 4:
            results[f["family"]] = {"skipped": f"too few sequences ({n_e} eukaryote, {len(keep) - n_e} prokaryote)"}
            continue
        msa = pyhmmer.hmmer.hmmalign(hmms[a], dom, trim=True, all_consensus_cols=True)
        rows = {}
        for nm, al in zip(msa.names, msa.alignment):
            nm = nm.decode() if isinstance(nm, bytes) else nm
            rows[nm] = "".join(c for c in al if not (c.islower() or c == "."))
        aln = trim(rows)
        if len(aln) < 8:
            results[f["family"]] = {"skipped": "alignment too short after trimming"}
            continue
        with tempfile.NamedTemporaryFile("w", suffix=".fa", delete=False) as tmp:
            for i, (nm, s) in enumerate(aln.items()):
                tmp.write(f">s{i}\n{s}\n")
        ids = {f"s{i}": nm for i, nm in enumerate(aln)}
        ft = shutil.which("FastTree") or shutil.which("fasttree")
        nwk = subprocess.run([ft, "-lg", "-gamma", "-quiet", tmp.name], capture_output=True, text=True,
                             check=True).stdout
        for k, nm in ids.items():
            nwk = nwk.replace(f"{k}:", f"{nm}:")
        (OUT / "trees" / f"{f['family']}.nwk").write_text(nwk)
        tags = {nm: panel[nm.split("|")[0]] for nm in aln}
        results[f["family"]] = {**metrics(nwk, tags), "n_sequences": len(aln),
                                "n_columns": len(next(iter(aln.values())))}
        print(f"  {f['family']}: {results[f['family']]}", flush=True)
    (OUT / f"part_{shard}.json").write_text(json.dumps(results, indent=1))


def trim(rows, max_gap=0.5, min_res=0.3):
    names = list(rows)
    if not names:
        return {}
    L = len(rows[names[0]])
    arr = np.array([list(rows[n]) for n in names])
    keep_col = (arr == "-").mean(0) <= max_gap
    arr = arr[:, keep_col]
    if arr.shape[1] == 0:
        return {}
    ok = (arr != "-").mean(1) >= min_res
    assert L >= arr.shape[1]
    return {n: "".join(arr[i]) for i, n in enumerate(names) if ok[i]}


# ---------------------------------------------------------------- tree metrics (unit-tested)
def metrics(nwk, tags, support=SUPPORT):
    """Per-family counts on a gene tree whose leaves are tagged {domain: E|P, supergroup, amorphea}.

    Rooted on the prokaryote leaf farthest (mean path length) from the eukaryote leaves.
    K_raw: number of maximal eukaryote-only clades.
    K_sup: the same after collapsing internal nodes with support < `support`: at each node that holds
           both domains, its eukaryote-only children could be joined into one clade by resolving the
           polytomy, so K_sup counts mixed nodes with at least one eukaryote-only child.
    leca_like: the largest eukaryote group (collapsed tree) holds tips from both sides of the
           Amorphea | rest split and from at least three supergroups.
    prok_nearest: share of eukaryote leaves whose nearest leaf (path length) is a prokaryote.
    """
    from run_clade_ancestor import farthest_outgroup_tip, reroot
    from run_mito_ancestor import parse_newick, postorder

    parent, length, label = parse_newick(nwk.strip())
    order, children = postorder(parent)
    tips = [v for v in range(len(parent)) if not children[v]]
    is_e = {v: tags[label[v]]["domain"] == "E" for v in tips}
    t = farthest_outgroup_tip(parent, np.maximum(length, 1e-6), set(tips), is_e)
    sup_label = {v: label[v] for v in range(len(parent)) if children[v]}
    # keep supports through rerooting by tagging internal nodes with unique names
    tagged = [label[v] if not children[v] else f"__n{v}" for v in range(len(parent))]
    parent, length, lab2 = reroot(parent, np.maximum(length, 1e-6), tagged, t)
    order, children = postorder(parent)
    sup = np.ones(len(parent))
    for v in range(len(parent)):
        if children[v] and lab2[v].startswith("__n"):
            try:
                sup[v] = float(sup_label[int(lab2[v][3:])] or 1.0)
            except ValueError:
                sup[v] = 1.0
    tips = [v for v in range(len(parent)) if not children[v]]
    tag = {v: tags[lab2[v]] for v in tips}
    # collapse: children of a node with low support are lifted to the parent
    eff_children = {}

    def lifted(v):
        out = []
        for c in children[v]:
            if children[c] and sup[c] < support:
                out += lifted(c)
            else:
                out.append(c)
        return out
    for v in range(len(parent)):
        if children[v]:
            eff_children[v] = lifted(v)
    leaves_under = {}
    for v in order:
        leaves_under[v] = [v] if not children[v] else [x for c in children[v] for x in leaves_under[c]]
    pure_e = {v: all(tag[x]["domain"] == "E" for x in leaves_under[v]) for v in leaves_under}
    any_e = {v: any(tag[x]["domain"] == "E" for x in leaves_under[v]) for v in leaves_under}

    def count(childmap, nodes):
        k, groups = 0, []
        for v in nodes:
            if pure_e[v] or not any_e[v]:
                continue
            pe = [c for c in childmap[v] if pure_e[c]]
            if pe:
                k += 1
                groups.append([x for c in pe for x in leaves_under[c]])
        return k, groups
    kept_internal = [v for v in range(len(parent)) if children[v] and (v == 0 or sup[v] >= support)]
    raw_internal = [v for v in range(len(parent)) if children[v]]
    k_raw, _ = count({v: children[v] for v in raw_internal}, raw_internal)
    k_sup, groups = count(eff_children, kept_internal)
    if pure_e[0]:
        k_raw, k_sup, groups = 1, 1, [leaves_under[0]]
    big = max(groups, key=len) if groups else []
    sides = {tag[x]["amorphea"] for x in big}
    sgs = {tag[x]["supergroup"] for x in big}
    # nearest leaf by path length
    dep = np.zeros(len(parent))
    for v in reversed(order):
        if v:
            dep[v] = dep[parent[v]] + length[v]
    anc = {}
    for v in tips:
        path, w = [], v
        while w != -1:
            path.append(w)
            w = parent[w]
        anc[v] = path
    e_tips = [v for v in tips if tag[v]["domain"] == "E"]
    near_p = 0
    anc_set = {v: set(p) for v, p in anc.items()}
    for v in e_tips:
        best, bd = None, np.inf
        s = anc_set[v]
        for w in tips:
            if w == v:
                continue
            m = next(x for x in anc[w] if x in s)
            d = dep[v] + dep[w] - 2 * dep[m]
            if d < bd:
                best, bd = w, d
        near_p += tag[best]["domain"] == "P"
    return {"K_raw": int(k_raw), "K_sup": int(k_sup), "leca_like": bool(len(sides) == 2 and len(sgs) >= 3),
            "largest_group_supergroups": len(sgs), "n_eukaryote_leaves": len(e_tips),
            "prok_nearest": round(near_p / max(len(e_tips), 1), 4)}


# ---------------------------------------------------------------- pre-registered analysis
def analyze():
    from scipy.stats import rankdata
    fams = {f["family"]: f for f in json.loads(FAMS.read_text())["families"]}
    res = {}
    for p in sorted(OUT.glob("part_*.json")):
        res.update(json.loads(p.read_text()))
    done = [k for k, v in res.items() if "K_sup" in v]
    skipped = {k: v["skipped"] for k, v in res.items() if "skipped" in v}
    y = np.array([fams[k]["vosseberg_leca"] for k in done])
    bact = np.array([fams[k]["bacteria_share"] for k in done])
    lf = np.log(np.array([fams[k]["eukaryote_frequency"] for k in done]) + 1e-3)
    ksup2 = np.array([res[k]["K_sup"] >= 2 for k in done], float)
    kraw2 = np.array([res[k]["K_raw"] >= 2 for k in done], float)

    def resid(v, x):
        r, xr = rankdata(v), rankdata(x)
        b = np.polyfit(xr, r, 1)
        return r - np.polyval(b, xr)

    def pcor(a, b, ix):
        ra, rb = resid(a[ix], lf[ix]), resid(b[ix], lf[ix])
        if ra.std() == 0 or rb.std() == 0:
            return np.nan
        return float(np.corrcoef(ra, rb)[0, 1])
    rng = np.random.default_rng(0)
    n = len(done)
    allix = np.arange(n)
    stats = {"bact~Ksup2": (bact, ksup2), "bact~Kraw2": (bact, kraw2)}
    out = {"n_families_with_tree": n, "n_skipped": len(skipped), "skipped": skipped}
    for name, (a, b) in stats.items():
        bs = [pcor(a, b, rng.integers(0, n, n)) for _ in range(2000)]
        lo, hi = np.nanpercentile(bs, [2.5, 97.5])
        out[name] = {"partial_spearman": round(pcor(a, b, allix), 4), "ci95": [round(float(lo), 4), round(float(hi), 4)]}
    s, r = out["bact~Ksup2"]["ci95"], out["bact~Kraw2"]["ci95"]
    if s[0] > 0:
        out["verdict"] = "해석 1 지지: 세균에 흔할수록 '확실히 갈라진' 진핵 기원이 늘어남 (수평이동)"
    elif s[0] <= 0 <= s[1] and r[0] > 0:
        out["verdict"] = "해석 2 지지: 늘어나는 것은 불확실한 끼어듦뿐 (나무 그리기의 착시)"
    else:
        out["verdict"] = "판정 불가"
    # Q1 replication: our supported multiple origins vs their labels
    out["Q1_share_Ksup2"] = {"vosseberg_leca": round(float(ksup2[y].mean()), 4),
                             "vosseberg_not_leca": round(float(ksup2[~y].mean()), 4)}
    bs = []
    for _ in range(2000):
        ix = rng.integers(0, n, n)
        yy, kk = y[ix], ksup2[ix]
        if yy.all() or (~yy).all():
            continue
        bs.append(kk[~yy].mean() - kk[yy].mean())
    lo, hi = np.percentile(bs, [2.5, 97.5])
    out["Q1_share_Ksup2"]["not_minus_leca_ci95"] = [round(float(lo), 4), round(float(hi), 4)]
    leca_like = np.array([res[k]["leca_like"] for k in done])
    out["secondary_our_leca_like_vs_theirs"] = {
        "agreement": round(float((leca_like == y).mean()), 4),
        "leca_like_share_in_their_leca": round(float(leca_like[y].mean()), 4),
        "leca_like_share_in_their_not": round(float(leca_like[~y].mean()), 4)}
    out["secondary_prok_nearest_mean"] = {
        "vosseberg_leca": round(float(np.mean([res[k]["prok_nearest"] for k in np.array(done)[y]])), 4),
        "vosseberg_not_leca": round(float(np.mean([res[k]["prok_nearest"] for k in np.array(done)[~y]])), 4)}
    (OUT / "summary.json").write_text(json.dumps(out, ensure_ascii=False, indent=1))
    print(json.dumps({k: v for k, v in out.items() if k != "skipped"}, ensure_ascii=False, indent=1))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("step", choices=["panel", "fetch", "build", "analyze"])
    ap.add_argument("--shard", type=int, default=0)
    ap.add_argument("--n-shards", type=int, default=1)
    ap.add_argument("--pfam", default="pfam/Pfam-A.hmm")
    a = ap.parse_args()
    if a.step == "panel":
        make_panel()
    elif a.step == "fetch":
        fetch(a.shard, a.n_shards)
    elif a.step == "build":
        build(a.shard, a.n_shards, a.pfam)
    else:
        analyze()


if __name__ == "__main__":
    main()
