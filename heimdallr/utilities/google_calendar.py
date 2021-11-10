from __future__ import print_function

import datetime
import pickle
from pathlib import Path

import pandas
from dash import dash_table
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

from apppath import ensure_existence
from heimdallr.configuration.heimdallr_settings import HeimdallrSettings
from heimdallr.utilities.date_tools import iso_dt_to_datetime

__all__ = ["get_calender_df"]

SCOPES = ["https://www.googleapis.com/auth/calendar.readonly"]


# If modifying these scopes, delete the file token.pickle.
"""
def implicit():
    from google.cloud import storage

    # If you don't specify credentials when constructing the client, the
    # client library will look for credentials in the environment.
    storage_client = storage.Client()

    # Make an authenticated API request
    buckets = list(storage_client.list_buckets())
    print(buckets)
"""


def get_calender_df(
    calendar_id: str, credentials_base_path: Path, num_entries: int = 30
) -> dash_table.DataTable:
    """Shows basic usage of the Google Calendar API.
    Prints the start and name of the next 10 events on the user's calendar.

    :param num_entries:
    :param credentials_base_path:
    :type calendar_id: object
    :rtype: object
    """
    credentials = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.

    tokens_path = ensure_existence(credentials_base_path / "google") / "token.pickle"
    if tokens_path.exists():
        with open(tokens_path, "rb") as token:
            credentials = pickle.load(token)

    if not credentials or not credentials.valid:
        # If there are no (valid) credentials available, let the user log in.
        if credentials and credentials.expired and credentials.refresh_token:
            credentials.refresh(Request())
        else:
            a = ensure_existence(credentials_base_path / "google") / "credentials.json"
            if a.exists():
                flow = InstalledAppFlow.from_client_secrets_file(str(a), SCOPES)
                credentials = flow.run_local_server()
            else:
                if False:
                    raise Exception(f"Missing {a}")
                else:
                    print(f"Missing {a}")

        with open(tokens_path, "wb") as token:
            # Save the credentials for the next run
            pickle.dump(credentials, token)

    df = pandas.DataFrame(columns=("start", "summary"))
    if credentials:
        service = build("calendar", "v3", credentials=credentials)

        # Call the Calendar API

        events_result = (
            service.events()
            .list(
                calendarId=calendar_id,
                timeMin=f"{datetime.datetime.utcnow().isoformat()}Z",  # 'Z' indicates UTC time
                maxResults=num_entries,
                singleEvents=True,
                orderBy="startTime",
            )
            .execute()
        )
        events = events_result.get("items", [])

        if not events:
            print("No upcoming events found.")
        else:
            for event in events:
                start = event["start"].get("dateTime", event["start"].get("date"))
                if "summary" in event:
                    df.loc[-1] = (start, event["summary"])  # 'summary'
                    df.index = df.index + 1
                    df = df.sort_index(ascending=False)

        df.start = df.start.map(iso_dt_to_datetime)

    return df


if __name__ == "__main__":
    CALENDAR_ID = HeimdallrSettings().google_calendar_id  # Christian Alexandra

    print(get_calender_df(CALENDAR_ID, HeimdallrSettings()._credentials_base_path))
