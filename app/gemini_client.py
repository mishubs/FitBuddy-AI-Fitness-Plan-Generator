from .config import GEMINI_API_KEY

_client = None

def get_client():
    global _client
    if not GEMINI_API_KEY:
        return None
    if _client is None:
        from google import genai
        _client = genai.Client(api_key=GEMINI_API_KEY)
    return _client
