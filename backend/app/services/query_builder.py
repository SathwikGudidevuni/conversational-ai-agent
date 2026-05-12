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


def clean_search_text(user_message: str):
  words_to_remove = [
    "find",
    "search",
    "show",
    "get",
    "me",
    "files",
    "file",
    "pdf",
    "doc",
    "document",
    "sheet",
    "spreadsheet",
    "excel",
    "image",
    "photo",
    "picture",
    "with",
    "named",
    "called",
    "containing",
    "about",
  ]

  words = user_message.lower().split()
  useful_words = []

  for word in words:
      cleaned_word = word.strip(".,?!'\"")

      if cleaned_word not in words_to_remove:
        useful_words.append(cleaned_word)

  return " ".join(useful_words).strip()


def build_drive_query(user_message: str, folder_id: str):
  query_parts = [
    f"'{folder_id}' in parents",
    "trashed = false",
  ]

  mime_type = get_mime_type(user_message)
  search_text = clean_search_text(user_message)

  if mime_type:
    if mime_type == "image/":
      query_parts.append("mimeType contains 'image/'")
    else:
      query_parts.append(f"mimeType = '{mime_type}'")

  if search_text:
    query_parts.append(f"name contains '{search_text}'")

  return " and ".join(query_parts)
