from fastapi import FastAPI

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
