
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

FULLWIDTH_DIGITS = str.maketrans("0123456789", "０１２３４５６７８９")

RANK_LABELS = {
    1: "🥇 نفر اول",
    2: "🥈 نفر دوم",
    3: "🥉 نفر سوم",
}


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


def build_main_keyboard(owner_id: int) -> InlineKeyboardMarkup:
    keyboard = [
        [InlineKeyboardButton("🤖 AI", callback_data=f"ai:{owner_id}")],
        [InlineKeyboardButton("⚙️ Settings", callback_data=f"settings:{owner_id}")],
        [InlineKeyboardButton("📊 Statistics", callback_data=f"statistics:{owner_id}")],
        [InlineKeyboardButton("❓ Help", callback_data=f"help:{owner_id}")],
    ]
    return InlineKeyboardMarkup(keyboard)


def build_back_keyboard(owner_id: int) -> InlineKeyboardMarkup:
    keyboard = [[InlineKeyboardButton("Back", callback_data=f"back:{owner_id}")]]
    return InlineKeyboardMarkup(keyboard)


async def show_panel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    owner_id = update.effective_user.id
    await update.message.reply_text(
        "پنل مدیریت ربات 👇",
        reply_markup=build_main_keyboard(owner_id),
    )


def get_user_role_label(user_id: int) -> str:
    if is_owner(user_id):
        return "مالک"
    if is_admin(user_id):
        return "ادمین"
    return "کاربر عادی"


def format_rank(rank: int | None) -> str:
    if rank is None:
        return "نامشخص"
    if rank in RANK_LABELS:
        return RANK_LABELS[rank]
    return f"#{rank}"


async def build_statistics_text(context: ContextTypes.DEFAULT_TYPE, update: Update, target_user_id: int) -> tuple[str, str | None]:
    """ساخت متن آمار کاربر (امروز + کل) طبق فرمت مشخص‌شده."""
    query = update.callback_query
    chat_id = query.message.chat.id

    user = await context.bot.get_chat(target_user_id)
    photos = await context.bot.get_user_profile_photos(target_user_id, limit=1)
    photo_count = photos.total_count
    photo_file_id = photos.photos[0][-1].file_id if photo_count > 0 else None

    full_name = " ".join(filter(None, [user.first_name, user.last_name])) or "نامشخص"
    username = f"@{user.username}" if user.username else "ندارد"
    role = get_user_role_label(target_user_id)

    stats = get_user_stats(chat_id, target_user_id)
    today_count_fmt = str(stats["today_count"]).translate(FULLWIDTH_DIGITS)
    total_count_fmt = str(stats["total_count"]).translate(FULLWIDTH_DIGITS)
    photo_count_fmt = str(photo_count).translate(FULLWIDTH_DIGITS)
    today_rank_fmt = format_rank(stats["today_rank"])
    total_rank_fmt = format_rank(stats["total_rank"])

    text = (
        f"◂ نام کاربر : {full_name}\n"
        f"◂ آیدی عددی : {target_user_id}\n"
        f"◂ یوزرنیم : {username}\n"
        f"◂ تعداد تصاویر پروفایل : {photo_count_fmt} عدد\n"
        f"◂ مقام کاربر : {role}\n\n"
        "─┅━ آمار کاربر ━┅─\n"
        f"◂ پیام های امروز : {today_count_fmt} عدد\n"
        f"◂ رتبه در تعداد پیام : {today_rank_fmt}\n"
        f"◂ کل پیام ها : {total_count_fmt} عدد\n"
        f"◂ رتبه در کل پیام ها : {total_rank_fmt}"
    )

    return text, photo_file_id


async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    clicker_id = query.from_user.id

    action, _, owner_id_str = query.data.partition(":")
    owner_id = int(owner_id_str)

    if clicker_id != owner_id:
        await query.answer("این پنل مال شما نیست 🙅‍♂️ خودتون یه پنل جدید باز کنید.", show_alert=True)
        return

    await query.answer()

    if action == "back":
        await query.edit_message_text("پنل مدیریت ربات 👇", reply_markup=build_main_keyboard(owner_id))
        return

    if action == "help":
        text = "راهنما — به‌زودی تکمیل می‌شود."
        await query.edit_message_text(text, reply_markup=build_back_keyboard(owner_id))

    elif action == "statistics":
        text, photo_file_id = await build_statistics_text(context, update, owner_id)
        await query.edit_message_text(text, reply_markup=build_back_keyboard(owner_id))
        if photo_file_id:
            await context.bot.send_photo(chat_id=query.message.chat.id, photo=photo_file_id)

    elif action == "settings":
        if is_owner(owner_id) or is_admin(owner_id):
            text = "بخش Settings — در مرحله هفتم تکمیل می‌شود."
        else:
            text = "🚫 شما به بخش Settings دسترسی ندارید."
        await query.edit_message_text(text, reply_markup=build_back_keyboard(owner_id))

    elif action == "ai":
        if is_owner(owner_id):
            text = "بخش AI — در مرحله پنجم تکمیل می‌شود."
        else:
            text = "🚫 این بخش فقط برای مالک ربات قابل دسترسی است."
        await query.edit_message_text(text, reply_markup=build_back_keyboard(owner_id))

    else:
        await query.edit_message_text("بخش نامشخص.", reply_markup=build_back_keyboard(owner_id))


async def chat_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
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
# TODO (آینده): افزودن دکمه‌های جدید به build_main_keyboard()