"""
handlers.py
-----------
تمام Handlerهای تلگرام (دستورات، دکمه‌ها، پیام‌های چت) فقط اینجا نوشته می‌شوند.
"""

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes

from permissions import (
    is_main_owner,
    is_owner,
    is_admin,
    add_owner,
    remove_owner,
    add_admin,
    remove_admin,
)
from utils.stats import record_message, get_user_stats
from ai import generate_response
from memory import get_history, add_message, is_memory_enabled

WAKE_WORDS = ["گابیمارو", "گابی"]

FULLWIDTH_DIGITS = str.maketrans("0123456789", "０１２３４５６７８９")

RANK_LABELS = {
    1: "🥇 نفر اول",
    2: "🥈 نفر دوم",
    3: "🥉 نفر سوم",
}

ROLE_COMMANDS = {
    "تنظیم مالک": "set_owner",
    "حذف مالک": "remove_owner",
    "تنظیم مدیر": "set_admin",
    "حذف مدیر": "remove_admin",
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
    if is_main_owner(user_id):
        return "مالک اصلی"
    if is_owner(user_id):
        return "مالک"
    if is_admin(user_id):
        return "مدیر"
    return "کاربر عادی"


def format_rank(rank: int | None) -> str:
    if rank is None:
        return "نامشخص"
    if rank in RANK_LABELS:
        return RANK_LABELS[rank]
    return f"#{rank}"


async def build_statistics_text(context: ContextTypes.DEFAULT_TYPE, update: Update, target_user_id: int) -> str:
    query = update.callback_query
    chat_id = query.message.chat.id

    user = await context.bot.get_chat(target_user_id)
    photos = await context.bot.get_user_profile_photos(target_user_id, limit=1)
    photo_count = photos.total_count

    full_name = " ".join(filter(None, [user.first_name, user.last_name])) or "نامشخص"
    username = f"@{user.username}" if user.username else "ندارد"
    role = get_user_role_label(target_user_id)

    stats = get_user_stats(chat_id, target_user_id)
    today_count_fmt = str(stats["today_count"]).translate(FULLWIDTH_DIGITS)
    total_count_fmt = str(stats["total_count"]).translate(FULLWIDTH_DIGITS)
    photo_count_fmt = str(photo_count).translate(FULLWIDTH_DIGITS)
    today_rank_fmt = format_rank(stats["today_rank"])
    total_rank_fmt = format_rank(stats["total_rank"])

    return (
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
        text = (
            "راهنمای گابیمارو 🤖\n\n"
            "کافیه اسمم رو صدا بزنی (گابی یا گابیمارو) و هرچی می‌خوای بگی، "
            "یا مستقیم روی پیام‌هام ریپلای کنی 🙂"
        )
        await query.edit_message_text(text, reply_markup=build_back_keyboard(owner_id))

    elif action == "statistics":
        text = await build_statistics_text(context, update, owner_id)
        await query.edit_message_text(text, reply_markup=build_back_keyboard(owner_id))

    elif action == "settings":
        if is_main_owner(owner_id) or is_owner(owner_id) or is_admin(owner_id):
            text = "بخش Settings — در مرحله هفتم تکمیل می‌شود."
        else:
            text = "🚫 شما به بخش Settings دسترسی ندارید."
        await query.edit_message_text(text, reply_markup=build_back_keyboard(owner_id))

    elif action == "ai":
        if is_main_owner(owner_id) or is_owner(owner_id):
            text = "🤖 هوش مصنوعی گابیمارو فعاله! کافیه اسمم رو صدا بزنی و سوالت رو بپرسی."
        else:
            text = "🚫 این بخش فقط برای مالک قابل دسترسی است."
        await query.edit_message_text(text, reply_markup=build_back_keyboard(owner_id))

    else:
        await query.edit_message_text("بخش نامشخص.", reply_markup=build_back_keyboard(owner_id))


def build_user_mention(user_id: int, name: str) -> str:
    """ساخت منشن قابل‌کلیک؛ فقط اسم نمایش داده می‌شود و به پروفایل کاربر لینک می‌خورد."""
    return f'<a href="tg://user?id={user_id}">{name}</a>'


def format_role_message(mention: str, body: str) -> str:
    """فرمت پیام‌های مدیریت نقش."""
    return f"▸ {mention}\n    {body}"


async def handle_role_command(update: Update, context: ContextTypes.DEFAULT_TYPE, command: str) -> None:
    reply = update.message.reply_to_message
    if reply is None or reply.from_user is None:
        await update.message.reply_text("باید روی پیام همون شخص ریپلای کنی.")
        return

    actor_id = update.effective_user.id
    target_user = reply.from_user
    target_id = target_user.id
    mention = build_user_mention(target_id, target_user.first_name)

    if command == "set_owner":
        if not is_main_owner(actor_id):
            await update.message.reply_text(
                "▸ دسترسی محدود\n    فقط مالک اصلی می‌تواند مالک تنظیم کند.", parse_mode="HTML"
            )
            return
        if add_owner(target_id):
            text = format_role_message(mention, "به‌عنوان مالک تنظیم شد.")
        else:
            text = format_role_message(mention, "در حال حاضر مالک است.")
        await update.message.reply_text(text, parse_mode="HTML")

    elif command == "remove_owner":
        if not is_main_owner(actor_id):
            await update.message.reply_text(
                "▸ دسترسی محدود\n    فقط مالک اصلی می‌تواند مالک را حذف کند.", parse_mode="HTML"
            )
            return
        if remove_owner(target_id):
            text = format_role_message(mention, "از لیست مالکان ربات حذف شد.")
        else:
            text = format_role_message(mention, "در لیست مالکان ربات وجود ندارد.")
        await update.message.reply_text(text, parse_mode="HTML")

    elif command == "set_admin":
        if not (is_main_owner(actor_id) or is_owner(actor_id)):
            await update.message.reply_text(
                "▸ دسترسی محدود\n    فقط مالک اصلی یا مالک‌ها می‌توانند مدیر تنظیم کنند.", parse_mode="HTML"
            )
            return
        if add_admin(target_id):
            text = format_role_message(mention, "به‌عنوان مدیر تنظیم شد.")
        else:
            text = format_role_message(mention, "در لیست مدیران ربات وجود دارد.")
        await update.message.reply_text(text, parse_mode="HTML")

    elif command == "remove_admin":
        if not (is_main_owner(actor_id) or is_owner(actor_id)):
            await update.message.reply_text(
                "▸ دسترسی محدود\n    فقط مالک اصلی یا مالک‌ها می‌توانند مدیر را حذف کنند.", parse_mode="HTML"
            )
            return
        if remove_admin(target_id):
            text = format_role_message(mention, "از لیست مدیران ربات حذف شد.")
        else:
            text = format_role_message(mention, "در لیست مدیران ربات وجود ندارد.")
        await update.message.reply_text(text, parse_mode="HTML")


async def chat_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    text = update.message.text or ""

    record_message(update.effective_chat.id, update.effective_user.id)

    wake_word_present = has_wake_word(text)
    replied_to_bot = await is_reply_to_bot(update, context)

    if not wake_word_present and not replied_to_bot:
        return

    content = strip_wake_word(text) if wake_word_present else text.strip()

    if content in ROLE_COMMANDS:
        await handle_role_command(update, context, ROLE_COMMANDS[content])
        return

    if content == "پنل":
        await show_panel(update, context)
        return

    chat_id = update.effective_chat.id
    user_id = update.effective_user.id
    message_for_ai = content if content else text

    memory_on = is_memory_enabled()
    history = get_history(chat_id, user_id) if memory_on else None

    await context.bot.send_chat_action(chat_id=chat_id, action="typing")
    ai_reply = generate_response(message_for_ai, history)
    await update.message.reply_text(ai_reply)

    if memory_on:
        add_message(chat_id, user_id, "user", message_for_ai)
        add_message(chat_id, user_id, "assistant", ai_reply)


# TODO (مرحله هفتم): تکمیل واقعی بخش Settings (شامل روشن/خاموش کردن Memory)
# TODO (آینده): افزودن دکمه‌های جدید به build_main_keyboard()، و کارکرد واقعی
#               تعویض مدل/provider داخل بخش AI پنل