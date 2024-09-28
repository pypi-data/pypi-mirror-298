from obstechutils.mqtt import MQTTClient
from obstechutils.dataclasses import strictdataclass
from obstechutils import logging

import json
from pathlib import Path

@strictdataclass
class NinaMonitor(MQTTClient):

    @classmethod
    def from_credentials(cls, user):

        topics = [
            '/ElSauce/IsRunning/NinaDimm',
            '/ElSauce/Dimm/Nina',
        ]
        return super().from_credentials(user=user, topics=topics)

    def on_message(self, client, userdata, message):

        logger = logging.getLogger('nina')

        payload = message.payload.decode()
        try:
            info = json.loads(payload)
        except:
            logger.error(f'error with payload: {payload}')
        else:
            logger.info(payload)
        
if __name__ == "__main__":

    logging.periodicFileConfig('nina', path=Path('./nina'))
    monitor = NinaMonitor.from_credentials(user='generic_obstech')
    monitor.loop_forever()
