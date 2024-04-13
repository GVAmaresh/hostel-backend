import pickle
import os
import datetime
from google_auth_oauthlib.flow import Flow, InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload
from google.auth.transport.requests import Request


def Create_Service(client_secret_file, api_name, api_version, *scopes):
    CLIENT_SECRET_FILE = client_secret_file
    API_SERVICE_NAME = api_name
    API_VERSION = api_version
    SCOPES = [scope for scope in scopes[0]]

    cred = None
    pickle_file = f'token_{API_SERVICE_NAME}_{API_VERSION}.pickle'

    if os.path.exists(pickle_file):
        with open(pickle_file, 'rb') as token:
            cred = pickle.load(token)

    if not cred or not cred.valid:
        if cred and cred.expired and cred.refresh_token:
            cred.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRET_FILE, SCOPES)
            cred = flow.run_local_server()

        with open(pickle_file, 'wb') as token:
            pickle.dump(cred, token)

    try:
        service = build(API_SERVICE_NAME, API_VERSION, credentials=cred)
        return service
    except Exception as e:
        print('Unable to connect.')
        print(e)
        return None

def convert_to_RFC_datetime(year=1900, month=1, day=1, hour=0, minute=0):
    dt = datetime.datetime(year, month, day, hour, minute, 0).isoformat() + 'Z'
    return dt

import os
def removeAccount():
    directory = os.getcwd()
    files = os.listdir(directory)

    for file in files:
        if "token" in file:
            try:
                os.remove(os.path.join(directory, file))
                print(f"File '{file}' deleted successfully.")
            except Exception as e:
                print(f"Error deleting file '{file}': {e}")


def checkFake(service, path="root", Folder_Name="Details"):
    resource = service.files()
    result = resource.list(
        q=f"mimeType = 'application/vnd.google-apps.folder' and '{path}' in parents",
        fields="nextPageToken, files(id, name)",
    ).execute()
    list_folders = result.get("files")
    fake_folder_id = None

    for folder in list_folders:
        if folder["name"] == Folder_Name:
            fake_folder_id = folder["id"]
            break

    return fake_folder_id

def CheckFolders(service):
    return checkFake(service)

import gdown
def list_file(file_id):
    try:
        files = gdown.download_folder(
            url=f'https://drive.google.com/drive/folders/{file_id}?usp=sharing',
            skip_download=True,
        )
        if files is None:
            print("Failed to retrieve folder contents.")
            return []
        file_info = []
        for file in files:
            if file.local_path.split('\\')[-1] == "sample.json":
                file_name = file.local_path.split('\\')[-1]
                file_id = file.id
                return file_id
        return "Not Found"
    except Exception as e:
        print(f"An error occurred: {e}")
        return []

CLIENT_FILE_NAME = "./client_secret.json"
API_DRIVE = "drive"
API_VERSION = "v3"
SCOPES = ["https://www.googleapis.com/auth/drive"]

services = Create_Service(CLIENT_FILE_NAME, API_DRIVE, API_VERSION, SCOPES)

def GET_THE_URL():
    services = Create_Service(CLIENT_FILE_NAME, API_DRIVE, API_VERSION, SCOPES)
    folder_id = CheckFolders(services)
    file_id = list_file(folder_id)
    return "https://drive.google.com/uc?id=" + file_id