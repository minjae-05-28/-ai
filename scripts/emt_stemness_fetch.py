"""EMT and stemness scores per cell line for pre-registration 25, computed on a GitHub runner from CCLE
expression (same file as pre-registration 23).

  data/emt/scores.tsv        line, lineage, tilt, proliferation, epithelial, mesenchymal, emt (= M - E), stemness
  data/emt/depmap_module.tsv line, SREBP module gene effects (SCD, SREBF1, SCAP, MBTPS1, MBTPS2)
  data/emt/source.json
"""

import json
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
from depmap_fetch import get  # noqa: E402
from drug_fetch import figshare_find, read_matrix  # noqa: E402

OUT = Path("data/emt")
EPI = ["CDH1", "EPCAM", "KRT8", "KRT18", "KRT19", "CLDN4", "CLDN7", "OCLN", "DSP", "ESRP1", "ESRP2", "GRHL2"]
MES = ["VIM", "CDH2", "FN1", "ZEB1", "ZEB2", "SNAI1", "SNAI2", "TWIST1", "SPARC", "FBN1", "COL5A2", "ITGB1"]
MODULE = ["SCD", "SREBF1", "SCAP", "MBTPS1", "MBTPS2"]
STEM = ["POU5F1", "NANOG", "SOX2", "LIN28A", "LIN28B", "KLF4", "MYC", "SALL4", "PROM1", "ALDH1A1", "CD44", "THY1",
        "BMI1", "EZH2"]


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    prev = [x.split("\t") for x in Path("data/drug/lines.tsv").read_text().splitlines()[1:]]
    known = {r[0]: (r[1], r[2], r[3]) for r in prev}
    title, aid, urls = figshare_find(["DepMap 24Q4 Public", "DepMap Public"],
                                     ["OmicsExpressionProteinCodingGenesTPMLogp1.csv", "CRISPRGeneEffect.csv"])
    ids, genes, X = read_matrix(get(urls["OmicsExpressionProteinCodingGenesTPMLogp1.csv"]))
    sym = [g.split(" (")[0] for g in genes]
    gi = {g: j for j, g in enumerate(sym)}
    Z = (X - np.nanmean(X, 0)) / (np.nanstd(X, 0) + 1e-6)
    pick = lambda names: [gi[g] for g in names if g in gi]
    e, m, s = pick(EPI), pick(MES), pick(STEM)
    E, M, S = np.nanmean(Z[:, e], 1), np.nanmean(Z[:, m], 1), np.nanmean(Z[:, s], 1)
    n = 0
    with open(OUT / "scores.tsv", "w") as f:
        f.write("line\tlineage\ttilt\tproliferation\tepithelial\tmesenchymal\temt\tstemness\n")
        for k, line in enumerate(ids):
            if line not in known:
                continue
            lin, tilt, prol = known[line]
            f.write(f"{line}\t{lin}\t{tilt}\t{prol}\t{E[k]:.4f}\t{M[k]:.4f}\t{M[k] - E[k]:.4f}\t{S[k]:.4f}\n")
            n += 1
    cids, cg, E2 = read_matrix(get(urls["CRISPRGeneEffect.csv"]))
    cj = {g.split(" (")[0]: j for j, g in enumerate(cg)}
    mi = [cj[g] for g in MODULE if g in cj]
    with open(OUT / "depmap_module.tsv", "w") as f:
        f.write("line\t" + "\t".join(g for g in MODULE if g in cj) + "\n")
        for k, line in enumerate(cids):
            if line in known:
                f.write(line + "\t" + "\t".join(f"{E2[k, j]:.4f}" for j in mi) + "\n")
    (OUT / "source.json").write_text(json.dumps(
        {"depmap": f"{title} (figshare {aid})", "lines": n,
         "genes_found": {"epithelial": len(e), "mesenchymal": len(m), "stemness": len(s),
                         "depmap_module": [g for g in MODULE if g in cj]},
         "genes_missing": {"epithelial": [g for g in EPI if g not in gi],
                           "mesenchymal": [g for g in MES if g not in gi],
                           "stemness": [g for g in STEM if g not in gi]}}, indent=1))
    print(n, "lines", len(e), len(m), len(s), "genes", flush=True)


if __name__ == "__main__":
    main()
