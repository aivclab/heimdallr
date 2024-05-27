#!/usr/bin/env python3
# -*- coding: utf-8 -*-

try:
    from importlib.resources import files
    from importlib.metadata import PackageNotFoundError
except (ModuleNotFoundError, ImportError) as e:
    from importlib_metadata import PackageNotFoundError
    from importlib_resources import files

from apppath import AppPath
from warg import clean_string, get_version, package_is_editable

__project__ = "Heimdallr"
__author__ = "Christian Heider Nielsen"
__version__ = "0.2.8"
__doc__ = """
Created on 27/04/2019

@author: cnheider
"""

# __all__ = ["PROJECT_APP_PATH", "PROJECT_NAME", "PROJECT_VERSION", "get_version"]


PROJECT_NAME = clean_string(__project__)
PROJECT_VERSION = __version__
PROJECT_YEAR = 2019
PROJECT_AUTHOR = clean_string(__author__)
PROJECT_ORGANISATION = clean_string("Aivclab")
PROJECT_APP_PATH = AppPath(app_name=PROJECT_NAME, app_author=PROJECT_AUTHOR)

PACKAGE_DATA_PATH = files(PROJECT_NAME) / "data"

try:
    DEVELOP = package_is_editable(PROJECT_NAME)
except PackageNotFoundError as e:
    DEVELOP = True

__version__ = get_version(__version__, append_time=DEVELOP)
__version_info__ = tuple(int(segment) for segment in __version__.split("."))

if __name__ == "__main__":
    print(__project__, __version_info__)
