from organelle_evo.animals.catalog import PAIR_AXES, PAIR_SPECS, SPECIES, design, resolve_pairs
from organelle_evo.laws import registry_for


def test_pairs_use_catalogue_species():
    for _, proxies, desc, _ in PAIR_SPECS:
        assert desc in SPECIES
        assert all(p in SPECIES for p in proxies)
    assert len(resolve_pairs(SPECIES)) == len(PAIR_SPECS)


def test_design_directions():
    z = dict(zip(("base", *PAIR_AXES), design("Takifugu rubripes", "Notothenia coriiceps")))
    assert z["colder"] > 1 and z["parasite"] == 0
    z = dict(zip(("base", *PAIR_AXES), design("Nematostella vectensis", "Hydra vulgaris")))
    assert z["freshwater"] == 1
    z = dict(zip(("base", *PAIR_AXES), design("Crocodylus porosus", "Gallus gallus")))
    assert z["endothermy"] == 1 and z["colder"] < 0
    z = dict(zip(("base", *PAIR_AXES), design("Caenorhabditis elegans", "Brugia malayi")))
    assert z["parasite"] == 1


def test_controls_change_little():
    for origin, proxies, desc, _ in PAIR_SPECS:
        if origin.startswith("control"):
            assert max(abs(v) for v in design(proxies[0], desc)[1:]) <= 0.25


def test_animal_laws_go_to_animal_registry():
    assert registry_for("animals").name == "animals"
