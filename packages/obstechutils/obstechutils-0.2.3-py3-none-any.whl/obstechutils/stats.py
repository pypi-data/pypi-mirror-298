from obstechutils.types import Vector, TypeAlias
from obstechutils.dataclasses import strictdataclass, Field
from typing import Callable

import numpy as np
import scipy as sp

MeasurementType: TypeAlias = dict[str, float]

def trimmed_mean(x: Vector, axis: int = 0) -> float:
    """Trimmed mean keeping about half of the points"""

    if len(x) < 4:
        return np.median(x, axis=axis)

    # Of N = 15 measurements average the middle 7
    # If mesaurements errors are independant normal, the resulting
    # error is ~1.1 sigma_x / sqrt(N)
    return sp.stats.trim_mean(x, 0.27, axis=axis)

def average(
    x: Vector,
    is_angle: bool = False,
    averaging_fun: Callable = np.mean
) -> float:
    """Average function able to deal with angles"""
    if is_angle:
        x = np.deg2rad(x)
        x = np.array([np.cos(x), np.sin(x)])

    x = averaging_fun(x, axis=-1)

    if is_angle:
        x = np.rad2deg(np.arctan2(x[0], x[1]))

    return x

@strictdataclass
class MeasurementBinner:
    """Bin measurments from a list of dictionaries

Arguments:

    average_type [str]:  
        Either mean or median or trimmed_mean 
    angle_variables [list[str]]:
        These variables will be averaged more carefully 
    max [list[str]]:
        These variables will be given a maximum value too
    min [list[str]]:
        Same as maximum_variables.

    """
    average_type: str = 'trimmed_mean'
    angles: list[str] = Field(default_factory=lambda: [])
    max: list[str] = Field(default_factory=lambda: [])
    min: list[str] = Field(default_factory=lambda: [])

    def __call__(self, measurements: list[MeasurementType]) -> MeasurementType:

        measurements = [m for m in measurements if m]
        measurement = {}

        if self.average_type == 'mean':
            mean = np.mean
            std = np.std
        elif self.average_type == 'median':
            mean = np.median
            std = np.std
        else:
            mean = trimmed_mean
            std = np.std

        keys = np.unique(np.hstack([list(m.keys()) for m in measurements]))
        for key in keys:

            values = [v for m in measurements
                            if (v := m.get(key, None)) is not None]
                
            value = None
            if values:
                is_angle = key in self.angles
                value = average(values, is_angle=is_angle, averaging_fun=mean)
            measurement[key] = value

            if key in self.max:
                value = np.max(values)
                max_var = f'{key}_max'
                measurement[max_var] = value

            if key in self.min:
                value = np.min(values)
                max_var = f'{key}_min'
                measurment[min_var] = value

        return measurement

