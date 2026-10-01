"""Family-level sequence laws: which protein families carry temperature and salt adaptation?

    python scripts/run_family_sequence.py

Uses data/family_composition/prokaryotes (amino-acid counts of each Pfam family's domains).
For every relative -> extremophile pair and every family both carry:
    delta_f = statistic(descendant's family f) - statistic(relative's family f)
for IVYWREL (temperature) and acidic excess (salt).

  1. uniform or family-specific?  share of the variance of delta_f explained by the pair's
     proteome-wide shift (one number per pair)
  2. family sensitivity           per family, delta_f regressed on the environment change
                                  across pairs (families in >= MIN_PAIRS pairs)
  3. what predicts sensitivity    Spearman of the sensitivities with family features
                                  (hydrophobicity, TM helices, GO slims, keywords)
"""

import json
from pathlib import Path

import numpy as np
from scipy.stats import spearmanr

from organelle_evo.eukaryotes.features import enriched_features
from organelle_evo.eukaryotes.model import counts, family_features
from organelle_evo.laws import LAWS_DIR, save_law
from organelle_evo.prokaryotes import catalog as pro
from organelle_evo.sequence import AA

FC = Path("data/family_composition/prokaryotes")
MIN_RES = 80
MIN_PAIRS = 12
STATS = {
    "ivywrel": (lambda f: sum(f[a] for a in "IVYWREL"), "colder", -1),   # sensitivity per 30 C of warming
    "acidic_excess": (lambda f: f["D"] + f["E"] - f["K"] - f["R"], "saltier", 1),  # per 10% NaCl
}


def shares(row):
    c = np.array(row[2:], dtype=float)
    return None if c.sum() < MIN_RES else dict(zip(AA, c / c.sum()))


def main():
    comp = {}
    for f in FC.glob("*.json"):
        d = json.loads(f.read_text())
        comp[d["species"]] = {fam: shares(v) for fam, v in d["families"].items()}
    pairs = [(a, d) for a, d in pro.resolve_pairs(comp)]
    print(f"{len(comp)} species, {len(pairs)} pairs")

    # family features from the Pfam profiles
    meta = json.loads(Path("data/eukaryotes/pfam_meta.json").read_text())
    ann = json.loads(Path("data/eukaryotes/family_annotations.json").read_text())
    profiles = {json.loads(f.read_text())["species"]: json.loads(f.read_text()) for f in Path("data/prokaryotes").glob("*.json")}
    fams, _ = family_features(list(profiles.values()), meta)
    c = {s: counts(p, fams) for s, p in profiles.items()}
    fams, names, X = enriched_features(profiles, meta, ann, c, free=[s for s in profiles if s not in pro.CLIMATE_TARGETS])
    fidx = {f: i for i, f in enumerate(fams)}

    res = {"n_pairs": len(pairs)}
    for stat, (fn, axis, sign) in STATS.items():
        ax = 1 + pro.AXES.index(axis)
        deltas = {}  # family -> list of (pair index, delta)
        uni_num, uni_den = 0.0, 0.0
        for p, (a, d) in enumerate(pairs):
            ds = []
            for fam, sa in comp[a].items():
                sd = comp[d].get(fam)
                if sa is None or sd is None:
                    continue
                dv = fn(sd) - fn(sa)
                ds.append(dv)
                deltas.setdefault(fam, []).append((p, dv))
            if len(ds) > 20:
                ds = np.array(ds)
                uni_num += len(ds) * ds.mean() ** 2
                uni_den += (ds ** 2).sum()
        Z = np.array([pro.design(a, d) for a, d in pairs])
        sens = {}
        for fam, rows in deltas.items():
            if len(rows) < MIN_PAIRS:
                continue
            idx = [r[0] for r in rows]
            y = np.array([r[1] for r in rows])
            Zf = Z[idx][:, [0, ax]]
            if np.linalg.matrix_rank(Zf) < 2:
                continue
            b = np.linalg.lstsq(Zf, y, rcond=None)[0]
            sens[fam] = sign * float(b[1])
        sf = [f for f in sens if f in fidx]
        s = np.array([sens[f] for f in sf])
        feat = {}
        for j, nm in enumerate(names):
            col = X[[fidx[f] for f in sf], j]
            if col.std() > 0:
                feat[nm] = float(spearmanr(col, s).correlation)
        top_feat = sorted(feat.items(), key=lambda kv: -abs(kv[1]))[:10]
        desc = lambda f: f"{f}: {meta.get(f, {}).get('description', '')}"  # noqa: E731
        order = sorted(sens, key=lambda f: -sens[f])
        res[stat] = {"axis": axis, "uniform_share_of_family_variance": uni_num / uni_den if uni_den else None,
                     "families_tested": len(sens), "median_sensitivity": float(np.median(list(sens.values()))),
                     "share_positive": float(np.mean(np.array(list(sens.values())) > 0)),
                     "most_sensitive": [(desc(f), round(sens[f], 4)) for f in order[:12]],
                     "least_sensitive": [(desc(f), round(sens[f], 4)) for f in order[-12:]],
                     "feature_correlations": top_feat}
        print(f"\n== {stat} ({axis}): {len(sens)} families; pair-wide shift explains "
              f"{res[stat]['uniform_share_of_family_variance']:.0%} of family-level change; "
              f"{res[stat]['share_positive']:.0%} of families move in the adaptive direction")
        print("   most sensitive: " + "; ".join(f"{d} {v:+.3f}" for d, v in res[stat]["most_sensitive"][:5]))
        print("   least: " + "; ".join(f"{d} {v:+.3f}" for d, v in res[stat]["least_sensitive"][-5:]))
        print("   features: " + ", ".join(f"{k} {v:+.2f}" for k, v in top_feat[:6]))

    out = Path("results/family_sequence")
    out.mkdir(parents=True, exist_ok=True)
    (out / "metrics.json").write_text(json.dumps(res, indent=2))
    save_law(LAWS_DIR / "family_sequence_v1.json", id="family_sequence_v1",
             scope="Which protein families carry temperature (IVYWREL) and salt (acidic excess) adaptation in bacteria and archaea.",
             model="Per-family change in domain composition across relative -> extremophile pairs, regressed on the environment change.",
             feature_names=[], data={"pairs": len(pairs)}, validation=res, contexts={},
             caveats=["Composition is over Pfam domain regions only.", f"Families need >= {MIN_PAIRS} pairs."])
    print(f"Done -> {out}/ and laws/family_sequence_v1.json")


if __name__ == "__main__":
    main()
