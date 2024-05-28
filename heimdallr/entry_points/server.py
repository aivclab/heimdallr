#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "Christian Heider Nielsen"
__doc__ = r"""

           Created on 19/03/2020
           """

import datetime
import json
import logging
import socket
from typing import Any

import dash
import flask
import paho
from dash import Dash
from dash.dash_table import DataTable
from dash.dependencies import Input, Output
from dash.html import Div
from draugr.writers import LogWriter, MockWriter, Writer
from flask import Response
from paho import mqtt
from paho.mqtt.client import Client, MQTTv5
from paho.mqtt.enums import CallbackAPIVersion
from pandas import DataFrame
from waitress import serve
from warg import NOD, default_datetime_repr, ensure_existence

from heimdallr import PROJECT_APP_PATH, PROJECT_NAME
from heimdallr.configuration.heimdallr_config import ALL_CONSTANTS
from heimdallr.configuration.heimdallr_settings import (
    HeimdallrSettings,
    SettingScopeEnum,
)
from heimdallr.server.board_layout import get_root_layout
from heimdallr.utilities.server import (
    get_calender_df,
    per_machine_per_device_pie_charts,
    to_overall_gpu_process_df,
)

__all__ = ["main"]

from heimdallr.utilities.server.du_utilities import to_overall_du_process_df
from heimdallr.utilities.server.teams_status import team_members_status
import dash_bootstrap_components

logger = logging.getLogger(__name__)

log = logging.getLogger("werkzeug")
log.setLevel(logging.ERROR)

# external JavaScript files
external_scripts = [
    "https://www.google-analytics.com/analytics.js",
    {"src": "https://cdn.polyfill.io/v2/polyfill.min.js"},
    {
        "src": "https://cdnjs.cloudflare.com/ajax/libs/lodash.js/4.17.10/lodash.core.js",
        "integrity": "sha256-Qqd/EfdABZUcAxjOkMi8eGEivtdTkh3b65xCZL4qAQA=",
        "crossorigin": "anonymous",
    },
]

# external CSS stylesheets
external_stylesheets = [
    "https://codepen.io/chriddyp/pen/bWLwgP.css",
    # {
    #    "href": "https://stackpath.bootstrapcdn.com/bootstrap/4.1.3/css/bootstrap.min.css",
    #    "rel": "stylesheet",
    #    "integrity": "sha384-MCw98/SFnGE8fJT3GXwEOngsV7Zt27NXFoaoApmYm81iuXoPkFOJwJ8ERdknLPMO",
    #    "crossorigin": "anonymous",
    # },
    dash_bootstrap_components.themes.DARKLY,
]

GPU_STATS = NOD()
DU_STATS = NOD()
KEEP_ALIVE = NOD()

# CLIENT_ID = str(uuid.getnode())
HOSTNAME = socket.gethostname()
CLIENT_ID = HOSTNAME
MQTT_CLIENT = Client(
    client_id=CLIENT_ID,
    protocol=MQTTv5,
callback_api_version=CallbackAPIVersion.VERSION2
    # clean_session=True
)
MQTT_CLIENT.tls_set(tls_version=paho.mqtt.client.ssl.PROTOCOL_TLS)
DASH_APP = Dash(
    __name__,
    external_scripts=external_scripts,
    external_stylesheets=external_stylesheets,
)

DEVELOPMENT = False
DASH_APP.layout = get_root_layout(DEVELOPMENT)
# LOG_WRITER: Writer = MockWriter()


@DASH_APP.callback(
    Output(ALL_CONSTANTS.TIME_ID, "children"),
    [Input(ALL_CONSTANTS.TIME_INTERVAL_ID, "n_intervals")],
)
def update_time(n: int) -> str:
    """description"""
    global GPU_STATS
    global KEEP_ALIVE
    try:
        for k, v in KEEP_ALIVE.items():
            if v > ALL_CONSTANTS.TIMEOUT_MACHINES_SEC:
                if k in GPU_STATS.keys():
                    GPU_STATS.pop(k)
                    print(f"deleting {k} from stats")

        for key in list(KEEP_ALIVE.keys()):
            if key in GPU_STATS.keys():
                KEEP_ALIVE[key] = KEEP_ALIVE[key] + 1
            else:
                KEEP_ALIVE.pop(key)
                print(f"deleting {key} from keep alive")

    except Exception as e:
        print(e)

    return default_datetime_repr(datetime.datetime.now())


@DASH_APP.callback(
    Output(ALL_CONSTANTS.CALENDAR_ID, "children"),
    [Input(ALL_CONSTANTS.CALENDAR_INTERVAL_ID, "n_intervals")],
)
def update_calendar_live(n: int) -> DataTable:
    """description"""
    try:
        df = get_calender_df(
            HeimdallrSettings().google_calendar_id,
            HeimdallrSettings()._credentials_base_path,
            num_entries=ALL_CONSTANTS.TABLE_PAGE_SIZE,
        )

        return DataTable(
            id="calender-table-0",
            columns=[{"name": i, "id": i} for i in df.columns],
            data=df.to_dict("records"),
            page_size=ALL_CONSTANTS.TABLE_PAGE_SIZE,
            style_as_list_view=True,
            style_data_conditional=[
                {
                    "if": {"column_id": "start", "filter_query": "{start} > 3.9"},
                    "backgroundColor": "green",
                    "color": "white",
                },
            ],  # TODO: MAKE GRADIENT TO ORANGE FOR WHEN NEARING START, and GREEN WHEN IN PROGRESS
        )
    except Exception as e:
        return Div([f"Error: {e}"])


@DASH_APP.callback(
    Output(ALL_CONSTANTS.TEAMS_STATUS_ID, "children"),
    [Input(ALL_CONSTANTS.TEAMS_STATUS_INTERVAL_ID, "n_intervals")],
)
def update_teams_status_live(n: int) -> Div:
    """description"""

    return Div(team_members_status(None), className="row")


@DASH_APP.callback(
    Output(ALL_CONSTANTS.GPU_GRAPHS_ID, "children"),
    [Input(ALL_CONSTANTS.GPU_INTERVAL_ID, "n_intervals")],
)
def update_graph(n: int) -> Div:
    """description"""
    global GPU_STATS
    global KEEP_ALIVE
    compute_machines = []
    if GPU_STATS:
        compute_machines.extend(
            per_machine_per_device_pie_charts(GPU_STATS.as_dict(), KEEP_ALIVE.as_dict())
        )
    return Div(compute_machines)


@DASH_APP.callback(
    Output(ALL_CONSTANTS.GPU_TABLES_ID, "children"),
    [Input(ALL_CONSTANTS.GPU_INTERVAL_ID, "n_intervals")],
)
def update_table(n: int) -> Div:
    """description"""
    MQTT_CLIENT.loop()

    compute_machines = []

    if GPU_STATS:
        df = to_overall_gpu_process_df(GPU_STATS.as_dict())
    else:
        df = DataFrame(["No data"], columns=("data",))

    logger.warning(df)

    compute_machines.append(
        DataTable(
            id="gpu-table-0",
            columns=[{"name": i, "id": i} for i in df.columns],
            data=df.to_dict("records"),
            page_size=ALL_CONSTANTS.TABLE_PAGE_SIZE,
            # style_as_list_view=True,
            style_data_conditional=[
                {"if": {"row_index": "odd"}, "backgroundColor": "rgb(50, 50, 50)"},
                {"if": {"row_index": "even"}, "backgroundColor": "rgb(60, 60, 60)"},
            ],
            style_header={
                "backgroundColor": "rgb(30, 30, 30)",
                "fontWeight": "bold",
            },
        )
    )

    return Div(compute_machines)


@DASH_APP.callback(
    Output(ALL_CONSTANTS.DU_TABLES_ID, "children"),
    [Input(ALL_CONSTANTS.DU_INTERVAL_ID, "n_intervals")],
)
def update_table(n: int) -> Div:
    """description"""
    MQTT_CLIENT.loop()

    compute_machines = []

    if DU_STATS:
        df = to_overall_du_process_df(DU_STATS.as_dict())
    else:
        df = DataFrame(["No data"], columns=("data",))

    logger.warning(df)

    compute_machines.append(
        DataTable(
            id="du-table-0",
            columns=[{"name": i, "id": i} for i in df.columns],
            data=df.to_dict("records"),
            page_size=ALL_CONSTANTS.TABLE_PAGE_SIZE,
            # style_as_list_view=True,
            style_data_conditional=[
                {"if": {"row_index": "odd"}, "backgroundColor": "rgb(50, 50, 50)"},
                {"if": {"row_index": "even"}, "backgroundColor": "rgb(60, 60, 60)"},
            ],
            style_header={
                "backgroundColor": "rgb(30, 30, 30)",
                "fontWeight": "bold",
            },
        )
    )

    return Div(compute_machines)


@DASH_APP.callback(
    dash.dependencies.Output("menu_container", "style"),
    [dash.dependencies.Input("menu_toggle_button", "n_clicks")],
)
def menu_toggle(n_clicks: int) -> dict:
    """

    Args:
      n_clicks:

    Returns:

    """
    if n_clicks and n_clicks % 2 == 1:
        return {"display": "block"}
    return {"display": "none"}


@DASH_APP.server.route("/config", methods=["POST"])
def on_post_config() -> Response:
    """

    Returns:

    """
    if DEVELOPMENT:
        settings = HeimdallrSettings()
        for k, v in flask.request.form.items():
            if v != "":
                setattr(settings, k, v)
    else:
        print("Not in development mode")
    return flask.redirect("/")


def on_message(client: Any, userdata: Any, result: mqtt.client.MQTTMessage) -> None:
    """description"""
    global GPU_STATS
    global KEEP_ALIVE

    d = json.loads(result.payload)

    keys = d.keys()

    logger.warning("received message")

    for key in keys:

        if "gpu_stats" in d[key]:
            GPU_STATS[key] = d[key]["gpu_stats"]
            DU_STATS[key] = d[key]["du_stats"]
        else:
            GPU_STATS[key] = d[key]  # ["gpu_stats"]
            DU_STATS[key] = {}

        KEEP_ALIVE[key] = 0

    logger.warning(
        f"received payload for {keys}, retain:{result.retain}, timestamp:{result.timestamp}"
    )


def on_disconnect(client: Any, userdata: Any, rc: Any) -> None:
    """description"""
    if rc != 0:
        print("Unexpected MQTT disconnection. Will auto-reconnect")
        client.reconnect()
        client.subscribe(ALL_CONSTANTS.MQTT_TOPIC, ALL_CONSTANTS.MQTT_QOS)


def setup_mqtt_connection(settings) -> None:
    """

    :param settings:
    :type settings:
    """
    if (
        False
        # settings.mqtt_access_token and False
    ):  # TODO: not implemented
        pass
        # MQTT_CLIENT.username_pw_set(settings.MQTT_ACCESS_TOKEN)
    else:
        MQTT_CLIENT.username_pw_set(
            settings.mqtt_username,
            settings.mqtt_password,
        )
    try:

        MQTT_CLIENT.user_data_set([])

        MQTT_CLIENT.connect(
            settings.mqtt_broker,
            settings.mqtt_port,
            keepalive=60,
        )

    except Exception as e:
        logger.error(f"MQTT connection error: {e}")
        # raise e

def on_unsubscribe(client, userdata, mid, reason_code_list, properties):
    # Be careful, the reason_code_list is only present in MQTTv5.
    # In MQTTv3 it will always be empty
    if len(reason_code_list) == 0 or not reason_code_list[0].is_failure:
        print("unsubscribe succeeded (if SUBACK is received in MQTTv3 it success)")
    else:
        print(f"Broker replied with failure: {reason_code_list[0]}")
    #client.disconnect()


def on_subscribe(client, userdata, mid, reason_code_list, properties):
    # Since we subscribed only for a single channel, reason_code_list contains
    # a single entry
    if reason_code_list[0].is_failure:
        logger.warning(f"Broker rejected you subscription: {reason_code_list[0]}")
    else:
        logger.warning(f"Broker granted the following QoS: {reason_code_list[0].value}")


def on_connect(client, userdata, flags, reason_code, properties):
    if reason_code.is_failure:
        print(f"Failed to connect: {reason_code}. loop_forever() will retry connection")
    else:
        # we should always subscribe from on_connect callback to be sure
        # our subscribed is persisted across reconnections.

        MQTT_CLIENT.subscribe(ALL_CONSTANTS.MQTT_TOPIC, qos=ALL_CONSTANTS.MQTT_QOS)



def main(
    *args,
    setting_scope: SettingScopeEnum = SettingScopeEnum.user,
    development=False,
    **kwargs,
) -> None:
    """description"""
    global DEVELOPMENT
    global MQTT_CLIENT

    if False:
        if setting_scope == SettingScopeEnum.user:
            LOG_WRITER = LogWriter(
                ensure_existence(PROJECT_APP_PATH.user_log)
                / f"{PROJECT_NAME}_server.log"
            )
        else:
            LOG_WRITER = LogWriter(
                ensure_existence(PROJECT_APP_PATH.site_log)
                / f"{PROJECT_NAME}_server.log"
            )

        LOG_WRITER.open()

    MQTT_CLIENT.on_message = on_message
    MQTT_CLIENT.on_subscribe = on_subscribe
    MQTT_CLIENT.on_unsubscribe = on_unsubscribe
    MQTT_CLIENT.on_connect = on_connect

    crystallised_heimdallr_settings = HeimdallrSettings(setting_scope)
    setup_mqtt_connection(settings=crystallised_heimdallr_settings)


    DASH_APP.title = ALL_CONSTANTS.HTML_TITLE
    DASH_APP.update_title = ALL_CONSTANTS.HTML_TITLE
    host = ALL_CONSTANTS.SERVER_ADDRESS
    port = ALL_CONSTANTS.SERVER_PORT

    DEVELOPMENT = development
    DASH_APP.layout = get_root_layout(DEVELOPMENT)

    if development:
        DASH_APP.run(
            host=host,
            port=port,
            debug=ALL_CONSTANTS.DEBUG,
            dev_tools_hot_reload=ALL_CONSTANTS.DEBUG,
        )
    else:
        # DASH_APP.run_server(host=host, port=port)
        serve(DASH_APP.server, **kwargs)

    # LOG_WRITER.close()


if __name__ == "__main__":
    main(development=True)
