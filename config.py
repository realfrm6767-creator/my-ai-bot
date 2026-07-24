"""
config.py
---------
تمام تنظیمات ثابت پروژه اینجا قرار می‌گیرند.
این فایل هیچ منطق اجرایی ندارد، فقط مقداردهی و خواندن از Environment Variables.
"""

import os

# توکن ربات تلگرام (از Environment Variable خوانده می‌شود - هرگز هاردکد نشود)
TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "")

# Owner ID ثابت پروژه. اولویت با Environment Variable است.
OWNER_ID = int(os.environ.get("OWNER_ID", "6554724892"))

# تنظیمات هوش مصنوعی Groq
GROQ_API_KEY = os.environ.get("GROQ_API_KEY", "")
DEFAULT_PROVIDER = "groq"
DEFAULT_MODEL = "openai/gpt-oss-120b"
DEFAULT_TEMPERATURE = 0.7
DEFAULT_LANGUAGE = "fa"
DEFAULT_MEMORY_STATE = True

# مسیر فایل تنظیمات پویا
SETTINGS_FILE = os.path.join(os.path.dirname(__file__), "settings.json")

# تنظیمات اجرای وب‌سرور (Flask + Waitress) روی Render
PORT = int(os.environ.get("PORT", "10000"))
HOST = "0.0.0.0"