#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "Christian Heider Nielsen"
__doc__ = r"""

           Created on 17/03/2020
           """

import getpass
import sys
from pathlib import Path

import sh

from heimdallr import PROJECT_NAME

__all__ = [
  "install_systemd_service",
  "remove_systemd_service",
  "enable_systemd_service",
  "disable_systemd_service",
  ]

"""
@sh.contrib("ls")
def my_ls(original):
  ls = original.bake("-l")
  return ls
"""


def install_systemd_service(service_entry_point_path: Path, service_name: str) -> None:
  assert service_entry_point_path.is_file() and service_entry_point_path.name.endswith(
    ".py"
    )
  service_name_a = f"{PROJECT_NAME}_{service_name}"
  user = getpass.getuser()
  systemd_service_file_path = f"/lib/systemd/system/{service_name_a}.service"
  print(f"Installing {systemd_service_file_path}")
  sudo = sh.sudo.bake(
    "-S", _in=getpass.getpass(prompt=f"[sudo] password for {user}: ")
    )
  sudo.touch(systemd_service_file_path)
  sudo.chown(f"{user}:{user}", systemd_service_file_path)
  with open(systemd_service_file_path, "w") as f:
    f.writelines(
      f"""[Unit]
Description={service_name_a} Service
After=multi-user.target

[Service]
Type=simple
ExecStart={sys.executable} {service_entry_point_path}

[Install]
WantedBy=multi-user.target"""
      )
  sudo.chmod("644", systemd_service_file_path)

  sudo.systemctl("daemon-reload")
  enable_systemd_service(service_name)


def remove_systemd_service(service_name: str) -> None:
  disable_systemd_service(service_name)
  target_service_file_path = (
    f"/lib/systemd/system/{PROJECT_NAME}_{service_name}.service"
  )
  print(f"Removing {target_service_file_path}")
  sudo = sh.sudo.bake(
    "-S", _in=getpass.getpass(prompt=f"[sudo] password for {getpass.getuser()}: ")
    )
  sudo.rm(target_service_file_path)
  sudo.systemctl("daemon-reload")


def enable_systemd_service(service_name: str) -> None:
  service_name_a = f"{PROJECT_NAME}_{service_name}"
  print(f"Enabling {service_name_a}")
  sudo = sh.sudo.bake(
    "-S", _in=getpass.getpass(prompt=f"[sudo] password for {getpass.getuser()}: ")
    )
  sudo.systemctl(f"enable", f"{service_name_a}.service")
  sudo.systemctl(f"start", f"{service_name_a}.service")


def disable_systemd_service(service_name: str) -> None:
  service_name_a = f"{PROJECT_NAME}_{service_name}"
  print(f"Disabling {service_name_a}")
  sudo = sh.sudo.bake(
    "-S", _in=getpass.getpass(prompt=f"[sudo] password for {getpass.getuser()}: ")
    )
  sudo.systemctl("stop", f"{service_name_a}.service")
  sudo.systemctl("disable", f"{service_name_a}.service")


if __name__ == "__main__":
  from heimdallr.entry_points import publisher

  # print()
  install_systemd_service(Path(publisher.__file__), "publisher")
  # print(sh.ls("/home/heider"))
  # print(sys.executable)

  # print(sh.systemctl('status', 'lightdm.service'))
