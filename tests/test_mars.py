import numpy as np

from organelle_evo.mars import EARLY_MARS, EARTH_SOIL, IDX, MODERN_MARS, START, RandomLaw, evolve, log_fitness


def test_requirements_rank_environments_and_modules():
    G = START[None, :].copy()
    assert log_fitness(G, MODERN_MARS)[0] < log_fitness(G, EARLY_MARS)[0]
    # Perchlorate reduction and osmoprotection help in present-day Mars brine.
    better = G.copy()
    better[0, IDX["perchlorate_reduction"]] = 6
    better[0, IDX["osmoprotection"]] = 10
    assert log_fitness(better, MODERN_MARS)[0] > log_fitness(G, MODERN_MARS)[0] + 1
    # Losing an essential module is lethal anywhere.
    dead = G.copy()
    dead[0, IDX["translation"]] = 10
    assert np.isneginf(log_fitness(dead, EARTH_SOIL)[0])


def test_evolution_is_bounded_and_reproducible():
    law = RandomLaw.sample(np.random.default_rng(1))
    a = evolve(law, [EARTH_SOIL, EARTH_SOIL], n=50, generations=300, rng=np.random.default_rng(2))
    b = evolve(law, [EARTH_SOIL, EARTH_SOIL], n=50, generations=300, rng=np.random.default_rng(2))
    assert a["survived"] and a["final"] == b["final"]
    assert sum(a["final"]) < 3 * START.sum()
