from __future__ import annotations

def _init_zwolib():
    import ctypes
    global zwolib
    library_file= "C:/Users/I5 Astro Backup/PycharmProjects/dimm/lib/ASICamera2.dll"
    zwolib = ctypes.cdll.LoadLibrary(library_file)
_init_zwolib()

from obstechutils.dataclasses import autoconverted
from obstechutils.cameras.base import Camera, controls_to_properties 
from obstechutils.cameras import cdlltools

from pydantic import validate_call
from pydantic.types import FilePath
import re
import numpy as np

from abc import ABC, abstractclassmethod
import functools

import zwoasi as _zwoasi

# Enumarations

class AsiEnum(cdlltools.Enum):
    module = _zwoasi
    namespace = 'ASI'

class AsiImg(AsiEnum):
    subnamespace = 'IMG'
AsiImgType = autoconverted(AsiImg)

class AsiMode(AsiEnum):
    subnamespace = 'MODE'
AsiModeType = autoconverted(AsiMode)

class AsiBayer(AsiEnum):
    subnamespace = 'BAYER'
AsiBayerType = autoconverted(AsiBayer)

class AsiGuide(AsiEnum):
    subnamespace = 'GUIDE'
AsiGuideType = autoconverted(AsiGuide)

def _camel_to_underscore(value):
    value = re.sub('([^A-Z])(?=[A-Z])', '\\1_', value).lower()
    if value == 'band_width':
        value = 'bandwidth_percentage'
    elif value == 'auto_exp_max_exp_ms':
        value = 'auto_exp_max_exp'
    return value


# this decorator will add properties for the camera controls
# such as gain, exposure, etc.
@controls_to_properties(
    controls=[
        # name of the control           type   factor give_auto_methods
        ('gain',                        float, 1,     True),
        ('auto_exp_max_gain',           float, 1,     False),
        ('offset',                      int,   1,     True),
        ('exposure',                    float, 1e-6,  True),
        ('auto_exp_max_exp',            float, 1e-3,  False),
        ('auto_exp_target_brightness',  float, 1,     False),
        ('flip',                        int,   1,     True),
        ('bandwidth_percentage',        int,   1,     True),
        ('hardware_bin',                bool,  1,     True),
        ('high_speed_mode',             bool,  1,     True),
        ('temperature',                 float, 0.1,   True),
    ],
)    

class AsiCamera(Camera):

    def __repr__(self):

        return f"<AsiCamera {self.name} at {hex(id(self))}>" 

    def __str__(self):

        variables = [f"{k} = {repr(v)}" for k, v in vars(self).items() if k[0] != '_']
        variables = '\n    '.join(variables) 
        return f"AsiCamera\n    {variables}"

    def __init__(self, name):

        self.name = name
        self._dark_frame = None
 
        try:
            index = _zwoasi.list_cameras().index(name)
        except ValueError:
            raise ValueError(f'camera {name} not found') 
        
        self._camera = _zwoasi.Camera(index)
        self._controls = {
            _camel_to_underscore(key): {
                _camel_to_underscore(k): v 
                    for k, v in val.items()
            }
                for key, val in self._camera.get_controls().items()
        }

        for name, value in self._camera.get_camera_property().items():
            name = _camel_to_underscore(name)
            setattr(self, name, value)

        self._image_types = {
            v: k for k, v in vars(_zwoasi).items() 
                if k.startswith('ASI_IMG_')
        }
        self._modes = {
            v: k for k, v in vars(_zwoasi).items()
                if k.startswith('ASI_MODE_')
        }

        # change a few defaults

        self.high_speed_mode = True
        self.bandwidth_percentage = 100

        self._video = False

        # some units
        self.pixel_size /= 1e6

    @property
    def video(self) -> bool:
        return self._video

    @video.setter
    def video(self, v: bool) -> None:
        if v == self._video:
            return
        if v:
            self._camera.start_video_capture()
        else:
            self._camera.stop_video_capture()
        self._video = v

    def capture(self) -> np.ndarray:
        if self._video:
            return self._camera.capture_video_frame()
        return self._camera.capture()
        
    # methods to control routines.  They are called by the automatically
    # generated properties
    def _get_control(self, name: str) -> dict[str, int]:
        try:
            control = self._controls[name]
        except:
            raise AttributeError(f'control {name} is not available')
        return control

    def _get_control_type(self, name: str) -> int:
        control = self._get_control(name)
        return control['control_type']

    def _get_control_min(self, name: str) -> int:
        return self._get_control(name)['min_value']
    
    def _get_control_max(self, name: str) -> int:
        return self._get_control(name)['max_value']

    def _is_control_supported(self, name: str) -> bool:
        return name in self._controls
      
    def _is_control_writable(self, name: str) -> bool:
        return self._get_control(name)['is_writable']

    def _is_control_auto_supported(self, name: str):
        return self._get_control(name)['is_auto_supported']

    def _set_control_auto(self, auto: bool):
        self._set_control_value(value=None, auto=auto)

    def _set_control_value(self, name: str, value: int | None, auto: bool = False):

        control_type = self._get_control_type(name)

        is_writable = self._is_control_writable(name)
        if not is_writable:
            raise ValueError(f'{name} cannot be set')
       
        if value is None:
            value = self._camera.get_control_value(control_type)[0]
 
        min = self._get_control_min(name)
        max = self._get_control_max(name)
        if value < min or value > max:
            raise ValueError(f'{name} should be between {min} and {max}')
        
        self._camera.set_control_value(control_type, value, auto=auto)
    
    def _get_control_value(self, name: str) -> int:

        control_type = self._get_control_type(name)
        return self._camera.get_control_value(control_type)[0]
    
    def _get_control_auto(self, name: str) -> int:

        control_type = self._get_control_type(name) 
        return self._camera.get_control_value(control_type)[1]
    
    # Image type

    @property
    @validate_call(validate_return=True)
    def image_type(self) -> AsiImgType:
        return self._camera.get_image_type()

    @image_type.setter
    @validate_call
    def image_type(self, imgtype: AsiImgType) -> None:
        return self._camera.set_image_type(imgtype)
    
    # Camera mode

    @property
    @validate_call(validate_return=True)
    def mode(self) -> AsiModeType:
        return self._camera.get_camera_mode()

    @mode.setter
    @validate_call
    def mode(self, mode: AsiModeType) -> None:
        return self._camera.set_camera_mode(mode)

    # Binning

    @property
    def bin(self) -> tuple[int, int]:
        b = self._camera.get_roi_format()[2]
        return (b, b)

    @bin.setter
    def bin(self, b: tuple[int, int]) -> None:
        if b[0] != b[1]:
            raise ValueError(f'Camera does not accept {"x".join(b)} binning')
        self._camera.set_roi(bins=b[0])

    # Dimensions

    @property
    def roi(self) -> int:
        return self._camera.get_roi()

    @roi.setter
    def roi(self, r: tuple[int,int] | tuple[int,int,int,int]) -> None:
        if len(r) == 2:
            self._camera.set_roi(width=r[0], height=r[1])
        else:
            self._camera.set_roi(start_x=r[0], start_y=r[1], width=r[2], height=r[3])

    @property
    def start_x(self) -> int:
        return self.roi[0]

    @property
    def end_x(self) -> int:
        return self.roi[2] + self.roi[0]

    @property
    def start_y(self) -> int:
        return self.roi[1]

    @property
    def end_y(self) -> int:
        return self.roi[3] + self.roi[1]

    @property
    def width(self) -> int:
        return self.roi[2]

    @property
    def height(self) -> int:
        return self.roi[3]
   
    @property
    def dropped_frames(self) -> int:
        return self._camera.get_dropped_frames()

    # Dark

    @property
    def dark_frame(self) -> FilePath:
        return self._dark_frame

    @dark_frame.setter
    @validate_call
    def dark_frame(self, path: FilePath | None) -> None:
        if self.dark_frame == path:
            return
        if self.dark_frame is None:
            self._camera.disable_dark_subtract()
            self._dark_frame = None
            return
        self.enable_dark_subtract(str(path))
        self._dark_frame = path
    
 
if __name__ == "__main__":
    cam = AsiCamera(name='ZWO ASI178MM')
