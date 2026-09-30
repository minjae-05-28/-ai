"""Gene names, functional classes and sequence-derived features for real genomes."""

import re

import numpy as np

# Kyte & Doolittle (1982) hydropathy scale.
KYTE_DOOLITTLE = {
    "A": 1.8, "R": -4.5, "N": -3.5, "D": -3.5, "C": 2.5, "Q": -3.5, "E": -3.5,
    "G": -0.4, "H": -3.2, "I": 4.5, "L": 3.8, "K": -3.9, "M": 1.9, "F": 2.8,
    "P": -1.6, "S": -0.8, "T": -0.7, "W": -0.9, "Y": -1.3, "V": 4.2,
}  # fmt: skip

# Synonyms seen across mitochondrial annotations -> one canonical symbol.
_MITO_SYNONYMS = {
    **{f"nd{i}": f"nad{i}" for i in range(1, 12)},
    "nd4l": "nad4l", "nadh4l": "nad4l",
    **{f"nadh{i}": f"nad{i}" for i in range(1, 12)},
    "coi": "cox1", "coii": "cox2", "coiii": "cox3", "co1": "cox1", "co2": "cox2", "co3": "cox3",
    "coxi": "cox1", "coxii": "cox2", "coxiii": "cox3",
    "cytb": "cob", "cyb": "cob", "cob": "cob",
    "atpase6": "atp6", "atpase8": "atp8", "atpase9": "atp9",
    "mttb": "tatc", "ymf16": "tatc",
}  # fmt: skip

_AMINO_ACIDS = (
    "ala arg asn asp cys gln glu gly his ile leu lys met phe pro ser thr trp tyr val".split()
)


def normalize_gene_name(name: str) -> str | None:
    """Canonical lower-case symbol, or None for names we can't compare across species."""
    if not name:
        return None
    n = name.strip().lower().replace(" ", "")
    n = re.sub(r"[-_.](exon|part)?\d+$", "", n)  # nad5-1, rps12_2, ...
    n = _MITO_SYNONYMS.get(n, n)
    # Open reading frames are lineage-specific, so they can't be compared across species.
    if n.startswith(("orf", "ymf")):
        return None
    # Gene symbols look like thrA, nad4L, rps12, rpoC1, ycf1; locus tags don't.
    if not re.fullmatch(r"[a-z]{2,4}\d{0,2}[a-z]?\d?", n):
        return None
    return n


_ROMAN = {"i": "1", "ii": "2", "iii": "3"}
_RNAP = {"alpha": "rpoa", "beta": "rpob", "beta'": "rpoc1", "beta''": "rpoc2"}


def symbol_from_product(product: str, organelle: str = "") -> str | None:
    """Canonical symbol from a /product description, for records without /gene.

    Only unambiguous core organelle genes are mapped; the organelle matters because
    "NADH dehydrogenase subunit 2" is nad2 in mitochondria but ndhB in plastids.
    """
    p = product.strip().lower()
    if m := re.fullmatch(r"(?:small subunit |large subunit )?ribosomal protein ([sl])(\d+)", p):
        return f"rp{m[1]}{m[2]}"
    if m := re.fullmatch(r"(?:ycf|hypothetical chloroplast rf)(\d+)", p):
        return f"ycf{m[1]}"
    if organelle.startswith("mitochondri"):
        if m := re.fullmatch(r"nadh dehydrogenase subunit (\d+l?)", p):
            return f"nad{m[1]}"
        if m := re.fullmatch(r"cytochrome c oxidase subunit (1|2|3|i{1,3})", p):
            return f"cox{_ROMAN.get(m[1], m[1])}"
        if p in ("cytochrome b", "apocytochrome b"):
            return "cob"
        if m := re.fullmatch(r"atp(?:ase| synthase) (?:f0 )?subunit (6|8|9|a|c)", p):
            return "atp" + {"a": "6", "c": "9"}.get(m[1], m[1])
    if organelle.startswith(("plastid", "chloroplast", "chromatophore", "apicoplast")):
        if m := re.fullmatch(r"(?:dna-directed )?rna polymerase (alpha|beta'{0,2}) (?:subunit|chain)", p):
            return _RNAP[m[1]]
        if p == "elongation factor tu":
            return "tufa"
        if p == "atp-dependent clp protease proteolytic subunit":
            return "clpp"
    return None


# (class name, regex on canonical symbol). First match wins.
FUNCTIONAL_CLASSES = [
    ("redox_core", r"^(nad\d|nad4l|ndh[a-z]|nuo[a-n]|cob|cox[123]|cyo[a-d]|cyd[ab]|sdh[1-4a-d]|"
                   r"psa[a-z]|psb[a-z]+|pet[a-z])$"),
    ("atp_synthase", r"^atp[a-i1-9]$"),
    ("translation", r"^(rps\d+|rpl\d+|rpm[a-j]|tuf[ab]?|inf[abc]|fus[a]?|tsf|prf[abc]|efp|"
                    r"(" + "|".join(_AMINO_ACIDS) + r")[st])$"),
    ("transcription", r"^(rpo[a-z]\d?|rpo[a-z]{1,2}|sig[a-z])$"),
    ("protein_targeting", r"^(sec[a-z]|tat[a-e]|ffh|fts[y]|yid[c]|ccm[a-z]+|ccs[a-z]|cem[a])$"),
    ("carbon_fixation", r"^(rbc[ls]|cbb[a-z]+)$"),
]


def functional_class(symbol: str) -> str:
    for name, pattern in FUNCTIONAL_CLASSES:
        if re.match(pattern, symbol):
            return name
    return "other"


def gravy(protein: str) -> float:
    vals = [KYTE_DOOLITTLE[a] for a in protein.upper() if a in KYTE_DOOLITTLE]
    return float(np.mean(vals)) if vals else 0.0


def tm_helices(protein: str, window: int = 19, threshold: float = 1.6) -> int:
    """Count putative transmembrane helices (Kyte-Doolittle 19-residue window >= 1.6)."""
    vals = np.array([KYTE_DOOLITTLE.get(a, 0.0) for a in protein.upper()])
    if len(vals) < window:
        return 0
    smooth = np.convolve(vals, np.ones(window) / window, mode="valid")
    count, i = 0, 0
    while i < len(smooth):
        if smooth[i] >= threshold:
            count += 1
            i += window
        else:
            i += 1
    return count


FEATURE_NAMES = (
    "hydrophobicity_gravy",
    "tm_helices",
    "protein_length",
    "redox_core",
    "atp_synthase",
    "translation",
    "transcription",
    "protein_targeting",
)


def gene_features(proteins_by_gene: dict[str, list[str]]) -> tuple[list[str], np.ndarray]:
    """Features per gene from all observed copies of its protein.

    Continuous features are z-scored within the gene set so weights are comparable
    across systems; functional classes are 0/1 indicators.
    """
    genes = sorted(proteins_by_gene)
    if not genes:
        return [], np.zeros((0, len(FEATURE_NAMES)))
    raw = []
    for g in genes:
        prots = [p for p in proteins_by_gene[g] if p] or [""]
        raw.append(
            (
                np.mean([gravy(p) for p in prots]),
                np.log1p(np.mean([tm_helices(p) for p in prots])),
                np.log(max(1.0, np.mean([len(p) for p in prots]))),
            )
        )
    raw = np.array(raw, dtype=float)
    cont = (raw - raw.mean(0)) / np.where(raw.std(0) > 0, raw.std(0), 1.0)
    classes = [functional_class(g) for g in genes]
    onehot = np.array(
        [[c == name for name in FEATURE_NAMES[3:]] for c in classes], dtype=float
    ).reshape(len(genes), len(FEATURE_NAMES) - 3)
    return genes, np.concatenate([cont, onehot], axis=1)
