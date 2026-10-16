"""Atavism signature for drug searches (pre-registration 23): unicellular-era genes up in tumours and
multicellular-era genes down, from the paired TCGA QC data (13 cohorts, median of cohort mean LFC).

    python scripts/atavism_signature.py   -> results/drug/signature.json
"""

import json
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import cancer_atavism as ca  # noqa: E402
from cancer_composition import IMMUNE, STROMAL  # noqa: E402
from cancer_depmap import tumour_lfc  # noqa: E402
from cancer_proliferation import load_p  # noqa: E402

N_GENES, MIN_ABS = 150, 0.5


def main():
    ages = ca.load_ages()
    go, hall, _ = load_p()
    skip = go | hall | set(IMMUNE) | set(STROMAL)
    lfc = tumour_lfc()
    med = {g: float(np.median(list(v.values()))) for g, v in lfc.items()
           if len(v) >= 7 and g in ages and g not in skip}
    up = sorted([g for g, m in med.items() if ages[g][0] <= 3 and m >= MIN_ABS], key=lambda g: -med[g])[:N_GENES]
    down = sorted([g for g, m in med.items() if ages[g][0] > 3 and m <= -MIN_ABS], key=lambda g: med[g])[:N_GENES]
    out = {"rule": f"top {N_GENES} UC genes with median LFC >= {MIN_ABS}; bottom {N_GENES} MC genes <= -{MIN_ABS}; "
                   "proliferation, immune and stromal marker genes excluded",
           "up": up, "down": down, "median_lfc": {g: round(med[g], 3) for g in up + down}}
    Path("results/drug").mkdir(parents=True, exist_ok=True)
    Path("results/drug/signature.json").write_text(json.dumps(out, indent=1))
    print(len(up), "up", len(down), "down; e.g.", up[:8], down[:8])


if __name__ == "__main__":
    main()
