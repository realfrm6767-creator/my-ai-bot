import os

# ==========================
# Telegram
# ==========================

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN", "")

# ==========================
# Server
# ==========================

HOST = "0.0.0.0"
PORT = int(os.getenv("PORT", "10000"))

# ==========================
# AI
# ==========================

AI_PROVIDER = os.getenv("AI_PROVIDER", "groq")
AI_MODEL = os.getenv("AI_MODEL", "openai/gpt-oss-120b")
AI_TEMPERATURE = 0.8
AI_MAX_TOKENS = 700

# ==========================
# Memory
# ==========================

MAX_HISTORY = 20

# ==========================
# Files
# ==========================

SETTINGS_FILE = "settings.json"

# ==========================
# Project
# ==========================

BOT_NAME = "Gabimaru AI X"
BOT_VERSION = "1.0.0"