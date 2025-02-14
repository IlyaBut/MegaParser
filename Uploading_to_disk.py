from dataclasses import fields

from google.oauth2 import service_account
from googleapiclient.http import MediaIoBaseDownload,MediaFileUpload
from googleapiclient.discovery import build
import csv

SCOPES = ['https://www.googleapis.com/auth/drive']
SERVICE_ACCOUNT_FILE = "forparsed-5e95b7eff266.json"
credentials = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)
service = build('drive', 'v3', credentials=credentials)

folder_id = "1C3TNEc8r_GL87UJXJPSUscfQ-XvEvpSV"
name = "parsed.csv"
file_path = "result_parsed.csv"
file_metadata = {
        "name": name,
        "mimeType": 'application/vnd.google-apps.spreadsheet',
        "parents": [folder_id]
}

media = MediaFileUpload(file_path,mimetype= "text/csv", resumable=True)
r = service.files().create(body = file_metadata, media_body = media, fields ="id").execute()
print(r)