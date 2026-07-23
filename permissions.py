"""
permissions.py
--------------
تمام منطق مربوط به سطوح دسترسی کاربران فقط اینجا نوشته می‌شود.

سطوح دسترسی:
    - Owner  (ثابت، از config.py خوانده می‌شود)
    - Admin  (داخل settings.json ذخیره می‌شود)
    - User   (کاربر عادی)

نکته: پنل برای همه باز می‌شود؛ محدودیت واقعی روی هر دکمه (مثل
Settings یا AI) در سطح button_handler اعمال می‌شود، نه در ورودی پنل.
"""

import config
from settings import load_settings, save_settings


def is_owner(user_id: int) -> bool:
    return user_id == config.OWNER_ID


def is_admin(user_id: int) -> bool:
    settings = load_settings()
    return user_id in settings.get("admins", [])


def has_panel_access(user_id: int) -> bool:
    """فعلاً همه کاربران اجازه‌ی باز کردن پنل را دارند."""
    return True


def add_admin(user_id: int) -> bool:
    settings = load_settings()
    admins = settings.get("admins", [])
    if user_id in admins:
        return False
    admins.append(user_id)
    settings["admins"] = admins
    save_settings(settings)
    return True


def remove_admin(user_id: int) -> bool:
    settings = load_settings()
    admins = settings.get("admins", [])
    if user_id not in admins:
        return False
    admins.remove(user_id)
    settings["admins"] = admins
    save_settings(settings)
    return True