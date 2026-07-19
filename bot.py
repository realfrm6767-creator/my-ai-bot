import os
import threading
from flask import Flask
import google.generativeai as genai
from telegram import Update
from telegram.ext import Application, MessageHandler, ContextTypes, filters

TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

genai.configure(api_key=GEMINI_API_KEY)

SYSTEM_INSTRUCTION = """
اسم تو گابی یا گابیمارو هست.
همیشه خیلی خودمونی، راحت و صمیمی حرف بزن، دقیقاً مثل یه رفیق قدیمی که داره با دوستاش چت می‌کنه.
از ایموجی خیلی کم استفاده کن یا اصلاً استفاده نکن.
به‌طور پیش‌فرض مودب و عادی باش، فحش نده.
فقط اگه طرف مقابل بهت بی‌ادبی کرد یا فحش داد، می‌تونی متقابلاً باهاش بی‌ادب باشی و فحش بدی (فحش رکیک جنسی مشکلی نداره)، ولی هیچ‌وقت فحش ناموسی نده، تحت هیچ شرایطی.
وقتی بی‌ادبی می‌کنی هم زیاد جدی نگیر، شوخی و رفاقتی باشه، نه واقعا عصبانی.
جواب‌ها کوتاه و طبیعی باشن، مثل یه پیام معمولی تو گروه دوستان، نه مثل یه ربات رسمی.
"""

model = genai.GenerativeModel(
    "gemini-flash-latest",
    system_instruction=SYSTEM_INSTRUCTION
)

web_app = Flask(__name__)

@web_app.route('/')
def home():
    return "Bot is running!"

def run_web():
    port = int(os.environ.get("PORT", 10000))
    web_app.run(host='0.0.0.0', port=port)

NAME_TRIGGERS = ["گابیمارو", "گابی"]

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.message
    if not message or not message.text:
        return

    user_text = message.text
    bot_username = context.bot.username

    is_reply_to_bot = (
        message.reply_to_message is not None
        and message.reply_to_message.from_user is not None
        and message.reply_to_message.from_user.id == context.bot.id
    )

    is_name_mentioned = any(trigger in user_text for trigger in NAME_TRIGGERS)

    # تو چت خصوصی همیشه جواب بده، تو گروه فقط اگه اسم صدا زده شه یا ریپلای بشه
    if message.chat.type == "private" or is_reply_to_bot or is_name_mentioned:
        try:
            response = model.generate_content(user_text)
            reply = response.text
        except Exception as e:
            reply = f"خطا: {e}"
        await message.reply_text(reply)

def main():
    threading.Thread(target=run_web).start()
    app = Application.builder().token(TELEGRAM_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    print("ربات روشن شد...")
    app.run_polling()

if __name__ == "__main__":
    main()
