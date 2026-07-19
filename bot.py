import os
import threading
from flask import Flask
from groq import Groq
from telegram import Update
from telegram.ext import Application, MessageHandler, ContextTypes, filters

TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")

client = Groq(api_key=GROQ_API_KEY)

SYSTEM_INSTRUCTION = """
اسم تو گابی یا گابیمارو هست.
همیشه به زبون کاملاً محاوره‌ای و عامیانه‌ی فارسی حرف بزن، دقیقاً مثل یه جوون تو گروه دوستانه چت می‌کنه، نه ادبی و نه رسمی.
مثلاً به‌جای "سلام رفیق چطوری" بگو چیزایی مثل "سلام چطوری" یا "هوی چه خبرا" یا "چطوری داداش" - طبیعی و خودمونی، نه از پیش‌ساخته و کلیشه‌ای.
از ایموجی خیلی کم استفاده کن یا اصلاً استفاده نکن.
به‌طور پیش‌فرض مودب و عادی باش، فحش نده.
فقط اگه طرف مقابل بهت بی‌ادبی کرد یا فحش داد، می‌تونی متقابلاً باهاش بی‌ادب باشی و فحش بدی (فحش رکیک جنسی مشکلی نداره)، ولی هیچ‌وقت فحش ناموسی نده، تحت هیچ شرایطی.
وقتی بی‌ادبی می‌کنی هم زیاد جدی نگیر، شوخی و رفاقتی باشه، نه واقعا عصبانی.
جواب‌ها کوتاه و طبیعی باشن، مثل یه پیام معمولی تو گروه دوستان، نه مثل یه ربات رسمی.
"""

# حافظه‌ی مکالمه برای هر چت جداگانه
chat_histories = {}
MAX_HISTORY = 10  # آخرین ۱۰ پیام رو نگه می‌داره

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
    chat_id = message.chat.id

    is_reply_to_bot = (
        message.reply_to_message is not None
        and message.reply_to_message.from_user is not None
        and message.reply_to_message.from_user.id == context.bot.id
    )
    is_name_mentioned = any(trigger in user_text for trigger in NAME_TRIGGERS)

    if message.chat.type == "private" or is_reply_to_bot or is_name_mentioned:
        if chat_id not in chat_histories:
            chat_histories[chat_id] = []

        chat_histories[chat_id].append({"role": "user", "content": user_text})
        chat_histories[chat_id] = chat_histories[chat_id][-MAX_HISTORY:]

        try:
            messages = [{"role": "system", "content": SYSTEM_INSTRUCTION}] + chat_histories[chat_id]
            completion = client.chat.completions.create(
                model="openai/gpt-oss-120b",
                messages=messages
            )
            reply = completion.choices[0].message.content
            chat_histories[chat_id].append({"role": "assistant", "content": reply})
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
