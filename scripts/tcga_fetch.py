"""Paired tumour / normal expression from the UCSC Xena TCGA hub, reduced on a GitHub runner
(pre-registration 17, docs/preregistration/2026-10-16_cancer_atavism.md).

    data/tcga/<COHORT>.npz   genes, patients, lfc (tumour - normal, log2, float16, patients x genes),
                             normal_mean, tumour_mean (over the paired patients)
    data/tcga/manifest.json  pairs per cohort, including cohorts below 10 pairs (not saved)

Quality control (pre-registration 17, deviation 1; written before any data was seen), saved separately as
data/tcga_qc/<COHORT>.npz with the same fields, plus data/tcga_qc/manifest.json:
  1. swapped / low-purity pairs: on the 1,000 most variable genes (all tumour and normal samples of the cohort),
     a pair is dropped if its normal correlates better with the tumour centroid than with the normal centroid,
     or its tumour better with the normal centroid (centroids leave the sample out);
  2. genes missing in more than 10% of pairs are dropped;
  3. pairs whose LFC size (median |LFC|) is more than 3 MADs above the cohort median are dropped;
  the 10-pair minimum is applied after QC.

Aggregate public expression only; patients are kept as TCGA barcodes, nothing else about them.
"""

import gzip
import io
import json
import time
import urllib.request
from pathlib import Path

import numpy as np

OUT = Path("data/tcga")
OUT_QC = Path("data/tcga_qc")
HUB = "https://tcga.xenahubs.net/download/TCGA.{c}.sampleMap/HiSeqV2.gz"
COHORTS = ["ACC", "BLCA", "BRCA", "CESC", "CHOL", "COAD", "DLBC", "ESCA", "GBM", "HNSC", "KICH", "KIRC", "KIRP",
           "LAML", "LGG", "LIHC", "LUAD", "LUSC", "MESO", "OV", "PAAD", "PCPG", "PRAD", "READ", "SARC", "SKCM",
           "STAD", "TGCT", "THCA", "THYM", "UCEC", "UCS", "UVM"]
MIN_PAIRS = 10


def get(url, tries=5):
    for i in range(tries):
        try:
            with urllib.request.urlopen(url, timeout=600) as r:
                return r.read()
        except Exception as e:
            print(f"attempt {i + 1} {url}: {e}", flush=True)
            time.sleep(15 * (i + 1))
    return None


def pairs(samples):
    """patient -> (tumour column, normal column): first primary tumour (01) and first solid normal (11)."""
    tum, nor = {}, {}
    for j, s in enumerate(samples):
        if len(s) < 15:
            continue
        pat, code = s[:12], s[13:15]
        if code == "01":
            tum.setdefault(pat, j)
        elif code == "11":
            nor.setdefault(pat, j)
    return {p: (tum[p], nor[p]) for p in sorted(tum) if p in nor}


def qc(T, N):
    """T, N: patients x genes (paired). Returns kept-pair mask, kept-gene mask and counts per rule."""
    ok_gene = np.isnan(T - N).mean(0) <= 0.10
    X = np.vstack([T, N])[:, ok_gene]
    X = np.where(np.isnan(X), np.nanmean(X, 0), X)
    top = np.argsort(np.var(X, 0))[::-1][:1000]
    X = X[:, top]
    n = len(T)
    Tt, Nn = X[:n], X[n:]

    def closer_to_other(own, other):
        out = np.zeros(n, bool)
        so, sx = own.sum(0), other.mean(0)
        for i in range(n):
            c_own = (so - own[i]) / (n - 1)
            out[i] = np.corrcoef(own[i], sx)[0, 1] > np.corrcoef(own[i], c_own)[0, 1]
        return out
    swapped = closer_to_other(Nn, Tt) | closer_to_other(Tt, Nn)
    size = np.nanmedian(np.abs(T - N)[:, ok_gene], 1)
    med = np.median(size)
    mad = np.median(np.abs(size - med)) or 1e-9
    extreme = size > med + 3 * mad
    keep = ~swapped & ~extreme
    return keep, ok_gene, {"swapped_or_low_purity": int(swapped.sum()), "extreme_lfc": int((extreme & ~swapped).sum()),
                           "genes_dropped_missing": int((~ok_gene).sum())}


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    OUT_QC.mkdir(parents=True, exist_ok=True)
    manifest, manifest_qc = {}, {}
    for c in COHORTS:
        raw = get(HUB.format(c=c))
        if raw is None:
            manifest[c] = {"error": "download failed"}
            continue
        lines = gzip.decompress(raw).decode().splitlines()
        samples = lines[0].split("\t")[1:]
        pr = pairs(samples)
        manifest[c] = {"samples": len(samples), "pairs": len(pr)}
        print(c, manifest[c], flush=True)
        if len(pr) < MIN_PAIRS:
            continue
        genes, rows = [], []
        ti = np.array([t for t, _ in pr.values()])
        ni = np.array([n for _, n in pr.values()])
        for line in lines[1:]:
            x = line.split("\t")
            v = np.array([float(a) if a not in ("", "NA") else np.nan for a in x[1:]])
            genes.append(x[0])
            rows.append((v[ti], v[ni]))
        T = np.array([r[0] for r in rows]).T
        N = np.array([r[1] for r in rows]).T
        pats = np.array(list(pr))
        if not (OUT / f"{c}.npz").exists():
            np.savez_compressed(OUT / f"{c}.npz", genes=np.array(genes), patients=pats,
                                lfc=(T - N).astype(np.float16), normal_mean=np.nanmean(N, 0).astype(np.float32),
                                tumour_mean=np.nanmean(T, 0).astype(np.float32))
        keep, ok_gene, counts = qc(T, N)
        manifest_qc[c] = {"pairs_before": len(pr), "pairs_after": int(keep.sum()), **counts}
        print(c, "QC", manifest_qc[c], flush=True)
        if keep.sum() < MIN_PAIRS:
            continue
        T, N = T[keep][:, ok_gene], N[keep][:, ok_gene]
        np.savez_compressed(OUT_QC / f"{c}.npz", genes=np.array(genes)[ok_gene], patients=pats[keep],
                            lfc=(T - N).astype(np.float16), normal_mean=np.nanmean(N, 0).astype(np.float32),
                            tumour_mean=np.nanmean(T, 0).astype(np.float32))
    (OUT / "manifest.json").write_text(json.dumps(manifest, indent=1))
    (OUT_QC / "manifest.json").write_text(json.dumps(manifest_qc, indent=1))


if __name__ == "__main__":
    main()
