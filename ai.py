import os
import datetime

from groq import Groq


GROQ_API_KEY = os.getenv("GROQ_API_KEY")


client = Groq(
    api_key=GROQ_API_KEY
)


MAX_HISTORY = 14


chat_histories = {}

chat_languages = {}

NAME_TRIGGERS = [
    "گابیمارو",
    "گابی",
    "gabimaru",
    "gabi"
]


def current_time():

    return datetime.datetime.now().strftime(
        "%Y-%m-%d %H:%M"
    )


def build_instruction_fa():

    now = current_time()

    return f"""
اسم تو گابی یا گابیمارو هست

الان تاریخ و ساعت
{now}

مثل یه پسر جوون واقعی حرف بزن

هیچوقت رسمی نباش

ایموجی استفاده نکن

تقریبا هیچوقت از نقطه و کاما استفاده نکن

جواب ها کوتاه باشن

از تکرار حرف کاربر خودداری کن

اگر طرف فحش داد میتونی جوابشو بدی ولی هیچوقت فحش خانوادگی نده

اگر کاربر درخواست ترجمه کرد کامل ترجمه کن

اگر درخواست محاسبه داشت دقیق انجام بده

اگر پیام ریپلای بود باید به متن ریپلای هم توجه کنی

هیچوقت نگو
متاسفم
نمیتونم
قادر نیستم

همیشه یه جواب طبیعی بده
"""


def build_instruction_en():

    now = current_time()

    return f"""
Your name is Gabi

Current time

{now}

Reply only in English

Talk like a normal young guy

Never be formal

Never use emojis

Keep replies short

Avoid repeating user words

If the user is rude you may answer rudely but never use family insults

Translate everything correctly

Never refuse requests with phrases like

I can't

I'm sorry

Always answer naturally
"""

class HistoryManager:

    @staticmethod
    def get(user_id):

        if user_id not in chat_histories:

            chat_histories[user_id] = []

        return chat_histories[user_id]

    @staticmethod
    def clear(user_id):

        chat_histories[user_id] = []

    @staticmethod
    def add(user_id, role, content):

        history = HistoryManager.get(user_id)

        history.append(
            {
                "role": role,
                "content": content
            }
        )

        if len(history) > MAX_HISTORY:

            history.pop(0)

    @staticmethod
    def export(user_id):

        return list(
            HistoryManager.get(user_id)
        )


class LanguageManager:

    @staticmethod
    def get(user_id):

        if user_id not in chat_languages:

            chat_languages[user_id] = "fa"

        return chat_languages[user_id]

    @staticmethod
    def set(user_id, language):

        chat_languages[user_id] = language

    @staticmethod
    def auto_detect(text):

        english = 0

        for ch in text:

            if "a" <= ch.lower() <= "z":

                english += 1

        if english >= 5:

            return "en"

        return "fa"

class PromptManager:

    @staticmethod
    def build(user_id):

        language = LanguageManager.get(user_id)

        if language == "fa":

            system = build_instruction_fa()

        else:

            system = build_instruction_en()

        messages = [

            {

                "role": "system",

                "content": system

            }

        ]

        messages.extend(

            HistoryManager.export(user_id)

        )

        return messages


class GroqManager:

    @staticmethod
    def chat(user_id, message):

        language = LanguageManager.auto_detect(message)

        LanguageManager.set(user_id, language)

        HistoryManager.add(

            user_id,

            "user",

            message

        )

        messages = PromptManager.build(user_id)

        response = client.chat.completions.create(

            model="openai/gpt-oss-120b",

            messages=messages,

            temperature=0.8,

            max_completion_tokens=700

        )

        answer = response.choices[0].message.content.strip()

        HistoryManager.add(

            user_id,

            "assistant",

            answer

        )

        return answer

async def ask_ai(user_id, text):

    try:

        answer = GroqManager.chat(
            user_id,
            text
        )

        return answer

    except Exception as e:

        print(e)

        return (
            "❌ ارتباط با هوش مصنوعی برقرار نشد"
        )