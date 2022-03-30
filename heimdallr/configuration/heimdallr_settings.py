#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "Christian Heider Nielsen"
__doc__ = r"""

           Created on 17/03/2020
           """

import getpass
import inspect
import os

import shelve
from enum import Enum
from typing import Union

from warg.os_platform import is_nix

if is_nix():
    try:
        import sh
    except (ImportError, ModuleNotFoundError) as e:
        print(e)
        print("Please install sh and dependencies")

from sorcery import assigned_names

from apppath import ensure_existence
from heimdallr import PROJECT_APP_PATH
from warg import PropertySettings, is_windows

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
    _github_settings_path = None
    _credentials_base_path = None
    _teams_settings_path = None
    _look_up_env_on_missing = True

    def __init__(self, setting_scope: SettingScopeEnum = SettingScopeEnum.user):
        """Protects from overriding on initialisation"""
        pass
        # super().__init__()
        # TODO: FIGURE OUT A WAY TO EASILY COPY SETTINGS TO ROOT; for services
        # print(f'Using settings from {PROJECT_APP_PATH.user_config}')

        _setting_scope = setting_scope
        if setting_scope == SettingScopeEnum.user or is_windows():
            p = PROJECT_APP_PATH.user_config
        elif setting_scope == SettingScopeEnum.site and is_nix():
            p = PROJECT_APP_PATH.site_config
            if not p.exists():
                with sh.contrib.sudo(
                    password=getpass.getpass(
                        prompt=f"[sudo] password for {getpass.getuser()}: "
                    ),
                    _with=True,
                ):
                    sh.chown(
                        f"{getpass.getuser()}:", PROJECT_APP_PATH.site_config
                    )  # If a colon but no group name follows the user name, that user is made the owner of the files and the group of the files is changed to that user's login group.
        elif setting_scope == SettingScopeEnum.root and is_nix():
            p = PROJECT_APP_PATH.root_config
            if not HeimdallrSettings._credentials_base_path.exists():
                with sh.contrib.sudo(
                    password=getpass.getpass(
                        prompt=f"[sudo] password for {getpass.getuser()}: "
                    ),
                    _with=True,
                ):
                    sh.chown(
                        f"{getpass.getuser()}:", PROJECT_APP_PATH.root_config
                    )  # If a colon but no group name follows the user name, that user is made the owner of the files and the group of the files is changed to that user's login group.
        else:
            raise ValueError(
                "Invalid setting scope",
                setting_scope,
            )

        HeimdallrSettings._credentials_base_path = ensure_existence(p / "credentials")
        HeimdallrSettings._mqtt_settings_path = ensure_existence(p / "google.settings")
        HeimdallrSettings._google_settings_path = ensure_existence(p / "mqtt.settings")
        HeimdallrSettings._github_settings_path = ensure_existence(
            p / "github.settings"
        )
        HeimdallrSettings._teams_settings_path = ensure_existence(p / "teams.settings")

    @property
    def teams_config(self) -> Union[object, dict, None]:
        """ """
        key = inspect.currentframe().f_code.co_name
        with shelve.open(str(HeimdallrSettings._teams_settings_path)) as d:
            if key in d:
                return d[key]
        if self._look_up_env_on_missing:
            return os.environ.get(key)
        return None

    @teams_config.setter
    def teams_config(self, config: dict) -> None:
        """

        Args:
            config ():

        Returns:

        """
        key = inspect.currentframe().f_code.co_name
        with shelve.open(
            str(HeimdallrSettings._teams_settings_path, writeback=True)
        ) as d:
            d[key] = config

    @property
    def google_calendar_id(self) -> Union[object, str, None]:
        """ """
        key = inspect.currentframe().f_code.co_name
        with shelve.open(str(HeimdallrSettings._google_settings_path)) as d:
            if key in d:
                return d[key]
        if self._look_up_env_on_missing:
            return os.environ.get(key)
        return None

    @google_calendar_id.setter
    def google_calendar_id(self, calendar_id: str) -> None:
        """

        Args:
            calendar_id ():

        Returns:

        """
        key = inspect.currentframe().f_code.co_name
        with shelve.open(
            str(HeimdallrSettings._google_settings_path, writeback=True)
        ) as d:
            d[key] = calendar_id

    @google_calendar_id.deleter
    def google_calendar_id(self) -> None:
        """

        Args:
            calendar_id ():

        Returns:

        """
        key = inspect.currentframe().f_code.co_name
        with shelve.open(
            str(HeimdallrSettings._github_settings_path, writeback=True)
        ) as d:
            del d[key]

    @property
    def github_token(self) -> Union[object, str, None]:
        """ """
        key = inspect.currentframe().f_code.co_name
        with shelve.open(str(HeimdallrSettings._github_settings_path)) as d:
            if key in d:
                return d[key]
        if self._look_up_env_on_missing:
            return os.environ.get(key)
        return None

    @github_token.setter
    def github_token(self, calendar_id: str) -> None:
        """

        Args:
            calendar_id ():

        Returns:

        """
        key = inspect.currentframe().f_code.co_name
        with shelve.open(
            str(HeimdallrSettings._github_settings_path, writeback=True)
        ) as d:
            d[key] = calendar_id

    @github_token.deleter
    def github_token(self) -> None:
        """

        Args:
            calendar_id ():

        Returns:

        """
        key = inspect.currentframe().f_code.co_name
        with shelve.open(
            str(HeimdallrSettings._github_settings_path, writeback=True)
        ) as d:
            del d[key]

    '''
  @property
  def mqtt_access_token(self) -> Optional[str]:
      """ """
      key = inspect.currentframe().f_code.co_name
      with shelve.open(str(HeimdallrSettings._mqtt_settings_path)) as d:
          if key in d:
              return d[key]
      if self._look_up_env_on_missing:
          return os.environ.get(key)
      return None

  @mqtt_access_token.setter
  def mqtt_access_token(self, token: str) -> None:
      key = inspect.currentframe().f_code.co_name
      with shelve.open(str(HeimdallrSettings._mqtt_settings_path, writeback=True)) as d:
          d[key] = token
  '''

    @property
    def mqtt_username(self) -> Union[object, str, None]:
        """ """
        key = inspect.currentframe().f_code.co_name
        with shelve.open(str(HeimdallrSettings._mqtt_settings_path)) as d:
            if key in d:
                return d[key]
        if self._look_up_env_on_missing:
            return os.environ.get(key)
        return None

    @mqtt_username.setter
    def mqtt_username(self, username: str) -> None:
        """

        Args:
            username ():

        Returns:

        """
        key = inspect.currentframe().f_code.co_name
        with shelve.open(
            str(HeimdallrSettings._mqtt_settings_path, writeback=True)
        ) as d:
            d[key] = username

    @mqtt_username.deleter
    def mqtt_username(self) -> None:
        """

        Returns:

        """
        key = inspect.currentframe().f_code.co_name
        with shelve.open(
            str(HeimdallrSettings._mqtt_settings_path, writeback=True)
        ) as d:
            del d[key]

    @property
    def mqtt_password(self) -> Union[object, str, None]:
        """ """
        key = inspect.currentframe().f_code.co_name
        with shelve.open(str(HeimdallrSettings._mqtt_settings_path)) as d:
            if key in d:
                return d[key]
        if self._look_up_env_on_missing:
            return os.environ.get(key)
        return None

    @mqtt_password.setter
    def mqtt_password(self, password: str) -> None:
        """

        Args:
            password ():

        Returns:

        """
        key = inspect.currentframe().f_code.co_name
        with shelve.open(
            str(HeimdallrSettings._mqtt_settings_path, writeback=True)
        ) as d:
            d[key] = password

    @mqtt_password.deleter
    def mqtt_password(self) -> None:
        """

        Returns:

        """
        key = inspect.currentframe().f_code.co_name
        with shelve.open(
            str(HeimdallrSettings._mqtt_settings_path, writeback=True)
        ) as d:
            del d[key]

    @property
    def mqtt_broker(self) -> Union[object, str, None]:
        """ """
        key = inspect.currentframe().f_code.co_name
        with shelve.open(str(HeimdallrSettings._mqtt_settings_path)) as d:
            if key in d:
                return d[key]
        if self._look_up_env_on_missing:
            return os.environ.get(key)
        return None

    @mqtt_broker.setter
    def mqtt_broker(self, broker: str) -> None:
        """

        Args:
            broker ():

        Returns:

        """
        key = inspect.currentframe().f_code.co_name
        with shelve.open(
            str(HeimdallrSettings._mqtt_settings_path, writeback=True)
        ) as d:
            d[key] = broker

    @mqtt_broker.deleter
    def mqtt_broker(self) -> None:
        """

        Returns:

        """
        key = inspect.currentframe().f_code.co_name
        with shelve.open(
            str(HeimdallrSettings._mqtt_settings_path, writeback=True)
        ) as d:
            del d[key]

    @property
    def mqtt_port(self) -> Union[object, str, None]:
        """ """
        key = inspect.currentframe().f_code.co_name
        with shelve.open(str(HeimdallrSettings._mqtt_settings_path)) as d:
            if key in d:
                return d[key]
        if self._look_up_env_on_missing:
            return os.environ.get(key)
        return None

    @mqtt_port.setter
    def mqtt_port(self, port: int) -> None:
        """

        Args:
            port ():

        Returns:

        """
        key = inspect.currentframe().f_code.co_name
        with shelve.open(
            str(HeimdallrSettings._mqtt_settings_path, writeback=True)
        ) as d:
            d[key] = port

    @mqtt_port.deleter
    def mqtt_port(self) -> None:
        """

        Returns:

        """
        key = inspect.currentframe().f_code.co_name
        with shelve.open(
            str(HeimdallrSettings._mqtt_settings_path, writeback=True)
        ) as d:
            del d[key]


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
        print(k, settings[k])

    """
  set_all_heimdallr_settings(
      **{
          k: getattr(settings, k) if getattr(settings, k) else None
          for k in iter(settings)
      }
  )
  """
