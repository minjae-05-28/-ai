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


def test_every_law_has_an_environment_card():
    import json

    from organelle_evo.laws import ANIMAL_LAWS_DIR, LAWS_DIR

    cards = LAWS_DIR / "environments"
    for path in [*LAWS_DIR.glob("*.json"), *ANIMAL_LAWS_DIR.glob("*.json")]:
        law_id = json.loads(path.read_text())["id"]
        card = json.loads((cards / f"{law_id}.json").read_text())
        assert card["law_id"] == law_id and "findings" in card
