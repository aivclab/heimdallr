#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "Christian Heider Nielsen"
__doc__ = r"""

           Created on 19/03/2020
           """

import time

import psutil

from heimdallr.utilities.nvidia import bindings
from warg import NOD

try:
  bindings.nvmlInit()
except Exception as e:
  print(e)


def get_nv_info(include_graphics_processes: bool = True):
  devices = []
  try:
    driver_version = bindings.nvmlSystemGetDriverVersion().decode()
    device_count = bindings.nvmlDeviceGetCount()

    for device_i in range(device_count):
      handle = bindings.nvmlDeviceGetHandleByIndex(device_i)
      device_name = bindings.nvmlDeviceGetName(handle).decode()
      gpu_mem_info = bindings.nvmlDeviceGetMemoryInfo(handle)

      gpu_processes = bindings.nvmlDeviceGetComputeRunningProcesses(handle)
      if include_graphics_processes:
        gpu_processes = (
          gpu_processes
          + bindings.nvmlDeviceGetGraphicsRunningProcesses(handle)
        )

      processes_info = []

      for p in gpu_processes:
        pid = p.pid
        used_gpu_mem = p.usedGpuMemory
        p = psutil.Process(pid=pid)
        _ = p.cpu_percent()
        time.sleep(
          0.1
          )  # Recommended to preprobe and sleep for atleast 0.1 seconds.
        processes_info.append(
          NOD(
            used_gpu_mem=used_gpu_mem,
            device_idx=device_i,
            name=p.name(),
            username=p.username(),
            memory_percent=p.memory_percent(),
            cpu_percent=p.cpu_percent(),
            cmdline=" ".join(p.cmdline()),
            device_name=device_name,
            create_time=p.create_time(),
            status=p.status(),
            pid=pid,
            ).as_dict()
          )

      """
try:
  fan_speed = pynvml.nvmlDeviceGetFanSpeed(handle)
  power_usage = pynvml.nvmlDeviceGetPowerUsage(handle)  # milliwatts mW
except pynvml.NVMLError_NotSupported as e:
  fan_speed = None
  power_usage = None

power_state = pynvml.nvmlDeviceGetPowerState(handle)
temperature = pynvml.nvmlDeviceGetTemperature(handle, pynvml.NVML_TEMPERATURE_GPU)
"""

      devices.append(
        NOD(
          id=device_i,
          name=device_name,
          free=gpu_mem_info.free,
          used=gpu_mem_info.used,
          total=gpu_mem_info.total,
          processes=processes_info,
          ).as_dict()
        )
  except Exception as e:
    print(e)
    driver_version = "No nvidia driver"

  return driver_version, devices
