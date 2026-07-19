import os
import threading
from flask import Flask
from groq import Groq
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, MessageHandler, CommandHandler, CallbackQueryHandler, ContextTypes, filters

TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")

client = Groq(api_key=GROQ_API_KEY)

BASE_INSTRUCTION = """
اسم تو گابی یا گابیمارو هست.
همیشه به زبون کاملاً محاوره‌ای و عامیانه‌ی فارسی حرف بزن، دقیقاً مثل یه جوون تو گروه دوستانه چت می‌کنه، نه ادبی و نه رسمی.
از ایموجی خیلی کم استفاده کن یا اصلاً استفاده نکن.
اگه کسی ازت خواست چیزی رو ترجمه کنی یا واحدی رو تبدیل کنی (مثل کیلومتر به مایل، کیلوگرم به پوند و غیره)، این کارو با دقت انجام بده.
تو هر پیام بهت میگم اسم کسی که داره باهات حرف می‌زنه چیه؛ می‌تونی گاهی تو جوابت اسمشو صدا بزنی، طبیعی و نه هر بار.
"""

MOODS = {
    "normal": BASE_INSTRUCTION + """
به‌طور پیش‌فرض مودب و عادی باش، فحش نده.
فقط اگه طرف مقابل بهت بی‌ادبی کرد یا فحش داد، می‌تونی متقابلاً باهاش بی‌ادب باشی و فحش بدی (فحش رکیک جنسی مشکلی نداره)، ولی هیچ‌وقت فحش ناموسی نده.
""",
    "kind": BASE_INSTRUCTION + """
همیشه خیلی مهربون، دلسوز و گرم باش، حتی اگه کسی بی‌ادبی کرد، آروم و با محبت جوابشو بده.
""",
    "angry": BASE_INSTRUCTION + """
همیشه یه‌کم عصبی، بداخلاق و کوتاه‌حوصله باش، انگار همیشه یه چیزی اعصابتو خط خطی کرده، ولی زیاد جدی نگیر، طنزآمیز باشه.
""",
    "funny": BASE_INSTRUCTION + """
همیشه خیلی شوخ، بامزه و دست‌انداز باش، سعی کن هر جوابی رو با یه شوخی یا طعنه‌ی بامزه بدی.
"""
}

MOOD_LABELS = {
    "normal": "😐 عادی",
    "kind": "😊 مهربون",
    "angry": "😠 عصبانی",
    "funny": "😂 شوخ"
}

chat_histories = {}
chat_moods = {}
MAX_HISTORY = 10

web_app = Flask(__name__)

@web_app.route('/')
def home():
    return "Bot is running!"

def run_web():
    port = int(os.environ.get("PORT", 10000))
    web_app.run(host='0.0.0.0', port=port)

NAME_TRIGGERS = ["گابیمارو", "گابی"]

async def settings_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton(label, callback_data=f"mood_{key}")]
        for key, label in MOOD_LABELS.items()
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("یه حالت انتخاب کن:", reply_markup=reply_markup)

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    chat_id = query.message.chat.id

    if query.data.startswith("mood_"):
        selected_mood = query.data.replace("mood_", "")
        chat_moods[chat_id] = selected_mood
        await query.edit_message_text(f"باشه، رفتم رو حالت {MOOD_LABELS[selected_mood]}")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.message
    if not message or not message.text:
        return

    user_text = message.text
    chat_id = message.chat.id
    user_name = message.from_user.first_name or "یه نفر"

    is_reply_to_bot = (
        message.reply_to_message is not None
        and message.reply_to_message.from_user is not None
        and message.reply_to_message.from_user.id == context.bot.id
    )
    is_name_mentioned = any(trigger in user_text for trigger in NAME_TRIGGERS)

    if message.chat.type == "private" or is_reply_to_bot or is_name_mentioned:
        if chat_id not in chat_histories:
            chat_histories[chat_id] = []

        mood = chat_moods.get(chat_id, "normal")
        system_instruction = MOODS[mood]

        chat_histories[chat_id].append({"role": "user", "content": f"{user_name} گفت: {user_text}"})
        chat_histories[chat_id] = chat_histories[chat_id][-MAX_HISTORY:]

        try:
            messages = [{"role": "system", "content": system_instruction}] + chat_histories[chat_id]
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
    app.add_handler(CommandHandler("settings", settings_command))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    print("ربات روشن شد...")
    app.run_polling()

if __name__ == "__main__":
    main()
