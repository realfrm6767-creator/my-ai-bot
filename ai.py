"""
ai.py
-----
هماهنگ‌کننده (Dispatcher) بین provider های مختلف هوش مصنوعی.
"""

import traceback

import config
from settings import load_settings
from utils.locales import get_system_prompt, t
from providers import groq_provider, gemini_provider

CODE_KEYWORDS = [
    "کد", "برنامه", "پایتون", "python", "کدنویسی", "تابع", "function",
    "bug", "دیباگ", "الگوریتم", "javascript", "html", "css", "sql",
]

ANALYTICAL_KEYWORDS = [
    "تحلیل", "مقایسه", "توضیح بده", "چرا", "علت", "بررسی", "خلاصه",
    "explain", "analyze", "compare", "summarize",
]


def _pick_auto_provider(user_message: str) -> str:
    lowered = user_message.lower()
    is_code = any(k in lowered for k in CODE_KEYWORDS)
    is_analytical = any(k in lowered for k in ANALYTICAL_KEYWORDS)
    is_long = len(user_message) > 200

    if is_code or is_analytical or is_long:
        return "gemini"
    return "groq"


def generate_response(
    user_message: str,
    history: list[dict] | None = None,
    quoted_message: str | None = None,
) -> str:
    settings = load_settings()
    provider = settings.get("provider", config.DEFAULT_PROVIDER)
    temperature = settings.get("temperature", config.DEFAULT_TEMPERATURE)
    lang = settings.get("language", config.DEFAULT_LANGUAGE)
    system_prompt = get_system_prompt(lang)

    final_message = user_message
    if quoted_message:
        final_message = (
            f"[پیامی که کاربر روی آن ریپلای کرده: \"{quoted_message}\"]\n"
            f"پیام کاربر: {user_message}"
        )

    active_provider = _pick_auto_provider(user_message) if provider == "auto" else provider

    try:
        if active_provider == "gemini":
            return gemini_provider.generate(system_prompt, final_message, history, temperature)
        return groq_provider.generate(system_prompt, final_message, history, temperature)
    except Exception:
        print(f"=== AI ERROR (provider={active_provider}) ===")
        print(traceback.format_exc())
        print("=== END AI ERROR ===")
        return t("ai_error", lang)