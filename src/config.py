import os
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
MURF_API_KEY = os.getenv("MURF_API_KEY", "")
MURF_VOICE_ID = os.getenv("MURF_VOICE_ID", "en-US-Jordan")
DEFAULT_LANGUAGE = os.getenv("DEFAULT_LANGUAGE", "en-IN")