"""Which public drug-combination screen can we actually reach, and does it contain a lipid synthesis
inhibitor? (pre-registration 27 — the test needs both.)

Probe only: it reads drug NAMES and column headers, never a synergy value, so the pre-registration stays
intact until a usable source is found.

  data/combo_probe/report.json   per source: reachable, rows, columns, drugs, lipid drugs found
"""

import csv
import gzip
import io
import json
import re
import sys
import urllib.parse
import urllib.request
import zipfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from depmap_fetch import get  # noqa: E402

OUT = Path("data/combo_probe")
PEEK = 4_000_000          # bytes read from a plain table just to see its drug names
MAX_FULL = 400_000_000    # skip anything bigger than this

# canonical lipid synthesis inhibitors, by target, in addition to whatever PRISM annotates (data/drug/compounds.tsv)
LIPID_NAMES = [
    # SCD1
    "a-939572", "a939572", "mk-8245", "mk8245", "cay10566", "ssi-4", "ssi4", "ccr-1", "t-3764518",
    # FASN
    "orlistat", "cerulenin", "c75", "tvb-2640", "tvb-3166", "tvb-3664", "denifanstat", "gsk2194069",
    "fasnall", "platensimycin", "epigallocatechingallate",
    # ACC
    "soraphena", "nd-646", "nd646", "tofa", "cp-640186", "firsocostat", "gs-0976", "nd-630",
    # HMGCR / mevalonate
    "simvastatin", "atorvastatin", "lovastatin", "mevastatin", "compactin", "fluvastatin", "pravastatin",
    "rosuvastatin", "cerivastatin", "pitavastatin", "zaragozicacid", "zoledronicacid", "alendronate",
    # SQLE / downstream sterol
    "terbinafine", "nb-598", "ro48-8071", "ro-48-8071", "butenafine", "naftifine",
    # SREBP / SCAP / S1P
    "fatostatin", "betulin", "pf-429242", "pf429242", "25-hydroxycholesterol", "25hydroxycholesterol",
    "xanthohumol", "nelfinavir",
]
# word fragments in a MOA / target column
LIPID_WORDS = ["SCD1", "SCD ", "STEAROYL", "FATTY ACID SYNTH", "FASN", "SREBP", "SREBF", "ACETYL-COA CARBOXYL",
               "ACACA", "HMG-COA REDUCT", "HMGCR", "SQUALENE", "SQLE", "LIPOGEN", "DESATURASE", "MEVALONATE",
               "CHOLESTEROL BIOSYNTH", "LIPID SYNTH"]

SOURCES = {
    # DrugCombDB (Deng lab) — ~6,000 drugs, the broadest aggregate
    "drugcombdb_scored_http": "http://drugcombdb.denglab.org/download/drugcombs_scored.csv",
    "drugcombdb_scored_https": "https://drugcombdb.denglab.org/download/drugcombs_scored.csv",
    "drugcombdb_response": "http://drugcombdb.denglab.org/download/drugcombs_response.csv",
    "drugcombdb_chem": "http://drugcombdb.denglab.org/download/drug_chemical_info.csv",
    "drugcombdb_alt": "http://drugcombdb.denglab.org/static/download/drugcombs_scored.csv",
    # DrugComb v1.5
    "drugcomb_api_summary": "https://api.drugcomb.org/summary",
    "drugcomb_api_drugs": "https://api.drugcomb.org/drugs",
    "drugcomb_jing": "https://drugcomb.fimm.fi/jing/summary_v_1_5.csv",
    # SynergxDB
    "synergxdb_api": "https://www.synergxdb.ca/api/synergy?limit=10",
    "synergxdb_dl": "https://www.synergxdb.ca/downloads/synergy.csv",
    # O'Neil / Merck 2016 (38 drugs) via the DeepSynergy release
    "oneil_deepsynergy": "https://raw.githubusercontent.com/KristinaPreuer/DeepSynergy/master/labels.csv",
    # GDSC combination screen (Jaaks 2022)
    "gdsc_combo_portal": "https://gdsc-combinations.depmap.sanger.ac.uk/",
    "gdsc_combo_anchor": "https://cog.sanger.ac.uk/cancerrxgene/GDSC_release8.5/combinations_anchor.csv",
    "gdsc_combo_matrix": "https://cog.sanger.ac.uk/cancerrxgene/GDSC_release8.5/combinations_matrix.csv",
    # NCATS matrix screens
    "ncats_matrix": "https://matrix.ncats.nih.gov/api/matrices",
}
SEARCH = {"zenodo": ["drug combination synergy", "drug combination screen cancer cell lines"],
          "figshare": ["drug combination synergy", "drug synergy screen"]}


def lipid_hits(names, moas=()):
    norm = lambda x: re.sub(r"[^a-z0-9.]", "", (x or "").lower())
    want = {norm(x) for x in LIPID_NAMES} | prism_lipid()
    hit = sorted({n for n in names if norm(n) in want})
    txt = " ".join(moas).upper()
    return hit, sorted({w for w in LIPID_WORDS if w in txt})


def prism_lipid():
    """PRISM compound names whose MOA or target names a lipid synthesis enzyme (data/drug/compounds.tsv)."""
    out, p = set(), Path("data/drug/compounds.tsv")
    if not p.exists():
        return out
    for line in p.read_text().splitlines()[1:]:
        x = line.split("\t")
        if len(x) >= 4 and x[1]:
            txt = (x[2] + " " + x[3]).upper()
            if any(w in txt for w in LIPID_WORDS):
                out.add(re.sub(r"[^a-z0-9.]", "", x[1].lower()))
    return out


def peek(url):
    """Download at most PEEK bytes (whole file for an archive), or None."""
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "organelle-evo research script"})
        with urllib.request.urlopen(req, timeout=600) as r:
            size = int(r.headers.get("Content-Length") or 0)
            if size > MAX_FULL:
                return b"", f"too big ({size} bytes)"
            ctype = (r.headers.get("Content-Type") or "").lower()
            whole = url.endswith((".zip", ".gz", ".xlsx")) or "zip" in ctype or "gzip" in ctype
            return r.read() if whole else r.read(PEEK), None
    except Exception as e:
        return None, str(e)


def tables(raw, url):
    """(name, rows) for each table inside raw; a truncated last row is dropped."""
    if raw[:2] == b"\x1f\x8b":
        try:
            raw = gzip.decompress(raw)
        except Exception:
            pass
    if raw[:2] == b"PK":
        try:
            z = zipfile.ZipFile(io.BytesIO(raw))
        except Exception:
            return []
        out = []
        for n in z.namelist():
            if n.lower().endswith((".csv", ".tsv", ".txt")):
                out += [(n, parse(z.read(n)))]
        return out
    return [(url.rsplit("/", 1)[-1], parse(raw))]


def parse(raw):
    text = raw.decode(errors="replace")
    if text.lstrip()[:1] in ("<", "{", "["):
        return text[:400]                              # HTML or JSON: hand back a sample
    sep = "\t" if text.count("\t") > text.count(",") else ","
    rows = list(csv.DictReader(io.StringIO(text), delimiter=sep))
    return rows[:-1] if len(rows) > 1 else rows        # the last row may be cut by PEEK


def drug_columns(head):
    low = {h.lower(): h for h in head}
    d = [low[h] for h in low if re.search(r"(drug|compound|agent|nsc|cpd)", h) and
         not re.search(r"(id$|cid|smiles|conc|dose|row_conc|col_conc)", h)]
    m = [low[h] for h in low if re.search(r"(moa|mechanism|target|class)", h)]
    return d, m


def report_table(name, rows):
    if isinstance(rows, str):
        return {"not_a_table": rows[:200]}
    if not rows:
        return {"rows": 0}
    head = list(rows[0])
    d, m = drug_columns(head)
    names, moas = set(), []
    for r in rows:
        for c in d:
            if r.get(c):
                names.add(str(r[c]).strip())
        for c in m:
            if r.get(c):
                moas.append(str(r[c]))
    hit, words = lipid_hits(names, moas)
    return {"rows_seen": len(rows), "columns": head[:25], "drug_columns": d, "annotation_columns": m,
            "distinct_drug_values_seen": len(names), "drug_sample": sorted(names)[:25],
            "lipid_drugs_found": hit, "lipid_words_in_annotation": words}


def search_zenodo(q):
    raw = get(f"https://zenodo.org/api/records?q={urllib.parse.quote(q)}&size=10&sort=mostrecent", tries=2)
    if raw is None:
        return {"error": "unreachable"}
    try:
        hits = json.loads(raw)["hits"]["hits"]
    except Exception as e:
        return {"error": str(e)}
    return [{"title": h.get("metadata", {}).get("title", "")[:120], "doi": h.get("doi"),
             "files": [{"name": f.get("key"), "size": f.get("size"),
                        "url": (f.get("links") or {}).get("self")} for f in (h.get("files") or [])][:10]}
            for h in hits]


def search_figshare(q):
    body = json.dumps({"search_for": q, "page_size": 10}).encode()
    try:
        req = urllib.request.Request("https://api.figshare.com/v2/articles/search", data=body,
                                     headers={"Content-Type": "application/json"})
        with urllib.request.urlopen(req, timeout=120) as r:
            arts = json.loads(r.read())
    except Exception as e:
        return {"error": str(e)}
    out = []
    for a in arts:
        files = []
        raw = get(f"https://api.figshare.com/v2/articles/{a['id']}", tries=1)
        if raw:
            try:
                files = [{"name": f["name"], "size": f["size"], "url": f["download_url"]}
                         for f in json.loads(raw).get("files", [])][:10]
            except Exception:
                pass
        out.append({"title": a.get("title", "")[:120], "id": a.get("id"), "files": files})
    return out


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    rep = {"direct": {}, "search": {}}
    for key, url in SOURCES.items():
        raw, err = peek(url)
        if raw is None or not raw:
            rep["direct"][key] = {"url": url, "reachable": False, "error": (err or "empty")[:200]}
            print(f"{key}: FAIL {err}", flush=True)
            continue
        ts = tables(raw, url)
        rep["direct"][key] = {"url": url, "reachable": True, "bytes": len(raw),
                              "tables": {n: report_table(n, r) for n, r in ts}}
        print(f"{key}: OK {len(raw)} bytes, {len(ts)} table(s)", flush=True)
        for n, r in ts:
            info = report_table(n, r)
            print("   ", n, json.dumps(info, ensure_ascii=False)[:600], flush=True)
    for q in SEARCH["zenodo"]:
        rep["search"][f"zenodo: {q}"] = search_zenodo(q)
    for q in SEARCH["figshare"]:
        rep["search"][f"figshare: {q}"] = search_figshare(q)
    print(json.dumps(rep["search"], ensure_ascii=False, indent=1)[:8000], flush=True)
    (OUT / "report.json").write_text(json.dumps(rep, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
