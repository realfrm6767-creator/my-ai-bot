"""
ai.py
-----
اتصال به سرویس هوش مصنوعی Groq. زبان پاسخ همیشه بر اساس تنظیم
زبان ربات است، نه زبان پیام کاربر.
"""

from groq import Groq

import config
from settings import load_settings
from utils.locales import get_system_prompt, t

_client = Groq(api_key=config.GROQ_API_KEY)


def generate_response(user_message: str, history: list[dict] | None = None) -> str:
    settings = load_settings()
    model = settings.get("model", config.DEFAULT_MODEL)
    temperature = settings.get("temperature", config.DEFAULT_TEMPERATURE)
    lang = settings.get("language", config.DEFAULT_LANGUAGE)

    messages = [{"role": "system", "content": get_system_prompt(lang)}]
    if history:
        messages.extend(history)
    messages.append({"role": "user", "content": user_message or "hi"})

    try:
        completion = _client.chat.completions.create(model=model, temperature=temperature, messages=messages)
        return completion.choices[0].message.content.strip()
    except Exception:
        return t("ai_error", lang)