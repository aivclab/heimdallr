#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "Christian Heider Nielsen"
__doc__ = r"""

           Created on 17/03/2020
           """

import getpass
import shelve
from enum import Enum
from typing import Optional

import sh
from sorcery import assigned_names

from apppath import ensure_existence
from heimdallr import PROJECT_APP_PATH
from warg import PropertySettings

__all__ = [
    "HeimdallrSettings",  # Setting Class
    "SettingScopeEnum",  # Setting scope Enum
    "set_all_heimdallr_settings",  # Set settings function
]


# PropertySettings.raise_exception_on_none = False


class SettingScopeEnum(Enum):
    """ """

    user, site, root = assigned_names()


class HeimdallrSettings(PropertySettings):
    """ """

    _setting_scope = None
    _google_settings_path = None
    _mqtt_settings_path = None
    _credentials_base_path = None

    def __init__(self, setting_scope: SettingScopeEnum = SettingScopeEnum.user):
        """Protects from overriding on initialisation"""
        pass
        # super().__init__()
        # TODO: FIGURE OUT A WAY TO EASILY COPY SETTINGS TO ROOT; for services
        # print(f'Using settings from {PROJECT_APP_PATH.user_config}')

        _setting_scope = setting_scope
        if setting_scope == SettingScopeEnum.user:
            HeimdallrSettings._credentials_base_path = ensure_existence(
                PROJECT_APP_PATH.user_config / "credentials"
            )
            HeimdallrSettings._google_settings_path = str(
                ensure_existence(PROJECT_APP_PATH.user_config) / "google.settings"
            )
            HeimdallrSettings._mqtt_settings_path = str(
                ensure_existence(PROJECT_APP_PATH.user_config) / "mqtt.settings"
            )

            # print(f'Using config at {PROJECT_APP_PATH.site_config}')
        elif setting_scope == SettingScopeEnum.site:
            prev_val = PROJECT_APP_PATH._ensure_existence
            PROJECT_APP_PATH._ensure_existence = False
            HeimdallrSettings._credentials_base_path = (
                PROJECT_APP_PATH.site_config / "credentials"
            )
            if not HeimdallrSettings._credentials_base_path.exists():
                with sh.contrib.sudo(
                    password=getpass.getpass(
                        prompt=f"[sudo] password for {getpass.getuser()}: "
                    ),
                    _with=True,
                ):
                    sh.mkdir(["-p", HeimdallrSettings._credentials_base_path])
                    sh.chown(
                        f"{getpass.getuser()}:", PROJECT_APP_PATH.site_config
                    )  # If a colon but no group name follows the user name, that user is made the owner of the files and the group of the files is changed to that user's login group.
            PROJECT_APP_PATH._ensure_existence = prev_val
            HeimdallrSettings._google_settings_path = str(
                ensure_existence(PROJECT_APP_PATH.site_config) / "google.settings"
            )
            HeimdallrSettings._mqtt_settings_path = str(
                ensure_existence(PROJECT_APP_PATH.site_config) / "mqtt.settings"
            )

            # print(f'Using config at {PROJECT_APP_PATH.site_config}')
        elif setting_scope == SettingScopeEnum.root:
            prev_val = PROJECT_APP_PATH._ensure_existence
            PROJECT_APP_PATH._ensure_existence = False
            HeimdallrSettings._credentials_base_path = (
                PROJECT_APP_PATH.root_config / "credentials"
            )
            if not HeimdallrSettings._credentials_base_path.exists():
                with sh.contrib.sudo(
                    password=getpass.getpass(
                        prompt=f"[sudo] password for {getpass.getuser()}: "
                    ),
                    _with=True,
                ):
                    sh.mkdir(["-p", HeimdallrSettings._credentials_base_path])
                    sh.chown(
                        f"{getpass.getuser()}:", PROJECT_APP_PATH.root_config
                    )  # If a colon but no group name follows the user name, that user is made the owner of the files and the group of the files is changed to that user's login group.
            PROJECT_APP_PATH._ensure_existence = prev_val
            HeimdallrSettings._google_settings_path = str(
                ensure_existence(PROJECT_APP_PATH.root_config) / "google.settings"
            )
            HeimdallrSettings._mqtt_settings_path = str(
                ensure_existence(PROJECT_APP_PATH.root_config) / "mqtt.settings"
            )

            # print(f'Using config at {PROJECT_APP_PATH.site_config}')
        else:
            raise ValueError()

    @property
    def google_calendar_id(self) -> Optional[str]:
        """ """
        with shelve.open(HeimdallrSettings._google_settings_path) as d:
            if "google_calendar_id" in d:
                return d["google_calendar_id"]
        return None

    @google_calendar_id.setter
    def google_calendar_id(self, calendar_id: str) -> None:
        with shelve.open(HeimdallrSettings._google_settings_path, writeback=True) as d:
            d["google_calendar_id"] = calendar_id

    @property
    def mqtt_access_token(self) -> Optional[str]:
        """ """
        with shelve.open(HeimdallrSettings._mqtt_settings_path) as d:
            if "mqtt_access_token" in d:
                return d["mqtt_access_token"]
        return None

    @mqtt_access_token.setter
    def mqtt_access_token(self, token: str) -> None:
        with shelve.open(HeimdallrSettings._mqtt_settings_path, writeback=True) as d:
            d["mqtt_access_token"] = token

    @property
    def mqtt_username(self) -> Optional[str]:
        """ """
        with shelve.open(HeimdallrSettings._mqtt_settings_path) as d:
            if "mqtt_username" in d:
                return d["mqtt_username"]
        return None

    @mqtt_username.setter
    def mqtt_username(self, username: str) -> None:
        with shelve.open(HeimdallrSettings._mqtt_settings_path, writeback=True) as d:
            d["mqtt_username"] = username

    @property
    def mqtt_password(self) -> Optional[str]:
        """ """
        with shelve.open(HeimdallrSettings._mqtt_settings_path) as d:
            if "mqtt_password" in d:
                return d["mqtt_password"]
        return None

    @mqtt_password.setter
    def mqtt_password(self, password: str) -> None:
        with shelve.open(HeimdallrSettings._mqtt_settings_path, writeback=True) as d:
            d["mqtt_password"] = password

    @property
    def mqtt_broker(self) -> Optional[str]:
        """ """
        with shelve.open(HeimdallrSettings._mqtt_settings_path) as d:
            if "mqtt_broker" in d:
                return d["mqtt_broker"]
        return None

    @mqtt_broker.setter
    def mqtt_broker(self, broker: str) -> None:
        with shelve.open(HeimdallrSettings._mqtt_settings_path, writeback=True) as d:
            d["mqtt_broker"] = broker

    @property
    def mqtt_port(self) -> Optional[str]:
        """ """
        with shelve.open(HeimdallrSettings._mqtt_settings_path) as d:
            if "mqtt_port" in d:
                return d["mqtt_port"]
        return None

    @mqtt_port.setter
    def mqtt_port(self, port: int) -> None:
        with shelve.open(HeimdallrSettings._mqtt_settings_path, writeback=True) as d:
            d["mqtt_port"] = port


def set_all_heimdallr_settings(
    setting_scope: SettingScopeEnum = SettingScopeEnum.user,
    *,
    _lower_keys: bool = True,
    **kwargs,
):
    """ """
    HEIMDALLR_SETTINGS = HeimdallrSettings(setting_scope)
    # print(f"current heimdallr settings: {HEIMDALLR_SETTINGS}")
    if _lower_keys:
        kwargs = {k.lower(): v for k, v in kwargs.items()}

    # for k in kwargs.keys():
    #    assert k in HEIMDALLR_SETTINGS, f'"{k}" is not in Heimdallrs settings'

    for k in HEIMDALLR_SETTINGS:
        assert k in kwargs.keys(), f'Missing "{k}" from kwargs'

    HEIMDALLR_SETTINGS.__from_dict__(kwargs)

    print(f"new heimdallr settings: {HeimdallrSettings()}")


if __name__ == "__main__":
    settings = HeimdallrSettings()

    for k in settings:
        print(k)

    set_all_heimdallr_settings(
        **{
            k: getattr(settings, k) if getattr(settings, k) else None
            for k in iter(settings)
        }
    )
