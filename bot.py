"""
bot.py
------
تنها مسئولیت این فایل:
    1. ساخت Application تلگرام
    2. ثبت Handlerها (از handlers.py)
    3. اجرای Polling
    4. اجرای Flask + Waitress
"""

import threading

from flask import Flask
from waitress import serve
from telegram.ext import Application, CommandHandler, CallbackQueryHandler

import config
from handlers import start_command, panel, button_handler


def run_web_server() -> None:
    """اجرای یک وب‌سرور ساده تا Render سرویس را زنده تشخیص دهد."""
    app = Flask(__name__)

    @app.route("/")
    def health_check():
        return "Gabimaru AI X is alive.", 200

    serve(app, host=config.HOST, port=config.PORT)


def main() -> None:
    """نقطه ورود اصلی برنامه."""
    web_thread = threading.Thread(target=run_web_server, daemon=True)
    web_thread.start()

    application = Application.builder().token(config.TELEGRAM_BOT_TOKEN).build()

    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("panel", panel))
    application.add_handler(CallbackQueryHandler(button_handler))

    application.run_polling()


if __name__ == "__main__":
    main()