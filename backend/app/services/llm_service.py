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


def format_chat_history(chat_history):
  if not chat_history:
    return "No previous conversation."

  recent_messages = chat_history[-6:]
  lines = []

  for message in recent_messages:
    role = message.get("role", "user")
    content = message.get("content", "")
    lines.append(f"{role}: {content}")

  return "\n".join(lines)


def ask_agent(user_message: str, chat_history=None):
  llm = get_llm()
  llm_with_tools = llm.bind_tools([drive_search_tool])

  prompt = (
    "You are a Google Drive file discovery assistant. "
    "When the user wants to find files, call the drive_search_tool. "
    "The tool can search by exact name, partial name, file type, fullText/content, "
    "and modified date. If the user asks a follow-up question, rewrite it as a "
    "complete search request before calling the tool.\n\n"
    f"Recent conversation:\n{format_chat_history(chat_history)}\n\n"
    f"User request: {user_message}"
  )

  response = llm_with_tools.invoke(prompt)

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
