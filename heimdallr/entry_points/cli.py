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

    (
        install,
        remove,
        uninstall,
        disable,
        enable,
        start,
        stop,
        restart,
        status,
    ) = assigned_names()  # same


class HeimdallrMode(Enum):
    """ """

    server, publisher = assigned_names()


class HeimdallrCLI:
    """ """

    def __init__(self, *, setting_scope: SettingScopeEnum = SettingScopeEnum.user):
        try:
            self.setting_scope = SettingScopeEnum(setting_scope)
        except ValueError as a:
            print(f"Valid options {list(SettingScopeEnum.__iter__())}")
            raise a

        for k in HeimdallrSettings(setting_scope=self.setting_scope):
            setattr(self, f"set_{k}", partial(self.set, k))
            setattr(self, f"get_{k}", partial(self.get, k))

    def serve(self):
        """serve metrics at localhost:5555"""
        from heimdallr.entry_points import server

        server.main(setting_scope=SettingScopeEnum(self.setting_scope))

    def publish(self):
        """publish metrics"""
        from heimdallr.entry_points import publisher

        publisher.main(setting_scope=SettingScopeEnum(self.setting_scope))

    def set(
        self,
        setting: str,
        value: Any,
    ) -> None:
        """Setting options: [mqtt_access_token, mqtt_username, mqtt_password, mqtt_broker, mqtt_port]"""
        print(self.setting_scope)
        settings = HeimdallrSettings(setting_scope=self.setting_scope)
        print(settings._mqtt_settings_path)
        settings.__setattr__(setting, value)

    def multi_set(self, **kw) -> None:
        """prefix kwargs sequence with a '-' eg. 'heimdallr multi_set -mqtt_port=9213' Setting options: [
        mqtt_access_token,
        mqtt_username,
        mqtt_password,
        mqtt_broker,
        mqtt_port]"""
        settings = HeimdallrSettings(SettingScopeEnum(self.setting_scope))
        for setting, value in kw.items():
            settings.__setattr__(setting, value)

    def get(self, setting: str) -> None:
        """Setting options: [mqtt_access_token, mqtt_username, mqtt_password, mqtt_broker, mqtt_port, all]"""
        print(self.setting_scope)
        settings = HeimdallrSettings(setting_scope=self.setting_scope)
        print(settings._mqtt_settings_path)
        if setting == "all":
            print(settings)
        else:
            print(getattr(settings, setting))

    def service(
        self,
        option: ServiceOption,
        mode: HeimdallrMode,
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
            if self.setting_scope == SettingScopeEnum.user:
                run_as = RunAsEnum.user
            elif self.setting_scope == SettingScopeEnum.root:
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
            elif option == ServiceOption.remove or option == ServiceOption.uninstall:
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
