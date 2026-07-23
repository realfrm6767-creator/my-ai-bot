"""
memory.py
---------
مدیریت حافظه (تاریخچه مکالمه) کاربران، مستقل از ai.py.

اگر Memory خاموش باشد -> هیچ History ای ارسال نمی‌شود.
اگر Memory روشن باشد  -> History همراه پیام جدید ارسال می‌شود.

توابعی که در مرحله ششم پیاده‌سازی می‌شوند:
    - get_history(user_id)
    - add_message(user_id, role, content)
    - clear_history(user_id)
    - is_memory_enabled()
"""