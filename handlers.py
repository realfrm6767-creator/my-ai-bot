"""
handlers.py
-----------
تمام Handlerهای تلگرام (دستورات، دکمه‌ها، پیام‌های چت) فقط اینجا نوشته می‌شوند.

توابعی که در مراحل بعدی تکمیل خواهند شد:
    - panel()
    - button_handler()
    - chat_handler()
    - addadmin_handler()
    - removeadmin_handler()
"""

from telegram import Update
from telegram.ext import ContextTypes


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """دستور تست /start - فقط برای اطمینان از اجرای صحیح ربات روی Render (مرحله دوم)."""
    await update.message.reply_text("سلام! ربات با موفقیت روی Render اجرا شد. ✅")


# TODO (مرحله سوم): پیاده‌سازی panel() و button_handler()
# TODO (مرحله چهارم): اتصال به permissions.py برای کنترل دسترسی
# TODO (مرحله پنجم): اتصال chat_handler() به ai.py