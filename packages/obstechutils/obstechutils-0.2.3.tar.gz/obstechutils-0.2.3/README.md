## Obstech python utilities

Utilities for El Sauce observatory to make life easier dealing with MySQL, MQTT, Google sheets, mailing, Telegram, command line options and configuration files, socket/serial connections, etc.

## Installation

* From local sources, within a virtual environment, `pip install -e .`
* From python repository, within a virtual environment, `pip install obstechutils`.

## Utilities
* `db/`: connect to MySQL plus observatory-specific queries
* `meteo/`: basic meteo functions plus DIMM analysis
* `sensors/`: handle the various weather sensors at the observatory 
* `cameras/`: pythonic drivers for cameras (so far ASI)
* `argparse/`: extensions to argparse
* `google`: down from google services like sheets
* `roof`: list roof info
* `mqtt`: MQTT client
* `inventory`: read inventory from the main Google Sheets database
* `credentials`: deal with logging into servers
* `email`: basic email sender
* `telegram`: basic Telegram client
* `connection`: unified interface to serial port/socket connections
* `coordinates`: coordinates utilities (e.g. GeoidLocation)
* `array`: array utilities such as masked array interpolation/binning
* `dataclasses`: dataclass improvements with pydantic
* `rinex`: some basic utils for RINEX GPS format
* `precise_timing`: close to real time tools, such as periodic calls of functions

## Scripts

Upon installation of the package the following scripts will be made available
from the command line.

ElSauce User Interface scripts
* `monitor_weather_sensor SENSOR`
* `mix_weather_sensors`
* `update_sql_table DATABASE TABLE`

Miscellaneous
* `mqtt_console`: display MQTT messages on the weather workstation
* `report_device_status`: check whether PCs and devices are turned on
* `list_roofs`: list roof parameters

## Credentials file
The credentials file should be in `~/.config/obstechutils` with the following
format

```
mail:
    device_status:
        username:     xxxxxxx@yyyy.zzz
        password:     xxxx xxxx xxxx xxxx
        server:       smtp.xxxx.yyy
        port:         465
mqtt:
    generic_obstech:
        username:     obstech
        password:     xxxxxxxxxx
        server:       yyy.yyy.yyy
        port:         1883
        qos:          2
        timeout:      60
mysql:
    generic_obstech:
        username:     obstech
        password:     xxxxxxxxxx
        server:       yyy.yyy.yyy.yyy
        port:         3306
googleapi:
    generic_obstech:
        username:     googleuser@gmail.com
        token:        googleapi/token-generic_obstech.json
        credentials:  googleapi/credentials-generic_obstech.json
        scopes:
        - https://www.googleapis.com/auth/spreadsheets.readonly

``` 
