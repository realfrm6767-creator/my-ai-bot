"""
handlers.py
-----------
تمام Handlerهای تلگرام (دستورات، دکمه‌ها، پیام‌های چت) فقط اینجا نوشته می‌شوند.
"""

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """دستور تست /start."""
    await update.message.reply_text("سلام! ربات با موفقیت روی Render اجرا شد. ✅")


def build_panel_keyboard() -> InlineKeyboardMarkup:
    """ساخت دکمه‌های شیشه‌ای پنل اصلی."""
    keyboard = [
        [InlineKeyboardButton("🤖 AI", callback_data="panel_ai")],
        [InlineKeyboardButton("⚙️ Settings", callback_data="panel_settings")],
        [InlineKeyboardButton("📊 Statistics", callback_data="panel_statistics")],
        [InlineKeyboardButton("❓ Help", callback_data="panel_help")],
    ]
    return InlineKeyboardMarkup(keyboard)


async def panel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """دستور /panel - نمایش پنل اصلی."""
    await update.message.reply_text(
        "پنل مدیریت ربات 👇",
        reply_markup=build_panel_keyboard(),
    )


async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """مدیریت کلیک روی دکمه‌های پنل."""
    query = update.callback_query
    await query.answer()

    section_messages = {
        "panel_ai": "بخش AI — در مرحله پنجم تکمیل می‌شود.",
        "panel_settings": "بخش Settings — در مرحله هفتم تکمیل می‌شود.",
        "panel_statistics": "بخش Statistics — به‌زودی اضافه می‌شود.",
        "panel_help": "راهنما — به‌زودی تکمیل می‌شود.",
    }

    text = section_messages.get(query.data, "بخش نامشخص.")
    await query.edit_message_text(text, reply_markup=build_panel_keyboard())


# TODO (مرحله چهارم): اتصال panel() و button_handler() به permissions.py
# TODO (مرحله پنجم): اضافه کردن chat_handler() و اتصال به ai.py
# TODO (مرحله هفتم): تکمیل واقعی بخش Settings داخل button_handler()