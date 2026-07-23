"""
permissions.py
--------------
تمام منطق مربوط به سطوح دسترسی کاربران فقط اینجا نوشته می‌شود.

سلسله‌مراتب دسترسی:
    - مالک اصلی  (ثابت، از config.py / OWNER_ID - فقط یک نفر، هرگز تغییر نمی‌کند)
    - مالک       (چند نفر می‌توانند باشند؛ فقط مالک اصلی اضافه/حذف می‌کند)
    - مدیر       (چند نفر می‌توانند باشند؛ مالک اصلی و مالک‌ها اضافه/حذف می‌کنند - خود مدیرها نمی‌توانند مدیر دیگر را حذف کنند)
    - کاربر عادی
"""

import config
from settings import load_settings, save_settings


def is_main_owner(user_id: int) -> bool:
    return user_id == config.OWNER_ID


def is_owner(user_id: int) -> bool:
    settings = load_settings()
    return user_id in settings.get("owners", [])


def is_admin(user_id: int) -> bool:
    settings = load_settings()
    return user_id in settings.get("admins", [])


def has_panel_access(user_id: int) -> bool:
    """پنل برای همه باز است."""
    return True


def add_owner(user_id: int) -> bool:
    settings = load_settings()
    owners = settings.get("owners", [])
    if user_id in owners or is_main_owner(user_id):
        return False
    owners.append(user_id)
    settings["owners"] = owners
    save_settings(settings)
    return True


def remove_owner(user_id: int) -> bool:
    settings = load_settings()
    owners = settings.get("owners", [])
    if user_id not in owners:
        return False
    owners.remove(user_id)
    settings["owners"] = owners
    save_settings(settings)
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