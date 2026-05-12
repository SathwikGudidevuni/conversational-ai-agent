from langchain_core.tools import tool
from backend.app.services.drive_service import search_files_from_message

@tool
def drive_search_tool(user_message: str) -> dict:
  """
  Search Google Drive files using a natural language user request.

  Use this tool when the user asks to find, search, show, or list files
  from Google Drive.
  """
  return search_files_from_message(user_message)
