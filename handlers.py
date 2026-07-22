from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)

from telegram.ext import (
    ContextTypes,
)

from permissions import Permission


async def panel(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user_id = update.effective_user.id

    if not Permission.has_panel_access(user_id):

        await update.message.reply_text(
            "❌ دسترسی نداری."
        )

        return

    keyboard = [

        [
            InlineKeyboardButton(
                "🤖 AI",
                callback_data="panel_ai"
            )
        ],

        [
            InlineKeyboardButton(
                "⚙ Settings",
                callback_data="panel_settings"
            )
        ],

        [
            InlineKeyboardButton(
                "📊 Statistics",
                callback_data="panel_stats"
            )
        ],

        [
            InlineKeyboardButton(
                "❓ Help",
                callback_data="panel_help"
            )
        ]

    ]

    await update.message.reply_text(

        "پنل مدیریت",

        reply_markup=InlineKeyboardMarkup(keyboard)

    )

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query

    await query.answer()

    data = query.data

    if data == "panel_ai":

        await query.edit_message_text(

            "🤖 بخش هوش مصنوعی\n\n"

            "به زودی تکمیل می‌شود."

        )

        return

    if data == "panel_settings":

        await query.edit_message_text(

            "⚙ تنظیمات\n\n"

            "به زودی تکمیل می‌شود."

        )

        return

    if data == "panel_stats":

        await query.edit_message_text(

            "📊 آمار\n\n"

            "به زودی تکمیل می‌شود."

        )

        return

    if data == "panel_help":

        await query.edit_message_text(

            "❓ راهنما\n\n"

            "به زودی تکمیل می‌شود."

        )

        return

from ai import ask_ai
from memory import memory


async def chat_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if not update.message:
        return

    user_id = update.effective_user.id
    text = update.message.text

    memory.add(user_id, "user", text)

    response = await ask_ai(user_id, text)

    memory.add(user_id, "assistant", response)

    await update.message.reply_text(response)