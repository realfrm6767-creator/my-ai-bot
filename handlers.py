from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)

from telegram.ext import (
    ContextTypes,
)

from permissions import Permission
from ai import ask_ai


async def panel(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if not update.message:
        return

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
                callback_data="panel_ai",
            )
        ],
        [
            InlineKeyboardButton(
                "⚙ Settings",
                callback_data="panel_settings",
            )
        ],
        [
            InlineKeyboardButton(
                "📊 Statistics",
                callback_data="panel_stats",
            )
        ],
        [
            InlineKeyboardButton(
                "❓ Help",
                callback_data="panel_help",
            )
        ],
    ]

    await update.message.reply_text(
        "پنل مدیریت",
        reply_markup=InlineKeyboardMarkup(keyboard),
    )


async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query

    if not query:
        return

    await query.answer()

    data = query.data

    pages = {
        "panel_ai":
            "🤖 بخش هوش مصنوعی\n\nبه زودی تکمیل می‌شود.",
        "panel_settings":
            "⚙ تنظیمات\n\nبه زودی تکمیل می‌شود.",
        "panel_stats":
            "📊 آمار\n\nبه زودی تکمیل می‌شود.",
        "panel_help":
            "❓ راهنما\n\nبه زودی تکمیل می‌شود.",
    }

    if data in pages:
        await query.edit_message_text(
            pages[data]
        )


async def chat_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if not update.message:
        return

    text = update.message.text

    if not text:
        return

    user_id = update.effective_user.id

    response = await ask_ai(
        user_id,
        text,
    )

    await update.message.reply_text(
        response
    )