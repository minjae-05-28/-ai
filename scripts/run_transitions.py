"""Do independent origins of a lifestyle transition lose (or gain) the same gene families?

    python scripts/run_transitions.py anaerobic        -> results/transitions/anaerobic/summary.json
    python scripts/run_transitions.py multicellular    -> results/transitions/multicellular/summary.json
    python scripts/run_transitions.py anaerobic --save-law anaerobic_transition_v1

Pairs come from scripts/transition_catalog.py (curated from taxonomy, not from gene content).
Profiles are Pfam presence and gene counts from the collected UniProt proteomes.

Anaerobic (losses). For each origin, the candidates are the families most of its aerobic relatives
carry, and a family counts as lost when most of the anaerobes lack it. Predict the losses of one
held-out origin from:
    law                the share of the OTHER anaerobic origins that lost the family (convergence)
    parasite_baseline  the share of aerobic parasite pairs that lost it (what parasitism alone removes)
    rarity_baseline    1 - the family's prevalence across all collected eukaryotes
The decisive test is law - the better baseline, per origin, with a bootstrap interval over origins.
The two parasitism-matched origins (Microsporidia, Cryptosporidium: both sides are parasites) say
whether oxygen matters beyond parasitism.

Multicellular (gains). Candidates are the families no unicellular relative carries; a family
counts as gained when most multicellular members carry it. Baselines: the gain rate of
unicellular-unicellular pairs (background turnover) and prevalence. Copy-number expansion of
shared families is compared between origins and between control pairs.

Incomplete proteomes read as losses here (no completeness model in a pair comparison), which
inflates anaerobe losses; the parasite pairs share that problem, which is why they are the baseline.
"""

import argparse
import gzip
import json
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import transition_catalog as T  # noqa: E402

from organelle_evo.predict import auroc  # noqa: E402

OUT = Path("results/transitions")


def load_profiles():
    prof = {}
    for f in sorted(Path("data/uniprot/shards").glob("*.json.gz")):
        for p in json.loads(gzip.open(f, "rt").read()).values():
            if p.get("kingdom") in ("eukaryotes", "fungi") and p.get("pfam"):
                old = prof.get(p["organism"])
                if old is None or len(p["pfam"]) > len(old):
                    prof[p["organism"]] = p["pfam"]
    return prof


def majority(prof, names, f):
    return sum(f in prof[n] for n in names) >= len(names) / 2


def losses(prof, derived, relatives):
    """{family: 1 lost / 0 kept} over the families most relatives carry."""
    fams = {f for n in relatives for f in prof[n]}
    return {f: int(not majority(prof, derived, f)) for f in fams if majority(prof, relatives, f)}


def gains(prof, derived, relatives):
    """{family: 1 gained / 0 not} over the families no relative carries."""
    have_rel = {f for n in relatives for f in prof[n]}
    fams = {f for n in derived for f in prof[n]} | {f for p in prof.values() for f in p}
    return {f: int(majority(prof, derived, f)) for f in fams if f not in have_rel}


def signature(tables, f):
    """Share of the given origins that changed f, among those where f was a candidate."""
    vals = [t[f] for t in tables if f in t]
    return float(np.mean(vals)) if vals else np.nan


def score_origins(event, prevalence, baselines, prev_sign):
    """Leave-one-origin-out AUROC of the law (other origins) and each baseline."""
    rows = {}
    names = list(event)
    for o in names:
        tab = event[o]
        fams = sorted(tab)
        y = np.array([tab[f] for f in fams])
        if y.min() == y.max():
            continue
        others = [event[x] for x in names if x != o]
        law = np.array([signature(others, f) for f in fams])
        fill = np.nanmean(law)
        law = np.where(np.isnan(law), fill, law)
        r = {"n_candidates": len(fams), "n_changed": int(y.sum()), "share_changed": round(float(y.mean()), 4),
             "law": round(float(auroc(law, y)), 4)}
        bvec = {}
        for bname, btables in baselines.items():
            b = np.array([signature(btables, f) for f in fams])
            b = np.where(np.isnan(b), np.nanmean(b), b)
            r[bname] = round(float(auroc(b, y)), 4)
            bvec[bname] = b
        pv = np.array([prevalence.get(f, 0.0) for f in fams])
        r["rarity_baseline"] = round(float(auroc(prev_sign * pv, y)), 4)
        # Does the convergent signal carry anything rarity does not? Average of the two ranks.
        both = rank(law) + rank(prev_sign * pv)
        r["law+rarity"] = round(float(auroc(both, y)), 4)
        r["combined_minus_rarity"] = round(r["law+rarity"] - r["rarity_baseline"], 4)
        # The same combination for the control signature: if it adds as much, the signal is generic
        # reduction (or turnover), not specific to this transition.
        for bname, b in bvec.items():
            r[f"{bname}+rarity"] = round(float(auroc(rank(b) + rank(prev_sign * pv), y)), 4)
            r["law_vs_control_combined"] = round(r["law+rarity"] - r[f"{bname}+rarity"], 4)
        rows[o] = r
    return rows


def matched_law_vs_control(event, ctrl_tables, prevalence, prev_sign):
    """law+rarity minus control+rarity with the law built from as many origins as there are control
    tables (every combination, averaged): the law should not win only by averaging more sources."""
    import itertools

    k = len(ctrl_tables)
    out = []
    for o in event:
        fams = sorted(event[o])
        y = np.array([event[o][f] for f in fams])
        if y.min() == y.max():
            continue
        pv = prev_sign * np.array([prevalence.get(f, 0.0) for f in fams])
        b = np.array([signature(ctrl_tables, f) for f in fams])
        b = np.where(np.isnan(b), np.nanmean(b), b)
        cb = auroc(rank(b) + rank(pv), y)
        others = [x for x in event if x != o]
        vals = []
        for combo in itertools.combinations(others, min(k, len(others))):
            law = np.array([signature([event[x] for x in combo], f) for f in fams])
            law = np.where(np.isnan(law), np.nanmean(law), law)
            vals.append(auroc(rank(law) + rank(pv), y))
        out.append(float(np.mean(vals)) - float(cb))
    return out


def boot_ci(diffs, seed=0):
    diffs = np.asarray(diffs)
    rng = np.random.default_rng(seed)
    boot = [rng.choice(diffs, len(diffs), replace=True).mean() for _ in range(5000)]
    return {"mean": round(float(diffs.mean()), 4),
            "ci95": [round(float(np.percentile(boot, 2.5)), 4), round(float(np.percentile(boot, 97.5)), 4)]}


def decisive(rows, base_keys, seed=0):
    diffs = np.array([r["law"] - max(r[k] for k in base_keys) for r in rows.values()])
    rng = np.random.default_rng(seed)
    boot = [rng.choice(diffs, len(diffs), replace=True).mean() for _ in range(5000)]
    return {"mean": round(float(diffs.mean()), 4),
            "ci95": [round(float(np.percentile(boot, 2.5)), 4), round(float(np.percentile(boot, 97.5)), 4)],
            "per_origin": {o: round(float(d), 4) for o, d in zip(rows, diffs)},
            "note": "law minus the better baseline in each held-out origin; bootstrap over origins"}


def rank(x):
    r = np.empty(len(x))
    r[np.argsort(x, kind="stable")] = np.arange(len(x))
    return r


def spearman(a, b):
    if len(a) < 10:
        return np.nan
    return float(np.corrcoef(rank(np.asarray(a)), rank(np.asarray(b)))[0, 1])


def expansion(prof, derived, relatives):
    """log2 mean copy number, derived over relatives, for families every member of both carries."""
    shared = set.intersection(*[set(prof[n]) for n in derived + relatives])
    return {f: float(np.log2(np.mean([prof[n][f] for n in derived]) / np.mean([prof[n][f] for n in relatives])))
            for f in shared}


def panel(prof, groups, pathway, event_tables, control_tables):
    out = {}
    for g, fams in T.PANELS[pathway].items():
        out[g] = {}
        for f in fams:
            out[g][f] = {
                "share_of_derived_with_it": round(float(np.mean([f in prof[n] for o in groups.values()
                                                                for n in o[0]])), 3),
                "share_of_relatives_with_it": round(float(np.mean([f in prof[n] for o in groups.values()
                                                                  for n in o[1]])), 3),
                "changed_in_origins": round(signature(list(event_tables.values()), f), 3)
                if any(f in t for t in event_tables.values()) else None,
                "changed_in_controls": round(signature(list(control_tables.values()), f), 3)
                if any(f in t for t in control_tables.values()) else None}
    return out


def run(pathway):
    prof = load_profiles()
    n_all = len(prof)
    counts = {}
    for p in prof.values():
        for f in p:
            counts[f] = counts.get(f, 0) + 1
    prevalence = {f: c / n_all for f, c in counts.items()}
    res = {"pathway": pathway, "n_reference_proteomes": n_all}
    if pathway == "anaerobic":
        groups = {o: (v["anaerobes"], v["relatives"]) for o, v in T.ANAEROBIC.items()}
        event = {o: losses(prof, d, r) for o, (d, r) in groups.items()}
        ctrl = {o: losses(prof, v["derived"], v["relatives"]) for o, v in T.AEROBIC_PARASITES.items()}
        rows = score_origins(event, prevalence, {"parasite_baseline": list(ctrl.values())}, prev_sign=-1)
        res["leave_one_origin_out"] = {"metric": "auroc", "what": "predict which candidate families the held-out "
                                       "origin lost", "per_origin": rows,
                                       "law": round(float(np.mean([r["law"] for r in rows.values()])), 4),
                                       "parasite_baseline": round(float(np.mean([r["parasite_baseline"] for r in rows.values()])), 4),
                                       "rarity_baseline": round(float(np.mean([r["rarity_baseline"] for r in rows.values()])), 4)}
        res["law_minus_best_baseline"] = decisive(rows, ("parasite_baseline", "rarity_baseline"))
        res["law_vs_control_matched_sources"] = {
            **boot_ci(matched_law_vs_control(event, list(ctrl.values()), prevalence, -1)),
            "what": f"as law_vs_control_signature, with the law built from {len(ctrl)} origins (all combinations) "
                    f"to match the {len(ctrl)} control pairs"}
        res["law_adds_to_rarity"] = {**boot_ci([r["combined_minus_rarity"] for r in rows.values()]),
                                     "what": "AUROC of law+rarity (rank average) minus rarity alone, per origin: "
                                             "does the convergent signal carry information rarity does not"}
        res["law_vs_control_signature"] = {**boot_ci([r["law_vs_control_combined"] for r in rows.values()]),
                                           "what": "law+rarity minus control+rarity, per origin: is the added "
                                                   "information specific to this transition"}
        matched = {o: r for o, r in rows.items() if T.ANAEROBIC[o]["parasitism_matched"]}
        res["parasitism_matched_origins"] = {
            o: {"law": r["law"], "parasite_baseline": r["parasite_baseline"], "rarity_baseline": r["rarity_baseline"],
                "share_lost": r["share_changed"]} for o, r in matched.items()}
        res["share_lost"] = {"anaerobic_origins": {o: r["share_changed"] for o, r in rows.items()},
                             "aerobic_parasite_controls": {o: round(float(np.mean(list(t.values()))), 4)
                                                           for o, t in ctrl.items()}}
        res["panel"] = panel(prof, groups, "anaerobic", event, ctrl)
        # Gains too: the anaerobic toolkit (hydrogenase, PFOR) is thought to be acquired.
        g_ev = {o: gains(prof, d, r) for o, (d, r) in groups.items()}
        res["panel_gains"] = {f: signature(list(g_ev.values()), f)
                              for g, fams in T.PANELS["anaerobic"].items() if "GAINED" in g for f in fams}
    else:
        groups = {o: (v["derived"], v["relatives"]) for o, v in T.MULTICELLULAR.items()}
        event = {o: gains(prof, d, r) for o, (d, r) in groups.items()}
        ctrl = {}
        for o, (a, b) in T.UNICELLULAR_CONTROLS.items():
            ctrl[f"{o} (a over b)"] = gains(prof, a, b)
            ctrl[f"{o} (b over a)"] = gains(prof, b, a)
        rows = score_origins(event, prevalence, {"control_baseline": list(ctrl.values())}, prev_sign=1)
        res["leave_one_origin_out"] = {"metric": "auroc", "what": "predict which candidate families the held-out "
                                       "origin gained", "per_origin": rows,
                                       "law": round(float(np.mean([r["law"] for r in rows.values()])), 4),
                                       "control_baseline": round(float(np.mean([r["control_baseline"] for r in rows.values()])), 4),
                                       "rarity_baseline": round(float(np.mean([r["rarity_baseline"] for r in rows.values()])), 4)}
        res["law_minus_best_baseline"] = decisive(rows, ("control_baseline", "rarity_baseline"))
        res["law_adds_to_rarity"] = {**boot_ci([r["combined_minus_rarity"] for r in rows.values()]),
                                     "what": "AUROC of law+rarity (rank average) minus rarity alone, per origin: "
                                             "does the convergent signal carry information rarity does not"}
        res["law_vs_control_signature"] = {**boot_ci([r["law_vs_control_combined"] for r in rows.values()]),
                                           "what": "law+rarity minus control+rarity, per origin: is the added "
                                                   "information specific to this transition"}
        res["share_gained"] = {"multicellular_origins": {o: r["share_changed"] for o, r in rows.items()},
                               "unicellular_controls": {o: round(float(np.mean(list(t.values()))), 4)
                                                        for o, t in ctrl.items()}}
        # Copy-number expansion: do independent origins expand the same shared families?
        ex = {o: expansion(prof, d, r) for o, (d, r) in groups.items()}
        cx = {o: expansion(prof, a, b) for o, (a, b) in T.UNICELLULAR_CONTROLS.items()}

        def pairwise(tabs):
            vals = []
            keys = list(tabs)
            for i in range(len(keys)):
                for j in range(i + 1, len(keys)):
                    sh = sorted(set(tabs[keys[i]]) & set(tabs[keys[j]]))
                    vals.append(spearman([tabs[keys[i]][f] for f in sh], [tabs[keys[j]][f] for f in sh]))
            vals = [v for v in vals if not np.isnan(v)]
            return round(float(np.mean(vals)), 4) if vals else None, len(vals)
        m, nm = pairwise(ex)
        c, nc = pairwise(cx)
        res["expansion_concordance"] = {
            "metric": "spearman", "what": "mean pairwise rank correlation of log2 copy-number change over shared "
            "families", "multicellular_origins": m, "n_origin_pairs": nm, "control_baseline": c, "n_control_pairs": nc}
        res["panel"] = panel(prof, groups, "multicellular", event, ctrl)
    out = OUT / pathway
    out.mkdir(parents=True, exist_ok=True)
    (out / "summary.json").write_text(json.dumps(res, ensure_ascii=False, indent=1))
    lo = res["leave_one_origin_out"]
    print(json.dumps({k: v for k, v in lo.items() if k != "per_origin"}, ensure_ascii=False))
    for o, r in lo["per_origin"].items():
        print(f"  {o:45s} {r}")
    print("decisive:", res["law_minus_best_baseline"])
    print("law adds to rarity:", res["law_adds_to_rarity"])
    print("law vs control signature (both + rarity):", res["law_vs_control_signature"])
    if "law_vs_control_matched_sources" in res:
        print("  with matched number of sources:", res["law_vs_control_matched_sources"])
    for k in ("parasitism_matched_origins", "share_lost", "share_gained", "expansion_concordance", "panel_gains"):
        if k in res:
            print(k, json.dumps(res[k], ensure_ascii=False))
    print(f"-> {out}/summary.json")
    return res


def save(pathway, law_id):
    from organelle_evo.laws import LAWS_DIR, save_law

    dest = LAWS_DIR / f"{law_id}.json"
    if dest.exists():
        raise SystemExit(f"{dest} exists; laws are never overwritten — use a new id")
    s = json.loads((OUT / pathway / "summary.json").read_text())
    d = s["law_minus_best_baseline"]
    lo = s["leave_one_origin_out"]
    base = [k for k in lo if k.endswith("_baseline")]
    verdict = ("the law beats the better baseline" if d["ci95"][0] > 0 else
               "the law loses to the better baseline" if d["ci95"][1] < 0 else
               "the law is not separated from the better baseline (interval holds zero)")
    cav = [
        f"Leave-one-origin-out AUROC: law {lo['law']} against " + ", ".join(f"{b} {lo[b]}" for b in base)
        + f". Law minus the better baseline per origin: {d['mean']} [{d['ci95'][0]}, {d['ci95'][1]}] — {verdict}.",
        f"{len(lo['per_origin'])} independent origins; the interval is a bootstrap over origins, so it is wide and "
        "would narrow only with more origins, not more species per origin.",
        "Pairs are curated from taxonomy (scripts/transition_catalog.py); the relative stands in for the ancestor, "
        "so changes on the relative's own branch are counted as the transition's.",
        "Presence comes from UniProt Pfam cross-references with no completeness model: an incomplete proteome "
        "reads as losses. Reduced genomes (Microsporidia, Giardia, Cryptosporidium) are both incomplete-looking "
        "and genuinely reduced, which this design cannot separate.",
    ]
    a, c = s["law_adds_to_rarity"], s["law_vs_control_signature"]
    cav.insert(1, f"Added to rarity, the law gains {a['mean']} [{a['ci95'][0]}, {a['ci95'][1]}] AUROC; against the "
                  f"control signature added to rarity the same way: {c['mean']} [{c['ci95'][0]}, {c['ci95'][1]}]"
               + (f"; with the law built from as many origins as there are control pairs: "
                  f"{s['law_vs_control_matched_sources']['mean']} {s['law_vs_control_matched_sources']['ci95']}"
                  if "law_vs_control_matched_sources" in s else "") + ".")
    if pathway == "anaerobic":
        cav.append("Panel limits: ATP-synt_C and Fe_hyd_lg_C are Pfam families shared with the vacuolar ATPase and "
                   "with the cytosolic Fe-S assembly protein NAR1, so aerobes carry them too; they are not markers of "
                   "mitochondrial ATP synthase or of hydrogenase. The respiratory chain (COX15, COX17, Cytochrom_C1, "
                   "Rieske, UCR_14kD) is lost in every anaerobic origin where it was a candidate and in no aerobic "
                   "parasite pair.")
        m = s["parasitism_matched_origins"]
        cav.append("Parasitism-matched origins (both sides parasites): " + "; ".join(
            f"{o}: law {v['law']} vs parasite {v['parasite_baseline']} vs rarity {v['rarity_baseline']}"
            for o, v in m.items()) + ". These are the only comparisons where oxygen is not confounded with parasitism.")
        cav.append("Metamonada's aerobic relatives are in another supergroup (Discoba), so its losses mix the "
                   "anaerobic transition with a deep split.")
    else:
        e = s["expansion_concordance"]
        cav.append(f"Copy-number expansion concordance (Spearman between origins): {e['multicellular_origins']} "
                   f"against {e['control_baseline']} between unicellular control pairs.")
        cav.append("Dictyostelia are aggregative (cells gather), the others clonal (cells stay together after "
                   "division): different routes to multicellularity are pooled.")
    save_law(dest, id=law_id,
             scope=f"Whether independent origins of the {pathway} transition change the same gene families "
                   "(Pfam presence) — eukaryotes, UniProt reference and collected proteomes.",
             model="Leave-one-origin-out: the share of the other origins that changed each family, scored as a "
                   "predictor of the held-out origin's changes (AUROC), against baselines.",
             feature_names=[], data={"origins": list(lo["per_origin"]), "catalogue": "scripts/transition_catalog.py",
                                    "n_reference_proteomes": s["n_reference_proteomes"]},
             # The first "_minus_" entry is the law's own claim (the vault judges on it): specific to this
             # transition beyond the control signature and rarity, with matched numbers of sources.
             validation={**({"law_plus_rarity_minus_control_plus_rarity": s["law_vs_control_matched_sources"]}
                             if "law_vs_control_matched_sources" in s else
                             {"law_plus_rarity_minus_control_plus_rarity": s["law_vs_control_signature"]}),
                         "leave_one_origin_out": {k: v for k, v in lo.items() if k != "per_origin"},
                         "per_origin": lo["per_origin"], "law_alone_minus_best_baseline": d,
                         "law_plus_rarity_minus_rarity": s["law_adds_to_rarity"],
                         **({"parasitism_matched_origins": s["parasitism_matched_origins"]} if pathway == "anaerobic"
                            else {"expansion_concordance": s["expansion_concordance"]}),
                         "marker_panel": s["panel"]},
             caveats=cav, contexts={})
    print(f"law -> {dest}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("pathway", choices=("anaerobic", "multicellular"))
    ap.add_argument("--save-law", default="")
    args = ap.parse_args()
    if args.save_law:
        save(args.pathway, args.save_law)
    else:
        run(args.pathway)


if __name__ == "__main__":
    main()
