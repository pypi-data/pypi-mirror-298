# finmc

[![CI](https://github.com/finlib/finmc/actions/workflows/main.yml/badge.svg)](https://github.com/finlib/finmc/actions/workflows/main.yml)

This package contains Monte-Carlo implementations of many financial models derived from a common interface class. This interface allows for

 - [Shared utilities](https://finlib.github.io/finmc/utilities/) that can be used for all models for tasks such as calculating implied vol surface.
 - [Price Calculators](https://finlib.github.io/finmc/calculators/) that are model invariant.
 - High performance, even with a large number of paths.
 - [New models](https://finlib.github.io/finmc/models/api/#mc-models-in-other-repos) can be created outside this repositary, by indepedent contributors, and yet be compatible with above utilities and calculators.

## Documentation

- [Home](https://finlib.github.io/finmc/)
- [Models](https://finlib.github.io/finmc/models/localvol)

## Notebooks
<table>
<tr>
    <td> 
    <a href="https://github.com/finlib/finmc/blob/main/notebooks/hullwhite.ipynb">
    <img src="https://finlib.github.io/finmc/images/blank_mc.png"/>
    </td>
    <td>
    <a href="https://github.com/finlib/finmc/blob/main/notebooks/heston.ipynb">
    <img src="https://finlib.github.io/finmc/images/heston_vol_mc.png" alt="forward collar"/>
    </td>
</tr>
<tr>
    <td> Hull-White with a term structure of rates.</td>
    <td> Paths of Variance in Heston Model.</td>
</tr>
</table>

[All Notebooks](https://github.com/finlib/finmc/tree/main/notebooks)

## Install it from PyPI

```bash
pip install finmc
```

### Example
This is an example of pricing a vanilla option using the local volatility model.

```py
import numpy as np
from finmc.models.localvol import LVMC
from finmc.calc.option import opt_price_mc

# Define Dataset with zero rate curve, and forward curve.
dataset = {
    "MC": {"PATHS": 100_000, "TIMESTEP": 1 / 250},
    "BASE": "USD",
    "ASSETS": {
        "USD":("ZERO_RATES", np.array([[2.0, 0.05]])),
        "SPX": ("FORWARD", np.array([[0.0, 5500], [1.0, 5600]])),
        },
    "LV": {"ASSET": "SPX", "VOL": 0.3},
}

model = LVMC(dataset)
price = opt_price_mc(5500.0, 1.0, "Call", "SPX", model)
```
