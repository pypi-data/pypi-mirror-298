from obstechutils.sensors.meteosensor import MeteoSensor
from obstechutils.dataclasses import strictdataclass
from obstechutils.stats import MeasurementBinner, MeasurementType
from obstechutils import meteo
from obstechutils import logging
from obstechutils.connection import SerialException

import pynmea2
import time
from astropy.time import Time
import numpy as np

@strictdataclass
class NM150(MeteoSensor):

    timeout: float = 0.04 # Lines are <= 70 char long at 4800 B/s, i.e. ~ 0.1s
    baudrate: int = 4800
    id: str = 'nm150'
    binner: MeasurementBinner = MeasurementBinner(
        angles=['wind_direction'],
        max=['wind_speed']
    )

    @classmethod
    def parse_wimda_packet(cls, packet):

        try:
            if packet.startswith('$WIMDA'):
                m = pynmea2.parse(packet)
                m = dict(
                    pressure = float(m.b_pressure_bar) * 1e+3,
                    temperature = float(m.air_temp),
                    wind_speed = float(m.wind_speed_meters),
                    wind_direction  = float(m.direction_true),
                    humidity = float(m.rel_humidity),
                )
                return m
        except:
            ...

        return {}

    def get_wimda_message(self):

        # The issue is that readline() on serial may return a truncated
        # line for a finite timeout. We need to tread cautiously.
        #
        # Every second a GPGGA and a WIMDA message are published with an
        # interval of 0.16.  The write time is <0.02 s assuming 4800 B/s 
        # and <80 char long lines, and certainly less than 0.16 s  
        #
        # By sleeping 1.16 s we ensure that we have at least two full lines
        # (WIMDA + GGPA) in the buffer
        # GGPA - WIMDA - GGPA (incomplete or not)
        # WIMDA - GGPA - WIMDA (incomplete or not)
        # GGP (incomplete or not) - WIMDA - GGPA 
        # WIMDA (incomplete or not) - GGPA - WIMDA
        #
        # If not, it's a sensor-side issue and that will be dealt with 
 
        time.sleep(1.16) 
        packets = self.readlines()[-3:]

        if packets[-1].endswith('\n'):
            packets = packets[-2:]
        else:
            packets = packets[-3:-1]
 
        for packet in packets:
            if m := self.parse_wimda_packet(packet):
                return m

        raise RuntimeError(f'No valid WIMDA packet: {packets}')
    
    def measurement(self) -> dict:

        logger = logging.getLogger()
        id = f'weather sensor {self.id}'

        if self.simulate:
            s = 'simulated '
            m = self._simulated_measurement()
        else:
            s = ''
            m = self._measurement()
            
        msg = (
            f"{self.id} {s}measurement: "
            f"T={m['temperature']:.1f} P={m['pressure']:.1f}"
            f"v={m['wind_speed']:.1f} h={m['humidity']:.1f}"
        )
        logger.debug(msg)

        return m

            
    def _simulated_measurement(self) -> dict:

        t = Time.now()
        c = np.sin(np.pi * (t.mjd % 1))

        temperature = 15 + 10 * c + 0.2 * np.random.random()
        humidity = 45 + 25 * c + 1.0 * np.random.random() 
        dew_point = meteo.dew_point(temperature, humidity)
        message = dict(
            pressure = 1020 + 7 * c + 0.2 * np.random.random(),
            temperature = temperature,
            wind_speed = 1.5 + 1 * c + 1.0 * np.random.random(),
            wind_direction = 180 + 40 * c + 10 * np.random.random(),
            humidity = humidity,
            dew_point = dew_point,
            unix_time = t.unix,
        )

        return message

    def _measurement(self) -> dict:

        logger = logging.getLogger()

        # Try to get a correct packet within a sampling time
        #
        # * First attempt: at most ~ 1.2 seconds 
        # * Subsequent attemps: at most ~ 1.3 seconds (reconnect is fast)
        #
        # Within 1 sampling time of 4 s, either of the following will have
        # occured:
        #  * a well-formed packet has been read
        #  * or three attempts and a reconnection to port have been tried

        t = time.time()
        needs_reconnect = False
        message = None
        n_tries = 0
        
        while message is None and time.time() - t < self.sampling.sec - 1.5:

            n_tries += 1

            try:

                if needs_reconnect:
                    logger.info(f'{id}: try to reconnect to serial port')
                    self.reconnect()
                    needs_reconnect = False

                # try to read WIMDA NMEA packet. That takes ~ 1.1 s 
                message = self.get_wimda_message()
                break

            except SerialException as e:

                logger.info(f'{id}: serial port error: {e}')
                needs_reconnect = True

            except Exception as e:

                # after every second consecutive failure to have a correct 
                # NMEA packet we will try a reconnect just in case
                if n_tries % 2 == 0:
                    msg = (f'{id}: {n_tries} consecutive failures '
                            'to get a properly filled WIMDA packet')
                    logger.warning(msg)
                    needs_reconnect = True

        else:

            logger.warning(f'{id}: no measurement obtained')
            return { }

        dewpoint = meteo.dew_point(message['temperature'], message['humidity'])
        message['dew_point'] = dewpoint
        message['unix_time'] = Time.now().unix

        return message
