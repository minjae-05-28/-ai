"""Law-agnostic Mars experiment: one minimal cell, environment variables, random laws.

Nothing here is learned from data. The only biology fixed in advance is
  1. the starting cell (a LUCA-like minimal anaerobic autotroph, ~400 genes in modules),
  2. what each environment demands (REQUIREMENTS below: which modules a cell needs to get
     energy, make its building blocks and survive cold, salt, radiation and perchlorate).
How genomes change is left to random laws: for every module, the rates of gene loss,
duplication and gain respond to the environment variables with random coefficients.
Many random laws are run through a population simulation (mutation + selection) while
the environment moves from early Mars to present-day Mars, and the question is which
outcomes recur whatever the law is.
"""

from dataclasses import dataclass

import numpy as np

# Environment variables. Values are habitat conditions where the cells live.
ENV_VARS = ("temp_c", "salt_pct", "o2_pal", "radiation_x", "organics", "h2", "perchlorate", "light")


@dataclass(frozen=True)
class Environment:
    name: str
    temp_c: float  # deg C
    salt_pct: float  # % NaCl-equivalent
    o2_pal: float  # O2 relative to present Earth atmosphere
    radiation_x: float  # ionising dose relative to Earth's surface
    organics: float  # 0-1, available organic carbon
    h2: float  # 0-1, available hydrogen (e.g. serpentinisation)
    perchlorate: float  # 0-1, perchlorate in the brine
    light: float  # 0-1, usable light at the habitat

    def vector(self) -> np.ndarray:
        return np.array([getattr(self, v) for v in ENV_VARS], dtype=float)


EARTH_SOIL = Environment("Earth soil", 20, 1, 1.0, 1, 1.0, 0.2, 0.0, 0.3)
EARLY_MARS = Environment("early Mars lake (~3.8 Gya)", 10, 3, 0.0, 10, 0.3, 0.6, 0.1, 0.5)
MODERN_MARS = Environment("present Mars subsurface brine", -15, 25, 0.001, 30, 0.01, 0.3, 1.0, 0.0)


def stresses(env: Environment) -> dict[str, float]:
    """Environment variables as 0-1 pressures (0 = Earth-like, 1 = extreme)."""
    return {
        "cold": float(np.clip((15 - env.temp_c) / 30, 0, 1)),
        "salt": float(np.clip(env.salt_pct / 25, 0, 1)),
        "o2": float(np.clip(env.o2_pal, 0, 1)),
        "radiation": float(np.clip(np.log10(max(env.radiation_x, 1)) / 2, 0, 1)),
        "organics": float(np.clip(env.organics, 0, 1)),
        "h2": float(np.clip(env.h2, 0, 1)),
        "perchlorate": float(np.clip(env.perchlorate, 0, 1)),
        "light": float(np.clip(env.light, 0, 1)),
    }


STRESS_NAMES = ("cold", "salt", "o2", "radiation", "organics", "h2", "perchlorate", "light")

# module: (genes in the starting cell, genes needed for full function, essential)
MODULES = {
    "replication": (30, 25, True),
    "transcription": (20, 15, True),
    "translation": (120, 100, True),
    "membrane": (20, 15, True),
    "cell_division": (8, 6, True),
    "chaperones": (10, 6, True),
    "regulation": (10, 10, False),
    "unknown": (30, 1, False),
    "fermentation": (4, 12, False),
    "aerobic_respiration": (0, 20, False),
    "h2_oxidation": (8, 8, False),
    "carbon_fixation": (15, 15, False),
    "photosynthesis": (0, 30, False),
    "perchlorate_reduction": (0, 6, False),
    "transporters": (25, 30, False),
    "amino_acid_synthesis": (30, 25, False),
    "nucleotide_synthesis": (15, 12, False),
    "cofactor_synthesis": (15, 12, False),
    "cold_adaptation": (2, 8, False),
    "osmoprotection": (1, 10, False),
    "dna_repair": (15, 30, False),
    "oxidative_stress": (2, 8, False),
    "pigments_uv": (0, 6, False),
    "dormancy": (0, 15, False),
    "motility": (10, 10, False),
}
NAMES = tuple(MODULES)
START = np.array([v[0] for v in MODULES.values()], dtype=np.int64)
REQ = np.array([v[1] for v in MODULES.values()], dtype=float)
ESSENTIAL = np.array([v[2] for v in MODULES.values()])
IDX = {n: i for i, n in enumerate(NAMES)}
GENE_COST = 4e-4  # log-fitness cost per gene (replication and expression)
DOSAGE_COST = 3e-3  # extra cost per gene beyond twice what a module needs (dosage burden)


def capacity(G: np.ndarray) -> np.ndarray:
    """(N, M) share of each module's full function, 0-1."""
    return np.minimum(G / REQ, 1.0)


def log_fitness(G: np.ndarray, env: Environment) -> np.ndarray:
    """REQUIREMENTS: log fitness of genomes G (N, M) in an environment."""
    s = stresses(env)
    cap = capacity(G)
    c = lambda name: cap[:, IDX[name]]  # noqa: E731
    # Energy: the best pathway the environment and the genome allow.
    ferment = 0.3 * s["organics"] * c("fermentation")
    aerobic = 1.0 * min(s["organics"] + 0.5 * s["h2"], 1.0) * s["o2"] * c("aerobic_respiration")
    acceptor = 0.3 + 0.7 * s["perchlorate"] * c("perchlorate_reduction")  # CO2 alone yields little
    h2_auto = s["h2"] * c("h2_oxidation") * c("carbon_fixation") * acceptor
    photo = 0.8 * s["light"] * c("photosynthesis") * c("carbon_fixation")
    energy = np.max(np.stack([ferment, aerobic, h2_auto, photo]), 0)
    # Building blocks: made in the cell, or taken up when the environment has organics.
    uptake = s["organics"] * c("transporters")
    build = np.mean([np.maximum(c(k), uptake) for k in ("amino_acid_synthesis", "nucleotide_synthesis",
                                                       "cofactor_synthesis")], 0)
    # Stresses: each removes up to its strength unless the matching modules are present.
    protect = {
        "cold": c("cold_adaptation"),
        "salt": c("osmoprotection"),
        "radiation": 0.6 * c("dna_repair") + 0.25 * c("oxidative_stress") + 0.15 * c("pigments_uv"),
        "perchlorate": np.maximum(c("perchlorate_reduction"), c("oxidative_stress")),
        "o2": c("oxidative_stress"),
    }
    lw = np.log(energy + 1e-4) + np.log(build + 1e-4)
    for k, prot in protect.items():
        lw += np.log(np.clip(1 - 0.9 * s[k] * (1 - prot), 1e-4, 1))
    # Dormancy buffers the harshest conditions a little (survives between brief wet periods).
    harsh = np.mean([s["cold"], s["salt"], s["radiation"]])
    lw += 0.5 * harsh * c("dormancy")
    lw -= GENE_COST * G.sum(1) + DOSAGE_COST * np.maximum(G - 2 * REQ, 0).sum(1)
    lethal = (G[:, ESSENTIAL] < REQ[ESSENTIAL] * 0.8).any(1)
    return np.where(lethal, -np.inf, lw)


@dataclass
class RandomLaw:
    """Rates per module respond to the environment pressures with random coefficients."""
    loss: np.ndarray  # (M, S)
    dup: np.ndarray
    gain: np.ndarray

    @staticmethod
    def sample(rng, scale: float = 1.0) -> "RandomLaw":
        shape = (len(NAMES), len(STRESS_NAMES))
        return RandomLaw(*(rng.normal(0, scale, shape) for _ in range(3)))

    def rates(self, env: Environment, base=(2e-4, 1e-4, 3e-4)) -> tuple[np.ndarray, ...]:
        s = np.array([stresses(env)[k] for k in STRESS_NAMES])
        return tuple(b * np.exp(np.clip(W @ s, -4, 2)) for b, W in zip(base, (self.loss, self.dup, self.gain)))


def interpolate(a: Environment, b: Environment, t: float) -> Environment:
    return Environment(f"{a.name} -> {b.name}", *[(1 - t) * getattr(a, v) + t * getattr(b, v) for v in ENV_VARS])


def evolve(law: RandomLaw, path: list[Environment], *, n: int = 300, generations: int = 6000,
           ramp: float = 0.7, rng=None, record_every: int = 500, gain_scale: float = 1.0) -> dict:
    """Population of n asexual cells; the environment moves along `path` over the first
    `ramp` share of generations, then stays at the last one. gain_scale < 1 models an
    isolated biosphere (no other organisms to take genes from: new functions must arise de
    novo). Returns survival, the final mean genome and a trajectory."""
    rng = rng or np.random.default_rng()
    G = np.repeat(START[None, :], n, 0)
    traj = []
    for t in range(generations):
        u = min(t / (ramp * generations), 1.0) * (len(path) - 1)
        k = min(int(u), len(path) - 2)
        env = interpolate(path[k], path[k + 1], u - k)
        loss, dup, gain = law.rates(env)
        gain = gain * gain_scale
        # Mutation: per-gene loss, duplication, and per-module gain (horizontal transfer).
        # Duplication events scale with module size up to what the module needs, so a
        # duplication-biased law grows a module linearly rather than exponentially.
        G = G - rng.binomial(G, np.minimum(loss, 0.5)) + rng.poisson(dup * np.minimum(G, REQ)) \
            + rng.poisson(gain, size=G.shape)
        lw = log_fitness(G, env)
        if not np.isfinite(lw).any() or lw.max() < np.log(1e-3):
            return {"survived": False, "extinct_at": t, "env_at_extinction": env.vector().tolist(),
                    "final": G.mean(0).tolist(), "trajectory": traj}
        w = np.exp(lw - lw.max())
        G = G[rng.choice(n, n, p=w / w.sum())]
        if t % record_every == 0:
            traj.append({"t": t, "mean_genes": G.sum(1).mean(), "log_fitness": float(lw.max())})
    return {"survived": True, "extinct_at": None, "final": G.mean(0).tolist(),
            "final_log_fitness": float(log_fitness(G, path[-1]).mean()), "trajectory": traj}
