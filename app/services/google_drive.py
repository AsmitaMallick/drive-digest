from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials

import io

from googleapiclient.http import MediaIoBaseDownload


def get_drive_service(token):

    creds = Credentials(token=token)

    return build("drive", "v3", credentials=creds)


def list_files(service, folder_id):

    results = service.files().list(
        q=f"'{folder_id}' in parents",
        fields="files(id, name, mimeType)"
    ).execute()

    return results.get("files", [])


def download_file(service, file_id, filename):

    request = service.files().get_media(fileId=file_id)

    file_stream = io.BytesIO()

    downloader = MediaIoBaseDownload(
        file_stream,
        request
    )

    done = False

    while not done:
        _, done = downloader.next_chunk()

    with open(filename, "wb") as f:
        f.write(file_stream.getvalue())