"""AI part 2: infer a lineage's hidden evolutionary history from its genome.

Amortised simulation-based inference (neural posterior estimation): simulate many
lineages from the prior, then train a network that maps an observed end-state genome
to a Gaussian posterior over (log_transfer, log_loss, coupling). Once trained,
inference on a new organelle genome is a single forward pass.
"""

from dataclasses import dataclass

import numpy as np
import torch
from torch import nn

from .ancestor import AncestorGenome
from .simulator import LOST, NUCLEUS, PARAM_NAMES, Rules, sample_prior, simulate


def encode_states(states: np.ndarray) -> torch.Tensor:
    """(B, G) states -> (B, 2G) indicators for 'in nucleus' and 'lost'."""
    states = np.atleast_2d(states)
    return torch.as_tensor(
        np.concatenate([states == NUCLEUS, states == LOST], axis=1), dtype=torch.float32
    )


class PosteriorNet(nn.Module):
    def __init__(self, n_inputs: int, n_params: int, hidden: int = 256):
        super().__init__()
        self.body = nn.Sequential(
            nn.Linear(n_inputs, hidden),
            nn.GELU(),
            nn.Dropout(0.1),
            nn.Linear(hidden, hidden // 2),
            nn.GELU(),
            nn.Linear(hidden // 2, 2 * n_params),
        )

    def forward(self, x):
        mean, log_std = self.body(x).chunk(2, dim=-1)
        return mean, log_std.clamp(-6, 3)


@dataclass
class Posterior:
    mean: np.ndarray  # (B, P)
    std: np.ndarray  # (B, P)

    def sample(self, n: int, rng: np.random.Generator) -> np.ndarray:
        """(n, P) samples for a single observation (B must be 1)."""
        return rng.normal(self.mean[0], self.std[0], size=(n, len(self.mean[0])))


class EvolutionInferrer:
    def __init__(self, genome: AncestorGenome, rules: Rules, prior_low, prior_high):
        self.genome = genome
        self.rules = rules
        self.low = np.asarray(prior_low, dtype=float)
        self.high = np.asarray(prior_high, dtype=float)
        self.net = PosteriorNet(2 * genome.n_genes, len(PARAM_NAMES))

    def simulate_dataset(self, n: int, rng: np.random.Generator, chunk: int = 2000):
        params, states = [], []
        for start in range(0, n, chunk):
            p = sample_prior(min(chunk, n - start), rng, self.low, self.high)
            states.append(simulate(self.genome, self.rules, p, rng=rng).states)
            params.append(p)
        return np.concatenate(params), np.concatenate(states)

    def _scale(self, params):
        return (params - self.low) / (self.high - self.low)

    def train(
        self,
        n_sims: int = 20000,
        epochs: int = 60,
        batch_size: int = 256,
        lr: float = 1e-3,
        seed: int = 0,
        verbose: bool = False,
    ) -> list[float]:
        rng = np.random.default_rng(seed)
        torch.manual_seed(seed)
        params, states = self.simulate_dataset(n_sims, rng)
        x = encode_states(states)
        y = torch.as_tensor(self._scale(params), dtype=torch.float32)
        n_val = max(1, n_sims // 10)
        x_val, y_val, x_tr, y_tr = x[:n_val], y[:n_val], x[n_val:], y[n_val:]

        opt = torch.optim.AdamW(self.net.parameters(), lr=lr, weight_decay=1e-4)
        sched = torch.optim.lr_scheduler.CosineAnnealingLR(opt, epochs)
        val_history, best, best_state = [], np.inf, None
        for epoch in range(epochs):
            self.net.train()
            perm = torch.randperm(len(x_tr))
            for i in range(0, len(perm), batch_size):
                idx = perm[i : i + batch_size]
                opt.zero_grad()
                self._nll(x_tr[idx], y_tr[idx]).backward()
                opt.step()
            sched.step()
            self.net.eval()
            with torch.no_grad():
                val = float(self._nll(x_val, y_val))
            val_history.append(val)
            if val < best:
                best, best_state = val, {k: v.clone() for k, v in self.net.state_dict().items()}
            if verbose:
                print(f"  epoch {epoch + 1:3d}  val NLL {val:.3f}")
        self.net.load_state_dict(best_state)
        return val_history

    def _nll(self, x, y):
        mean, log_std = self.net(x)
        return (log_std + 0.5 * ((y - mean) / log_std.exp()).square()).sum(-1).mean()

    @torch.no_grad()
    def infer(self, states: np.ndarray) -> Posterior:
        self.net.eval()
        mean, log_std = self.net(encode_states(states))
        span = self.high - self.low
        return Posterior(
            mean=mean.numpy() * span + self.low,
            std=log_std.exp().numpy() * span,
        )
