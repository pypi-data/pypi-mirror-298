from __future__ import annotations

from obstechutils.db import DataBase
from obstechutils.mqtt import MQTTClient
from obstechutils.dataclasses import strictdataclass, Field
from obstechutils import logging

import numpy as np
import json
import argparse

def data_as_sql(v):
    """Ensure valid values are sent to SQL the database. Check tables
    all accept NULL!!"""
    if isinstance(v, str):
        return f"'{v}'"
    if v is None or not np.isfinite(v):
        return "NULL"
    return f"{v}"

@strictdataclass
class WeatherDataBaseWriter(MQTTClient):

    database: DataBase | None = None
    table_name: str = 'weather'
    
    @classmethod
    def from_credentials(
            cls, 
            mqtt_user: str, 
            database_user: str, 
            database_name: str,
            topics: str,
            table_name: str,
            **kwargs,
    ) -> WeatherDataBaseWriter:

        database = None
        if database_name:
            database = DataBase.from_credentials(
                user=database_user,
                database=database_name,    
            )
        
        writer = super().from_credentials(
            user=mqtt_user, topics=topics, 
            database=database, table_name=table_name,
            **kwargs,
        )

        return writer

    def write(self, data: dict[str, object]) -> bool:
        
        names = list(data.keys())
        values = [data_as_sql(v) for v in data.values()]
        command = f"""
            INSERT INTO {self.table_name} ({', '.join(names)})
            VALUES 
            ({', '.join(values)})
        """
       
        try:  

            if self.database is not None:
                
                if self.table_name == 'weather_test':   
                    print(command)
                
                with self.database.connect() as conn:
                    cursor = conn.cursor()
                    cursor.execute(command)
                    conn.commit()
             
            else:
                print(command)

        except Exception as e:

            logger = logging.getLogger()
            logger.error(f'error writing to table {self.table_name}: {e}')
            return False 

        else: 

            return True

    def on_message(self, client, data, message) -> None: 

        logger = logging.getLogger()
        print('message')

        topic = message.topic

        try:
            payload = message.payload.decode()
            data = json.loads(payload)
        except Exception as e:
            logger.error(f'could not process MQTT message payload: ignored')
            logger.error(f'error is: {e}')
            return

        ok = self.write(data)
        
        if ok and self.default_publish_topic:
            self.publish(payload='OK', qos=1)
        
        logger.debug(f'received message on {topic}: {payload}') 

def update_database(
    database_user='generic_obstech',
    database_name='',
    topic='weatherdata',
    notification_topic='update_weather_database',
    table='weather',
):
    
    writer = WeatherDataBaseWriter.from_credentials(
        database_user=database_user,
        database_name=database_name,
        table_name=table,
        mqtt_user='generic_obstech',
        topics=[f'/ElSauce/Weather/{topic}'],
        default_publish_topic=notification_topic
    )
    print(f"{writer=}")
    writer.connect()
    writer.loop_forever()
    
