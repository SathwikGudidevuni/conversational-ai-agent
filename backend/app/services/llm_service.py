import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()

llm = ChatGoogleGenerativeAI(
  model="gemini-2.5-flash",
  google_api_key=os.getenv("GOOGLE_API_KEY"),
  temperature=0,
  timeout=10,
  max_retries=1,
)

def test_llm_connection():
  response = llm.invoke(
    "Reply only with this text: Gemini connection works"
  )
  return response.content
