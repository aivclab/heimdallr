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
from sorcery import assigned_names

from draugr.python_utilities import get_terminal_size
from heimdallr import get_version
from heimdallr.configuration.heimdallr_settings import (
    HeimdallrSettings,
    SettingScopeEnum,
)

margin_percentage = 0 / 6
terminal_width = get_terminal_size().columns
margin = int(margin_percentage * terminal_width)
width = terminal_width - 2 * margin
underline = "_" * width
indent = " " * margin
sponsors = "Alexandra Institute"


class ServiceOption(Enum):
    """ """

    install, remove, disable, enable, start, stop, restart, status = assigned_names()


class HeimdallrMode(Enum):
    """ """

    server, publisher = assigned_names()


class HeimdallrCLI:
    """ """

    def __init__(self, user_settings: SettingScopeEnum = SettingScopeEnum.site):
        for k in HeimdallrSettings(user_settings):
            setattr(self, f"set_{k}", partial(self.set, k))
            setattr(self, f"get_{k}", partial(self.get, k))

    @staticmethod
    def serve():
        """serve metrics at localhost:5555"""
        from heimdallr.entry_points import server

        server.main()

    @staticmethod
    def publish():
        """publish metrics"""
        from heimdallr.entry_points import publisher

        publisher.main()

    @staticmethod
    def set(
        setting: str,
        value: Any,
        user_settings: SettingScopeEnum = SettingScopeEnum.site,
    ) -> None:
        """Setting options: [mqtt_access_token, mqtt_username, mqtt_password, mqtt_broker, mqtt_port]"""
        HeimdallrSettings(user_settings).__setattr__(setting, value)

    @staticmethod
    def multi_set(
        user_settings: SettingScopeEnum = SettingScopeEnum.site, **kw
    ) -> None:
        """Setting options: [mqtt_access_token, mqtt_username, mqtt_password, mqtt_broker, mqtt_port]"""
        settings = HeimdallrSettings(user_settings)
        for setting, value in kw.items():
            settings.__setattr__(setting, value)

    @staticmethod
    def get(
        setting: str, user_settings: SettingScopeEnum = SettingScopeEnum.site
    ) -> None:
        """Setting options: [mqtt_access_token, mqtt_username, mqtt_password, mqtt_broker, mqtt_port, all]"""
        if setting == "all":
            print(HeimdallrSettings(user_settings))
        else:
            print(getattr(HeimdallrSettings(user_settings), setting))

    @staticmethod
    def service(
        option: ServiceOption,
        mode: HeimdallrMode,
        scope: SettingScopeEnum = SettingScopeEnum.site,
    ):
        """
        Only support systemd implementation
        TODO: support Windows tasks
        """
        try:
            option = ServiceOption(option)
            mode = HeimdallrMode(mode)
            service_name = f"heimdallr_{mode.value}"

            from draugr.os_utilities.linux_utilities import RunAsEnum

            run_as = RunAsEnum.app_user
            if scope == SettingScopeEnum.user:
                run_as = RunAsEnum.user
            elif scope == SettingScopeEnum.root:
                run_as = RunAsEnum.root

            if option == ServiceOption.install:
                from draugr.os_utilities.linux_utilities import (
                    install_service,
                )

                if mode == HeimdallrMode.server:
                    from heimdallr.entry_points import server

                    install_service(Path(server.__file__), service_name, run_as=run_as)
                elif mode == HeimdallrMode.publisher:
                    from heimdallr.entry_points import publisher

                    install_service(
                        Path(publisher.__file__), service_name, run_as=run_as
                    )
                else:
                    raise Exception
            elif option == ServiceOption.remove:
                if mode in HeimdallrMode:
                    from draugr.os_utilities.linux_utilities import (
                        remove_service,
                    )

                    remove_service(service_name, run_as=run_as)
                else:
                    raise Exception
            elif option == ServiceOption.enable:
                if mode in HeimdallrMode:
                    from draugr.os_utilities.linux_utilities import (
                        enable_service,
                    )

                    enable_service(service_name, run_as=run_as)
                else:
                    raise Exception
            elif option == ServiceOption.disable:
                if mode in HeimdallrMode:
                    from draugr.os_utilities.linux_utilities import (
                        disable_service,
                    )

                    disable_service(service_name, run_as=run_as)
                else:
                    raise Exception
            elif option == ServiceOption.start:
                if mode in HeimdallrMode:
                    from draugr.os_utilities.linux_utilities import (
                        start_service,
                    )

                    start_service(service_name, run_as=run_as)
                else:
                    raise Exception
            elif option == ServiceOption.stop:
                if mode in HeimdallrMode:
                    from draugr.os_utilities.linux_utilities import (
                        stop_service,
                    )

                    stop_service(service_name, run_as=run_as)
                else:
                    raise Exception
            elif option == ServiceOption.restart:
                if mode in HeimdallrMode:
                    from draugr.os_utilities.linux_utilities import (
                        restart_service,
                    )

                    restart_service(service_name, run_as=run_as)
                else:
                    raise Exception
            elif option == ServiceOption.status:
                if mode in HeimdallrMode:
                    from draugr.os_utilities.linux_utilities import (
                        status_service,
                    )

                    status_service(service_name, run_as=run_as)
                else:
                    raise Exception
            else:
                raise Exception
            message = str(option.value).capitalize().rstrip("e")
            if message[-1] == "p":  # E.g. stop -> stop+p(ed)
                # A little bit yucky
                message += "p"
            print(
                f"{message}ed the Heimdallr",
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
        Prints the version of this Heimdallr installation."""
        draw_cli_header()
        print(f"Version: {get_version()}")

    @staticmethod
    def sponsors(*, drawer: callable = print) -> None:
        """emits sponsors"""
        drawer(sponsors)


def draw_cli_header(
    *, title: str = "Heimdallr", font: str = "big", drawer: callable = print
):
    """ """
    drawer(
        f"{Figlet(font=font, justify='center', width=terminal_width).renderText(title)}{underline}\n"
    )


def main(*, always_draw_header: bool = False):
    """ """
    if always_draw_header:
        draw_cli_header()
    fire.Fire(HeimdallrCLI, name="heimdallr")


if __name__ == "__main__":
    main()
