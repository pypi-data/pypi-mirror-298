from obstechutils.types import TypeAlias, TimeDeltaType, TimeType
from obstechutils.regression import RunningLinearRegression
from obstechutils.dataclasses import autoconverted, dataclass

from astropy.time import Time, TimeDelta
from pydantic import validate_call, BaseModel, Field, PositiveFloat
import numpy as np
from typing import Iterator

MeasurementSet: TypeAlias = dict[str, float]
SensorSet: TypeAlias = dict[str, RunningLinearRegression]
ArrayType = autoconverted(np.ndarray, converter_function=np.array)
MaskedArrayType = autoconverted(np.ma.masked_array)

_dataclass_config = dict(
        validate_assignment=True, 
        validate_default=True, 
        extra='forbid'
)

@dataclass(config=_dataclass_config)
class SensorFuser:
    """Fuse data from sensors of unknown noise.  

The noise of each sensor is estimated by assuming the quantity locally
follows a linear function of time and uses an unbiased estimate of the
variance of y_i - (a t_i + b). Older data can be phased out progressively
with a dampening timescale.

The fusion uses a Kálmán filtre with a scalar state.

Missing or new data are automatically dealt with.

MANDATORY KEYWORD ARGUMENTS

    min_data_dev [float]:
        Ensure that deduced or assumed data standard deviations are at 
        least equal to min_data_dev.  It is useful for discrete data
        values where small deviations are rounded to zero.

    max_data_dev [float]:
        Maximum data deviation.  If measured variance is higher, it's assume
        some of it is made of real, short-scale variations rather than sensor
        noise. 

    process_dev [float]:
        Typical deviation of state prediction from real value

OPTIONAL KEYWORD ARGUMENTS

    dampening_timescale [TimeDelta or None, default None]:
        Dampening time for the calculation of sensor noise.  Weight
        is exp(-t / dampening_time) if specified, otherwise no dampening
        occurs.

ADD MEASUREMENT SET AND DETERMINE FUSED VALUE

    __call__

        A call of the fuser adds a data point and computes the fused value.

        Arguments
            
            m [dict[str, float]]

                The argument of the call is a dictionary associating 
                floating point values to sensor ids.  NaN or inf value 
                will be considered as zero weight data.

            t [Time, default current]

                Time (Time object) or time ellapsed since last measurement
                (TimeDelta object or float in seconds)

        Return value [float]

            Estimated value

    add_measurement_set

        Same as __call__ but does not return the fused value.

READ-ONLY PROPERTIES

    value [float]
        Estimated value for the quantity

    error [float]
        Uncertainty on the quantity

    sensor_ids [list[str]]
        All sensor ids received.

    sensor_values [list[float]]
        Last values of the sensors.  

    sensor_errors [list[float]]
        Standard deviation of sensor values with respect to the current 
        trend

    sensors [iterable [str, float]]
        Return an iterable on pairs of sensor id and sensor value

    time [Time]
        Time of last measurement

    time_ellapsed [TimeDelta]
        Time ellapsed since first measurement

EXAMPLE USE

    temp_mixer = SensorFuser(
        dampening_time='15min',  
        min_data_std=0.05, # data is given with 1 decimal digit 
        process_std=0.1,   # dev. from linear law of 0.1⁰C between points 
    )
    while True:
        time.sleep(15)
        t1, t2, t3 = get_sensor1(), get_sensor2(), get_sensor3()
        t = dict(sensor1=t1, sensor2=t2, sensor3=t3)
        t_mean = mixer(t)   
        # alternatively
        # t_mean = mixer.add_measurement_set(t) 
        t_error = mixer.error
        ...

MAIN HYPOTHESES

    * All sensors measure the same quantity.
    * The sensors feature mainly Gaussian noise.
    * The quantity varies smoothly with time.
    * The noise of each sensor varies smoothly with time.
    
    """
    process_dev: PositiveFloat 
    min_data_dev: PositiveFloat 
    max_data_dev: PositiveFloat
    dampening_timescale: TimeDeltaType | None = None

    # internal state
    _sensors: SensorSet = Field(default_factory=lambda: {}, repr=False, init=0)
    _R: ArrayType = Field(default_factory=lambda: [], repr=False, init=0)
    _z: ArrayType = Field(default_factory=lambda: [], repr=False, init=0)
    _P: float | None = Field(default=None, repr=False, init=0)
    _x: float | None = Field(default=None, repr=False, init=0)
    _start_time: float = Field(default=0, repr=False, init=0)
    _time: float = Field(default=0, repr=False, init=0)

    @property
    def value(self) -> float:
        return self._x

    @property
    def error(self) -> float:
        return self._P ** .5

    @property
    def time(self) -> TimeType:
        t = Time(self._start_time + self._time, format='unix')
        t.format = 'iso'
        return t

    @property
    def time_ellapsed(self) -> TimeDeltaType:
        return TimeDelta(self._time, format='sec')

    @property
    def sensor_ids(self) -> list[str]:
        return list(self._sensors)

    @property
    def sensors(self) -> Iterator[tuple[str, float]]:
        for id, val in zip(self.sensor_ids, self.sensor_values):
            yield (id, float(val))

    @property
    def sensor_errors(self) -> ArrayType:
        return np.array(self._R) ** 0.5 

    @property
    def sensor_values(self) -> ArrayType:
        z = np.array(self._z)
        z[self._z.mask] = np.nan
        return z

    def add_measurement_set(
            self, 
            m: MeasurementSet, 
            t: TimeType | TimeDeltaType | None = None
    ) -> None:
        
        # first measurement 

        if self._start_time == 0:
            self._start_time = Time.now().unix
        
        # A new measurement updates the measurement noise matrix using past
        # data.  This steps also indicates how to incorporate a new sensor or
        # deal with missing data.
        
        z = self._add_measurement_set(m, t)
 
        # If there is no previous state, it was the first measurement.
        # State is initialised with mean and variance

        if self._x is None:
            self._x = z.mean()
            self._P = max(self.process_dev ** 2, z.var(ddof=1))
            return self.value

        # The Kálmán filter proper

        self._kalman_step(z)

    @validate_call
    def __call__(
            self, 
            m: MeasurementSet, 
            t: TimeType | TimeDeltaType | None = None
    ) -> float:
        self.add_measurement_set(m, t)
        return self.value

    def _add_measurement_set(
            self, 
            m: MeasurementSet,
            t: Time | TimeDelta | None = None
    ) -> np.ma.masked_array:
   
        # Determine the time of measurement.  If t is float or TimeDelta,
        # assume a time increment

        if t is None:
            t = Time.now()
        if isinstance(t, TimeDelta):
            t = t.sec
        
        t = t.unix - self._start_time if isinstance(t, Time) else self._time + t

        assert t > self._time, 'time must be increasing'
        self._time = t

        # If new, unpreviously used sensors appear, add them

        sensors = self._sensors

        new_sensors = set(m) - set(sensors)
        for sensor in new_sensors:
            sensors[sensor] = RunningLinearRegression(
                weight_dampening_scale=self.dampening_timescale.sec,
                fit_invalid=True,
            )
        
        # Pass measurement values to each sensor running linear regression,
        # with missing value as NaN.

        z = [m.get(sensor_id, np.nan) for sensor_id in sensors]
        self._z = np.ma.masked_invalid(z)

        for sensor_id, zi in zip(sensors, z):
            sensors[sensor_id].add_point(self._time, zi)

        # Variances.  Attribue to invalid variances the mean of the valid
        # ones, if not possible, use the default minimum variance. 

        R = np.array([fit.y_var for fit in sensors.values()])
        R_ok = np.isfinite(R)
        rmin = self.min_data_dev ** 2
        rmax = self.max_data_dev ** 2
        if not any(R_ok):
            R[:] = rmin
        else:
            R[~R_ok] = R[R_ok].mean() 
        R = np.minimum(np.maximum(R, rmin), rmax)

        self._R = R

        # We yield measurement value, not fitted ones. The running fits
        # are only used to estimate variances for the Kálmán filtre.

        return self._z

    def _kalman_step(self, z: np.ma.masked_array) -> None:
        
        # Prediction state and variance

        xp = self._x
        Q = self.process_dev ** 2
        Pp = self._P + Q

        # Innovation 

        y = z - xp
        y[z.mask] = 0

        # Innovation covariance matrix. 
        #
        # From a numerical point of view, setting the invalid / missing points'
        # variances to infinity is problematic, since we need a matrix inverse
        # at some point.
        #
        # Instead, I use the Sherman-Morrison formula to invert
        #
        # S = R + Ht.Pp.Ht 
        #   = R + Pp uv      where u=[1, ..., 1] and v = u.T   
        #
        # as
        #
        #   S⁻¹ = R⁻¹ - Pn R⁻¹ uv R⁻¹  / (1 + Pn v R⁻¹ u)
        # 
        # which for diagonal R reduces to
        #
        #       = R⁻¹ - Pp diag(R⁻¹) x diag(R⁻¹) / (1 + Pp tr(R⁻¹))
        #
        # Invalid/missind data are set to 0 in the diag(R⁻¹).

        Ri_diag = ~z.mask / self._R 
        Ri = np.diag(Ri_diag)
        Si = Ri - Pp * np.outer(Ri_diag, Ri_diag) / (1 + Pp * Ri_diag.sum())

        # Optimal Kálmán gain. 

        K = Pp * Si.sum(axis=0)

        # Estimation 

        self._x += (K * y).sum()
        self._P = Pp * (1 - K.sum()) 

        return self._x

