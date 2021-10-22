import json
import socket
import time


import paho.mqtt.client as mqtt
import schedule
from warg import NOD

from draugr.python_utilities.business import busy_indicator
from draugr import IgnoreInterruptSignal
from draugr.writers import LogWriter, MockWriter, Writer
from heimdallr import PROJECT_APP_PATH, PROJECT_NAME
from heimdallr.configuration.heimdallr_settings import HeimdallrSettings

from heimdallr.utilities.gpu_utilities import pull_gpu_info
from heimdallr.configuration.heimdallr_config import ALL_CONSTANTS

HOSTNAME = socket.gethostname()

__all__ = ["main"]

LOG_WRITER: Writer = MockWriter()


def on_publish(client, userdata, result) -> None:
    """ """
    global LOG_WRITER
    LOG_WRITER(result)


def on_disconnect(client, userdata, rc):
    """ """
    if rc != 0:
        print("Unexpected MQTT disconnection. Will auto-reconnect")
        client.reconnect()


def main():
    """ """
    global LOG_WRITER
    LOG_WRITER = LogWriter(PROJECT_APP_PATH.user_log / f"{PROJECT_NAME}_publisher.log")
    LOG_WRITER.open()
    client = mqtt.Client()
    client.on_publish = on_publish
    client.on_disconnect = on_disconnect

    HEIMDALLR_SETTINGS = HeimdallrSettings()

    client.username_pw_set(
        HEIMDALLR_SETTINGS.mqtt_username, HEIMDALLR_SETTINGS.mqtt_password
    )
    client.connect(
        HEIMDALLR_SETTINGS.mqtt_broker, HEIMDALLR_SETTINGS.mqtt_port, keepalive=60
    )
    client.loop_start()

    sensor_data = NOD({HOSTNAME: pull_gpu_info()})

    with IgnoreInterruptSignal():
        print("Publisher started")

        def job():
            """ """
            sensor_data[HOSTNAME] = pull_gpu_info()
            s = sensor_data.as_dict()
            s = json.dumps(s)
            client.publish(ALL_CONSTANTS.MQTT_TOPIC, s, ALL_CONSTANTS.MQTT_QOS)

        schedule.every(ALL_CONSTANTS.MQTT_PUBLISH_INTERVAL_SEC).seconds.do(job)

        for _ in busy_indicator():
            schedule.run_pending()
            time.sleep(1)

    # noinspection PyUnreachableCode
    LOG_WRITER.close()
    client.loop_stop()
    client.disconnect()


if __name__ == "__main__":
    main()
