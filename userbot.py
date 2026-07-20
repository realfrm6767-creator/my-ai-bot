import os
import asyncio
import threading
from flask import Flask
from telethon.sync import TelegramClient
from telethon.sessions import StringSession
from telethon import events

api_id = 34806713
api_hash = "57b940a7292f53fe93d2cccc7938d9b7"
SESSION_STRING = os.environ.get("SESSION_STRING")

web_app = Flask(__name__)

@web_app.route('/')
def home():
    return "Userbot is running!"

def run_web():
    port = int(os.environ.get("PORT", 10000))
    web_app.run(host='0.0.0.0', port=port)

client = TelegramClient(StringSession(SESSION_STRING), api_id, api_hash)

active_tasks = {}

async def repeat_sender(chat_id, word, interval):
    try:
        while True:
            await asyncio.sleep(interval)
            await client.send_message(chat_id, word)
    except asyncio.CancelledError:
        pass

@client.on(events.NewMessage(outgoing=True, pattern=r'^تنظیم (.+) (\d+)$'))
async def set_handler(event):
    word = event.pattern_match.group(1)
    seconds = int(event.pattern_match.group(2))
    chat_id = event.chat_id

    if chat_id in active_tasks:
        active_tasks[chat_id].cancel()

    task = asyncio.create_task(repeat_sender(chat_id, word, seconds))
    active_tasks[chat_id] = task

    await event.reply(f"باشه، هر {seconds} ثانیه یه‌بار می‌نویسم: {word}")

@client.on(events.NewMessage(outgoing=True, pattern=r'^لغو$'))
async def cancel_handler(event):
    chat_id = event.chat_id
    if chat_id in active_tasks:
        active_tasks[chat_id].cancel()
        del active_tasks[chat_id]
        await event.reply("باشه لغو شد")
    else:
        await event.reply("چیزی برای لغو کردن نیست")

async def main():
    await client.start()
    print("Userbot روشن شد...")
    await client.run_until_disconnected()

if __name__ == "__main__":
    threading.Thread(target=run_web).start()
    with client:
        client.loop.run_until_complete(main())
