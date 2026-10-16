"""Inputs for pre-registration 24, reduced on a GitHub runner.

  data/srebp/score_module.tsv   ModelID, SangerModelID, fold change of SCD, SREBF1, SCAP, MBTPS1, MBTPS2 (Project Score)
  data/srebp/gdsc_lipid.tsv     ModelID, drug, putative target, ln IC50 (GDSC2 drugs targeting lipid synthesis)
  data/srebp/source.json
"""

import csv
import io
import json
import sys
import zipfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from depmap_fetch import get  # noqa: E402
from drug_fetch import figshare_find  # noqa: E402

OUT = Path("data/srebp")
MODULE = ["SCD", "SREBF1", "SCAP", "MBTPS1", "MBTPS2"]
LIPID = ["SCD", "SREBF", "FASN", "ACACA", "HMGCR", "SQLE"]
SCORE_URLS = ["https://cog.sanger.ac.uk/cmp/download/essentiality_matrices.zip",
              "https://cog.sanger.ac.uk/cmp/download/Project_score_combined_Sanger_v1_Broad_20Q2_fitness_scores_fold_change_values_20240111.zip"]
GDSC_URLS = ["https://cog.sanger.ac.uk/cancerrxgene/GDSC_release8.5/GDSC2_fitted_dose_response_27Oct23.xlsx",
             "https://cog.sanger.ac.uk/cancerrxgene/GDSC_release8.4/GDSC2_fitted_dose_response_24Jul22.xlsx"]


def model_map():
    dm = figshare_find(["DepMap 24Q4 Public", "DepMap Public"], ["Model.csv"])
    rows = list(csv.DictReader(io.StringIO(get(dm[2]["Model.csv"]).decode())))
    sanger = {r["SangerModelID"]: r["ModelID"] for r in rows if r.get("SangerModelID")}
    names = {}
    for r in rows:
        for k in ("StrippedCellLineName", "CellLineName"):
            if r.get(k):
                names[r[k].upper().replace("-", "").replace(" ", "")] = r["ModelID"]
    return sanger, names


def to_model(key, sanger, names):
    return sanger.get(key) or names.get(key.upper().replace("-", "").replace(" ", ""))


def score(sanger, names, source):
    for url in SCORE_URLS:
        raw = get(url, tries=2)
        if raw is None:
            continue
        z = zipfile.ZipFile(io.BytesIO(raw))
        listing = z.namelist()
        source["score_zip"] = {"url": url, "files": listing[:50]}
        pick = [n for n in listing if "fold" in n.lower() or "fc" in n.lower().split("/")[-1]]
        pick = [n for n in pick if n.lower().endswith((".tsv", ".txt", ".csv"))] or \
               [n for n in listing if n.lower().endswith((".tsv", ".txt", ".csv"))]
        for name in pick:
            text = z.read(name).decode(errors="replace")
            sep = "\t" if text.count("\t") > text.count(",") else ","
            rows = list(csv.reader(io.StringIO(text), delimiter=sep))
            head = rows[0]
            gene_col = {r[0]: r for r in rows[1:] if r}
            if not all(g in gene_col for g in MODULE[:3]):
                continue
            out = ["ModelID\tline\t" + "\t".join(MODULE)]
            n = 0
            for j in range(1, len(head)):
                m = to_model(head[j], sanger, names)
                if not m:
                    continue
                vals = [gene_col[g][j] if g in gene_col and len(gene_col[g]) > j else "" for g in MODULE]
                out.append(f"{m}\t{head[j]}\t" + "\t".join(vals))
                n += 1
            (OUT / "score_module.tsv").write_text("\n".join(out) + "\n")
            source["score_file"] = name
            source["score_lines_mapped"] = n
            return
    source["score_file"] = None


def gdsc(sanger, names, source):
    import openpyxl
    for url in GDSC_URLS:
        raw = get(url, tries=2)
        if raw is None:
            continue
        wb = openpyxl.load_workbook(io.BytesIO(raw), read_only=True)
        ws = wb.active
        it = ws.iter_rows(values_only=True)
        head = [str(h) for h in next(it)]
        ci = {h: i for i, h in enumerate(head)}
        out = ["ModelID\tdrug\ttarget\tln_ic50"]
        for r in it:
            tg = str(r[ci["PUTATIVE_TARGET"]] or "")
            if not any(k in tg.upper() for k in LIPID):
                continue
            m = sanger.get(str(r[ci["SANGER_MODEL_ID"]])) or to_model(str(r[ci["CELL_LINE_NAME"]]), sanger, names)
            if m:
                out.append(f"{m}\t{r[ci['DRUG_NAME']]}\t{tg}\t{r[ci['LN_IC50']]}")
        (OUT / "gdsc_lipid.tsv").write_text("\n".join(out) + "\n")
        source["gdsc"] = {"url": url, "rows": len(out) - 1}
        return
    source["gdsc"] = None


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    source = {}
    sanger, names = model_map()
    score(sanger, names, source)
    try:
        gdsc(sanger, names, source)
    except Exception as e:
        source["gdsc_error"] = str(e)
    (OUT / "source.json").write_text(json.dumps(source, indent=1))
    print(json.dumps(source, indent=1), flush=True)


if __name__ == "__main__":
    main()
