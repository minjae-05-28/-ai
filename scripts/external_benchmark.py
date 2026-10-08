"""External benchmark: our ancestral reconstructions against Zmasek & Godzik 2011 (Genome Biol 12:R4).

    python scripts/external_benchmark.py
        reads  results/external/zmasek2011/gb-2011-12-1-r4-S4.zip (phyloXML: Pfam domains present at every
               ancestral node, Dollo parsimony over 114 eukaryote genomes, Pfam 24.0)
        writes results/external_benchmark/summary.json

Follows docs/preregistration/2026-10-08_external_benchmark.md, committed before their file was opened:
    families   Pfam names in both universes (theirs: any domain on their tree; ours: the families scored)
    label      1 if their ancestral node carries the domain
    primary    AUROC of our posterior (LECA: minimum over root positions) for their label, against the
               AUROC of present-day frequency in our sample; difference with a 2,000-resample bootstrap
               over families; above zero = positive, below = negative, holding zero = draw
    secondary  Jaccard, precision and recall of our P >= 0.9 list against their set
Anything beyond that is labelled exploratory in the output.
"""

import io
import json
import xml.etree.ElementTree as ET
import zipfile
from pathlib import Path

import numpy as np

from organelle_evo.predict import auroc

SRC = Path("results/external/zmasek2011/gb-2011-12-1-r4-S4.zip")
OUT = Path("results/external_benchmark")
NS = {"p": "http://www.phyloxml.org"}


def their_nodes():
    with zipfile.ZipFile(SRC) as z:
        xml = z.read([n for n in z.namelist() if n.endswith(".xml")][0])
    root = ET.parse(io.BytesIO(xml)).getroot()
    nodes, universe = {}, set()

    def walk(c, path):
        name = c.find("p:taxonomy/p:scientific_name", NS)
        name = name.text if name is not None else "?"
        bc = c.find("p:binary_characters/p:present", NS)
        present = {e.text for e in bc.findall("p:bc", NS)} if bc is not None else set()
        universe.update(present)
        nodes.setdefault(name, present)
        for k in c.findall("p:clade", NS):
            walk(k, path + [name])

    walk(root.find("p:phylogeny/p:clade", NS), [])
    return nodes, universe


def compare(fams, post, freq, theirs, universe, seed=0):
    keep = [i for i, f in enumerate(fams) if f in universe]
    f = [fams[i] for i in keep]
    p, q = post[keep], freq[keep]
    y = np.array([x in theirs for x in f], dtype=float)
    a_ours, a_freq = float(auroc(p, y)), float(auroc(q, y))
    rng = np.random.default_rng(seed)
    diffs = []
    for _ in range(2000):
        ix = rng.integers(0, len(y), len(y))
        if y[ix].min() == y[ix].max():
            continue
        diffs.append(auroc(p[ix], y[ix]) - auroc(q[ix], y[ix]))
    lo, hi = np.percentile(diffs, [2.5, 97.5])
    ours = {x for x, v in zip(f, p) if v >= 0.9}
    th = {x for x in f if x in theirs}
    inter = ours & th
    verdict = "양성" if lo > 0 else ("음성" if hi < 0 else "무승부")
    top_ours_only = sorted(((v, x) for x, v in zip(f, p) if x not in theirs and v >= 0.9), reverse=True)[:25]
    top_theirs_only = sorted(((v, x) for x, v in zip(f, p) if x in theirs and v < 0.1))[:25]
    return {
        "n_families_compared": len(f), "n_in_their_node": int(y.sum()),
        "auroc_ours": round(a_ours, 4), "auroc_present_day_frequency": round(a_freq, 4),
        "ours_minus_frequency": {"mean": round(a_ours - a_freq, 4), "ci95": [round(float(lo), 4), round(float(hi), 4)]},
        "verdict": verdict,
        "ours_p_ge_0.9": len(ours), "theirs": len(th),
        "jaccard": round(len(inter) / max(len(ours | th), 1), 4),
        "precision": round(len(inter) / max(len(ours), 1), 4), "recall": round(len(inter) / max(len(th), 1), 4),
        "ours_only_examples": [x for _, x in top_ours_only], "theirs_only_examples": [x for _, x in top_theirs_only],
    }


def load(path, which="posterior"):
    z = np.load(path, allow_pickle=False)
    fams = [str(x) for x in z["families"]]
    if which == "core":
        j = int(np.argmax(z["child_n_tips"]))
        post = z["child_posteriors"][j]
    elif which.startswith("root:"):
        roots = [str(r) for r in z["roots"]]
        post = z["per_root"][roots.index(which[5:])]
    else:
        post = z[which]
    return fams, post, z["clade_frequency"]


def main():
    nodes, universe = their_nodes()
    print(f"their tree: {len(nodes)} named nodes, {len(universe)} domains; LECA {len(nodes['Eukaryota'])}, "
          f"Fungi {len(nodes.get('Fungi', ()))}")
    res = {"source": "Zmasek & Godzik 2011, Genome Biol 12:R4, Additional file 4 (Dollo parsimony, Pfam 24.0, "
                     "114 genomes); their tree is rooted between Unikonta and Bikonta",
           "preregistration": "docs/preregistration/2026-10-08_external_benchmark.md",
           "preregistered": {}, "exploratory": {}}
    runs = {
        "LECA v2 (minimum over 4 roots) vs their Eukaryota": ("results/clade_ancestor/leca2/posterior.npz",
                                                              "posterior", "Eukaryota", True),
        "LECA v1 (minimum over 2 roots) vs their Eukaryota": ("results/clade_ancestor/leca/posterior.npz",
                                                              "posterior", "Eukaryota", True),
        "Fungi (our root, Rozella included) vs their Fungi": ("results/clade_ancestor/fungi/posterior.npz",
                                                             "posterior", "Fungi", True),
        # Exploratory: matched to their root position, and our core-fungi node.
        "LECA v2, Amorphea root only (their root) vs their Eukaryota": (
            "results/clade_ancestor/leca2/posterior.npz", "root:amorphea", "Eukaryota", False),
        "Core fungi (Rozella lineage excluded) vs their Fungi": (
            "results/clade_ancestor/fungi/posterior.npz", "core", "Fungi", False),
    }
    for label, (path, which, node, pre) in runs.items():
        if not Path(path).exists() or node not in nodes:
            continue
        fams, post, freq = load(path, which)
        r = compare(fams, post, freq, nodes[node], universe)
        (res["preregistered"] if pre else res["exploratory"])[label] = r
        print(f"\n{label}  [{'pre-registered' if pre else 'exploratory'}]")
        print(f"  n={r['n_families_compared']} (theirs {r['n_in_their_node']})  AUROC ours {r['auroc_ours']} vs "
              f"frequency {r['auroc_present_day_frequency']}  diff {r['ours_minus_frequency']}  -> {r['verdict']}")
        print(f"  P>=0.9: ours {r['ours_p_ge_0.9']}, theirs {r['theirs']}, Jaccard {r['jaccard']}, "
              f"precision {r['precision']}, recall {r['recall']}")
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "summary.json").write_text(json.dumps(res, ensure_ascii=False, indent=1))
    print(f"\n-> {OUT}/summary.json")


if __name__ == "__main__":
    main()
