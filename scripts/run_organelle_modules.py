"""Which organelle and endosymbiont genes are lost together?

    python scripts/run_organelle_modules.py [--k 2]

run_gaps.py showed that, unlike in parasites, co-loss modules improve prediction in
mitochondria, plastids and insect endosymbionts. This fits the rank-k module model to
every lineage of each system and names each module by the genes at its loss end and
the lineages that lost it.
"""

import argparse
import json
import sys
from pathlib import Path

import numpy as np
import torch

sys.path.insert(0, str(Path(__file__).resolve().parent))
from run_nestedness import load_system  # noqa: E402
from run_realdata import CATALOG  # noqa: E402

from organelle_evo.eukaryotes.modules import fit_modules  # noqa: E402
from organelle_evo.laws import LAWS_DIR, save_law  # noqa: E402
from organelle_evo.realdata.genes import functional_class  # noqa: E402


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--k", type=int, default=2)
    args = ap.parse_args()
    torch.set_num_threads(2)
    out = Path("results/organelle_modules")
    out.mkdir(parents=True, exist_ok=True)
    cache = json.loads(Path("data/processed/homology.json").read_text()) if Path("data/processed/homology.json").exists() else {}
    result = {}
    for system in CATALOG:
        ds, _ = load_system(system, Path("data/raw"), cache)
        L = (~ds.present).astype(float)
        keep = (L.sum(0) > 0) & (L.sum(0) < len(L))
        genes = [g for g, k in zip(ds.genes, keep) if k]
        L = L[:, keep]
        model = fit_modules(L, args.k, epochs=600)
        mods = []
        for m in np.argsort(-np.abs(model.u).sum(0)):
            u, v = model.u[:, m], model.v[:, m]
            if u.mean() < 0:  # orient: positive u = the lineage lost the module
                u, v = -u, -v
            top = np.argsort(-v)[:15]
            classes = {}
            for j in top:
                c = functional_class(genes[j])
                classes[c] = classes.get(c, 0) + 1
            lost_by = [ds.lineages[i] for i in np.argsort(-u)[:6]]
            mods.append({"genes": [genes[j] for j in top], "classes": classes, "lost_by": lost_by,
                         "strength": float(np.abs(model.u[:, m]).sum())})
            print(f"{system:20s} module: {', '.join(genes[j] for j in top[:10])}")
            print(f"{'':20s}   classes {classes}; lost most by {', '.join(lost_by[:4])}")
        result[system] = mods
    (out / "metrics.json").write_text(json.dumps(result, indent=2))
    gaps = json.loads(Path("results/gaps/metrics.json").read_text())["endosymbiosis_together"]
    save_law(LAWS_DIR / "organelle_modules_v1.json", id="organelle_modules_v1",
             scope="Genes that organelles and insect endosymbionts lose together (co-loss modules).",
             model=f"Logistic rank-{args.k} factorisation of gene loss per lineage; modules named by top-loading genes.",
             feature_names=[], data={s: len(v) for s, v in result.items()},
             validation={"hidden_half_auroc": gaps},
             caveats=["Modules can reflect shared function (complexes, operons) or shared phylogeny."],
             contexts={"modules": result})
    print(f"Done -> {out}/ and laws/organelle_modules_v1.json")


if __name__ == "__main__":
    main()
