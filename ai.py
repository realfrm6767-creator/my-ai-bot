"""
ai.py
-----
اتصال به سرویس هوش مصنوعی Groq و تولید پاسخ.
لحن پاسخ‌ها محاوره‌ای و عامیانه است، بدون تظاهر به صمیمیت مصنوعی.
"""

from groq import Groq

import config
from settings import load_settings
from utils.language import detect_language

_client = Groq(api_key=config.GROQ_API_KEY)

SYSTEM_PROMPT_FA = (
    "تو گابیمارو هستی، یک ربات هوش مصنوعی داخل تلگرام. "
    "با لحن محاوره‌ای و عامیانه‌ی خودمونی جواب بده، دقیقاً همونجوری که "
    "یه آدم عادی توی چت تایپ می‌کنه، نه رسمی و نه با ادای دوستی مصنوعی. "
    "جواب‌ها کوتاه و مستقیم باشن. از ایموجی خیلی کم استفاده کن، فقط "
    "توی موارد حساس یا مهم یه ایموجی مناسب بذار، نه در حد تزئین."
)

SYSTEM_PROMPT_EN = (
    "You are Gabimaru, an AI bot inside Telegram. "
    "Reply in a casual, slang-heavy, everyday texting tone — not formal, "
    "and not overly friendly or performative. Keep replies short and direct. "
    "Use emojis rarely, only for sensitive or important moments, not as decoration."
)


def generate_response(user_message: str, history: list[dict] | None = None) -> str:
    """
    تولید پاسخ هوش مصنوعی بر اساس پیام کاربر و تاریخچه مکالمه (در صورت وجود).
    history لیستی از دیکشنری‌های {"role": "user"/"assistant", "content": "..."} است.
    """
    settings = load_settings()
    model = settings.get("model", config.DEFAULT_MODEL)
    temperature = settings.get("temperature", config.DEFAULT_TEMPERATURE)

    language = detect_language(user_message)
    system_prompt = SYSTEM_PROMPT_FA if language == "fa" else SYSTEM_PROMPT_EN

    messages = [{"role": "system", "content": system_prompt}]
    if history:
        messages.extend(history)
    messages.append({"role": "user", "content": user_message or "سلام"})

    try:
        completion = _client.chat.completions.create(
            model=model,
            temperature=temperature,
            messages=messages,
        )
        return completion.choices[0].message.content.strip()
    except Exception:
        return (
            "یه مشکلی موقع پاسخ دادن پیش اومد، دوباره امتحان کن 🙏"
            if language == "fa"
            else "Something went wrong while generating a response, please try again 🙏"
        )