"""
settings.py
-----------
مسئول خواندن و نوشتن فایل settings.json (تنظیمات پویای پروژه).
"""

import json

import config


def load_settings() -> dict:
    """خواندن تنظیمات؛ اگر فایل نبود یا خراب بود، مقدار پیش‌فرض برمی‌گردد."""
    try:
        with open(config.SETTINGS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {
            "admins": [],
            "provider": config.DEFAULT_PROVIDER,
            "model": config.DEFAULT_MODEL,
            "language": config.DEFAULT_LANGUAGE,
            "memory": config.DEFAULT_MEMORY_STATE,
            "temperature": config.DEFAULT_TEMPERATURE,
        }


def save_settings(data: dict) -> None:
    """ذخیره تنظیمات در settings.json."""
    with open(config.SETTINGS_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def get_setting(key: str):
    return load_settings().get(key)


def update_setting(key: str, value) -> None:
    data = load_settings()
    data[key] = value
    save_settings(data)