#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "Christian Heider Nielsen"
__doc__ = r"""

           Created on 15/03/2020
           """

import base64
from pathlib import Path

from dash import dcc, html

import heimdallr
from heimdallr.configuration.heimdallr_config import (
    HTML_TITLE,
    TIME_ID,
    TIME_INTERVAL_ID,
)

__all__ = ["get_header"]


def get_header() -> html.Div:
    """
    header
    """
    svg_p = Path(heimdallr.__file__).parent / "entry_points" / "assets" / "aivclab.svg"
    if svg_p.exists():
        with open(
            svg_p,
            "rb",
        ) as svg:
            encoded = base64.b64encode(svg.read())
    else:
        encoded = None

    return html.Div(
        [
            html.Div(
                [html.H1(HTML_TITLE)],
                className="col text-left align-self-center p-1",
            ),
            html.Div(
                []
                #     +[
                #         html.Img(
                #             src="/assets/alexandra.png",
                #             style={"height": "110px", "object-fit": "contain"},
                #         ),
                #     ]
                #     + (
                #         [
                #             html.Img(
                #                 src=f"data:image/svg+xml;base64,{encoded.decode()}",
                #                 # className='img-responsive',
                #                 style={"height": "110px", "object-fit": "contain"},
                #             )
                #         ]
                #         if encoded
                #         else []
                #     ),
                ,
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
