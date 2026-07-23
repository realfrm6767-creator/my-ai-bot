"""
ai.py
-----
اتصال به سرویس هوش مصنوعی (Groq) و تولید پاسخ.

قابلیت‌هایی که در مرحله پنجم پیاده‌سازی می‌شوند:
    - generate_response(user_id, message, language)
    - انتخاب خودکار Prompt فارسی/انگلیسی
    - اتصال به memory.py

بعداً پروایدرهای دیگر (OpenRouter, Gemini, OpenAI, Claude) از طریق
پوشه providers/ اضافه می‌شوند.
"""