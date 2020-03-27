from __future__ import print_function

import datetime
import pickle

import dash_table
import pandas
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

from heimdallr import PROJECT_APP_PATH
from heimdallr.utilities.date_tools import isoformat2datetime
from heimdallr.utilities.heimdallr_settings import HeimdallrSettings

__all__ = ["get_calender_df"]

SCOPES = ["https://www.googleapis.com/auth/calendar.readonly"]


# If modifying these scopes, delete the file token.pickle.


def get_calender_df(
  calendar_id: str, credentials_base_path, num_entries=30
  ) -> dash_table.DataTable:
  """Shows basic usage of the Google Calendar API.
Prints the start and name of the next 10 events on the user's calendar.
"""
  credentials = None
  # The file token.pickle stores the user's access and refresh tokens, and is
  # created automatically when the authorization flow completes for the first
  # time.

  tokens_path = credentials_base_path / "token.pickle"
  if tokens_path.exists():
    with open(tokens_path, "rb") as token:
      credentials = pickle.load(token)

  if not credentials or not credentials.valid:
    # If there are no (valid) credentials available, let the user log in.
    if credentials and credentials.expired and credentials.refresh_token:
      credentials.refresh(Request())
    else:
      a = credentials_base_path / "credentials.json"
      if a.exists():
        flow = InstalledAppFlow.from_client_secrets_file(a, SCOPES)
        credentials = flow.run_local_server()
      else:
        raise Exception(f"Missing {a}")

    with open(tokens_path, "wb") as token:
      # Save the credentials for the next run
      pickle.dump(credentials, token)

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

  df = pandas.DataFrame(columns=("start", "summary"))

  if not events:
    print("No upcoming events found.")
  else:
    for event in events:
      start = event["start"].get("dateTime", event["start"].get("date"))
      if "summary" in event:
        df.loc[-1] = (start, event["summary"])  # 'summary'
        df.index = df.index + 1
        df = df.sort_index(ascending=False)

  df.start = df.start.map(isoformat2datetime)

  return df


if __name__ == "__main__":
  CALENDAR_ID = HeimdallrSettings().calendar_id  # Christian Alexandra

  print(get_calender_df(CALENDAR_ID, PROJECT_APP_PATH.user_config))
