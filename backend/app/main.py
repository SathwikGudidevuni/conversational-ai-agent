from fastapi import FastAPI
from backend.app.services.drive_service import search_files_by_name, test_drive_connection

app = FastAPI(
  title="Conversational Google Drive AI Agent",
  description="A FastAPI backend for searching Google Drive using natural language.",
  version="0.1.0",
)

@app.get("/")
def root():
  return {
    "message": "Google Drive AI Agent backend is running"
  }

@app.get("/test-drive")
def test_drive():
  files = test_drive_connection()
  return {
    "count": len(files),
    "files": files,
  }

@app.get("/search")
def search(name: str):
  files = search_files_by_name(name)
  return {
      "query": name,
      "count": len(files),
      "files": files,
  }
