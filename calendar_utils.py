import os
import json
from datetime import datetime, timezone
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google.oauth2.service_account import Credentials as ServiceAccountCredentials
from googleapiclient.discovery import build

SCOPES = ['https://www.googleapis.com/auth/calendar']

def get_calendar_service():
    creds = None
    token_path = 'token.json'

    # Load Google credentials from environment variable (as JSON string)
    google_creds_json = os.getenv("GOOGLE_CLIENT_SECRET_JSON")

    if google_creds_json:
        # Load credentials from environment variable as service account
        google_creds_dict = json.loads(google_creds_json)
        creds = ServiceAccountCredentials.from_service_account_info(google_creds_dict, scopes=SCOPES)
    elif os.path.exists(token_path):
        creds = Credentials.from_authorized_user_file(token_path, SCOPES)
    else:
        raise Exception("No valid Google credentials found. Set GOOGLE_CLIENT_SECRET_JSON in environment variables.")

    return build('calendar', 'v3', credentials=creds)

def get_available_slots():
    service = get_calendar_service()
    now = datetime.now(timezone.utc).isoformat()

    events_result = service.events().list(
        calendarId='primary',
        timeMin=now,
        maxResults=10,
        singleEvents=True,
        orderBy='startTime'
    ).execute()

    events = events_result.get('items', [])
    return events

def create_event(start_time, end_time, summary="Meeting"):
    service = get_calendar_service()
    event = {
        'summary': summary,
        'start': {'dateTime': start_time, 'timeZone': 'Asia/Kolkata'},
        'end': {'dateTime': end_time, 'timeZone': 'Asia/Kolkata'}
    }
    event = service.events().insert(calendarId='primary', body=event).execute()
    return event.get('htmlLink')
