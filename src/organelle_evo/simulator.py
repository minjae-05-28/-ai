"""Forward model: endosymbiont -> organelle genome reduction.

Every ancestral gene starts in the symbiont (ORGANELLE) and can undergo one of two
irreversible events, as competing risks in continuous time:

- endosymbiotic gene transfer to the host nucleus (NUCLEUS)
- loss / pseudogenisation (LOST)

Per-gene hazards follow log-linear "rules" of the gene features. A lineage is described
by three hidden parameters:

- log_transfer : log of integrated host-driven transfer pressure (host control x time)
- log_loss     : log of integrated loss pressure (drift / Muller's ratchet x time)
- coupling     : pathway collapse; once part of a pathway is lost, the remaining
                 genes in it lose faster (loss hazard x (1 + coupling * lost fraction))

Because hazards and time only enter as products, time is absorbed into the pressures:
a snapshot alone cannot separate "strong pressure" from "long time".
"""

from dataclasses import dataclass, field

import numpy as np

from .ancestor import AncestorGenome

ORGANELLE, NUCLEUS, LOST = 0, 1, 2
STATE_NAMES = ("organelle", "nucleus", "lost")


@dataclass(frozen=True)
class Rules:
    transfer_bias: float
    transfer_weights: tuple[float, ...]
    loss_bias: float
    loss_weights: tuple[float, ...]

    def base_log_rates(self, genome: AncestorGenome) -> tuple[np.ndarray, np.ndarray]:
        x = genome.features
        return (
            self.transfer_bias + x @ np.asarray(self.transfer_weights),
            self.loss_bias + x @ np.asarray(self.loss_weights),
        )


# Ground-truth "laws" of the synthetic world. Signs follow the literature:
# hydrophobic and redox-coupled genes resist transfer; redundant genes get lost;
# genes the organelle still needs are transferred rather than lost.
TRUE_RULES = Rules(
    transfer_bias=-1.0,
    transfer_weights=(-3.0, -2.0, 0.5, 1.5),
    loss_bias=-1.5,
    loss_weights=(0.0, -0.5, 3.0, -3.0),
)

PARAM_NAMES = ("log_transfer", "log_loss", "coupling")
PRIOR_LOW = np.array([-1.0, -1.0, 0.0])
PRIOR_HIGH = np.array([3.0, 3.0, 3.0])


def sample_prior(n: int, rng: np.random.Generator, low=PRIOR_LOW, high=PRIOR_HIGH) -> np.ndarray:
    """Uniform prior over lineage parameters, shape (n, 3)."""
    return rng.uniform(low, high, size=(n, len(PARAM_NAMES)))


@dataclass
class SimResult:
    states: np.ndarray  # (B, G) final state per gene
    counts: np.ndarray  # (B, n_steps + 1, 3) number of genes in each state over time
    snapshots: dict[int, np.ndarray] = field(default_factory=dict)  # step -> (B, G)


def simulate(
    genome: AncestorGenome,
    rules: Rules,
    params: np.ndarray,
    *,
    horizon: float = 1.0,
    n_steps: int = 100,
    initial_states: np.ndarray | None = None,
    snapshot_steps: tuple[int, ...] = (),
    rng: np.random.Generator | None = None,
) -> SimResult:
    """Simulate B lineages in parallel.

    `params` is (B, 3) in PARAM_NAMES order. `horizon` is measured in units of the
    history the params describe, so horizon=0.5 continues evolution for half as long
    again (used for forecasting from a snapshot).
    """
    rng = rng or np.random.default_rng()
    params = np.atleast_2d(params)
    batch, n_genes = len(params), genome.n_genes
    base_t, base_l = rules.base_log_rates(genome)
    k_transfer = np.exp(params[:, :1] + base_t[None])
    k_loss_base = np.exp(params[:, 1:2] + base_l[None])
    coupling = params[:, 2:3]

    membership = np.zeros((n_genes, genome.n_pathways))
    membership[np.arange(n_genes), genome.pathway] = 1.0
    pathway_size = membership.sum(0)

    if initial_states is None:
        state = np.full((batch, n_genes), ORGANELLE, dtype=np.int8)
    else:
        state = np.broadcast_to(initial_states, (batch, n_genes)).astype(np.int8)

    dt = horizon / n_steps
    counts = np.empty((batch, n_steps + 1, 3), dtype=np.int32)
    snapshots = {}

    def record(step):
        for s in range(3):
            counts[:, step, s] = (state == s).sum(1)
        if step in snapshot_steps:
            snapshots[step] = state.copy()

    record(0)
    for step in range(1, n_steps + 1):
        lost_frac = ((state == LOST) @ membership) / pathway_size
        k_loss = k_loss_base * (1.0 + coupling * lost_frac[:, genome.pathway])
        k_total = k_transfer + k_loss
        p_event = -np.expm1(-k_total * dt)
        u = rng.random((batch, n_genes))
        event = (state == ORGANELLE) & (u < p_event)
        # Reuse u: conditional on an event, u/p_event is uniform, so this picks
        # transfer with probability k_transfer / k_total.
        transfer = event & (u < p_event * k_transfer / k_total)
        state[transfer] = NUCLEUS
        state[event & ~transfer] = LOST
        record(step)

    return SimResult(states=state, counts=counts, snapshots=snapshots)
