"""Paired tumour / normal expression from the UCSC Xena TCGA hub, reduced on a GitHub runner
(pre-registration 17, docs/preregistration/2026-10-16_cancer_atavism.md).

    data/tcga/<COHORT>.npz   genes, patients, lfc (tumour - normal, log2, float16, patients x genes),
                             normal_mean, tumour_mean (over the paired patients)
    data/tcga/manifest.json  pairs per cohort, including cohorts below 10 pairs (not saved)

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


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    manifest = {}
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
        np.savez_compressed(OUT / f"{c}.npz", genes=np.array(genes), patients=np.array(list(pr)),
                            lfc=(T - N).astype(np.float16), normal_mean=np.nanmean(N, 0).astype(np.float32),
                            tumour_mean=np.nanmean(T, 0).astype(np.float32))
    (OUT / "manifest.json").write_text(json.dumps(manifest, indent=1))


if __name__ == "__main__":
    main()
