"""
ai.py
-----
اتصال به سرویس هوش مصنوعی Groq و تولید پاسخ.
لحن پاسخ‌ها خودمونی و دوستانه است، نه رسمی.
"""

from groq import Groq

import config
from settings import load_settings
from utils.language import detect_language

_client = Groq(api_key=config.GROQ_API_KEY)

SYSTEM_PROMPT_FA = (
    "تو گابیمارو هستی، یک ربات هوش مصنوعی دوستانه و خودمونی داخل تلگرام. "
    "با لحن صمیمی، ساده و کوتاه فارسی جواب بده. از ایموجی مناسب استفاده کن. "
    "رسمی و خشک صحبت نکن."
)

SYSTEM_PROMPT_EN = (
    "You are Gabimaru, a friendly and casual AI assistant inside Telegram. "
    "Reply in a warm, simple, and concise tone in English. Use emojis where fitting. "
    "Avoid sounding formal or robotic."
)


def generate_response(user_message: str) -> str:
    """
    تولید پاسخ هوش مصنوعی بر اساس پیام کاربر.
    فعلاً بدون تاریخچه مکالمه (History) کار می‌کند؛ اتصال Memory در مرحله ششم اضافه می‌شود.
    """
    settings = load_settings()
    model = settings.get("model", config.DEFAULT_MODEL)
    temperature = settings.get("temperature", config.DEFAULT_TEMPERATURE)

    language = detect_language(user_message)
    system_prompt = SYSTEM_PROMPT_FA if language == "fa" else SYSTEM_PROMPT_EN

    try:
        completion = _client.chat.completions.create(
            model=model,
            temperature=temperature,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message or "سلام"},
            ],
        )
        return completion.choices[0].message.content.strip()
    except Exception:
        return (
            "یه مشکلی موقع پاسخ دادن پیش اومد، دوباره امتحان کن 🙏"
            if language == "fa"
            else "Something went wrong while generating a response, please try again 🙏"
        )


# TODO (مرحله ششم): اضافه کردن پارامتر history و ارسال آن به messages
#                     در صورت روشن بودن Memory کاربر