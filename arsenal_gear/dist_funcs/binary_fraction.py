"""
binary_fraction
==========

This submodule contains all the code required to sample from a mass-dependent binary fraction.
"""

from typing import Type

import astropy.units as u
import numpy as np
from astropy.units import Quantity
from scipy.stats import rv_continuous, rv_histogram

from arsenal_gear.population import StarPopulation

class BinaryFraction:
    """
    This class is the superclass of all mass-dependent binary fraction
    This assumes that the binary fraction is a step function

    :param fraction: Binary fraction of the mass bins, of length k
    :type fraction: float
    :param mass_bins: Limit of the mass bins, of length k-1
    :type mass_bins: astropy mass unit
    :param stars: Potential primaries
    :type stars: StarPopulation
    """
    def __init__(self, fraction: float, mass_bins: Quantity["mass"], stars: StarPopulation, name=""):
        self.fraction:  float = fraction
        self.mass_bins: float = mass_bins.to(u.Msun).value
        self.stars:     float = stars["mass"].to(u.Msun).value
        assert(np.min(self.fraction) >= 0)
        assert(np.max(self.fraction) <= 1)
        assert(np.min(self.mass_bins) >= 0)
        #assert(len(self.fraction)-len(self.mass_bins) == 1)
        #super().__init__(a=self.fraction, b=self.mass_bins, c=self.stars, name=name)

    
class Step(BinaryFraction):
    """
    A simple step function binary fraction, with a binary fraction
    of 0 below the changeover mass and 1 above the changeover mass

    :param mass: Changeover mass between binary fractions of 0 and 1
    :type mass: astropy mass unit
    """
    def __init__(self, fraction: float, mass_bins: Quantity["mass"], stars: StarPopulation):
        self.name = "Step"
        assert(len(fraction) == 2)
        super().__init__(fraction, mass_bins, stars, name=self.name)

    def binary_fraction(self) -> np.float64:
        prob = np.piecewise(self.stars, [self.stars < self.mass_bins, self.stars >= self.mass_bins], self.fraction)
        return prob
    
    def sample(self) -> bool:
        """
        Determine which stars are primaries

        :return: Boolean array
        :rtype: bool
        """
        _sample = np.random.rand(len(self.stars))
        _binary = np.zeros(len(self.stars), dtype=bool)
        _select = np.where(_sample <= self.binary_fraction())
        _binary[_select] = np.ones(len(_select), dtype=bool)
        return _binary

    


