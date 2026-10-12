"""Ancestor function atlas: for every ancestor in the learning-loop tree, which cellular functions it had,
gene family by gene family, with a reliability grade (docs/ancestor_atlas.md).

    python scripts/ancestor_atlas.py build     -> results/ancestor_atlas/atlas.json.gz (+ modules.json)
    python scripts/ancestor_atlas.py query "Homo sapiens"     (or a genus, family, ... name)

Gene-family level only: presence or absence of Pfam families, never sequences.
"""

import argparse
import base64
import gzip
import hashlib
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))

OUT = Path("results/ancestor_atlas")

# Cellular functions, each a set of GO slim terms (data/eukaryotes/family_annotations.json). Fixed before any
# ancestor was looked at; a family can belong to several functions.
MODULES = [
    ("nucleus", "핵·핵막·핵공 수송", ["GO:0005634", "GO:0005635", "GO:0005654", "GO:0005730", "GO:0006913",
                                  "GO:0000228"]),
    ("chromosome", "염색체·DNA 복제·텔로미어", ["GO:0005694", "GO:0006260", "GO:0032200"]),
    ("dna_repair", "DNA 수선·재조합", ["GO:0006281", "GO:0006310"]),
    ("chromatin", "크로마틴·RNA 간섭", ["GO:0006325", "GO:0031047"]),
    ("transcription", "전사·전사 조절", ["GO:0006351", "GO:0006355"]),
    ("mrna", "mRNA·snRNA 가공", ["GO:0016071", "GO:0016073"]),
    ("translation", "리보솜·번역·tRNA", ["GO:0005840", "GO:0042254", "GO:0006399", "GO:0002181"]),
    ("mitochondrion", "미토콘드리아", ["GO:0005739", "GO:0007005", "GO:0140053"]),
    ("energy", "에너지 대사(호흡 등)", ["GO:0006091"]),
    ("plastid", "엽록체·광합성", ["GO:0009536", "GO:0009579", "GO:0015979"]),
    ("er", "소포체", ["GO:0005783"]),
    ("golgi", "골지체", ["GO:0005794"]),
    ("vesicle", "소포 수송·엔도솜", ["GO:0016192", "GO:0031410", "GO:0005768", "GO:0006886"]),
    ("lysosome", "리소좀·액포·자가포식", ["GO:0005773", "GO:0005764", "GO:0006914", "GO:0007040"]),
    ("peroxisome", "퍼옥시좀", ["GO:0005777", "GO:0007031"]),
    ("cytoskeleton", "세포골격·중심체", ["GO:0005856", "GO:0007010", "GO:0005815"]),
    ("cilium", "섬모·편모·세포 운동", ["GO:0005929", "GO:0044782", "GO:0007018", "GO:0048870"]),
    ("mitosis", "세포분열", ["GO:0000278", "GO:0007059", "GO:0000910", "GO:0140014"]),
    ("meiosis", "감수분열·유성생식", ["GO:0140013", "GO:0022414"]),
    ("membrane", "세포막·막 수송체", ["GO:0005886", "GO:0055085", "GO:0061024"]),
    ("cell_wall", "세포벽·외피", ["GO:0005618", "GO:0030312", "GO:0071554"]),
    ("extracellular", "세포 밖 기질·부착", ["GO:0005576", "GO:0031012", "GO:0030198", "GO:0007155"]),
    ("signaling", "신호 전달", ["GO:0023052"]),
    ("proteostasis", "단백질 접힘·성숙·분해", ["GO:0006457", "GO:0051604", "GO:0030163"]),
    ("carbohydrate", "탄수화물 대사", ["GO:0005975", "GO:1901135"]),
    ("lipid", "지질 대사", ["GO:0006629"]),
    ("amino_acid", "아미노산·황 대사", ["GO:0006520", "GO:0006790", "GO:0006575"]),
    ("development", "다세포 발생·신경·면역", ["GO:0048856", "GO:0030154", "GO:0050877", "GO:0002376",
                                       "GO:0003013"]),
]

# Grades from the call's own confidence |2P - 1|. Pre-registration 11 found calibrated reliability no better
# than this confidence (draw); agreement with gene trees per band, test half of its 35,115 checks:
GRADES = [("A", 0.98, 0.965), ("B", 0.90, 0.781), ("C", 0.60, 0.655), ("D", 0.0, 0.548)]


def grade_agreement():
    """Recompute the agreement per confidence band from the stored gene-tree checks (pre-registration 11)."""
    z = np.load("results/reliability/checks.npz", allow_pickle=False)
    a, fams = z["rows"], [str(f) for f in z["families"]]
    a = a[a[:, 2] >= 0]
    agree = (a[:, 3] >= 0.5) == (a[:, 2] == 1)
    conf = np.abs(a[:, 3] - 0.5) * 2
    test = np.array([hashlib.md5(fams[int(j)].encode()).digest()[0] % 2 == 1 for j in a[:, 0]])
    out, hi = {}, 1.01
    for g, lo, _ in GRADES:
        m = test & (conf >= lo) & (conf < hi)
        out[g] = {"min_confidence": lo, "n": int(m.sum()), "agreement": round(float(agree[m].mean()), 3)}
        hi = lo
    return out


def module_families(universe):
    ann = json.loads(Path("data/eukaryotes/family_annotations.json").read_text())["families"]
    meta = json.loads(Path("data/eukaryotes/pfam_meta.json").read_text())
    fams = {}
    for key, _, gos in MODULES:
        fams[key] = sorted(f for f in universe if set(ann.get(f, {}).get("go_slim") or []) & set(gos))
    desc = {f: (meta.get(f, {}).get("description") or "")[:80] for fl in fams.values() for f in fl}
    return fams, desc


def build(min_tips=3):
    import learning_loop as ll
    from reliability import group_node
    from run_clade_ancestor import load_profiles as base_loader
    base_prof = ll.compact(base_loader())
    ll.load_shares_cache()
    held = ll.compact(ll.all_new_species())
    base_lin = {r["organism"].replace("'", ""): r["lineage"]
                for r in json.loads(Path("data/markers/leca2_pick.json").read_text())["lineage"].values()}
    lin_all = {**base_lin, **{k: v["lineage"] for k, v in held.items()}}
    prof_all = {**base_prof, **{k: {**v, "kingdom": "eukaryotes"} for k, v in held.items()}}
    d, fams, names = ll.load_tree_rooted(lin_all, prof_all)
    names = {v: names[v] for v in d["tips"]}
    tip_name = {v: (held[n]["organism"] if n in held else n) for v, n in names.items()}
    tip_lin = {v: list(lin_all.get(n, [])) for v, n in names.items()}
    print(f"tree: {len(d['tips'])} tips, {len(fams)} families", flush=True)
    # one node per taxon name (the 90%-pure group node), for taxa with >= min_tips tips
    members = defaultdict(set)
    for v, L in tip_lin.items():
        for t in L[:-1]:
            if t:
                members[t].add(v)
    root = int(np.where(d["parent"] < 0)[0][0])
    taxon_node = {}
    for t, m in members.items():
        if len(m) >= min_tips:
            node = group_node(d, m)
            if node is not None:
                taxon_node[t] = int(node)
    nodes = sorted(set(taxon_node.values()) | {root})
    print(f"{len(taxon_node)} taxa -> {len(nodes)} ancestor nodes", flush=True)
    post, _, info = ll.fit_model(d, fams, nodes)
    # Plastid gene transfer (pre-registration 4, H2): families concentrated in plastid-bearing lineages can come
    # from the plastid's own genome moved to the nucleus, which makes deep ancestors look photosynthetic. For
    # those families, ancestors whose tips are mostly NOT plastid-bearing use a fit with plastid tips hidden;
    # ancestors inside plastid lineages keep the ordinary fit.
    from tree_scramble_transfer import PLASTID
    plastid = np.array([bool(PLASTID & set(tip_lin[v])) for v in d["tips"]])
    X = d["X"][d["tips"]]
    enriched = X[plastid].mean(0) > 2 * X[~plastid].mean(0)
    vis_h = np.zeros(len(d["parent"]), bool)
    vis_h[np.array(d["tips"])[~plastid]] = True
    post_h, _, info_h = ll.fit_model(d, fams, nodes, vis=vis_h)
    is_pl = np.zeros(len(d["parent"]), float)
    is_pl[np.array(d["tips"])] = plastid
    cnt = np.zeros(len(d["parent"]))
    tot = np.zeros(len(d["parent"]))
    for v in d["order"]:
        if not d["children"][v]:
            cnt[v], tot[v] = is_pl[v], 1
        else:
            cnt[v] = sum(cnt[c] for c in d["children"][v])
            tot[v] = sum(tot[c] for c in d["children"][v])
    for v in nodes:
        if cnt[v] < 0.5 * tot[v]:
            post[v] = np.where(enriched, post_h[v], post[v])
    info["plastid_enriched_families"] = int(enriched.sum())
    print(f"plastid transfer: {int(enriched.sum())} enriched families, {int(plastid.sum())} plastid tips", flush=True)
    col = {f: j for j, f in enumerate(fams)}
    mfams, desc = module_families(set(fams))
    flist = sorted({f for fl in mfams.values() for f in fl})
    fidx = np.array([col[f] for f in flist])
    # per node: 3-bit code per module family = call (present/absent) x grade (A..D); packed as base64
    node_label = defaultdict(list)
    for t, v in taxon_node.items():
        node_label[v].append(t)
    depth = d["depth"]
    ntips = np.zeros(len(d["parent"]), int)
    for v in d["order"]:
        ntips[v] = 1 if not d["children"][v] else sum(ntips[c] for c in d["children"][v])
    out_nodes = {}
    for v in nodes:
        p = post[v].astype(float)
        conf = np.abs(p - 0.5) * 2
        g = np.select([conf >= 0.98, conf >= 0.9, conf >= 0.6], [0, 1, 2], 3)
        code = ((p >= 0.5).astype(int) << 2) | g
        pf = code[fidx].astype(np.uint8)
        packed = np.zeros((len(pf) + 1) // 2, np.uint8)       # two 3-bit codes per byte (4 bits each)
        packed[:len(pf[0::2])] = pf[0::2] << 4
        packed[:len(pf[1::2])] |= pf[1::2]
        mods = {}
        for key, fl in mfams.items():
            if not fl:
                continue
            j = np.array([col[f] for f in fl])
            mods[key] = [round(float(p[j].mean()), 3), int((p[j] >= 0.5).sum()), int(((p[j] >= 0.5) & (conf[j] >= 0.98)).sum())]
        labels = sorted(node_label.get(v, []), key=lambda t: -len(members[t]))
        if v == root:
            labels = ["LECA (진핵생물 공통조상)"] + labels
        out_nodes[str(v)] = {"labels": labels[:6], "depth": round(float(depth[v]), 4),
                             "n_tips": int(ntips[v]),
                             "expected_families": int(round(float(p.sum()))),
                             "confident_present": int(((p >= 0.5) & (conf >= 0.98)).sum()),
                             "modules": mods, "codes": base64.b64encode(packed.tobytes()).decode()}
    # parent of each kept node among kept nodes (for the lineage path)
    keep = set(nodes)
    kept_parent = {}
    for v in nodes:
        w = d["parent"][v]
        while w != -1 and w not in keep:
            w = d["parent"][w]
        kept_parent[str(v)] = int(w) if w != -1 else None
    # name index: every taxon or species name -> deepest kept node on its path
    index = {}
    for t, v in taxon_node.items():
        index[t] = v
    for u, L in tip_lin.items():
        w = int(u)
        while w not in keep and d["parent"][w] != -1:
            w = int(d["parent"][w])
        sp = tip_name[u]
        index.setdefault(sp, w)
        for t in L[:-1]:
            if t and t not in index:
                index[t] = w
    add_binomials(index)
    OUT.mkdir(parents=True, exist_ok=True)
    atlas = {"version": 1, "tree_tips": len(d["tips"]), "families_in_model": len(fams),
             "fit": {"m": info["m"], "plastid_enriched_families": info["plastid_enriched_families"]},
             "grades": grade_agreement(), "root": root,
             "modules": [{"key": k, "name": n, "families": mfams[k]} for k, n, _ in MODULES if mfams[k]],
             "family_order": flist, "descriptions": desc, "nodes": out_nodes, "parent": kept_parent,
             "index": index}
    with gzip.open(OUT / "atlas.json.gz", "wt") as f:
        json.dump(atlas, f, ensure_ascii=False)
    print(f"atlas: {len(out_nodes)} ancestors, {len(index)} names, {len(flist)} function families, "
          f"{(OUT / 'atlas.json.gz').stat().st_size / 1e6:.1f} MB", flush=True)


def add_binomials(index):
    """'Homo sapiens (Human)' and strain names are also found as 'Homo sapiens'."""
    from learning_loop import binomial
    for name, v in list(index.items()):
        bn = binomial(name)
        if len(bn.split()) == 2 and bn not in index:
            index[bn] = v
    return index


def lineage_lookup(name):
    """Lineage of a name not in the atlas, from the UniProt taxonomy service (needs network)."""
    import urllib.parse
    from uniprot_proteomes import REST, get
    from new_species import taxonomy
    q = urllib.parse.quote(f'scientific:"{name}"')
    hits = json.loads(get(f"{REST}/taxonomy/search?query={q}&format=json&size=1", tries=3)).get("results", [])
    if not hits:
        return None
    return taxonomy(hits[0]["taxonId"])["lineage"]


def path_to_root(atlas, v):
    out = []
    while v is not None:
        out.append(v)
        v = atlas["parent"].get(str(v))
    return out[::-1]


def decode(atlas, node):
    raw = np.frombuffer(base64.b64decode(atlas["nodes"][str(node)]["codes"]), np.uint8)
    codes = np.empty(len(raw) * 2, np.uint8)
    codes[0::2], codes[1::2] = raw >> 4, raw & 15
    return codes[:len(atlas["family_order"])]


def query(name):
    atlas = json.loads(gzip.open(OUT / "atlas.json.gz", "rt").read())
    v, via = atlas["index"].get(name), name
    if v is None:
        try:
            lin = lineage_lookup(name) or []
        except Exception as e:                       # no network: say so instead of failing
            print(f"분류 서비스에 연결하지 못했습니다({e}). 속이나 과 이름으로 다시 찾아보세요.")
            lin = []
        for t in lin[::-1]:
            if t in atlas["index"]:
                v, via = atlas["index"][t], t
                break
    if v is None:
        print(f"'{name}': 분류 정보를 찾지 못했습니다(학명으로 입력해 주세요).")
        return
    if via != name:
        print(f"'{name}'은 아틀라스에 직접 없어서, 분류상 가장 가까운 '{via}' 위치로 예측합니다.")
    for node in path_to_root(atlas, v):
        n = atlas["nodes"][str(node)]
        print(f"\n■ {' / '.join(n['labels'][:3]) or '(이름 없는 조상)'}  — 예상 유전자군 {n['expected_families']}개, "
              f"A등급으로 있음 {n['confident_present']}개")
        for m in atlas["modules"]:
            frac, n_present, n_a = n["modules"][m["key"]]
            bar = "█" * int(round(frac * 10)) + "·" * (10 - int(round(frac * 10)))
            print(f"   {m['name']:<14} {bar} {n_present}/{len(m['families'])} (A {n_a})")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("step", choices=["build", "query"])
    ap.add_argument("name", nargs="?")
    a = ap.parse_args()
    if a.step == "build":
        build()
    else:
        query(a.name)


if __name__ == "__main__":
    main()
