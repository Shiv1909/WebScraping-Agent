# All environment and static configs # agent/config.py

import os
from dotenv import load_dotenv

load_dotenv()

GOOGLE_CSE_API_KEY = os.getenv("GOOGLE_CSE_API_KEY")
GOOGLE_CSE_CX = os.getenv("GOOGLE_CSE_CX")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
