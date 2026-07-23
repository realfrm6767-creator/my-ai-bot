"""
permissions.py
--------------
تمام منطق مربوط به سطوح دسترسی کاربران (Owner / Admin / User).

توابعی که در مرحله چهارم پیاده‌سازی می‌شوند:
    - is_owner(user_id)
    - is_admin(user_id)
    - has_panel_access(user_id)
    - add_admin(user_id)
    - remove_admin(user_id)

نکته: دستور /setowner در این پروژه وجود ندارد؛ Owner همیشه از config.py
(Environment Variable OWNER_ID) تعیین می‌شود.
"""