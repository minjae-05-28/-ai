"""Download Pfam clan membership and GO-slim functions for every Pfam family.

    python scripts/fetch_family_annotations.py --out data/eukaryotes/family_annotations.json

Runs on GitHub Actions (EBI and the Gene Ontology site are not reachable from the
development sandbox). Sources:
  Pfam-A.clans.tsv    family -> clan
  pfam2go             family -> GO terms (InterPro2GO-style mapping maintained by GO)
  go-basic.obo        GO graph, used to map each term up to the generic GO slim
  goslim_generic.obo  the ~70 broad slim categories
"""

import argparse
import gzip
import io
import json
import re
import urllib.request

CLANS = "https://ftp.ebi.ac.uk/pub/databases/Pfam/current_release/Pfam-A.clans.tsv.gz"
PFAM2GO = "https://current.geneontology.org/ontology/external2go/pfam2go"
GO_BASIC = "https://current.geneontology.org/ontology/go-basic.obo"
GO_SLIM = "https://current.geneontology.org/ontology/subsets/goslim_generic.obo"


def get(url: str) -> bytes:
    with urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": "organelle-evo"}), timeout=300) as r:
        return r.read()


def parse_obo(text: str) -> dict[str, dict]:
    """GO id -> {name, namespace, parents} (is_a and part_of edges)."""
    terms, cur = {}, None
    for line in text.splitlines():
        if line == "[Term]":
            cur = {"parents": []}
        elif line.startswith("[") and line != "[Term]":
            cur = None
        elif cur is not None and ": " in line:
            key, val = line.split(": ", 1)
            if key == "id":
                terms[val] = cur
            elif key == "name":
                cur["name"] = val
            elif key == "namespace":
                cur["namespace"] = val
            elif key == "is_a":
                cur["parents"].append(val.split(" ! ")[0])
            elif key == "relationship" and val.startswith("part_of "):
                cur["parents"].append(val.split()[1])
    return terms


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default="data/eukaryotes/family_annotations.json")
    args = ap.parse_args()

    clans = {}
    for line in gzip.decompress(get(CLANS)).decode().splitlines():
        cols = line.split("\t")
        if len(cols) >= 4:
            clans[cols[3]] = cols[2] or None  # pfamA_id -> clan_id

    go = parse_obo(get(GO_BASIC).decode())
    slim_ids = set(parse_obo(get(GO_SLIM).decode())) & set(go)
    ancestors_cache: dict[str, set] = {}

    def ancestors(t: str) -> set:
        if t not in ancestors_cache:
            out = {t}
            for p in go.get(t, {}).get("parents", []):
                out |= ancestors(p)
            ancestors_cache[t] = out
        return ancestors_cache[t]

    fam_go: dict[str, set] = {}
    for line in get(PFAM2GO).decode().splitlines():
        m = re.match(r"Pfam:(PF\d+) (\S+) > .* ; (GO:\d+)", line)
        if m:
            fam_go.setdefault(m[2], set()).add(m[3])

    families = {}
    for fam in set(clans) | set(fam_go):
        slims = sorted({a for t in fam_go.get(fam, ()) for a in ancestors(t)} & slim_ids)
        families[fam] = {"clan": clans.get(fam), "go_slim": slims}
    slim_names = {s: {"name": go[s]["name"], "namespace": go[s].get("namespace", "")} for s in slim_ids}
    # the three root terms carry no information
    for root in ("GO:0008150", "GO:0003674", "GO:0005575"):
        slim_names.pop(root, None)
    with open(args.out, "w") as f:
        json.dump({"slims": slim_names, "families": families}, f)
    n_go = sum(bool(v["go_slim"]) for v in families.values())
    print(f"{len(families)} families, {n_go} with GO slim terms, {len(slim_names)} slim categories")


if __name__ == "__main__":
    main()
