"""A lineage-spread sample of one kingdom's collected UniProt proteomes, for a marker tree.

    python scripts/pick_clade_sample.py --kingdom fungi --n 300 --set fungi
        -> data/markers/<set>_pick.json  {"upids": [...], "lineage": {upid: {...}}, "rule": ...}

Why a spread sample and not the first N: 1,526 fungal proteomes are mostly Dikarya (yeasts,
moulds, mushrooms). Taking them in order would leave the early-diverging lineages (chytrids,
Mucoromycota, Microsporidia, Rozella) with one or two tips, and the node the reconstruction reaches
would be a Dikarya ancestor, not the fungal one (results/sample_size: a subsample never reaches the
clade root by itself). So the sample is drawn round-robin over orders: every order gets its best
proteome before any order gets a second one.

"Best" is the proteome with the most Pfam families in its order, a proxy for completeness.
Lineage comes from UniProt's taxonomy endpoint (not reachable from the sandbox; run on Actions).
"""

import argparse
import gzip
import json
import sys
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from uniprot_proteomes import REST, get  # noqa: E402

RANKS = ("phylum", "subphylum", "class", "order", "family")


def ranks_of(entry):
    """{rank: name} from a UniProt taxonomy JSON entry; lineage items are dicts or 'Name (rank)'."""
    out = {}
    for it in entry.get("lineage", []) + [entry]:
        if isinstance(it, dict):
            name, rank = it.get("scientificName"), (it.get("rank") or "").lower()
        else:
            s = str(it)
            name, _, rank = s.rpartition(" (")
            rank = rank.rstrip(")").lower()
        if name and rank in RANKS:
            out[rank] = name
    return out


def lineage(taxid):
    return ranks_of(json.loads(get(f"{REST}/taxonomy/{taxid}?format=json", tries=4)))


def pick(rows, lin, n):
    """Round-robin over orders, best (most families) first within each order."""
    by_order = defaultdict(list)
    for upid, r in rows.items():
        L = lin.get(upid, {})
        key = (L.get("phylum", "?"), L.get("class", "?"), L.get("order", "?"))
        by_order[key].append((-r["n_families"], r["organism"], upid))
    for v in by_order.values():
        v.sort()
    keys = sorted(by_order)
    chosen, k = [], 0
    while len(chosen) < n and any(len(by_order[o]) > k for o in keys):
        for o in keys:
            if len(by_order[o]) > k and len(chosen) < n:
                chosen.append(by_order[o][k][2])
        k += 1
    return chosen, len(keys)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--kingdom", required=True)
    ap.add_argument("--n", type=int, default=300)
    ap.add_argument("--set", required=True)
    ap.add_argument("--min-families", type=int, default=500,
                    help="skip near-empty proteomes when choosing the order's representative")
    args = ap.parse_args()

    rows = {}
    for f in sorted(Path("data/uniprot/shards").glob("*.json.gz")):
        for upid, p in json.loads(gzip.open(f, "rt").read()).items():
            if p.get("kingdom") != args.kingdom or not p.get("pfam"):
                continue
            nf = len(p["pfam"])
            if upid not in rows or nf > rows[upid]["n_families"]:
                rows[upid] = {"organism": p["organism"], "taxid": p["taxid"], "n_families": nf}
    print(f"{len(rows)} {args.kingdom} proteomes collected")
    taxids = sorted({r["taxid"] for r in rows.values()})
    with ThreadPoolExecutor(8) as ex:
        got = dict(zip(taxids, ex.map(lambda t: _safe(lineage, t), taxids)))
    lin = {u: got.get(r["taxid"]) or {} for u, r in rows.items()}
    missing = sum(1 for v in lin.values() if not v.get("order"))
    print(f"lineage found for {len(rows) - missing}/{len(rows)} (no order rank: {missing})")
    by_order = defaultdict(list)
    for u, r in rows.items():
        by_order[lin[u].get("order", "?")].append(r["n_families"])
    # Very reduced genomes (Microsporidia) are real biology, not low quality: keep them eligible
    # when they are the only members of their order, by relaxing the floor to 100 for those.
    eligible = {u: r for u, r in rows.items()
                if r["n_families"] >= args.min_families
                or max(by_order[lin[u].get("order", "?")]) < args.min_families and r["n_families"] >= 100}
    chosen, n_orders = pick(eligible, lin, args.n)
    phyla = defaultdict(int)
    for u in chosen:
        phyla[lin[u].get("phylum", "?")] += 1
    print(f"picked {len(chosen)} from {n_orders} orders; per phylum: {dict(sorted(phyla.items()))}")
    out = Path("data/markers") / f"{args.set}_pick.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps({
        "kingdom": args.kingdom, "upids": chosen,
        "lineage": {u: {**lin[u], "organism": rows[u]["organism"], "n_families": rows[u]["n_families"]}
                    for u in chosen},
        "per_phylum": dict(sorted(phyla.items())), "orders": n_orders,
        "rule": f"round-robin over (phylum, class, order), most Pfam families first; floor "
                f"{args.min_families} families unless the whole order is below it (then 100)",
    }, indent=1))
    print(f"-> {out}")


def _safe(fn, x):
    try:
        return fn(x)
    except Exception as e:
        print(f"  lineage {x}: {e}", flush=True)
        return None


if __name__ == "__main__":
    main()
