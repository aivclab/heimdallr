#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "Christian Heider Nielsen"
__doc__ = ""

import sys

from .date_tools import *
from .google_calendar import *
from .gpu_utilities import *
from .system_resources import *

if sys.platform[:3] == "win":
    from .windows_task_scheduler_utilities import *
else:
    pass

    # from .systemd_utilities import * # deprecated
