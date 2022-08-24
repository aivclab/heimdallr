#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "Christian Heider Nielsen"
__doc__ = r"""

           Created on 15/03/2020
           """

import datetime

__all__ = ["timestamp_to_datetime", "iso_dt_to_datetime"]

from warg import default_datetime_repr


def timestamp_to_datetime(t: int) -> str:
    """
    time stamp to datetime
    """
    return default_datetime_repr(datetime.datetime.fromtimestamp(t))


def iso_dt_to_datetime(t: str) -> str:
    """
    iso datetime to datetime
    """
    return default_datetime_repr(datetime.datetime.fromisoformat(t[:-1]))
