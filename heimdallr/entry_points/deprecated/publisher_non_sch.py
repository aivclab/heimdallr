import json
import socket
import time

import paho.mqtt.client
from draugr.writers import LogWriter, MockWriter, Writer
from warg import IgnoreInterruptSignal, NOD, busy_indicator, ensure_existence

from heimdallr import PROJECT_APP_PATH, PROJECT_NAME
from heimdallr.configuration.heimdallr_config import ALL_CONSTANTS
from heimdallr.configuration.heimdallr_settings import HeimdallrSettings
from heimdallr.utilities.publisher.unpacking import pull_gpu_info

HOSTNAME = socket.gethostname()

__all__ = ["main"]

LOG_WRITER: Writer = MockWriter()


def on_publish(client, userdata, result) -> None:
    """description"""
    global LOG_WRITER
    LOG_WRITER(result)


def on_disconnect(client, userdata, rc):
    """description"""
    if rc != 0:
        print("Unexpected MQTT disconnection. Will auto-reconnect")
        client.reconnect()


def main(is_user: bool = False):
    """description"""
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
    client = paho.mqtt.client.Client()
    client.on_publish = on_publish
    client.on_disconnect = on_disconnect

    heimdallr_settings = HeimdallrSettings()  # TODO input scope

    client.username_pw_set(
        heimdallr_settings.mqtt_username, heimdallr_settings.mqtt_password
    )
    try:
        client.connect(
            heimdallr_settings.mqtt_broker, heimdallr_settings.mqtt_port, keepalive=60
        )
    except ValueError as ve:
        raise ValueError(
            f"{heimdallr_settings._mqtt_settings_path},"
            f"{heimdallr_settings.mqtt_broker},"
            f"{heimdallr_settings.mqtt_port},"
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
