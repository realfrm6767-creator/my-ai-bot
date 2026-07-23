"""
handlers.py
-----------
تمام Handlerهای تلگرام (دستورات، دکمه‌ها، پیام‌های چت) فقط اینجا نوشته می‌شوند.

به‌جای دستورات اسلش (/panel)، ربات با تشخیص عبارات طبیعی فعال می‌شود.
کاربر باید نام ربات (گابی یا گابیمارو) را همراه درخواست بگوید، مثلاً:
    "گابی پنل" یا "گابیمارو پنل"
"""

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes

# نام‌های مجاز برای صدا زدن ربات
WAKE_WORDS = ["گابیمارو", "گابی"]


def has_wake_word(text: str) -> bool:
    """بررسی می‌کند که آیا پیام حاوی نام ربات هست یا نه."""
    return any(wake_word in text for wake_word in WAKE_WORDS)


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """دستور /start - این یکی طبق قرارداد تلگرام همیشه با / باقی می‌ماند."""
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


async def show_panel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """نمایش پنل اصلی (با گفتن «گابی پنل» یا «گابیمارو پنل»)."""
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


async def chat_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    مسیریاب اصلی پیام‌های متنی معمولی.
    اگر پیام شامل نام ربات (گابی/گابیمارو) باشد، بسته به کلمه‌ی بعدی
    به بخش مربوطه هدایت می‌شود. در غیر این صورت (در مراحل بعدی) به ai.py می‌رود.
    """
    text = update.message.text or ""

    if not has_wake_word(text):
        # TODO (مرحله پنجم): اگر پیام عادی بود (بدون نام ربات)، به ai.py فرستاده شود
        return

    # تشخیص دستور بر اساس کلمه‌ی همراه نام ربات
    if "پنل" in text:
        await show_panel(update, context)
        return

    # TODO: اضافه کردن سایر عبارات (راهنما، آمار فوتبال، قیمت ارز و ...) در مراحل آینده
    await update.message.reply_text(
        "متوجه نشدم چی خواستی. فعلاً فقط «پنل» رو می‌شناسم 🙂"
    )


# TODO (مرحله چهارم): اتصال show_panel() و button_handler() به permissions.py
# TODO (مرحله پنجم): اتصال بخش AI در chat_handler() به ai.py
# TODO (مرحله هفتم): تکمیل واقعی بخش Settings داخل button_handler()