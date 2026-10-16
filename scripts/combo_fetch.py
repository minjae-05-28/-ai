"""Drug combination synergy for pre-registration 27, reduced on a GitHub runner.

  data/combo/combos.tsv   drug1, drug2, cell line, synergy scores (loewe, zip, bliss, hsa)
  data/combo/source.json

Tries DrugComb first (API summary table), then NCI-ALMANAC (ComboScore) as the fallback.
"""

import csv
import gzip
import re
import io
import json
import sys
import zipfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from depmap_fetch import get  # noqa: E402

OUT = Path("data/combo")
DRUGCOMB = ["https://drugcomb.fimm.fi/jing/summary_v_1_5.csv",
            "https://api.drugcomb.org/summary",
            "https://drugcomb.org/download/summary_v_1_5.csv"]
ALMANAC = ["https://wiki.nci.nih.gov/download/attachments/338237347/ComboDrugGrowth_Nov2017.zip",
           "https://ctd2-data.nci.nih.gov/Public/JHU-FSU/NCI-ALMANAC/ComboDrugGrowth_Nov2017.zip"]
ALMANAC_NAMES = ["https://wiki.nci.nih.gov/download/attachments/338237347/ComboCompoundNames_small.txt",
                 "https://wiki.nci.nih.gov/download/attachments/338237347/ComboCompoundNames_all.txt"]


def rows_from_csv(raw, sep=","):
    text = raw.decode(errors="replace")
    if text.lstrip()[:1] == "<":
        return None
    return list(csv.DictReader(io.StringIO(text), delimiter=sep))


def try_drugcomb(source):
    for url in DRUGCOMB:
        raw = get(url, tries=2)
        if raw is None:
            continue
        if raw[:2] == b"\x1f\x8b":
            raw = gzip.decompress(raw)
        rows = rows_from_csv(raw)
        if not rows:
            print(f"{url}: not a table", flush=True)
            continue
        head = list(rows[0])
        print(f"{url}: {len(rows)} rows, columns {head[:20]}", flush=True)
        low = {h.lower(): h for h in head}
        need = [low.get(k) for k in ("drug_row", "drug_col", "cell_line_name")]
        if not all(need):
            print("missing expected columns", flush=True)
            continue
        d1, d2, cl = need
        score = {k: low.get(f"synergy_{k}") for k in ("loewe", "zip", "bliss", "hsa")}
        with open(OUT / "combos.tsv", "w") as f:
            f.write("drug1\tdrug2\tline\tloewe\tzip\tbliss\thsa\n")
            n = 0
            for r in rows:
                if not r.get(d1) or not r.get(d2) or not r.get(cl):
                    continue
                vals = [r.get(score[k]) or "" for k in ("loewe", "zip", "bliss", "hsa")]
                if not any(vals):
                    continue
                f.write(f"{r[d1]}\t{r[d2]}\t{r[cl]}\t" + "\t".join(vals) + "\n")
                n += 1
        source["combo"] = {"source": "DrugComb", "url": url, "rows": n, "columns": head[:20]}
        return True
    return False


def try_almanac(source):
    for url in ALMANAC:
        raw = get(url, tries=2)
        if raw is None:
            continue
        try:
            z = zipfile.ZipFile(io.BytesIO(raw))
        except Exception as e:
            print(f"{url}: not a zip ({e})", flush=True)
            continue
        name = next((n for n in z.namelist() if n.lower().endswith((".csv", ".txt"))), None)
        rows = rows_from_csv(z.read(name))
        if not rows:
            continue
        head = list(rows[0])
        print(f"{url}/{name}: {len(rows)} rows, columns {head[:20]}", flush=True)
        low = {h.lower(): h for h in head}
        d1, d2 = low.get("nsc1"), low.get("nsc2")
        cl, sc = low.get("cellname"), low.get("score") or low.get("comboscore")
        if not all((d1, d2, cl, sc)):
            print("missing expected ALMANAC columns", flush=True)
            continue
        names = {}
        for n in z.namelist():                              # a names file inside the zip, if the release has one
            if "name" in n.lower() and n.lower().endswith((".txt", ".csv", ".tsv")):
                for line in z.read(n).decode(errors="replace").splitlines():
                    parts = re.split(r"[\t,]", line, maxsplit=1)
                    if len(parts) == 2 and parts[0].strip().isdigit():
                        names.setdefault(parts[0].strip(), parts[1].strip())
        for u in ALMANAC_NAMES:                              # else the separate names table
            if names:
                break
            raw2 = get(u, tries=1)
            if raw2 is None:
                continue
            for line in raw2.decode(errors="replace").splitlines():
                parts = re.split(r"[\t,]", line, maxsplit=1)
                if len(parts) == 2 and parts[0].strip().isdigit():
                    names.setdefault(parts[0].strip(), parts[1].strip())
        source["nsc_names"] = len(names)
        print("NSC names:", len(names), list(names.items())[:5], flush=True)
        label = lambda nsc: names.get(str(nsc).strip(), f"NSC{nsc}")
        agg = {}
        for r in rows:
            if not r.get(d2) or not r.get(sc):
                continue
            k = (r[d1], r[d2], r[cl])
            try:
                agg.setdefault(k, []).append(float(r[sc]))
            except ValueError:
                pass
        with open(OUT / "combos.tsv", "w") as f:
            f.write("drug1\tdrug2\tline\tloewe\tzip\tbliss\thsa\n")
            for (a, b, c), v in agg.items():
                f.write(f"{label(a)}\t{label(b)}\t{c}\t\t\t\t{sum(v) / len(v):.4f}\n")
        source["combo"] = {"source": "NCI-ALMANAC", "url": url, "file": name, "pairs": len(agg),
                           "note": "ComboScore stored in the hsa column; drugs are NSC numbers"}
        return True
    return False


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    source = {}
    if not try_drugcomb(source) and not try_almanac(source):
        source["combo"] = None
    (OUT / "source.json").write_text(json.dumps(source, indent=1))
    print(json.dumps(source, indent=1), flush=True)


if __name__ == "__main__":
    main()
