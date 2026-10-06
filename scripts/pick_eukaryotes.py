"""A supergroup-balanced sample of eukaryote proteomes for the LECA reconstruction, picked BEFORE
fetching, so thousands of animal and plant proteomes are not downloaded to be thrown away.

    python scripts/pick_eukaryotes.py --n 300 --set leca --n-shards 12
        -> data/markers/leca_pick.json   chosen proteomes, full lineage, supergroup
        -> data/uniprot/proteomes.tsv, data/uniprot/todo.json   the ones not collected yet
        -> last stdout line: the shard matrix for public-genomes.yml's fetch job

Why balanced by supergroup: the last eukaryotic common ancestor (LECA) sits where the supergroups
meet. UniProt has thousands of animal, plant and fungal proteomes and a handful for Metamonada,
Cryptophyta or Haptista; a sample proportional to UniProt would reconstruct an opisthokont. Each
supergroup gets an equal share (unused shares go round-robin to the others), and within one the
share is spread round-robin over the next two lineage levels, best BUSCO first.

Supergroups follow NCBI taxonomy names, so the assignment is reproducible from the lineage alone.
Run on Actions (UniProt is not reachable from the sandbox).
"""

import argparse
import gzip
import json
import re
import sys
import urllib.parse
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from uniprot_proteomes import COLS, REST, get  # noqa: E402

SUPERGROUPS = ["Metazoa", "Fungi", "Choanoflagellata", "Ichthyosporea", "Filasterea", "Rotosphaerida",
               "Amoebozoa", "Apusozoa", "Breviatea", "Viridiplantae", "Rhodophyta", "Glaucocystophyceae",
               "Stramenopiles", "Alveolata", "Rhizaria", "Haptista", "Cryptophyceae", "Discoba",
               "Metamonada", "Ancyromonadida", "Malawimonadida", "CRuMs", "Hemimastigophora",
               "Telonemida", "Picozoa"]
# Reference proteomes everywhere, plus every proteome outside the three big kingdoms, where
# reference proteomes are too few.
QUERIES = ["reference:true AND taxonomy_id:2759",
           "taxonomy_id:2759 NOT taxonomy_id:33208 NOT taxonomy_id:33090 NOT taxonomy_id:4751"]


def lineage_names(taxid):
    """Root-first list of lineage names (the organism itself last)."""
    e = json.loads(get(f"{REST}/taxonomy/{taxid}?format=json", tries=4))
    names = []
    for it in e.get("lineage", []):
        names.append(it.get("scientificName") if isinstance(it, dict) else str(it).rsplit(" (", 1)[0])
    names = [n for n in names if n]
    if "Eukaryota" in names and names.index("Eukaryota") > len(names) / 2:
        names.reverse()
    return names + [e.get("scientificName", "")]


def supergroup(names):
    for g in SUPERGROUPS:
        if g in names:
            return g
    return None


def busco_c(s):
    m = re.search(r"C:([\d.]+)%", s or "")
    return float(m.group(1)) if m else None


def balanced(cands, n):
    """cands: {group: {key: [(sortkey, upid), ...]}} -> chosen upids, equal shares per group."""
    queues = {}
    for g, by_key in cands.items():
        for v in by_key.values():
            v.sort()
        keys, q, k = sorted(by_key), [], 0
        while any(len(by_key[x]) > k for x in keys):
            q += [by_key[x][k][1] for x in keys if len(by_key[x]) > k]
            k += 1
        queues[g] = q
    chosen, i = [], 0
    while len(chosen) < n and any(len(q) > i for q in queues.values()):
        for g in sorted(queues):
            if len(queues[g]) > i and len(chosen) < n:
                chosen.append(queues[g][i])
        i += 1
    return chosen


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", type=int, default=300)
    ap.add_argument("--set", default="leca")
    ap.add_argument("--n-shards", type=int, default=12)
    ap.add_argument("--min-busco", type=float, default=60.0)
    args = ap.parse_args()

    rows = {}
    for q in QUERIES:
        text = get(f"{REST}/proteomes/stream?query={urllib.parse.quote(q)}&format=tsv"
                   "&fields=upid,organism,organism_id,protein_count,busco")
        for ln in text.strip().split("\n")[1:]:
            upid, org, tid, n, busco = (ln.split("\t") + [""] * 5)[:5]
            if upid and int(n or 0) >= 1000:
                rows[upid] = {"upid": upid, "organism": org, "taxid": tid, "protein_count": n, "busco": busco}
    print(f"{len(rows)} eukaryote proteomes listed (>= 1000 proteins)")
    taxids = sorted({r["taxid"] for r in rows.values()})
    with ThreadPoolExecutor(8) as ex:
        got = dict(zip(taxids, ex.map(lambda t: _safe(lineage_names, t), taxids)))

    # one proteome per species, best BUSCO
    best = {}
    for u, r in rows.items():
        names = got.get(r["taxid"]) or []
        g = supergroup(names)
        if not g:
            continue
        sp = " ".join(r["organism"].split()[:2]).lower()
        c = busco_c(r["busco"])
        score = (c if c is not None else -1, int(r["protein_count"] or 0))
        if sp not in best or score > best[sp][0]:
            best[sp] = (score, u, g, names)
    floor_ok = defaultdict(bool)
    for score, u, g, names in best.values():
        floor_ok[g] |= score[0] >= args.min_busco
    cands = defaultdict(lambda: defaultdict(list))
    for score, u, g, names in best.values():
        if floor_ok[g] and 0 <= score[0] < args.min_busco:
            continue   # the group has good proteomes; skip the poor ones (no BUSCO: kept, ranked last)
        i = names.index(g)
        key = tuple(names[i + 1:i + 3])
        cands[g][key].append(((-score[0], -score[1], rows[u]["organism"]), u))
    chosen = balanced(cands, args.n)
    per = defaultdict(int)
    lin = {}
    for score, u, g, names in best.values():
        if u in set(chosen):
            per[g] += 1
            lin[u] = {"organism": rows[u]["organism"], "supergroup": g, "lineage": names, "busco": rows[u]["busco"]}
    print(f"picked {len(chosen)}; per supergroup: {dict(sorted(per.items()))}")

    collected = set()
    for f in Path("data/uniprot/shards").glob("*.json.gz"):
        collected |= set(json.loads(gzip.open(f, "rt").read()))
    todo = [u for u in chosen if u not in collected]
    Path("data/uniprot").mkdir(parents=True, exist_ok=True)
    with (Path("data/uniprot") / "proteomes.tsv").open("w") as f:
        f.write("\t".join(COLS) + "\n")
        for u in todo:
            r = {**rows[u], "kingdom": "fungi" if lin[u]["supergroup"] == "Fungi" else "eukaryotes",
                 "assembly": ""}
            f.write("\t".join(str(r.get(k, "")) for k in COLS) + "\n")
    (Path("data/uniprot") / "todo.json").write_text(json.dumps(todo))
    out = Path("data/markers") / f"{args.set}_pick.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps({"upids": chosen, "lineage": lin, "per_supergroup": dict(sorted(per.items())),
                               "rule": f"equal share per supergroup, round-robin over the next two lineage "
                                       f"levels, best BUSCO first; BUSCO C >= {args.min_busco} where the "
                                       f"group has any"}, indent=1))
    print(f"{len(todo)} to fetch, {len(chosen) - len(todo)} already collected -> {out}")
    n = max(1, min(args.n_shards, len(todo)))
    print(json.dumps(list(range(n))) if todo else "[]")


def _safe(fn, x):
    try:
        return fn(x)
    except Exception as e:
        print(f"  lineage {x}: {e}", flush=True)
        return None


if __name__ == "__main__":
    main()
