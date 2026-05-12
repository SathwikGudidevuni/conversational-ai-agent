from fastapi import FastAPI
from pydantic import BaseModel
from backend.app.services.drive_service import search_files_by_name,search_files_from_message, test_drive_connection
from backend.app.services.llm_service import ask_agent, test_llm_connection

app = FastAPI(
  title="Conversational Google Drive AI Agent",
  description="A FastAPI backend for searching Google Drive using natural language.",
  version="0.1.0",
)

class ChatRequest(BaseModel):
  message: str

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

@app.get("/test-llm")
def test_llm():
  response = test_llm_connection()
  return {
    "response": response,
  }

@app.get("/smart-search")
def smart_search(message: str):
  result = search_files_from_message(message)
  return {
    "message": message,
    "drive_query": result["drive_query"],
    "count": len(result["files"]),
    "files": result["files"],
  }

@app.get("/agent-search")
def agent_search(message: str):
  result = ask_agent(message)
  return result

@app.post("/chat")
def chat(request: ChatRequest):
  result = ask_agent(request.message)

  return {
    "message": request.message,
    "answer": result.get("answer"),
    "tool_used": result.get("tool_used"),
    "drive_query": result.get("drive_query"),
    "files": result.get("files", []),
  }

