# Description: Tests for the multi asset black scholes model for vanilla options.

import pytest
from pytest import approx

from finmc.utils.assets import Discounter, Forwards
from tests.multi.dataset import data_three_asset
import numpy as np
from finmc.utils.bs import opt_price


def _basket_price_mc(model, maturity, strike, spots):
    """Calculate the price of a equal weight basket call option using simulation."""
    model.reset()
    model.advance(maturity)
    pay = -strike
    for asset_name, spot in spots.items():
        pay += 0.5 * model.get_value(asset_name) / spot

    df = model.get_df()
    price = np.maximum(pay, 0.0).mean() * df
    return price


def _basket_price_bs(dataset, maturity, strike, spots):
    """Calculate the price of a equal weight basket call option using closed form."""
    ccy = dataset["BASE"]
    discounter = Discounter(dataset["ASSETS"][ccy])
    df = discounter.discount(maturity)

    F = 0.0
    for asset_name, spot in spots.items():
        asset_fwds = Forwards(dataset["ASSETS"][asset_name])
        Fi = asset_fwds.forward(maturity)
        F += 0.5 * Fi / spot

    sigma = np.sqrt(dataset["BSM"]["COV"].sum()) / 2.0
    expected, _ = opt_price(
        strike,
        maturity,
        "Call",
        F=F,
        df=df,
        sigma=sigma,
    )
    return expected


@pytest.fixture(scope="module")
def data():
    return data_three_asset()


@pytest.mark.parametrize("maturity", [0.1, 2.0])
@pytest.mark.parametrize("strike", [0.01, 0.95, 1.00, 1.05, 1.2])
def test_call(data, maturity, strike):
    """Test the price of a basket call option."""

    model_cls, dataset, other = data
    spots = other["spots"]

    model = model_cls(dataset)

    # Calculate (two asset) basket price using MC
    price = _basket_price_mc(model, maturity, strike, spots)

    # Calculate (two asset) basket price using BS
    expected = _basket_price_bs(dataset, maturity, strike, spots)

    error = price - expected
    contract = f"Call {maturity:4.2f} {strike:6.2f}"
    assert error == approx(0.0, abs=1e-3)
    print(f"{contract}: {price:11.6f} {expected:11.6f} {error * 1e4:7.2f}")


if __name__ == "__main__":
    pytest.main([__file__])
