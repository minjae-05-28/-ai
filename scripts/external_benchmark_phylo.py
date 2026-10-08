"""External benchmark 2: LECA against Vosseberg et al. 2021 (Nat Ecol Evol 5:92) gene-tree LECA families.

    python scripts/external_benchmark_phylo.py
        reads  results/external/vosseberg2021/leca_families.tsv and the *.tar.gz.names.txt member lists
        writes results/external_benchmark/phylogenetic.json

Follows docs/preregistration/2026-10-08_external_benchmark_phylogenetic.md, committed before their data was
downloaded:
    families   Pfam accessions (version dropped) they built a tree for, intersected with ours
    label      1 if leca_families.tsv holds a LECA family from that Pfam
    primary    AUROC of our LECA v2 posterior (minimum over roots) against present-day frequency;
               2,000-resample family bootstrap, seed 0; above zero positive, below negative, else draw
    secondary  frequency-stratified AUROC (deciles, weighted by family count); LECA v1 and each root;
               precision, recall and Jaccard of P >= 0.9
"""

import json
import re
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
from external_benchmark import compare, load  # noqa: E402
from organelle_evo.predict import auroc  # noqa: E402

SRC = Path("results/external/vosseberg2021")
OUT = Path("results/external_benchmark")
PF = re.compile(r"PF\d{5}")


def theirs():
    leca = set()
    for line in (SRC / "leca_families.tsv").read_text().splitlines()[1:]:
        leca.update(PF.findall(line.split("\t")[0]))  # Family_ID, e.g. PF00780_OG1.1
    tested = set()
    for f in SRC.glob("*.names.txt"):
        for line in f.read_text().splitlines():
            tested.update(PF.findall(Path(line).name))
    return leca, tested


def stratified(post, freq, y, seed=0, n=2000):
    edges = np.quantile(freq, np.linspace(0, 1, 11))
    bins = np.clip(np.searchsorted(edges, freq, side="right") - 1, 0, 9)

    def score(ix):
        tot, w = 0.0, 0
        for b in range(10):
            m = ix[bins[ix] == b]
            if len(m) and y[m].min() != y[m].max():
                tot += auroc(post[m], y[m]) * len(m)
                w += len(m)
        return tot / w if w else np.nan

    est = score(np.arange(len(y)))
    rng = np.random.default_rng(seed)
    bs = [score(rng.integers(0, len(y), len(y))) for _ in range(n)]
    lo, hi = np.nanpercentile(bs, [2.5, 97.5])
    return {"weighted_auroc": round(float(est), 4), "ci95": [round(float(lo), 4), round(float(hi), 4)],
            "above_0.5": bool(lo > 0.5)}


def main():
    leca, tested = theirs()
    meta = json.loads(Path("data/eukaryotes/pfam_meta.json").read_text())
    acc = {n: m["accession"].split(".")[0] for n, m in meta.items()}
    fallback = not tested
    print(f"their LECA Pfams {len(leca)}, Pfams with a tree {len(tested)}" + ("  -> FALLBACK rule" if fallback else ""))
    res = {"source": "Vosseberg et al. 2021, Nat Ecol Evol 5:92, figshare 10.6084/m9.figshare.10069985 "
                     "(leca_families.tsv; tested Pfams from the tree-archive member names)",
           "preregistration": "docs/preregistration/2026-10-08_external_benchmark_phylogenetic.md",
           "their_leca_pfams": len(leca), "their_tested_pfams": len(tested), "fallback_rule_used": fallback,
           "leca_not_in_tested": len(leca - tested) if tested else None,
           "preregistered": {}, "secondary": {}}
    runs = {"LECA v2 (minimum over 4 roots)": ("results/clade_ancestor/leca2/posterior.npz", "posterior", True)}
    runs["LECA v1 (minimum over 2 roots)"] = ("results/clade_ancestor/leca/posterior.npz", "posterior", False)
    for r in ["discoba", "opisthokonta", "amorphea", "metamonada"]:
        runs[f"LECA v2, {r} root only"] = ("results/clade_ancestor/leca2/posterior.npz", f"root:{r}", False)
    for label, (path, which, pre) in runs.items():
        fams, post, freq = load(path, which)
        accs = [acc.get(f, "") for f in fams]
        universe = tested if tested else {a for a in accs if a}
        r = compare(accs, post, freq, leca, universe)
        keep = np.array([a in universe for a in accs])
        y = np.array([a in leca for a in np.array(accs)[keep]], dtype=float)
        r["frequency_stratified"] = stratified(post[keep], freq[keep], y)
        names = dict(zip(accs, fams))
        r["ours_only_examples"] = [names[a] for a in r["ours_only_examples"]]
        r["theirs_only_examples"] = [names[a] for a in r["theirs_only_examples"]]
        (res["preregistered"] if pre else res["secondary"])[label] = r
        print(f"\n{label}  [{'pre-registered' if pre else 'secondary'}]")
        print(f"  n={r['n_families_compared']} (LECA {r['n_in_their_node']})  AUROC ours {r['auroc_ours']} vs "
              f"frequency {r['auroc_present_day_frequency']}  diff {r['ours_minus_frequency']} -> {r['verdict']}")
        print(f"  stratified {r['frequency_stratified']}")
        print(f"  P>=0.9: ours {r['ours_p_ge_0.9']}, theirs {r['theirs']}, precision {r['precision']}, "
              f"recall {r['recall']}, Jaccard {r['jaccard']}")
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "phylogenetic.json").write_text(json.dumps(res, ensure_ascii=False, indent=1))
    print(f"\n-> {OUT}/phylogenetic.json")


if __name__ == "__main__":
    main()
