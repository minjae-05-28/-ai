import random

from organelle_evo.context import CODE, cai, cai_weights, family_context, gff_cds, parse_cds_fasta


def _seq(rng, preferred, n=120):
    """Random CDS; with `preferred`, always the first synonymous codon (high CAI)."""
    syn = {}
    for c, a in CODE.items():
        if a != "*":
            syn.setdefault(a, []).append(c)
    aas = sorted(syn)
    return "".join(syn[a][0] if preferred else rng.choice(syn[a]) for a in (rng.choice(aas) for _ in range(n)))


def test_cai_ranks_reference_like_genes_higher():
    rng = random.Random(0)
    w = cai_weights([_seq(rng, True) for _ in range(20)])
    assert cai(_seq(rng, True), w) > 0.9 > cai(_seq(rng, False), w)


def test_family_context_end_to_end():
    rng = random.Random(1)
    cds, fams_of, gff = {}, {}, ["##gff-version 3"]
    pos = 1
    for i in range(80):
        pid = f"P{i}"
        ribo = i < 15
        cds[pid] = _seq(rng, ribo or i % 2 == 0)
        fams_of[pid] = {"Ribosomal_L1"} if ribo else ({"FamA", "FamB"} if i % 2 == 0 else {"FamC"})
        end = pos + len(cds[pid]) - 1
        gff.append(f"chr\tx\tCDS\t{pos}\t{end}\t.\t+\t0\tID=c{i};protein_id={pid}")
        pos = end + (10 if i % 2 == 0 else 500)
    fasta = "\n".join(f">lcl|x [protein_id={p}] [gbkey=CDS]\n{s}" for p, s in cds.items())
    assert parse_cds_fasta(fasta) == cds
    loc = gff_cds("\n".join(gff))
    out = family_context(fams_of, cds, loc, prokaryote=True)
    n, cz, nc, multi, partners, op, nb, exons = out["FamA"]
    assert n == nc == multi and partners == 1 and exons == n
    assert cz / nc > out["FamC"][1] / out["FamC"][2]  # preferred codons -> higher expression z
    assert op > 0 and out["FamC"][3] == 0
