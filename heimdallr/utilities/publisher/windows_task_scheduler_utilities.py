#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "Christian"
__doc__ = r"""

           Created on 29/03/2020
           """

__all__ = ["disable_service", "remove_service", "install_service", "enable_service"]

from pathlib import Path

from draugr.os_utilities.windows_utilities import (
    delete_task,
    new_user_logon_execute_task,
    set_task_activity,
)


def disable_service(service_name: str) -> None:
    """
    disable service

    Args:
      service_name:
    """
    set_task_activity(service_name, False)


def enable_service(service_name: str) -> None:
    """
    enable service

    Args:
      service_name:
    """
    set_task_activity(service_name, True)


def install_service(service_name: str) -> None:
    """
    install service

    Args:
      service_name:
    """

    new_user_logon_execute_task(
        service_name,
        service_name,
        "python.exe",  # cmd.exe python.exe .....
        "-m heimdallr publish",
    )


def remove_service(service_name) -> None:
    """
    remove service

    Args:
      service_name:
    """
    delete_task(service_name)


if __name__ == "__main__":
    # remove_service("heimdallr_publisher")
    install_service("heimdallr_publisher")
    disable_service("heimdallr_publisher")
    # enable_service("heimdallr_publisher")
