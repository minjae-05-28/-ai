"""Per-sample unicellular tilt for every TCGA primary tumour and normal, with stage (pre-registration 20,
docs/preregistration/2026-10-16_cancer_atavism_stage.md). Runs on a GitHub runner; only per-sample scores are kept.

    data/tcga_stage/<COHORT>.tsv   sample, kind (tumour/normal), stage (1-4 or blank), delta, s, i, t
    data/tcga_stage/manifest.json
"""

import gzip
import json
import re
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import cancer_atavism as ca  # noqa: E402
from cancer_composition import IMMUNE, STROMAL  # noqa: E402
from cancer_proliferation import load_p  # noqa: E402
from tcga_fetch import COHORTS, get  # noqa: E402

OUT = Path("data/tcga_stage")
EXPR = "https://tcga.xenahubs.net/download/TCGA.{c}.sampleMap/HiSeqV2.gz"
CLIN = "https://tcga.xenahubs.net/download/TCGA.{c}.sampleMap/{c}_clinicalMatrix"
MIN_NORMALS = 10


def stage_number(text):
    m = re.match(r"\s*stage\s+(iv|iii|ii|i)(?![v])", (text or "").lower())
    return {"i": 1, "ii": 2, "iii": 3, "iv": 4}[m.group(1)] if m else None


def stages(c):
    raw = get(CLIN.format(c=c))
    if raw is None:
        return {}, None
    lines = raw.decode(errors="replace").splitlines()
    head = lines[0].split("\t")
    col = next((x for x in ("pathologic_stage", "clinical_stage") if x in head), None)
    if col is None:
        return {}, None
    j = head.index(col)
    out = {}
    for line in lines[1:]:
        x = line.split("\t")
        if len(x) > j:
            k = stage_number(x[j])
            if k:
                out[x[0][:12]] = k
    return out, col


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    ages = ca.load_ages()
    go, hall, _ = load_p()
    P = go | hall
    manifest = {}
    for c in COHORTS:
        raw = get(EXPR.format(c=c))
        if raw is None:
            manifest[c] = {"error": "download failed"}
            continue
        lines = gzip.decompress(raw).decode().splitlines()
        samples = lines[0].split("\t")[1:]
        code = [s[13:15] if len(s) >= 15 else "" for s in samples]
        nor = [j for j, k in enumerate(code) if k == "11"]
        seen, tum = set(), []
        for j, k in enumerate(code):
            if k == "01" and samples[j][:12] not in seen:
                seen.add(samples[j][:12])
                tum.append(j)
        manifest[c] = {"tumours": len(tum), "normals": len(nor)}
        if len(nor) < MIN_NORMALS:
            continue
        genes, X = [], []
        for line in lines[1:]:
            x = line.split("\t")
            genes.append(x[0])
            X.append([float(a) if a not in ("", "NA") else np.nan for a in x[1:]])
        X = np.array(X, dtype=np.float32).T                      # samples x genes
        ref = np.nanmean(X[nor], 0)
        tmean = np.nanmean(X[tum], 0)
        gset = np.array(genes)
        expressed = (ref >= 1) | (tmean >= 1)
        is_p = np.isin(gset, list(P)) & expressed
        imm, stro = np.isin(gset, IMMUNE), np.isin(gset, STROMAL)
        keep = np.array([g in ages for g in genes]) & expressed & ~is_p & ~imm & ~stro
        age = np.array([ages[g][0] if g in ages else 0 for g in genes])
        uc, mc = keep & (age <= 3), keep & (age > 3)
        cuts = np.quantile(ref[keep], np.linspace(0, 1, 11)[1:-1])
        dec = np.searchsorted(cuts, ref, side="right")
        L = np.empty((len(tum) + len(nor), len(genes)), np.float32)
        L[:len(tum)] = X[tum] - ref
        n_nor = len(nor)
        for k, j in enumerate(nor):                             # normals against the mean of the other normals
            L[len(tum) + k] = X[j] - (ref * n_nor - X[j]) / (n_nor - 1)
        d = ca.delta_per_patient(L, uc, mc, dec)
        s = np.nanmean(L[:, is_p], 1)
        i = np.nanmean(L[:, imm], 1)
        t = np.nanmean(L[:, stro], 1)
        st, col = stages(c)
        manifest[c].update(stage_column=col, staged_tumours=sum(samples[j][:12] in st for j in tum))
        rows = ["sample\tkind\tstage\tdelta\ts\ti\tt"]
        for k, j in enumerate(tum + nor):
            kind = "tumour" if k < len(tum) else "normal"
            sg = st.get(samples[j][:12], "") if kind == "tumour" else ""
            rows.append(f"{samples[j]}\t{kind}\t{sg}\t{d[k]:.5f}\t{s[k]:.5f}\t{i[k]:.5f}\t{t[k]:.5f}")
        (OUT / f"{c}.tsv").write_text("\n".join(rows) + "\n")
        print(c, manifest[c], flush=True)
    (OUT / "manifest.json").write_text(json.dumps(manifest, indent=1))


if __name__ == "__main__":
    main()
