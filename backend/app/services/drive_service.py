import os
import json
from dotenv import load_dotenv
from google.oauth2 import service_account
from googleapiclient.discovery import build
from backend.app.services.query_builder import build_drive_query

load_dotenv()

SCOPES = ["https://www.googleapis.com/auth/drive.readonly"]


def get_drive_service():
    credentials_json = os.getenv("GOOGLE_SERVICE_ACCOUNT_JSON")
    credentials_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")

    if credentials_json:
      credentials_info = json.loads(credentials_json)
      credentials = service_account.Credentials.from_service_account_info(
          credentials_info,
          scopes=SCOPES,
      )
    elif credentials_path:
      credentials = service_account.Credentials.from_service_account_file(
          credentials_path,
          scopes=SCOPES,
      )
    else:
      raise ValueError("Google credentials are missing")

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

def search_files_from_message(user_message: str):
  folder_id = os.getenv("GOOGLE_DRIVE_FOLDER_ID")

  if not folder_id:
    raise ValueError("GOOGLE_DRIVE_FOLDER_ID is missing in .env")

  service = get_drive_service()
  query = build_drive_query(user_message, folder_id)

  results = (
    service.files()
    .list(
      q=query,
      fields="files(id, name, mimeType, webViewLink)",
      pageSize=10,
    )
    .execute()
  )

  return {
    "drive_query": query,
    "files": results.get("files", []),
  }

