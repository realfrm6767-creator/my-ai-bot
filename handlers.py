"""
handlers.py
-----------
تمام Handlerهای تلگرام (دستورات، دکمه‌ها، پیام‌های چت) فقط اینجا نوشته می‌شوند.

قوانین پنل:
    - هرکسی می‌تواند پنل خودش را باز کند (پنل شخصی هر کاربر است).
    - فقط همان کاربری که پنل را باز کرده می‌تواند روی دکمه‌هایش کلیک کند.
    - هر بخش (AI, Settings, Statistics, Help) صفحه‌ی جدا با دکمه
      «🔙 بازگشت» دارد؛ از یک بخش مستقیم به بخش دیگر نمی‌رود.
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


# ---------------------------------------------------------------------------
# ساخت کیبوردها
# callback_data همیشه شامل آیدی صاحب پنل است: "action:owner_id"
# تا فقط خودش بتواند روی دکمه‌ها کلیک کند.
# ---------------------------------------------------------------------------

def build_main_keyboard(owner_id: int) -> InlineKeyboardMarkup:
    keyboard = [
        [InlineKeyboardButton("🤖 AI", callback_data=f"ai:{owner_id}")],
        [InlineKeyboardButton("⚙️ Settings", callback_data=f"settings:{owner_id}")],
        [InlineKeyboardButton("📊 Statistics", callback_data=f"statistics:{owner_id}")],
        [InlineKeyboardButton("❓ Help", callback_data=f"help:{owner_id}")],
    ]
    return InlineKeyboardMarkup(keyboard)


def build_back_keyboard(owner_id: int) -> InlineKeyboardMarkup:
    keyboard = [[InlineKeyboardButton("🔙 بازگشت", callback_data=f"back:{owner_id}")]]
    return InlineKeyboardMarkup(keyboard)


async def show_panel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """پنل برای همه‌ی کاربران باز می‌شود؛ ولی هرکس فقط پنل خودش را می‌بیند/کنترل می‌کند."""
    owner_id = update.effective_user.id
    await update.message.reply_text(
        "پنل مدیریت ربات 👇",
        reply_markup=build_main_keyboard(owner_id),
    )


def build_statistics_text(update: Update, target_user_id: int) -> str:
    """ساخت متن آمار شخصی کاربر."""
    query = update.callback_query
    chat_id = query.message.chat.id

    stats = get_user_stats(chat_id, target_user_id)
    rank_text = f"#{stats['rank']}" if stats["rank"] else "نامشخص"

    return (
        "📊 آمار شما\n\n"
        f"🆔 آیدی عددی: {target_user_id}\n"
        f"💬 تعداد پیام در این چت: {stats['message_count']}\n"
        f"🏆 رتبه در این چت: {rank_text}"
    )


async def send_profile_photo(context: ContextTypes.DEFAULT_TYPE, chat_id: int, user_id: int) -> None:
    """در صورت وجود عکس پروفایل، آن را به‌صورت یک پیام جدا ارسال می‌کند."""
    photos = await context.bot.get_user_profile_photos(user_id, limit=1)
    if photos.total_count > 0:
        file_id = photos.photos[0][-1].file_id
        await context.bot.send_photo(chat_id=chat_id, photo=file_id)


async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """مدیریت کلیک روی دکمه‌های پنل، با کنترل مالکیت پنل و سطح دسترسی."""
    query = update.callback_query
    clicker_id = query.from_user.id

    # جدا کردن action و owner_id از callback_data
    action, _, owner_id_str = query.data.partition(":")
    owner_id = int(owner_id_str)

    # فقط صاحب پنل اجازه‌ی کلیک دارد
    if clicker_id != owner_id:
        await query.answer("این پنل مال شما نیست 🙅‍♂️ خودتون یه پنل جدید باز کنید.", show_alert=True)
        return

    await query.answer()

    if action == "back":
        await query.edit_message_text("پنل مدیریت ربات 👇", reply_markup=build_main_keyboard(owner_id))
        return

    if action == "help":
        text = "راهنما — به‌زودی تکمیل می‌شود."

    elif action == "statistics":
        text = build_statistics_text(update, owner_id)
        await send_profile_photo(context, query.message.chat.id, owner_id)

    elif action == "settings":
        if is_owner(owner_id) or is_admin(owner_id):
            text = "بخش Settings — در مرحله هفتم تکمیل می‌شود."
        else:
            text = "🚫 شما به بخش Settings دسترسی ندارید."

    elif action == "ai":
        if is_owner(owner_id):
            text = "بخش AI — در مرحله پنجم تکمیل می‌شود."
        else:
            text = "🚫 این بخش فقط برای مالک ربات قابل دسترسی است."

    else:
        text = "بخش نامشخص."

    await query.edit_message_text(text, reply_markup=build_back_keyboard(owner_id))


async def chat_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """مسیریاب اصلی پیام‌های متنی معمولی."""
    text = update.message.text or ""

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
# TODO (آینده): افزودن دکمه‌های جدید به build_main_keyboard()،
#               هر بخش جدید باید صفحه جدا با build_back_keyboard() داشته باشد