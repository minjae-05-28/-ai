"""A completeness score for every collected proteome, computed from the data itself.

    PYTHONPATH=src python scripts/genome_quality.py

Why not just use BUSCO: UniProt reports it for bacteria, archaea and fungi, but not for viruses
(0% of 15,891) and it is missing for part of the eukaryotes. An incomplete proteome reads as gene
loss, so the reconstruction needs a completeness number for EVERY tip, not for most of them.

The score: within a kingdom, take the Pfam families carried by almost every high-quality proteome
(BUSCO C >= 97%) — these are the families a complete proteome of that kingdom should have — and
score each proteome by the share of them it carries. This is the same idea as BUSCO's single-copy
orthologues, built from families we already count, so it needs no sequences and no external tool.

Validation: against BUSCO where BUSCO exists. The score is only worth using if it agrees.

Writes data/quality/completeness.json  {upid: {organism, kingdom, busco, markers, completeness}}
      results/quality/summary.json     marker sets, agreement with BUSCO, what each kingdom looks like
"""

import gzip
import json
import re
from collections import defaultdict
from pathlib import Path

import numpy as np

OUT = Path("data/quality")
RES = Path("results/quality")
HIGH = 97.0      # BUSCO completeness that defines a reference-quality proteome
UNIVERSAL = 0.95  # a marker family must be in this share of those
MAX_MARKERS = 150


def load():
    rows = {}
    for f in sorted(Path("data/uniprot/shards").glob("*.json.gz")):
        for upid, p in json.loads(gzip.open(f, "rt").read()).items():
            m = re.search(r"C:([\d.]+)%", p.get("busco") or "")
            rows[upid] = {"organism": p["organism"], "kingdom": p.get("kingdom", "?"),
                          "busco": float(m.group(1)) if m else None,
                          "pfam": set(p.get("pfam") or ())}
    return rows


def markers_for(profiles, share=0.95, max_markers=MAX_MARKERS, top_quartile=True):
    """Marker families for one ANALYSIS SET, not a whole kingdom.

    profiles: {name: set of families}. The reference group is the top quartile by family count,
    and the markers are the families almost all of them carry. Kingdom-wide sets fail where the
    kingdom is diverse (the 60 eukaryote proteomes span Amoebozoa and Discoba: Spearman 0.07
    against BUSCO), so every reconstruction builds its own set from its own tips.
    """
    pool = [f for f in profiles.values() if f]
    if len(pool) < 8:
        return []
    if top_quartile:
        cut = np.percentile([len(f) for f in pool], 75)
        pool = [f for f in pool if len(f) >= cut]
    counts = defaultdict(int)
    for f in pool:
        for fam in f:
            counts[fam] += 1
    return sorted((f for f, c in counts.items() if c >= share * len(pool)), key=lambda f: -counts[f])[:max_markers]


def completeness_for(profiles, markers=None):
    """name -> share of the set's marker families it carries (1.0 = as complete as the best here)."""
    markers = markers if markers is not None else markers_for(profiles)
    if not markers:
        return {k: 1.0 for k in profiles}, []
    ms = set(markers)
    return {k: len(ms & f) / len(markers) for k, f in profiles.items()}, markers


def marker_set(rows, kingdom):
    """Families carried by almost every reference-quality proteome of this kingdom."""
    ref = [r for r in rows.values() if r["kingdom"] == kingdom and r["busco"] is not None
           and r["busco"] >= HIGH and r["pfam"]]
    if len(ref) < 20:
        # No BUSCO to lean on (viruses): fall back to the proteomes in the top quartile by family
        # count, which is a weaker but still data-driven notion of "a complete one of these".
        pool = [r for r in rows.values() if r["kingdom"] == kingdom and r["pfam"]]
        if len(pool) < 20:
            return [], 0, "too few proteomes"
        cut = np.percentile([len(r["pfam"]) for r in pool], 75)
        ref = [r for r in pool if len(r["pfam"]) >= cut]
        basis = f"상위 4분위 (유전자군 {int(cut)}개 이상), BUSCO 없음"
    else:
        basis = f"BUSCO C>={HIGH:.0f}%"
    counts = defaultdict(int)
    for r in ref:
        for f in r["pfam"]:
            counts[f] += 1
    fams = sorted((f for f, c in counts.items() if c >= UNIVERSAL * len(ref)),
                  key=lambda f: -counts[f])[:MAX_MARKERS]
    return fams, len(ref), basis


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    RES.mkdir(parents=True, exist_ok=True)
    rows = load()
    kingdoms = sorted({r["kingdom"] for r in rows.values()})
    summary = {"high_busco": HIGH, "universal_share": UNIVERSAL, "kingdoms": {}}
    out = {}
    for k in kingdoms:
        fams, n_ref, basis = marker_set(rows, k)
        mine = [(u, r) for u, r in rows.items() if r["kingdom"] == k]
        if not fams:
            for u, r in mine:
                out[u] = {"organism": r["organism"], "kingdom": k, "busco": r["busco"],
                          "markers": None, "completeness": None}
            summary["kingdoms"][k] = {"proteomes": len(mine), "markers": 0, "note": basis}
            continue
        fs = set(fams)
        comp, busco = [], []
        for u, r in mine:
            c = len(fs & r["pfam"]) / len(fams)
            out[u] = {"organism": r["organism"], "kingdom": k, "busco": r["busco"],
                      "markers": len(fs & r["pfam"]), "completeness": round(c, 4)}
            if r["busco"] is not None:
                comp.append(c)
                busco.append(r["busco"] / 100)
        agree = {}
        if len(comp) > 30:
            c, b = np.array(comp), np.array(busco)
            rank = lambda a: np.argsort(np.argsort(a))  # noqa: E731
            agree = {"n": len(c), "pearson": round(float(np.corrcoef(c, b)[0, 1]), 3),
                     "spearman": round(float(np.corrcoef(rank(c), rank(b))[0, 1]), 3),
                     "median_abs_diff": round(float(np.median(np.abs(c - b))), 3),
                     # the case that matters: does the score catch what BUSCO calls incomplete?
                     "median_score_where_busco_below_90": round(float(np.median(c[b < 0.9])), 3)
                     if (b < 0.9).any() else None,
                     "median_score_where_busco_at_least_97": round(float(np.median(c[b >= 0.97])), 3)
                     if (b >= 0.97).any() else None}
        allc = np.array([out[u]["completeness"] for u, _ in mine])
        summary["kingdoms"][k] = {
            "proteomes": len(mine), "reference_proteomes": n_ref, "basis": basis,
            "markers": len(fams), "marker_examples": fams[:12],
            "score_percentiles": {p: round(float(np.percentile(allc, p)), 3) for p in (5, 25, 50, 75, 95)},
            "share_below_0.9": round(float((allc < 0.9).mean()), 3),
            "share_below_0.5": round(float((allc < 0.5).mean()), 3),
            "agreement_with_busco": agree,
            "markers_full": fams,
        }
        print(f"{k:12s} {len(mine):6d}종  마커 {len(fams):3d}개 ({basis})  "
              f"중앙 완전도 {summary['kingdoms'][k]['score_percentiles'][50]:.2f}  "
              f"0.9 미만 {summary['kingdoms'][k]['share_below_0.9']:.1%}"
              + (f"  BUSCO와 스피어만 {agree['spearman']}" if agree else ""))
    (OUT / "completeness.json").write_text(json.dumps(out, separators=(",", ":")))
    (RES / "summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=1))
    print(f"\n{len(out)} proteomes -> {OUT}/completeness.json, {RES}/summary.json")


if __name__ == "__main__":
    main()
