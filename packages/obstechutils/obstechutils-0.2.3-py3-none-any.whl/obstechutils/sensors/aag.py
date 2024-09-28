from __future__ import annotations

from obstechutils.sensors.meteosensor import MeteoSensor
from obstechutils.sensors.pyrgeometer import PyrgeometerCalibrator
from obstechutils.dataclasses import strictdataclass
from obstechutils.stats import MeasurementBinner, MeasurementType
from obstechutils import logging

import numpy as np
import time
from astropy.time import Time
from functools import cached_property

from typing import ClassVar

@strictdataclass
class AAG(MeteoSensor):
    
    encoding: str = 'latin_1' 
    timeout: float = 1.0
    baudrate: int = 9600
    id: str = 'aag'
    binner: MeasurementBinner = MeasurementBinner()
    cloud_calib: PyrgeometerCalibrator | None = None    
    check_wind: bool = False
    rain_limit: int = 1700
    wet_limit: int = 2000

    # Recommandations from manuals is to wait 2 s after connection to try
    # and read data.

    def connect(self, wait_before: float = 0, wait_after: float = 2) -> None:

        super().connect(wait_before=wait_before, wait_after=wait_after)
    
    def reconnect(self, wait_before: float = 0, wait_after: float = 2) -> None:

        super().reconnect(wait_before=wait_before, wait_after=wait_after)

    # See manuals for serial communication and value conversion: 
    # * https://lunaticoastro.com/aagcw/TechInfo/Rs232_Comms_v100.pdf
    # * https://lunaticoastro.com/aagcw/TechInfo/Rs232_Comms_v110.pdf
    # * https://lunaticoastro.com/aagcw/TechInfo/Rs232_Comms_v120.pdf
    # * https://lunaticoastro.com/aagcw/TechInfo/Rs232_Comms_v130.pdf
    # * https://lunaticoastro.com/aagcw/TechInfo/Rs232_Comms_v140.pdf
    #
    # Most commands are of the form x! and the answer is made of several
    # 15 characters blocks terminated by 
    #    !\x11            0
    #
    # The blocks are generally of the form
    #    !xy      value 
    #
    # I am careful to flush device before trying to read.

    @staticmethod
    def _parse_block(s: str) -> tuple[str, str] | None:
        
        # handshake
        if s[1] == '\x11':
            return None

        # this command is badly formatted, cf v110 doc. however it returns
        # M in v 5.60, not K
        if s[1] == 'M':
            return ('M', s[2:14])

        return s[1:2].strip(), s[3:15].strip()


    def _get_data(self, cmd: str, convert: Callable = lambda x: x) -> dict:
                    
        self.flush_input()
        self.flush_output()
        self.send(cmd)

        values = {}
        while block := self._parse_block(self.receive(size=15)):
            values[block[0]] = convert(block[1])

        return values

    # Properties to be read only once

    @cached_property
    def has_wind(self) -> float:

        if self.firmware[0] < 5:
            return False

        if self.check_wind is False:
            return False

        return self.read_device('v!')['v'] > 0

    @cached_property
    def firmware(self) -> tuple:

        fw = self._get_data('B!')['V'].split('.')
        return tuple(int(f) for f in fw)

    @cached_property
    def _M(self) -> np.ndarray:
   
        if self.firmware[0] <= 3: 
            # in v. 5.60 zener constant is 2.56
            return [3, 200_000, 56_000, 3_450, 1_000, 1_000] 

        constants = np.array([1/100, 1000, 100, 1, 100, 100])
        m = self._get_data('M!')['M']
        m = (np.array([ord(c) << 8 for c in m[::2]])
            + np.array([ord(c) for c in m[1::2]]))
        
        return m * constants


    @cached_property
    def zener_constant(self) -> float: return self._M[0]
    
    @cached_property
    def ldr_max_resistance(self) -> float: return self._M[1]
    
    @cached_property
    def ldr_pullup_resistance(self) -> float: return self._M[2]
    
    @cached_property
    def rain_beta(self) -> float: return self._M[3]
    
    @cached_property
    def rain_resistance_at_298K(self) -> float: return self._M[4]

    @cached_property
    def rain_pullup_resistance(self) -> float: return self._M[5]

    def read_device(self, cmd) -> list[float]:
       
        # Except for wind readings (deactivated by default), this calls
        # takes ~ 0.1 s if successful on the first try, but might take
        # up to ~ 3s if not

        logger = logging.getLogger()
 
        ntries = 3
        for i in range(ntries):

            try:

                return self._get_data(cmd, convert=int)

            except Exception as e:
                if i < ntries-1:
                    logger.info(f'device error: {e}')
                    self.reset_buffers()
                else:
                    raise
    
    def measurement(self):
        
        logger = logging.getLogger()

        if self.simulate:
            s = 'simulated '
            m = self._simulated_measurement()
        else:
            s = ''
            m = self._measurement()

        msg = (
            f"{self.id} {s}measurement: "
            f"T={m['temperature']:.2f} T_ir={m['temperature_ir']:.2f} "
            f"rain={m['rain']:.1f} LDR={m['ldr_resistance']:.0f}"
        ) 
        logger.debug(msg)

        return m

    def _simulated_measurement(self):
        
        t = Time.now()
        c = np.sin(np.pi * (t.mjd % 1))

        temperature = 14.2 + 11 * c + 0.2 * np.random.random()
        temperature_ir = -20 + 6 * c + 0.1 * np.random.random()
        m = dict(
            unix_time = Time.now().unix,
            temperature = temperature,
            temperature_ir = temperature_ir,
            rain = 0.,
            supply_voltage = 5.0 + 0.01 * np.random.random(),
            ldr_resistance = 50_000 + 1000 * np.random.random(),
            rain_sensor_temperature = temperature - 1 - 0.2*np.random.random(),
        ) 
        return m
                    
    def reset(self) -> None:
        logger = logging.getLogger()
        logger.info(f'device buffers will be restarted')
        self._get_data('z!') 

    @property
    def wind_speed (self) -> float:
        return self.read_device('V!')['w'] / 3.6

    @property
    def temperature(self) -> float:
        return 0.01 * self.read_device('T!')['2']
    
    @property
    def temperature_ir(self) -> float:
        return 0.01 * self.read_device('S!')['1']

    @property
    def rain_frequency(self) -> float:
        return float(self.read_device('E!')['R'])

    def _measurement(self):

        # A measurement lasts about 1.5s if wind is read and 0.5s otherwise
        # (the default), in most cases.  It could last significantly more if
        # there are recurrent errors, but timeout on read ensures it won't
        # block.

        logger = logging.getLogger()
       
        try:

            temperature_ir = self.temperature_ir
            temperature = self.temperature
            try:
                values = self.read_device('C!')
            except:
                values = {} 

            rain = self.rain_frequency
            wind_speed = self.wind_speed if self.has_wind else None

        except Exception as e:

            logger.warning(f"could not read AAG sensor: {e}")
            self.reconnect()
            return {}

        # Supply voltage
        v = 1023 / max(values['6'], 1)
        supply_voltage = self.zener_constant * v

        # Light dependent resistor. Little info on calibration, internet
        # fora claim it's just useful to detect wether it's day, at best. 
        v = 1023 / min(max(values['4'], 1), 1022) - 1
        ldr_resistance = self.ldr_pullup_resistance / v
        
        # Rain sensor temperature.  Not sure what it's useful for. 
        # Calibration of rain frequency? 
        v = 1023 / min(max(values['5'], 1), 1022) - 1
        r = self.rain_pullup_resistance / v
        r = np.log(r / self.rain_resistance_at_298K)
        rain_sensor_temperature =  1 / (r/self.rain_beta + 1/298.15) - 273.15

       
        # rain = 0 if dry, 0.5 if wet, 1.0 if raining 
        if rain == 400:
            rain = np.nan
        else:
            rain = ((rain < self.wet_limit) + (rain < self.rain_limit)) / 2


        m = dict(
            unix_time = Time.now().unix,
            temperature = temperature,
            temperature_ir = temperature_ir,
            rain = rain,
            supply_voltage = supply_voltage,
            ldr_resistance = ldr_resistance,
            rain_sensor_temperature = rain_sensor_temperature,
        )
        
        # check if wind is obtained
        if wind_speed is not None:
            m['wind_speed'] = wind_speed 

        return m

    def after_averaging(self, m: MeasurementType) -> MeasurementType:

        if (cal := self.cloud_calib) is not None:

            temperature = m['temperature']
            temperature_ir = m['temperature_ir']
            temperature_sky = cal.sky_temperature(temperature, temperature_ir)
            m['temperature_sky'] = temperature_sky

        return m
