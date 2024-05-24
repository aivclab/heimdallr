#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "Christian"
__doc__ = r"""

           Created on 29/03/2020
           """

import json
import logging
import random
from typing import List

import requests

__all__ = ["meet_members_status"]

from dash import html
from dash.html import Div, H3, H4, H2


def meet_members_status(access_token: str) -> List[html.Div]:
    """
    Get the status of all teams in the tenant
    """
    members = []
    for i in range(4):
        members.append(
            Div(
                [
                    H2(
                        f"member{i}",
                        className="text-monospace",
                        style={"text-decoration": "underline"},
                    ),
                    H3(
                        f"status: {'online' if random.randint(0, 1) > 0 else 'offline'}",
                        className="text-monospace",
                        style={"text-decoration": "underline"},
                    ),
                    H4(
                        f"{random.randint(0, 10)} sec ago",
                        className="text-monospace",
                        style={"text-decoration": "underline"},
                    ),
                ],
                style={
                    "text-align": "center",
                    "width": "100%",
                },
                className="col p-1",
            )
        )
    return members


if __name__ == "__main__":
    from exclude.calendar_app.tutorial.set_teams_config import s
    import msal

    app = msal.ConfidentialClientApplication(
        s.teams_client_id,
        authority=s.teams_authority,
        client_credential=s.teams_secret,
        # token_cache=...  # Default cache is in memory only.
        # You can learn how to use SerializableTokenCache from
        # https://msal-python.rtfd.io/en/latest/#msal.SerializableTokenCache
    )  # Create a preferably long-lived app instance which maintains a token cache.

    result = app.acquire_token_silent(
        s.teams_scope, account=None
    )  # Firstly, looks up a token from cache since we are looking for token for the current app, NOT for an end user, notice we give account parameter as None.

    if not result:
        logging.info("No suitable token exists in cache. Let's get a new one from AAD.")
        result = app.acquire_token_for_client(scopes=s.teams_scope)

    if "access_token" in result:
        # Calling graph using the access token
        graph_data = requests.get(  # Use token to call downstream service
            s.teams_endpoint,
            headers={"Authorization": "Bearer " + result["access_token"]},
        ).json()
        print("Graph API call result: ")
        print(json.dumps(graph_data, indent=2))
    else:
        print(result.get("error"))
        print(result.get("error_description"))
        print(result.get("correlation_id"))  # You may need this when reporting a bug
