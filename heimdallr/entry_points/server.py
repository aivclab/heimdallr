import copy
import datetime
import json
import logging
import socket
from typing import Any

import dash
import flask
from apppath import ensure_existence
from dash import Dash
from dash.dash_table import DataTable
from dash.dependencies import Input, Output
from dash.html import Div
from draugr.python_utilities import default_datetime_repr
from draugr.writers import LogWriter, MockWriter, Writer
from flask import Response
from paho import mqtt
from paho.mqtt.client import Client
from pandas import DataFrame
from warg import NOD

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

from heimdallr.utilities.server.teams_status import team_members_status

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
    {
        "href": "https://stackpath.bootstrapcdn.com/bootstrap/4.1.3/css/bootstrap.min.css",
        "rel": "stylesheet",
        "integrity": "sha384-MCw98/SFnGE8fJT3GXwEOngsV7Zt27NXFoaoApmYm81iuXoPkFOJwJ8ERdknLPMO",
        "crossorigin": "anonymous",
    },
]

GPU_STATS = NOD()
DU_STATS = NOD()
KEEP_ALIVE = NOD()

# CLIENT_ID = str(uuid.getnode())
HOSTNAME = socket.gethostname()
CLIENT_ID = HOSTNAME
MQTT_CLIENT = Client(
    client_id=CLIENT_ID,
    # clean_session=True
)
DASH_APP = Dash(
    __name__,
    external_scripts=external_scripts,
    external_stylesheets=external_stylesheets,
)
DASH_APP.layout = get_root_layout()
LOG_WRITER: Writer = MockWriter()


@DASH_APP.callback(
    Output(ALL_CONSTANTS.TIME_ID, "children"),
    [Input(ALL_CONSTANTS.TIME_INTERVAL_ID, "n_intervals")],
)
def update_time(n: int) -> str:
    """ """
    global GPU_STATS
    global KEEP_ALIVE
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

    return default_datetime_repr(datetime.datetime.now())


@DASH_APP.callback(
    Output(ALL_CONSTANTS.CALENDAR_ID, "children"),
    [Input(ALL_CONSTANTS.CALENDAR_INTERVAL_ID, "n_intervals")],
)
def update_calendar_live(n: int) -> DataTable:
    """ """
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


@DASH_APP.callback(
    Output(ALL_CONSTANTS.TEAMS_STATUS_ID, "children"),
    [Input(ALL_CONSTANTS.TEAMS_STATUS_INTERVAL_ID, "n_intervals")],
)
def update_teams_status_live(n: int) -> Div:
    """ """

    return Div(team_members_status(None), className="row")


@DASH_APP.callback(
    Output(ALL_CONSTANTS.GPU_GRAPHS_ID, "children"),
    [Input(ALL_CONSTANTS.GPU_INTERVAL_ID, "n_intervals")],
)
def update_graph(n: int) -> Div:
    """ """
    global GPU_STATS
    global KEEP_ALIVE
    compute_machines = []
    if GPU_STATS:
        compute_machines.extend(
            per_machine_per_device_pie_charts(copy.deepcopy(GPU_STATS), KEEP_ALIVE)
        )
    return Div(compute_machines)


@DASH_APP.callback(
    Output(ALL_CONSTANTS.GPU_TABLES_ID, "children"),
    [Input(ALL_CONSTANTS.GPU_INTERVAL_ID, "n_intervals")],
)
def update_table(n: int) -> Div:
    """ """
    MQTT_CLIENT.loop()

    compute_machines = []

    if GPU_STATS:
        df = to_overall_gpu_process_df(copy.deepcopy(GPU_STATS))
    else:
        df = DataFrame(["No data"], columns=("data",))

    compute_machines.append(
        DataTable(
            id="gpu-table-0",
            columns=[{"name": i, "id": i} for i in df.columns],
            data=df.to_dict("records"),
            page_size=ALL_CONSTANTS.TABLE_PAGE_SIZE,
            # style_as_list_view=True,
            style_data_conditional=[
                {"if": {"row_index": "odd"}, "backgroundColor": "rgb(248, 248, 248)"}
            ],
            style_header={
                "backgroundColor": "rgb(230, 230, 230)",
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
    settings = HeimdallrSettings()
    for k, v in flask.request.form.items():
        if v != "":
            setattr(settings, k, v)
    return flask.redirect("/")


def on_message(client: Any, userdata: Any, result: mqtt.client.MQTTMessage) -> None:
    """ """
    global LOG_WRITER
    global GPU_STATS
    global KEEP_ALIVE
    d = json.loads(result.payload)
    keys = d.keys()
    GPU_STATS[keys] = d.values()["gpu_stats"]
    DU_STATS[keys] = d.values()["du_stats"]
    KEEP_ALIVE[keys] = [0] * len(keys)
    LOG_WRITER(
        f"received payload for {keys}, retain:{result.retain}, timestamp:{result.timestamp}"
    )


def on_disconnect(client: Any, userdata: Any, rc: Any) -> None:
    """ """
    if rc != 0:
        print("Unexpected MQTT disconnection. Will auto-reconnect")
        client.reconnect()
        client.subscribe(ALL_CONSTANTS.MQTT_TOPIC, ALL_CONSTANTS.MQTT_QOS)


def setup_mqtt_connection(settings) -> None:
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
        MQTT_CLIENT.connect(
            settings.mqtt_broker,
            settings.mqtt_port,
            keepalive=60,
        )
        MQTT_CLIENT.subscribe(ALL_CONSTANTS.MQTT_TOPIC, ALL_CONSTANTS.MQTT_QOS)
    except Exception as e:
        LOG_WRITER(f"MQTT connection error: {e}")
        # raise e


def main(setting_scope: SettingScopeEnum = SettingScopeEnum.user):
    """ """
    global LOG_WRITER
    if setting_scope == SettingScopeEnum.user:
        LOG_WRITER = LogWriter(
            ensure_existence(PROJECT_APP_PATH.user_log) / f"{PROJECT_NAME}_server.log"
        )
    else:
        LOG_WRITER = LogWriter(
            ensure_existence(PROJECT_APP_PATH.site_log) / f"{PROJECT_NAME}_server.log"
        )
    LOG_WRITER.open()
    MQTT_CLIENT.on_message = on_message
    MQTT_CLIENT.on_disconnect = on_disconnect

    if True:
        crystallised_heimdallr_settings = HeimdallrSettings(setting_scope)
        setup_mqtt_connection(settings=crystallised_heimdallr_settings)

    DASH_APP.title = ALL_CONSTANTS.HTML_TITLE
    DASH_APP.update_title = ALL_CONSTANTS.HTML_TITLE

    DASH_APP.run_server(
        host=ALL_CONSTANTS.SERVER_ADDRESS,
        port=ALL_CONSTANTS.SERVER_PORT,
        debug=ALL_CONSTANTS.DEBUG,
        dev_tools_hot_reload=ALL_CONSTANTS.DEBUG,
    )

    LOG_WRITER.close()


if __name__ == "__main__":
    main()
