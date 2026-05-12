import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from backend.app.tools.drive_search_tool import drive_search_tool

load_dotenv()


def get_llm():
  return ChatGoogleGenerativeAI(
    model=os.getenv("GEMINI_MODEL", "gemini-2.5-flash"),
    google_api_key=os.getenv("GOOGLE_API_KEY"),
    temperature=0,
    timeout=10,
    max_retries=1,
  )

def test_llm_connection():
  llm = get_llm()
  response = llm.invoke(
    "Reply only with this text: Gemini connection works"
  )
  return response.content


def ask_agent(user_message: str):
  llm = get_llm()
  llm_with_tools = llm.bind_tools([drive_search_tool])

  response = llm_with_tools.invoke(user_message)

  if not response.tool_calls:
    return {
      "answer": response.content,
      "tool_used": False,
      "files": [],
    }

  tool_call = response.tool_calls[0]
  tool_result = drive_search_tool.invoke(tool_call["args"])

  files = tool_result["files"]

  if not files:
    answer = "I could not find any matching files in Google Drive."
  else:
    file_names = [file["name"] for file in files]
    answer = "I found these files: " + ", ".join(file_names)

  return {
    "answer": answer,
    "tool_used": True,
    "drive_query": tool_result["drive_query"],
    "files": files,
  }
