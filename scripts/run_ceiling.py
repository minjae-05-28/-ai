"""How high can a gene-loss prediction score go? Sibling-lineage ceiling.

    python scripts/run_ceiling.py

For every descendant whose ancestor proxy has other descendants with the same lifestyle
design in the same clade (siblings), predict its losses from the siblings' loss rate per
family. Siblings share the target's ancestor, lifestyle and much of its history, so this
"sibling oracle" approximates the best any model could do; what it still misses is
lineage-specific chance (drift) plus annotation noise.

Compared on the same targets with:
  memorisation (other clades)   loss rate of each family in parasites of other clades
  law                           eukaryote_axes_v3-style law transferred from other clades
                                (results/transfer heldout rows, when present)
The gap oracle - memorisation(other clades) is clade-specific history no cross-lineage law
can reach; 1 - oracle is chance.
"""

import json
from collections import defaultdict
from pathlib import Path

import numpy as np

from organelle_evo.eukaryotes import catalog as euk
from organelle_evo.eukaryotes.model import counts, family_features
from organelle_evo.predict import auroc
from organelle_evo.prokaryotes import catalog as pro


def load(dirname, skip=("pfam_meta.json", "family_annotations.json")):
    return {json.loads(f.read_text())["species"]: json.loads(f.read_text())
            for f in Path(dirname).glob("*.json") if f.name not in skip}


def run(profiles, pairs, key, other_ok):
    meta = json.loads(Path("data/eukaryotes/pfam_meta.json").read_text())
    fams, _ = family_features(list(profiles.values()), meta)
    c = {s: counts(p, fams) for s, p in profiles.items()}
    groups = defaultdict(list)
    for a, d in pairs:
        groups[key(a, d)].append((a, d))
    rows = []
    for (a, d) in pairs:
        sibs = [x for x in groups[key(a, d)] if x[1] != d]
        if not sibs:
            continue
        n, m = c[a], c[d]
        had = n > 0
        lost = (m == 0)[had]
        if lost.all() or not lost.any():
            continue
        oracle = np.mean([(c[s] == 0)[had] for _, s in sibs], axis=0)
        others = [(c[x], c[y]) for x, y in pairs if other_ok(a, d, x, y)]
        idx = np.flatnonzero(had)
        memo = np.array([np.mean([om[j] == 0 for on, om in others if on[j] > 0]) if any(on[j] > 0 for on, _ in others) else 0.5
                         for j in idx])
        one = [auroc((c[s] == 0)[had].astype(float), lost) for _, s in sibs]
        rows.append({"pair": f"{a} -> {d}", "n_siblings": len(sibs), "sibling_oracle": auroc(oracle, lost),
                     "best_single_sibling": float(max(one)), "memorisation_other_clades": auroc(memo, lost)})
    return rows


def summary(rows, name, law=None):
    keys = ("sibling_oracle", "best_single_sibling", "memorisation_other_clades")
    mean = {k: float(np.mean([r[k] for r in rows])) for k in keys}
    if law:
        ls = [law[r["pair"]] for r in rows if r["pair"] in law]
        mean["law_other_clades"] = float(np.mean(ls)) if ls else None
        mean["n_with_law"] = len(ls)
    print(f"\n{name} ({len(rows)} targets with siblings): " + ", ".join(
        f"{k} {v:.3f}" if isinstance(v, float) else f"{k} {v}" for k, v in mean.items()))
    return {"mean_auroc": mean, "targets": rows}


def main():
    res = {}
    E = load("data/eukaryotes")
    clade = lambda s: euk.SPECIES[s].group.split("_")[0]  # noqa: E731
    epairs = [(a, d) for a, d in euk.resolve_pairs(E) if euk.design(d)[1]]
    rows = run(E, epairs, lambda a, d: (a, euk.design(d), clade(d)), lambda a, d, x, y: clade(y) != clade(d))
    law = {}
    t = Path("results/transfer/metrics.json")
    if t.exists():
        law = {r["pair"]: r["law"] for r in json.loads(t.read_text()).get("heldout", [])}
    res["parasites"] = summary(rows, "parasites", law)

    P = load("data/prokaryotes")
    ppairs = pro.resolve_pairs(P)
    rows = run(P, ppairs, lambda a, d: a, lambda a, d, x, y: x != a)
    res["extremophiles"] = summary(rows, "extremophiles (siblings share the ancestor, environments differ)")

    for k, v in res.items():
        m = v["mean_auroc"]
        print(f"{k}: chance (1 - oracle) {1 - m['sibling_oracle']:.3f}; clade-specific history "
              f"(oracle - memorisation from other lineages) {m['sibling_oracle'] - m['memorisation_other_clades']:.3f}")
    out = Path("results/ceiling")
    out.mkdir(parents=True, exist_ok=True)
    (out / "metrics.json").write_text(json.dumps(res, indent=2))
    print(f"Done -> {out}/")


if __name__ == "__main__":
    main()
