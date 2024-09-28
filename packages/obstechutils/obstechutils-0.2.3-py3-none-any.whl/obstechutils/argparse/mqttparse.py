from obstechutils.mqtt import MQTTClient
from obstechutils.types import LockType as _LockType
from obstechutils.dataclasses import strictdataclass, Field

from threading import Lock as _Lock
from argparse import ArgumentParser as _ArgumentParser
from argparse import *

@strictdataclass
class SingleMQTTMessageReceiver(MQTTClient):

    timeout: float = 10
    polling_time: float = 1

    _message: str | None = Field(default=None, repr=False)
    _lock: _LockType = Field(default_factory=lambda: _Lock(), repr=False)

    def get_message(self):
        
        self.connect() 
        self.loop_start()
    
        def on_message(self, obj, x, message):

            with self._lock:
                self._message = message.payload.decode()
        
        for i in range(self.timeout // self.polling_time):

            time.sleep(self.polling_time)

            with self._lock:
                if (message := self._message) is not None:
                    self.loop_stop()
                    self._message = None
                    return message

        self.loop_stop()
        raise TimeoutError('No MQTT message received')

class MQTTArgumentParser(_ArgumentParser):
    """Parse command line arguments sent a a single MQTT message in JSON
    array format."""

    def __init__(
        self, 
        *args, *,
        mqtt_user: str = '', 
        mqtt_topic: str = '',
        timeout: float = 10,
        polling_time: float = 1,
        **kwargs
    ) -> None:

        mqtt_client = SingleMQTTMessageReceiver.from_credentials(
            user=mqtt_user,
            topics=[mqtt_topic],
            timeout=timeout,
            polling_time=polling_time,
        )

        super().__init__(*args, **kwargs)
        self.mqtt_client = mqtt_client

    def parse_args(self, args=None, namespace=None):

        if args is None:
            command_line = self.mqtt_client.get_message()
            args = json.loads(command_line)

        super().parse_args(args=args, namespace=namespace)
