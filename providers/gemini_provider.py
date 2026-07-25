"""
providers/gemini_provider.py
------------------------------
پروایدر Google Gemini (رایگان): تولید پاسخ با مدل gemini-2.0-flash.
"""

import google.generativeai as genai

import config

genai.configure(api_key=config.GEMINI_API_KEY)


def generate(system_prompt: str, user_message: str, history: list[dict] | None, temperature: float) -> str:
    model = genai.GenerativeModel(
        model_name=config.GEMINI_MODEL,
        system_instruction=system_prompt,
    )

    gemini_history = []
    if history:
        for msg in history:
            role = "user" if msg["role"] == "user" else "model"
            gemini_history.append({"role": role, "parts": [msg["content"]]})

    chat = model.start_chat(history=gemini_history)
    response = chat.send_message(
        user_message or "hi",
        generation_config={"temperature": temperature},
    )
    return response.text.strip()