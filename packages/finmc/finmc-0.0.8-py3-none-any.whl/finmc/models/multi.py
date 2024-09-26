import numpy as np
from finmc.models.base import MCFixedStep
from finmc.utils.assets import Discounter, Forwards
from numpy.random import SFC64, Generator


class BSMC(MCFixedStep):
    """Class for the multi asset Black Scholes model."""

    def reset(self):
        """Fetch any information from the dataset or timetable, that needs to be stored into self,
        to facilitate the 'advance' method to run as quickly as possible."""
        # common MC parameters
        self.n = self.dataset["MC"]["PATHS"]
        self.timestep = self.dataset["MC"]["TIMESTEP"]

        # fetch the model parameters from the dataset
        modeldata = self.dataset["BSM"]
        self.cov = modeldata["COV"]

        # Create a dictionary of assets, so that we can easily access the idx and spot from string name.
        # Also create ordered lists of forwards and variances for the assets.
        self.assets = {}
        self.fwds = []
        self.vars = []
        for idx, asset in enumerate(modeldata["ASSETS"]):
            fwd = Forwards(self.dataset["ASSETS"][asset])
            self.assets[asset] = {"idx": idx, "spot": fwd.forward(0)}
            self.fwds.append(fwd)
            self.vars.append(self.cov[idx][idx])

        self.discounter = Discounter(
            self.dataset["ASSETS"][self.dataset["BASE"]]
        )

        # Initialize the RNG and the x_vec (log process for each asset)

        self.rng = Generator(SFC64(self.dataset["MC"]["SEED"]))
        self.x_vec = np.zeros((len(self.assets), self.n))

        self.cur_time = 0

    def step(self, new_time):
        """Update x_vec in place when we move simulation by time dt."""

        dt = new_time - self.cur_time

        drifts = np.array(
            [fwd.rate(new_time, self.cur_time) for fwd in self.fwds]
        )
        drifts -= np.array(self.vars) / 2.0

        # generate the random numbers and advance the log stock process
        dz = self.rng.multivariate_normal(
            drifts * dt, self.cov * dt, self.n
        ).transpose()

        self.x_vec += dz

        self.cur_time = new_time

    def get_value(self, unit):
        """If this asset is part of the model, return its value using the simulated array.
        For any other asset that may exist in the timetable, return the default implementation in qablet base model.
        """

        info = self.assets.get(unit)
        if info:
            return info["spot"] * np.exp(self.x_vec[info["idx"]])

    def get_df(self):
        return self.discounter.discount(self.cur_time)
