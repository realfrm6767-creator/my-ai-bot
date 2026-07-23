"""
utils/stats.py
--------------
ردیابی تعداد پیام‌های امروز و کل هر کاربر در هر چت، برای نمایش
در بخش Statistics پنل. داده‌ها در stats.json ذخیره می‌شوند.
"""

import json
import os
from datetime import date

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


def _today() -> str:
    return date.today().isoformat()


def record_message(chat_id: int, user_id: int) -> None:
    """پیام امروز کاربر را در چت مربوطه ثبت می‌کند (برای شمارش امروز و کل)."""
    data = _load()
    chat_key, user_key, today = str(chat_id), str(user_id), _today()

    data.setdefault(chat_key, {})
    data[chat_key].setdefault(user_key, {})
    data[chat_key][user_key][today] = data[chat_key][user_key].get(today, 0) + 1
    _save(data)


def _rank_of(counts: dict, user_key: str) -> int | None:
    ranking = sorted(counts.items(), key=lambda item: item[1], reverse=True)
    return next((i + 1 for i, (uid, _) in enumerate(ranking) if uid == user_key), None)


def get_user_stats(chat_id: int, user_id: int) -> dict:
    """آمار امروز و کل کاربر، به‌همراه رتبه‌ی هرکدام در همان چت."""
    data = _load()
    chat_key, user_key, today = str(chat_id), str(user_id), _today()
    chat_data = data.get(chat_key, {})

    today_counts = {uid: days.get(today, 0) for uid, days in chat_data.items()}
    total_counts = {uid: sum(days.values()) for uid, days in chat_data.items()}

    return {
        "today_count": today_counts.get(user_key, 0),
        "today_rank": _rank_of(today_counts, user_key),
        "total_count": total_counts.get(user_key, 0),
        "total_rank": _rank_of(total_counts, user_key),
    }