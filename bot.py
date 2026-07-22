import os
import json
import logging

from flask import Flask

from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)

from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

logging.basicConfig(
    format="%(asctime)s | %(levelname)s | %(message)s",
    level=logging.INFO
)

TOKEN = os.getenv("TELEGRAM_TOKEN")
PORT = int(os.getenv("PORT", 10000))

SETTINGS_FILE = "settings.json"

app = Flask(__name__)

@app.route("/")
def home():
    return "Gabimaru AI X Online"

class SettingsManager:

    DEFAULT = {
        "owner": 0,
        "admins": [],
        "provider": "groq",
        "model": "openai/gpt-oss-120b",
        "language": "fa",
        "memory": True,
    }

    @classmethod
    def load(cls):

        if not os.path.exists(SETTINGS_FILE):

            cls.save(cls.DEFAULT)

        with open(
            SETTINGS_FILE,
            "r",
            encoding="utf-8"
        ) as f:

            return json.load(f)

    @classmethod
    def save(cls, data):

        with open(
            SETTINGS_FILE,
            "w",
            encoding="utf-8"
        ) as f:

            json.dump(
                data,
                f,
                ensure_ascii=False,
                indent=4
            )

class PermissionManager:

    @staticmethod
    def is_owner(user_id):

        data = SettingsManager.load()

        return user_id == data["owner"]

    @staticmethod
    def is_admin(user_id):

        data = SettingsManager.load()

        return user_id in data["admins"]

    @staticmethod
    def can_open_panel(user_id):

        return (
            PermissionManager.is_owner(user_id)
            or
            PermissionManager.is_admin(user_id)
            )

class AIManager:

    @staticmethod
    def provider():

        return SettingsManager.load()["provider"]

    @staticmethod
    def model():

        return SettingsManager.load()["model"]

    @staticmethod
    def language():

        return SettingsManager.load()["language"]

    @staticmethod
    def memory():

        return SettingsManager.load()["memory"]

async def panel(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user = update.effective_user.id

    if not PermissionManager.can_open_panel(user):

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

