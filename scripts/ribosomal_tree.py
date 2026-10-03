"""Sequence-based phylogenies from ribosomal proteins, to replace the taxonomy stand-in.

    python scripts/ribosomal_tree.py --list-missing
    python scripts/ribosomal_tree.py --entry "prokaryotes/Thermus thermophilus" --pfam pfam/Pfam-A.hmm
    python scripts/ribosomal_tree.py --build            # needs mafft and FastTree on PATH
    python scripts/ribosomal_tree.py --build --only amoeba   # one set, leaving the others alone

Markers: for every species, the best hit of each ribosomal-protein Pfam family
(data/markers/<set>/<slug>.json). Three trees, one per analysis set:
  prokaryotes   universal (non-'e') families, bacteria + archaea
  eukaryotes    eukaryote/archaea-specific ('e') families, so mitochondrial and plastid
                ribosomal paralogs (bacterial-type) are never picked up
  symbionts     insect endosymbionts + E. coli, from the GenBank records in data/raw
Families present in >= 80% of a set are aligned (mafft --auto), concatenated (missing =
gaps) and given to FastTree (-lg -gamma). Output: results/phylo_tree/<set>.nwk with
species names as leaves.
"""

import argparse
import json
import re
import shutil
import subprocess
from pathlib import Path

from organelle_evo.eukaryotes import catalog as euk
from organelle_evo.prokaryotes import catalog as pro

OUT = Path("data/markers")
TREES = Path("results/phylo_tree")
RAW = Path("data/raw/insect_endosymbiont")
MIN_COVERAGE = 0.8


def entries():
    out = [f"prokaryotes/{s}" for s in pro.SPECIES]
    out += [f"eukaryotes/{s}" for s in euk.SPECIES]
    out += [f"symbionts/{f.stem}" for f in sorted(Path("data/composition/endosymbiosis/insect_endosymbiont").glob("*.json"))]
    return out


def path(entry):
    cat, sp = entry.split("/", 1)
    name = sp if cat == "symbionts" else (pro if cat == "prokaryotes" else euk).slug(sp)
    return OUT / cat / f"{name}.json"


def wanted(fam, cat):
    if not fam.startswith("Ribosomal_") or re.search(r"\d+m(_|-|$)", fam):
        return False  # mitochondrial-type families (bL9m, uL24m-like, uS5m)
    if fam == "Ribosomal_S30AE":
        return False  # ribosome hibernation factor, not a ribosomal protein
    euk_specific = bool(re.search(r"(e|ae|AE|Ae)(_[NC])?$", fam))
    return euk_specific if cat == "eukaryotes" else not euk_specific


def symbiont_proteins(stem):
    from Bio import SeqIO

    comp = json.loads(Path(f"data/composition/endosymbiosis/insect_endosymbiont/{stem}.json").read_text())
    prots = {}
    for rec in SeqIO.parse(RAW / f"{stem}.gb", "genbank"):
        for f in rec.features:
            if f.type == "CDS" and "translation" in f.qualifiers:
                pid = f.qualifiers.get("protein_id", f.qualifiers.get("locus_tag", [f"p{len(prots)}"]))[0]
                prots[pid] = f.qualifiers["translation"][0]
    return comp["species"], prots


def collect(entry, pfam):
    import pyhmmer

    from organelle_evo.eukaryotes.pfam import _digitize, _s, load_hmms

    cat, sp = entry.split("/", 1)
    if cat == "symbionts":
        species, proteins = symbiont_proteins(sp)
    else:
        from organelle_evo.eukaryotes.proteomes import fetch_proteome

        species = sp
        _, proteins = fetch_proteome(sp)
    hmms = [h for h in load_hmms(pfam) if wanted(_s(h.name), cat)]
    best = {}
    for top in pyhmmer.hmmsearch(hmms, _digitize(proteins), bit_cutoffs="gathering"):
        fam = _s(top.query.name)
        hits = [h for h in top if h.included]
        if hits:
            h = max(hits, key=lambda h: h.score)
            best[fam] = proteins[_s(h.name)].rstrip("*")
    p = path(entry)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps({"species": species, "markers": best}))
    print(f"{entry}: {len(best)} ribosomal markers")


def build(n_boot=0, only=None):
    import tempfile

    TREES.mkdir(parents=True, exist_ok=True)
    for cat_dir in sorted(OUT.iterdir()):
        if only and cat_dir.name not in only:
            continue  # so a new set does not rebuild (and overwrite) the existing trees
        data = {json.loads(f.read_text())["species"]: json.loads(f.read_text())["markers"] for f in cat_dir.glob("*.json")}
        if len(data) < 4:
            continue
        species = sorted(data)
        ids = {s: f"t{i}" for i, s in enumerate(species)}
        fams = sorted({f for m in data.values() for f in m})
        fams = [f for f in fams if sum(f in data[s] for s in species) >= MIN_COVERAGE * len(species)]
        concat = {s: [] for s in species}
        with tempfile.TemporaryDirectory() as tmp:
            for fam in fams:
                fa = Path(tmp) / f"{fam}.fa"
                fa.write_text("".join(f">{ids[s]}\n{data[s][fam]}\n" for s in species if fam in data[s]))
                aln = subprocess.run(["mafft", "--auto", "--quiet", str(fa)], capture_output=True, text=True, check=True).stdout
                seqs, cur = {}, None
                for line in aln.splitlines():
                    if line.startswith(">"):
                        cur = line[1:].strip()
                        seqs[cur] = []
                    else:
                        seqs[cur].append(line.strip())
                seqs = {k: "".join(v) for k, v in seqs.items()}
                width = len(next(iter(seqs.values())))
                for s in species:
                    concat[s].append(seqs.get(ids[s], "-" * width))
            sup = Path(tmp) / "concat.fa"
            sup.write_text("".join(f">{ids[s]}\n{''.join(concat[s])}\n" for s in species))
            ft = shutil.which("FastTreeMP") or shutil.which("FastTree") or shutil.which("fasttree")
            nwk = subprocess.run([ft, "-lg", "-gamma", "-quiet", str(sup)], capture_output=True, text=True, check=True).stdout
            boots = []
            if n_boot:
                # Nonparametric bootstrap: resample alignment columns, one tree per replicate
                import random

                rng = random.Random(0)
                rows = {s: "".join(concat[s]) for s in species}
                width = len(rows[species[0]])
                for b in range(n_boot):
                    cols = [rng.randrange(width) for _ in range(width)]
                    rep = Path(tmp) / f"boot{b}.fa"
                    rep.write_text("".join(f">{ids[s]}\n{''.join(rows[s][c] for c in cols)}\n" for s in species))
                    boots.append(subprocess.run([ft, "-lg", "-gamma", "-quiet", "-nosupport", str(rep)],
                                                capture_output=True, text=True, check=True).stdout.strip())
                    print(f"  {cat_dir.name} bootstrap {b + 1}/{n_boot}", flush=True)
        back = {v: k for k, v in ids.items()}
        rename = lambda t: re.sub(r"\b(t\d+)(?=[:,)])", lambda m: "'" + back[m.group(1)].replace("'", "") + "'", t)  # noqa: E731
        nwk = rename(nwk)
        (TREES / f"{cat_dir.name}.nwk").write_text(nwk)
        if boots:
            (TREES / f"{cat_dir.name}.boot.nwk").write_text("\n".join(rename(t) for t in boots) + "\n")
        (TREES / f"{cat_dir.name}.json").write_text(json.dumps({"species": len(species), "families": fams,
                                                                "alignment_length": len("".join(concat[species[0]]))}, indent=1))
        print(f"{cat_dir.name}: {len(species)} species, {len(fams)} families -> {TREES / cat_dir.name}.nwk")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--entry")
    ap.add_argument("--pfam", default="pfam/Pfam-A.hmm")
    ap.add_argument("--list-missing", action="store_true")
    ap.add_argument("--build", action="store_true")
    ap.add_argument("--bootstrap", type=int, default=0, help="bootstrap replicate trees per set")
    ap.add_argument("--only", help="comma-separated marker sets to build (default: all)")
    args = ap.parse_args()
    if args.list_missing:
        print(json.dumps([e for e in entries() if not path(e).exists()]))
    elif args.build:
        build(args.bootstrap, args.only.split(",") if args.only else None)
    else:
        collect(args.entry, args.pfam)


if __name__ == "__main__":
    main()
