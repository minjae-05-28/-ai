"""How much horizontal transfer is in OUR data? (not where the method breaks — that is hgt_limit.py)

    PYTHONPATH=src python scripts/hgt_rate.py [--levels 0,0.02,0.05,0.1,0.2,0.35,0.5,0.8]

results/hgt_limit/ measured where ancestral reconstruction fails: calibration breaks above a
transfer level of 0.5, ranking above 0.8, size starts inflating around 0.35. What was never
measured is where our own clades sit on that scale, so the thresholds could not be applied.

The estimator: fit each family its own gain and loss rate on an uncapped grid and look at the
distribution of the fitted gain/loss ratio. Transfer makes a family appear in tips that are not
each other's relatives, which the model can only explain by raising that family's gain rate.

The statistic has no meaning on its own, so it is CALIBRATED: the same estimator is run on data
simulated on the same tree at known transfer levels, giving a curve from statistic to level, and
the real data is read off that curve. Calibration is per tree, because branch lengths set how much
transfer a given level produces.
"""

import argparse
import json
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
from mito_model_search import GENERATORS, fit, load_cache, simulate, visible_mask  # noqa: E402

OUT = Path("results/hgt_rate")
SPEC = {"ratio": None, "root": "stationary", "min_busco": 0, "drop_mag": False, "mult": 14.0, "tip_mult": 1.0}
# The thresholds hgt_limit.py measured, for reading the answer.
GATES = [(0.35, "크기(유전자군 수) 부풀기 시작"), (0.5, "확률 보정이 깨짐"), (0.8, "순위도 무너짐")]


def statistic(d, X, vis, spec=SPEC):
    """Median fitted gain/loss ratio over families, plus the share the model has to call gain-heavy."""
    g, lo, root, mult, _ = fit(d, X, vis, spec)
    q = np.asarray(g, dtype=float) / np.maximum(np.asarray(lo, dtype=float), 1e-9)
    return {"median_q": float(np.median(q)), "mean_log10_q": float(np.mean(np.log10(np.clip(q, 1e-3, 1e3)))),
            "share_q_ge_1": float((q >= 1).mean()), "share_q_ge_0.3": float((q >= 0.3).mean())}


def calibrate(d, levels, n_fam, reps, vis, label):
    curve = []
    for lv in levels:
        gen = dict(GENERATORS["reduced_x5"])
        gen["hgt"] = lv
        vals = []
        for rep in range(reps):
            _, obs = simulate(d, gen, n_fam, seed=7000 + rep)
            vals.append(statistic(d, obs, vis))
        row = {"hgt": lv, **{k: round(float(np.mean([v[k] for v in vals])), 4) for k in vals[0]}}
        curve.append(row)
        print(f"  [{label}] hgt {lv:<5} -> median q {row['median_q']:.3f}  "
              f"q>=0.3 {row['share_q_ge_0.3']:.3f}  q>=1 {row['share_q_ge_1']:.3f}", flush=True)
    return curve


def read_off(curve, value, key="share_q_ge_0.3"):
    """Where on the calibration curve the observed statistic falls.

    The curve saturates: past a transfer level of about 0.1 the statistic sits at 1.0 and several
    levels share it. Interpolating over the tied points is meaningless (and undefined for
    np.interp), so only the strictly increasing part is used and anything above it is reported as
    off the top of the scale rather than as a number.
    """
    rows = sorted(curve, key=lambda c: c["hgt"])
    xs, ys, last = [], [], -np.inf
    for c in rows:
        if c[key] > last + 1e-9:
            xs.append(c["hgt"])
            ys.append(c[key])
            last = c[key]
    if value <= ys[0]:
        return float(xs[0]), "아래로 벗어남 (전달 신호가 모의 0 수준 이하)"
    if value >= ys[-1]:
        return float(xs[-1]), f"위로 벗어남 — 곡선이 {xs[-1]}에서 포화해 그 위는 구분 불가"
    return float(np.interp(value, ys, xs)), "보간"


def load_lineage(path):
    if not path:
        return None
    return {r["organism"].replace("'", ""): r["lineage"]
            for r in json.loads(Path(path).read_text())["lineage"].values()}


def clade_tree(tree, genera=(), kingdom=None, root_outgroup=False, root_split=None, lineage=None):
    from run_clade_ancestor import build
    d, fams, names, in_clade, _, _ = build(tree, set(genera), 100, kingdom, root_outgroup, root_split, lineage)
    # simulate() drops a tip's genes at busco/100, so feed it the completeness this data really has
    # (Entamoeba near 0.45) instead of a flat 90%.
    d["busco"] = np.clip(d["completeness_vec"] * 100, 5, 100)
    vis = np.zeros(len(d["parent"]), dtype=bool)
    vis[d["tips"]] = True
    return d, d["X"], vis, len(fams), names, in_clade


def amoeba_tree():
    genera = {"Acanthamoeba", "Balamuthia", "Cavenderia", "Dictyostelium", "Entamoeba", "Heterostelium",
              "Pelomyxa", "Planoprotostelium", "Polysphondylium", "Physarum", "Vermamoeba",
              "Mastigamoeba", "Tieghemostelium"}
    return clade_tree("results/phylo_tree/amoeba.nwk", genera)[:4]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--levels", default="0,0.02,0.05,0.1,0.2,0.35,0.5,0.8")
    ap.add_argument("--families", type=int, default=600)
    ap.add_argument("--reps", type=int, default=2)
    ap.add_argument("--out", default=str(OUT))
    ap.add_argument("--tree", default="", help="measure only this clade tree (written to <out>/<name>/)")
    ap.add_argument("--name", default="")
    ap.add_argument("--clade-kingdom", default="")
    ap.add_argument("--label", default="")
    ap.add_argument("--root-split", default="")
    ap.add_argument("--lineage", default="")
    args = ap.parse_args()
    out = Path(args.out) / args.name if args.tree else Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    levels = [float(x) for x in args.levels.split(",")]

    sets = {}
    if args.tree:
        cd, cX, cvis, nf = clade_tree(args.tree, (), args.clade_kingdom or None, not args.root_split,
                                      args.root_split or None, load_lineage(args.lineage))[:4]
        sets[args.name] = (cd, cX, cvis, nf, args.label or f"{args.name} ({len(cd['tips'])}종)")
    else:
        d = load_cache()
        sets["alphaproteobacteria"] = (d, d["X"], visible_mask(d, SPEC), d["X"].shape[1],
                                       "알파프로테오박테리아 (GTDB 종 대표 2,526종, 유전자군 1,500개 표본)")
        try:
            ad, aX, avis, nf = amoeba_tree()
            sets["amoebozoa"] = (ad, aX, avis, nf, "아메보조아 + 외군 (40종)")
        except Exception as e:
            print(f"amoeba tree unavailable: {e}")

    result = {
        "estimator": "유전자군별 적합된 획득/손실 비 (상한 없는 격자)", "gates": GATES,
        "limits": [
            "이 추정량은 전달과 '원래 획득이 잦은 것'(유전자 중복·신규 생성·수렴 획득)을 구분하지 못합니다. "
            "둘 다 모형에게는 획득률을 올리라는 신호이므로, 나온 값은 전달의 상한으로 읽어야 합니다.",
            "보정 곡선이 전달 0.1 위에서 포화합니다(통계량이 0.99에 붙음). 따라서 이 측정은 '0.35 아래인가'에만 "
            "답하고, 그보다 높은 값들끼리는 구분하지 못합니다.",
            "모의 자료는 reduced_x5 생성기(획득 <= 0.1 x 손실)로 만들었습니다. 실제 분류군의 바탕 획득률이 "
            "이보다 높으면 전달이 과대평가됩니다.",
            "불완전한 프로테옴은 실제로 있는 유전자군을 없는 것으로 만들어 손실 쪽 신호를 키우므로, 이 추정을 "
            "낮추는 쪽으로 작용합니다. 품질 보정(genome_quality.py)은 여기 적용하지 않았습니다.",
            "두 분류군의 유전자군 표본이 다릅니다. 알파프로테오박테리아는 모형 탐색 캐시의 1,500개로, 빈도 "
            "십분위마다 같은 수를 뽑은 층화 표본입니다(드문 유전자군이 자연 분포보다 많이 들어 있음). "
            "아메보조아는 5,771개 전부입니다. 드문 유전자군일수록 가짜 획득 신호가 많으므로 층화 표본은 "
            "전달을 높게 보이게 하는 쪽입니다 — 세균 값 0.005는 그런 의미에서 보수적인 상한입니다. "
            "두 수치를 서로 직접 비교하지 마세요.",
            "획득/손실 비는 격자값(0.01, 0.03, 0.1, 0.2, 0.3, 0.5, 1, 3, 10)에서만 나오므로 중앙값으로 읽은 "
            "값은 거칠고, 비율 통계량(q>=0.3)이 주 판독값입니다.",
        ],
        "sets": {}}
    for name, (dd, X, vis, nf, label) in sets.items():
        print(f"\n=== {label} ===", flush=True)
        obsstat = statistic(dd, X, vis)
        print(f"  실제 자료: median q {obsstat['median_q']:.3f}  q>=0.3 {obsstat['share_q_ge_0.3']:.3f}  "
              f"q>=1 {obsstat['share_q_ge_1']:.3f}", flush=True)
        curve = calibrate(dd, levels, args.families, args.reps, vis, name)
        est, how = read_off(curve, obsstat["share_q_ge_0.3"])
        est2, _ = read_off(curve, obsstat["median_q"], "median_q")
        verdict = [g for g, _ in GATES if est >= g]
        result["sets"][name] = {"label": label, "families": int(nf), "observed": obsstat,
                                "calibration": curve, "estimated_hgt": round(est, 3),
                                "estimated_hgt_by_median_q": round(est2, 3), "how": how,
                                "gates_passed": [f"{g} ({w})" for g, w in GATES if est < g],
                                "gates_broken": [f"{g} ({w})" for g, w in GATES if est >= g]}
        print(f"  => 추정 전달 수준 {est:.3f} ({how}); 중앙 q로 읽으면 {est2:.3f}")
        print(f"     깨진 기준: {verdict or '없음'}")
    (out / "summary.json").write_text(json.dumps(result, ensure_ascii=False, indent=1))
    print(f"\nDone -> {out}/summary.json")


if __name__ == "__main__":
    main()
