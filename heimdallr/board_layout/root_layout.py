#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from heimdallr.board_layout import get_footer, get_header
from heimdallr.board_layout.body import get_body

__author__ = "Christian Heider Nielsen"
__doc__ = ""

import dash_html_components as html


def get_root_layout():
  return html.Div(
    [get_header(), get_body(), get_footer(), ], className="container-fluid",
    )
