"""
handlers.py
-----------
تمام Handlerهای تلگرام (دستورات، دکمه‌ها، پیام‌های چت) فقط اینجا نوشته می‌شوند.

قانون فعال‌سازی ربات (بدون دستور اسلش):
    - اگر پیام شامل نام ربات (گابی/گابیمارو) باشد -> بررسی می‌شود.
    - اگر پیام مستقیماً ریپلای روی پیام خود ربات باشد -> بررسی می‌شود.
    - در غیر این صورت (در گروه‌ها به‌خصوص) ربات کاملاً سکوت می‌کند.

فعلاً فقط دستور «پنل» شناخته شده است. تشخیص هوشمند بقیه‌ی پیام‌ها
(شامل پاسخ به سلام ساده یا سوالات عمومی) در مرحله پنجم (AI) اضافه
می‌شود؛ تا آن زمان عمداً هیچ پاسخ ثابتی داده نمی‌شود تا با پاسخ واقعی
هوش مصنوعی تداخل نکند.
"""

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes

# نام‌های مجاز برای صدا زدن ربات
WAKE_WORDS = ["گابیمارو", "گابی"]


def has_wake_word(text: str) -> bool:
    """بررسی می‌کند که آیا پیام حاوی نام ربات هست یا نه."""
    return any(wake_word in text for wake_word in WAKE_WORDS)


def strip_wake_word(text: str) -> str:
    """نام ربات را از پیام حذف می‌کند تا فقط محتوای اصلی درخواست باقی بماند."""
    cleaned = text
    for wake_word in WAKE_WORDS:
        cleaned = cleaned.replace(wake_word, "")
    return cleaned.strip()


async def is_reply_to_bot(update: Update, context: ContextTypes.DEFAULT_TYPE) -> bool:
    """بررسی می‌کند که آیا کاربر روی پیام قبلی خود ربات ریپلای کرده است."""
    reply = update.message.reply_to_message
    if reply is None or reply.from_user is None:
        return False
    return reply.from_user.id == context.bot.id


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
    """نمایش پنل اصلی."""
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
    """
    text = update.message.text or ""

    wake_word_present = has_wake_word(text)
    replied_to_bot = await is_reply_to_bot(update, context)

    if not wake_word_present and not replied_to_bot:
        # نه اسم ربات گفته شده، نه ریپلای روی ربات -> سکوت کامل
        return

    content = strip_wake_word(text) if wake_word_present else text.strip()

    if "پنل" in content:
        await show_panel(update, context)
        return

    # TODO (مرحله پنجم): تنها دستور فعلی «پنل» است. سایر پیام‌ها
    #                     (شامل صدا زدن ساده‌ی ربات بدون درخواست خاص،
    #                     یا سوالات عمومی، یا ریپلای بدون دستور مشخص)
    #                     عمداً فعلاً بدون پاسخ رها می‌شوند تا در مرحله
    #                     پنجم مستقیماً به ai.py وصل شده و خود هوش مصنوعی
    #                     پاسخ بدهد. هیچ پاسخ ثابتی اینجا اضافه نشود.
    return


# TODO (مرحله چهارم): اتصال show_panel() و button_handler() به permissions.py
# TODO (مرحله پنجم): اتصال بخش بالا در chat_handler() به ai.py برای پاسخ
#                     هوشمند به هر پیامی غیر از «پنل» (شامل سلام ساده،
#                     سوالات عمومی، فوتبال، ارز، طلا و ...) با ذکر منبع
#                     در صورت نیاز (مثلاً FotMob)
# TODO (مرحله هفتم): تکمیل واقعی بخش Settings داخل button_handler()