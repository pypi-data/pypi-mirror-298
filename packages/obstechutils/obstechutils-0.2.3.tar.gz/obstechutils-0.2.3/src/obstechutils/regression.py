from obstechutils import dataclasses as _dc

from pydantic import (BaseModel as _BaseModel, validate_call as _validate_call,
                      PositiveFloat, NonNegativeFloat, NonNegativeInt,
                      ConfigDict as _ConfigDict) 
import numpy as _np

NumpyArray = _dc.autoconverted(_np.ndarray)

class _StrictModel(_BaseModel, 
    extra='forbid', 
    validate_default=True,
    validate_assignment=True, 
):
    ...

class RunningLinearRegression(_StrictModel):
    """Running weighted linear regression 

Yield a linear regression at each new data point (x_n, y_n +/ dy_n) of
a data series.

If a weight dampening scale is given, the linear regression is local and
weights of data x_i (i < n) are decreased by a factor
    exp ( -(x_i - x_n) / weight_dampening_scale)
In that case, x_i must be increasing.

The data series is not kept and the computation is incremental.

ARGUMENTS

    weight_dampening_scale [float]
        Decrease weights of distant data by exp dx / -weight_dampening_scale
        to obtain a local linear regression.  If not specified, no decrease
        in weights ocurrs and the fit is global.

    fit_invalid [bool]
        If fit_invalid is True, the fit will be made for the current data
        point even if it's invalid (either NaN or weight = 0).  Otherwise
        properties will return NaN 

PROPERTIES

    slope [float]
        Slope

    slope_std [float]
        Standard deviation of the slope, in the case weights have been scaled
        to match data uncertainities.

    intercept [float]
        Intercept
    
    intercept_std [float]
        Standard deviation of the intercept, in the case weights have been 
        scaled to match data uncertainities.

    y_fit [float]
        Fitted value for last point 

    y_std [float]
        Standard deviation of data from the fit
    
    y_var [float]
        Data variance

    ndata [int]
        Number of valid data points (NaN and zero weight points excluded)

    nfree [float]
        Effective number of degrees of freedom

METHODS
    
    add_point(x, y, dy=1)
        Add a point to the the regression

EXAMPLE USE

    lr = RunningLinearRegression
    while point := get_data(): 
        lr.add_point(*point)
        print(f"{lr.slope=:.4f} {lr.intercept=:.4f} {lr.y_std=:.4f}")
    print(f"{lr.ndata}")

    """
    weight_dampening_scale: PositiveFloat | None = None
    fit_invalid: bool = False
 
    _invalid: bool = False
    _M: NumpyArray = _np.zeros((3,3))
    _M2: NumpyArray = _np.zeros((3,1))
    _a: float = _np.nan
    _avar: float = _np.nan
    _b: float = _np.nan
    _bvar: float = _np.nan
    _abcov: float = _np.nan
    _var: NonNegativeFloat = _np.nan
    _x: float = _np.nan
    _ndata: NonNegativeInt = 0
    _nfree: NonNegativeFloat = 0 
    _fit_done: bool = False

    @property
    def slope(self) -> float: 
        self._fit()
        return self._a

    @property
    def intercept(self) -> float: 
        self._fit()
        return self._b - self._a * self._x 

    @property
    def slope_std(self) -> float:
        self._fit()
        return self._avar ** 0.5

    @property
    def intercept_std(self) -> float:
        self._fit()
        var = self._bvar + self._avar * self._x**2 - 2 * self._x * self._abcov
        return var ** .5

    @property
    def y_fit(self) -> float: 
        self._fit()
        return self._b

    @property
    def y_std(self) -> NonNegativeFloat: 
        self._fit()
        return self._var ** 0.5 
    
    @property
    def y_var(self) -> NonNegativeFloat: 
        self._fit()
        return self._var 

    @property
    def ndata(self) -> NonNegativeInt: 
        return self._ndata

    @property
    def nfree(self) -> float:
        # return self._ndata - 2
        return self._nfree

    @_validate_call
    def add_point(self, x: float, y: float, dy: NonNegativeFloat = 1) -> None:
       
        # Fit will only be performed when a parameter is asked for, this
        # function leaves the fit undone.
        self._fit_done = False

        # All fitted quantities can be expressed using the following
        # moments of the data.  They can be updated at each new data point
        # without keeping registry of the data series.
        #
        # For all quantities
        #   M_ij  = sum_k w_k  x_k^i y_k^j   [i + j <= 2]
        #
        # To debias the variance using the generalised number of degrees
        # of freedom
        #   M2_ij = sum_k w_k² x_k^i y_k^j   [i <= 2, j = 0]

        M = self._M
        M2 = self._M2
        weight = _np.isfinite(y) / dy ** 2
        
        # If there were already values, update the moments to take into
        # account data weight dampening 
        if _np.isfinite(dx := x - self._x):
    
            assert dx > 0, 'data x must be increasing'
 
            # update the weights of past data 
            if tau := self.weight_dampening_scale:
                M *= _np.exp(-dx / tau)
                M2 *= _np.exp(-2*dx / tau)

            # Perform the change of variable x' = x - dx, to maintain
            # current x at (0, 0), i.e. all past data negative in case
            # of increasing x.
            #
            # Go by decreasing order!

            M[2,0]  += dx ** 2 * M[0,0]  - 2 * dx * M[1,0]
            M2[2,0] += dx ** 2 * M2[0,0] - 2 * dx * M2[1,0]
            M[1,0]  -= dx * M[0,0]
            M2[1,0] -= dx * M2[0,0]
            M[1,1] -= dx * M[0,1] 

        self._x = x

        self._invalid = weight == 0
        if self._invalid:
            return
       
        # Add the current value to data moments.  The x' = x - dx
        # change of variables ensures x' = 0.
        for l in range(3):
            M[0,l] += weight * y ** l
        M2[0,0] += weight ** 2

        # Number of degrees of freedom
        #
        # The variance estimator 
        #
        #  Sb = <[y - (a x + b)]²>
        #
        #     = Σ w_i [y_i - (a x_i + b)]²
        #
        #                             [Σ w_i (y_i - <y>)(x_i - <x>)]² 
        #     = Σ w_i y_i² - <y>² -   -------------------------------
        #                                   Σ w_i (x_i - <x>)²
        # 
        # is biased and can be shown to be
        #
        #          /               Σ w_i²(x_i - <x>)²  \
        #  ŝ² = σ² | 1 - Σ w_i² -  ------------------  |
        #          \               Σ w_i(x_i - <x>)²   /
        #
        #          /              Σ w²x² + (Σ w²)(Σ wx)² - 2(Σ w²x) Σ wx) \
        #     = σ² | 1 - Σ w_i² - --------------------------------------- |
        #          \                Σ wi xi² - (Σ w x)²                   /
        #
        # when renormalising Σ w_i = 1. We call nfree/ndata the parenthesis
        # as an analogy to the unweighted case where Sb reduces to σ(N-2)/N
        #
        # Sanity check: x_i = -n/2 ... n/2 and w_i = 1/n.
        #
        #  Sb  = σ² [ 1 - 1/n - 1/n ]
        
        self._ndata += 1

        if self.ndata > 2:

            self._delta = M[2,0] * M[0,0] - M[1,0]**2
            self._nfree = self._ndata * (
                1 
                - (
                     M2[0,0]    
                  + (
                        M2[2,0]*M[0,0]**2 
                     - 2*M2[1,0]*M[1,0]*M[0,0] 
                     + M2[0,0]*M[1,0]**2
                    ) / self._delta
                ) / M[0,0] **2
            ) 

    def _fit(self) -> None:

        if self._fit_done:
            return
        self._fit_done = True
        
        M = self._M

        # Determine the fit from past values.  The moments have all the info we
        # need, there is no need to keep timeseries. 
        #
        # Linear fit, slope and intercept
        #
        #       Δ = M20 M00 - M10²
        #
        #       a = <w(z-|z|)(t-|t|)>/<w(t-|t|)>
        #
        #         = (<wzt> - <w>|z||t|) / (<wt²> - <w>|t|²)
        #
        #         = (M11 M00 - N01 M10) / Δ
        #
        #       b = |z| - a|t|
        #
        #         = (M20 M01 - M10 M11) / Δ 
        #
        #                                                                       
        # Mean(z) = b
        #
        #  Var(z) = <w(|z| - z - a(t - |t|)²>
        #         = a² <w(|t| - t)²> - a<w(|t|-t)(|z|-z)> + <w(z-|z|)>
        #         = a²(<wt²> - w|t|²) - 2a(<wzt> - w|z|t|) + <wz²> -<w>|t|² 
        #
        #            M20 M00 - M10²   (M11 M00 - M10 * M01)² 
        #         =  -------------- - -----------------------
        #                M00²               Δ M00²
        #
        # but the latter is biased and correction ndata / nfree must be
        # applied

        if self.nfree <= 0 or not self.fit_invalid and self._invalid:
            self._a = _np.nan
            self._b = _np.nan
            self._avar = _np.nan
            self._bvar = _np.nan
            self._abvar = _np.nan
            self._var = _np.nan
            return
       
        var_corr = self.ndata / self.nfree

        self._a = (M[1,1]*M[0,0] - M[0,1]*M[1,0]) / self._delta
        self._b = (M[2,0]*M[0,1] - M[1,0]*M[1,1]) / self._delta
        self._avar =   M[0, 0] / self._delta / M[0,0] * var_corr
        self._bvar =   M[2, 0] / self._delta / M[0,0] * var_corr
        self._abcov = -M[1, 0] / self._delta / M[0,0] * var_corr
        
        self._var = (
            (M[0,0] * M[0,2] - M[0,1]**2)
          - (M[0,0]*M[1,1] - M[1,0]*M[0,1]) ** 2 / self._delta
        ) / M[0,0]**2 * var_corr
