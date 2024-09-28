from __future__ import annotations

from obstechutils.credentials import Credentials
from obstechutils.dataclasses import strictdataclass, Field, autoconverted 
from obstechutils.types import QOSType, PortType

from functools import cached_property
import paho.mqtt.client as mqtt
from typing_extensions import Annotated
from pydantic import PositiveInt, NonNegativeInt
from pydantic.networks import IPvAnyAddress
import json
import yaml
import re
import os
import sys
            
CALLBACK_NAMES = [
    'on_connect', 'on_connect_fail', 'on_disconnect',
    'on_subscribe', 'on_unsubscribe',
    'on_message', 'on_publish', 'on_log'
]

    
def mqtt_client_from_api_version(n):
    try:
        api = getattr(mqtt.CallbackAPIVersion, f"VERSION{n}")
    except:
        raise RuntimeError(f'No such MQTT callback API: {n}')
    return mqtt.Client(api) 

MQTTClientType = autoconverted(
    mqtt.Client,
    converter_function=mqtt_client_from_api_version
)

@strictdataclass
class MQTTClient:

    username: str
    password: str
    server: IPvAnyAddress
    topics: list[str] = Field(default_factory=lambda: [])
    port: PortType = 1883
    qos: QOSType = 2
    timeout: PositiveInt = 60
    default_publish_topic: str = ''
    client: MQTTClientType = 2

    @classmethod
    def from_credentials(
        cls, 
        user: str ='generic_obstech', 
        **kwargs
    ) -> MQTTClient:

        creds = Credentials.load('mqtt', user=user)
        kwargs = {**creds, **kwargs}
        return cls(**kwargs)

    def __post_init__(self):

        self.client.username_pw_set(self.username, password=self.password)

        for callback_name in CALLBACK_NAMES:
            if callback := getattr(self, callback_name, None):
                setattr(self.client, callback_name, callback)

    def loop_forever(self): 
        self.connect()
        self.client.loop_forever()

    def loop_start(self): 
        self.connect()
        self.client.loop_start()

    def loop_stop(self): 
        self.connect()
        self.client.loop_stop()

    def publish(self, topic: str = '', payload: object = '', **kwargs):
        if topic == '':
            topic = self.default_publish_topic 
        info = self.client.publish(topic=topic, payload=payload, **kwargs)

    @cached_property
    def running_notification_topic(self):
       
        topic = ' '.join([os.path.basename(sys.argv[0]), *sys.argv[1:]]) 
        topic = re.sub('[$/#+]', '?', topic)
        topic = f'/ElSauce/IsRunning/{topic}'

        return topic

    def notify_running(self):
        """Notify that the program calling it is running.

        Message OK is sent to topic /ElSauce/IsRunning/program arg1 arg2 ...

        """
        self.publish(topic=self.running_notification_topic, payload='OK')
        
    def publish_json(self, topic: str = '', payload: object = '', **kwargs): 
        self.publish(topic, json.dumps(payload), **kwargs)
 
    def connect(self):

        server = str(self.server)
        self.client.connect(server, self.port, self.timeout)

    def disconnect(self):

        self.client.disconnect()

    def on_connect(self, client, userdata, flags, rc, prop):

        if rc != 0:
            msg = 'MQTT connection to {self.server}:{self.port} failed'
            raise ConnectionError(msg)

        topics = [(t, self.qos) for t in self.topics]
        self.client.subscribe(topics)

@strictdataclass
class MQTTConsole(MQTTClient):

    width: NonNegativeInt = 0
    
    def on_message(self, client, userdata, message):

        topic = message.topic
        data = message.payload.decode()
        # data = re.sub('\\s', '', data)
        msg = f"{topic}:\n{data}"
        
        if self.width:
            w = self.width + len(topic) + 1
            msg = msg if len(data) < w else f"{msg[:w-3]}..."

        print(msg)
    
def console_script():

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
