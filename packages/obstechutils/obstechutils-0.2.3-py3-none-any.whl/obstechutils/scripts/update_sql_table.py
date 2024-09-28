#!/usr/bin/env python3

from obstechutils.db.weatherupdate import update_database
from obstechutils import logging

import argparse 

def main() -> None:

    parser = argparse.ArgumentParser(
        description="Update the weather-related tables in the SQL database"
    )
    parser.add_argument(
        '--log_path', default='./logs',
        help='Log file path',
    )
    parser.add_argument(
        'db', metavar='DB', 
        choices=['local', 'remote'],
        help='Database to update (local, remote)',
    )
    parser.add_argument(
        'table', metavar='TABLE',
        choices=['dimm', 'weather', 'ninox', 'Solar_seeing'],
        help='Name of the table to update (weather, dimm, ninox, Solar_seeing)'
    )
    parser.parse_args()

    basename='update_sql_table_{args.db}_{args.table}'
    logging.periodicFileConfig(
        level=logging.DEBUG, basename=basename, path=args.log_path,
        force=True
    )
      
    if args.d == 'local':
        database_name = 'ElSauceWeather' 
        database_user='generic_obstech'
    else:
        database_name = 'obtecho_test'
        database_user='remote_obstech'

    topic = '_'.join(w.lcfirst() for w in table.split('_'))

    update_database(
        database_user=database_user, 
        database_name=database_name, 
        table=table,
        topic=topic, 
        notification_topic='/ElSauce/IsRunning/update_sql_table_{args.t}_{args.d}'
    )

if __name__ == "__main__":
    main()
