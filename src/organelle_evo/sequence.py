"""Proteome-level sequence statistics: amino-acid composition and what it is known to track.

Each statistic is a published signal of adaptation:
  ivywrel        share of I, V, Y, W, R, E, L; rises with optimal growth temperature
                 (Zeldovich, Berezovsky & Shakhnovich 2007)
  cvp            charged minus polar (D+E+K+R) - (N+Q+S+T); also rises with temperature
                 (Suhre & Claverie 2003)
  acidic_excess  (D+E) - (K+R); high in 'salt-in' halophiles
  median_pi      median isoelectric point; halophile proteomes are acidic
  n_side         nitrogen atoms per residue in side chains; low in N-limited oligotrophs
                 (Grzymski & Dussaq 2012)
  c_side         carbon atoms per residue in side chains
  fymink, garp   residues encoded by AT-rich (F, Y, M, I, N, K) and GC-rich (G, A, R, P)
                 codons; FYMINK rises with AT bias in reduced genomes
"""

import numpy as np

AA = "ACDEFGHIKLMNPQRSTVWY"
SIDE_N = {"R": 3, "H": 2, "K": 1, "N": 1, "Q": 1, "W": 1}
SIDE_C = {"A": 1, "R": 4, "N": 2, "D": 2, "C": 1, "E": 3, "Q": 3, "G": 0, "H": 4, "I": 4, "L": 4, "K": 4,
          "M": 3, "F": 7, "P": 3, "S": 1, "T": 2, "W": 9, "Y": 7, "V": 3}
KD = {"A": 1.8, "R": -4.5, "N": -3.5, "D": -3.5, "C": 2.5, "Q": -3.5, "E": -3.5, "G": -0.4, "H": -3.2, "I": 4.5,
      "L": 3.8, "K": -3.9, "M": 1.9, "F": 2.8, "P": -1.6, "S": -0.8, "T": -0.7, "W": -0.9, "Y": -1.3, "V": 4.2}
# pKa values (EMBOSS set) for the isoelectric point
PKA = {"Nterm": 8.6, "Cterm": 3.6, "C": 8.5, "D": 3.9, "E": 4.1, "H": 6.5, "K": 10.8, "R": 12.5, "Y": 10.1}


def isoelectric_point(seq: str) -> float:
    n = {k: seq.count(k) for k in "CDEHKRY"}
    lo, hi = 0.0, 14.0
    for _ in range(40):
        ph = (lo + hi) / 2
        pos = 1 / (1 + 10 ** (ph - PKA["Nterm"])) + sum(n[k] / (1 + 10 ** (ph - PKA[k])) for k in "HKR")
        neg = 1 / (1 + 10 ** (PKA["Cterm"] - ph)) + sum(n[k] / (1 + 10 ** (PKA[k] - ph)) for k in "CDEY")
        lo, hi = (ph, hi) if pos > neg else (lo, ph)
    return (lo + hi) / 2


def proteome_stats(proteins) -> dict:
    """proteins: iterable of amino-acid strings (one per gene)."""
    seqs = [s.upper().replace("*", "") for s in proteins if s]
    seqs = [s for s in seqs if len(s) >= 30]
    allaa = "".join(seqs)
    counts = np.array([allaa.count(a) for a in AA], dtype=float)
    total = counts.sum()
    f = dict(zip(AA, counts / total))
    pis = np.array([isoelectric_point(s) for s in seqs])
    stats = {
        "n_proteins": len(seqs),
        "residues": int(total),
        "mean_length": float(total / len(seqs)),
        "composition": {a: round(float(v), 6) for a, v in f.items()},
        "ivywrel": sum(f[a] for a in "IVYWREL"),
        "cvp": (f["D"] + f["E"] + f["K"] + f["R"]) - (f["N"] + f["Q"] + f["S"] + f["T"]),
        "acidic_excess": (f["D"] + f["E"]) - (f["K"] + f["R"]),
        "median_pi": float(np.median(pis)),
        "share_pi_below_5": float((pis < 5).mean()),
        "n_side": sum(f[a] * SIDE_N.get(a, 0) for a in AA),
        "c_side": sum(f[a] * SIDE_C[a] for a in AA),
        "gravy": sum(f[a] * KD[a] for a in AA),
        "fymink": sum(f[a] for a in "FYMINK"),
        "garp": sum(f[a] for a in "GARP"),
        "aromatic": f["F"] + f["W"] + f["Y"],
        "cysteine": f["C"],
    }
    return {k: (round(v, 6) if isinstance(v, float) else v) for k, v in stats.items()}


SCALARS = ("ivywrel", "cvp", "acidic_excess", "median_pi", "share_pi_below_5", "n_side", "c_side", "gravy",
           "fymink", "garp", "aromatic", "cysteine", "mean_length")
