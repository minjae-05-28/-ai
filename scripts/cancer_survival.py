"""Is a tumour with stronger unicellular tilt more lethal? (pre-registration 28,
docs/preregistration/2026-10-17_tilt_and_survival.md)

    python scripts/cancer_survival.py   -> results/cancer_survival/summary.json

Cox proportional hazards (Breslow ties) fitted by Newton-Raphson, hazard ratio per standard deviation
of the tilt score, 2,000-patient bootstrap interval (seed 0).
"""

import json
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import cancer_atavism as ca  # noqa: E402

TILT = Path("data/tcga_stage")
SURV = Path("data/tcga_survival")
OUT = Path("results/cancer_survival")
MIN_PATIENTS = 50
MIN_DEATHS = 10
TWO_THIRDS = 2 / 3


def cox(X, time, event, iters=50, ridge=1e-6):
    """Breslow partial likelihood. X: n x p (already centred/scaled), returns coefficients or None."""
    n, p = X.shape
    order = np.argsort(-time)                       # longest first: risk sets grow by cumulative sum
    X, time, event = X[order], time[order], event[order]
    # tied times share one risk set (Breslow): the last row of each tied group. Fixed by the data, so it is
    # computed once rather than inside the Newton loop.
    change = np.diff(time) != 0
    group_end = np.r_[np.flatnonzero(change), n - 1]
    last = group_end[np.r_[0, np.cumsum(change)]]
    idx = last[event == 1]
    if len(idx) == 0:
        return None
    Xd = X[event == 1].sum(0)
    b = np.zeros(p)
    for _ in range(iters):
        eta = np.clip(X @ b, -30, 30)
        w = np.exp(eta)
        # risk set of a death at t = everyone with time >= t; with time descending that is a running sum,
        # and tied times must share the same running sum (Breslow)
        cw = np.cumsum(w)
        cwx = np.cumsum(w[:, None] * X, 0)
        cwxx = np.cumsum(w[:, None, None] * (X[:, :, None] * X[:, None, :]), 0)
        S0 = cw[idx]
        S1 = cwx[idx] / S0[:, None]
        grad = Xd - S1.sum(0)
        H = (cwxx[idx] / S0[:, None, None]).sum(0) - np.einsum("mj,mk->jk", S1, S1)
        H += ridge * np.eye(p)
        try:
            step = np.linalg.solve(H, grad)
        except np.linalg.LinAlgError:
            return None
        if not np.all(np.isfinite(step)):
            return None
        step = np.clip(step, -5, 5)
        b = b + step
        if np.max(np.abs(step)) < 1e-7:
            break
    return b if np.all(np.isfinite(b)) else None


def concordance(score, time, event):
    """Harrell C: over comparable pairs, how often the higher score dies earlier."""
    n = len(time)
    num = den = 0.0
    for i in range(n):
        if not event[i]:
            continue
        later = time > time[i]
        if not later.any():
            continue
        den += later.sum()
        num += (score[later] < score[i]).sum() + 0.5 * (score[later] == score[i]).sum()
    return num / den if den else np.nan


def fit_hr(X, time, event, boot=ca.N_BOOT):
    """Hazard ratio of the first column, with a patient bootstrap interval."""
    b = cox(X, time, event)
    if b is None:
        return {"skipped": "model did not converge"}
    rng = np.random.default_rng(ca.SEED)
    n, bs = len(time), []
    for _ in range(boot):
        s = rng.integers(0, n, n)
        bb = cox(X[s], time[s], event[s])
        if bb is not None:
            bs.append(bb[0])
    if len(bs) < boot // 2:
        return {"log_hr": round(float(b[0]), 4), "skipped": "bootstrap did not converge"}
    lo, hi = np.percentile(bs, [2.5, 97.5])
    return {"hr": round(float(np.exp(b[0])), 4), "lo": round(float(np.exp(lo)), 4),
            "hi": round(float(np.exp(hi)), 4), "log_hr": round(float(b[0]), 4),
            "log_hr_se": round(float(np.std(bs, ddof=1)), 4), "n_boot_ok": len(bs),
            "verdict": "양성" if lo > 0 else ("음성" if hi < 0 else "무승부")}


def load(c):
    """Patients of one cohort with tilt, survival and covariates; returns a dict of arrays."""
    tf, sf = TILT / f"{c}.tsv", SURV / f"{c}.tsv"
    if not (tf.exists() and sf.exists()):
        return None
    tilt = {}
    for line in tf.read_text().splitlines()[1:]:
        x = line.split("\t")
        if len(x) >= 7 and x[1] == "tumour":
            tilt[x[0][:12]] = (float(x[3]), float(x[4]), float(x[5]), float(x[6]))
    rows = []
    for line in sf.read_text().splitlines()[1:]:
        x = line.split("\t")
        if len(x) < 5 or x[0] not in tilt:
            continue
        d, s, i, t = tilt[x[0]]
        rows.append((float(x[1]), int(x[2]), x[3], x[4], d, s, i, t))
    if not rows:
        return None
    time = np.array([r[0] for r in rows], float)
    event = np.array([r[1] for r in rows], int)
    age = np.array([float(r[2]) if r[2] else np.nan for r in rows])
    stage = np.array([float(r[3]) if r[3] else np.nan for r in rows])
    d = np.array([r[4] for r in rows])
    z = lambda v: (v - np.nanmean(v)) / (np.nanstd(v) or 1.0)
    return {"time": time, "event": event, "age": age, "stage": stage,
            "delta": z(d), "s": z(np.array([r[5] for r in rows])),
            "i": z(np.array([r[6] for r in rows])), "t": z(np.array([r[7] for r in rows])),
            "n": len(rows), "deaths": int(event.sum())}


def design(D, cols, keep=None):
    """Columns, dropping patients with a missing covariate; returns X, time, event, n used."""
    X = np.column_stack([D[c] for c in cols])
    ok = np.isfinite(X).all(1)
    if keep is not None:
        ok &= keep
    X = X[ok]
    for j in range(1, X.shape[1]):                  # centre and scale the adjustments, tilt stays first
        sd = X[:, j].std() or 1.0
        X[:, j] = (X[:, j] - X[:, j].mean()) / sd
    return X, D["time"][ok], D["event"][ok], int(ok.sum())


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    cohorts = sorted(p.stem for p in TILT.glob("*.tsv"))
    out = {"cohorts": {}, "min_patients": MIN_PATIENTS, "min_deaths": MIN_DEATHS}
    for c in cohorts:
        D = load(c)
        if D is None:
            out["cohorts"][c] = {"skipped": "no overlapping patients"}
            continue
        has_stage = np.isfinite(D["stage"]).sum() >= MIN_PATIENTS
        base = ["delta", "age", "stage"] if has_stage else ["delta", "age"]
        X, t, e, n = design(D, base)
        r = {"patients_with_tilt_and_survival": D["n"], "deaths": D["deaths"],
             "patients_used": n, "covariates": base}
        if n < MIN_PATIENTS or int(e.sum()) < MIN_DEATHS:
            r["skipped"] = f"fewer than {MIN_PATIENTS} patients or {MIN_DEATHS} deaths"
            out["cohorts"][c] = r
            continue
        r["primary"] = fit_hr(X, t, e)
        Xu, tu, eu, _ = design(D, ["delta"])
        r["aux1_unadjusted"] = fit_hr(Xu, tu, eu)
        Xa, ta, ea, na = design(D, base + ["s", "i", "t"])
        r["aux2_plus_proliferation_immune_stromal"] = fit_hr(Xa, ta, ea) if na >= MIN_PATIENTS else \
            {"skipped": "too few patients"}
        # auxiliary 3: median split, 5-year survival by Kaplan-Meier
        km = lambda tt, ee: np.prod([1 - ee[tt == u].sum() / (tt >= u).sum()
                                     for u in np.unique(tt[(ee == 1) & (tt <= 1825)])]) \
            if ((ee == 1) & (tt <= 1825)).any() else 1.0
        hi = D["delta"] > np.median(D["delta"])
        r["aux3_median_split_5y_survival"] = {
            "high_tilt": round(float(km(D["time"][hi], D["event"][hi])), 4),
            "low_tilt": round(float(km(D["time"][~hi], D["event"][~hi])), 4),
            "difference_high_minus_low": round(float(km(D["time"][hi], D["event"][hi]) -
                                                     km(D["time"][~hi], D["event"][~hi])), 4)}
        # auxiliary 4: stage I-II only
        if has_stage:
            early = np.isfinite(D["stage"]) & (D["stage"] <= 2)
            Xe, te, ee, ne = design(D, base, keep=early)
            r["aux4_stage_1_2_only"] = fit_hr(Xe, te, ee) if ne >= MIN_PATIENTS and ee.sum() >= MIN_DEATHS \
                else {"patients_used": ne, "deaths": int(ee.sum()), "skipped": "too few patients or deaths"}
        # auxiliary 5: concordance, tilt against the proliferation score
        r["aux5_concordance"] = {
            "tilt": round(float(concordance(D["delta"], D["time"], D["event"])), 4),
            "proliferation": round(float(concordance(D["s"], D["time"], D["event"])), 4)}
        # auxiliary 6: tilt against stage
        if has_stage:
            ok = np.isfinite(D["stage"])
            r["aux6_corr_tilt_stage"] = round(float(np.corrcoef(D["delta"][ok], D["stage"][ok])[0, 1]), 4)
        out["cohorts"][c] = r
    judged = {c: v["primary"] for c, v in out["cohorts"].items()
              if "primary" in v and "verdict" in v["primary"]}
    pos = [c for c, v in judged.items() if v["verdict"] == "양성"]
    neg = [c for c, v in judged.items() if v["verdict"] == "음성"]
    out["judged"] = len(judged)
    out["positive"], out["negative"] = sorted(pos), sorted(neg)
    out["undecided"] = sorted(c for c in judged if c not in pos and c not in neg)
    out["overall"] = ("지지" if judged and len(pos) >= TWO_THIRDS * len(judged) else "지지하지 않음") \
        if judged else "판정 불가"
    # inverse-variance fixed-effect combination of the per-cohort log hazard ratios
    w = [(judged[c]["log_hr"], judged[c]["log_hr_se"]) for c in judged if judged[c].get("log_hr_se")]
    if w:
        b = np.array([x[0] for x in w])
        se = np.array([x[1] for x in w])
        iv = 1 / np.maximum(se, 1e-6) ** 2
        m = float((b * iv).sum() / iv.sum())
        sm = float(np.sqrt(1 / iv.sum()))
        out["combined"] = {"hr": round(float(np.exp(m)), 4), "lo": round(float(np.exp(m - 1.96 * sm)), 4),
                           "hi": round(float(np.exp(m + 1.96 * sm)), 4), "cohorts": len(w)}
    (OUT / "summary.json").write_text(json.dumps(out, ensure_ascii=False, indent=1))
    print(json.dumps({k: v for k, v in out.items() if k != "cohorts"}, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
