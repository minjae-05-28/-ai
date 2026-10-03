"""Gene-content (Pfam) laws for animal cells, on designed within-clade pairs.

    python scripts/run_animal_content.py [--epochs 300] [--n-boot 20]

Animals have no ancestor -> descendant pairs of their own; organelle_evo.animals.catalog
PAIR_SPECS designs them (a relative that kept the ancestral condition -> a lineage that
changed one axis). The model is the same linear birth-death law as the microbial and
eukaryote laws, with design (base, colder, freshwater, hypoxia, endothermy, parasite).

Validation, leave-one-origin-out: every pair from one evolutionary event (e.g. all four
birds) is held out together, the law is refitted on the rest, and the held-out descendants'
lost families are ranked. Reported side by side:
    copies_only     fewer ancestral copies -> lost first
    rarity          families carried by fewer of the training species -> lost first
    memorisation    each family's loss frequency in the training pairs
    no_axes         the same law with the base row only
    axis_law        the law with the animal axes
Pairs with a distant proxy (flatworm parasites, mammals) are reported with and without.
Intervals: bootstrap over origins.

Writes laws/animals/animal_content_v1.json (animal registry, never laws/).
"""

import argparse
import json
from pathlib import Path

import numpy as np
import torch

from organelle_evo.animals.catalog import PAIR_AXES, SPECIES, design, resolve_pairs
from organelle_evo.eukaryotes.features import enriched_features
from organelle_evo.eukaryotes.model import counts, family_features, fit_bd, loss_probability, offset_for_losses
from organelle_evo.laws import registry_for, save_law
from organelle_evo.predict import auroc

DATA = Path("data/animals")
ANN = Path("data/eukaryotes")
LABELS = ("base", *PAIR_AXES)
KEYS = ("copies_only", "rarity", "memorisation", "no_axes", "axis_law")


def load(data=DATA):
    meta = json.loads((ANN / "pfam_meta.json").read_text())
    ann = json.loads((ANN / "family_annotations.json").read_text())
    profiles = {}
    for f in Path(data).glob("*.json"):
        d = json.loads(f.read_text())
        if "families" in d and d.get("species") in SPECIES:
            profiles[d["species"]] = d
    return profiles, meta, ann


def features(profiles, meta, ann, ubiquity_species):
    fams, _ = family_features(list(profiles.values()), meta)
    c = {s: counts(p, fams) for s, p in profiles.items()}
    fams, names, x = enriched_features(profiles, meta, ann, c, free=ubiquity_species)
    return fams, names, x, c


def predicted_loss(law, z, n, x, n_lost):
    wl, wm, _ = law.weights(z)
    a_lam = float(np.mean(law.a_lam))
    return loss_probability(n, x, wl, wm, a_lam, offset_for_losses(n, x, wl, wm, a_lam, n_lost))


def boot_ci(rows, key, n=2000, seed=0):
    """Mean over pairs and a 95% interval from resampling origins."""
    rng = np.random.default_rng(seed)
    by = {}
    for r in rows:
        by.setdefault(r["origin"], []).append(r[key] if not callable(key) else key(r))
    units = list(by)
    stats = []
    for _ in range(n):
        pick = rng.choice(len(units), len(units))
        stats.append(np.mean([v for i in pick for v in by[units[i]]]))
    vals = [v for vs in by.values() for v in vs]
    return {"mean": round(float(np.mean(vals)), 4),
            "ci95": [round(float(np.percentile(stats, 2.5)), 4), round(float(np.percentile(stats, 97.5)), 4)],
            "n_pairs": len(vals), "n_origins": len(units)}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--epochs", type=int, default=300)
    ap.add_argument("--n-boot", type=int, default=20)
    ap.add_argument("--threads", type=int, default=4)
    ap.add_argument("--out", default="results/animal_content")
    ap.add_argument("--law-id", default="animal_content_v1")
    ap.add_argument("--data", default=str(DATA))
    args = ap.parse_args()
    torch.set_num_threads(args.threads)
    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)

    profiles, meta, ann = load(args.data)
    pairs = resolve_pairs(profiles)
    if not pairs:
        raise SystemExit(f"no animal pairs with profiles in {DATA}/ (run animal-pfam.yml first)")
    proxies = sorted({a for _, a, _, _ in pairs})
    print(f"{len(profiles)} animal profiles, {len(pairs)} pairs "
          f"({sum(o.startswith('control') for o, *_ in pairs)} controls)")

    # Share of ancestral families lost, per pair (descriptive, like severity_v1)
    fams_all, names, x_all, c_all = features(profiles, meta, ann, proxies)
    share = {}
    for o, a, d, dist in pairs:
        had = c_all[a] > 0
        share[f"{a} -> {d}"] = round(float((c_all[d][had] == 0).mean()), 4)
        print(f"  {o:34s} {a:26s} -> {d:30s} lost {share[f'{a} -> {d}']:.3f}")

    # Leave one origin out
    origins = [o for o in dict.fromkeys(o for o, *_ in pairs) if not o.startswith("control")]
    rows = []
    for origin in origins:
        held = [p for p in pairs if p[0] == origin]
        held_desc = {d for _, _, d, _ in held}
        train = [p for p in pairs if p[0] != origin]
        ubiq = [s for s in proxies if s not in held_desc]
        fams, names, x, c = features(profiles, meta, ann, ubiq)
        train_data = [(c[a], c[d], design(a, d)) for _, a, d, _ in train]
        law = fit_bd(x, train_data, LABELS, epochs=args.epochs)
        base = fit_bd(x, [(n, m, (1.0,)) for n, m, _ in train_data], ("base",), epochs=args.epochs)
        train_species = {s for _, a, d, _ in train for s in (a, d)} - held_desc
        carried = np.array([sum(c[s][j] > 0 for s in train_species) for j in range(len(fams))], dtype=float)
        for _, a, d, dist in held:
            n, m, z = c[a], c[d], design(a, d)
            had = n > 0
            lost = (m == 0)[had]
            idx = np.flatnonzero(had)
            freq = np.array([np.mean([tm[j] == 0 for tn, tm, _ in train_data if tn[j] > 0])
                             if any(tn[j] > 0 for tn, _, _ in train_data) else 0.5 for j in idx])
            row = {"origin": origin, "pair": f"{a} -> {d}", "distant": dist, "design": [round(v, 3) for v in z],
                   "n_ancestral": int(had.sum()), "n_lost": int(lost.sum()),
                   "copies_only": auroc(-n[had].astype(float), lost),
                   "rarity": auroc(-carried[had], lost),
                   "memorisation": auroc(freq, lost),
                   "no_axes": auroc(predicted_loss(base, (1.0,), n[had], x[had], lost.sum()), lost),
                   "axis_law": auroc(predicted_loss(law, z, n[had], x[had], lost.sum()), lost)}
            rows.append(row)
            print(f"  [{origin}] {d:30s} copies {row['copies_only']:.3f} rarity {row['rarity']:.3f} "
                  f"memo {row['memorisation']:.3f} no-axes {row['no_axes']:.3f} axes {row['axis_law']:.3f}",
                  flush=True)

    summary = {}
    for label, sel in (("all", rows), ("close_proxies_only", [r for r in rows if not r["distant"]])):
        if not sel:
            continue
        s = {k: boot_ci(sel, k) for k in KEYS}
        s["axis_law - no_axes"] = boot_ci(sel, lambda r: r["axis_law"] - r["no_axes"])
        s["axis_law - memorisation"] = boot_ci(sel, lambda r: r["axis_law"] - r["memorisation"])
        s["axis_law - rarity"] = boot_ci(sel, lambda r: r["axis_law"] - r["rarity"])
        s["axes_better_in"] = int(sum(r["axis_law"] > r["no_axes"] for r in sel))
        summary[label] = s
        print(f"\n{label}: " + ", ".join(f"{k}={s[k]['mean']:.3f}" for k in KEYS))
        for k in ("axis_law - no_axes", "axis_law - memorisation", "axis_law - rarity"):
            print(f"  {k}: {s[k]['mean']:+.4f} {s[k]['ci95']}")

    # Full law; intervals from resampling origins
    data = [(c_all[a], c_all[d], design(a, d)) for _, a, d, _ in pairs]
    law = fit_bd(x_all, data, LABELS, epochs=args.epochs)
    all_origins = list(dict.fromkeys(o for o, *_ in pairs))
    rng = np.random.default_rng(0)
    boots = {"lam": [], "mu": [], "nu": []}
    for b in range(args.n_boot):
        pick = rng.choice(len(all_origins), len(all_origins))
        sample = [data[i] for k in pick for i, p in enumerate(pairs) if p[0] == all_origins[k]]
        f = fit_bd(x_all, sample, LABELS, epochs=args.epochs, seed=b + 1)
        boots["lam"].append(f.w_lam)
        boots["mu"].append(f.w_mu)
        boots["nu"].append(f.w_nu)
    se = {k: np.std(v, axis=0) for k, v in boots.items()}
    effects = {}
    for kind, W, SE in (("loss", law.w_mu, se["mu"]), ("duplication", law.w_lam, se["lam"]),
                        ("gain", law.w_nu, se["nu"])):
        for r, lab in enumerate(LABELS[1:], start=1):
            sig = [(names[j], round(float(W[r, j]), 3), round(float(SE[r, j]), 3)) for j in range(len(names))
                   if SE[r, j] > 0 and abs(W[r, j]) > 1.96 * SE[r, j]]
            effects[f"{kind}_{lab}"] = sorted(sig, key=lambda t: -abs(t[1]))[:10]
    for lab in PAIR_AXES:
        print(f"  loss {lab}: " + ", ".join(f"{n_}={w:+.2f}" for n_, w, _ in effects[f'loss_{lab}'][:5]))

    pairs_out = [{"origin": o, "proxy": a, "descendant": d, "distant": dist, "design": list(design(a, d)),
                  "share_lost": share[f"{a} -> {d}"]} for o, a, d, dist in pairs]
    (out / "metrics.json").write_text(json.dumps(
        {"pairs": pairs_out, "heldout": rows, "summary": summary, "significant_effects": effects}, indent=2))

    n_axis = {lab: sum(1 for p in pairs_out if abs(p["design"][i + 1]) >= 0.25 and not p["origin"].startswith("control"))
              for i, lab in enumerate(PAIR_AXES)}
    save_law(
        registry_for("animals") / f"{args.law_id}.json",
        id=args.law_id,
        scope=("Gene-family (Pfam) loss, duplication and gain in animals when a lineage changes cell "
               "temperature, moves from sea to fresh water, into hypoxia, becomes endothermic or parasitic. "
               "Learned from designed within-clade pairs; animal registry only."),
        model="Linear birth-death per family; log rate = a_pair + x @ (axis change @ W), "
              "design = (base, colder, freshwater, hypoxia, endothermy, parasite).",
        feature_names=names,
        data={"pairs": pairs_out, "n_families": len(fams_all), "pairs_per_axis": n_axis},
        validation={"leave_one_origin_out_auroc": summary},
        caveats=[
            "Ancestors are extant relatives that kept the ancestral condition; they have evolved too.",
            "Few pairs per axis and several pairs share one origin; intervals resample origins.",
            "Flatworm parasites use an annelid proxy and mammals a lizard proxy (hundreds of Myr): "
            "results are reported with and without these distant pairs.",
            "Animal genome annotation quality varies; a family missing from an assembly reads as lost.",
            "Axis values are literature approximations (see organelle_evo.animals.catalog).",
            "The urea axis of animal_axes_v1 has no pair and is not in this law.",
            "Noise floor: on random profiles (smoke test, no signal) the pipeline gave axis_law - rarity "
            "+0.005 [0.001, 0.010]; differences below about 0.01 should not be read as effects.",
        ],
        contexts={
            f"{kind}_{lab}": {f: {"weight": round(float(W[r, j]), 4),
                                  "ci95": [round(float(W[r, j] - 1.96 * SE[r, j]), 4),
                                           round(float(W[r, j] + 1.96 * SE[r, j]), 4)]}
                              for j, f in enumerate(names)}
            for kind, W, SE in (("loss", law.w_mu, se["mu"]), ("duplication", law.w_lam, se["lam"]),
                                ("gain", law.w_nu, se["nu"]))
            for r, lab in enumerate(LABELS)
        },
    )
    print(f"Done -> {out}/ and laws/animals/{args.law_id}.json")


if __name__ == "__main__":
    main()
