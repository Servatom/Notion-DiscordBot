from __future__ import print_function
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
import sys
import json
SCOPES = ['https://www.googleapis.com/auth/drive','https://www.googleapis.com/auth/drive.file']



def delete_file(file_id):
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('./creds/token.json'):
        creds = Credentials.from_authorized_user_file('./creds/token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    # if this file isnt there this may be a heroku instance
    elif os.path.exists('/app/google-credentials.json'):
        creds = Credentials.from_authorized_user_file('/app/google-credentials.json', SCOPES)
    else:
        print("Please run upload upload.py before using it!!!")
        sys.exit(1)

    service = build('drive', 'v3', credentials=creds)

    try:
        service.files().delete(fileId = file_id).execute()
        return 0
    except:
        print("ERROR, file didnt get deleted")
        return 1