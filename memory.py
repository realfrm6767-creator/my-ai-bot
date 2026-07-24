"""
memory.py
---------
مدیریت حافظه (تاریخچه مکالمه) کاربران، مستقل از ai.py.
هر کاربر در هر چت، تاریخچه‌ی جداگانه‌ی خودش را دارد.
داده‌ها در memory_store.json ذخیره می‌شوند.
"""

import json
import os

import config
from settings import load_settings

MEMORY_FILE = os.path.join(os.path.dirname(__file__), "memory_store.json")

MAX_HISTORY_MESSAGES = 20  # حداکثر تعداد پیام نگه‌داشته‌شده برای هر کاربر


def _load() -> dict:
    try:
        with open(MEMORY_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}


def _save(data: dict) -> None:
    with open(MEMORY_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def _key(chat_id: int, user_id: int) -> str:
    return f"{chat_id}:{user_id}"


def is_memory_enabled() -> bool:
    """بررسی می‌کند که آیا حافظه مکالمه (سراسری) روشن است یا خاموش."""
    settings = load_settings()
    return settings.get("memory", config.DEFAULT_MEMORY_STATE)


def get_history(chat_id: int, user_id: int) -> list[dict]:
    """تاریخچه مکالمه‌ی کاربر را برمی‌گرداند (لیستی از پیام‌های user/assistant)."""
    data = _load()
    return data.get(_key(chat_id, user_id), [])


def add_message(chat_id: int, user_id: int, role: str, content: str) -> None:
    """یک پیام جدید (user یا assistant) به تاریخچه‌ی کاربر اضافه می‌کند."""
    data = _load()
    key = _key(chat_id, user_id)
    history = data.get(key, [])
    history.append({"role": role, "content": content})
    data[key] = history[-MAX_HISTORY_MESSAGES:]
    _save(data)


def clear_history(chat_id: int, user_id: int) -> None:
    """تاریخچه‌ی مکالمه‌ی کاربر را پاک می‌کند."""
    data = _load()
    key = _key(chat_id, user_id)
    if key in data:
        del data[key]
        _save(data)

def clear_chat_memory(chat_id: int) -> None:
    """تمام تاریخچه‌های مکالمه‌ی مربوط به یک چت (همه کاربران آن) را پاک می‌کند."""
    data = _load()
    prefix = f"{chat_id}:"
    for key in [k for k in data if k.startswith(prefix)]:
        del data[key]
    _save(data)