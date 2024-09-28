#! /usr/bin/env python3

from obstechutils.sensors import NM150, AAG
from obstechutils.mqtt import MQTTClient
from obstechutils import logging

import warnings
warnings.filterwarnings("error")
import argparse

def main() -> None:

    parser = argparse.ArgumentParser(
        description='Simulate weather data'
    )
    parser.add_argument(
        '-s', default=False, action='store_true',
        help='Simulate weather sensor data for testing purposes'
    )
    parser.add_argument(
        '--log_path', default='./logs',
        help='Log file path'
    )
    parser.add_argument(
        'sensor', choices=['NM150', 'AAG1', 'AAG2'],
        help='Weather sensor ID'
    )
    args = parser.parse_args()

    basename = f"{'simulate' if args.s else 'monitor'}_{args.sensor}_sensor"

    logging.periodicFileConfig(
        level=logging.DEBUG, basename=basename, path=args.log_path, 
        force=True
    )
    mqtt = MQTTClient.from_credentials('generic_obstech')

    if args.sensor == 'NM150':
        sensor = NM150(
            simulate=True, interval='60s', sampling='4s',
            id='nm150', vendor_id=1741, product_id=289, mqtt=mqtt,
        )

    elif args.sensor == 'AAG1':
        sensor = AAG(
            simulate=True, interval='60s', sampling='4s',
            id='aag1', vendor_id=1027, product_id=24577, mqtt=mqtt,
        )

    elif args.sensor == 'AAG2':
        sensor = AAG(
            simulate=True, interval='60s', sampling='4s',
            id='aag2', vendor_id=1659, product_id=8963, mqtt=mqtt
        )

    else:
        raise NotImplementedError(f'Sensor {args.sensor} not supported')

    sensor.loop_forever()

if __name__ == "__main__":
    main()
