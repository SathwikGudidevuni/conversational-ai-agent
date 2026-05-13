from langchain_core.tools import tool
from backend.app.services.drive_service import search_files_from_message

@tool
def drive_search_tool(user_message: str) -> dict:
  """
  Search Google Drive files using a natural language user request.

  Use this tool when the user asks to find, search, show, or list files
  from Google Drive. It supports exact file name search, partial file name
  search, MIME type filtering, fullText/content search, and modified date
  filters by building a Google Drive files.list q parameter.
  """
  return search_files_from_message(user_message)
