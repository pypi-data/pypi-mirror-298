# Description: datasets for the Heston model.

from finmc.models.multi import BSMC
from finmc.utils.assets import flat_discount, flat_fwds
import numpy as np


def data_three_asset():
    """Define a three asset dataset."""
    spots = {
        "NVDA": 116.00,
        "INTC": 21.84,
    }
    rate = 0.03

    # Asset forwards and discount curve
    assets = {k: flat_fwds(v, rate, 0.0, 3.0) for k, v in spots.items()}
    assets["USD"] = flat_discount(rate, 3.0)

    # Covariance matrix
    cov = np.array(
        [
            [0.09, 0.03],
            [0.03, 0.04],
        ]
    )

    # Complete dataset
    dataset = {
        "MC": {
            "PATHS": 100_000,
            "TIMESTEP": 1 / 10,
            "SEED": 1,
        },
        "BASE": "USD",
        "ASSETS": assets,
        "BSM": {
            "ASSETS": list(spots.keys()),
            "COV": cov,
        },
    }

    return (
        BSMC,
        dataset,
        {"spots": spots, "rate": rate},
    )
