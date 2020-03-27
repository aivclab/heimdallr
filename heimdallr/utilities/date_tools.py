#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "Christian Heider Nielsen"
__doc__ = r"""

           Created on 15/03/2020
           """

import datetime

from draugr import default_datetime_repr

__all__ = ["timestamp2datetime", "isoformat2datetime"]


def timestamp2datetime(t: int) -> str:
  return default_datetime_repr(datetime.datetime.fromtimestamp(t))


def isoformat2datetime(t: str) -> str:
  return default_datetime_repr(datetime.datetime.fromisoformat(t[:-1]))
