#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "Christian Heider Nielsen"
__doc__ = r"""

           Created on 19/01/2020
           """

from enum import Enum
from functools import partial
from pathlib import Path
from typing import Any

import fire
from pyfiglet import Figlet

from draugr.python_utilities.styling import get_terminal_size
from heimdallr import get_version
from heimdallr.entry_points import publisher, server
from heimdallr.utilities import (
  disable_systemd_service,
  enable_systemd_service,
  install_systemd_service,
  remove_systemd_service,
  )
from heimdallr.utilities.heimdallr_settings import HeimdallrSettings

margin_percentage = 0 / 6
terminal_width = get_terminal_size().columns
margin = int(margin_percentage * terminal_width)
width = terminal_width - 2 * margin
underline = "_" * width
indent = " " * margin
sponsors = "Alexandra Institute"


class ServiceOption(Enum):
  install = "install"
  remove = "remove"
  disable = "disable"
  enable = "enable"


class HeimdallrMode(Enum):
  server = "server"
  publisher = "publisher"


class HeimdallrCLI:
  def __init__(self):
    for k in HeimdallrSettings():
      setattr(self, f"set_{k}", partial(self.set, k))
      setattr(self, f"get_{k}", partial(self.get, k))

  def server(self):
    server.main()

  def serve(self):
    self.server()

  def publisher(self):
    publisher.main()

  def publish(self):
    self.publisher()

  def set(self, setting: str, value: Any):
    HeimdallrSettings().__setattr__(setting, value)

  def get(self, setting: str):
    print(getattr(HeimdallrSettings(), setting))

  def service(self, option: ServiceOption, mode: HeimdallrMode):
    try:
      option = ServiceOption(option)
      mode = HeimdallrMode(mode)
      if option == ServiceOption.install:
        if mode == HeimdallrMode.server:
          install_systemd_service(Path(server.__file__), str(mode.value))
        elif mode == HeimdallrMode.publisher:
          install_systemd_service(Path(publisher.__file__), str(mode.value))
        else:
          raise Exception
      elif option == ServiceOption.remove:
        if mode in HeimdallrMode:
          remove_systemd_service(str(mode.value))
        else:
          raise Exception
      elif option == ServiceOption.enable:
        if mode in HeimdallrMode:
          enable_systemd_service(str(mode.value))
        else:
          raise Exception
      elif option == ServiceOption.disable:
        if mode in HeimdallrMode:
          disable_systemd_service(str(mode.value))
        else:
          raise Exception
      else:
        raise Exception
      print(
        f'{str(option.value).capitalize().rstrip("e")}ed the Heimdallr',
        mode.value,
        "service",
        )
    except ValueError as a:
      print(a)
      print(f"Valid options {list(ServiceOption.__iter__())}")
      print(f"Valid modes {list(HeimdallrMode.__iter__())}")

  @staticmethod
  def version() -> None:
    """
Prints the version of this Neodroid installation.
"""
    draw_cli_header()
    print(f"Version: {get_version()}")

  @staticmethod
  def sponsors() -> None:
    print(sponsors)


def draw_cli_header(*, title="Heimdallr", font="big"):
  figlet = Figlet(font=font, justify="center", width=terminal_width)
  description = figlet.renderText(title)

  print(f"{description}{underline}\n")


def main(*, always_draw_header=False):
  if always_draw_header:
    draw_cli_header()
  fire.Fire(HeimdallrCLI, name="heimdallr")


if __name__ == "__main__":
  main()
