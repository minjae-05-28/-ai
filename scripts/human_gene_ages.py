"""Human gene ages from Lecio ancestors (pre-registration 16, docs/preregistration/2026-10-15_human_gene_ages.md).

    python scripts/human_gene_ages.py fit    -> results/human_gene_ages/strata_posteriors.json.gz
    python scripts/human_gene_ages.py ages   -> results/human_gene_ages/gene_ages.tsv, summary.json

Gene-family level only: presence or absence of Pfam families, never sequences.
"""

import argparse
import bisect
import gzip
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))

OUT = Path("results/human_gene_ages")
HUMAN = "Homo sapiens"

# (stratum, taxon name whose 90%-pure group node marks it); PS1/PS2 are LECA, PS4 is the unicellular-holozoan split
STRATA = [("PS1", "세포 생물 공통", None), ("PS2", "진핵생물", None), ("PS3", "후편모생물", "Opisthokonta"),
          ("PS4", "홀로조아", None), ("PS5", "동물", "Metazoa"), ("PS6", "진정후생동물", "Eumetazoa"),
          ("PS7", "좌우대칭동물", "Bilateria"), ("PS8", "후구동물", "Deuterostomia"), ("PS9", "척삭동물", "Chordata"),
          ("PS10", "척추동물", "Vertebrata"), ("PS11", "경골어류 이후", "Euteleostomi"), ("PS12", "사지동물", "Tetrapoda"),
          ("PS13", "양막류", "Amniota"), ("PS14", "포유류", "Mammalia"), ("PS15", "진수류", "Eutheria"),
          ("PS16", "영장류 이후", "Primates")]
UNICELLULAR_HOLOZOA = {"Choanoflagellata", "Filasterea", "Ichthyosporea"}
PROKARYOTE_SHARE = 0.05


def load_tree(drop=(), tree=None, base_only=False):
    """The learning-loop tree (or `tree`) with its tip lineages, minus the tips in `drop` (they lose their
    profile). base_only: the base tree before any grafting."""
    import learning_loop as ll
    if tree is not None:
        ll.current_tree = lambda: str(tree)
    from run_clade_ancestor import load_profiles as base_loader
    base_prof = ll.compact(base_loader())
    ll.load_shares_cache()
    held = ll.compact(ll.all_new_species())
    base_lin = {r["organism"].replace("'", ""): r["lineage"]
                for r in json.loads(Path("data/markers/leca2_pick.json").read_text())["lineage"].values()}
    lin_all = {**base_lin, **{k: v["lineage"] for k, v in held.items()}}
    prof_all = {**base_prof, **{k: {**v, "kingdom": "eukaryotes"} for k, v in held.items()}}
    if base_only:
        prof_all = dict(base_prof)
    for lab in drop:
        prof_all.pop(lab, None)
        prof_all.pop(lab.replace("'", ""), None)
    d, fams, names = ll.load_tree_rooted(lin_all, prof_all)
    names = {v: names[v] for v in d["tips"]}
    tip_name = {v: (held[n]["organism"] if n in held else n) for v, n in names.items()}
    tip_lin = {v: list(lin_all.get(n, [])) for v, n in names.items()}
    return d, fams, names, tip_name, tip_lin


def _tips_under(d):
    under = defaultdict(set)
    for v in d["tips"]:
        w = v
        while w != -1:
            under[int(w)].add(int(v))
            w = d["parent"][w]
    return under


def strata_nodes(d, tip_name, tip_lin):
    """Stratum node = common ancestor of every tip of the stratum's taxon on the taxonomy tree (deviation 2);
    PS4 = Holozoa (animals + unicellular holozoans)."""
    from run_clade_ancestor import mrca
    human = [v for v, n in tip_name.items() if n.startswith(HUMAN)]
    assert len(human) == 1, human
    h = human[0]
    path = set()
    w = h
    while w != -1:
        path.add(int(w))
        w = d["parent"][w]
    root = int(np.where(d["parent"] < 0)[0][0])
    nodes, notes = {"PS1": root, "PS2": root}, []
    for ps, _, taxon in STRATA[2:]:
        group = {"Metazoa"} | UNICELLULAR_HOLOZOA if ps == "PS4" else {taxon}
        A = [v for v, L in tip_lin.items() if group & set(L)]
        nodes[ps] = int(mrca(A, d["parent"], d["depth"]))
        if nodes[ps] not in path:
            notes.append(f"{ps} node {nodes[ps]} is not on the human path")
    return h, nodes, notes


TREE = Path("results/human_gene_ages/tree_taxonomy.nwk")


def fit():
    d, fams, names, tip_name, tip_lin = load_tree(tree=TREE)
    print(f"taxonomy tree: {len(d['tips'])} tips, {len(fams)} families", flush=True)
    h, nodes, notes = strata_nodes(d, tip_name, tip_lin)
    drop = []
    for n in notes:
        print("NOTE", n, flush=True)
    import learning_loop as ll
    from tree_scramble_transfer import PLASTID
    want = sorted(set(nodes.values()))
    post, _, info = ll.fit_model(d, fams, want)
    plastid = np.array([bool(PLASTID & set(tip_lin[v])) for v in d["tips"]])
    X = d["X"][d["tips"]]
    enriched = X[plastid].mean(0) > 2 * X[~plastid].mean(0)
    vis_h = np.zeros(len(d["parent"]), bool)
    vis_h[np.array(d["tips"])[~plastid]] = True
    post_h, _, _ = ll.fit_model(d, fams, want, vis=vis_h)
    tips_under = defaultdict(list)
    for i, v in enumerate(d["tips"]):
        w = v
        while w != -1:
            tips_under[int(w)].append(i)
            w = d["parent"][w]
    for v in want:                       # all human-path strata nodes are animal or deeper: H2 where < 50% plastid
        if plastid[tips_under[v]].mean() < 0.5:
            post[v] = np.where(enriched, post_h[v], post[v])
    # tips present per family, for the classic phylostratigraphy baseline: which outgroup branch has the family
    outgroup = {}
    ps_list = [ps for ps, _, _ in STRATA]
    for k in range(2, len(ps_list)):
        inner, outer = set(tips_under[nodes[ps_list[k]]]), set(tips_under[nodes[ps_list[k - 1]]])
        idx = sorted(outer - inner)
        outgroup[ps_list[k]] = (X[idx].sum(0) > 0) if idx else np.zeros(len(fams), bool)
    import leca_v3_model as lv
    share = np.array([max(lv._SHARES["bacteria"].get(f, 0), lv._SHARES["archaea"].get(f, 0)) for f in fams])
    human_has = d["X"][h] > 0
    res = {"families": list(fams), "human_has": human_has.astype(int).tolist(),
           "prokaryote_share": [round(float(x), 6) for x in share],
           "strata": {ps: {"name": nm, "node": nodes[ps], "n_tips": len(tips_under[nodes[ps]]),
                           "posterior": [round(float(x), 4) for x in post[nodes[ps]]]} for ps, nm, _ in STRATA},
           "outgroup_has": {ps: m.astype(int).tolist() for ps, m in outgroup.items()},
           "fit": {"m": info["m"], "plastid_enriched": int(enriched.sum()), "tips": len(d["tips"]),
                   "dropped": len(drop)}, "notes": notes}
    with gzip.open(OUT / "strata_posteriors.json.gz", "wt") as f:
        json.dump(res, f)
    merged = Counter(nodes.values())
    print("strata nodes:", {ps: (nodes[ps], len(tips_under[nodes[ps]])) for ps in nodes}, flush=True)
    print("shared nodes:", {v: c for v, c in merged.items() if c > 1}, flush=True)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("step", choices=["fit", "ages"])
    a = ap.parse_args()
    if a.step == "fit":
        fit()
    else:
        ages()


LS_BIN = {"Cellular_organisms": 1, "Euk_Archaea": 1, "Euk+Bac": 1, "Eukaryota": 2, "Opisthokonta": 3,
          "Eumetazoa": 4, "Vertebrata": 5, "Mammalia": 6}


def ls_bin(k):
    """Our stratum index (1..16) on Litman & Stein's coarser scale (1..6)."""
    return 1 if k == 1 else 2 if k == 2 else 3 if k == 3 else 4 if k <= 9 else 5 if k <= 13 else 6


def family_ages(res):
    """Lecio age and classic (any-hit) age of every model family, as stratum indices 1..16, plus the grade
    of the Lecio call at its age node."""
    fams = res["families"]
    P = np.array([res["strata"][f"PS{k}"]["posterior"] for k in range(1, 17)])     # 16 x F
    share = np.array(res["prokaryote_share"])
    present = P >= 0.5
    k_old = np.where(present.any(0), present.argmax(0) + 1, 16)
    lecio = np.where((k_old == 1) & (share < PROKARYOTE_SHARE), 2, k_old)          # PS1 vs PS2 at LECA
    conf = np.abs(P - 0.5) * 2
    grade = np.select([conf >= 0.98, conf >= 0.9, conf >= 0.6], ["A", "B", "C"], "D")
    g_at = grade[np.minimum(k_old, 16) - 1, np.arange(len(fams))]
    classic = np.full(len(fams), 16)
    for k in range(16, 2, -1):                         # oldest outgroup branch holding the family wins
        classic = np.where(np.array(res["outgroup_has"][f"PS{k}"]) > 0, k - 1, classic)
    classic = np.where(share > 0, 1, classic)
    return {f: (int(lecio[i]), int(classic[i]), str(g_at[i])) for i, f in enumerate(fams)}


def ages():
    from scipy.stats import spearmanr
    with gzip.open(OUT / "strata_posteriors.json.gz", "rt") as f:
        res = json.load(f)
    fa = family_ages(res)
    meta = json.loads(Path("data/eukaryotes/pfam_meta.json").read_text())
    acc2name = {m["accession"].split(".")[0]: n for n, m in meta.items()}
    rows = []
    with gzip.open("data/human/uniprot_human.tsv.gz", "rt") as f:
        next(f)
        for line in f:
            acc, gene, pfam, geneid, _ = (line.rstrip("\n").split("\t") + [""] * 5)[:5]
            doms = [acc2name.get(x) for x in pfam.split(";") if x]
            inm = sorted({x for x in doms if x in fa})
            row = {"accession": acc, "gene": gene, "entrez": geneid.split(";")[0], "n_pfam": len([x for x in pfam.split(";") if x]),
                   "domains_in_model": inm}
            if inm:
                la = [fa[x][0] for x in inm]
                ca = [fa[x][1] for x in inm]
                row.update(age=max(la), age_oldest_domain=min(la), age_classic=max(ca),
                           grade=fa[inm[int(np.argmax(la))]][2])
            rows.append(row)
    aged = [r for r in rows if "age" in r]
    ls = {}
    with open("data/human/litman_stein/Main__main_HUMAN.csv") as f:
        head = next(f).rstrip().split(",")
        j = head.index("modeAge")
        for line in f:
            x = line.rstrip().split(",")
            if x[j] in LS_BIN:
                ls[x[0]] = LS_BIN[x[j]]
    uc = lambda k, holo=False: k <= (4 if holo else 3)

    def compare(key, holo=False):
        both = [(r[key], ls[r["accession"]]) for r in aged if r["accession"] in ls]
        a = np.array([uc(k, holo) for k, _ in both])
        b = np.array([l <= 3 for _, l in both])
        rho = spearmanr([ls_bin(k) for k, _ in both], [l for _, l in both]).correlation
        return {"n": len(both), "uc_mc_agreement": round(float((a == b).mean()), 4),
                "ours_uc_share": round(float(a.mean()), 4), "litman_uc_share": round(float(b.mean()), 4),
                "spearman_6_bins": round(float(rho), 4)}
    fam_l = np.array([v[0] for v in fa.values()])
    fam_c = np.array([v[1] for v in fa.values()])
    gl = np.array([r["age"] for r in aged])
    gc = np.array([r["age_classic"] for r in aged])
    sanity = {}
    for name, test in [("ribosomal RPL/RPS", lambda g: g.startswith(("RPL", "RPS")) and not g.startswith("RPS6K")),
                       ("MHC I (HLA-A/B/C)", lambda g: g in ("HLA-A", "HLA-B", "HLA-C"))]:
        sel = [r["age"] for r in aged if test(r["gene"])]
        sanity[name] = dict(sorted(Counter(f"PS{k}" for k in sel).items(), key=lambda x: int(x[0][2:])))
    summary = {
        "families": {"n": len(fa), "lecio_by_stratum": dict(Counter(f"PS{k}" for k in fam_l)),
                     "grade_at_age_node": dict(Counter(v[2] for v in fa.values())),
                     "lecio_minus_classic_mean_index": round(float((fam_l - fam_c).mean()), 3),
                     "lecio_younger_share": round(float((fam_l > fam_c).mean()), 4),
                     "lecio_older_share": round(float((fam_l < fam_c).mean()), 4),
                     "spearman_lecio_classic": round(float(spearmanr(fam_l, fam_c).correlation), 4)},
        "genes": {"uniprot_reviewed": len(rows), "with_age": len(aged),
                  "lecio_by_stratum": dict(sorted(Counter(f"PS{r['age']}" for r in aged).items(), key=lambda x: int(x[0][2:]))),
                  "grade_at_age_node": dict(Counter(r["grade"] for r in aged)),
                  "lecio_minus_classic_mean_index": round(float((gl - gc).mean()), 3),
                  "spearman_lecio_classic": round(float(spearmanr(gl, gc).correlation), 4)},
        "litman_stein": {"primary_youngest_domain": compare("age"),
                         "secondary_oldest_domain": compare("age_oldest_domain"),
                         "classic_baseline": compare("age_classic"),
                         "sensitivity_PS4_as_UC": compare("age", holo=True)},
        "gate_pass": None, "sanity": sanity, "strata_nodes": {k: v["node"] for k, v in res["strata"].items()},
        "fit": res["fit"], "notes": res["notes"]}
    summary["gate_pass"] = summary["litman_stein"]["primary_youngest_domain"]["uc_mc_agreement"] >= 0.60
    (OUT / "summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=1))
    with open(OUT / "gene_ages.tsv", "w") as f:
        f.write("accession\tgene\tentrez\tage_stratum\tage_name\tunicellular\tgrade\tage_oldest_domain\tage_classic\tdomains\n")
        names = {f"PS{k}": nm for k, (_, nm, _) in enumerate(STRATA, 1)}
        for r in aged:
            f.write(f"{r['accession']}\t{r['gene']}\t{r['entrez']}\tPS{r['age']}\t{names['PS' + str(r['age'])]}\t"
                    f"{int(r['age'] <= 3)}\t{r['grade']}\tPS{r['age_oldest_domain']}\tPS{r['age_classic']}\t"
                    f"{','.join(r['domains_in_model'])}\n")
    print(json.dumps(summary, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
