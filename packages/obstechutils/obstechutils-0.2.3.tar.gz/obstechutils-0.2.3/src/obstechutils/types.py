from obstechutils.dataclasses import autoconverted, Field

from astropy import time as _time, coordinates as _coordinates
from typing_extensions import Annotated as _Annotated
import queue as _queue
import numpy as _np
from typing import Union as _Union
import threading as _threading

def _timedelta_convert(x) -> _time.TimeDelta:
    format = None if isinstance(x, str) else 'sec'
    return _time.TimeDelta(x, format=format)
        

TimeType = autoconverted(_time.Time)
TimeDeltaType = autoconverted(
    _time.TimeDelta,
    converter_function=_timedelta_convert
)
PortType = _Annotated[int, Field(ge=0, lt=65535)]
QOSType = _Annotated[int, Field(ge=0, le=2)]
EarthLocationType = autoconverted(_coordinates.EarthLocation)
SkyCoordType = autoconverted(_coordinates.SkyCoord)
QueueType = autoconverted(_queue.Queue)
LockType = autoconverted(type(_threading.Lock()))

try:
    from typing import TypeAlias
except:
    TypeAlias = type

Vector: TypeAlias = _Union[list[float], _np.ndarray]
VectorOrScalar: TypeAlias = _Union[float, list[float], _np.ndarray]
