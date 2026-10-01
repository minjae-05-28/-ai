"""Published laws of genome evolution, re-tested on this project's data.

    python scripts/run_literature.py

Each law is stated as its authors stated it, with the source, then tested here where the
data allow. Verdicts: consistent / partly / contradicted / not testable here.
Writes laws/literature/laws.json (the registry is written by hand from these results) and results/literature/metrics.json.
"""

import json
import sys
from pathlib import Path

import numpy as np
from scipy.stats import spearmanr

sys.path.insert(0, str(Path(__file__).resolve().parent))
from run_nestedness import load_system  # noqa: E402

from organelle_evo.eukaryotes.catalog import SPECIES as EUK, resolve_pairs as euk_pairs  # noqa: E402
from organelle_evo.eukaryotes.model import counts, family_features  # noqa: E402
from organelle_evo.laws import LAWS_DIR, load_law  # noqa: E402
from organelle_evo.prokaryotes.catalog import SPECIES as PRO  # noqa: E402

ANN = json.loads(Path("data/eukaryotes/family_annotations.json").read_text())
META = json.loads(Path("data/eukaryotes/pfam_meta.json").read_text())
SLIM = {v["name"]: k for k, v in ANN["slims"].items()}
rng = np.random.default_rng(0)


def fams_with(*slim_names):
    ids = {SLIM[n] for n in slim_names}
    return {f for f, a in ANN["families"].items() if ids & set(a.get("go_slim", ()))}


def load_profiles(d):
    out = {}
    for f in Path(d).glob("*.json"):
        if f.name in ("pfam_meta.json", "family_annotations.json"):
            continue
        p = json.loads(f.read_text())
        out[p["species"]] = p
    return out


def genes_in(p, fams):
    return sum(v[0] for f, v in p["families"].items() if f in fams)


def slope_ci(x, y, n=2000):
    b = np.polyfit(x, y, 1)[0]
    bs = []
    for _ in range(n):
        i = rng.integers(0, len(x), len(x))
        bs.append(np.polyfit(x[i], y[i], 1)[0])
    return float(b), [float(v) for v in np.percentile(bs, [2.5, 97.5])]


def scaling(pro):
    """van Nimwegen 2003: genes per functional category scale as N^alpha."""
    cats = {
        "transcription_regulation": fams_with("regulation of DNA-templated transcription", "transcription regulator activity"),
        "signal_transduction": fams_with("signaling", "molecular transducer activity"),
        "metabolism": fams_with("carbohydrate metabolic process", "nucleobase-containing small molecule metabolic process",
                                "sulfur compound metabolic process", "vitamin metabolic process"),
        "translation": fams_with("ribosome", "cytoplasmic translation"),
    }
    N = np.log([p["n_genes"] for p in pro.values()])
    res = {}
    for k, fs in cats.items():
        y = np.log([max(genes_in(p, fs), 1) for p in pro.values()])
        res[k] = slope_ci(N, y)
    return res


def black_queen(pro):
    """Morris, Lenski & Zinser 2012: streamlined oligotrophs drop leaky functions such as H2O2 removal."""
    detox = {"Catalase", "Catalase_C", "peroxidase"}
    pairs = [("Synechococcus elongatus", "Prochlorococcus marinus"), ("Cereibacter sphaeroides", "Candidatus Pelagibacter ubique"),
             ("Synechococcus elongatus", "Synechococcus sp. WH 8102"), ("Nitrososphaera viennensis", "Nitrosopumilus maritimus"),
             ("Sphingobium japonicum", "Sphingopyxis alaskensis"), ("Cupriavidus necator", "Polynucleobacter asymbioticus")]
    rows = []
    for a, d in pairs:
        if a in pro and d in pro:
            rows.append({"relative": a, "oligotroph": d, "relative_detox_genes": genes_in(pro[a], detox),
                         "oligotroph_detox_genes": genes_in(pro[d], detox)})
    return rows


def streamlining(pro):
    """Giovannoni et al. 2014: oligotrophs have small genomes and few regulators."""
    tf = fams_with("regulation of DNA-templated transcription", "transcription regulator activity")
    rows = []
    for s, p in pro.items():
        rows.append({"species": s, "oligo": PRO[s].oligo if s in PRO else 0, "genes": p["n_genes"],
                     "tf_per_1000_genes": 1000 * genes_in(p, tf) / p["n_genes"]})
    olig = [r for r in rows if r["oligo"]]
    rest = [r for r in rows if not r["oligo"]]
    return {"oligotrophs": olig, "median_genes": [float(np.median([r["genes"] for r in olig])), float(np.median([r["genes"] for r in rest]))],
            "median_tf_per_1000": [float(np.median([r["tf_per_1000_genes"] for r in olig])), float(np.median([r["tf_per_1000_genes"] for r in rest]))]}


def plastid_order():
    """Wicke & Naumann 2018 / Graham et al. 2017: when a plant becomes parasitic, its plastome
    degrades ndh -> photosynthesis & plastid RNA polymerase -> ATP synthase -> housekeeping.
    Tested as in the classic comparison: Epifagus (holoparasite) against tobacco, on the genes
    tobacco carries."""
    ds, _ = load_system("plastid", Path("data/raw"), json.loads(Path("data/processed/homology.json").read_text()))
    stages = [("ndh", ("ndh",)), ("photosynthesis_and_PEP", ("psa", "psb", "pet", "rbc", "rpo")), ("atp_synthase", ("atp",)),
              ("housekeeping", ("rpl", "rps", "clpp", "accd", "infa", "matk", "ycf1", "ycf2"))]
    lin = {name: i for i, name in enumerate(ds.lineages)}
    ref = ds.present[next(i for n, i in lin.items() if n.startswith("Nicotiana"))]
    par = ds.present[next(i for n, i in lin.items() if n.startswith("Epifagus"))]
    out = {}
    for name, pref in stages:
        ix = [i for i, g in enumerate(ds.genes) if g.lower().startswith(pref) and ref[i]]
        out[name] = {"genes_in_tobacco": len(ix), "share_lost_in_epifagus": float(1 - par[ix].mean()) if ix else None}
    shares = [out[n]["share_lost_in_epifagus"] for n, _ in stages]
    out["monotone_with_stage"] = all(shares[i] >= shares[i + 1] - 0.05 for i in range(len(shares) - 1))
    return out


def krylov(euk):
    """Krylov et al. 2003: genes with low dispensability / high conservation have low propensity for loss."""
    fams, _ = family_features(list(euk.values()), META)
    c = {s: counts(p, fams) for s, p in euk.items()}
    free = [s for s in c if s in EUK and EUK[s].lifestyle == "free_living"]
    ubiq = np.mean([c[s] > 0 for s in free], 0)
    pairs = [(a, d) for a, d in euk_pairs(euk) if EUK[d].lifestyle == "parasite"]
    had = np.array([c[a] > 0 for a, _ in pairs])
    lost = np.array([(c[a] > 0) & (c[d] == 0) for a, d in pairs])
    n_had = had.sum(0)
    ok = n_had >= 5
    rate = lost.sum(0)[ok] / n_had[ok]
    rho = spearmanr(ubiq[ok], rate).correlation
    q = np.quantile(ubiq[ok], [0.25, 0.75])
    return {"spearman_ubiquity_vs_loss_rate": float(rho), "families": int(ok.sum()),
            "loss_rate_least_ubiquitous_quartile": float(rate[ubiq[ok] <= q[0]].mean()),
            "loss_rate_most_ubiquitous_quartile": float(rate[ubiq[ok] >= q[1]].mean())}


def universal_retention():
    """Giannakis et al. 2022: the same gene features predict retention in mitochondria and plastids."""
    cache = json.loads(Path("data/processed/homology.json").read_text())
    data = {}
    for s in ("mitochondrion", "plastid"):
        ds, _ = load_system(s, Path("data/raw"), cache)
        data[s] = (ds.features, ds.present.mean(0), list(ds.feature_names))
    out = {}
    for train, test in (("mitochondrion", "plastid"), ("plastid", "mitochondrion")):
        X, y, _ = data[train]
        Xt, yt, _ = data[test]
        A = np.c_[np.ones(len(X)), X]
        w = np.linalg.solve(A.T @ A + 1.0 * np.eye(A.shape[1]), A.T @ y)
        pred = np.c_[np.ones(len(Xt)), Xt] @ w
        out[f"{train}->{test}"] = float(spearmanr(pred, yt).correlation)
        # within-system reference: leave-one-gene-out
        At = np.c_[np.ones(len(Xt)), Xt]
        loo = []
        for i in range(len(Xt)):
            m = np.ones(len(Xt), bool)
            m[i] = False
            wi = np.linalg.solve(At[m].T @ At[m] + np.eye(At.shape[1]), At[m].T @ yt[m])
            loo.append(At[i] @ wi)
        out[f"{test} within"] = float(spearmanr(loo, yt).correlation)
    return out


def hydrophobicity():
    """von Heijne 1986 / Björkholm et al. 2015: hydrophobic proteins stay in the organelle (hard to import)."""
    law = load_law("endosymbiosis_v1")
    out = {}
    for ctx in law.weights:
        for f in ("hydrophobicity_gravy", "tm_helices"):
            j = law.feature_names.index(f)
            lo, hi = law.ci95[ctx][j]
            out[f"{ctx}:{f}"] = {"loss_weight": float(law.weights[ctx][j]), "ci95": [float(lo), float(hi)]}
    return out


def main():
    out_dir = Path("results/literature")
    out_dir.mkdir(parents=True, exist_ok=True)
    pro, euk = load_profiles("data/prokaryotes"), load_profiles("data/eukaryotes")
    r = {"scaling": scaling(pro), "black_queen": black_queen(pro), "streamlining": streamlining(pro),
         "plastid_order": plastid_order(), "krylov": krylov(euk), "universal_retention": universal_retention(),
         "hydrophobicity": hydrophobicity()}
    (out_dir / "metrics.json").write_text(json.dumps(r, indent=2, default=float))
    for k, v in r.items():
        print(f"== {k}")
        print(json.dumps(v, default=float)[:900])


if __name__ == "__main__":
    main()
