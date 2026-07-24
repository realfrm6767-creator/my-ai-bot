"""
utils/status.py
----------------
ردیابی زمان شروع ربات و ساخت گزارش وضعیت (آپتایم، تعداد گروه‌ها و کاربران).
"""

import time

from utils.stats import get_global_counts

_start_time = time.time()


def mark_start_time() -> None:
    """زمان شروع اجرای ربات را ثبت می‌کند؛ باید یک‌بار موقع راه‌اندازی صدا زده شود."""
    global _start_time
    _start_time = time.time()


def get_uptime_seconds() -> int:
    return int(time.time() - _start_time)


def format_uptime(seconds: int) -> str:
    days, rem = divmod(seconds, 86400)
    hours, rem = divmod(rem, 3600)
    minutes, _ = divmod(rem, 60)
    parts = []
    if days:
        parts.append(f"{days}d")
    if hours:
        parts.append(f"{hours}h")
    parts.append(f"{minutes}m")
    return " ".join(parts)


def get_status_data() -> dict:
    total_chats, total_users = get_global_counts()
    return {
        "uptime": format_uptime(get_uptime_seconds()),
        "total_chats": total_chats,
        "total_users": total_users,
    }