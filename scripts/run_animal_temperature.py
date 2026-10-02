"""Does the microbial temperature law transfer to animal cells?

    python scripts/run_animal_temperature.py

The project's strongest sequence law is composition versus temperature, fitted to 86
prokaryotes and archaea: IVYWREL rises +0.00098 per degree of optimal growth temperature
(p 4e-25; it survives taxonomy GLS, tree PGLS, all 20 bootstrap trees, and GC and GC3 as
covariates). In those species the cell's temperature *is* the habitat temperature.

Before that law can say anything about an animal cell, it has to hold for animal cells.
Animals supply a natural experiment: birds and mammals hold their cells at 36-42 C, while
invertebrates and ectothermic vertebrates sit near ambient, usually 15-25 C. That is a
15-20 C difference in the law's own input variable, so the law predicts endotherms should
carry roughly +0.015 to +0.020 more IVYWREL.

This script tests that on the mitochondrion-encoded proteomes we already have (75 species,
data/composition/endosymbiosis/mitochondrion). It also controls for the AT bias that this
project measured as the main driver of mitochondrial composition, using FYMINK as the GC
proxy (our own GC check found r(GC, FYMINK) = -0.88 to -0.94).

Output: results/animal_temperature/.
"""

import json
from pathlib import Path

import numpy as np
from scipy.stats import mannwhitneyu, spearmanr

from organelle_evo.laws import ANIMAL_LAWS_DIR, save_law

MITO = Path("data/composition/endosymbiosis/mitochondrion")
OUT = Path("results/animal_temperature")

# Coefficient of the project's temperature law (results/phylo, ivywrel_vs_temperature):
# OLS +0.0009836, tree PGLS +0.0006997, rank GLS +0.0007847 per degree C.
LAW_PER_C = {"ols": 0.0009836, "tree_pgls": 0.0006997, "rank_gls": 0.0007847}

# Metazoa only, with the temperature the cells actually run at. Endotherms are textbook
# core temperatures; ectotherms are typical habitat temperatures, which are the uncertain
# ones, so the test below also uses the endotherm/ectotherm split on its own.
ANIMALS = {
    "Homo sapiens": (37.0, "endotherm"),
    "Mus musculus": (37.0, "endotherm"),
    "Gallus gallus": (41.5, "endotherm"),
    "Danio rerio": (26.0, "ectotherm"),
    "Xenopus laevis": (22.0, "ectotherm"),
    "Ciona intestinalis B CG-2006": (18.0, "ectotherm"),
    "Branchiostoma floridae": (22.0, "ectotherm"),
    "Strongylocentrotus purpuratus": (14.0, "ectotherm"),
    "Drosophila melanogaster": (25.0, "ectotherm"),
    "Anopheles gambiae": (27.0, "ectotherm"),
    "Apis mellifera": (25.0, "ectotherm"),
    "Daphnia pulex": (20.0, "ectotherm"),
    "Caenorhabditis elegans": (20.0, "ectotherm"),
    "Amphimedon queenslandica": (25.0, "ectotherm"),
    "Metridium senile": (12.0, "ectotherm"),
    "Nematostella sp. JVK-2006": (20.0, "ectotherm"),
    "Trichoplax adhaerens": (25.0, "ectotherm"),
    # parasites of warm-blooded hosts: their cells run at host temperature, but their
    # genomes are also degrading, which this project has shown shifts composition
    "Ascaris suum": (39.0, "parasite of an endotherm"),
    "Schistosoma mansoni": (37.0, "parasite of an endotherm"),
}


def load():
    rows = []
    for f in sorted(MITO.glob("*.json")):
        d = json.loads(f.read_text())
        sp = d["species"]
        if sp in ANIMALS and d["n_proteins"] >= 10:
            t, group = ANIMALS[sp]
            rows.append({"species": sp, "temperature_c": t, "group": group,
                         "ivywrel": d["ivywrel"], "fymink": d["fymink"],
                         "cvp": d["cvp"], "n_proteins": d["n_proteins"]})
    return rows


def partial_spearman(x, y, z):
    from scipy.stats import rankdata
    rx, ry, rz = (rankdata(v) for v in (x, y, z))
    A = np.c_[np.ones_like(rz), rz]
    ex = rx - A @ np.linalg.lstsq(A, rx, rcond=None)[0]
    ey = ry - A @ np.linalg.lstsq(A, ry, rcond=None)[0]
    return float(np.corrcoef(ex, ey)[0, 1])


def main():
    rows = load()
    res = {"law_per_degree_c": LAW_PER_C, "n_animals": len(rows), "species": rows}
    endo = [r for r in rows if r["group"] == "endotherm"]
    ecto = [r for r in rows if r["group"] == "ectotherm"]
    para = [r for r in rows if r["group"].startswith("parasite")]
    print(f"{len(rows)} animals with a mitochondrial proteome: {len(endo)} endotherms, "
          f"{len(ecto)} ectotherms, {len(para)} parasites of endotherms\n")

    ei = np.array([r["ivywrel"] for r in endo])
    ci = np.array([r["ivywrel"] for r in ecto])
    dT = float(np.mean([r["temperature_c"] for r in endo]) - np.mean([r["temperature_c"] for r in ecto]))
    observed = float(ei.mean() - ci.mean())
    print(f"endotherms  IVYWREL {ei.mean():.4f}  ({', '.join(r['species'].split()[0] + ' ' + format(r['ivywrel'], '.3f') for r in endo)})")
    print(f"ectotherms  IVYWREL {ci.mean():.4f}  [{ci.min():.3f}, {ci.max():.3f}], n={len(ecto)}")
    print(f"\nendotherm cells run {dT:.1f} C warmer, so the law predicts:")
    for k, v in LAW_PER_C.items():
        print(f"   {k:10s} {v * dT:+.4f}")
    print(f"observed difference:  {observed:+.4f}")
    u = mannwhitneyu(ei, ci, alternative="two-sided")
    print(f"Mann-Whitney U p = {u.pvalue:.3f} ({'n.s.' if u.pvalue > 0.05 else 'significant'})")
    pred = LAW_PER_C["ols"] * dT
    print(f"\nThe law predicts {pred:+.4f}; the data give {observed:+.4f} "
          f"-> {'OPPOSITE SIGN' if np.sign(pred) != np.sign(observed) else 'same sign'}, "
          f"off by {abs(observed - pred):.4f} ({abs(observed - pred) / abs(pred):.1f}x the predicted effect)")
    res["endotherm_vs_ectotherm"] = {
        "n_endotherm": len(endo), "n_ectotherm": len(ecto),
        "mean_ivywrel_endotherm": float(ei.mean()), "mean_ivywrel_ectotherm": float(ci.mean()),
        "delta_temperature_c": dT, "predicted_delta_ivywrel": pred,
        "observed_delta_ivywrel": observed, "mannwhitney_p": float(u.pvalue),
        "transfers": bool(np.sign(pred) == np.sign(observed) and u.pvalue < 0.05)}

    # continuous version over every animal, and the AT-bias control
    T = np.array([r["temperature_c"] for r in rows if not r["group"].startswith("parasite")])
    Y = np.array([r["ivywrel"] for r in rows if not r["group"].startswith("parasite")])
    F = np.array([r["fymink"] for r in rows if not r["group"].startswith("parasite")])
    rho = float(spearmanr(T, Y).correlation)
    slope = float(np.polyfit(T, Y, 1)[0])
    print(f"\nacross all {len(T)} non-parasitic animals: Spearman(cell temperature, IVYWREL) {rho:+.2f}, "
          f"slope {slope:+.5f} per C (law says {LAW_PER_C['ols']:+.5f})")
    print(f"  IVYWREL vs FYMINK (our GC proxy): Spearman {spearmanr(Y, F).correlation:+.2f} "
          f"-> composition tracks AT bias, not temperature")
    print(f"  Spearman(temperature, IVYWREL) controlling for FYMINK: {partial_spearman(T, Y, F):+.2f}")
    res["all_animals"] = {"n": len(T), "spearman_temperature_vs_ivywrel": rho,
                          "slope_per_degree_c": slope,
                          "spearman_ivywrel_vs_fymink": float(spearmanr(Y, F).correlation),
                          "partial_spearman_controlling_at_bias": partial_spearman(T, Y, F)}

    if para:
        print(f"\nparasites of warm-blooded hosts (cells at 37-39 C, but degrading genomes):")
        for r in para:
            print(f"   {r['species']:24s} IVYWREL {r['ivywrel']:.3f}  FYMINK {r['fymink']:.3f}")
        print("   the highest values in the set, but this project already attributed that to "
              "genome AT bias in reduced genomes, not to host temperature")
        res["parasites_of_endotherms"] = para

    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "metrics.json").write_text(json.dumps(res, indent=2))
    save_law(ANIMAL_LAWS_DIR / "animal_temperature_v1.json", id="animal_temperature_v1",
             scope="Whether the prokaryote temperature-composition law transfers to animal cells, tested on "
                   "mitochondrion-encoded proteomes of endotherms (cells at 36-42 C) against ectotherms "
                   "(cells near ambient, 12-27 C).",
             model="Predicted IVYWREL difference from the fitted law (+0.00098 per C) against the observed "
                   "difference; continuous slope over all animals; AT bias (FYMINK) as the control.",
             feature_names=["cell_temperature_c"], data={"animals": len(rows)}, validation=res, contexts={},
             caveats=["Only three endotherms have a mitochondrial proteome here, so the group test is weak; "
                      "the sign and magnitude of the mismatch carry the result, not the p-value.",
                      "Ectotherm temperatures are typical habitat values, not measured cell temperatures.",
                      "Mitochondrion-encoded proteins are few, membrane-bound and hydrophobic, and their "
                      "composition is dominated by mitochondrial AT bias; nuclear proteomes would be the "
                      "better test and are not in this dataset.",
                      "A failure to transfer does not mean temperature has no effect on animal proteins, only "
                      "that this law, fitted to microbes, does not predict it.",
                      "SUPERSEDED IN PART by animal_axes_v1, which uses nuclear proteomes (69 species, ~20k "
                      "proteins each) instead of the 13 mitochondrion-encoded genes: there the temperature "
                      "coefficient for IVYWREL is +0.0002 per C, the SAME sign as the microbial law but about "
                      "five times weaker, and it does not survive leave-one-clade-out or the clade-level "
                      "refit. So the reversed sign reported here is a property of mitochondrial proteomes, "
                      "driven by mitochondrial AT bias, and not of animal cells in general. The conclusion "
                      "that the microbial law must not be applied to animal cells stands on both datasets; "
                      "the claim of an inverted law does not."])
    print(f"\nDone -> {OUT}/")


if __name__ == "__main__":
    main()
