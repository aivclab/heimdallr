#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "Christian Heider Nielsen"
__doc__ = r"""

           Created on 15/03/2020
           """

from itertools import cycle

from dash import dcc, html

from heimdallr.configuration.heimdallr_settings import HeimdallrSettings

# import dash_bootstrap_components #TODO

"""
import dash_bootstrap_components as dbc
import dash_html_components as html
from dash.dependencies import Input, Output, State

collapse = html.Div(
    [
        dbc.Button(
            "Open collapse",
            id="collapse-button",
            className="mb-3",
            color="primary",
            n_clicks=0,
        ),
        dbc.Collapse(
            dbc.Card(dbc.CardBody("This content is hidden in the collapse")),
            id="collapse",
            is_open=False,
        ),
    ]
)


@app.callback(
    Output("collapse", "is_open"),
    [Input("collapse-button", "n_clicks")],
    [State("collapse", "is_open")],
)
def toggle_collapse(n, is_open):
    if n:
        return not is_open
    return is_open

"""

__all__ = ["get_menu"]

ALLOWED_TYPES = (
    "text",
    "number",
    "password",
    "email",
    "search",
    "tel",
    "url",
    "range",
    "hidden",
)

"""
                  [
                      dcc.Input(
                          id=f"input_{inp_type}",
                          type=inp_type,
                          placeholder=f"input type {inp_type}",
                          )
                      for inp_type in ALLOWED_TYPES
                      ]
"""


def get_menu():
    """ """
    return html.Div(
        [
            html.Div(
                [
                    html.Div(
                        [html.Button("Show/Hide Menu", id="menu_toggle_button")],
                        className="row p-1",
                    ),
                    html.Div(
                        [
                            html.Form(
                                [
                                    dcc.Input(
                                        id=f"input_{k}",
                                        name=f"{k}",
                                        type=input_type,
                                        placeholder=f"{k}",
                                    )
                                    for k, input_type in zip(
                                        HeimdallrSettings().__to_dict__().keys(),
                                        cycle(("text",)),
                                    )
                                ]
                                + [html.Button("submit", type="submit")],
                                className="col text-center align-self-center p-1",
                                action="/config",
                                method="post",
                            ),
                        ],
                        className="row p-1",
                        id="menu_container",
                    ),
                ],
                className="col text-center align-self-center p-1",
            ),
        ],
        className="row p-1",
    )
