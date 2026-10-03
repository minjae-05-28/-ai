"""Probe UniProt's proteome query syntax (run on Actions; UniProt is blocked in the sandbox).

    python scripts/probe_uniprot.py      -> results/external/uniprot_probe.json

Two test runs of uniprot_proteomes.py listed no reference proteomes: one query returned an
empty table without error, another HTTP 400. This prints the status, error body and first
lines for each candidate query and field set, so the collector can use what actually works.
"""

import json
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

BASE = "https://rest.uniprot.org"
QUERIES = ["(proteome_type:1) AND (taxonomy_id:2)", "(taxonomy_id:2) AND (proteome_type:1)", "taxonomy_id:2",
           "(organism_id:2)", "(taxonomy_id:2157)", "reference:true AND taxonomy_id:2157",
           "(proteome_type:1) AND (taxonomy_id:2157)", "(taxonomy_id:4751) AND (proteome_type:1)",
           "proteome_type:1", "upid:UP000000625"]
FIELDS = ["upid,organism,organism_id,protein_count", "upid,organism,organism_id,protein_count,proteome_type",
          "upid,organism,organism_id,protein_count,busco"]


def call(url):
    try:
        with urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": "organelle-evo"}), timeout=120) as r:
            body = r.read().decode(errors="replace")
            return {"status": r.status, "total": r.headers.get("X-Total-Results"), "head": body[:400]}
    except urllib.error.HTTPError as e:
        return {"status": e.code, "error": e.read().decode(errors="replace")[:600]}
    except Exception as e:
        return {"status": None, "error": str(e)[:300]}


def main():
    out = {}
    for q in QUERIES:
        url = f"{BASE}/proteomes/search?query={urllib.parse.quote(q)}&format=tsv&size=3&fields={FIELDS[0]}"
        out[f"search {q}"] = r = call(url)
        print(f"{q!r}: {r.get('status')} total={r.get('total')} {(r.get('head') or r.get('error') or '')[:200]!r}")
    for f in FIELDS[1:]:
        url = f"{BASE}/proteomes/search?query=taxonomy_id:2157&format=tsv&size=3&fields={f}"
        out[f"fields {f}"] = r = call(url)
        print(f"fields {f}: {r.get('status')} {(r.get('head') or r.get('error') or '')[:300]!r}")
    url = f"{BASE}/proteomes/search?query=taxonomy_id:2157&format=json&size=1"
    out["json"] = r = call(url)
    print("json:", (r.get("head") or r.get("error") or "")[:400])
    url = f"{BASE}/uniprotkb/search?query=proteome:UP000000625&format=tsv&size=3&fields=accession,xref_pfam,sequence"
    out["uniprotkb pfam"] = r = call(url)
    print("uniprotkb:", r.get("status"), r.get("total"), (r.get("head") or r.get("error") or "")[:300])
    Path("results/external").mkdir(parents=True, exist_ok=True)
    Path("results/external/uniprot_probe.json").write_text(json.dumps(out, indent=1))


if __name__ == "__main__":
    main()
