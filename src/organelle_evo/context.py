"""Per-gene context features, summarised per Pfam family, for new gene-loss law features.

For one genome (proteins, coding sequences, GFF and the Pfam families each protein carries):

  expression    codon adaptation index (CAI, Sharp & Li 1987) against the species' ribosomal
                protein genes, z-scored within the species so genome-wide GC and codon bias
                cancel. Highly expressed genes are known to be lost less often.
  domain        multi-domain share and the number of distinct partner families a family
                shares proteins with (domain promiscuity, a proxy for interaction hubs).
  operon        (prokaryotes) share of members with a same-strand neighbour < 50 bp away,
                and the number of distinct families in the +/-2 same-strand neighbourhood.
  exons         (eukaryotes) mean number of CDS segments per gene.

Output per family: [n_genes, sum_cai_z, n_with_cai, n_multi_domain, n_partners,
n_operon, n_neighbour_families, sum_exons].
"""

import math
import re
from collections import defaultdict

CODE = {}
_b = "TCAG"
_aa = "FFLLSSSSYY**CC*WLLLLPPPPHHQQRRRRIIIMTTTTNNKKSSRRVVVVAAAADDEEGGGG"
for i, a in enumerate(_b):
    for j, b in enumerate(_b):
        for k, c in enumerate(_b):
            CODE[a + b + c] = _aa[16 * i + 4 * j + k]
SYN = defaultdict(list)
for cod, aa in CODE.items():
    SYN[aa].append(cod)
SKIP = {"M", "W", "*"}

COLUMNS = ["n_genes", "sum_cai_z", "n_with_cai", "n_multi_domain", "n_partners", "n_operon",
           "n_neighbour_families", "sum_exons"]


def codons(seq: str) -> list[str]:
    s = seq.upper()
    return [s[i:i + 3] for i in range(0, len(s) - len(s) % 3, 3) if s[i:i + 3] in CODE]


def cai_weights(ref_seqs: list[str]) -> dict[str, float]:
    count = defaultdict(float)
    for s in ref_seqs:
        for c in codons(s):
            count[c] += 1
    w = {}
    for aa, cods in SYN.items():
        if aa in SKIP or len(cods) < 2:
            continue
        top = max(count[c] + 0.5 for c in cods)
        for c in cods:
            w[c] = (count[c] + 0.5) / top
    return w


def cai(seq: str, w: dict[str, float]) -> float | None:
    logs = [math.log(w[c]) for c in codons(seq) if c in w]
    return math.exp(sum(logs) / len(logs)) if len(logs) >= 30 else None


def parse_cds_fasta(text: str) -> dict[str, str]:
    """protein_id -> coding sequence, from an NCBI Datasets cds_from_genomic.fna."""
    out, pid, buf = {}, None, []
    for line in text.splitlines():
        if line.startswith(">"):
            if pid:
                out[pid] = "".join(buf)
            m = re.search(r"\[protein_id=([^\]]+)\]", line)
            pid, buf = (m.group(1) if m else None), []
        elif pid:
            buf.append(line.strip())
    if pid:
        out[pid] = "".join(buf)
    return out


def gff_cds(gff_text: str) -> dict[str, dict]:
    """protein_id -> {seqid, start, end, strand, exons}."""
    out = {}
    for line in gff_text.splitlines():
        if line.startswith("#"):
            continue
        c = line.split("\t")
        if len(c) < 9 or c[2] != "CDS":
            continue
        m = re.search(r"protein_id=([^;]+)", c[8])
        if not m:
            continue
        pid, s, e = m.group(1), int(c[3]), int(c[4])
        r = out.get(pid)
        if r is None:
            out[pid] = {"seqid": c[0], "start": s, "end": e, "strand": c[6], "exons": 1}
        else:
            r["start"], r["end"], r["exons"] = min(r["start"], s), max(r["end"], e), r["exons"] + 1
    return out


def family_context(fams_of: dict[str, set], cds: dict[str, str], loc: dict[str, dict], prokaryote: bool) -> dict:
    """fams_of: protein_id -> Pfam families carried (proteins without hits may be absent)."""
    ref = [cds[p] for p, f in fams_of.items() if p in cds and any(x.startswith("Ribosomal_") for x in f)]
    z = {}
    if len(ref) >= 10:
        w = cai_weights(ref)
        vals = {p: cai(s, w) for p, s in cds.items()}
        vals = {p: v for p, v in vals.items() if v is not None}
        if len(vals) > 50:
            mu = sum(vals.values()) / len(vals)
            sd = math.sqrt(sum((v - mu) ** 2 for v in vals.values()) / len(vals)) or 1.0
            z = {p: (v - mu) / sd for p, v in vals.items()}

    operon, neigh = {}, {}
    if prokaryote and loc:
        by_seq = defaultdict(list)
        for p, r in loc.items():
            by_seq[r["seqid"]].append((r["start"], r["end"], r["strand"], p))
        for genes in by_seq.values():
            genes.sort()
            for i, (s, e, st, p) in enumerate(genes):
                close = False
                nb = set()
                for j in range(max(0, i - 2), min(len(genes), i + 3)):
                    if j == i or genes[j][2] != st:
                        continue
                    gap = genes[j][0] - e if j > i else s - genes[j][1]
                    if abs(j - i) == 1 and gap < 50:
                        close = True
                    if gap < 300:
                        nb |= fams_of.get(genes[j][3], set())
                operon[p], neigh[p] = close, nb

    acc = defaultdict(lambda: {"genes": 0, "cz": 0.0, "nc": 0, "multi": 0, "partners": set(), "op": 0,
                               "nb": set(), "exons": 0})
    for p, fams in fams_of.items():
        for f in fams:
            a = acc[f]
            a["genes"] += 1
            if p in z:
                a["cz"] += z[p]
                a["nc"] += 1
            if len(fams) > 1:
                a["multi"] += 1
                a["partners"] |= fams - {f}
            if operon.get(p):
                a["op"] += 1
            a["nb"] |= neigh.get(p, set()) - {f}
            a["exons"] += loc.get(p, {}).get("exons", 1)
    return {f: [a["genes"], round(a["cz"], 4), a["nc"], a["multi"], len(a["partners"]), a["op"], len(a["nb"]), a["exons"]]
            for f, a in acc.items()}
