"""Overall survival, age and stage per TCGA patient for pre-registration 28, reduced on a GitHub runner.
Only the clinical table is downloaded; the per-patient tilt scores already exist in data/tcga_stage/.

    data/tcga_survival/<COHORT>.tsv  patient, time (days), event (1 = died), age (years), stage (1-4 or blank)
    data/tcga_survival/manifest.json columns used per cohort, patients, deaths

Public aggregate clinical fields only, keyed by TCGA barcode; nothing else about the patients.
"""

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from tcga_fetch import get  # noqa: E402
from tcga_stage_fetch import CLIN, stage_number  # noqa: E402

OUT = Path("data/tcga_survival")
COHORTS = ["BLCA", "BRCA", "COAD", "ESCA", "HNSC", "KICH", "KIRC", "KIRP", "LIHC", "LUAD", "LUSC", "PRAD",
           "READ", "STAD", "THCA", "UCEC"]
# Xena clinicalMatrix names these differently across cohorts; first match wins.
TIME_DEAD = ["days_to_death", "OS.time"]
TIME_ALIVE = ["days_to_last_followup", "days_to_last_follow_up"]
STATUS = ["vital_status", "OS"]
AGE = ["age_at_initial_pathologic_diagnosis", "age_at_diagnosis"]
STAGE = ["pathologic_stage", "clinical_stage"]


def num(x):
    try:
        v = float(x)
    except (TypeError, ValueError):
        return None
    return v


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    manifest = {}
    for c in COHORTS:
        raw = get(CLIN.format(c=c))
        if raw is None:
            manifest[c] = {"error": "download failed"}
            print(c, "download failed", flush=True)
            continue
        lines = raw.decode(errors="replace").splitlines()
        head = lines[0].split("\t")
        pick = lambda names: next((head.index(n) for n in names if n in head), None)
        j_dead, j_alive = pick(TIME_DEAD), pick(TIME_ALIVE)
        j_status, j_age, j_stage = pick(STATUS), pick(AGE), pick(STAGE)
        used = {"time_dead": j_dead is not None and head[j_dead], "time_alive": j_alive is not None and head[j_alive],
                "status": j_status is not None and head[j_status], "age": j_age is not None and head[j_age],
                "stage": j_stage is not None and head[j_stage]}
        if j_status is None or (j_dead is None and j_alive is None):
            manifest[c] = {"error": "no survival columns", "columns_found": used}
            print(c, "no survival columns", flush=True)
            continue
        cell = lambda x, j: (x[j].strip() if j is not None and len(x) > j else "")
        rows, deaths = {}, 0
        for line in lines[1:]:
            x = line.split("\t")
            pat = x[0][:12]
            st = cell(x, j_status).lower()
            dead = st in ("dead", "deceased", "1", "1.0")
            alive = st in ("alive", "living", "0", "0.0")
            if not (dead or alive):
                continue
            t = num(cell(x, j_dead)) if dead else num(cell(x, j_alive))
            if t is None:                                  # OS.time style: one column for both
                t = num(cell(x, j_dead if j_dead is not None else j_alive))
            if t is None or t <= 0:
                continue
            prev = rows.get(pat)
            if prev and not (dead and not prev[1]) and prev[0] >= t:
                continue                                   # keep the longer record; a death wins over a follow-up
            rows[pat] = (t, dead, num(cell(x, j_age)), stage_number(cell(x, j_stage)))
        with open(OUT / f"{c}.tsv", "w") as f:
            f.write("patient\ttime\tevent\tage\tstage\n")
            for pat, (t, dead, age, stage) in sorted(rows.items()):
                deaths += int(dead)
                f.write(f"{pat}\t{t:.0f}\t{int(dead)}\t{'' if age is None else f'{age:.0f}'}"
                        f"\t{'' if stage is None else stage}\n")
        manifest[c] = {"patients": len(rows), "deaths": deaths, "columns_used": used}
        print(c, manifest[c], flush=True)
    (OUT / "manifest.json").write_text(json.dumps(manifest, indent=1))


if __name__ == "__main__":
    main()
