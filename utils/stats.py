"""
utils/stats.py
--------------
ردیابی ساده تعداد پیام‌های هر کاربر در هر گروه/چت،
برای نمایش در بخش Statistics پنل (تعداد پیام و رتبه در گروه).

داده‌ها در stats.json ذخیره می‌شوند (مشابه settings.json، مستقل از آن).
"""

import json
import os

STATS_FILE = os.path.join(os.path.dirname(os.path.dirname(__file__)), "stats.json")


def _load() -> dict:
    try:
        with open(STATS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}


def _save(data: dict) -> None:
    with open(STATS_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def record_message(chat_id: int, user_id: int) -> None:
    """هر پیام جدید کاربر در یک چت را ثبت می‌کند."""
    data = _load()
    chat_key, user_key = str(chat_id), str(user_id)
    data.setdefault(chat_key, {})
    data[chat_key][user_key] = data[chat_key].get(user_key, 0) + 1
    _save(data)


def get_user_stats(chat_id: int, user_id: int) -> dict:
    """تعداد پیام و رتبه‌ی کاربر در همان چت را برمی‌گرداند."""
    data = _load()
    chat_key, user_key = str(chat_id), str(user_id)
    chat_data = data.get(chat_key, {})
    count = chat_data.get(user_key, 0)

    ranking = sorted(chat_data.items(), key=lambda item: item[1], reverse=True)
    rank = next((i + 1 for i, (uid, _) in enumerate(ranking) if uid == user_key), None)

    return {
        "message_count": count,
        "rank": rank,
        "total_users_in_chat": len(chat_data),
    }