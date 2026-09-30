"""Learn, validate and forecast on real genomes fetched by scripts/fetch_data.py.

    python scripts/run_realdata.py [--data data/raw] [--out results/real] [--no-homology]

Genes are named by protein homology (reciprocal best hits, see realdata/homology.py)
on top of their annotation; searches are cached in data/processed/homology.json.
"""

import argparse
import json
import re
from pathlib import Path

import numpy as np
import torch

from organelle_evo.plots import plot_lolo, plot_real_laws
from organelle_evo.realdata.analysis import forecast_lineages, leave_one_lineage_out, universality_test
from organelle_evo.realdata.catalog import CATALOG
from organelle_evo.realdata.dataset import build_dataset, read_genbank
from organelle_evo.realdata.genes import FEATURE_NAMES
from organelle_evo.realdata.homology import name_by_homology, reference_from_records
from organelle_evo.rules import fit_retention_bootstrap

MIN_LINEAGES = 5


def load_system(system: str, data_dir: Path, homology_cache: dict | None):
    """Dataset for one system; with a cache dict, genes are also named by homology."""
    spec = CATALOG[system]
    files = sorted((data_dir / system).glob("*.gb"))
    ancestor_stem = re.sub(r"[^A-Za-z0-9]+", "_", spec["ancestor"]).strip("_") if spec["ancestor"] else None
    ancestor = None
    records = []
    for f in files:
        rec = read_genbank(f)
        if f.stem == ancestor_stem:
            ancestor = rec
        elif rec.proteins:
            records.append(rec)
    if spec["ancestor"] and ancestor is None:
        print(f"  {system}: ancestor proxy {spec['ancestor']} missing, using union of lineages")
    added = {}
    if homology_cache is not None:
        cache = homology_cache.setdefault(system, {})
        if ancestor is not None:
            # Symbionts: match every gene against the free-living relative's proteome.
            records, added = name_by_homology(records, reference_from_records([ancestor]), cache=cache)
        else:
            # Organelles: match each genome against the named genes of all the others.
            named = []
            for i, rec in enumerate(records):
                others = records[:i] + records[i + 1 :]
                (new,), a = name_by_homology([rec], reference_from_records(others), cache=cache)
                named.append(new)
                added.update(a)
            records = named
    return build_dataset(system, records, ancestor), added


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--data", default="data/raw")
    ap.add_argument("--out", default="results/real")
    ap.add_argument("--n-boot", type=int, default=20)
    ap.add_argument("--no-homology", action="store_true", help="match genes by name only")
    args = ap.parse_args()
    torch.set_num_threads(1)
    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)

    cache_path = Path(args.data).parent / "processed" / "homology.json"
    cache = None
    if not args.no_homology:
        cache = json.loads(cache_path.read_text()) if cache_path.exists() else {}

    datasets, homology_added = {}, {}
    for system in CATALOG:
        ds, homology_added[system] = load_system(system, Path(args.data), cache)
        if len(ds.lineages) < MIN_LINEAGES:
            print(f"  {system}: only {len(ds.lineages)} genomes, skipping (run fetch_data.py)")
            continue
        datasets[system] = ds
        sizes = ds.present.sum(1)
        print(f"{system}: {len(ds.lineages)} genomes, {len(ds.genes)} genes in universe, "
              f"kept {sizes.min()}-{sizes.max()}")
    if not datasets:
        raise SystemExit("No data. Run scripts/fetch_data.py first.")
    if cache is not None:
        cache_path.parent.mkdir(parents=True, exist_ok=True)
        cache_path.write_text(json.dumps(cache))

    metrics, laws, lolo = {}, {}, {}
    report = ["# Real-genome results\n"]
    for system, ds in datasets.items():
        law = fit_retention_bootstrap([(ds.features, ds.present)], n_boot=args.n_boot)
        laws[system] = law
        lolo[system] = leave_one_lineage_out(ds)
        forecasts = forecast_lineages(ds, law, law.lineage_offsets[0])
        metrics[system] = {
            "n_genomes": len(ds.lineages),
            "genes_added_by_homology": homology_added.get(system, {}),
            "n_genes": len(ds.genes),
            "law": {f: {"weight": float(w), "se": float(s)}
                    for f, w, s in zip(FEATURE_NAMES, law.weights[0], law.weights_se[0])},
            "lolo_auroc": {
                "law_features_only": float(np.nanmean(lolo[system].auroc_law)),
                "gene_prevalence": float(np.nanmean(lolo[system].auroc_prevalence)),
                "law_plus_prevalence": float(np.nanmean(lolo[system].auroc_combined)),
            },
        }
        report.append(f"## {system}\n")
        report.append("| lineage | genes now | projected after +50% time (90% CI) | most at risk next |")
        report.append("|---|---|---|---|")
        for fc in sorted(forecasts, key=lambda f: -f.n_now):
            q = fc.count_quantiles
            risk = ", ".join(f"{g} ({p:.0%})" for g, p in fc.at_risk)
            report.append(f"| *{fc.lineage}* | {fc.n_now} | {q[1]:.0f} ({q[0]:.0f}-{q[2]:.0f}) | {risk} |")
        report.append("")
        print(f"  {system} law: " + ", ".join(f"{f}={w:+.2f}" for f, w in zip(FEATURE_NAMES, law.weights[0])))
        print(f"  {system} held-out AUROC: {metrics[system]['lolo_auroc']}")

    if len(datasets) > 1:
        uni = universality_test(list(datasets.values()))
        metrics["universality"] = {
            "systems": list(datasets),
            "delta_aic_shared_minus_separate": float(uni["delta_aic"]),
            "shared_weights": dict(zip(FEATURE_NAMES, map(float, uni["shared_weights"]))),
        }
        print(f"  universality: ΔAIC(shared - separate) = {uni['delta_aic']:.1f}")

    plot_real_laws(laws, FEATURE_NAMES, out / "fig_real_laws.png")
    plot_lolo(lolo, out / "fig_real_heldout.png")
    (out / "metrics.json").write_text(json.dumps(metrics, indent=2))
    (out / "forecasts.md").write_text("\n".join(report))
    print(f"Done -> {out}/")


if __name__ == "__main__":
    main()
