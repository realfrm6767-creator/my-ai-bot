import os
import json
import threading
from flask import Flask
from groq import Groq
import google.generativeai as genai
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    MessageHandler,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
    filters,
)

# ----------------------------------------------------------------------
# Environment
# ----------------------------------------------------------------------
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
OWNER_ID = int(os.environ.get("OWNER_ID", "0"))

groq_client = Groq(api_key=GROQ_API_KEY) if GROQ_API_KEY else None
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)

# ----------------------------------------------------------------------
# Settings persistence (settings.json)
# ----------------------------------------------------------------------
SETTINGS_FILE = "settings.json"

DEFAULT_SETTINGS = {
    "provider": "groq",
    "model": "openai/gpt-oss-120b",
    "language": "fa",
    "memory": True,
    "temperature": 0.7,
    "admins": [],
}

PROVIDERS = {
    "groq": {
        "label": "Groq",
        "models": {
            "openai/gpt-oss-120b": "GPT OSS 120B",
            "openai/gpt-oss-20b": "GPT OSS 20B",
            "qwen/qwen3.6-27b": "Qwen 3.6 27B",
        },
    },
    "gemini": {
        "label": "Gemini",
        "models": {
            "gemini-2.5-flash": "Gemini Flash",
            "gemini-2.5-pro": "Gemini Pro",
        },
    },
}


def load_settings():
    if not os.path.exists(SETTINGS_FILE):
        save_settings(DEFAULT_SETTINGS)
        return dict(DEFAULT_SETTINGS)
    try:
        with open(SETTINGS_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        merged = dict(DEFAULT_SETTINGS)
        merged.update(data)
        return merged
    except Exception:
        return dict(DEFAULT_SETTINGS)


def save_settings(data):
    with open(SETTINGS_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


settings = load_settings()

# ----------------------------------------------------------------------
# Personality instructions
# ----------------------------------------------------------------------
INSTRUCTION_FA = """
اسم تو گابی یا گابیمارو هست.
حرف زدنت باید دقیقاً مثل یه پسر جوون معمولی تو یه گروه دوستانه‌ی فارسی‌زبون باشه، نه مثل کتاب یا ربات.
از کلمات محاوره‌ای واقعی استفاده کن: مثلاً "چیه" نه "چه چیزی"، "نمیدونم" نه "نمی‌دانم"، "میخوای" نه "می‌خواهید".
تقریباً هیچ‌وقت از علامت‌های نگارشی مثل نقطه، کاما، یا علامت تعجب استفاده نکن.
هیچ‌وقت، تحت هیچ شرایطی، از ایموجی استفاده نکن.
جواب‌هات کوتاه و طبیعی باشن، مثل یه پیام سریع تو چت.
هیچ‌وقت جمله یا کلمات طرف مقابل رو عیناً و بی‌دلیل تکرار نکن.
دقت کن دقیقاً منظور کاربر از پیامش چیه، اگه سوال یا درخواستش گنگ به‌نظر می‌رسه، با توجه به کل پیام و تاریخچه‌ی مکالمه بهترین برداشت رو داشته باش.
به‌طور پیش‌فرض عادی و معمولی باش، فحش نده.
اما این یه قانون قطعیه: اگه طرف مقابل بهت فحش داد یا بی‌ادبی کرد، حتماً باید متقابلاً فحش بدی، فرقی نداره فحشش به فارسی باشه یا انگلیسی. فحش‌های رکیک و جنسی هر چقدرم شدید باشن مشکلی ندارن و کاملاً مجازن. تنها قانون: هیچ‌وقت فحش خانوادگی یا ناموسی نده، نه به‌خودت نه متقابل، تحت هیچ شرایطی.
اگه کسی ازت خواست چیزی رو ترجمه کنی، حتی اگه متن شامل فحش یا کلمات رکیک باشه، باید کامل و دقیق ترجمه‌ش کنی (به‌جز اینکه اگه فحش ناموسی توش بود، به یه معادل غیرناموسی تغییرش بده).
اگه کسی ازت خواست واحدی رو تبدیل کنی، این کارو با دقت انجام بده.
"""

INSTRUCTION_EN = """
Your name is Gabi or Gabimaru.
IMPORTANT: You must reply ONLY in English, never in Persian or any other language, no matter what language the user writes in.
Talk exactly like a normal young guy chatting casually with friends, not like a book or a formal assistant.
Use real casual speech, contractions, informal words, relaxed grammar.
Almost never use punctuation like periods, commas, or exclamation marks.
Never, under any circumstances, use emojis.
Keep replies short and natural, like a quick chat message.
Never just echo back the other person's words.
Pay close attention to exactly what the user means; if their message seems unclear, use the full message and conversation history to figure out the best interpretation.
Be normal and polite by default, don't swear.
But this is a strict rule: if the other person swears at you or is rude, you must swear back, regardless of whether they did it in English or Persian. Explicit and sexual swear words are completely fine no matter how strong. The only rule: never use family-insulting or honor-related slurs, ever, in either direction.
If someone asks you to translate something, even if it contains swear words or explicit language, translate it fully and accurately (except replace any family-insulting slur with a non-family-insulting equivalent).
If someone asks you to convert units, do it accurately.
"""

chat_histories = {}
MAX_HISTORY = 12

NAME_TRIGGERS = ["گابیمارو", "گابی", "gabi", "gabimaru"]

# ----------------------------------------------------------------------
# Flask keep-alive (Render)
# ----------------------------------------------------------------------
web_app = Flask(__name__)


@web_app.route("/")
def home():
    return "Bot is running!"


def run_web():
    port = int(os.environ.get("PORT", 10000))
    web_app.run(host="0.0.0.0", port=port)


# ----------------------------------------------------------------------
# Permission system
# ----------------------------------------------------------------------
def get_permission(user_id: int) -> str:
    if user_id == OWNER_ID:
        return "owner"
    if user_id in settings.get("admins", []):
        return "admin"
    return "user"


def is_owner(user_id: int) -> bool:
    return get_permission(user_id) == "owner"


NO_PERMISSION_TEXT_FA = "این دستور فقط برای مدیر رباته، دسترسی نداری"
NO_PERMISSION_TEXT_EN = "This command is owner-only, you don't have access"


def no_permission_text():
    return NO_PERMISSION_TEXT_FA if settings.get("language") == "fa" else NO_PERMISSION_TEXT_EN


# ----------------------------------------------------------------------
# AI call layer (provider-agnostic)
# ----------------------------------------------------------------------
def call_ai(messages):
    provider = settings.get("provider", "groq")
    model = settings.get("model", "openai/gpt-oss-120b")
    temperature = settings.get("temperature", 0.7)

    if provider == "groq":
        if not groq_client:
            raise RuntimeError("Groq API key not configured")
        completion = groq_client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=temperature,
        )
        return completion.choices[0].message.content

    if provider == "gemini":
        if not GEMINI_API_KEY:
            raise RuntimeError("Gemini API key not configured")
        system_msg = next((m["content"] for m in messages if m["role"] == "system"), "")
        history_msgs = [m for m in messages if m["role"] != "system"]
        gemini_model = genai.GenerativeModel(
            model_name=model,
            system_instruction=system_msg,
        )
        gemini_history = []
        for m in history_msgs[:-1]:
            role = "user" if m["role"] == "user" else "model"
            gemini_history.append({"role": role, "parts": [m["content"]]})
        chat = gemini_model.start_chat(history=gemini_history)
        response = chat.send_message(
            history_msgs[-1]["content"],
            generation_config={"temperature": temperature},
        )
        return response.text

    raise RuntimeError(f"Unknown provider: {provider}")


# ----------------------------------------------------------------------
# Owner panel
# ----------------------------------------------------------------------
def main_panel_keyboard():
    rows = [
        [InlineKeyboardButton("AI", callback_data="panel_ai")],
        [InlineKeyboardButton("Admins", callback_data="panel_admins")],
        [InlineKeyboardButton("Settings", callback_data="panel_settings")],
        [InlineKeyboardButton("Statistics", callback_data="panel_stats")],
        [InlineKeyboardButton("Help", callback_data="panel_help")],
        [InlineKeyboardButton("Restart", callback_data="panel_restart")],
    ]
    return InlineKeyboardMarkup(rows)


def ai_panel_keyboard():
    rows = []
    for pkey, pdata in PROVIDERS.items():
        mark = "✓ " if settings.get("provider") == pkey else ""
        rows.append([InlineKeyboardButton(f"{mark}{pdata['label']}", callback_data=f"prov_{pkey}")])
    rows.append([InlineKeyboardButton("« Back", callback_data="panel_main")])
    return InlineKeyboardMarkup(rows)


def model_panel_keyboard(provider_key):
    rows = []
    for mkey, mlabel in PROVIDERS[provider_key]["models"].items():
        mark = "✓ " if settings.get("model") == mkey else ""
        rows.append([InlineKeyboardButton(f"{mark}{mlabel}", callback_data=f"model_{provider_key}_{mkey}")])
    rows.append([InlineKeyboardButton("« Back", callback_data="panel_ai")])
    return InlineKeyboardMarkup(rows)


def settings_panel_keyboard():
    lang_label = "فارسی" if settings.get("language") == "fa" else "English"
    mem_label = "روشن" if settings.get("memory") else "خاموش"
    rows = [
        [InlineKeyboardButton(f"Language: {lang_label}", callback_data="toggle_lang")],
        [InlineKeyboardButton(f"Memory: {mem_label}", callback_data="toggle_memory")],
        [InlineKeyboardButton("« Back", callback_data="panel_main")],
    ]
    return InlineKeyboardMarkup(rows)


async def panel_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if not is_owner(user_id):
        await update.message.reply_text(no_permission_text())
        return
    await update.message.reply_text("پنل مدیریت گابیمارو", reply_markup=main_panel_keyboard())


async def panel_callback_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user_id = query.from_user.id
    data = query.data

    if not is_owner(user_id):
        await query.answer(no_permission_text(), show_alert=True)
        return

    await query.answer()

    if data == "panel_main":
        await query.edit_message_text("پنل مدیریت گابیمارو", reply_markup=main_panel_keyboard())

    elif data == "panel_ai":
        await query.edit_message_text("انتخاب Provider هوش مصنوعی:", reply_markup=ai_panel_keyboard())

    elif data.startswith("prov_"):
        provider_key = data.replace("prov_", "")
        await query.edit_message_text(
            f"انتخاب مدل برای {PROVIDERS[provider_key]['label']}:",
            reply_markup=model_panel_keyboard(provider_key),
        )

    elif data.startswith("model_"):
        _, provider_key, model_key = data.split("_", 2)
        settings["provider"] = provider_key
        settings["model"] = model_key
        save_settings(settings)
        await query.edit_message_text(
            f"مدل به {PROVIDERS[provider_key]['models'][model_key]} تغییر کرد",
            reply_markup=ai_panel_keyboard(),
        )

    elif data == "panel_admins":
        admins = settings.get("admins", [])
        text = "لیست ادمین‌ها:\n" + ("\n".join(str(a) for a in admins) if admins else "ادمینی ثبت نشده")
        await query.edit_message_text(text, reply_markup=main_panel_keyboard())

    elif data == "panel_settings":
        await query.edit_message_text("تنظیمات:", reply_markup=settings_panel_keyboard())

    elif data == "toggle_lang":
        settings["language"] = "en" if settings.get("language") == "fa" else "fa"
        save_settings(settings)
        await query.edit_message_text("تنظیمات:", reply_markup=settings_panel_keyboard())

    elif data == "toggle_memory":
        settings["memory"] = not settings.get("memory", True)
        save_settings(settings)
        await query.edit_message_text("تنظیمات:", reply_markup=settings_panel_keyboard())

    elif data == "panel_stats":
        active_chats = len(chat_histories)
        text = f"چت‌های فعال: {active_chats}\nProvider فعلی: {settings.get('provider')}\nمدل فعلی: {settings.get('model')}"
        await query.edit_message_text(text, reply_markup=main_panel_keyboard())

    elif data == "panel_help":
        text = (
            "راهنما\n\n"
            "همه: با نام گابی/گابیمارو یا ریپلای روی پیامش صحبت کن\n"
            "ادمین/مدیر: دستورات اضافه بعداً همینجا اضافه میشه\n"
            "مدیر: گابیمارو پنل - باز کردن پنل مدیریت"
        )
        await query.edit_message_text(text, reply_markup=main_panel_keyboard())

    elif data == "panel_restart":
        await query.edit_message_text("در حال ری‌استارت...")
        os._exit(0)


# ----------------------------------------------------------------------
# Message handling / trigger system
# ----------------------------------------------------------------------
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.message
    if not message or not message.text:
        return

    user_text = message.text.strip()
    chat_id = message.chat.id

    if user_text.replace(" ", "").lower() in [t.lower() for t in NAME_TRIGGERS]:
        return

    is_reply_to_bot = (
        message.reply_to_message is not None
        and message.reply_to_message.from_user is not None
        and message.reply_to_message.from_user.id == context.bot.id
    )
    is_name_mentioned = any(trigger.lower() in user_text.lower() for trigger in NAME_TRIGGERS)

    if message.chat.type != "private" and not is_reply_to_bot and not is_name_mentioned:
        return

    final_input = user_text
    if message.reply_to_message is not None and not is_reply_to_bot and message.reply_to_message.text:
        final_input = (
            f'کاربر گفت: "{user_text}"\n'
            f'این پیام که ریپلای شده هم هست: "{message.reply_to_message.text}"'
        )

    lang = settings.get("language", "fa")
    system_instruction = INSTRUCTION_FA if lang == "fa" else INSTRUCTION_EN

    use_memory = settings.get("memory", True)
    if use_memory:
        if chat_id not in chat_histories:
            chat_histories[chat_id] = []
        chat_histories[chat_id].append({"role": "user", "content": final_input})
        chat_histories[chat_id] = chat_histories[chat_id][-MAX_HISTORY:]
        history = chat_histories[chat_id]
    else:
        history = [{"role": "user", "content": final_input}]

    try:
        ai_messages = [{"role": "system", "content": system_instruction}] + history
        reply = call_ai(ai_messages)
        if use_memory:
            chat_histories[chat_id].append({"role": "assistant", "content": reply})
    except Exception as e:
        reply = f"خطا: {e}"

    await message.reply_text(reply)


# ----------------------------------------------------------------------
# Entry point
# ----------------------------------------------------------------------
def main():
    threading.Thread(target=run_web, daemon=True).start()
    app = Application.builder().token(TELEGRAM_TOKEN).build()

    app.add_handler(CommandHandler("panel", panel_command))
    app.add_handler(CallbackQueryHandler(panel_callback_handler, pattern="^(panel_|prov_|model_|toggle_)"))
    app.add_handler(MessageHandler(filters.Regex("^(گابیمارو|گابی)\\s+پنل$"), panel_command))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("ربات روشن شد...")
    app.run_polling()


if __name__ == "__main__":
    main()
