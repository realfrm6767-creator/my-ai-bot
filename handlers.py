"""
handlers.py
-----------
تمام Handlerهای تلگرام (دستورات، دکمه‌ها، پیام‌های چت) فقط اینجا نوشته می‌شوند.
"""

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes

import config
from permissions import (
    is_main_owner, is_owner, is_admin,
    add_owner, remove_owner, add_admin, remove_admin,
)
from settings import load_settings, update_setting
from utils.stats import record_message, get_user_stats
from ai import generate_response
from memory import get_history, add_message, is_memory_enabled, clear_chat_memory
from utils.locales import t, get_role_commands, get_panel_trigger, SUPPORTED_LANGUAGES, LANGUAGE_NAMES

WAKE_WORDS = ["گابیمارو", "گابی"]
FULLWIDTH_DIGITS = str.maketrans("0123456789", "０１２３４５６７８９")


def get_current_language() -> str:
    return load_settings().get("language", config.DEFAULT_LANGUAGE)


def format_number(n: int, lang: str) -> str:
    return str(n).translate(FULLWIDTH_DIGITS) if lang == "fa" else str(n)


def has_wake_word(text: str) -> bool:
    return any(w in text for w in WAKE_WORDS)


def strip_wake_word(text: str) -> str:
    cleaned = text
    for w in WAKE_WORDS:
        cleaned = cleaned.replace(w, "")
    return cleaned.strip()


async def is_reply_to_bot(update: Update, context: ContextTypes.DEFAULT_TYPE) -> bool:
    reply = update.message.reply_to_message
    if reply is None or reply.from_user is None:
        return False
    return reply.from_user.id == context.bot.id


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("سلام! ربات با موفقیت روی Render اجرا شد. ✅")


def build_main_keyboard(owner_id: int, lang: str) -> InlineKeyboardMarkup:
    keyboard = [
        [InlineKeyboardButton(t("btn_ai", lang), callback_data=f"ai:{owner_id}")],
        [InlineKeyboardButton(t("btn_settings", lang), callback_data=f"settings:{owner_id}")],
        [InlineKeyboardButton(t("btn_statistics", lang), callback_data=f"statistics:{owner_id}")],
        [InlineKeyboardButton(t("btn_help", lang), callback_data=f"help:{owner_id}")],
    ]
    return InlineKeyboardMarkup(keyboard)


def build_back_keyboard(owner_id: int, lang: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup([[InlineKeyboardButton(t("btn_back", lang), callback_data=f"back:{owner_id}")]])


def build_settings_keyboard(owner_id: int, lang: str) -> InlineKeyboardMarkup:
    memory_label = t("btn_memory_on", lang) if is_memory_enabled() else t("btn_memory_off", lang)
    keyboard = [
        [InlineKeyboardButton(t("btn_language", lang), callback_data=f"settings_language:{owner_id}")],
        [InlineKeyboardButton(memory_label, callback_data=f"settings_memory_toggle:{owner_id}")],
        [InlineKeyboardButton(t("btn_memory_reset", lang), callback_data=f"settings_memory_reset:{owner_id}")],
        [InlineKeyboardButton(t("btn_back", lang), callback_data=f"back:{owner_id}")],
    ]
    return InlineKeyboardMarkup(keyboard)


def build_language_keyboard(owner_id: int, lang: str) -> InlineKeyboardMarkup:
    keyboard = [[InlineKeyboardButton(LANGUAGE_NAMES[code], callback_data=f"setlang_{code}:{owner_id}")] for code in SUPPORTED_LANGUAGES]
    keyboard.append([InlineKeyboardButton(t("btn_back", lang), callback_data=f"settings:{owner_id}")])
    return InlineKeyboardMarkup(keyboard)


async def show_panel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    owner_id = update.effective_user.id
    lang = get_current_language()
    await update.message.reply_text(t("panel_intro", lang), reply_markup=build_main_keyboard(owner_id, lang))


def get_user_role_label(user_id: int, lang: str) -> str:
    if is_main_owner(user_id):
        return t("role_main_owner", lang)
    if is_owner(user_id):
        return t("role_owner", lang)
    if is_admin(user_id):
        return t("role_admin", lang)
    return t("role_regular", lang)


def format_rank(rank: int | None, lang: str) -> str:
    if rank is None:
        return t("rank_unknown", lang)
    if rank == 1:
        return t("rank_1", lang)
    if rank == 2:
        return t("rank_2", lang)
    if rank == 3:
        return t("rank_3", lang)
    return f"#{rank}"


async def build_statistics_text(context: ContextTypes.DEFAULT_TYPE, update: Update, target_user_id: int, lang: str) -> str:
    query = update.callback_query
    chat_id = query.message.chat.id

    user = await context.bot.get_chat(target_user_id)
    photos = await context.bot.get_user_profile_photos(target_user_id, limit=1)
    photo_count = photos.total_count

    full_name = " ".join(filter(None, [user.first_name, user.last_name])) or "—"
    username = f"@{user.username}" if user.username else t("stat_username_none", lang)
    role = get_user_role_label(target_user_id, lang)

    stats = get_user_stats(chat_id, target_user_id)
    unit = t("stat_photo_unit", lang)
    unit_suffix = f" {unit}" if unit else ""

    return (
        f"◂ {t('stat_name', lang)} : {full_name}\n"
        f"◂ {t('stat_id', lang)} : {target_user_id}\n"
        f"◂ {t('stat_username', lang)} : {username}\n"
        f"◂ {t('stat_photo_count', lang)} : {format_number(photo_count, lang)}{unit_suffix}\n"
        f"◂ {t('stat_role', lang)} : {role}\n\n"
        f"─┅━ {t('stat_header', lang)} ━┅─\n"
        f"◂ {t('stat_today', lang)} : {format_number(stats['today_count'], lang)}{unit_suffix}\n"
        f"◂ {t('stat_today_rank', lang)} : {format_rank(stats['today_rank'], lang)}\n"
        f"◂ {t('stat_total', lang)} : {format_number(stats['total_count'], lang)}{unit_suffix}\n"
        f"◂ {t('stat_total_rank', lang)} : {format_rank(stats['total_rank'], lang)}"
    )


async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    clicker_id = query.from_user.id
    action, _, owner_id_str = query.data.partition(":")
    owner_id = int(owner_id_str)
    lang = get_current_language()

    if clicker_id != owner_id:
        await query.answer(t("not_your_panel", lang), show_alert=True)
        return

    await query.answer()

    if action == "back":
        await query.edit_message_text(t("panel_intro", lang), reply_markup=build_main_keyboard(owner_id, lang))
        return

    if action == "help":
        await query.edit_message_text(t("help_text", lang), reply_markup=build_back_keyboard(owner_id, lang))
        return

    if action == "statistics":
        text = await build_statistics_text(context, update, owner_id, lang)
        await query.edit_message_text(text, reply_markup=build_back_keyboard(owner_id, lang))
        return

    if action == "ai":
        text = t("ai_section_text", lang) if (is_main_owner(owner_id) or is_owner(owner_id)) else t("ai_access_denied", lang)
        await query.edit_message_text(text, reply_markup=build_back_keyboard(owner_id, lang))
        return

    if action == "settings":
        if not (is_main_owner(owner_id) or is_owner(owner_id) or is_admin(owner_id)):
            await query.edit_message_text(t("settings_access_denied", lang), reply_markup=build_back_keyboard(owner_id, lang))
            return
        await query.edit_message_text(t("settings_intro", lang), reply_markup=build_settings_keyboard(owner_id, lang))
        return

    if action == "settings_language":
        await query.edit_message_text(t("language_menu_intro", lang), reply_markup=build_language_keyboard(owner_id, lang))
        return

    if action == "settings_memory_toggle":
        update_setting("memory", not is_memory_enabled())
        await query.edit_message_text(t("settings_intro", lang), reply_markup=build_settings_keyboard(owner_id, lang))
        return

    if action == "settings_memory_reset":
        clear_chat_memory(query.message.chat.id)
        await query.edit_message_text(t("memory_reset_done", lang), reply_markup=build_back_keyboard(owner_id, lang))
        return

    if action.startswith("setlang_"):
        code = action.split("_", 1)[1]
        if code in SUPPORTED_LANGUAGES:
            update_setting("language", code)
            confirm = t("language_set_confirm", code).format(lang=LANGUAGE_NAMES[code])
            await query.edit_message_text(confirm, reply_markup=build_back_keyboard(owner_id, code))
        return

    await query.edit_message_text("Unknown section.", reply_markup=build_back_keyboard(owner_id, lang))


def build_user_mention(user_id: int, name: str) -> str:
    return f'<a href="tg://user?id={user_id}">{name}</a>'


def format_role_message(mention: str, body: str) -> str:
    return f"▸ {mention}\n    {body}"


async def handle_role_command(update: Update, context: ContextTypes.DEFAULT_TYPE, command: str, lang: str) -> None:
    reply = update.message.reply_to_message
    if reply is None or reply.from_user is None:
        await update.message.reply_text(t("role_reply_required", lang))
        return

    actor_id = update.effective_user.id
    target_user = reply.from_user
    mention = build_user_mention(target_user.id, target_user.first_name)

    def denied(key: str) -> str:
        return f"▸ {t('access_denied_title', lang)}\n    {t(key, lang)}"

    if command == "set_owner":
        if not is_main_owner(actor_id):
            await update.message.reply_text(denied("role_access_main_owner_only_set"), parse_mode="HTML")
            return
        text = format_role_message(mention, t("role_set_owner_ok", lang) if add_owner(target_user.id) else t("role_set_owner_already", lang))
        await update.message.reply_text(text, parse_mode="HTML")

    elif command == "remove_owner":
        if not is_main_owner(actor_id):
            await update.message.reply_text(denied("role_access_main_owner_only_remove"), parse_mode="HTML")
            return
        text = format_role_message(mention, t("role_remove_owner_ok", lang) if remove_owner(target_user.id) else t("role_remove_owner_not", lang))
        await update.message.reply_text(text, parse_mode="HTML")

    elif command == "set_admin":
        if not (is_main_owner(actor_id) or is_owner(actor_id)):
            await update.message.reply_text(denied("role_access_owner_level_set"), parse_mode="HTML")
            return
        text = format_role_message(mention, t("role_set_admin_ok", lang) if add_admin(target_user.id) else t("role_set_admin_already", lang))
        await update.message.reply_text(text, parse_mode="HTML")

    elif command == "remove_admin":
        if not (is_main_owner(actor_id) or is_owner(actor_id)):
            await update.message.reply_text(denied("role_access_owner_level_remove"), parse_mode="HTML")
            return
        text = format_role_message(mention, t("role_remove_admin_ok", lang) if remove_admin(target_user.id) else t("role_remove_admin_not", lang))
        await update.message.reply_text(text, parse_mode="HTML")


async def chat_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    text = update.message.text or ""
    record_message(update.effective_chat.id, update.effective_user.id)

    wake_word_present = has_wake_word(text)
    replied_to_bot = await is_reply_to_bot(update, context)

    if not wake_word_present and not replied_to_bot:
        return

    content = strip_wake_word(text) if wake_word_present else text.strip()
    lang = get_current_language()
    role_commands = get_role_commands(lang)

    if content in role_commands:
        await handle_role_command(update, context, role_commands[content], lang)
        return

    if content.casefold() == get_panel_trigger(lang).casefold():
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