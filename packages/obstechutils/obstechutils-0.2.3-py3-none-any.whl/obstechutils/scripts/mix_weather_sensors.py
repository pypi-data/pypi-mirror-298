#! /usr/bin/env python3

from __future__ import annotations

from obstechutils.sensors.mixer import DataMixer, MixType
from obstechutils.sensors.fuser import SensorFuser 
from obstechutils import meteo
from obstechutils import logging

import argparse
import numpy as np

def main() -> None:

    parser = argparse.ArgumentParser(
        description='mix meteo sensor data over MQTT'
    )
    parser.add_argument(
        '--log_path', default='./logs',
        help='Log file path'
    )
    parser.add_argument(
        '-k', dest='kalman', default=False, action='store_true',
        help='Use a Kálmán filtre for temperature, pressure, and humidity'
    ) 
    args = parser.parse_args()

    basename='mix_weather_sensors'
    logging.periodicFileConfig(
        level=logging.DEBUG, basename=basename, path=args.log_path, 
        force=True
    )

    mixing_methods = { }
    if args.kalman:
    
        # deviation of x - round(x) in uniform distributions, gives an
        # idea of the min. dispersion on discrete sensors.
        sig_u = 2 * np.sqrt(3) / 3 

        # Use Kálmán filtre on quantities that vary smoothly.  That excludes
        # wind.
        mixing_methods = dict(
            pressure = SensorFuser(
                process_dev = 0.05,          # 3 hPa/h
                min_data_dev = 1.0 * sig_u,  # steps of 1 mbar
                max_data_dev = 2,            # 1.5 hPa accuracy (NM150)
                dampening_timescale = '60 min',
            ),
            temperature = SensorFuser(
                process_dev = 0.1,           # 6⁰/h 
                min_data_dev = 0.1 * sig_u,  # steps of 0.1⁰C
                max_data_dev = 2,            # 1.5⁰C accuracy (NM150)
                dampening_timescale = '15 min',
            ),
            temperature_ir = SensorFuser(
                process_dev = 0.1,         
                min_data_dev = 0.1 * sig_u,  
                max_data_dev = 2,            
                dampening_timescale = '15 min',
            ),
            temperature_sky = SensorFuser(
                process_dev = 0.1,        
                min_data_dev = 0.1 * sig_u,
                max_data_dev = 2,  
                dampening_timescale = '15 min',
            ),
            humidity = SensorFuser(
                process_dev = 1,             # 60%/h 
                min_data_dev = 0.1 * sig_u,  # steps of 0.1%
                max_data_dev = 5.,           # 4% accuracy (NM150)
                dampening_timescale = '15 min',
            ),
        )

    # Fused dew point will be inconsistent with fused temperature
    # and humidity.  Fix that.

    def update_dew_point(m: MixType) -> None:
        
        T, h = m['temperature'], m['humidity']
        Tdew = meteo.functions.dew_point(T, h)
        m['dew_point'] = Tdew
    
    mixer = DataMixer.from_credentials(
        user='generic_obstech',
        topics=['/ElSauce/Weather/Sensors/#'],
        mixing_methods=mixing_methods,
        post_processing=update_dew_point,
        default_publish_topic='/ElSauce/Weather/Mixer',
    )

    # start processing regularly in the background and use the
    # infinite MQTT loop to process incoming messages

    mixer.start_background_processing() 
    mixer.loop_forever()

if __name__ == "__main__":
    main()
