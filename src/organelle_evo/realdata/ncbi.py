"""Minimal NCBI E-utilities client with an on-disk GenBank cache."""

import json
import re
import time
import urllib.parse
import urllib.request
from pathlib import Path

EUTILS = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils"
_last_call = [0.0]


def _get(endpoint: str, **params) -> bytes:
    params.setdefault("tool", "organelle-evo")
    wait = 0.4 - (time.time() - _last_call[0])  # NCBI allows 3 requests/s without a key
    if wait > 0:
        time.sleep(wait)
    url = f"{EUTILS}/{endpoint}?{urllib.parse.urlencode(params)}"
    for attempt in range(4):
        try:
            with urllib.request.urlopen(url, timeout=120) as r:
                _last_call[0] = time.time()
                return r.read()
        except OSError:
            if attempt == 3:
                raise
            time.sleep(2**attempt)


def _score(summary: dict, organism: str | None = None) -> tuple:
    title = summary.get("title", "").lower()
    acc = summary.get("caption", "")
    return (
        organism is not None and summary.get("organism", "").lower() == organism.lower(),
        2 if acc.startswith("NC_") else 1 if acc.startswith("NZ_") else 0,
        "complete" in title and "plasmid" not in title,
        int(summary.get("slen", 0)),
    )


def find_accession(term: str, organism: str | None = None) -> tuple[str, str] | None:
    """Best matching record: the exact organism (not a subspecies or strain), RefSeq,
    complete, longest."""
    ids = json.loads(_get("esearch.fcgi", db="nuccore", term=term, retmax=50, retmode="json"))
    ids = ids["esearchresult"]["idlist"]
    if not ids:
        return None
    summ = json.loads(_get("esummary.fcgi", db="nuccore", id=",".join(ids), retmode="json"))
    docs = [summ["result"][i] for i in summ["result"]["uids"]]
    best = max(docs, key=lambda d: _score(d, organism))
    return best["accessionversion"], best["title"]


def fetch_genbank(accession: str) -> str:
    return _get("efetch.fcgi", db="nuccore", id=accession, rettype="gbwithparts", retmode="text").decode()


def fetch_species(org: str, query: str, cache_dir: Path) -> Path | None:
    """Download (or reuse) the GenBank record for one organism."""
    cache_dir.mkdir(parents=True, exist_ok=True)
    path = cache_dir / (re.sub(r"[^A-Za-z0-9]+", "_", org).strip("_") + ".gb")
    if path.exists() and path.stat().st_size > 0:
        return path
    if query.startswith("accession:"):
        path.write_text(fetch_genbank(query.removeprefix("accession:")))
        return path
    query = query.format(org=org)
    hit = find_accession(query, org)
    if hit is None and "refseq[filter]" in query:
        # Some genomes (e.g. many Candidatus symbionts) are only in GenBank proper.
        hit = find_accession(query.replace(" AND refseq[filter]", ""), org)
    if hit is None:
        return None
    path.write_text(fetch_genbank(hit[0]))
    return path
