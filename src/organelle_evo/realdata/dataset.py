"""Turn GenBank records into gene-content matrices and per-gene features."""

from dataclasses import dataclass, field
from pathlib import Path

import numpy as np
from Bio import SeqIO

from .genes import (
    FEATURE_NAMES,
    functional_class,
    gene_features,
    normalize_gene_name,
    symbol_from_product,
)


@dataclass
class GenomeRecord:
    organism: str
    accession: str
    proteins: dict[str, str]  # canonical gene symbol -> protein sequence
    # Every protein-coding CDS, named or not: CDS id -> protein. Homology search uses
    # these to name genes the annotation left anonymous.
    cds: dict[str, str] = field(default_factory=dict)
    cds_symbol: dict[str, str] = field(default_factory=dict)  # CDS id -> symbol, if named

    def with_symbols(self, extra: dict[str, str]) -> "GenomeRecord":
        """Copy with additional CDS id -> symbol assignments (genes already present keep
        their annotated protein)."""
        symbols = {**self.cds_symbol, **extra}
        proteins = dict(self.proteins)
        for cid, sym in extra.items():
            if sym not in proteins:
                proteins[sym] = self.cds[cid]
        return GenomeRecord(self.organism, self.accession, proteins, self.cds, symbols)


def _translation(feat, rec) -> str:
    prot = feat.qualifiers.get("translation", [""])[0]
    if prot:
        return prot
    table = int(feat.qualifiers.get("transl_table", ["1"])[0])
    try:
        return str(feat.translate(rec.seq, table=table, cds=False)).rstrip("*")
    except Exception:  # noqa: BLE001 - malformed locations in old records
        return ""


def read_genbank(path: str | Path) -> GenomeRecord:
    """Protein-coding genes of a (possibly multi-record) GenBank file."""
    proteins, cds, cds_symbol, organism, accession = {}, {}, {}, "", ""
    for rec in SeqIO.parse(str(path), "genbank"):
        organism = organism or rec.annotations.get("organism", "")
        accession = accession or rec.id
        organelle = next(
            (f.qualifiers.get("organelle", [""])[0] for f in rec.features if f.type == "source"), ""
        )
        for feat in rec.features:
            if feat.type != "CDS" or "pseudo" in feat.qualifiers or "pseudogene" in feat.qualifiers:
                continue
            if "gene" in feat.qualifiers:
                name = normalize_gene_name(feat.qualifiers["gene"][0])
            else:
                name = symbol_from_product(feat.qualifiers.get("product", [""])[0], organelle)
            prot = _translation(feat, rec)
            cid = f"{rec.id}:{len(cds)}"
            if prot:
                cds[cid] = prot
                if name is not None:
                    cds_symbol[cid] = name
            if name is None:
                continue
            # Keep the longest copy (inverted repeats, split genes).
            if len(prot) >= len(proteins.get(name, "")):
                proteins[name] = prot
    return GenomeRecord(organism, accession, proteins, cds, cds_symbol)


@dataclass
class GeneContentDataset:
    system: str
    genes: list[str]
    features: np.ndarray  # (G, F), columns FEATURE_NAMES
    present: np.ndarray  # (L, G) bool: gene still encoded in the organelle/symbiont genome
    lineages: list[str]
    accessions: list[str]

    @property
    def classes(self) -> list[str]:
        return [functional_class(g) for g in self.genes]

    feature_names = FEATURE_NAMES


def build_dataset(
    system: str,
    records: list[GenomeRecord],
    ancestor: GenomeRecord | None = None,
    min_lineages: int = 2,
) -> GeneContentDataset:
    """Gene universe = the ancestor proxy's genes if given, else the union of genes seen
    in at least `min_lineages` lineages (the gene-richest genomes stand in for the
    ancestor; genes lost in every lineage are necessarily invisible)."""
    if ancestor is not None:
        universe = sorted(ancestor.proteins)
    else:
        counts: dict[str, int] = {}
        for r in records:
            for g in r.proteins:
                counts[g] = counts.get(g, 0) + 1
        universe = sorted(g for g, c in counts.items() if c >= min_lineages)

    proteins_by_gene = {g: [] for g in universe}
    for r in [*records, *([ancestor] if ancestor else [])]:
        for g, p in r.proteins.items():
            if g in proteins_by_gene:
                proteins_by_gene[g].append(p)
    if ancestor is not None:  # describe genes by the free-living ancestor's proteins
        proteins_by_gene = {g: [ancestor.proteins[g]] for g in universe}

    genes, features = gene_features(proteins_by_gene)
    present = np.array([[g in r.proteins for g in genes] for r in records], dtype=bool)
    return GeneContentDataset(
        system=system,
        genes=genes,
        features=features,
        present=present,
        lineages=[r.organism for r in records],
        accessions=[r.accession for r in records],
    )
