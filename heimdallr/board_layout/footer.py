#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "Christian Heider Nielsen"
__doc__ = r"""

           Created on 15/03/2020
           """

from dash import dcc, html

from heimdallr.configuration.heimdallr_config import (
    BUILD_STATUS_INTERVAL,
    BUILD_STATUS_MAPPING,
)

__all__ = ["get_footer"]


def get_footer():
    """ """
    return html.Footer(
        [
            html.Div(
                [
                    html.P([f"{k}: "]),
                    html.A([html.Img(src=v)], href=v.split(".svg")[0]),
                ],
                className="col",
            )
            for k, v in BUILD_STATUS_MAPPING
        ]
        + [dcc.Interval(id=BUILD_STATUS_INTERVAL, interval=60 * 1000, n_intervals=0)],
        className="page-footer text-center row p-3",
    )


# TODO: https://bamboo.alexandra.dk/telemetry.action?filter=project&projectKey=WGDEMO
