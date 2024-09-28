#! /usr/bin/env python3

from obstechutils.mqtt import MQTTConsole

import argparse
 
def main():

    import argparse

    parser = argparse.ArgumentParser(
        description='Print MQTT messages to the console'
    )
    parser.add_argument(
        '-t', nargs="+", default=['#'], metavar='TOPIC',
        help='MQTT topics to subscribe to.  By default, all.'
    )
    parser.add_argument(
        '-w', default=0, metavar='WIDTH',
        help='Console width to truncate messages. (By default no truncation.)'
    )
    args = parser.parse_args()

    user = 'generic_obstech'
    console = MQTTConsole.from_credentials(user, width=args.w, topics=args.t)
    console.connect()
    console.loop_forever()

if __name__ == "__main__":
    main()
