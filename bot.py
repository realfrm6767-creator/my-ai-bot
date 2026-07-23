"""
bot.py
------
تنها مسئولیت این فایل:
    1. ساخت Application تلگرام
    2. ثبت Handlerها (از handlers.py)
    3. اجرای Polling
    4. اجرای Flask + Waitress (برای بیدار نگه داشتن سرویس روی Render)

هیچ منطق دیگری نباید داخل این فایل نوشته شود.
"""

import threading

from flask import Flask
from waitress import serve
from telegram.ext import Application, CommandHandler

import config
from handlers import start_command


def run_web_server() -> None:
    """اجرای یک وب‌سرور ساده تا Render سرویس را زنده تشخیص دهد."""
    app = Flask(__name__)

    @app.route("/")
    def health_check():
        return "Gabimaru AI X is alive.", 200

    serve(app, host=config.HOST, port=config.PORT)


def main() -> None:
    """نقطه ورود اصلی برنامه."""
    # اجرای Flask + Waitress در یک Thread جدا (همزمان با Polling)
    web_thread = threading.Thread(target=run_web_server, daemon=True)
    web_thread.start()

    # ساخت Application تلگرام
    application = Application.builder().token(config.TELEGRAM_BOT_TOKEN).build()

    # ثبت Handlerها (فعلاً فقط /start برای تست مرحله دوم)
    application.add_handler(CommandHandler("start", start_command))

    # اجرای Polling
    application.run_polling()


if __name__ == "__main__":
    main()