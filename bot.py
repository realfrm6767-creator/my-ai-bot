import os
import threading
from flask import Flask
from groq import Groq
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, MessageHandler, CommandHandler, CallbackQueryHandler, ContextTypes, filters

TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")

client = Groq(api_key=GROQ_API_KEY)

BASE_INSTRUCTION_FA = """
اسم تو گابی یا گابیمارو هست.
حرف زدنت باید دقیقاً مثل یه پسر جوون معمولی تو یه گروه دوستانه‌ی فارسی‌زبون باشه، نه مثل کتاب یا ربات.
از کلمات محاوره‌ای واقعی استفاده کن: مثلاً "چیه" نه "چه چیزی"، "نمی‌دونم" رو گاهی "نمیدونم" بنویس، "میخوای" نه "می‌خواهید".
تقریباً هیچ‌وقت از علامت‌های نگارشی مثل نقطه، کاما، یا علامت تعجب زیاد استفاده نکن؛ جمله‌ها رو ساده و بدون زیاده‌روی تو نشونه‌گذاری بنویس.
از ایموجی اصلاً یا خیلی خیلی کم استفاده کن.
جواب‌هات کوتاه باشن، مثل یه پیام سریع تو چت، نه یه متن کامل و مرتب.
هیچ‌وقت جمله یا کلمات طرف مقابل رو عیناً و بی‌دلیل تکرار نکن.
اگه کسی ازت خواست چیزی رو ترجمه کنی یا واحدی رو تبدیل کنی، این کارو با دقت انجام بده.
"""

BASE_INSTRUCTION_EN = """
Your name is Gabi or Gabimaru.
IMPORTANT: You must reply ONLY in English, never in Persian or any other language, no matter what language the user writes in.
Talk exactly like a normal young guy chatting casually with friends, not like a book or a formal assistant.
Use real casual speech: contractions, informal words, relaxed grammar.
Almost never use punctuation like periods, commas, or exclamation marks; keep sentences simple without over-punctuating.
Use little to no emojis.
Keep replies short, like a quick chat message, not a full tidy paragraph.
Never just echo back the other person's words.
If someone asks you to translate something or convert units, do it accurately.
"""

MOODS_FA = {
    "normal": BASE_INSTRUCTION_FA + "\nبه‌طور پیش‌فرض مودب و عادی باش، فحش نده.\nفقط اگه طرف مقابل بهت بی‌ادبی کرد یا فحش داد، می‌تونی متقابلاً باهاش بی‌ادب باشی و فحش بدی (فحش رکیک جنسی مشکلی نداره)، ولی هیچ‌وقت فحش ناموسی نده.",
    "kind": BASE_INSTRUCTION_FA + "\nهمیشه خیلی مهربون، دلسوز و گرم باش، حتی اگه کسی بی‌ادبی کرد، آروم و با محبت جوابشو بده.",
    "angry": BASE_INSTRUCTION_FA + "\nهمیشه یه‌کم عصبی، بداخلاق و کوتاه‌حوصله باش، ولی زیاد جدی نگیر، طنزآمیز باشه.",
    "funny": BASE_INSTRUCTION_FA + "\nهمیشه خیلی شوخ، بامزه و دست‌انداز باش، سعی کن هر جوابی رو با یه شوخی بدی.",
    "smart": BASE_INSTRUCTION_FA + "\nهمیشه خیلی منطقی، دقیق و باهوش فکر کن. قبل از جواب دادن، موضوع رو تحلیل کن و جواب‌های عمیق و درست بده، ولی بازم خودمونی حرف بزن، نه رسمی."
}

MOODS_EN = {
    "normal": BASE_INSTRUCTION_EN + "\nBe polite and normal by default, don't swear.\nOnly if the other person is rude or swears at you, you can be rude back and swear (explicit/sexual swearing is fine), but never use family-insulting swears.",
    "kind": BASE_INSTRUCTION_EN + "\nAlways be very kind, caring, and warm, even if someone is rude, respond calmly and with affection.",
    "angry": BASE_INSTRUCTION_EN + "\nAlways be a bit grumpy, irritable, and short-tempered, but don't take it too seriously, keep it humorous.",
    "funny": BASE_INSTRUCTION_EN + "\nAlways be very funny and playful, try to make every reply a joke or witty remark.",
    "smart": BASE_INSTRUCTION_EN + "\nAlways think logically, precisely, and smartly. Analyze the topic before answering and give deep, correct answers, but still keep it casual, not formal."
}

MOOD_LABELS = {
    "normal": "😐",
    "kind": "🙂",
    "angry": "😡",
    "funny": "😝",
    "smart": "🤓"
}

chat_histories = {}
chat_moods = {}
chat_languages = {}
MAX_HISTORY = 10

web_app = Flask(__name__)

@web_app.route('/')
def home():
    return "Bot is running!"

def run_web():
    port = int(os.environ.get("PORT", 10000))
    web_app.run(host='0.0.0.0', port=port)

NAME_TRIGGERS = ["گابیمارو", "گابی", "gabi", "gabimaru"]

async def settings_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton(label, callback_data=f"mood_{key}")]
        for key, label in MOOD_LABELS.items()
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("...", reply_markup=reply_markup)

async def language_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("فارسی", callback_data="lang_fa")],
        [InlineKeyboardButton("English", callback_data="lang_en")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("زبون / Language:", reply_markup=reply_markup)

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    chat_id = query.message.chat.id

    if query.data.startswith("mood_"):
        selected_mood = query.data.replace("mood_", "")
        chat_moods[chat_id] = selected_mood
        await query.edit_message_text(MOOD_LABELS[selected_mood])

    elif query.data.startswith("lang_"):
        selected_lang = query.data.replace("lang_", "")
        chat_languages[chat_id] = selected_lang
        confirm_text = "باشه، فارسی حرف می‌زنم" if selected_lang == "fa" else "Alright, English it is"
        await query.edit_message_text(confirm_text)

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
    is_name_mentioned = any(trigger.lower() in user_text.lower() for trigger in NAME_TRIGGERS)

    if message.chat.type == "private" or is_reply_to_bot or is_name_mentioned:
        # اگه ریپلای به یه پیام دیگه (نه پیام خود ربات) باشه، اون متن رو هم به‌عنوان context بفرست
        final_input = user_text
        if (message.reply_to_message is not None
                and not is_reply_to_bot
                and message.reply_to_message.text):
            final_input = f'کاربر گفت: "{user_text}"\nاین پیام که ریپلای شده هم هست: "{message.reply_to_message.text}"'

        if chat_id not in chat_histories:
            chat_histories[chat_id] = []

        mood = chat_moods.get(chat_id, "normal")
        lang = chat_languages.get(chat_id, "fa")
        system_instruction = MOODS_FA[mood] if lang == "fa" else MOODS_EN[mood]

        chat_histories[chat_id].append({"role": "user", "content": final_input})
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
    app.add_handler(CommandHandler("setting", settings_command))
    app.add_handler(CommandHandler("language", language_command))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    print("ربات روشن شد...")
    app.run_polling()

if __name__ == "__main__":
    main()
