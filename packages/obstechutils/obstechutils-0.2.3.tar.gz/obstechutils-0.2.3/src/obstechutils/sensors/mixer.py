from __future__ import annotations

from obstechutils.dataclasses import strictdataclass, Field, autoconverted
from obstechutils.mqtt import MQTTClient
from obstechutils.types import TimeDeltaType, TypeAlias
from obstechutils import logging
from obstechutils.types import LockType
from obstechutils.precise_timing import synchronised_call
from obstechutils import meteo

from typing import Callable, Union

from threading import Lock as _Lock
import copy
from time import time
import numpy as np
import json

FloatOrStr: TypeAlias = Union[float, str]
AveragerType: TypeAlias = Callable[list[float], float]
SingleSensorDataType: TypeAlias = dict[str, FloatOrStr]
SensorDataType: TypeAlias = dict[str, SingleSensorDataType]
MixType: TypeAlias = dict[str, FloatOrStr]
PostProcFuncType: TypeAlias = Callable[[MixType], None]
PreProcFuncType: TypeAlias = Callable[[SensorDataType], None]

def inaction(x: MixType | SensorDataType) -> None: 
    ...

@strictdataclass
class DataMixer(MQTTClient):
    """
EXAMPLE USE

    def add_sky_temperature(data: SensorDataType):
        ...
        
    mixer = DataMixer.from_credentials(
                user='generic_obstech',
                topics=['/ElSauce/Weather/Sensors/#'],
                default_publish_topic='/ElSauce/Weather/Mixer',
            )

    # start processing regularly in the background
    mixer.start_background_processing() 

    # start the infinite MQTT loop to receive messages
    mixer.loop_forever()

OPTIONAL KEYWORD ARGUMENTS

    polling_period [TimeDelta, default 1min]
        Every polling_period, received MQTT messages from different data
        sources will be received.

    polling_offset [TimeDelta, default 5s]
        Offset with respect to a round UCT time when polling should occur.

    mixing_methods [dict[str, Callable]]
        For each quantity (e.g. temperature, pressure), indicates a function
        that performs the mixing.  By default, np.mean is used.  If a function 
        other than min, max or numpy array functions are used, it needs to 
        accept data in the format {sensor_id: value}.
    
    default_mixing_method: AveragerType = np.mean
        Default mixing method for measurements. Meta data, such as dates,
        number of measurements, etc. get their own hard-coded default.

    pre_processing [Callable]
        Does post-processing on the mixed quantities, for instance if derived
        quantities must be added.  By default, does nothing.

    post_processing [Callable]
        Does post-processing on the mixed quantities, for instance if derived
        quantities must be added.  By default, does nothing.

    """

    # Mixing occurs on the 5th second of every minute.   We target
    # every sensor to average in the previous minute from measurements at
    # seconds 2, 4, ..., 58 so this should be more than enough to have all
    # sensors ready.

    id: str = 'mixer'
    polling_period: TimeDeltaType = '1min'
    polling_offset: TimeDeltaType = '5s'
    default_mixing_method: AveragerType = np.mean
    mixing_methods: dict[str, AveragerType] = Field(default_factory=lambda: {})
    
    pre_processing: PreProcFuncType = Field(default_factory=lambda: inaction)
    post_processing: PostProcFuncType = Field(default_factory=lambda: inaction)    
    _lock: LockType = Field(default_factory=lambda: _Lock(), repr=False)
    _sensor_data: dict = Field(default_factory=lambda: {}, repr=False)

    def on_message(self, obj, userdata, message) -> None:

        """Receive messages.  

        Messages sent with paylod "OK" will be understood as a confirmation
        processing is correctly working, and the OK message will be
        forwarded to /ElSauce/IsRunning/mixer, confirming that both
        threads (periodic execution and MQTT loop) are running as intended.


        Other messages are expected to #/sensors containing the sensor
        data to be merged.

        """

        logger = logging.getLogger()

        payload = message.payload.decode()

        if payload == "OK":
            self.notify_running()
            return

        m = json.loads(payload)
        sensor = m.pop('sensor')
        logger.debug(f'received MQTT message for sensor: {sensor}')

        with self._lock:
            self._sensor_data[sensor] = m

    def _mix(self, q: str, data: SensorDataType) -> MixType:
    
        logger = logging.getLogger()        
    
        # sensible aggregation methods for non-measurement metadata

        if q in ['date', 'date_start']:
            default = min
        elif q == 'date_end':
            default = max
        elif q == 'n_measurements':
            default = sum
        elif q == 'average_type':
            default = lambda m: ','.join(list(m.values()))
        else:
            default = self.default_mixing_method

        average = self.mixing_methods.get(q, default)

        m = {sensor: value for sensor, values in data.items()
                            if (value := values.get(q, None)) is not None}

        # Keep individual sensor values before averaging them

        mix = {f'{q}_{sensor}': value for sensor, value in m.items()}

        if average in [
            np.mean, np.median, np.min, np.max, np.sum, np.std,
            min, max, sum
        ]:
            m = list(m.values())
        mix[q] = average(m)

        if isinstance(mix[q], (float, np.floating)):
            logger.debug(f'mixed value {q} = {mix[q]:.2f}')
        
        return mix
        
    def mix_last_data(self) -> None:

        logger = logging.getLogger()

        # get a copy of last data and remove it 

        logger.info('acquire the data published during interval')

        with self._lock:
            data = copy.deepcopy(self._sensor_data)
            for key in self._sensor_data:
                self._sensor_data[key] = {}

        # pre-processing, of interest if cross sensor calibration is
        # needed.

        logger.debug(f'sensors: {", ".join(data.keys())}')
        self.pre_processing(data)

        # find all existing quantities

        quantities = np.unique(np.hstack([list(d) for d in data.values()]))
        logger.debug(f'quantities: {", ".join(quantities)}')

        # mix sensor data for each quantity 

        mix = {k: v for q in quantities for k, v in self._mix(q, data).items()}
        self.post_processing(mix)
        
        # publish mix, do a reentrant call to on_message to make sure
        # we're running OK

        self.publish_json(payload=mix)
        ok_topic = self.topics[0].rstrip('#/')
        self.publish(topic=f"{ok_topic}/processing", payload='OK')        

    def start_background_processing(self) -> None:

        """Start mixing the data in the background at regular intervals."""
        
        @synchronised_call(
            initial_delay=self.polling_offset,
            interval=self.polling_period,
            sync_offset=self.polling_offset,
            threaded=True,
        )
        def periodic_processing() -> None:
            
            logger = logging.getLogger()
 
            try:
                self.mix_last_data()
            except Exception as e:
                logger.error(f'error mixing sensor data: {e}') 
                raise
     
        periodic_processing()

