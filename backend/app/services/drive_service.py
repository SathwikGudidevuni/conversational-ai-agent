import os

from dotenv import load_dotenv
from google.oauth2 import service_account
from googleapiclient.discovery import build

load_dotenv()

SCOPES = ["https://www.googleapis.com/auth/drive.readonly"]


def get_drive_service():
  credentials_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")

  if not credentials_path:
      raise ValueError("GOOGLE_APPLICATION_CREDENTIALS is missing in .env")

  credentials = service_account.Credentials.from_service_account_file(
      credentials_path,
      scopes=SCOPES,
  )

  service = build("drive", "v3", credentials=credentials)
  return service


def test_drive_connection():
  folder_id = os.getenv("GOOGLE_DRIVE_FOLDER_ID")

  if not folder_id:
      raise ValueError("GOOGLE_DRIVE_FOLDER_ID is missing in .env")

  service = get_drive_service()

  query = f"'{folder_id}' in parents and trashed = false"

  results = (
      service.files()
      .list(
          q=query,
          fields="files(id, name, mimeType, webViewLink)",
          pageSize=10,
      )
      .execute()
  )

  return results.get("files", [])

def search_files_by_name(name_text: str):
  folder_id = os.getenv("GOOGLE_DRIVE_FOLDER_ID")

  if not folder_id:
      raise ValueError("GOOGLE_DRIVE_FOLDER_ID is missing in .env")

  service = get_drive_service()

  query = (
      f"'{folder_id}' in parents "
      f"and trashed = false "
      f"and name contains '{name_text}'"
  )

  results = (
    service.files()
    .list(
        q=query,
        fields="files(id, name, mimeType, webViewLink)",
        pageSize=10,
    )
    .execute()
  )

  return results.get("files", [])
