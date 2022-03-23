#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "Christian"
__doc__ = r"""

           Created on 29/03/2020
           """


import sys

from .system_resources import *

if sys.platform[:3] == "win":
    from .windows_task_scheduler_utilities import *
else:
    pass
    # TODO: USE DRAUGR FOR NOW; make wrapper for platform agnostic behaviour later
    # from draugr.os_utilities.linux_utilities.systemd_utilities import *

    # from .systemd_utilities import * # deprecated
