import os
import requests
import streamlit as st

BACKEND_URL = os.getenv("BACKEND_URL", "http://127.0.0.1:8000")
API_URL = f"{BACKEND_URL}/chat"


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
    st.write(message["content"])

user_message = st.chat_input("Ask me to find files in Google Drive")

if user_message:
  st.session_state.messages.append({
    "role": "user",
    "content": user_message,
  })

  with st.chat_message("user"):
    st.write(user_message)

  try:
    response = requests.post(
      API_URL,
      json={"message": user_message},
      timeout=30,
    )
    response.raise_for_status()
    data = response.json()

    answer = data.get("answer", "No answer returned.")

    files = data.get("files", [])
    if files:
      answer += "\n\nMatching files:\n"
      for file in files:
        file_name = file.get("name", "Untitled")
        file_link = file.get("webViewLink", "")
        answer += f"\n- [{file_name}]({file_link})"

  except requests.exceptions.RequestException as error:
    answer = f"Backend error: {error}"

  st.session_state.messages.append({
    "role": "assistant",
    "content": answer,
  })

  with st.chat_message("assistant"):
    st.write(answer)
