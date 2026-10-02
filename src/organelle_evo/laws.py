"""A small registry of learned evolutionary laws.

Each law file in laws/ records what was learned, from which data, under which model,
and — most importantly — where it applies. Later analyses load laws from here to
compare against or to use as reference predictors, never silently as training input.
"""

import json
from dataclasses import dataclass
from pathlib import Path

import numpy as np

LAWS_DIR = Path(__file__).resolve().parents[2] / "laws"

# Laws fitted to animal cells live in their own registry and are never mixed with the
# microbial ones. This is not tidiness: the project measured that the microbial
# temperature law does not transfer to animals (laws/animals/animal_temperature_v1.json),
# so a coefficient from one registry applied to the other gives a wrong answer, and on
# IVYWREL it gave the wrong sign. ANIMAL_LAWS_DIR holds the animal registry.
ANIMAL_LAWS_DIR = LAWS_DIR / "animals"

# which registry a catalogue's species belong to
REGISTRY = {"prokaryotes": LAWS_DIR, "eukaryotes": LAWS_DIR, "realdata": LAWS_DIR,
            "animals": ANIMAL_LAWS_DIR}


def registry_for(catalog: str) -> Path:
    """The law directory a catalogue may read and write. Raises on an unknown catalogue
    rather than silently defaulting to the microbial registry."""
    if catalog not in REGISTRY:
        raise KeyError(f"unknown catalogue {catalog!r}; known: {sorted(REGISTRY)}")
    return REGISTRY[catalog]


@dataclass(frozen=True)
class Law:
    id: str
    scope: str
    model: str
    feature_names: tuple[str, ...]
    weights: dict[str, np.ndarray]  # context (e.g. system) -> weights over features
    ci95: dict[str, np.ndarray]  # context -> (F, 2) lower/upper bounds
    meta: dict

    def significant(self, context: str) -> np.ndarray:
        lo, hi = self.ci95[context].T
        return (lo > 0) | (hi < 0)


def load_law(law_id: str, directory: Path = LAWS_DIR) -> Law:
    d = json.loads((directory / f"{law_id}.json").read_text())
    feats = tuple(d["feature_names"])
    weights, ci = {}, {}
    for ctx, coefs in d["contexts"].items():
        # Structural laws (modules, orders, lists of families) keep descriptive contexts.
        if not feats or not isinstance(coefs, dict) or not all(isinstance(coefs.get(f), dict) for f in feats):
            continue
        weights[ctx] = np.array([coefs[f]["weight"] for f in feats])
        ci[ctx] = np.array([coefs[f]["ci95"] for f in feats])
    meta = {k: v for k, v in d.items() if k != "feature_names"}
    return Law(d["id"], d["scope"], d["model"], feats, weights, ci, meta)


def save_law(path: Path, **fields) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(fields, indent=2, ensure_ascii=False) + "\n")
