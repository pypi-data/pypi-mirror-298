from pydantic import validate_call
from abc import ABC, abstractmethod
import numpy as np

from collections import namedtuple

RegionOfInterest = namedtuple(
    'RegionOfInterest',
    ['x0', 'y0', 'width', 'height']
)
Subwindow = namedtuple(
    'Subwindow',
    ['x0', 'y0', 'x1', 'y1']
)

class Camera(ABC):
    
    @classmethod
    def brand(cls) -> str: 
        return cls.__name__.removeprefix('Camera').lower()
    
    @property
    @abstractmethod
    def capture(self) -> np.ndarray: ...

    @property
    @abstractmethod
    def gain(self) -> float: ...

    @property
    @abstractmethod
    def offset(self) -> int: ... 

    @property
    @abstractmethod
    def exposure(self) -> float: ... 
    
    @property
    def temperature(self) -> float: 
        raise NotImplementedError()
    
    @property
    @abstractmethod
    def video(self) -> bool: ...

    @property
    @abstractmethod
    def bin(self) -> tuple[int, int]: ...

    @property
    @abstractmethod
    def image_type(self) -> str: ...
    
    @property
    @abstractmethod
    def mode(self) -> str: ...

    @property
    @abstractmethod
    def width(self) -> int: ...
    
    @property
    @abstractmethod
    def height(self) -> int: ...

    @property
    @abstractmethod
    def start_x(self) -> int: ...

    @property
    @abstractmethod
    def end_x(self) -> int: ...

    @property
    @abstractmethod
    def start_y(self) -> int: ...

    @property
    @abstractmethod
    def end_y(self) -> int: ...

    @property
    @abstractmethod
    def roi(self) -> int: ...


def get_control_properties(
        name: str, 
        value_type: type, 
        factor: float = 1,
        auto: bool = True
) -> dict[str, property]:

    properties = {}
    
    # control available
    def supported(self) -> bool:
        return self._is_control_supported(name)
    properties[f'{name}_supported'] = property(supported)

    # getter and setter for property
    def writable(self) -> bool:
        return self._is_control_writable(name)
    @validate_call(validate_return=True)
    def getter(self) -> value_type:
        return value_type(self._get_control_value(name) * factor)
    @validate_call
    def setter(self, value: value_type) -> None:
        self._set_control_value(name, int(value / factor))
    properties[name] = property(getter, setter)
    properties[f'{name}_settable'] = property(writable)

    # min and max
    if value_type is not bool:
        def minval(self) -> value_type:
            return value_type(self._get_control_min(name) * factor)
        def maxval(self) -> value_type:
            return value_type(self._get_control_max(name) * factor)
        def range(self) -> tuple[value_type, value_type]:
            return minval(self), maxval(self)
        properties[f'min_{name}'] = property(minval)
        properties[f'max_{name}'] = property(maxval)
        properties[f'{name}_range'] = property(range)

    # auto
    if auto:
        def supported(self) -> bool:
            return self._is_control_auto_supported(name)
        def getter(self) -> bool:
            return self._get_control_auto(name)
        @validate_call
        def setter(self, value: bool) -> None:
            return self._set_control_auto(name, value)
        properties[f'{name}_auto'] = property(getter, setter)
        properties[f'{name}_auto_supported'] = property(supported)

    return properties
 
ControlListType: type = list[tuple[str, type, float, bool]]

def controls_to_properties(controls: ControlListType):
    
    def wrap(cls):
        defined_methods = set()
        for control in controls:
            properties = get_control_properties(*control)
            for name, method in properties.items():
                setattr(cls, name, method)
                defined_methods.add(name)
        if issubclass(cls, ABC):
            cls.__abstractmethods__ = cls.__abstractmethods__ - defined_methods
        return cls

    return wrap
