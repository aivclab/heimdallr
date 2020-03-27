#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "Christian Heider Nielsen"
__doc__ = ""

from warg import NOD

SERVER_ADDRESS = "0.0.0.0"
SERVER_PORT = 5555

TABLE_PAGE_SIZE = 30
TIMEOUT_MACHINES_SEC = 20  # SECONDS

MQTT_TOPIC = "v1/gpu/status"
MQTT_PUBLISH_INTERVAL_SEC = 2  # SECONDS
MQTT_QOS = 0  # At most once (0), At least once (1), Exactly once (2)

HTML_TITLE = "VCLab Board"

GPU_GRAPHS_ID = "gpu-graphs"
GPU_TABLES_ID = "gpu-tables"
GPU_INTERVAL_ID = "gpu-interval"
GPU_INTERVAL_MS = MQTT_PUBLISH_INTERVAL_SEC * 1000

INT_COLUMNS = ["device_idx", "pid"]  # "cpu_num", "num_threads"]
PERCENT_COLUMNS = ["cpu_percent", "memory_percent"]
MB_COLUMNS = ["used_gpu_mem"]
DROP_COLUMNS = ["cmdline", "cpu_percent", "memory_percent"]

TIME_ID = "time-text"
TIME_INTERVAL_ID = "time-interval"

CALENDAR_INTERVAL_ID = "calender-interval"
CALENDAR_ID = "calender-table"
CALENDAR_INTERVAL_MS = 1000 * 60 * 60

BUILD_STATUS_MAPPING = NOD(
  streamserver="https://travis-ci.org/aivclab/streamserver.svg?branch=master",
  dlcourse="https://github.com/aivclab/dlcourse.svg?branch=master",
  poserecorder="https://github.com/aivclab/pose-recorder.svg",
  vision="https://travis-ci.com/aivclab/vision.svg?branch=master",
  RayKarsten="https://github.com/aivclab/RayKarstenWebAsm.svg",
  dmr="https://github.com/aivclab/dmr.svg",
  )
BUILD_STATUS_INTERVAL = "build-status-interval"

DEBUG = True

ALL_CONSTANTS = NOD(locals())
