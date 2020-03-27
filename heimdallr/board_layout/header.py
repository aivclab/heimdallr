#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "Christian Heider Nielsen"
__doc__ = r"""

           Created on 15/03/2020
           """

import dash_core_components as dcc
import dash_html_components as html

from heimdallr.utilities.heimdallr_config import HTML_TITLE, TIME_ID, TIME_INTERVAL_ID


def get_header():
  return html.Div(
    [
      html.Div(
        [html.H1(HTML_TITLE)], className="col text-left align-self-center p-1"
        ),
      html.Div(
        [
          html.Img(
            src="/assets/alexandra.png",
            style={"height":"80px", "object-fit":"contain"},
            )
          ],
        className="col text-center p-1",
        ),
      html.Div(
        [
          html.H1(id=TIME_ID),
          dcc.Interval(id=TIME_INTERVAL_ID, interval=1000, n_intervals=0),
          ],
        className="col text-right align-self-center p-1",
        ),
      ],
    className="row p-3",
    )
