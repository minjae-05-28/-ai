"""PRISM drug response for pre-registration 23 (deviation 1: the figshare search in drug_fetch found no PRISM release,
so known article ids are tried too). Uses data/drug/lines.tsv from drug_fetch for the cell-line scores.

  data/drug/compounds.tsv, data/drug/prism_source.json
"""

import csv
import io
import json
import re
import sys
import urllib.request
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
from depmap_fetch import get  # noqa: E402
from drug_fetch import OUT, PRISM_OPTIONS, col, figshare_find, partial, read_matrix  # noqa: E402

ARTICLES = [9393293]                       # PRISM Repurposing 19Q4 (Corsello et al. 2020)
QUERIES = ["PRISM Repurposing", "Repurposing Public 24Q2", "PRISM Repurposing 19Q4", "PRISM 24Q2", "Corsello PRISM"]


def by_article(aid, names):
    files = json.loads(get(f"https://api.figshare.com/v2/articles/{aid}/files?page_size=1000", tries=2) or b"[]")
    have = {f["name"]: f["download_url"] for f in files}
    print(aid, sorted(have)[:30], flush=True)
    if all(n in have for n in names):
        return f"figshare article {aid}", aid, {n: have[n] for n in names}
    return None


def main():
    lines = [x.split("\t") for x in (OUT / "lines.tsv").read_text().splitlines()[1:]]
    score = {l[0]: (float(l[2]), float(l[3])) for l in lines}
    lineage = {l[0]: l[1] for l in lines}
    pr, opt = None, None
    for o in PRISM_OPTIONS:
        pr = figshare_find(QUERIES, o) or next((r for a in ARTICLES if (r := by_article(a, o))), None)
        if pr:
            opt = o
            break
    if pr is None:
        (OUT / "prism_source.json").write_text(json.dumps({"prism": "not found"}))
        raise SystemExit("PRISM not found")
    title, aid, urls = pr
    rows, cols, M = read_matrix(get(urls[opt[0]]))
    if any(str(c).startswith("ACH-") for c in cols[:50]):
        comp_ids, line_ids, V = rows, cols, M
    else:
        comp_ids, line_ids, V = cols, rows, M.T
    info = list(csv.reader(io.StringIO(get(urls[opt[1]]).decode())))
    ih = [h.lower() for h in info[0]]
    idset = set(comp_ids)
    idc = next((i for i in range(len(ih)) if sum(len(r) > i and r[i] in idset for r in info[1:]) > 0.3 * len(info[1:])), None)
    bc, nc, mc, tc = col(ih, "broad_id", "ids", "broad"), col(ih, "drug.name", "name"), col(ih, "moa"), col(ih, "target")
    meta = {}
    for r in info[1:]:
        if idc is not None and len(r) > idc:
            meta[r[idc]] = tuple(r[c] if c is not None and len(r) > c else "" for c in (bc, nc, mc, tc))
    t = np.array([score.get(l, (np.nan, np.nan))[0] for l in line_ids])
    p = np.array([score.get(l, (np.nan, np.nan))[1] for l in line_ids])
    g = np.array([lineage.get(l, "NA") for l in line_ids])
    groups = {}
    for k, cid in enumerate(comp_ids):
        bid = (meta.get(cid, ("",))[0] or re.sub(r"::.*$", "", cid))[:13]
        groups.setdefault(bid, []).append(k)
    n_out = 0
    with open(OUT / "compounds.tsv", "w") as f:
        f.write("compound\tname\tmoa\ttarget\tn\tmean_viability\trho_lineage\trho_partial\n")
        for bid, ks in groups.items():
            y = np.nanmean(V[ks], 0) if len(ks) > 1 else V[ks[0]]
            r = partial(y, t, p, g)
            if not r:
                continue
            _, nm, moa, tg = meta.get(comp_ids[ks[0]], ("", "", "", ""))
            f.write(f"{bid}\t{nm}\t{moa}\t{tg}\t{r[2]}\t{np.nanmean(y):.4f}\t{r[0]:.4f}\t{r[1]:.4f}\n")
            n_out += 1
    (OUT / "prism_source.json").write_text(json.dumps({"prism": f"{title} (figshare {aid}): {opt[0]}",
                                                       "meta_columns": info[0], "compounds": n_out,
                                                       "lines_in_matrix": len(line_ids)}, indent=1))
    print("compounds", n_out, flush=True)


if __name__ == "__main__":
    main()
