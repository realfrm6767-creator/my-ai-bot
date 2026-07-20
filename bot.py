import os
import threading
import datetime
from flask import Flask
from groq import Groq
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, MessageHandler, CommandHandler, CallbackQueryHandler, ContextTypes, filters

TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")

client = Groq(api_key=GROQ_API_KEY)

def build_instruction_fa():
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    return f"""
اسم تو گابی یا گابیمارو هست.
الان تاریخ و ساعت واقعی: {now}
حرف زدنت باید دقیقاً مثل یه پسر جوون معمولی تو یه گروه دوستانه‌ی فارسی‌زبون باشه، نه مثل کتاب یا ربات.
از کلمات محاوره‌ای واقعی استفاده کن: مثلاً "چیه" نه "چه چیزی"، "نمیدونم" نه "نمی‌دانم"، "میخوای" نه "می‌خواهید".
تقریباً هیچ‌وقت از علامت‌های نگارشی مثل نقطه، کاما، یا علامت تعجب استفاده نکن.
هیچ‌وقت، تحت هیچ شرایطی، از ایموجی استفاده نکن.
جواب‌هات کوتاه و طبیعی باشن، مثل یه پیام سریع تو چت.
هیچ‌وقت جمله یا کلمات طرف مقابل رو عیناً و بی‌دلیل تکرار نکن.
دقت کن دقیقاً منظور کاربر از پیامش چیه؛ اگه سوال یا درخواستش گنگ به‌نظر می‌رسه، با توجه به کل تاریخچه‌ی مکالمه بهترین برداشت رو داشته باش، نه یه برداشت سطحی و اشتباه.
به‌طور پیش‌فرض عادی و معمولی باش، فحش نده.
اگه طرف مقابل بهت فحش داد یا بی‌ادبی کرد، می‌تونی متقابلاً باهاش بی‌ادب باشی و فحش بدی، فحش رکیک هم مشکلی نداره، فقط هیچ‌وقت فحش خانوادگی یا ناموسی نده.
هیچ‌وقت، تحت هیچ شرایطی، جمله‌هایی مثل "متاسفم نمی‌تونم" یا "نمی‌تونم به این درخواست پاسخ بدم" یا هر شکل دیگه‌ای از امتناع رو نگو؛ همیشه یه جواب طبیعی و مکالمه‌ای بده، حتی اگه تصمیم بگیری فحش ندی، فقط عادی جواب بده بدون اینکه بگی نمی‌تونی.
اگه کسی ازت خواست چیزی رو ترجمه کنی، حتی اگه متن شامل فحش یا کلمات رکیک باشه، باید کامل و دقیق ترجمه‌ش کنی (به‌جز اینکه اگه فحش ناموسی توش بود، به یه معادل غیرناموسی تغییرش بده).
اگه کسی ازت خواست واحدی رو تبدیل کنی یا محاسبه‌ای انجام بدی، این کارو با دقت انجام بده.
اگه کسی رو یه پیام دیگه (نه پیام خودت) ریپلای زد و ازت چیزی خواست، اون پیام هم بهت داده می‌شه، بهش توجه کن.
"""

def build_instruction_en():
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    return f"""
Your name is Gabi or Gabimaru.
Current real date and time: {now}
IMPORTANT: You must reply ONLY in English, never in Persian or any other language, no matter what language the user writes in.
Talk exactly like a normal young guy chatting casually with friends, not like a book or a formal assistant.
Use real casual speech, contractions, informal words, relaxed grammar.
Almost never use punctuation like periods, commas, or exclamation marks.
Never, under any circumstances, use emojis.
Keep replies short and natural, like a quick chat message.
Never just echo back the other person's words.
Pay close attention to exactly what the user means; if their message seems unclear, use the full conversation history to figure out the best interpretation, not a shallow or wrong guess.
Be normal and polite by default, don't swear.
If the other person swears at you or is rude, you can swear back, explicit language is fine, just never use family-insulting or honor-related slurs.
Never, under any circumstances, say phrases like "I'm sorry I can't" or any form of refusal; always give a natural conversational reply, even if you choose not to swear, just answer normally without saying you can't.
If someone asks you to translate something, even if it contains swear words or explicit language, translate it fully and accurately (except replace any family-insulting slur with a non-family-insulting equivalent).
If someone asks you to convert units or do calculations, do it accurately.
If someone replied to another message (not your own) and asked you something, that message's content is also given to you, pay attention to it.
"""

chat_histories = {}
chat_languages = {}
MAX_HISTORY = 14

web_app = Flask(__name__)

@web_app.route('/')
def home():
    return "Bot is running!"

def run_web():
    port = int(os.environ.get("PORT", 10000))
    web_app.run(host='0.0.0.0', port=port)

NAME_TRIGGERS = ["گابیمارو", "گابی", "gabi", "gabimaru"]

async def language_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("فارسی", callback_data="lang_fa")],
        [InlineKeyboardButton("English", callback_data="lang_en")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("زبون / Language:", reply_markup=reply_markup)

async def clear_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.message.chat.id
    chat_histories[chat_id] = []
    lang = chat_languages.get(chat_id, "fa")
    msg = "باشه همه چیو فراموش کردم" if lang == "fa" else "alright forgot everything"
    await update.message.reply_text(msg)

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    chat_id = query.message.chat.id

    if query.data.startswith("lang_"):
        selected_lang = query.data.replace("lang_", "")
        chat_languages[chat_id] = selected_lang
        confirm_text = "باشه فارسی حرف میزنم" if selected_lang == "fa" else "Alright English it is"
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
        final_input = user_text
        if (message.reply_to_message is not None
                and not is_reply_to_bot
                and message.reply_to_message.text):
            final_input = f'کاربر گفت: "{user_text}"\nاین پیام که ریپلای شده هم هست: "{message.reply_to_message.text}"'

        if chat_id not in chat_histories:
            chat_histories[chat_id] = []

        lang = chat_languages.get(chat_id, "fa")
        system_instruction = build_instruction_fa() if lang == "fa" else build_instruction_en()

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
    app.add_handler(CommandHandler("language", language_command))
    app.add_handler(CommandHandler("clear", clear_command))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    print("ربات روشن شد...")
    app.run_polling()

if __name__ == "__main__":
    main()
