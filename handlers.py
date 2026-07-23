"""
handlers.py
-----------
تمام Handlerهای تلگرام (دستورات، دکمه‌ها، پیام‌های چت) فقط اینجا نوشته می‌شوند.
"""

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes

from permissions import is_owner, is_admin
from utils.stats import record_message, get_user_stats

WAKE_WORDS = ["گابیمارو", "گابی"]


def has_wake_word(text: str) -> bool:
    return any(wake_word in text for wake_word in WAKE_WORDS)


def strip_wake_word(text: str) -> str:
    cleaned = text
    for wake_word in WAKE_WORDS:
        cleaned = cleaned.replace(wake_word, "")
    return cleaned.strip()


async def is_reply_to_bot(update: Update, context: ContextTypes.DEFAULT_TYPE) -> bool:
    reply = update.message.reply_to_message
    if reply is None or reply.from_user is None:
        return False
    return reply.from_user.id == context.bot.id


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("سلام! ربات با موفقیت روی Render اجرا شد. ✅")


def build_panel_keyboard() -> InlineKeyboardMarkup:
    keyboard = [
        [InlineKeyboardButton("🤖 AI", callback_data="panel_ai")],
        [InlineKeyboardButton("⚙️ Settings", callback_data="panel_settings")],
        [InlineKeyboardButton("📊 Statistics", callback_data="panel_statistics")],
        [InlineKeyboardButton("❓ Help", callback_data="panel_help")],
    ]
    return InlineKeyboardMarkup(keyboard)


async def show_panel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """پنل برای همه‌ی کاربران باز می‌شود."""
    await update.message.reply_text(
        "پنل مدیریت ربات 👇",
        reply_markup=build_panel_keyboard(),
    )


def build_statistics_text(update: Update) -> str:
    """ساخت متن آمار شخصی کاربری که پنل را باز کرده."""
    user = update.callback_query.from_user
    chat_id = update.callback_query.message.chat.id

    stats = get_user_stats(chat_id, user.id)
    full_name = " ".join(filter(None, [user.first_name, user.last_name]))
    username = f"@{user.username}" if user.username else "ندارد"

    rank_text = f"{stats['rank']} از {stats['total_users_in_chat']}" if stats["rank"] else "نامشخص"

    return (
        "📊 آمار شما\n\n"
        f"👤 نام: {full_name}\n"
        f"🔗 یوزرنیم: {username}\n"
        f"🆔 آیدی عددی: {user.id}\n"
        f"💬 تعداد پیام در این چت: {stats['message_count']}\n"
        f"🏆 رتبه در این چت: {rank_text}"
    )


async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """مدیریت کلیک روی دکمه‌های پنل، با اعمال سطح دسترسی هر بخش."""
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id

    if query.data == "panel_help":
        text = "راهنما — به‌زودی تکمیل می‌شود."

    elif query.data == "panel_statistics":
        text = build_statistics_text(update)

    elif query.data == "panel_settings":
        if is_owner(user_id) or is_admin(user_id):
            text = "بخش Settings — در مرحله هفتم تکمیل می‌شود."
        else:
            text = "🚫 شما به بخش Settings دسترسی ندارید."

    elif query.data == "panel_ai":
        if is_owner(user_id):
            text = "بخش AI — در مرحله پنجم تکمیل می‌شود."
        else:
            text = "🚫 این بخش فقط برای مالک ربات قابل دسترسی است."

    else:
        text = "بخش نامشخص."

    await query.edit_message_text(text, reply_markup=build_panel_keyboard())


async def chat_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """مسیریاب اصلی پیام‌های متنی معمولی."""
    text = update.message.text or ""

    # ثبت آمار هر پیام (چه خطاب به ربات باشد چه نباشد)
    record_message(update.effective_chat.id, update.effective_user.id)

    wake_word_present = has_wake_word(text)
    replied_to_bot = await is_reply_to_bot(update, context)

    if not wake_word_present and not replied_to_bot:
        return

    content = strip_wake_word(text) if wake_word_present else text.strip()

    if "پنل" in content:
        await show_panel(update, context)
        return

    # TODO (مرحله پنجم): اتصال به ai.py برای پاسخ هوشمند به سایر پیام‌ها
    return


# TODO (مرحله پنجم): اتصال بخش AI به ai.py
# TODO (مرحله هفتم): تکمیل واقعی بخش Settings
# TODO (آینده): افزودن دکمه‌های جدید به build_panel_keyboard() و
#               section_handling در button_handler() به همین روش