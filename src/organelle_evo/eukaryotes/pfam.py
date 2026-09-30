"""Count Pfam domain families in a proteome with HMMER3 (pyhmmer).

A family's count in a species is the number of genes carrying at least one domain of
that family above the Pfam gathering threshold. Per-family sums of domain
hydrophobicity, TM helices and length are kept so features can be averaged across
species later.
"""

import re
from collections import defaultdict

import pyhmmer

from ..realdata.genes import gravy, tm_helices

_ALPHABET = pyhmmer.easel.Alphabet.amino()


def _s(x) -> str:
    return x.decode() if isinstance(x, bytes) else (x or "")


def load_hmms(path: str) -> list:
    with pyhmmer.plan7.HMMFile(path) as f:
        return list(f)


def hmm_metadata(hmms) -> dict[str, dict]:
    return {
        _s(h.name): {"accession": _s(h.accession), "description": _s(h.description), "length": h.M}
        for h in hmms
    }


def _digitize(proteins: dict[str, str]):
    block = pyhmmer.easel.DigitalSequenceBlock(_ALPHABET)
    for name, seq in proteins.items():
        clean = re.sub(r"[^ACDEFGHIKLMNPQRSTVWY]", "X", seq.upper().rstrip("*"))
        block.append(pyhmmer.easel.TextSequence(name=name.encode(), sequence=clean).digitize(_ALPHABET))
    return block


def family_profile(proteins: dict[str, str], hmms, *, cpus: int = 0, cutoffs: str | None = "gathering"):
    """family -> [n_genes, n_domains, sum_gravy, sum_tm_helices, sum_domain_length]."""
    seqs = _digitize(proteins)
    genes = defaultdict(set)
    stats = defaultdict(lambda: [0, 0.0, 0.0, 0])  # n_domains, gravy, tm, length
    options = {"bit_cutoffs": cutoffs} if cutoffs else {"E": 1e-5}
    for top in pyhmmer.hmmsearch(hmms, seqs, cpus=cpus, **options):
        fam = _s(top.query.name)
        for hit in top:
            if not hit.included:
                continue
            pid = _s(hit.name)
            for dom in hit.domains:
                if not dom.included:
                    continue
                seg = proteins[pid][dom.env_from - 1 : dom.env_to]
                s = stats[fam]
                s[0] += 1
                s[1] += gravy(seg)
                s[2] += tm_helices(seg)
                s[3] += len(seg)
                genes[fam].add(pid)
    return {f: [len(genes[f]), *stats[f]] for f in genes}
