import re
from datetime import datetime, timedelta, timezone


def escape_drive_value(value: str):
  return value.replace("\\", "\\\\").replace("'", "\\'")


def get_mime_type(user_message: str):
  message = user_message.lower()

  if "pdf" in message:
    return "application/pdf"

  if "sheet" in message or "spreadsheet" in message or "excel" in message:
    return "application/vnd.google-apps.spreadsheet"

  if "doc" in message or "document" in message:
    return "application/vnd.google-apps.document"

  if "image" in message or "photo" in message or "picture" in message:
    return "image/"

  return None


def get_search_mode(user_message: str):
  message = user_message.lower()

  if "exact name" in message or "named exactly" in message:
    return "exact_name"

  if (
    "fulltext" in message
    or "full text" in message
    or "content" in message
    or "containing" in message
    or "inside" in message
    or "mentions" in message
    or "text contains" in message
  ):
    return "full_text"

  return "partial_name"


def get_date_filter(user_message: str):
  message = user_message.lower()
  now = datetime.now(timezone.utc)

  if "today" in message:
    start = now.replace(hour=0, minute=0, second=0, microsecond=0)
    return f"modifiedTime >= '{start.isoformat().replace('+00:00', 'Z')}'"

  if "yesterday" in message:
    start = (now - timedelta(days=1)).replace(hour=0, minute=0, second=0, microsecond=0)
    end = now.replace(hour=0, minute=0, second=0, microsecond=0)
    return (
      f"modifiedTime >= '{start.isoformat().replace('+00:00', 'Z')}' "
      f"and modifiedTime < '{end.isoformat().replace('+00:00', 'Z')}'"
    )

  if "last week" in message or "last 7 days" in message:
    start = (now - timedelta(days=7)).replace(microsecond=0)
    return f"modifiedTime >= '{start.isoformat().replace('+00:00', 'Z')}'"

  after_match = re.search(r"after (\d{4}-\d{2}-\d{2})", message)
  if after_match:
    return f"modifiedTime > '{after_match.group(1)}T00:00:00Z'"

  before_match = re.search(r"before (\d{4}-\d{2}-\d{2})", message)
  if before_match:
    return f"modifiedTime < '{before_match.group(1)}T00:00:00Z'"

  return None


def clean_search_text(user_message: str):
  message = user_message.lower()

  quoted_match = re.search(r'"([^"]+)"|' + r"'([^']+)'", user_message)
  if quoted_match:
    return quoted_match.group(1) or quoted_match.group(2)

  exact_match = re.search(
    r"(?:exact name|named exactly|named|called) (.+)",
    user_message,
    re.IGNORECASE,
  )
  if exact_match:
    return exact_match.group(1).strip(" .,?!'\"")

  words_to_remove = [
    "find",
    "search",
    "show",
    "get",
    "me",
    "files",
    "file",
    "pdf",
    "pdfs",
    "doc",
    "docs",
    "document",
    "documents",
    "sheet",
    "sheets",
    "spreadsheet",
    "spreadsheets",
    "excel",
    "image",
    "images",
    "photo",
    "photos",
    "picture",
    "pictures",
    "with",
    "from",
    "named",
    "called",
    "containing",
    "about",
    "exact",
    "name",
    "fulltext",
    "full",
    "text",
    "content",
    "inside",
    "mentions",
    "modified",
    "created",
    "today",
    "yesterday",
    "last",
    "week",
    "days",
    "after",
    "before",
  ]

  words = user_message.lower().split()
  useful_words = []

  for word in words:
      cleaned_word = word.strip(".,?!'\"")

      if re.match(r"\d{4}-\d{2}-\d{2}", cleaned_word):
        continue

      if cleaned_word not in words_to_remove:
        useful_words.append(cleaned_word)

  return " ".join(useful_words).strip()


def build_drive_query(user_message: str, folder_id: str):
  query_parts = [
    f"'{folder_id}' in parents",
    "trashed = false",
  ]

  mime_type = get_mime_type(user_message)
  search_mode = get_search_mode(user_message)
  date_filter = get_date_filter(user_message)
  search_text = clean_search_text(user_message)

  if mime_type:
    if mime_type == "image/":
      query_parts.append("mimeType contains 'image/'")
    else:
      query_parts.append(f"mimeType = '{mime_type}'")

  if date_filter:
    query_parts.append(date_filter)

  if search_text:
    safe_search_text = escape_drive_value(search_text)

    if search_mode == "exact_name":
      query_parts.append(f"name = '{safe_search_text}'")
    elif search_mode == "full_text":
      query_parts.append(f"fullText contains '{safe_search_text}'")
    else:
      query_parts.append(f"name contains '{safe_search_text}'")

  return " and ".join(query_parts)
