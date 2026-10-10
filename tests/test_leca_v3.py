import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

from leca_v3_model import em_prior  # noqa: E402


def test_em_recovers_mixture_weights():
    rng = np.random.default_rng(0)
    # three grid points; families generated from point 0 (70%) and point 2 (30%), well separated
    true = rng.choice([0, 2], size=4000, p=[0.7, 0.3])
    ll = np.full((3, 4000), -50.0)
    ll[true, np.arange(4000)] = 0.0
    ll[1] = -3.0
    w, R, marg = em_prior(ll)
    assert abs(w[0] - 0.7) < 0.03 and abs(w[2] - 0.3) < 0.03 and w[1] < 0.02
    assert np.allclose(R.sum(0), 1.0)
