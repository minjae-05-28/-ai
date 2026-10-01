"""Do context features (expression, domain partners, operons, exons) improve the gene-loss law?

    python scripts/run_context_features.py [--epochs 300] [--threads 4]

Context features come from data/family_context (scripts/family_context.py), averaged per
family over the species that still carry it, then standardised:
    expression        mean codon-adaptation z (high = highly expressed)
    multi_domain      share of members with more than one Pfam family
    partners          log(1 + distinct partner families in the same proteins)
    operon            (prokaryotes) share of members with a close same-strand neighbour
    neighbourhood     (prokaryotes) log(1 + distinct families nearby)
    exons             (eukaryotes) log mean CDS segments per gene
    has_context       1 if the family was measured at all

Scores are kept separate (the law never sees other species' losses of the same family):
    law_base       enriched features (56)
    law_context    enriched + context features
    memorisation   each family's loss rate in the training pairs
    combined       memorisation shrunk toward law_context (pseudo-count S): used only when
                   asked for, reported side by side

Parasites: leave-one-clade-out (as run_transfer). Extremophiles: leave-one-pair-out with the
base law (environment axes did not help, environment_v2).
"""

import argparse
import json
from pathlib import Path

import numpy as np
import torch

from organelle_evo.eukaryotes import catalog as euk
from organelle_evo.eukaryotes.features import enriched_features
from organelle_evo.eukaryotes.model import counts, family_features, fit_bd, loss_probability, offset_for_losses
from organelle_evo.laws import LAWS_DIR, save_law
from organelle_evo.predict import auroc
from organelle_evo.prokaryotes import catalog as pro

CTX = Path("data/family_context")
SHRINK = (1.0, 3.0, 10.0)
CTX_NAMES = {"eukaryotes": ["ctx:expression", "ctx:multi_domain", "ctx:partners", "ctx:exons", "ctx:has_context"],
             "prokaryotes": ["ctx:expression", "ctx:multi_domain", "ctx:partners", "ctx:operon", "ctx:neighbourhood",
                             "ctx:has_context"]}


def load_context(cat):
    return {json.loads(f.read_text())["species"]: json.loads(f.read_text())["families"] for f in (CTX / cat).glob("*.json")}


def context_matrix(fams, ctx, cat, exclude=()):
    """(F, k) standardised context features; families never measured get 0 and has_context 0."""
    k = len(CTX_NAMES[cat]) - 1
    tot, cnt = np.zeros((len(fams), k)), np.zeros((len(fams), k))
    idx = {f: i for i, f in enumerate(fams)}
    for sp, fam in ctx.items():
        if sp in exclude:
            continue
        for f, v in fam.items():
            i = idx.get(f)
            if i is None:
                continue
            n, cz, nc, multi, partners, op, nb, exons = v
            vals = [cz / nc if nc else None, multi / n, np.log1p(partners)]
            vals += [op / n, np.log1p(nb)] if cat == "prokaryotes" else [np.log(exons / n)]
            for j, val in enumerate(vals):
                if val is not None:
                    tot[i, j] += val
                    cnt[i, j] += 1
    m = np.where(cnt > 0, tot / np.maximum(cnt, 1), np.nan)
    for j in range(k):
        col = m[:, j]
        ok = ~np.isnan(col)
        if ok.sum() > 1:
            col[ok] = (col[ok] - col[ok].mean()) / (col[ok].std() or 1)
        col[~ok] = 0.0
    return np.c_[m, (cnt.sum(1) > 0).astype(float)]


def predict(law, z, n, x, n_lost):
    wl, wm, _ = law.weights(z)
    a_lam = float(np.mean(law.a_lam))
    return loss_probability(n, x, wl, wm, a_lam, offset_for_losses(n, x, wl, wm, a_lam, n_lost))


def score(n, m, z, train, laws, xs, labels):
    """AUROCs of every score for one held-out pair."""
    had = n > 0
    lost = (m == 0)[had]
    idx = np.flatnonzero(had)
    k_lost = np.array([sum(tm[j] == 0 for tn, tm, _ in train if tn[j] > 0) for j in idx], dtype=float)
    k_seen = np.array([sum(tn[j] > 0 for tn, _, _ in train) for j in idx], dtype=float)
    memo = np.where(k_seen > 0, k_lost / np.maximum(k_seen, 1), 0.5)
    p = {name: predict(law, z, n[had], xs[name][had], lost.sum()) for name, law in laws.items()}
    row = {"copies_only": auroc(-n[had].astype(float), lost), "memorisation": auroc(memo, lost),
           **{name: auroc(v, lost) for name, v in p.items()}}
    for s in SHRINK:
        row[f"combined_s{s:g}"] = auroc((k_lost + s * p["law_context"]) / (k_seen + s), lost)
    return row


def summarise(rows, title):
    keys = [k for k in rows[0] if k not in ("pair", "clade")]
    mean = {k: float(np.mean([r[k] for r in rows])) for k in keys}
    gain = np.array([r["law_context"] - r["law_base"] for r in rows])
    print(f"\n{title}: " + ", ".join(f"{k} {v:.3f}" for k, v in mean.items()))
    print(f"   context vs base: mean {gain.mean():+.4f}, better in {(gain > 0).sum()}/{len(gain)}")
    return {"mean_auroc": mean, "context_gain": {"mean": float(gain.mean()), "n_better": int((gain > 0).sum()), "n": len(gain)},
            "heldout": rows}


def importance(law, names, ctx_names):
    wl, _, _ = law.weights((1.0,) + (0.0,) * (len(law.lifestyles) - 1))
    return {n: round(float(wl[names.index(n)]), 4) for n in ctx_names}


def parasites(epochs):
    D = Path("data/eukaryotes")
    meta = json.loads((D / "pfam_meta.json").read_text())
    ann = json.loads((D / "family_annotations.json").read_text())
    profiles = {}
    for f in D.glob("*.json"):
        if f.name not in ("pfam_meta.json", "family_annotations.json", "pfam_subset.txt"):
            d = json.loads(f.read_text())
            profiles[d["species"]] = d
    fams, _ = family_features(list(profiles.values()), meta)
    c = {s: counts(p, fams) for s, p in profiles.items()}
    fams, names, x = enriched_features(profiles, meta, ann, c)
    xc = np.c_[x, context_matrix(fams, load_context("eukaryotes"), "eukaryotes")]
    cnames = names + CTX_NAMES["eukaryotes"]
    pairs = euk.resolve_pairs(profiles)
    data = [(c[a], c[d], euk.design(d)) for a, d in pairs]
    labels = ("base", *euk.AXES)
    clade = lambda s: euk.SPECIES[s].group.split("_")[0]  # noqa: E731
    rows = []
    for cl in sorted({clade(d) for (a, d), (_, _, z) in zip(pairs, data) if z[1]}):
        drop = {i for i, (a, d) in enumerate(pairs) if clade(d) == cl}
        train = [p for j, p in enumerate(data) if j not in drop]
        laws = {"law_base": fit_bd(x, train, labels, epochs=epochs), "law_context": fit_bd(xc, train, labels, epochs=epochs)}
        for i in sorted(drop):
            (a, d), (n, m, z) = pairs[i], data[i]
            if not z[1]:
                continue
            r = {"pair": f"{a} -> {d}", "clade": cl, **score(n, m, z, train, laws, {"law_base": x, "law_context": xc}, labels)}
            rows.append(r)
            print(f"  {cl:14s} {d:32s} base {r['law_base']:.3f}  context {r['law_context']:.3f}  "
                  f"memo {r['memorisation']:.3f}  combined {r['combined_s3']:.3f}", flush=True)
    res = summarise(rows, "parasites, leave-one-clade-out")
    res["context_weights"] = importance(fit_bd(xc, data, labels, epochs=epochs), cnames, CTX_NAMES["eukaryotes"])
    print("   context loss weights (base law; negative = retained): " + ", ".join(f"{k} {v:+.2f}" for k, v in res["context_weights"].items()))
    return res, cnames


def extremophiles(epochs):
    D = Path("data/prokaryotes")
    meta = json.loads(Path("data/eukaryotes/pfam_meta.json").read_text())
    ann = json.loads(Path("data/eukaryotes/family_annotations.json").read_text())
    profiles = {json.loads(f.read_text())["species"]: json.loads(f.read_text()) for f in D.glob("*.json")}
    fams, _ = family_features(list(profiles.values()), meta)
    c = {s: counts(p, fams) for s, p in profiles.items()}
    fams, names, x = enriched_features(profiles, meta, ann, c, free=list(profiles))
    ctx = load_context("prokaryotes")
    pairs = pro.resolve_pairs(profiles)
    data = [(c[a], c[d], (1.0,)) for a, d in pairs]
    rows = []
    for i, (a, d) in enumerate(pairs):
        z = pro.design(a, d)
        if not any(z[1:]) or max(abs(v) for v in z[1:]) < 0.25:
            continue
        train = [p for j, p in enumerate(data) if j != i]
        xc = np.c_[x, context_matrix(fams, ctx, "prokaryotes", exclude={d})]
        laws = {"law_base": fit_bd(x, train, ("base",), epochs=epochs), "law_context": fit_bd(xc, train, ("base",), epochs=epochs)}
        n, m, _ = data[i]
        r = {"pair": f"{a} -> {d}", **score(n, m, (1.0,), train, laws, {"law_base": x, "law_context": xc}, ("base",))}
        rows.append(r)
        print(f"  {d:32s} base {r['law_base']:.3f}  context {r['law_context']:.3f}  "
              f"memo {r['memorisation']:.3f}  combined {r['combined_s3']:.3f}", flush=True)
    res = summarise(rows, "extremophiles, leave-one-pair-out")
    xc = np.c_[x, context_matrix(fams, ctx, "prokaryotes")]
    cnames = names + CTX_NAMES["prokaryotes"]
    res["context_weights"] = importance(fit_bd(xc, data, ("base",), epochs=epochs), cnames, CTX_NAMES["prokaryotes"])
    print("   context loss weights (negative = retained): " + ", ".join(f"{k} {v:+.2f}" for k, v in res["context_weights"].items()))
    return res, cnames


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--epochs", type=int, default=300)
    ap.add_argument("--threads", type=int, default=4)
    ap.add_argument("--out", default="results/context_features")
    args = ap.parse_args()
    torch.set_num_threads(args.threads)
    res = {}
    res["extremophiles"], pnames = extremophiles(args.epochs)
    res["parasites"], enames = parasites(args.epochs)
    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    (out / "metrics.json").write_text(json.dumps(res, indent=2))
    save_law(LAWS_DIR / "context_features_v1.json", id="context_features_v1",
             scope="Gene-family loss law with context features (codon-usage expression, domain partners, operons, exons) "
                   "for parasitic eukaryotes and extremophile bacteria/archaea; memorisation kept as a separate score.",
             model="Linear birth-death law on enriched + context family features; memorisation and a shrunk combination "
                   "reported side by side, never mixed into the law.",
             feature_names=[], data={"parasite_pairs": len(res["parasites"]["heldout"]),
                                     "extremophile_pairs": len(res["extremophiles"]["heldout"])},
             validation={k: {kk: v[kk] for kk in ("mean_auroc", "context_gain", "context_weights")} for k, v in res.items()},
             contexts={},
             caveats=["Context features are family averages over the species that carry the family.",
                      "Codon adaptation is a proxy for expression, weaker in eukaryotes.",
                      "combined_sN uses memorisation; it is a forecasting tool, not a law."])
    print(f"Done -> {out}/ and laws/context_features_v1.json")


if __name__ == "__main__":
    main()
