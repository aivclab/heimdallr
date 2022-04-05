from typing import List, Mapping, Sequence

import numpy
import pandas
from dash import html
from dash.dcc import Graph
from dash.html import Div, H3
from pandas import DataFrame
from plotly import graph_objs
from warg import Number

from heimdallr.configuration.heimdallr_config import (
    DROP_COLUMNS,
    INT_COLUMNS,
    MB_COLUMNS,
    PERCENT_COLUMNS,
)
from heimdallr.utilities.date_tools import timestamp_to_datetime

MB_DIVISOR = int(1024**2)

__all__ = [
    "to_overall_du_process_df",
]


def to_overall_du_process_df(gpu_stats: Mapping) -> DataFrame:
    """ """
    resulta = []
    columns = []
    for k2, v2 in gpu_stats.items():
        device_info = v2["partition"]
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
