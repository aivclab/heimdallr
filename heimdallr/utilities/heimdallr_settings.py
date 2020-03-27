#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "Christian Heider Nielsen"
__doc__ = r"""

           Created on 17/03/2020
           """

import shelve

from heimdallr import PROJECT_APP_PATH
from warg import PropertySettings

__all__ = [
  "HeimdallrSettings",  # Class
  "set_all_heimdallr_settings"  # Set settings function
  ]


class HeimdallrSettings(PropertySettings):
  _google_settings_path = str(PROJECT_APP_PATH.user_config / "google.settings")
  _mqtt_settings_path = str(PROJECT_APP_PATH.user_config / "mqtt.settings")

  def __init__(self):
    """Protects from overriding on initialisation"""
    pass
    # super().__init__()
    # TODO: FIGURE OUT A WAY TO EASILY COPY SETTINGS TO ROOT; for services
    # print(f'Using settings from {PROJECT_APP_PATH.user_config}')

  @property
  def google_calendar_id(self) -> str:
    with shelve.open(HeimdallrSettings._google_settings_path) as d:
      return d["google_calendar_id"]

  @google_calendar_id.setter
  def google_calendar_id(self, calendar_id: str) -> None:
    with shelve.open(HeimdallrSettings._google_settings_path) as d:
      d["google_calendar_id"] = calendar_id

  @property
  def mqtt_access_token(self) -> str:
    with shelve.open(HeimdallrSettings._mqtt_settings_path) as d:
      return d["mqtt_access_token"]

  @mqtt_access_token.setter
  def mqtt_access_token(self, token: str) -> None:
    with shelve.open(HeimdallrSettings._mqtt_settings_path) as d:
      d["mqtt_access_token"] = token

  @property
  def mqtt_username(self) -> str:
    with shelve.open(HeimdallrSettings._mqtt_settings_path) as d:
      return d["mqtt_username"]

  @mqtt_username.setter
  def mqtt_username(self, username: str) -> None:
    with shelve.open(HeimdallrSettings._mqtt_settings_path) as d:
      d["mqtt_username"] = username

  @property
  def mqtt_password(self) -> str:
    with shelve.open(HeimdallrSettings._mqtt_settings_path) as d:
      return d["mqtt_password"]

  @mqtt_password.setter
  def mqtt_password(self, password: str) -> None:
    with shelve.open(HeimdallrSettings._mqtt_settings_path) as d:
      d["mqtt_password"] = password

  @property
  def mqtt_broker(self) -> str:
    with shelve.open(HeimdallrSettings._mqtt_settings_path) as d:
      return d["mqtt_broker"]

  @mqtt_broker.setter
  def mqtt_broker(self, broker: str) -> None:
    with shelve.open(HeimdallrSettings._mqtt_settings_path) as d:
      d["mqtt_broker"] = broker

  @property
  def mqtt_port(self) -> int:
    with shelve.open(HeimdallrSettings._mqtt_settings_path) as d:
      return d["mqtt_port"]

  @mqtt_port.setter
  def mqtt_port(self, port: int) -> None:
    with shelve.open(HeimdallrSettings._mqtt_settings_path) as d:
      d["mqtt_port"] = port


def set_all_heimdallr_settings(*, _lower_keys: bool = True, **kwargs):
  HEIMDALLR_SETTINGS = HeimdallrSettings()
  print(f"current heimdallr settings: {HEIMDALLR_SETTINGS}")
  if _lower_keys:
    kwargs = {k.lower():v for k, v in kwargs.items()}

  # for k in kwargs.keys():
  #    assert k in HEIMDALLR_SETTINGS, f'"{k}" is not in Heimdallrs settings'

  for k in HEIMDALLR_SETTINGS:
    assert k in kwargs.keys(), f'Missing "{k}" from kwargs'

  HEIMDALLR_SETTINGS.__from_dict__(kwargs)

  print(f"new heimdallr settings: {HEIMDALLR_SETTINGS}")


if __name__ == "__main__":
  settings = HeimdallrSettings()

  for k in settings:
    print(k)
  # print(settings)
  # settings.mqtt_password = 2

  # set_all_heimdallr_settings(**settings)
