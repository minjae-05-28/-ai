"""Does the tilt-SREBP link survive adjusting for the epithelial state itself? (pre-registration 26,
docs/preregistration/2026-10-16_tilt_vs_epithelial.md)

    python scripts/tilt_vs_epithelial.py   -> results/srebp/epithelial_control.json
"""

import json
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
from drug_fetch import rank_center  # noqa: E402
from tilt_vs_emt import partial, resid, scores  # noqa: E402

OUT = Path("results/srebp/epithelial_control.json")
MIN_STRATUM = 100


def with_states():
    rows = [x.split("\t") for x in Path("data/emt/scores.tsv").read_text().splitlines()[1:]]
    return {r[0]: {"lineage": r[1], "tilt": float(r[2]), "prol": float(r[3]), "epi": float(r[4]),
                   "mes": float(r[5]), "emt": float(r[6]), "stem": float(r[7])} for r in rows}


def module_rows(path, cols):
    rows = [x.split("\t") for x in Path(path).read_text().splitlines()[1:]]
    F = np.array([[float(v) if v not in ("", "NA", "nan") else np.nan for v in r[cols]] for r in rows])
    ok = ~np.isnan(F).any(1)
    return [r[0] for r, o in zip(rows, ok) if o], F[ok]


def vif(cols):
    """Variance inflation factor per column (rank-transformed inputs)."""
    out = []
    for j in range(len(cols)):
        y = cols[j]
        others = [c for k, c in enumerate(cols) if k != j]
        r = resid(y, others)
        ss = np.var(y)
        out.append(round(float(ss / max(np.var(r), 1e-12)), 2))
    return out


def arm(lines, mod, S):
    g = np.array([S[l]["lineage"] for l in lines])
    get = lambda k: np.array([S[l][k] for l in lines])
    t, p, e, m, s = get("tilt"), get("prol"), get("epi"), get("mes"), get("stem")
    out = {"lines": len(lines),
           "primary_full_adjustment": partial(mod, t, [p, e, m, s], g),
           "steps": {"lineage_plus_prol": partial(mod, t, [p], g, boot=False),
                     "plus_epithelial": partial(mod, t, [p, e], g, boot=False),
                     "plus_mesenchymal": partial(mod, t, [p, e, m], g, boot=False),
                     "plus_stemness": partial(mod, t, [p, e, m, s], g, boot=False)},
           "epi_vs_module_given_prol": partial(mod, e, [p], g),
           "mes_vs_module_given_prol": partial(mod, m, [p], g),
           "epi_vs_module_given_prol_tilt": partial(mod, e, [p, t], g),
           "mes_vs_module_given_prol_tilt": partial(mod, m, [p, t], g),
           "tilt_vs_states_pearson": {"epithelial": round(float(np.corrcoef(t, e)[0, 1]), 3),
                                      "mesenchymal": round(float(np.corrcoef(t, m)[0, 1]), 3)},
           "vif_tilt_prol_epi_mes_stem": vif([rank_center(x, g) for x in (t, p, e, m, s)])}
    # tilt residual after removing the epithelial score
    tr = rank_center(t, g)
    res_t = resid(tr, [rank_center(e, g)])
    out["tilt_residual_after_epithelial"] = partial(mod, res_t, [p], g)
    # strata by epithelial score
    cut = np.median(e)
    strat = {}
    for name, mask in (("epithelial_high", e >= cut), ("epithelial_low", e < cut)):
        if mask.sum() >= MIN_STRATUM:
            strat[name] = partial(mod[mask], t[mask], [p[mask]], g[mask])
        else:
            strat[name] = {"n": int(mask.sum()), "skipped": f"fewer than {MIN_STRATUM}"}
    out["strata"] = strat
    return out


def main():
    S = with_states()
    arms = {}
    for name, path, cols in (("depmap", "data/emt/depmap_module.tsv", slice(1, 6)),
                             ("project_score", "data/srebp/score_module.tsv", slice(2, 7))):
        if not Path(path).exists():
            continue
        keep, F = module_rows(path, cols)
        pick = [k for k, l in enumerate(keep) if l in S]
        keep, F = [keep[k] for k in pick], F[pick]
        Z = (F - F.mean(0)) / (F.std(0) + 1e-9)
        arms[name] = arm(keep, Z.mean(1), S)
    v = [a["primary_full_adjustment"]["verdict"] for a in arms.values()]
    res = {"arms": arms,
           "overall": {"arms": len(v), "positive": v.count("양성"),
                       "call": "상피 상태로 설명되지 않음" if v and all(x == "양성" for x in v)
                       else ("상피 상태로 설명됨" if v and not any(x == "양성" for x in v) else "판단 보류")}}
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(res, ensure_ascii=False, indent=1))
    print(json.dumps(res, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
