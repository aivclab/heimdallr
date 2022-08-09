import json
import socket
import time
from typing import Any

import paho.mqtt.client as mqtt
import schedule
from apppath import ensure_existence
from warg import busy_indicator
from draugr.writers import LogWriter, MockWriter, Writer
from warg import NOD

from heimdallr import PROJECT_APP_PATH, PROJECT_NAME
from heimdallr.configuration.heimdallr_config import ALL_CONSTANTS
from heimdallr.configuration.heimdallr_settings import (
    HeimdallrSettings,
    SettingScopeEnum,
)
from heimdallr.utilities.publisher.unpacking import pull_disk_usage_info, pull_gpu_info

HOSTNAME = socket.gethostname()

__all__ = ["main"]

LOG_WRITER: Writer = MockWriter()


def on_publish(client: Any, userdata: Any, result, writer: callable = None) -> None:
    """description"""
    global LOG_WRITER
    LOG_WRITER(result)
    if writer:
        writer(result)


def on_disconnect(client: Any, userdata: Any, rc, writer: callable = print) -> None:
    """description"""
    global LOG_WRITER
    if rc != 0:
        client.reconnect()
        result = "Unexpected MQTT disconnection. Will auto-reconnect"
        LOG_WRITER(result)
        writer(result)


def main(setting_scope: SettingScopeEnum = SettingScopeEnum.user) -> None:
    """description"""
    global LOG_WRITER
    if setting_scope == SettingScopeEnum.user:
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
    client = mqtt.Client(HOSTNAME)
    client.on_publish = on_publish
    client.on_disconnect = on_disconnect

    HEIMDALLR_SETTINGS = HeimdallrSettings(setting_scope)

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

    sensor_data = NOD(
        {HOSTNAME: {"gpu_stats": pull_gpu_info(), "du_stats": pull_disk_usage_info()}}
    )

    if True:  # with IgnoreInterruptSignal():
        print("Publisher started")

        def job():
            """description"""
            sensor_data[HOSTNAME]["gpu_stats"] = pull_gpu_info()
            sensor_data[HOSTNAME]["du_stats"] = pull_disk_usage_info()
            client.publish(
                ALL_CONSTANTS.MQTT_TOPIC,
                json.dumps(sensor_data.as_dict()),
                ALL_CONSTANTS.MQTT_QOS,
            )

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
