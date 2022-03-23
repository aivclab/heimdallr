import json
import logging

import msal
import requests

# __all__ = [""]

from heimdallr.utilities.server.exclude.set_teams_config import s

if __name__ == "__main__":

    app = msal.ConfidentialClientApplication(
        s.teams_client_id,
        authority=s.teams_authority,
        client_credential=s.teams_secret,
        # token_cache=...  # Default cache is in memory only.
        # You can learn how to use SerializableTokenCache from
        # https://msal-python.rtfd.io/en/latest/#msal.SerializableTokenCache
    )  # Create a preferably long-lived app instance which maintains a token cache.

    result = app.acquire_token_silent(s.teams_scope, account=None)
    # Firstly, looks up a token from cache
    # Since we are looking for token for the current app, NOT for an end user,
    # notice we give account parameter as None.

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
