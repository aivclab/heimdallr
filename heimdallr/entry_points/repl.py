#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "Christian Heider Nielsen"
__doc__ = r"""

           Created on 19/01/2020
           """

from draugr import ConfigShell

from pyfiglet import Figlet

from heimdallr.configuration.heimdallr_settings import (
    HeimdallrSettings,
    SettingScopeEnum,
)
import warg

margin_percentage = 0 / 6
terminal_width = warg.get_terminal_size().columns
margin = int(margin_percentage * terminal_width)
width = terminal_width - 2 * margin
underline = "_" * width
indent = " " * margin
sponsors = "Alexandra Institute"


def draw_cli_header(
    *, title: str = "Heimdallr", font: str = "big", drawer: callable = print
) -> None:
    """description"""
    drawer(
        f"{Figlet(font = font, justify = 'center', width = terminal_width).renderText(title)}{underline}\n"
    )


def main(
    *,
    always_draw_header: bool = False,
    setting_scope: SettingScopeEnum = SettingScopeEnum.user,
) -> None:
    """description"""
    if always_draw_header:
        draw_cli_header()

    repl = ConfigShell("heimdallr")
    repl.add_property_options(HeimdallrSettings(setting_scope=setting_scope))
    repl.add_func("sponsor", lambda *e: print(sponsors))
    repl.cmdloop()


if __name__ == "__main__":
    main()
