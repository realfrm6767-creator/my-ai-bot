"""
config.py
---------
تمام تنظیمات ثابت پروژه اینجا قرار می‌گیرند.
"""

import os

TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "")

OWNER_ID = int(os.environ.get("OWNER_ID", "6554724892"))

GROQ_API_KEY = os.environ.get("GROQ_API_KEY", "")
GROQ_MODEL = "openai/gpt-oss-120b"

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")
GEMINI_MODEL = "gemini-2.0-flash"

DEFAULT_PROVIDER = "groq"
DEFAULT_MODEL = GROQ_MODEL
DEFAULT_TEMPERATURE = 0.7
DEFAULT_LANGUAGE = "fa"
DEFAULT_MEMORY_STATE = True

SETTINGS_FILE = os.path.join(os.path.dirname(__file__), "settings.json")

PORT = int(os.environ.get("PORT", "10000"))
HOST = "0.0.0.0"