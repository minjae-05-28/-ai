"""A cell suited to the human body: predict it from the laws, then check it against reality.

    python scripts/run_human_cell.py

This is a retrodiction test, not a design. Human body sites (gut, skin, mouth, blood) are
written as environment vectors; the laws learned on *other* systems then predict what a cell
living there should look like. Real human commensals (prokaryotes.catalog.HUMAN_TARGETS,
never part of any training pair) are the answer key.

  1. Proteome composition. The pair-level sequence law (change in IVYWREL, charged-vs-polar,
     acidic excess, side-chain N per residue for a given environment change) is applied to a
     soil bacterium moving to each body site, and compared with what the commensals measure.
  2. Genome size. The severity law for host association (how much of an ancestor's gene set a
     host-associated lineage keeps) against the commensals' actual family counts.
  3. Gene content. Starting from free-living soil and water bacteria, the environment law
     ranks every family by loss probability for the move to the gut. Score: how well that
     ranking separates families the real gut commensals kept from the ones they lack (AUROC),
     against the loss-propensity baseline and memorisation.
  4. What the laws say the cell gains, keeps and drops, with the functions involved.
"""

import json
from pathlib import Path

import numpy as np
import torch

from organelle_evo.eukaryotes.features import enriched_features
from organelle_evo.eukaryotes.model import counts, family_features, fit_bd, loss_probability, offset_for_losses
from organelle_evo.laws import LAWS_DIR, save_law
from organelle_evo.predict import auroc
from organelle_evo.prokaryotes.catalog import (AXES, HUMAN_SITES, HUMAN_TARGETS, SPECIES, design, env_change,
                                               resolve_pairs)

DATA = Path("data/prokaryotes")
ANN = Path("data/eukaryotes")
LABELS = ("base", *AXES)
SOIL = ("Bacillus subtilis", "Pseudomonas putida", "Micrococcus luteus")
OUT = Path("results/human_cell")


def load():
    meta = json.loads((ANN / "pfam_meta.json").read_text())
    ann = json.loads((ANN / "family_annotations.json").read_text())
    prof = {json.loads(f.read_text())["species"]: json.loads(f.read_text()) for f in DATA.glob("*.json")}
    fams, _ = family_features(list(prof.values()), meta)
    c = {s: counts(p, fams) for s, p in prof.items()}
    fams, names, x = enriched_features(prof, meta, ann, c, free=list(prof))
    return prof, meta, fams, names, x, c


def composition(res):
    """Sequence law: predicted composition of a soil bacterium moved to each body site."""
    comp = {json.loads(f.read_text())["species"]: json.loads(f.read_text())
            for f in Path("data/composition/prokaryotes").glob("*.json")}
    law = json.loads(Path("results/sequence/metrics.json").read_text())["environment_pairs"]["by_statistic"]
    stats = ("ivywrel", "cvp", "acidic_excess", "n_side")
    out = {}
    for site, env in HUMAN_SITES.items():
        z = env_change(SPECIES["Bacillus subtilis"], env)
        pred, obs = {}, {}  # absolute values: B. subtilis plus the environment-driven change
        for k in stats:
            coef = law[k]["coef"]
            delta = sum(coef[a] * v for a, v in zip(("base", *AXES), z))
            pred[k] = round(comp["Bacillus subtilis"][k] + delta - coef["base"], 4)
        here = [s for s in HUMAN_TARGETS if s in comp and
                abs(SPECIES[s].temp - env.temp) <= 3 and SPECIES[s].aerobic == env.aerobic]
        for k in stats:
            if here:
                obs[k] = round(float(np.mean([comp[s][k] for s in here])), 4)
        out[site] = {"predicted": pred, "observed_commensals": obs, "n_commensals": len(here),
                     "commensals": here,
                     "errors": {k: round(pred[k] - obs[k], 4) for k in stats if k in obs}}
        print(f"\n{site}: {len(here)} commensals")
        for k in stats:
            o = obs.get(k)
            print(f"   {k:14s} predicted {pred[k]:.4f}" + (f"   measured {o:.4f}   error {pred[k] - o:+.4f}" if o is not None else ""))
    res["composition"] = out


def genome_size(res, prof):
    sev = json.loads(Path("results/gaps/metrics.json").read_text())["environment_how_much"]
    have = {s: prof[s]["n_genes"] for s in HUMAN_TARGETS if s in prof}
    free = [s for s in prof if s not in HUMAN_TARGETS and s in SPECIES]
    res["genome_size"] = {"commensal_genes": have,
                          "free_living_median": float(np.median([prof[s]["n_genes"] for s in free])),
                          "severity_reference": {k: v for k, v in sev.items() if not isinstance(v, dict)}}
    if have:
        print(f"\ngenome size: commensals median {np.median(list(have.values())):.0f} genes, "
              f"free-living median {np.median([prof[s]['n_genes'] for s in free]):.0f}")


def gene_content(res, prof, fams, names, x, c, epochs=300):
    """Rank families by predicted loss for soil -> gut; score against real gut commensals."""
    pairs = resolve_pairs(prof)
    train = [(c[a], c[d], design(a, d)) for a, d in pairs]
    law = fit_bd(x, train, LABELS, epochs=epochs)
    gut = HUMAN_SITES["gut lumen (anaerobic, nutrient-rich)"]
    meta = json.loads((ANN / "pfam_meta.json").read_text())
    desc = lambda j: f"{fams[j]}: {meta.get(fams[j], {}).get('description', '')}"  # noqa: E731
    targets = [s for s in HUMAN_TARGETS if s in c and SPECIES[s].aerobic == 0 and SPECIES[s].temp >= 36]
    rows, pred_cache = {}, {}
    for anc in SOIL:
        if anc not in c:
            continue
        z = env_change(SPECIES[anc], gut)
        wl, wm, _ = law.weights(z)
        a_lam = float(np.mean(law.a_lam))
        n = c[anc]
        had = n > 0
        p = np.zeros(len(fams))
        p[had] = loss_probability(n[had], x[had], wl, wm, a_lam, offset_for_losses(n[had], x[had], wl, wm, a_lam, had.sum() * 0.3))
        pred_cache[anc] = (had, p)
        rows[anc] = {"families_today": int(had.sum()),
                     "most_likely_lost": [desc(j) for j in np.argsort(-p * had)[:10]],
                     "most_likely_kept": [desc(j) for j in np.argsort(p + ~had * 9)[:10]]}
        print(f"\n{anc} -> gut: {had.sum()} families")
        print("   predicted to go:   " + "; ".join(r.split(':')[0] for r in rows[anc]['most_likely_lost'][:6]))
        print("   predicted to stay: " + "; ".join(r.split(':')[0] for r in rows[anc]['most_likely_kept'][:6]))
    # validation: does the ranking separate what gut commensals actually have?
    scores = {}
    for t in targets:
        aucs = {}
        for anc, (had, p) in pred_cache.items():
            j = np.flatnonzero(had)
            y = c[t][j] == 0  # the commensal lacks it
            if y.all() or not y.any():
                continue
            aucs[anc] = auroc(p[j], y)
            others = [s for s in c if s not in HUMAN_TARGETS]
            freq = np.array([np.mean([c[s][k] == 0 for s in others if c[s][k] >= 0]) for k in j])
            aucs[anc + " (memorisation)"] = auroc(freq, y)
            aucs[anc + " (rarity baseline)"] = auroc(-np.array([sum(c[s][k] > 0 for s in c) for k in j], dtype=float), y)
        scores[t] = aucs
        if aucs:
            best = ", ".join(f"{k.split(' (')[0][:12]}{'' if '(' not in k else ' ' + k.split('(')[1][:4]} {v:.3f}" for k, v in aucs.items())
            print(f"   vs {t}: {best}")
    res["gene_content"] = {"per_ancestor": rows, "validation_auroc": scores, "gut_commensals_tested": targets}


def main():
    torch.set_num_threads(4)
    res = {"sites": {k: dict(zip(("group", "temp", "nacl", "aerobic", "radiation", "oligo"), v)) for k, v in HUMAN_SITES.items()},
           "note": "Prediction from laws trained on other systems; human commensals are held out."}
    prof, meta, fams, names, x, c = load()
    print(f"{len(prof)} prokaryote profiles, {sum(s in prof for s in HUMAN_TARGETS)}/{len(HUMAN_TARGETS)} human commensals available")
    print("\n1. Proteome composition predicted for each body site")
    composition(res)
    print("\n2. Genome size")
    genome_size(res, prof)
    print("\n3. Gene content: soil bacterium -> gut, scored against real gut commensals")
    gene_content(res, prof, fams, names, x, c)
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "metrics.json").write_text(json.dumps(res, indent=2))
    save_law(LAWS_DIR / "human_cell_v1.json", id="human_cell_v1",
             scope="What the laws predict for a cell living in the human body, tested against real human commensals.",
             model="Sequence law for composition, severity law for genome size, environment birth-death law for gene content; "
                   "commensals are never in a training pair.",
             feature_names=[], data={"commensals": sorted(set(HUMAN_TARGETS) & set(prof))},
             validation={k: res[k] for k in ("composition", "genome_size", "gene_content") if k in res}, contexts={},
             caveats=["Body sites are coarse: temperature, salt, oxygen and nutrient level only.",
                      "Host-specific pressures (immune system, mucus, host metabolites) are not in the model.",
                      "Commensal genomes are real but their habitat values are approximate."])
    print(f"\nDone -> {OUT}/")


if __name__ == "__main__":
    main()
