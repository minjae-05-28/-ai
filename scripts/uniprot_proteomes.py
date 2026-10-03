"""Pfam family counts and amino-acid composition for every UniProt reference proteome of a
kingdom, from UniProt's own precomputed Pfam cross-references (no HMMER run here).
Run by .github/workflows/uniprot-proteomes.yml (UniProt is not reachable from the sandbox).

    python scripts/uniprot_proteomes.py --list bacteria,archaea,fungi [--limit N]
    python scripts/uniprot_proteomes.py --list patescibacteria,asgard,omnitrophota   # all proteomes, 1/species
        -> data/uniprot/proteomes.tsv and prints the shard matrix as JSON
    python scripts/uniprot_proteomes.py --shard 3 --n-shards 40
        -> data/uniprot/shards/shard_003.json.gz

Scale: the profiles made with HMMER in this project take minutes to an hour per species, so
tens of thousands of genomes are only reachable through annotations someone has already
computed. UniProt annotates Pfam on every reference proteome (InterPro); a reference proteome
is one per species or strain chosen as representative.

Shard output: {upid: {"organism", "taxid", "kingdom", "n_proteins", "pfam": {name: n_genes},
"composition": proteome_stats(...)}} with Pfam names mapped from accessions through
data/eukaryotes/pfam_meta.json, so the counts read like the HMMER profiles (genes per family).
Differences from the HMMER profiles: UniProt keeps every protein entry (no longest-isoform
step, which matters for fungi, not prokaryotes) and uses InterPro's Pfam release.
"""

import argparse
import gzip
import io
import json
import time
import urllib.parse
import urllib.request
from pathlib import Path

OUT = Path("data/uniprot")
TAXA = {"bacteria": 2, "archaea": 2157, "fungi": 4751}
REST = "https://rest.uniprot.org"
COLS = ("upid", "organism", "taxid", "protein_count", "busco", "kingdom", "assembly")


def get(url, tries=6):
    for i in range(tries):
        try:
            req = urllib.request.Request(url, headers={"Accept-Encoding": "gzip", "User-Agent": "organelle-evo"})
            with urllib.request.urlopen(req, timeout=300) as r:
                data = r.read()
                while data[:2] == b"\x1f\x8b":  # UniProt can gzip twice (transfer + compressed=true)
                    data = gzip.decompress(data)
                return data.decode()
        except Exception as e:  # network hiccups and 429/5xx: back off and retry
            print(f"  retry {i + 1}/{tries} {url[:90]}: {e}", flush=True)
            time.sleep(10 * (i + 1))
    raise RuntimeError(f"failed: {url}")


# Lineages known mostly from metagenome-assembled genomes: few or no *reference* proteomes, so all
# proteomes are listed and one per species is kept (highest BUSCO completeness).
GROUPS = {"patescibacteria": (1783273, "bacteria"), "asgard": (1935183, "archaea"),
          "omnitrophota": (1817898, "bacteria")}


def list_group_proteomes(groups, limit):
    import re as _re

    rows = []
    for gname in groups:
        taxid, kingdom = GROUPS[gname]
        q = urllib.parse.quote(f"taxonomy_id:{taxid}")
        base = f"{REST}/proteomes/stream?query={q}&format=tsv&fields=upid,organism,organism_id,protein_count,busco"
        try:  # the assembly accession links a proteome to its GTDB tip exactly; older field sets lack it
            text = get(base + ",genome_assembly", tries=2)
        except RuntimeError:
            text = get(base)
        lines = [ln for ln in text.strip().split("\n")[1:] if ln]
        if not lines:
            print(f"::warning::{gname} (taxid {taxid}): UniProt listed no proteomes; reply starts {text[:200]!r}")
            continue
        best = {}
        for ln in lines:
            upid, org, tid, n, busco, asm = (ln.split("\t") + [""] * 6)[:6]
            words = org.replace("Candidatus ", "").split()
            # Unnamed MAGs ("X bacterium <strain>") are distinct species: keep the full name as the key.
            unnamed = len(words) > 1 and words[1].lower() in ("bacterium", "archaeon", "sp.", "sp")
            sp = org.lower() if unnamed else " ".join(words[:2]).lower()
            m = _re.search(r"C:([\d.]+)%", busco)
            c = float(m.group(1)) if m else 0.0
            if sp not in best or c > best[sp][0]:
                best[sp] = (c, {"upid": upid, "organism": org, "taxid": tid, "protein_count": n, "busco": busco,
                                "kingdom": kingdom, "assembly": asm.split(";")[0].strip() if asm else ""})
        kept = [r for _, r in best.values()][: limit or None]
        rows += kept
        print(f"{gname}: {len(lines)} proteomes, {len(best)} species, keeping {len(kept)}", flush=True)
    return rows


def list_proteomes(kingdoms, limit):
    """Reference proteomes per kingdom. `reference:true` is the working filter: the
    `proteome_type:1` form returns an empty table without error (results/external/uniprot_probe.json)."""
    rows = []
    for k in kingdoms:
        q = urllib.parse.quote(f"reference:true AND taxonomy_id:{TAXA[k]}")
        text = get(f"{REST}/proteomes/stream?query={q}&format=tsv&fields=upid,organism,organism_id,protein_count,busco")
        lines = [ln for ln in text.strip().split("\n")[1:] if ln]
        if not lines:
            raise SystemExit(f"{k}: UniProt listed no reference proteomes; reply starts {text[:300]!r}")
        for ln in lines[: limit or None]:
            upid, org, taxid, n, busco = (ln.split("\t") + [""] * 5)[:5]
            rows.append({"upid": upid, "organism": org, "taxid": taxid, "protein_count": n, "busco": busco,
                         "kingdom": k})
        print(f"{k}: {len(lines)} reference proteomes (keeping {min(len(lines), limit or len(lines))})", flush=True)
    return rows


def profile(upid, name_of):
    from organelle_evo.sequence import proteome_stats

    q = urllib.parse.quote(f"proteome:{upid}")
    text = get(f"{REST}/uniprotkb/stream?query={q}&format=tsv&fields=accession,xref_pfam,sequence&compressed=true")
    pfam, seqs = {}, []
    for ln in io.StringIO(text).read().split("\n")[1:]:
        if not ln:
            continue
        parts = ln.split("\t")
        if len(parts) < 3:
            continue
        seqs.append(parts[2])
        for acc in {a for a in parts[1].split(";") if a}:
            name = name_of.get(acc, acc)
            pfam[name] = pfam.get(name, 0) + 1
    return {"n_proteins": len(seqs), "pfam": pfam, "composition": proteome_stats(seqs) if seqs else None}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--list")
    ap.add_argument("--limit", type=int, default=0, help="per kingdom, for a test run")
    ap.add_argument("--shard", type=int)
    ap.add_argument("--n-shards", type=int, default=40)
    args = ap.parse_args()
    OUT.mkdir(parents=True, exist_ok=True)
    table = OUT / "proteomes.tsv"
    if args.list:
        names = args.list.split(",")
        rows = list_proteomes([n for n in names if n in TAXA], args.limit)
        rows += list_group_proteomes([n for n in names if n in GROUPS], args.limit)
        with table.open("w") as f:
            f.write("\t".join(COLS) + "\n")
            for r in rows:
                f.write("\t".join(r.get(k, "") for k in COLS) + "\n")
        done = set()
        for p in (OUT / "shards").glob("*.json.gz"):
            done |= set(json.loads(gzip.open(p, "rt").read()))
        todo = [r for r in rows if r["upid"] not in done]
        n = max(1, min(args.n_shards, len(todo)))
        print(json.dumps(list(range(n))) if todo else "[]")
        (OUT / "todo.json").write_text(json.dumps([r["upid"] for r in todo]))
        return

    meta = json.loads(Path("data/eukaryotes/pfam_meta.json").read_text())
    name_of = {v["accession"].split(".")[0]: k for k, v in meta.items()}
    rows = {r["upid"]: r for r in (dict(zip(COLS, ln.split("\t") + [""] * len(COLS)))
                                   for ln in table.read_text().strip().split("\n")[1:])}
    todo = json.loads((OUT / "todo.json").read_text())
    mine = todo[args.shard :: args.n_shards]
    out = {}
    t0 = time.time()
    for i, upid in enumerate(mine):
        try:
            p = profile(upid, name_of)
        except Exception as e:
            print(f"  skip {upid}: {e}", flush=True)
            continue
        r = rows[upid]
        out[upid] = {"organism": r["organism"], "taxid": r["taxid"], "kingdom": r["kingdom"], "busco": r["busco"],
                      "assembly": r.get("assembly", ""), **p}
        if i % 25 == 0:
            print(f"  {i + 1}/{len(mine)} {r['organism']}: {p['n_proteins']} proteins, {len(p['pfam'])} families "
                  f"({time.time() - t0:.0f}s)", flush=True)
    (OUT / "shards").mkdir(exist_ok=True)
    dest = OUT / "shards" / f"part_{int(time.time())}_{args.shard:03d}.json.gz"
    with gzip.open(dest, "wt") as f:
        json.dump(out, f)
    print(f"{len(out)} proteomes -> {dest}")


if __name__ == "__main__":
    main()
