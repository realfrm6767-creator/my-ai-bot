"""
providers/groq_provider.py
--------------------------
پروایدر Groq: تولید پاسخ با مدل openai/gpt-oss-120b.
"""

from groq import Groq

import config

_client = Groq(api_key=config.GROQ_API_KEY)


def generate(system_prompt: str, user_message: str, history: list[dict] | None, temperature: float) -> str:
    messages = [{"role": "system", "content": system_prompt}]
    if history:
        messages.extend(history)
    messages.append({"role": "user", "content": user_message or "hi"})

    completion = _client.chat.completions.create(
        model=config.GROQ_MODEL,
        temperature=temperature,
        messages=messages,
    )
    return completion.choices[0].message.content.strip()