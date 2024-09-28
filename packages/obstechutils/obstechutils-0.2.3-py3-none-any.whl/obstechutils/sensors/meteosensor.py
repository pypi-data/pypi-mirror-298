from __future__ import annotations

from obstechutils.connection import SerialConnection
from obstechutils.dataclasses import strictdataclass, Field
from obstechutils.mqtt import MQTTClient
from obstechutils.precise_timing import average as average_function
from obstechutils import logging
from obstechutils.stats import MeasurementType, MeasurementBinner
from obstechutils.types import TimeDeltaType

from abc import ABC, abstractmethod
from astropy.time import Time

@strictdataclass
class MeteoSensor(SerialConnection, ABC):

    vendor_id: int
    product_id: int            
    mqtt: MQTTClient | None = None 
    interval: TimeDeltaType = '1min'
    sampling: TimeDeltaType = Field(default='4s', ge='4s')
    sync: str = 'utc'
    binner: MeasurementBinner = MeasurementBinner()
    simulate: bool = False

    def connect(self, **kwargs):

        if not self.simulate:
            super().connect(**kwargs)

    def reconnect(self, **kwargs):

        if not self.simulate:
            super().reconnect(**kwargs)

    def disconnect(self):
        if not self.simulate:
            super().disconnect()

    def loop_forever(self) -> None:

        logger = logging.getLogger()
        
        if self.mqtt is None:
            raise RuntimeError('No MQTT client set to publish results to')
        self.mqtt.connect() 
        
        self.connect()

        while True:

            m = self.average_measurement()
            if not m:
                msg = 'no average measurement for weather sensor {self.id}'
                logger.error(msg)
                continue

            topic = f'/ElSauce/Weather/Sensors/{self.id}'
            self.mqtt.publish_json(topic=topic, payload=m)

    def average_measurement(self) -> MeasurementType:

        logger = logging.getLogger()

        averager = average_function(
            interval=self.interval, sampling=self.sampling, sync=self.sync,
            averaging_fun=self.binner, return_times=True,
        )
        def measurement_function():
            m = self.measurement()
            if m and self.mqtt is not None:
                self.mqtt.notify_running()
            return m
        logger.info(f'ready to start averaging at {Time.now().isot}')

        (date_start, date_end), dates, m = averager(measurement_function)()
        
        m['sensor'] = self.id
        m['date_start'] = date_start.isot
        m['date_end'] = date_end.isot
        m['n_measurements'] = len(dates)
        m['average_type'] = self.binner.average_type

        m = self.after_averaging(m)
       
        # print info 
        rep = [f'{k} = {v:.2f}' for k, v in m.items() if isinstance(v, float)] 
        logger.info(
            f"sensor {self.id}: measurement average for "
            f"{m['date_start']} - {m['date_end']}: {m['n_measurements']} points"
        )
        logger.info(f"sensor {self.id}: measurement average:"  + " ".join(rep))

        return m

    @abstractmethod
    def measurement(self) -> MeasurementType: ...

    def after_averaging(self, m: MeasurementType) -> MeasurementType:
        return m
