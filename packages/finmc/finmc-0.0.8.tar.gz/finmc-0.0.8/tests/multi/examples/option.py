# Description: Run Heston MC model with a vanilla option contract.

from tests.multi.dataset import data_three_asset
from tests.multi.tests.test_basket import _basket_price_mc


def run_model():
    """Price a vanilla option with the Heston MC model."""

    model_cls, dataset, other = data_three_asset()
    model = model_cls(dataset)
    spots = other["spots"]
    price = _basket_price_mc(model, maturity=1.0, strike=1.0, spots=spots)

    return price


if __name__ == "__main__":
    price = run_model()
    print(f"price = {price}")
