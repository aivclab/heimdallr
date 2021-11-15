"""Function to get GPU infomations.
"""
from typing import Mapping, Sequence

import numpy
import pandas
from dash.dcc import Graph
from dash.html import Div, H3
from pandas import DataFrame
from plotly import graph_objs

from heimdallr.configuration.heimdallr_config import (
    DROP_COLUMNS,
    INT_COLUMNS,
    MB_COLUMNS,
    PERCENT_COLUMNS,
)
from heimdallr.utilities.date_tools import timestamp_to_datetime
from warg import Number

from heimdallr.utilities.unpacking import pull_gpu_info

MB_DIVISOR = int(1024 ** 2)

__all__ = [
    "to_overall_gpu_process_df",
    "per_machine_per_device_pie_charts",
]


def to_overall_gpu_process_df(gpu_stats: Mapping) -> DataFrame:
    """ """
    resulta = []
    columns = []
    for k2, v2 in gpu_stats.items():
        device_info = v2["devices"]
        for device_i in device_info:
            processes = device_i["processes"]
            if len(processes) > 0:
                columns = list(processes[0].keys())
            df = pandas.DataFrame(data=processes)
            df["machine"] = [k2] * len(processes)
            resulta.append(df)

    out_df = pandas.concat(resulta, sort=False)
    out_df.sort_values(by="used_gpu_mem", axis=0, ascending=False, inplace=True)
    if len(out_df) == 0:
        return pandas.DataFrame()

    k = columns
    idx = ["machine", *k]
    out_df = out_df[idx]
    out_df.create_time = out_df.create_time.map(timestamp_to_datetime)

    for c in INT_COLUMNS:
        out_df[c] = out_df[c].astype(int)
    for c in PERCENT_COLUMNS:
        out_df[c] = numpy.round(out_df[c], 2)
    for c in MB_COLUMNS:
        out_df[c] = numpy.round(out_df[c] // MB_DIVISOR, 2)

    out_cols = [c for c in out_df.columns if c not in DROP_COLUMNS]
    out_df = out_df[out_cols]

    return out_df


def per_machine_per_device_pie_charts(gpu_stats: Mapping, keep_alive: Sequence[Number]):
    """ """
    compute_machines = []
    for machine_name, machine in gpu_stats.items():
        machine_devices = []
        devices = machine["devices"]

        for i, d in enumerate(devices):

            used = d["used"] // MB_DIVISOR
            total = d["total"] // MB_DIVISOR

            used_ratio = used / total
            used_ratio = [used_ratio] + [1.0 - used_ratio]

            hover_text = [f"used:{used:.0f}mb", f"free:{total - used:.0f}mb"]

            machine_devices.append(
                Div(
                    [
                        Graph(
                            id=f"gpu_stats_{machine_name}{i}",
                            figure={
                                "data": [
                                    graph_objs.Pie(
                                        values=used_ratio,
                                        text=hover_text,
                                        name="used ratio",
                                        hole=0.4,
                                    )
                                ],
                                "layout": graph_objs.Layout(
                                    title=f"{d['name']} cuda_idx:{d['id']}",
                                    showlegend=False,
                                    hovermode="closest",
                                ),
                            },
                            style={
                                "width": "100%",
                            },
                        )
                    ],
                    className="col",
                )
            )
        compute_machines.append(
            Div(
                [
                    H3(
                        f"{machine_name}: {keep_alive[machine_name]} sec ago",
                        className="text-monospace",
                        style={"text-decoration": "underline"},
                    ),
                    Div([*machine_devices], className="row"),
                ],
                style={
                    "text-align": "center",
                    "width": "100%",
                },
            )
        )
    return compute_machines


if __name__ == "__main__":
    infos = pull_gpu_info()
    print(infos)
