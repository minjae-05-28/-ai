"""DepMap CRISPR dependencies and DGIdb approved-drug genes for pre-registration 21, reduced on a GitHub runner.

  data/depmap/gene_dependency.tsv     gene, n_lines, mean_effect, frac_dependent (< -0.5), common_essential
  data/depmap/lineage_dependency.tsv  gene x lineage fraction dependent (lineages with their line counts in the header)
  data/depmap/approved_drug_genes.txt genes with an approved drug in DGIdb (empty if unavailable)
  data/depmap/source.json             release and files used
"""

import csv
import io
import json
import time
import urllib.request
from collections import defaultdict
from pathlib import Path

import numpy as np

OUT = Path("data/depmap")
INDEX = "https://depmap.org/portal/api/download/files"   # falls back to the figshare copies
WANT = ["CRISPRGeneEffect.csv", "Model.csv", "CRISPRInferredCommonEssentials.csv"]
DGIDB = ["https://dgidb.org/data/latest/interactions.tsv", "https://www.dgidb.org/data/latest/interactions.tsv"]
DEP = -0.5


def get(url, tries=4):
    for i in range(tries):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "organelle-evo research script"})
            with urllib.request.urlopen(req, timeout=900) as r:
                return r.read()
        except Exception as e:
            print(f"attempt {i + 1} {url}: {e}", flush=True)
            time.sleep(15 * (i + 1))
    return None


def _from_index():
    raw = get(INDEX + "?format=csv")
    if raw is None or raw.lstrip()[:1] == b"<":
        return None
    rows = list(csv.DictReader(io.StringIO(raw.decode())))
    rel_key = next(k for k in rows[0] if k.lower() in ("release", "release_name"))
    date_key = next((k for k in rows[0] if "date" in k.lower()), None)
    by_rel, dates = defaultdict(dict), {}
    for r in rows:
        by_rel[r[rel_key]][r["filename"]] = r["url"]
        if date_key:
            dates[r[rel_key]] = r[date_key]
    ok = [rel for rel, f in by_rel.items() if all(w in f for w in WANT) and "public" in rel.lower()]
    if not ok:
        return None
    rel = max(ok, key=lambda x: dates.get(x, x))
    return rel, {w: by_rel[rel][w] for w in WANT}


def _from_figshare():
    """DepMap posts each public release on figshare ("DepMap 24Q4 Public" etc.); newest one with all files."""
    found = []
    for q in ("DepMap Public", "DepMap Q Public"):
        body = json.dumps({"search_for": q, "page_size": 100}).encode()
        req = urllib.request.Request("https://api.figshare.com/v2/articles/search", data=body,
                                     headers={"Content-Type": "application/json"})
        try:
            with urllib.request.urlopen(req, timeout=120) as r:
                found += json.loads(r.read())
        except Exception as e:
            print("figshare search:", e, flush=True)
    seen = set()
    cands = []
    for a in found:
        if a["id"] in seen or "depmap" not in a["title"].lower() or "public" not in a["title"].lower():
            continue
        seen.add(a["id"])
        cands.append(a)
    cands.sort(key=lambda a: a.get("published_date", ""), reverse=True)
    for a in cands[:15]:
        files = json.loads(get(f"https://api.figshare.com/v2/articles/{a['id']}/files?page_size=1000") or b"[]")
        names = {f["name"]: f["download_url"] for f in files}
        if all(w in names for w in WANT):
            return f"{a['title']} (figshare {a['id']})", {w: names[w] for w in WANT}
    return None


def latest_files():
    res = _from_index() or _from_figshare()
    if res is None:
        raise SystemExit("DepMap release not found (portal index and figshare)")
    return res


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    rel, urls = latest_files()
    print("release", rel, flush=True)
    model = list(csv.DictReader(io.StringIO(get(urls["Model.csv"]).decode())))
    lineage = {m["ModelID"]: (m.get("OncotreeLineage") or "") for m in model}
    ce_raw = get(urls["CRISPRInferredCommonEssentials.csv"]).decode().splitlines()
    common = {line.split(",")[0].split(" (")[0].strip('"') for line in ce_raw[1:] if line}
    text = get(urls["CRISPRGeneEffect.csv"]).decode()
    reader = csv.reader(io.StringIO(text))
    head = next(reader)
    genes = [h.split(" (")[0] for h in head[1:]]
    ids, vals = [], []
    for row in reader:
        ids.append(row[0])
        vals.append([float(x) if x not in ("", "NA") else np.nan for x in row[1:]])
    E = np.array(vals, dtype=np.float32)
    dep = (E < DEP).astype(np.float32)
    dep[np.isnan(E)] = np.nan
    n = np.sum(~np.isnan(E), 0)
    with open(OUT / "gene_dependency.tsv", "w") as f:
        f.write("gene\tn_lines\tmean_effect\tfrac_dependent\tcommon_essential\n")
        for j, g in enumerate(genes):
            f.write(f"{g}\t{n[j]}\t{np.nanmean(E[:, j]):.4f}\t{np.nanmean(dep[:, j]):.4f}\t{int(g in common)}\n")
    lin = np.array([lineage.get(i, "") for i in ids])
    names = sorted({x for x in lin if x})
    cols = [(nm, lin == nm) for nm in names]
    with open(OUT / "lineage_dependency.tsv", "w") as f:
        f.write("gene\t" + "\t".join(f"{nm} ({int(m.sum())})" for nm, m in cols) + "\n")
        for j, g in enumerate(genes):
            f.write(g + "\t" + "\t".join(f"{np.nanmean(dep[m, j]):.4f}" for _, m in cols) + "\n")
    approved = set()
    for url in DGIDB:
        raw = get(url, tries=2)
        if raw is None:
            continue
        lines = raw.decode(errors="replace").splitlines()
        h = lines[0].split("\t")
        gi = h.index("gene_name") if "gene_name" in h else None
        ai = h.index("approved") if "approved" in h else None
        if gi is None or ai is None:
            print("DGIdb columns:", h, flush=True)
            continue
        for line in lines[1:]:
            x = line.split("\t")
            if len(x) > max(gi, ai) and x[ai].strip().lower() in ("true", "t", "1") and x[gi]:
                approved.add(x[gi])
        break
    (OUT / "approved_drug_genes.txt").write_text("\n".join(sorted(approved)) + "\n")
    (OUT / "source.json").write_text(json.dumps({"release": rel, "files": urls, "lines": len(ids),
                                                 "genes": len(genes), "common_essentials": len(common),
                                                 "approved_drug_genes": len(approved)}, indent=1))
    print(len(ids), "lines", len(genes), "genes", len(common), "common", len(approved), "approved-drug genes", flush=True)


if __name__ == "__main__":
    main()
