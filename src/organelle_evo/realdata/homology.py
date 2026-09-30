"""Name genes by protein homology instead of annotation text.

Annotations are inconsistent: the same gene is unnamed in one record, named
differently in another, or only described in free text. Gene-name matching then
reports false losses. Here every CDS is compared to a named reference proteome with
phmmer (HMMER3), and a CDS takes a reference gene's name only if the two are
reciprocal best hits, cover most of each other, and pass an E-value cutoff.
"""

import re

import pyhmmer

from .dataset import GenomeRecord

_ALPHABET = pyhmmer.easel.Alphabet.amino()


def _digitize(seqs: dict[str, str]) -> pyhmmer.easel.DigitalSequenceBlock:
    block = pyhmmer.easel.DigitalSequenceBlock(_ALPHABET)
    for name, seq in seqs.items():
        clean = re.sub(r"[^ACDEFGHIKLMNPQRSTVWY]", "X", seq.upper().rstrip("*"))
        text = pyhmmer.easel.TextSequence(name=name.encode(), sequence=clean)
        block.append(text.digitize(_ALPHABET))
    return block


def _name(x) -> str:
    return x.decode() if isinstance(x, bytes) else x


def best_hits(
    queries: dict[str, str], targets: dict[str, str], *, evalue: float = 1e-10, min_cov: float = 0.5
) -> dict[str, tuple[str, float]]:
    """query id -> (best target id, bit score), among hits covering >= min_cov of both."""
    if not queries or not targets:
        return {}
    target_block = _digitize(targets)
    out = {}
    for top in pyhmmer.hmmer.phmmer(_digitize(queries), target_block, cpus=0, E=evalue):
        qname = _name(top.query.name)
        for hit in top:
            if not hit.included:
                continue
            aln = hit.best_domain.alignment
            q_cov = (aln.hmm_to - aln.hmm_from + 1) / aln.hmm_length
            t_cov = (aln.target_to - aln.target_from + 1) / aln.target_length
            if min(q_cov, t_cov) >= min_cov:
                out[qname] = (_name(hit.name), hit.score)
                break  # hits are sorted best first
    return out


def reciprocal_best_hits(
    lineage: dict[str, str], reference: dict[str, str], **kwargs
) -> dict[str, str]:
    """lineage CDS id -> reference id, for pairs that are each other's best hit."""
    forward = best_hits(lineage, reference, **kwargs)
    hit_refs = {r for r, _ in forward.values()}
    backward = best_hits({r: reference[r] for r in hit_refs}, lineage, **kwargs)
    return {q: r for q, (r, _) in forward.items() if backward.get(r, (None,))[0] == q}


def name_by_homology(
    records: list[GenomeRecord],
    reference: dict[str, tuple[str, str]],
    *,
    cache: dict | None = None,
    **kwargs,
) -> tuple[list[GenomeRecord], dict[str, int]]:
    """Assign reference gene symbols to CDSs by reciprocal best hit.

    `reference` maps an id to (symbol, protein); several ids may share a symbol (e.g.
    the same gene from different species). A CDS is searched if it is unnamed or its
    name is not one of the reference's (e.g. a different naming convention).
    `cache` (accession -> {cds id: symbol}) is read and filled to skip repeat searches.
    Returns updated records and, per lineage, how many genes were newly added.
    """
    ref_seqs = {rid: prot for rid, (_, prot) in reference.items()}
    ref_symbols = {sym for sym, _ in reference.values()}
    updated, added = [], {}
    for rec in records:
        if cache is not None and rec.accession in cache:
            extra = cache[rec.accession]
        else:
            query = {
                cid: p for cid, p in rec.cds.items() if rec.cds_symbol.get(cid) not in ref_symbols
            }
            pairs = reciprocal_best_hits(query, ref_seqs, **kwargs)
            extra = {cid: reference[rid][0] for cid, rid in pairs.items()}
            if cache is not None:
                cache[rec.accession] = extra
        new = rec.with_symbols(extra)
        added[rec.organism] = len(new.proteins) - len(rec.proteins)
        updated.append(new)
    return updated, added


def reference_from_records(records: list[GenomeRecord]) -> dict[str, tuple[str, str]]:
    """Named proteins of a set of genomes, as a homology reference."""
    return {
        f"{sym}|{i}": (sym, prot)
        for i, rec in enumerate(records)
        for sym, prot in rec.proteins.items()
        if prot
    }
