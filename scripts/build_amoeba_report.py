"""Chart data and a full family table for the amoebozoan ancestor report.

    PYTHONPATH=src python scripts/build_amoeba_report.py

Reads results/clade_ancestor/amoebozoa/ (written by run_clade_ancestor.py) and writes
  report_data.json  figures for the report page
  families.tsv      every family's posterior, spread and present-day share

Nothing here reinterprets the reconstruction: the marker panel is the same one the law card
carries, and the Korean glosses name what each family does. No ancestor size is derived,
because the subsampling experiment showed a 16-17% underestimate at this sample size.
"""

import json
from collections import Counter
from pathlib import Path

import numpy as np

R = Path("results/clade_ancestor/amoebozoa")

# Marker families, grouped as the law card groups them, with a Korean gloss each.
GROUPS = [
    ("위족 (기어다니고 감싸기)", "live", [
        ("Actin", "액틴"), ("ARPC4", "ARP2/3 — 액틴 가지내기"), ("FH2", "포르민 — 액틴 신장"),
        ("Cofilin_ADF", "코필린 — 해체"), ("Gelsolin", "젤솔린 — 절단"), ("Myosin_head", "미오신 — 수축"),
        ("Filamin", "필라민 — 액틴 그물"), ("Rho_GDI", "Rho 신호 — 이동 방향")]),
    ("식세포작용 (삼켜 녹이기)", "live", [
        ("PX", "식세포작용 지질 신호"), ("SNARE", "막 융합"), ("V_ATPase_I", "액포 산성화"),
        ("Clathrin", "피막소포 운반"), ("Vps35", "레트로머"), ("Glyco_hydro_18", "키틴가수분해효소 — 균류 먹이"),
        ("ATG8", "자가포식")]),
    ("핵과 성", "live", [
        ("Histone", "히스톤"), ("TP6A_N", "SPO11 — 감수분열 교차 개시"), ("Telomerase_RBD", "텔로머라아제"),
        ("Cyclin_N", "사이클린 — 세포주기"), ("DNA_pol_A", "DNA 중합효소"), ("RNA_pol_Rpb1_1", "RNA 중합효소 II")]),
    ("산소호흡 (핵이 만드는 부품)", "live", [
        ("ATP-synt_ab", "ATP 합성효소 α/β"), ("Complex1_51K", "복합체 I 51 kDa"),
        ("ATP-synt_D", "ATP 합성효소 D"), ("Mito_carr", "미토콘드리아 운반체"),
        ("Porin_3", "외막 포린 (VDAC)"), ("NDUFA12", "복합체 I 보조")]),
    ("소기관과 산화환원", "live", [
        ("Pex2_Pex12", "퍼옥시좀 단백질 수입"), ("Catalase", "카탈라아제"), ("Thioredoxin", "티오레독신"),
        ("Tubulin", "튜불린"), ("Kinesin", "키네신"), ("Proteasome", "프로테아좀"),
        ("Calreticulin", "칼레티쿨린 — 접힘 감시")]),
    ("신호전달", "live", [
        ("Ras", "Ras"), ("Pkinase", "단백질 인산화효소"), ("PH", "PH 영역"),
        ("PDEase_I", "cAMP 분해효소"), ("SH3_1", "SH3")]),
    ("편모 — 이 표본으로 판정 불가", "ghost", [
        ("IFT52_GIFT", "섬모내 운반"), ("BBS2_Mid", "BBSome"), ("Radial_spoke_3", "축사 방사살"),
        ("IFT57", "섬모내 운반")]),
    ("자실체(다세포) — 지지되지 않음", "ghost", [
        ("Chitin_bind_1", "키틴 결합"), ("Lectin_C", "C형 렉틴")]),
    ("미토콘드리아 유전체가 만드는 부품 — 자료의 흠", "artifact", [
        ("COX2", "사이토크롬 c 산화효소 II"), ("COX3", "사이토크롬 c 산화효소 III"),
        ("Cytochrome_B", "사이토크롬 b"), ("Complex1_49kDa", "복합체 I 49 kDa"), ("NADHdh", "NADH 탈수소효소")]),
]
SAMPLE = [("세포성 점균 (딕티오스텔리움류)", 8), ("엔타모에바 (장 기생)", 3), ("아칸타모에바 (토양)", 1)]


def main():
    s = json.loads((R / "summary.json").read_text())
    z = np.load(R / "posterior.npz", allow_pickle=False)
    fams, p, msd, tsd, cf = (z["families"], z["posterior"], z["model_sd"], z["tree_sd"],
                             z["clade_frequency"])
    col = {f: i for i, f in enumerate(fams)}
    meta = json.loads(Path("data/eukaryotes/pfam_meta.json").read_text())

    def desc(f):
        return (meta.get(f) or {}).get("description", "")

    rows = []
    for title, kind, items in GROUPS:
        g = []
        for f, ko in items:
            if f not in col:
                continue
            i = col[f]
            g.append({"family": f, "ko": ko, "p": round(float(p[i]), 3),
                      "msd": round(float(msd[i]), 3), "tsd": round(float(tsd[i]), 3),
                      "today": round(float(cf[i]), 3), "desc": desc(f)})
        rows.append({"title": title, "kind": kind, "families": g})

    # Density of all families in the (present-day share, posterior) plane: a 2D grid, so the
    # whole set is shown without plotting 5,771 marks.
    NB = 20
    grid = np.zeros((NB, NB), dtype=int)
    for a, b in zip(cf, p):
        grid[min(int(b * NB), NB - 1), min(int(a * NB), NB - 1)] += 1

    # The two tails of the gap: families the ancestor had that few descendants kept, and
    # families common today that the reconstruction puts after this node.
    gap = p - cf
    def tail(idx):
        return [{"family": str(fams[i]), "p": round(float(p[i]), 3), "today": round(float(cf[i]), 3),
                 "gap": round(float(gap[i]), 2), "desc": desc(str(fams[i]))} for i in idx]

    out = {
        "validation": {"reconstruction": s["leave_tips_out_auroc"]["reconstruction"],
                       "clade_frequency": s["leave_tips_out_auroc"]["clade_frequency"],
                       "bacteria_reconstruction": 0.985, "bacteria_frequency": 0.962},
        "counts": {"clade_tips": s["clade_tips"], "outgroup_tips": s["tips"] - s["clade_tips"],
                   "families": s["families_considered"], "confident": s["n_confident_families"],
                   "uncertain": s["n_uncertain_families"], "bootstrap_trees": s["n_bootstrap_trees"],
                   "models": s["n_models"]},
        "sample": [{"label": k, "n": v} for k, v in SAMPLE],
        "species": s["clade_species"], "reduced": s["reduced_lineages"],
        "groups": rows,
        "histogram": np.histogram(p, bins=20, range=(0, 1))[0].tolist(),
        "density": {"bins": NB, "grid": grid.tolist(), "max": int(grid.max())},
        "lost_by_descendants": tail(np.argsort(-gap)[:12]),
        "after_this_node": tail(np.argsort(gap)[:12]),
        "functions": s["functions_of_confident_families"][:12],
    }
    (R / "report_data.json").write_text(json.dumps(out, ensure_ascii=False, separators=(",", ":")))
    with (R / "families.tsv").open("w") as f:
        f.write("family\tposterior\tmodel_sd\ttree_sd\tshare_of_clade_tips_today\tdescription\n")
        for i in np.argsort(-p):
            f.write(f"{fams[i]}\t{p[i]:.4f}\t{msd[i]:.4f}\t{tsd[i]:.4f}\t{cf[i]:.4f}\t{desc(str(fams[i]))}\n")
    print(f"report_data.json ({(R / 'report_data.json').stat().st_size // 1024} KB), "
          f"families.tsv ({len(fams)} rows)")
    print("marker families found:", sum(len(g['families']) for g in rows))


if __name__ == "__main__":
    main()
