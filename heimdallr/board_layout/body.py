#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "Christian Heider Nielsen"
__doc__ = r"""

           Created on 15/03/2020
           """

import dash_core_components as dcc
import dash_html_components as html

from heimdallr.utilities.heimdallr_config import (
  CALENDAR_ID,
  CALENDAR_INTERVAL_ID,
  CALENDAR_INTERVAL_MS,
  GPU_GRAPHS_ID,
  GPU_INTERVAL_ID,
  GPU_INTERVAL_MS,
  GPU_TABLES_ID,
  )


def get_body():
  return html.Div(
    [
      html.Div(
        [
          html.Div([], id=CALENDAR_ID),
          dcc.Interval(
            id=CALENDAR_INTERVAL_ID,
            interval=CALENDAR_INTERVAL_MS,
            n_intervals=0,
            ),
          ],
        className="col p-2",
        ),
      html.Div([html.Div([], id=GPU_GRAPHS_ID)], className="col"),
      html.Div([html.Div([], id=GPU_TABLES_ID), ], className="col p-2"),
      dcc.Interval(id=GPU_INTERVAL_ID, interval=GPU_INTERVAL_MS, n_intervals=0),
      ],
    className="row p-3",
    )
