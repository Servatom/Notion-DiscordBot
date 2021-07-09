from __future__ import print_function
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.http import MediaFileUpload
import sys
import magic

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/drive','https://www.googleapis.com/auth/drive.file']

folder_id = ""

def downloadFile(url):
    os.system(f"wget {url} -P ./data/")
    g_link = uploadFiles(url.split("/")[-1], url)
    return g_link

def uploadFiles(fileName, url):
    """Shows basic usage of the Drive v3 API.
    Prints the names and ids of the first 10 files the user has access to.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('/GDrive_Cred/token.json'):
        creds = Credentials.from_authorized_user_file('/GDrive_Cred/token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    else:
        print("Please run upload upload.py before using it!!!")
        sys.exit(1)

    service = build('drive', 'v3', credentials=creds)

    # Call the Drive v3 API
    file_metadata = {
        "name": fileName,
        "parents": [folder_id]
    }
    path = "./data/{}".format(fileName)
    media = MediaFileUpload(path, mimetype=giveMimeType(fileName))
    file = service.files().create(body=file_metadata, media_body=media, fields='id').execute()

    with open("dataUploaded.txt", "a+") as log:
        # Move read cursor to the start of file.
        log.seek(0)
        # If file is not empty then append '\n'
        data = log.read(100)
        if len(data) > 0 :
            log.write("\n")
        # Append text at the end of file
        log.write(url)

    link = f"https://drive.google.com/file/d/{file.get('id')}"
    os.system("rm ./data/*")
    return link

def giveMimeType(file):
    mime = magic.Magic(mime=True)
    return mime.from_file(f"./data/{file}")

def main():
    creds = None
    if os.path.exists('/GDrive_Cred/token.json'):
        creds = Credentials.from_authorized_user_file('/GDrive_Cred/token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                '/GDrive_Cred/credentials.json', SCOPES)
            creds = flow.run_local_server(port=5000)
        # Save the credentials for the next run
        with open('/GDrive_Cred/token.json', 'w') as token:
            token.write(creds.to_json())
        print("Logging in")
        return
    print("All good")
    return

if __name__ == '__main__':
    main()

try:
    print(os.environ['GDRIVE_FOLDER'])
    folder_id = str(os.environ['GDRIVE_FOLDER'])

except:
    print("Invalid folder id")