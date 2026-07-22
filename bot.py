import logging
import threading

from flask import Flask
from waitress import serve

from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

from config import (
    TELEGRAM_TOKEN,
    HOST,
    PORT,
    BOT_NAME,
)

from handlers import (
    panel,
    button_handler,
    chat_handler,
)

from permissions import Permission

logging.basicConfig(
    format="%(asctime)s | %(levelname)s | %(message)s",
    level=logging.INFO
)

app = Flask(__name__)


@app.route("/")
def home():
    return f"{BOT_NAME} Online"


async def set_owner(update, context: ContextTypes.DEFAULT_TYPE):

    data = Permission.load()

    if data["owner"] != 0:
        await update.message.reply_text("❌ Owner قبلاً ثبت شده.")
        return

    Permission.set_owner(update.effective_user.id)

    await update.message.reply_text("✅ شما Owner شدید.")


async def add_admin(update, context: ContextTypes.DEFAULT_TYPE):

    if not Permission.is_owner(update.effective_user.id):
        await update.message.reply_text("❌ فقط Owner.")
        return

    if len(context.args) != 1:
        await update.message.reply_text("/addadmin USER_ID")
        return

    Permission.add_admin(int(context.args[0]))

    await update.message.reply_text("✅ Admin اضافه شد.")


async def remove_admin(update, context: ContextTypes.DEFAULT_TYPE):

    if not Permission.is_owner(update.effective_user.id):
        return

    if len(context.args) != 1:
        return

    Permission.remove_admin(int(context.args[0]))

    await update.message.reply_text("✅ حذف شد.")


def run_web():

    serve(
        app,
        host=HOST,
        port=PORT,
    )


def build_application():

    application = Application.builder().token(TELEGRAM_TOKEN).build()

    application.add_handler(CommandHandler("panel", panel))
    application.add_handler(CommandHandler("setowner", set_owner))
    application.add_handler(CommandHandler("addadmin", add_admin))
    application.add_handler(CommandHandler("removeadmin", remove_admin))

    application.add_handler(CallbackQueryHandler(button_handler))

    application.add_handler(
        MessageHandler(
            filters.TEXT & ~filters.COMMAND,
            chat_handler,
        )
    )

    return application


def main():

    threading.Thread(
        target=run_web,
        daemon=True,
    ).start()

    application = build_application()

    print(f"{BOT_NAME} Started")

    application.run_polling(
        drop_pending_updates=True
    )


if __name__ == "__main__":
    main()