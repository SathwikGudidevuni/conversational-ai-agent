import os
import requests
import streamlit as st

BACKEND_URL = os.getenv("BACKEND_URL", "http://127.0.0.1:8000")
API_URL = f"{BACKEND_URL}/chat"


def get_file_type_label(mime_type: str):
  if mime_type == "application/pdf":
    return "PDF"

  if mime_type == "application/vnd.google-apps.document":
    return "Google Doc"

  if mime_type == "application/vnd.google-apps.spreadsheet":
    return "Google Sheet"

  if mime_type.startswith("image/"):
    return "Image"

  return "File"


def format_files(files):
  if not files:
    return "No matching files found."

  lines = []

  for file in files:
    file_name = file.get("name", "Untitled")
    file_link = file.get("webViewLink", "")
    mime_type = file.get("mimeType", "")
    modified_time = file.get("modifiedTime", "")
    file_type = get_file_type_label(mime_type)

    if file_link:
      line = f"- **{file_type}**: [{file_name}]({file_link})"
    else:
      line = f"- **{file_type}**: {file_name}"

    if modified_time:
      line += f"  \n  Modified: `{modified_time[:10]}`"

    lines.append(line)

  return "\n".join(lines)


st.set_page_config(
  page_title="Google Drive AI Agent",
  page_icon="🔎",
  layout="centered",
)

st.title("Google Drive AI Agent")

if "messages" not in st.session_state:
  st.session_state.messages = []

for message in st.session_state.messages:
  with st.chat_message(message["role"]):
    st.markdown(message["content"])

user_message = st.chat_input("Ask me to find files in Google Drive")

if user_message:
  st.session_state.messages.append({
    "role": "user",
    "content": user_message,
  })

  with st.chat_message("user"):
    st.markdown(user_message)

  try:
    response = requests.post(
      API_URL,
      json={
        "message": user_message,
        "history": st.session_state.messages[:-1],
      },
      timeout=30,
    )
    response.raise_for_status()
    data = response.json()

    answer = data.get("answer", "No answer returned.")
    files = data.get("files", [])

    if files:
      answer += "\n\nMatching files:\n"
      answer += format_files(files)
    else:
      answer = "No matching files found. Try a simpler keyword, file type, content word, or date filter."

    drive_query = data.get("drive_query")
    if drive_query:
      answer += f"\n\nDrive query used:\n`{drive_query}`"

  except requests.exceptions.RequestException as error:
    answer = f"Backend error: {error}"

  st.session_state.messages.append({
    "role": "assistant",
    "content": answer,
  })

  with st.chat_message("assistant"):
    st.markdown(answer)
