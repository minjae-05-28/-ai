"""Measured knockout phenotypes and protein abundance, mapped to Pfam families.

    python scripts/collect_phenotypes.py --source fitness   # Fitness Browser (transposon knockouts, ~50 bacteria)
    python scripts/collect_phenotypes.py --source deg       # Database of Essential Genes (bacteria, archaea, eukaryotes)
    python scripts/collect_phenotypes.py --source yeast     # S. cerevisiae deletion viability (SGD)
    python scripts/collect_phenotypes.py --source pombe     # S. pombe deletion viability (PomBase)
    python scripts/collect_phenotypes.py --source paxdb     # measured protein abundance (PaxDb) for catalogue species

Runs on GitHub Actions (.github/workflows/phenotypes.yml): the sources are not reachable
from the development sandbox. Proteins are assigned to Pfam families with HMMER (gathering
thresholds) over the families that occur in the project's profiles. Output in
data/phenotypes/<source>/.

Knockout data say what happens when a gene is removed in a living cell: whether the cell
dies (essential), and how much growth it costs in each condition (fitness, log2 ratio).
"""

import argparse
import csv
import gzip
import io
import json
import os
import re
import sqlite3
import sys
import urllib.request
import zipfile
from collections import defaultdict
from pathlib import Path

OUT = Path("data/phenotypes")
UA = {"User-Agent": "organelle-evo/1.0 (research; github.com/minjae-05-28/-ai)"}
csv.field_size_limit(sys.maxsize)


def get(url, timeout=600):
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read()


def download(url, dest):
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=600) as r, open(dest, "wb") as f:
        size = int(r.headers.get("Content-Length") or 0)
        print(f"downloading {url} ({size / 1e9:.2f} GB)", flush=True)
        done = 0
        while chunk := r.read(1 << 24):
            f.write(chunk)
            done += len(chunk)
            if done % (1 << 30) < (1 << 24):
                print(f"  {done / 1e9:.1f} GB", flush=True)
    return dest


def fasta(text):
    seqs, name, buf = {}, None, []
    for line in text.splitlines():
        if line.startswith(">"):
            if name:
                seqs[name] = "".join(buf)
            name, buf = line[1:].split()[0], []
        elif name:
            buf.append(line.strip())
    if name:
        seqs[name] = "".join(buf)
    return seqs


def project_families():
    fams = set(Path("data/eukaryotes/pfam_subset.txt").read_text().split())
    for f in Path("data/prokaryotes").glob("*.json"):
        fams |= set(json.loads(f.read_text())["families"])
    return fams


_HMMS = None


def families_of(proteins, pfam):
    """protein id -> sorted Pfam families (gathering thresholds)."""
    global _HMMS
    import pyhmmer

    from organelle_evo.eukaryotes.pfam import _digitize, _s, load_hmms

    if _HMMS is None:
        keep = project_families()
        _HMMS = [h for h in load_hmms(pfam) if _s(h.name) in keep]
        print(f"{len(_HMMS)} Pfam HMMs", flush=True)
    proteins = {k: v for k, v in proteins.items() if v and len(v) >= 30}
    out = defaultdict(set)
    for top in pyhmmer.hmmsearch(_HMMS, _digitize(proteins), cpus=0, bit_cutoffs="gathering"):
        fam = _s(top.query.name)
        for hit in top:
            if hit.included:
                out[_s(hit.name)].add(fam)
    return {k: sorted(v) for k, v in out.items()}


# --- Fitness Browser -------------------------------------------------------------------

RICH = re.compile(r"\b(lb|rich|tsb|yeast extract|ypd|2xyt|r2a|marine broth|bhi)\b", re.I)


def fitness(pfam, tmp):
    db = download("https://fit.genomics.lbl.gov/cgi_data/feba.db", Path(tmp) / "feba.db")
    con = sqlite3.connect(db)
    cur = con.cursor()
    print("tables:", [r[0] for r in cur.execute("select name from sqlite_master where type='table'")])
    orgs = {r[0]: f"{r[1]} {r[2]} {r[3] or ''}".strip() for r in cur.execute("select orgId, genus, species, strain from Organism")}
    seqs = fasta(get("https://fit.genomics.lbl.gov/cgi_data/aaseqs").decode())
    by_org = defaultdict(dict)
    for k, v in seqs.items():
        org, locus = k.split(":", 1)
        by_org[org][locus] = v
    (OUT / "fitness").mkdir(parents=True, exist_ok=True)
    only = set(filter(None, os.environ.get("FB_ORGS", "").split(",")))  # set by --orgs
    for org, name in sorted(orgs.items()):
        if only and org not in only:
            continue
        exps = {r[0]: (r[1] or "", r[2] or "", r[3] or "") for r in cur.execute(
            "select expName, expGroup, condition_1, media from Experiment where orgId=?", (org,))}
        if not exps:
            continue
        fit = defaultdict(dict)
        for locus, exp, f in cur.execute("select locusId, expName, fit from GeneFitness where orgId=?", (org,)):
            fit[locus][exp] = f
        names = {r[0]: (r[1] or "", r[2] or "") for r in cur.execute(
            "select locusId, sysName, gene from Gene where orgId=? and type=1", (org,))}
        genes = list(names)
        prots = {g: by_org[org].get(g) for g in genes if by_org[org].get(g)}
        fams = families_of(prots, pfam)
        rich = {e for e, (grp, cond, media) in exps.items() if RICH.search(media) and grp.lower() not in ("carbon source", "nitrogen source")}
        minimal = {e for e, (grp, _, _) in exps.items() if grp.lower() in ("carbon source", "nitrogen source")}
        rows = {}
        for g, p in prots.items():
            f = fit.get(g, {})
            vals = list(f.values())
            r = [f[e] for e in f if e in rich]
            m = [f[e] for e in f if e in minimal]
            essential = int(not vals and len(p) >= 100)  # no mutants recovered: likely essential
            rows[g] = [fams.get(g, []), essential, len(vals),
                       round(sum(vals) / len(vals), 3) if vals else None, round(min(vals), 3) if vals else None,
                       round(sum(r) / len(r), 3) if r else None, round(min(m), 3) if m else None,
                       names[g][0], names[g][1]]
        (OUT / "fitness" / f"{org}.json").write_text(json.dumps(
            {"org": org, "organism": name, "n_experiments": len(exps), "n_rich": len(rich), "n_minimal": len(minimal),
             "columns": ["families", "likely_essential", "n_fitness", "mean_fit", "min_fit", "rich_mean_fit", "minimal_min_fit",
                         "sys_name", "gene"],
             "genes": rows}, separators=(",", ":")))
        print(f"{org:24s} {name[:40]:40s} {len(prots)} genes, {sum(r[1] for r in rows.values())} likely essential, "
              f"{len(exps)} experiments ({len(rich)} rich, {len(minimal)} minimal)", flush=True)


# --- DEG -------------------------------------------------------------------------------

def deg(pfam, tmp):
    base = "http://tubic.org/deg/public/download/"
    (OUT / "deg").mkdir(parents=True, exist_ok=True)
    for domain, aa, ann in (("bacteria", "DEG10.aa.gz", "deg_bacteria.csv.zip"),
                            ("eukaryotes", "DEG20.aa.gz", "deg_eukaryotes.csv.zip"),
                            ("archaea", "DEG30.aa.gz", "deg_archaea.csv.zip")):
        seqs = fasta(gzip.decompress(get(base + aa)).decode("utf-8", "replace"))
        z = zipfile.ZipFile(io.BytesIO(get(base + ann)))
        text = z.read(z.namelist()[0]).decode("utf-8", "replace")
        rows = list(csv.reader(io.StringIO(text), delimiter=";" if text.count(";") > text.count(",") else ","))
        # One row per study: organism name first, study id (DEGnnnn) near the end. Protein ids
        # in the FASTA start with the study id (e.g. DEG10010001 -> DEG1001).
        study_org = {}
        for r in rows:
            sid = next((c for c in r if re.fullmatch(r"DEG\d{4}", c.strip())), None)
            if sid and r and r[0].strip():
                study_org[sid] = r[0].strip()
        org_of = {k: study_org.get(m.group(1), "unknown") for k in seqs if (m := re.match(r"(DEG\d{4})", k))}
        print(f"{domain}: {len(seqs)} essential proteins, {len(study_org)} studies, {len(set(org_of.values()))} organisms")
        per_org = defaultdict(dict)
        for k, v in seqs.items():
            per_org[org_of.get(k, "unknown")][k] = v
        res = {}
        for org, prots in sorted(per_org.items()):
            if org == "unknown" or len(prots) > 8000:
                print(f"  skip {org}: {len(prots)} entries")
                continue
            fams = families_of(prots, pfam)
            cnt = defaultdict(int)
            for fs in fams.values():
                for f in fs:
                    cnt[f] += 1
            res[org] = {"n_essential": len(prots), "families": dict(cnt)}
            print(f"  {org[:50]:50s} {len(prots)} essential, {len(cnt)} families", flush=True)
        (OUT / "deg" / f"{domain}.json").write_text(json.dumps(res, separators=(",", ":")))


# --- Yeasts ----------------------------------------------------------------------------

def yeast(pfam, tmp):
    rows = get("https://downloads.yeastgenome.org/curation/literature/phenotype_data.tab").decode("utf-8", "replace")
    viable, inviable = set(), set()
    for line in rows.splitlines():
        c = line.split("\t")
        if len(c) > 9 and c[6] == "null":
            if c[9] == "inviable":
                inviable.add(c[0])
            elif c[9] == "viable":
                viable.add(c[0])
    seqs = fasta(gzip.decompress(get("https://downloads.yeastgenome.org/sequence/S288C_reference/orf_protein/orf_trans_all.fasta.gz")).decode())
    seqs = {k: v.rstrip("*") for k, v in seqs.items()}
    fams = families_of(seqs, pfam)
    genes = {g: [fams.get(g, []), int(g in inviable), int(g in viable and g not in inviable)] for g in seqs if g in viable | inviable}
    (OUT / "yeast").mkdir(parents=True, exist_ok=True)
    (OUT / "yeast" / "Saccharomyces_cerevisiae.json").write_text(json.dumps(
        {"organism": "Saccharomyces cerevisiae", "columns": ["families", "inviable", "viable"], "genes": genes}, separators=(",", ":")))
    print(f"S. cerevisiae: {len(genes)} genes with deletion viability, {sum(v[1] for v in genes.values())} inviable")


def pombe(pfam, tmp):
    base = "https://www.pombase.org/latest_release/"
    phaf = get(base + "phenotypes_and_genotypes/pombase_single_locus_haploid_phenotype_annotation.phaf.tsv").decode()
    viable, inviable = set(), set()
    for line in phaf.splitlines():
        c = line.split("\t")
        if len(c) > 11 and c[11] == "deletion":
            if c[2] in ("FYPO:0002061", "FYPO:0000049"):  # inviable vegetative cell population / inviable cell
                inviable.add(c[1])
            elif c[2] == "FYPO:0002060":  # viable vegetative cell population
                viable.add(c[1])
    # find the peptide FASTA in the release listing
    listing = get(base + "genome_sequence_and_features/fasta_format/").decode()
    links = re.findall(r'href="([^"]+)"', listing)
    pep = next((l for l in links if "pep" in l.lower()), None)
    if pep is None:
        sub = [l for l in links if l.endswith("/") and not l.startswith(("/", "?", ".."))]
        for d in sub:
            inner = re.findall(r'href="([^"]+)"', get(base + "genome_sequence_and_features/fasta_format/" + d).decode())
            hit = next((l for l in inner if "pep" in l.lower()), None)
            if hit:
                pep = d + hit
                break
    url = pep if pep.startswith("http") else base + "genome_sequence_and_features/fasta_format/" + pep
    raw = get(url)
    raw = gzip.decompress(raw) if raw[:2] == b"\x1f\x8b" else raw
    seqs = {k.split(":")[0]: v.rstrip("*") for k, v in fasta(raw.decode()).items()}
    fams = families_of(seqs, pfam)
    genes = {g: [fams.get(g, []), int(g in inviable), int(g in viable and g not in inviable)] for g in seqs if g in viable | inviable}
    (OUT / "pombe").mkdir(parents=True, exist_ok=True)
    (OUT / "pombe" / "Schizosaccharomyces_pombe.json").write_text(json.dumps(
        {"organism": "Schizosaccharomyces pombe", "columns": ["families", "inviable", "viable"], "genes": genes}, separators=(",", ":")))
    print(f"S. pombe: {len(genes)} genes with deletion viability, {sum(v[1] for v in genes.values())} inviable ({url})")


# --- PaxDb -----------------------------------------------------------------------------

def taxid(name):
    from organelle_evo.eukaryotes.proteomes import API, _get

    import urllib.parse

    for q in (name, " ".join(name.split()[:2])):
        try:
            rep = json.loads(_get(f"{API}/taxonomy/taxon/{urllib.parse.quote(q)}")).get("taxonomy_nodes", [])
        except Exception:  # noqa: BLE001
            continue
        for n in rep:
            t = n.get("taxonomy", {})
            if t.get("tax_id"):
                return int(t["tax_id"])
    return None


def paxdb(pfam, tmp):
    from organelle_evo.eukaryotes import catalog as euk
    from organelle_evo.prokaryotes import catalog as pro

    listing = get("https://pax-db.org/downloads/latest/datasets/").decode()
    have = set(re.findall(r'href="(\d+)\.zip"', listing))
    seq_listing = get("https://pax-db.org/downloads/latest/paxdb-protein-sequences-v6.1/").decode()
    pax_seqs = set(re.findall(r'fasta\.v12\.0\.(\d+)\.fa', seq_listing))
    (OUT / "paxdb").mkdir(parents=True, exist_ok=True)
    names = sorted(set(euk.SPECIES) | set(pro.SPECIES) | {"Escherichia coli", "Homo sapiens"})
    for name in names:
        t = taxid(name)
        if t is None or str(t) not in have:
            continue
        z = zipfile.ZipFile(io.BytesIO(get(f"https://pax-db.org/downloads/latest/datasets/{t}.zip")))
        files = [n for n in z.namelist() if n.endswith(".txt")]
        pick = next((n for n in files if "WHOLE_ORGANISM" in n.upper() and "INTEGRATED" in n.upper()), None) or \
            next((n for n in files if "INTEGRATED" in n.upper()), None) or (files[0] if files else None)
        if pick is None:
            continue
        ab = {}
        for line in z.read(pick).decode("utf-8", "replace").splitlines():
            if line.startswith("#") or not line.strip():
                continue
            c = line.split("\t")
            try:
                ab[c[-2] if len(c) > 2 else c[0]] = float(c[-1])
            except ValueError:
                continue
        if str(t) in pax_seqs:
            raw = get(f"https://pax-db.org/downloads/latest/paxdb-protein-sequences-v6.1/fasta.v12.0.{t}.fa")
        else:
            raw = gzip.decompress(get(f"https://stringdb-downloads.org/download/protein.sequences.v12.0/{t}.protein.sequences.v12.0.fa.gz"))
        seqs = fasta(raw.decode())
        seqs = {k: v for k, v in seqs.items() if k in ab}
        fams = families_of(seqs, pfam)
        per_fam = defaultdict(list)
        for p, fs in fams.items():
            for f in fs:
                per_fam[f].append(ab[p])
        (OUT / "paxdb" / f"{re.sub(r'[^A-Za-z0-9]+', '_', name)}.json").write_text(json.dumps(
            {"species": name, "taxid": t, "dataset": pick, "n_proteins": len(ab),
             "families": {f: sorted(v) for f, v in per_fam.items()}}, separators=(",", ":")))
        print(f"{name}: taxid {t}, {pick}, {len(ab)} proteins, {len(per_fam)} families", flush=True)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--source", required=True, choices=["fitness", "deg", "yeast", "pombe", "paxdb"])
    ap.add_argument("--pfam", default="pfam/Pfam-A.hmm")
    ap.add_argument("--tmp", default="/tmp")
    ap.add_argument("--orgs", default="", help="Fitness Browser orgIds to export (comma-separated; default all)")
    args = ap.parse_args()
    os.environ["FB_ORGS"] = args.orgs
    globals()[args.source](args.pfam, args.tmp)


if __name__ == "__main__":
    main()
