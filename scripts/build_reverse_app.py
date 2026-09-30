"""Build the interactive ancestor reverse-tracer page (results/reverse_app.html).

    python scripts/build_reverse_app.py [--refit] [--out results/reverse_app.html]

Everything the browser needs is embedded: Pfam family features, every profiled
species' family counts, the axis law (fitted on all pairs, cached in
results/reverse_app_law.json) and the stored endosymbiosis laws. The page runs the
same Bayesian reverse birth-death reconstruction as eukaryotes/reverse.py in JS.
"""

import argparse
import json
from pathlib import Path

import numpy as np
import torch

from organelle_evo.eukaryotes.catalog import AXES, SPECIES, design, resolve_pairs
from organelle_evo.eukaryotes.model import FAMILY_FEATURES, counts, family_features, fit_bd, pfam_class
from organelle_evo.eukaryotes.reverse import MAX_COUNT
from organelle_evo.laws import load_law

DATA = Path("data/eukaryotes")
LABELS = ("base", *AXES)
CLASSES = FAMILY_FEATURES[3:]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--refit", action="store_true")
    ap.add_argument("--epochs", type=int, default=300)
    ap.add_argument("--out", default="results/reverse_app.html")
    args = ap.parse_args()
    torch.set_num_threads(4)

    meta = json.loads((DATA / "pfam_meta.json").read_text())
    profiles = {}
    for f in DATA.glob("*.json"):
        if f.name != "pfam_meta.json":
            d = json.loads(f.read_text())
            if d["species"] in SPECIES:
                profiles[d["species"]] = d
    fams, x = family_features(list(profiles.values()), meta)
    c = {s: counts(p, fams) for s, p in profiles.items()}
    pairs = resolve_pairs(profiles)

    law_path = Path("results/reverse_app_law.json")
    if args.refit or not law_path.exists() or json.loads(law_path.read_text()).get("n_pairs") != len(pairs):
        fit = fit_bd(x, [(c[a], c[d], design(d)) for a, d in pairs], LABELS, epochs=args.epochs)
        law_path.write_text(json.dumps({"n_pairs": len(pairs), "w_lam": fit.w_lam.tolist(),
                                        "w_mu": fit.w_mu.tolist(), "w_nu": fit.w_nu.tolist()}))
    law = json.loads(law_path.read_text())
    endo = load_law("endosymbiosis_v1")

    cls_names = list(CLASSES)
    fam_class = []
    for f in fams:
        cl = pfam_class(f, meta.get(f, {}).get("description", ""))
        fam_class.append(cls_names.index(cl) if cl in cls_names else -1)
    species = []
    for s, p in profiles.items():
        n = np.minimum(c[s], MAX_COUNT)
        nz = np.flatnonzero(n)
        sp = SPECIES[s]
        species.append({"name": s, "group": sp.group, "lifestyle": sp.lifestyle, "location": sp.location,
                        "energy": sp.energy, "idx": nz.tolist(), "n": n[nz].tolist(),
                        "families": int((c[s] > 0).sum())})
    data = {
        "K": MAX_COUNT,
        "features": list(FAMILY_FEATURES),
        "classes": cls_names,
        "fam": fams,
        "desc": [meta.get(f, {}).get("description", "")[:90] for f in fams],
        "cls": fam_class,
        "x": np.round(x, 3).ravel().tolist(),
        "species": species,
        "pairs": {d: a for a, d in pairs},
        "law": {k: law[k] for k in ("w_lam", "w_mu", "w_nu")},
        "endo": {ctx: endo.weights[ctx].tolist() for ctx in endo.weights},
    }
    template = Path(__file__).with_name("reverse_app_template.html").read_text()
    core = Path(__file__).with_name("reverse_core.js").read_text()
    html = template.replace("/*__CORE__*/", core).replace("__DATA__", json.dumps(data, separators=(",", ":")))
    Path(args.out).write_text(html)
    print(f"wrote {args.out} ({len(html) / 1e6:.1f} MB), {len(species)} species, {len(fams)} families")


if __name__ == "__main__":
    main()
