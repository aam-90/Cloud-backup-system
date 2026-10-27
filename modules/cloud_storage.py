
import os

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build


SCOPES = ["https://www.googleapis.com/auth/drive.file"]

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CREDENTIALS_FILE = os.path.join(BASE_DIR, "credentials.json")
TOKEN_FILE = os.path.join(BASE_DIR, "token.json")
FOLDER_ID_FILE = os.path.join(BASE_DIR, "drive_folder_id.txt")


def get_drive_service():
    creds = None

    if os.path.exists(TOKEN_FILE):
        creds = Credentials.from_authorized_user_file(
            TOKEN_FILE, SCOPES
        )

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                CREDENTIALS_FILE, SCOPES
            )
            creds = flow.run_local_server(port=0)

        with open(TOKEN_FILE, "w", encoding="utf-8") as token:
            token.write(creds.to_json())

    return build("drive", "v3", credentials=creds)


def get_backup_folder(service):
    if os.path.exists(FOLDER_ID_FILE):
        with open(FOLDER_ID_FILE, "r", encoding="utf-8") as file:
            folder_id = file.read().strip()

        try:
            folder = service.files().get(
                fileId=folder_id, fields="id, name"
            ).execute()
            return folder["id"]
        except Exception:
            pass

    metadata = {
        "name": "CloudBackupSystem",
        "mimeType": "application/vnd.google-apps.folder"
    }

    folder = service.files().create(
        body=metadata, fields="id"
    ).execute()

    folder_id = folder["id"]

    with open(FOLDER_ID_FILE, "w", encoding="utf-8") as file:
        file.write(folder_id)

    return folder_id



def upload_file(local_path, relative_path):
    import os
    from googleapiclient.http import MediaFileUpload

    if not os.path.isfile(local_path):
        raise FileNotFoundError(
            f"Backup file not found: {local_path}"
        )

    service = get_drive_service()
    folder_id = get_backup_folder(service)

    cloud_name = relative_path.replace("\\", "__").replace("/", "__")

    query = (
        f"name = '{cloud_name}' and "
        f"'{folder_id}' in parents and trashed = false"
    )

    results = service.files().list(
        q=query,
        pageSize=100,
        fields="files(id, name)"
    ).execute()

    existing = results.get("files", [])

    media = MediaFileUpload(local_path, resumable=True)

    if existing:
        service.files().update(
            fileId=existing[0]["id"],
            media_body=media
        ).execute()

        print(f"Cloud backup updated: {cloud_name}")
    else:
        metadata = {
            "name": cloud_name,
            "parents": [folder_id]
        }

        service.files().create(
            body=metadata,
            media_body=media,
            fields="id, name"
        ).execute()

        print(f"Cloud backup uploaded: {cloud_name}")
