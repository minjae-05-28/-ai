"""Inputs for pre-registration 23 (docs/preregistration/2026-10-16_atavism_drugs.md), reduced on a GitHub runner.

  data/drug/l1000cds2_reverse.json, l1000cds2_mimic.json   L1000CDS2 query results for the atavism signature
  data/drug/lines.tsv        cell line, lineage, atavism (tilt) score, proliferation score
  data/drug/compounds.tsv    PRISM compound, name, moa, target, n lines, mean viability, rho (lineage), rho (partial)
  data/drug/genes.tsv        CRISPR gene, n lines, mean effect, rho (lineage), rho (partial)
  data/drug/source.json
"""

import csv
import io
import json
import re
import sys
import time
import urllib.request
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
from depmap_fetch import get  # noqa: E402

OUT = Path("data/drug")
L1000 = ["https://maayanlab.cloud/L1000CDS2/query", "https://amp.pharm.mssm.edu/L1000CDS2/query"]
DEPMAP_FILES = ["OmicsExpressionProteinCodingGenesTPMLogp1.csv", "CRISPRGeneEffect.csv", "Model.csv"]
PRISM_OPTIONS = [
    ["Repurposing_Public_24Q2_Extended_Primary_Data_Matrix.csv", "Repurposing_Public_24Q2_Extended_Primary_Compound_List.csv"],
    ["primary-screen-replicate-collapsed-logfold-change.csv", "primary-screen-replicate-collapsed-treatment-info.csv"],
]
MIN_LINES = 100


def figshare_find(queries, names):
    """Newest figshare article (from these searches) holding all `names`; name -> download url."""
    found, seen = [], set()
    for q in queries:
        body = json.dumps({"search_for": q, "page_size": 100}).encode()
        req = urllib.request.Request("https://api.figshare.com/v2/articles/search", data=body,
                                     headers={"Content-Type": "application/json"})
        try:
            with urllib.request.urlopen(req, timeout=120) as r:
                for a in json.loads(r.read()):
                    if a["id"] not in seen:
                        seen.add(a["id"])
                        found.append(a)
        except Exception as e:
            print("figshare search", q, e, flush=True)
    found.sort(key=lambda a: a.get("published_date", ""), reverse=True)
    for a in found[:40]:
        files = json.loads(get(f"https://api.figshare.com/v2/articles/{a['id']}/files?page_size=1000", tries=2) or b"[]")
        have = {f["name"]: f["download_url"] for f in files}
        if all(n in have for n in names):
            return a["title"], a["id"], {n: have[n] for n in names}
    return None


def read_matrix(raw):
    """CSV with a first id column: row ids, column names, float matrix."""
    reader = csv.reader(io.StringIO(raw.decode()))
    head = next(reader)
    rows, vals = [], []
    for r in reader:
        rows.append(r[0])
        vals.append([float(x) if x not in ("", "NA", "nan") else np.nan for x in r[1:]])
    return rows, head[1:], np.array(vals, dtype=np.float32)


def rank_center(x, groups):
    """Ranks (NaN kept), minus the group mean rank."""
    out = np.full(len(x), np.nan)
    ok = ~np.isnan(x)
    r = np.empty(ok.sum())
    r[np.argsort(x[ok], kind="stable")] = np.arange(ok.sum())
    out[ok] = r
    for g in set(groups):
        m = (groups == g) & ok
        if m.sum():
            out[m] -= out[m].mean()
    return out


def partial(y, t, p, groups):
    """(lineage-centered rank correlation, lineage-centered + proliferation-adjusted rank correlation, n)."""
    ok = ~np.isnan(y) & ~np.isnan(t) & ~np.isnan(p)
    if ok.sum() < MIN_LINES:
        return None
    g = groups[ok]
    yr, tr, pr = rank_center(y[ok], g), rank_center(t[ok], g), rank_center(p[ok], g)
    r1 = np.corrcoef(yr, tr)[0, 1]
    res = lambda a: a - (np.dot(a, pr) / np.dot(pr, pr)) * pr
    r2 = np.corrcoef(res(yr), res(tr))[0, 1]
    return float(r1), float(r2), int(ok.sum())


def l1000(sig, aggravate):
    payload = {"data": {"upGenes": sig["up"], "dnGenes": sig["down"]},
               "config": {"aggravate": aggravate, "searchMethod": "geneSet", "share": False, "combination": False,
                          "db-version": "latest"}, "metadata": []}
    for url in L1000:
        try:
            req = urllib.request.Request(url, data=json.dumps(payload).encode(),
                                         headers={"Content-Type": "application/json"})
            with urllib.request.urlopen(req, timeout=300) as r:
                return {"url": url, "result": json.loads(r.read())}
        except Exception as e:
            print("L1000CDS2", url, e, flush=True)
            time.sleep(10)
    return {"url": None, "result": None}


def col(names, *keys):
    for k in keys:
        for i, n in enumerate(names):
            if k in n.lower():
                return i
    return None


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    sig = json.loads(Path("results/drug/signature.json").read_text())
    source = {}
    for tag, agg in (("reverse", False), ("mimic", True)):
        res = l1000(sig, agg)
        (OUT / f"l1000cds2_{tag}.json").write_text(json.dumps(res, indent=1))
        source[f"l1000cds2_{tag}"] = res["url"]
    dm = figshare_find(["DepMap 24Q4 Public", "DepMap Public"], DEPMAP_FILES)
    title, aid, urls = dm
    source["depmap"] = f"{title} (figshare {aid})"
    model = list(csv.DictReader(io.StringIO(get(urls["Model.csv"]).decode())))
    lineage = {m["ModelID"]: (m.get("OncotreeLineage") or "NA") for m in model}
    ids, genes, X = read_matrix(get(urls["OmicsExpressionProteinCodingGenesTPMLogp1.csv"]))
    sym = [g.split(" (")[0] for g in genes]
    lines = [i for i in ids]
    first = ids and ids[0]
    if not str(first).startswith("ACH-"):                          # some releases put the model id in a later column
        print("expression row id example:", first, flush=True)
    Z = (X - np.nanmean(X, 0)) / (np.nanstd(X, 0) + 1e-6)
    gi = {g: j for j, g in enumerate(sym)}
    up = [gi[g] for g in sig["up"] if g in gi]
    dn = [gi[g] for g in sig["down"] if g in gi]
    P = {x.split("\t")[1] for x in Path("data/human/proliferation_go.tsv").read_text().splitlines()[1:]
         if len(x.split("\t")) > 1 and x.split("\t")[1]}
    P |= {g for v in json.loads(Path("data/human/hallmark_proliferation.json").read_text())["sets"].values() for g in v}
    pj = [gi[g] for g in P if g in gi]
    tilt = np.nanmean(Z[:, up], 1) - np.nanmean(Z[:, dn], 1)
    prol = np.nanmean(Z[:, pj], 1)
    score = {l: (t, p) for l, t, p in zip(lines, tilt, prol)}
    source.update(signature_genes_found={"up": len(up), "down": len(dn), "proliferation": len(pj)},
                  expression_lines=len(lines))
    with open(OUT / "lines.tsv", "w") as f:
        f.write("line\tlineage\ttilt\tproliferation\n")
        for l in lines:
            f.write(f"{l}\t{lineage.get(l, 'NA')}\t{score[l][0]:.4f}\t{score[l][1]:.4f}\n")

    def aligned(line_ids):
        t = np.array([score.get(l, (np.nan, np.nan))[0] for l in line_ids])
        p = np.array([score.get(l, (np.nan, np.nan))[1] for l in line_ids])
        g = np.array([lineage.get(l, "NA") for l in line_ids])
        return t, p, g
    cids, cg, E = read_matrix(get(urls["CRISPRGeneEffect.csv"]))
    t, p, g = aligned(cids)
    with open(OUT / "genes.tsv", "w") as f:
        f.write("gene\tn\tmean_effect\trho_lineage\trho_partial\n")
        for j, name in enumerate(cg):
            r = partial(E[:, j], t, p, g)
            if r:
                f.write(f"{name.split(' (')[0]}\t{r[2]}\t{np.nanmean(E[:, j]):.4f}\t{r[0]:.4f}\t{r[1]:.4f}\n")
    del E
    pr = None
    for opt in PRISM_OPTIONS:
        pr = figshare_find(["PRISM Repurposing", "Repurposing Public", "PRISM Repurposing 19Q4"], opt)
        if pr:
            break
    if pr is None:
        source["prism"] = "not found"
    else:
        ptitle, pid, purls = pr
        source["prism"] = f"{ptitle} (figshare {pid}): {opt[0]}"
        rows, cols, M = read_matrix(get(purls[opt[0]]))
        if any(str(c).startswith("ACH-") for c in cols[:50]):     # compounds x lines
            comp_ids, line_ids, V = rows, cols, M
        else:                                                      # lines x compounds
            comp_ids, line_ids, V = cols, rows, M.T
        info = list(csv.reader(io.StringIO(get(purls[opt[1]]).decode())))
        ih = [h.lower() for h in info[0]]
        idc = None
        idset = set(comp_ids)
        for i in range(len(ih)):
            if sum(r[i] in idset for r in info[1:] if len(r) > i) > 0.5 * len(info[1:]):
                idc = i
                break
        nc, mc, tc = col(ih, "drug.name", "name"), col(ih, "moa"), col(ih, "target")
        meta = {}
        for r in info[1:]:
            if idc is not None and len(r) > idc:
                meta[r[idc]] = (r[nc] if nc is not None else "", r[mc] if mc is not None else "",
                                r[tc] if tc is not None else "")
        source["prism_meta_columns"] = info[0]
        t, p, g = aligned(line_ids)
        groups = {}
        for k, cid in enumerate(comp_ids):
            groups.setdefault(re.sub(r"::.*$", "", cid), []).append(k)
        with open(OUT / "compounds.tsv", "w") as f:
            f.write("compound\tname\tmoa\ttarget\tn\tmean_viability\trho_lineage\trho_partial\n")
            for cid, ks in groups.items():
                y = np.nanmean(V[ks], 0) if len(ks) > 1 else V[ks[0]]
                r = partial(y, t, p, g)
                if not r:
                    continue
                nm, moa, tg = meta.get(comp_ids[ks[0]], meta.get(cid, ("", "", "")))
                f.write(f"{cid}\t{nm}\t{moa}\t{tg}\t{r[2]}\t{np.nanmean(y):.4f}\t{r[0]:.4f}\t{r[1]:.4f}\n")
    (OUT / "source.json").write_text(json.dumps(source, indent=1))
    print(json.dumps(source, indent=1), flush=True)


if __name__ == "__main__":
    main()
