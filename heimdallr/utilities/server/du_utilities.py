#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "Christian"
__doc__ = r"""

           Created on 29/03/2020
           """

from typing import Mapping

import numpy
import pandas
from pandas import DataFrame

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
    """
    to overall disk usage process df
    """
    resulta = []
    columns = []
    if len(gpu_stats):
        for k2, v2 in gpu_stats.items():
            if "partitions" in v2:
                for part_i in v2["partitions"]:
                    df = pandas.DataFrame(data=part_i)
                    resulta.append(df)
        if len(resulta):
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
    return pandas.DataFrame(data=["no data"], columns=["no data"])
