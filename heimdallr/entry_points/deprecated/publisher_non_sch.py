import json
import socket
import time

import paho.mqtt.client as mqtt

from apppath import ensure_existence
from draugr import IgnoreInterruptSignal
from draugr.python_utilities.business import busy_indicator
from draugr.writers import LogWriter, MockWriter, Writer
from heimdallr import PROJECT_APP_PATH, PROJECT_NAME
from heimdallr.configuration.heimdallr_config import ALL_CONSTANTS
from heimdallr.configuration.heimdallr_settings import HeimdallrSettings
from heimdallr.utilities.unpacking import pull_gpu_info
from warg import NOD

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


def main(is_user: bool = False):
    """ """
    global LOG_WRITER
    if is_user:
        LOG_WRITER = LogWriter(
            ensure_existence(PROJECT_APP_PATH.user_log)
            / f"{PROJECT_NAME}_publisher.log"
        )
    else:
        LOG_WRITER = LogWriter(
            ensure_existence(PROJECT_APP_PATH.site_log)
            / f"{PROJECT_NAME}_publisher.log"
        )
    LOG_WRITER.open()
    client = mqtt.Client()
    client.on_publish = on_publish
    client.on_disconnect = on_disconnect

    HEIMDALLR_SETTINGS = HeimdallrSettings()  # TODO input scope

    client.username_pw_set(
        HEIMDALLR_SETTINGS.mqtt_username, HEIMDALLR_SETTINGS.mqtt_password
    )
    try:
        client.connect(
            HEIMDALLR_SETTINGS.mqtt_broker, HEIMDALLR_SETTINGS.mqtt_port, keepalive=60
        )
    except ValueError as ve:
        raise ValueError(
            f"{HEIMDALLR_SETTINGS._mqtt_settings_path},"
            f"{HEIMDALLR_SETTINGS.mqtt_broker},"
            f"{HEIMDALLR_SETTINGS.mqtt_port},"
            f"{ve}"
        )
    client.loop_start()

    sensor_data = NOD({HOSTNAME: pull_gpu_info()})
    next_reading = time.time()

    with IgnoreInterruptSignal():
        print("Publisher started")

        for _ in busy_indicator():
            sensor_data[HOSTNAME] = pull_gpu_info()
            s = sensor_data.as_dict()
            s = json.dumps(s)
            client.publish(ALL_CONSTANTS.MQTT_TOPIC, s, ALL_CONSTANTS.MQTT_QOS)
            next_reading += ALL_CONSTANTS.MQTT_PUBLISH_INTERVAL_SEC
            sleep_time = next_reading - time.time()

            if sleep_time > 0:
                time.sleep(sleep_time)

    # noinspection PyUnreachableCode
    LOG_WRITER.close()
    client.loop_stop()
    client.disconnect()


if __name__ == "__main__":
    main()
